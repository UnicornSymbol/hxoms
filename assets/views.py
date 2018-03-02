#coding: utf-8

import os
import json
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse,HttpResponseBadRequest,StreamingHttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain  #QuerySet合并
from assets.forms import IdcForm,ServerForm,SupplierForm,ServiceForm,RequisitionForm
from assets.models import Idc,Server,ServerInfo,Supplier,Type,Service,Requisition
from assets.tasks import *
from utils.common import *

# Create your views here.
@login_required
def idc_list(request):
    if request.method == 'POST':
        idc =  Idc()
        form = IdcForm(request.POST, instance=idc)
        if form.is_valid():
            #print(request.POST)
            form.save()
            return JsonResponse({"status": u"添加成功"})
        else:
            return JsonResponse({"status": u"添加失败", "msg": u"机房名字已存在"})
    idcs = Idc.objects.all()
    form = IdcForm()
    return render(request, 'idc_list.html', locals())

@login_required
def idc_operate(request,id):
    idc = get_object_or_404(Idc, pk=id)
    if request.method == 'DELETE':
        try:
            idc.delete()
        except ProtectedError:
            return JsonResponse({"status": u"删除失败", "msg": u"请确保没有服务器依赖于它"})
        return JsonResponse({"status": u"删除成功"})
    if request.method == 'POST':
        form = IdcForm(request.POST, instance=idc)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": u"更新成功"})
        else:
            return render(request, 'idc_operate.html', locals())
    form = IdcForm(instance=idc)
    return render(request, 'idc_operate.html', locals())

@login_required
def server_list(request):
    if request.method == 'POST':
        server = Server()
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            #print(request.POST)
            form.save()
            return JsonResponse({"status": u"添加成功"})
        else:
            return JsonResponse({"status": u"添加失败", "msg": u"IP已存在"})
    servers = Server.objects.all()
    form = ServerForm()
    return render(request, 'server_list.html', locals())

@login_required
def server_operate(request,id):
    server = get_object_or_404(Server, pk=id)
    refresh = request.GET.get('refresh',"")
    if refresh:
        refresh_alive(server)
        return JsonResponse({"status": u"刷新成功", "alive": server.alive})
    if request.method == 'DELETE':
        try:
            server.serverinfo.delete()
        except ObjectDoesNotExist:
            pass
        except ProtectedError:
            return JsonResponse({"status": u"删除失败", "msg": u"请确保没有虚拟机依赖于{}".format(server.ip)})
        #delete_key.delay(server.node_name)
        server.delete()
        return JsonResponse({"status": u"删除成功"})
    if request.method == 'POST':
        #print(request.POST)
        #create_date = request.POST.get('create_date')
        end_date = request.POST.get('end_date')
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            inst = form.save(commit=False)
            #if create_date:
            #    inst.create_date = datetime.datetime.strptime(create_date,"%Y-%m-%d")
            if end_date:
                inst.end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
            inst.save()
            return JsonResponse({"status": u"更新成功"})
        else:
            return JsonResponse({"status": u"更新失败", "msg": u"表单错误"})
    form = ServerForm(instance=server)
    return render(request, 'server_operate.html', locals())

@login_required
def server_detail(request,id):
    server = Server.objects.get(pk=id)
    try:
        serverinfo = server.serverinfo
    except ObjectDoesNotExist:
        serverinfo = ServerInfo()
    return render(request, 'server_detail.html', locals())

@login_required
def update_serverinfo(request):
    if request.method == 'GET':
        ip = request.GET.get('ip', "")
        flush = request.GET.get('flush', "")
        get_server = request.GET.get('get_server', "")
        hosts = [i['ip'] for i in Server.objects.filter(status=1).exclude(ip=ip).order_by('ip').values('ip')]
        if get_server and ip:
            return HttpResponse(json.dumps(hosts))
        if flush and ip:
            ser = Server.objects.get(ip=ip)
            get_server_info(ser)
            return JsonResponse({"status": u"更新成功"})
    if request.method == 'POST':
        ip = request.POST.get('ip')
        value = request.POST.get('value')
        hosts = [i['ip'] for i in Server.objects.filter(status=1).exclude(ip=ip).order_by('ip').values('ip')]
        ser = Server.objects.get(ip=ip)
        try:
            serverinfo = ser.serverinfo  #本机info
            vm = hosts[int(value)]
            #print(vm)
            serverinfo.vm = ServerInfo.objects.get(ip=Server.objects.get(ip=vm))  #宿主机info
            serverinfo.save()
            return HttpResponse(vm)
        except ObjectDoesNotExist:
            return HttpResponse(u"请先获取本机或宿主机服务器信息...")
    raise Http404

@login_required
def status_change(request,sid,status):
    #print status,type(status)
    asset_type = request.GET.get('asset_type')
    if sid:
        if asset_type == "server":
            ser = get_object_or_404(Server, id=sid)
        elif asset_type == "service":
            ser = get_object_or_404(Service, id=sid)
        else:
            return JsonResponse({"status": u"更改失败", "msg": u"错误的资产类型"})
        if status in ["1","2"]:
            if asset_type == "server" and status == "2":
                try:
                    ser.serverinfo.delete()
                except ObjectDoesNotExist:
                    pass
                except ProtectedError:
                    return JsonResponse({"status": u"更改失败", "msg": u"请确保没有虚拟机依赖于{}".format(ser.ip)})
                #delete_key.delay(ser.node_name)
                ser.node_name = None
                ser.alive = False
            ser.status = status
            ser.save()
            return JsonResponse({"status": u"更改成功"})
        else:
            return JsonResponse({"status": u"更改失败", "msg": u"错误的状态值"})

@login_required
def contract_download(request,id):
    sup = get_object_or_404(Supplier, pk=id)
    filename=sup.contract.path    #要下载的文件路径  
    the_file_name=os.path.basename(filename)             #显示在弹出对话框中的默认的下载文件名      
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(file_iterator(filename))
    # 不加这两行文件流通常会以乱码形式显示到浏览器中，而非下载到硬盘上
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

@login_required
def supplier_list(request):
    if request.method == 'POST':
        #print(request.POST)
        #print(request.FILES)
        """contract = request.FILES.get('contract',None)
        contract_path = 'media/contract/{}'.format(request.POST.get('name'))
        if not os.path.exists(contract_path):
            os.makedirs(contract_path)
        if contract:
            with open(os.path.join(contract_path,contract.name),'wb+') as destination:  
                for chunk in contract.chunks():  
                    destination.write(chunk)"""
        supplier = Supplier()
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": u"添加成功"})
        else:
            return JsonResponse({"status": u"添加失败", "msg": u"供应商已存在"})
    suppliers = Supplier.objects.all()
    form_sup = SupplierForm()
    return render(request, 'supplier_list.html', locals())

@login_required
def supplier_operate(request, id=None):
    sup = get_object_or_404(Supplier, id=id)
    file_path = None
    if request.method == 'DELETE':
        try:
            if sup.contract:
                file_path = sup.contract.path
            sup.delete()
        except ProtectedError:
            return JsonResponse({"status": u"删除失败", "msg": u"请确保没有服务依赖于它"})
        else:
            if file_path:
                os.remove(file_path)
                os.rmdir(os.path.dirname(file_path))
        return JsonResponse({"status": u"删除成功"})
    if request.method == 'POST':
        if request.FILES.get('contract'):
            if sup.contract:
                file_path = sup.contract.path
            if file_path:
                os.remove(file_path)
                os.rmdir(os.path.dirname(file_path))
        form = SupplierForm(request.POST, request.FILES, instance=sup)
        if form.is_valid():
            form.save()
            #print sup.id,sup.name
            return JsonResponse({"status": u"更新成功", "id": sup.id})
        else:
            #print(form.cleaned_data)
            return JsonResponse({"status": u"更新失败", "msg": u"供应商已存在"})
    form = SupplierForm(instance=sup)
    return render(request, 'supplier_operate.html', locals())
    #return HttpResponseBadRequest("Bad Request")

@login_required
def service_list(request):
    #print(request.POST)
    type = request.POST.get('type')
    if request.method == 'POST':
        obj,created = Type.objects.get_or_create(name=type)
        service = Service()
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.type = obj
            inst.save()
            return JsonResponse({"status": u"添加成功"})
        else:
            return JsonResponse({"status": u"添加失败", "msg": u"服务名称已存在"})
    types = Type.objects.all()
    #suppliers = Supplier.objects.all()
    services = Service.objects.all()
    form_ser = ServiceForm()
    #form_sup = SupplierForm()
    return render(request, 'service_list.html', locals())

@login_required
def service_operate(request,id):
    service = get_object_or_404(Service, pk=id)
    if request.method == 'DELETE':
        service.delete()
        return JsonResponse({"status": u"删除成功"})
    if request.method == 'POST':
        type = request.POST.get('type')
        #create_date = request.POST.get('create_date')
        end_date = request.POST.get('end_date')
        obj,created = Type.objects.get_or_create(name=type)
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.type = obj
            #if create_date:
            #    inst.create_date = datetime.datetime.strptime(create_date,"%Y-%m-%d")
            if end_date:
                inst.end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
            inst.save()
            return JsonResponse({"status": u"更新成功"})
        else:
            return JsonResponse({"status": u"更新失败", "msg": u"服务名称已存在"})
    types = Type.objects.all()
    form = ServiceForm(instance=service)
    return render(request, 'service_operate.html', locals())

@login_required
def requisition_list(request):
    #print(request.COOKIES)
    if request.method == 'POST':
        #print(request.POST)
        asset = request.POST.get('asset')
        payment = request.POST.get('payment')
        alipay = request.POST.get('alipay', None)
        bank = request.POST.get('bank', "")
        bank_name = request.POST.get('bank_name', "")
        requisition = Requisition()
        form = RequisitionForm(request.POST, instance=requisition)
        if form.is_valid():
            inst = form.save(commit=False)
            if payment == '1':
                inst.info = "\n".join([bank, bank_name])
            else:
                inst.info = alipay
            inst.asset = asset
            inst.save()
            return JsonResponse({"status": u"添加成功"})
        else:
            return JsonResponse({"status": u"添加失败", "msg": u"表单错误"})
    servers = [s.ip for s in Server.objects.filter(status=1) if not Requisition.objects.filter(asset=s.ip)]
    services = [s.name for s in Service.objects.filter(status=1) if not Requisition.objects.filter(asset=s.name)]
    requisitions = Requisition.objects.all()
    form = RequisitionForm()
    return render(request, 'requisition_list.html', locals())

def requisition_operate(request,id,renew=None):
    req = get_object_or_404(Requisition, pk=id)
    try:
        ser = Server.objects.get(ip=req.asset)
    except ObjectDoesNotExist,e:
        ser = Service.objects.get(name=req.asset)
    if req.payment == 1:
        bank,bank_name = req.info.split("\n")
    else:
        alipay = req.info
    if request.method == 'DELETE':
        if ser.status == 2:
            req.delete()
            return JsonResponse({"status": u"删除成功"})
        else:
            return JsonResponse({"status": u"删除失败", "msg":"请确保资产已经停用"})
    if request.method == 'POST':
        payment = request.POST.get('payment')
        alipay = request.POST.get('alipay', None)
        bank = request.POST.get('bank', "")
        bank_name = request.POST.get('bank_name', "")
        if renew:
            req_old = req
            req = Requisition()
        form = RequisitionForm(request.POST, instance=req)
        if form.is_valid():
            inst = form.save(commit=False)
            if payment == '1':
                inst.info = "\n".join([bank, bank_name])
            else:
                inst.info = alipay
            if renew:
                inst.asset = req_old.asset
                req_old.payment_status = 4
                req_old.save()
            inst.save()
            return JsonResponse({"status": u"操作成功"})
        else:
            return JsonResponse({"status": u"操作失败", "msg": u"表单错误"})
    form = RequisitionForm(instance=req)
    return render(request, 'requisition_operate.html', locals())

@login_required
def requisition_renew_list(request):
    renews = []
    requisitions = Requisition.objects.filter(payment_status=3)
    for i in requisitions:
        try:
            ser = Server.objects.get(ip=i.asset)
        except ObjectDoesNotExist,e:
            ser = Service.objects.get(name=i.asset)
        if ser.status == 1:
            renews.append(i)
    return render(request, 'requisition_renew_list.html', {"renews": renews})

def req_approve(request,id,result):
    req = get_object_or_404(Requisition, pk=id)
    if result in ["yes","no"]:
        if result == "yes":
            req.approve_status = 2
        else:
            req.approve_status = 3
        req.save()
        return JsonResponse({"status": u"更改成功"})
    else:
        return JsonResponse({"status": u"更改失败", "msg": u"错误的审核结果"})

def pay_confirm(request,id):
    req = get_object_or_404(Requisition, pk=id)
    if req.approve_status != 2:
        return JsonResponse({"status": u"操作失败", "msg": u"申请单只有通过审核才能确认付款！"})
    try:
        ser = Server.objects.get(ip=req.asset)
    except ObjectDoesNotExist:
        ser = Service.objects.get(name=req.asset)
    req.payment_status = 2
    ser.end_date = req.end_date
    req.save()
    ser.save()
    return JsonResponse({"status": u"操作成功"})

def cost_show(request):
    now = datetime.datetime.now()
    data = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    count = 0
    categories = range(now.year-4, now.year+1)
    for y in categories:
        servers = Server.objects.filter(end_date__year__gte=y)
        services = Service.objects.filter(end_date__year__gte=y)
        for s in chain(servers,services):
            if s.end_date:
                quarter = get_quarter(s.end_date)
            else:
                quarter = None
            if quarter:
                if s.end_date.year > y:
                    if s.create_date.year < y:
                        for i in range(0,4):
                            data[i][count] += round(float(s.cost)*3,2)
                    elif s.create_date.year == y:
                        start_quarter = get_quarter(s.create_date)
                        for i in range(start_quarter-1,4):
                            if i == start_quarter-1:
                                data[i][count] += round(float(s.cost)*(start_quarter*3-s.create_date.month+1),2)
                            else:
                                data[i][count] += round(float(s.cost)*3,2)
                    else:
                        pass
                elif s.end_date.year == y:
                    if s.create_date.year < y:
                        for i in range(0,quarter):
                            if i == quarter-1:
                                data[i][count] += round(float(s.cost)*(s.end_date.month-(quarter-1)*3),2)
                            else:
                                data[i][count] += round(float(s.cost)*3,2)
                    elif s.create_date.year == y:
                        start_quarter = get_quarter(s.create_date)
                        for i in range(start_quarter-1,quarter):
                            if start_quarter == quarter:
                                data[i][count] += round(float(s.cost)*(s.end_date.month-s.create_date.month+1),2)
                            elif start_quarter < quarter:
                                if i == start_quarter-1:
                                    data[i][count] += round(float(s.cost)*(start_quarter*3-s.create_date.month+1),2)
                                elif i == quarter-1:
                                    data[i][count] += round(float(s.cost)*(s.end_date.month-(quarter-1)*3),2)
                                else:
                                    data[i][count] += round(float(s.cost)*3,2)
                    else:
                        pass
        count += 1
    return JsonResponse({"categories": categories,"data": data})
