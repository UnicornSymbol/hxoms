# coding:utf-8

import re
import time
import threading
#from celery import Celery,platforms
from celery import task
from ConfigParser import ConfigParser
from api.saltapi import SaltAPI
from assets.models import Server,ServerInfo
from audit.models import OperateLog
from django.core.exceptions import ObjectDoesNotExist

#app=Celery('tasks')
#platforms.C_FORCE_ROOT = True
CONFIG_FILE="./hxoms/config.ini"
config=ConfigParser()
config.read(CONFIG_FILE)
disk_pattern = re.compile(r'(?P<size>\d+(\.\d+)?)(?P<unit>.*)')
unit_convert_gb = {
    "MB":lambda x: float(x)/1000,
    "GB":lambda x: float(x),
    "TB":lambda x: float(x)*1000,
    "PB":lambda x: float(x)*1000*1000,
}

def check_alive(ser):
    sapi = SaltAPI(url=config.get('saltapi','url'), username=config.get('saltapi','username'), password=config.get('saltapi','password'))
    if ser.node_name:  #更新node_name手动刷新(refresh)
        online = sapi.salt_alive(ser.node_name)
        if not online:
            ser.alive = False
        else:
            ser.alive = True
        ser.save()
        return
    alive = sapi.salt_alive('*')
    for node_name in alive.keys():
        try:
            ipv4 = sapi.remote_execution(node_name, 'grains.item', 'ipv4')['ipv4']
        except KeyError:
            continue
        else:
            if ser.ip in ipv4:
                ser.alive = True
                ser.node_name = node_name
                ser.save()
                break
    else:
        ser.alive = False
        ser.save()

def refresh_alive(ser):
    if ser.status == 2:
        #time.sleep(5)
        return
    sapi = SaltAPI(url=config.get('saltapi','url'), username=config.get('saltapi','username'), password=config.get('saltapi','password'))
    alive = sapi.salt_alive('*')
    for node_name in alive.keys():
        try:
            ipv4 = sapi.remote_execution(node_name, 'grains.item', 'ipv4')['ipv4']
        except KeyError:
            continue
        else:
            if ser.ip in ipv4:
                ser.alive = True
                ser.node_name = node_name
                ser.save()
                break
    else:
        ser.alive = False
        ser.save()

def get_server_info(ser):
    sapi = SaltAPI(url=config.get('saltapi','url'), username=config.get('saltapi','username'), password=config.get('saltapi','password'))
    #minions,minions_pre = sapi.list_all_key()
    if ser.node_name:
        try:
            grains = sapi.remote_noarg_execution(ser.node_name, 'grains.items')
            #disk_usage = sapi.remote_noarg_execution(ser.node_name, 'disk.usage')
            # -s表示不提示用户
            disk = sapi.remote_execution(ser.node_name, 'cmd.run', "parted -ls | grep \"Disk \/dev\/[a-z]d\" | awk -F\"[ ]\" '{print $3}'")
        except KeyError:
            return
        else:
            try:
                serverinfo = ser.serverinfo
            except ObjectDoesNotExist:
                serverinfo = ServerInfo()
                serverinfo.ip = ser
            serverinfo.hostname = grains['fqdn']
            ip4_interfaces = grains['ip4_interfaces']
            ip4_interfaces.pop('lo')
            for interface,ip in ip4_interfaces.items():
                if ser.ip in ip:
                    ip.remove(ser.ip)
                    other_ip = ip
                    serverinfo.other_ip = "/".join(other_ip)
                    serverinfo.hwaddr = grains['hwaddr_interfaces'][interface]
            serverinfo.manufacturer = grains['manufacturer']
            serverinfo.brand = grains['productname']
            serverinfo.cpu = grains['cpu_model']
            serverinfo.cpu_num = grains['num_cpus']
            serverinfo.system_type = grains['os']
            serverinfo.system_version = grains['osrelease']
            serverinfo.system_arch = grains['osarch']
            serverinfo.virtual = grains['virtual']
            serverinfo.sn = grains['serialnumber']
            mem=grains['mem_total']
            if mem > 1000:
                mem = int(round(mem/1000.0))
                memory = ('%d'%mem) + ' GB'
            else:
                memory = str(mem) + ' MB'
            serverinfo.memory = memory
            size = 0
            for s in disk.split("\n"):
                d = disk_pattern.match(s).groupdict()
                size += unit_convert_gb[d['unit']](d['size'])
            if size < 1000:
                disk = str(size)+' GB'
            else:
                size = round(size/1000.0,1)
                if size < 1000:
                    disk = str(size)+' TB'
                else:
                    disk = str(round(size/1000.0),2)+' PB'
            serverinfo.disk = disk
            serverinfo.save()

@task
def alive_task():
    t_list = []
    servers = Server.objects.filter(status=1)
    loop=0
    max_threads=32
    ser_num = len(servers)
    for i in range(0, ser_num, max_threads):
        keys = range(loop*max_threads, (loop+1)*max_threads, 1)

        #实例化线程
        for i in keys:
            if i >= ser_num:
                break
            else:
                t = threading.Thread(target=check_alive, args=(servers[i],))
                t_list.append(t)
        #启动线程
        for i in keys:
            if i >= ser_num:
                break
            else:
                t_list[i].start()
        #等待并发线程结束
        for i in keys:
            if i >= ser_num:
                break
            else:
                t_list[i].join()
        loop = loop + 1

@task
def get_server_info_task():
    t_list = []
    servers = Server.objects.filter(status=1).filter(alive=True)
    loop=0
    max_threads=32
    ser_num = len(servers)
    for i in range(0, ser_num, max_threads):
        keys = range(loop*max_threads, (loop+1)*max_threads, 1)

        #实例化线程
        for i in keys:
            if i >= ser_num:
                break
            else:
                t = threading.Thread(target=get_server_info, args=(servers[i],))
                t_list.append(t)
        #启动线程
        for i in keys:
            if i >= ser_num:
                break
            else:
                t_list[i].start()
        #等待并发线程结束
        for i in keys:
            if i >= ser_num:
                break
            else:
                t_list[i].join()
        loop = loop + 1

@task()
def delete_key(node):
    sapi = SaltAPI(url=config.get('saltapi','url'), username=config.get('saltapi','username'), password=config.get('saltapi','password'))
    sapi.delete_key(node)

@task
def operate_log(user,ip,type,content):
    OperateLog.objects.create(user=user,action_ip=ip,type=type,content=content)
