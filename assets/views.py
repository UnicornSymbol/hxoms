#coding: utf-8

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse,HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from assets.forms import IdcForm,ServerForm,SupplierForm,ServiceForm
from assets.models import Idc,Server,Supplier,Type,Service

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
    if request.method == 'DELETE':
        server.delete()
        return JsonResponse({"status": u"删除成功"})
    if request.method == 'POST':
        #print(request.POST)
        buy_date = request.POST.get('buy_date')
        end_date = request.POST.get('end_date')
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            inst = form.save(commit=False)
            if buy_date:
                inst.buy_date = datetime.datetime.strptime(buy_date,"%Y-%m-%d")
            if end_date:
                inst.end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
            inst.save()
            return JsonResponse({"status": u"更新成功"})
        else:
            return JsonResponse({"status": u"更新失败", "msg": u"表单错误"})
    form = ServerForm(instance=server)
    return render(request, 'server_operate.html', locals())

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
            ser.status = status
            ser.save()
            return JsonResponse({"status": u"更改成功"})
        else:
            return JsonResponse({"status": u"更改失败", "msg": u"错误的状态值"})

@login_required
def supplier_operate(request, id=None):
    if id:
        sup = get_object_or_404(Supplier, id=id)
        status = u"更新成功"
    else:
        sup = Supplier()
        status = u"添加成功"
    if request.method == 'DELETE':
        try:
            sup.delete()
        except ProtectedError:
            return JsonResponse({"status": u"删除失败", "msg": u"请确保没有服务依赖于它"})
        return JsonResponse({"status": u"删除成功"})
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=sup)
        if form.is_valid():
            form.save()
            #print sup.id,sup.name
            return JsonResponse({"status": status, "id": sup.id})
        else:
            #print(form.cleaned_data)
            return JsonResponse({"status": u"添加失败", "msg": u"供应商已存在"})
    return HttpResponseBadRequest("Bad Request")

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
            return JsonResponse({"status": u"表单错误"})
    types = Type.objects.all()
    suppliers = Supplier.objects.all()
    services = Service.objects.all()
    form_ser = ServiceForm()
    form_sup = SupplierForm()
    return render(request, 'service_list.html', locals())

@login_required
def service_operate(request,id):
    service = get_object_or_404(Service, pk=id)
    if request.method == 'DELETE':
        service.delete()
        return JsonResponse({"status": u"删除成功"})
    if request.method == 'POST':
        type = request.POST.get('type')
        buy_date = request.POST.get('buy_date')
        end_date = request.POST.get('end_date')
        obj,created = Type.objects.get_or_create(name=type)
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.type = obj
            if buy_date:
                inst.buy_date = datetime.datetime.strptime(buy_date,"%Y-%m-%d")
            if end_date:
                inst.end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
            inst.save()
            return JsonResponse({"status": u"更新成功"})
        else:
            return JsonResponse({"status": u"更新失败", "msg": u"表单错误"})
    types = Type.objects.all()
    form = ServiceForm(instance=service)
    return render(request, 'service_operate.html', locals())
