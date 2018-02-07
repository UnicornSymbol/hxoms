#coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse,HttpResponseBadRequest,StreamingHttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from deploy.models import SaltHost
from assets.models import Server
from ConfigParser import ConfigParser
from api.saltapi import SaltAPI
from django.db.models import Q 

CONFIG_FILE="./hxoms/config.ini"
config=ConfigParser()
config.read(CONFIG_FILE)

# Create your views here.
@login_required
def key_manager(request):
    sapi = SaltAPI(url=config.get('saltapi','url'), username=config.get('saltapi','username'), password=config.get('saltapi','password'))
    node_name = request.GET.get('minion_id', "")
    action = request.GET.get('action', "")
    #print(node_name)
    #print(action)
    if node_name:
        salthost = get_object_or_404(SaltHost, node_name=node_name)
        if action == "delete_key":
            sapi.delete_key(node_name)
            salthost.key_status = 3
            if salthost.server:
                salthost.server.node_name = None
                salthost.server.alive = False
                salthost.server.save()
            salthost.save()
            return JsonResponse({"status": u"删除成功"})
        if action == "accept_key":
            sapi.accept_key(node_name)
            salthost.key_status = 1
            salthost.save()
            return JsonResponse({"status": u"接受成功"})
        if action == "refresh_host":
            try:
                server = Server.objects.get(node_name=node_name)
            except ObjectDoesNotExist:
                server = None
            if server:
                online = sapi.salt_alive(server.node_name)
                if not online:
                    server.alive = False
                else:
                    server.alive = True
                server.save()
            salthost.server = server
            salthost.save()
            if server:
                return JsonResponse({"status": u"刷新完成","host": server.ip, "alive": server.alive, "id": server.id})
            else:
                return JsonResponse({"status": u"刷新完成","server": server})
        if action == "refresh_status":
            minions,minions_pre = sapi.list_all_key()
            if node_name in minions_pre:
                salthost.key_status = 2
                salthost.save()
                return JsonResponse({"status": u"刷新完成"})
        if action == "delete":
            salthost.delete()
            return JsonResponse({"status": u"删除成功"})
    minions = SaltHost.objects.filter(key_status=1)
    minions_pre = SaltHost.objects.filter(~Q(key_status=1))
    return render(request, 'key_manager.html', locals())

@login_required
def refresh_salt_host(request):
    sapi = SaltAPI(url=config.get('saltapi','url'), username=config.get('saltapi','username'), password=config.get('saltapi','password'))
    minions,minions_pre = sapi.list_all_key()
    for node_name in minions:
        obj,created = SaltHost.objects.get_or_create(node_name=node_name)
        obj.key_status = 1
        try:
            obj.server = Server.objects.get(node_name=node_name)
        except ObjectDoesNotExist:
            obj.server = None
        obj.save()
    for node_name in minions_pre:
        obj,created = SaltHost.objects.get_or_create(node_name=node_name)
        obj.key_status = 2
        try:
            obj.server = Server.objects.get(node_name=node_name)
        except ObjectDoesNotExist:
            obj.server = None
        obj.save()
    return JsonResponse({"status": u"刷新完成"})
