#!/usr/bin/python
# coding:utf-8

import os
import json
import subprocess
import psutil
import socket
import time
import re
import platform
import requests


device_white = ['eth0','eth1', 'eth2', 'eth3', 'em1']

headers = {"Content-Type": "application/json"}


def get_hostname():
    return socket.gethostname()

def get_device_info():
    ret = []
    for device, info in psutil.net_if_addrs().iteritems():
        if device in device_white:
            device_info = {'device': device}
            for snic in info:
                if snic.family == 2:
                    device_info['ip'] = snic.address
                elif snic.family == 17:
                    device_info['mac'] = snic.address
            ret.append(device_info)
    return ret

def get_cpuinfo():
    '''
    Return some CPU information for Linux minions
    '''
    # Provides:
    #   num_cpus
    #   cpu_model
    #   cpu_flags
    ret = {}
    cpuinfo = '/proc/cpuinfo'
    # Parse over the cpuinfo file
    if os.path.isfile(cpuinfo):
        with open(cpuinfo, 'r') as _fp:
            for line in _fp:
                comps = line.split(':')
                if not len(comps) > 1:
                    continue
                key = comps[0].strip()
                val = comps[1].strip()
                if key == 'processor':
                    ret['num_cpus'] = int(val) + 1
                elif key == 'model name':
                    ret['cpu_model'] = val
                elif key == 'flags':
                    ret['cpu_flags'] = val.split()
                elif key == 'Features':
                    ret['cpu_flags'] = val.split()
    if 'num_cpus' not in ret:
        ret['num_cpus'] = 0
    if 'cpu_model' not in ret:
        ret['cpu_model'] = 'Unknown'
    if 'cpu_flags' not in ret:
        ret['cpu_flags'] = []
    return ret

def get_memtotal():
    ret = {'mem_total': 0}
    if osdata['kernel'] == 'Linux':
        meminfo = '/proc/meminfo'

        if os.path.isfile(meminfo):
            with open(meminfo, 'r') as ifile:
                for line in ifile:
                    comps = line.rstrip('\n').split(':')
                    if not len(comps) > 1:
                        continue
                    if comps[0].strip() == 'MemTotal':
                        ret['mem_total'] = int(comps[1].split()[0]) / 1024
    return ret

def get_disk():
    cmd = """/sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'"""
    disk_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    partition_size = []
    for dev in disk_data.stdout.readlines():
        try:
            size = int(dev.strip().split(', ')[1].split()[0]) / 1024 / 1024 / 1024
            partition_size.append(str(size))
        except:
            pass
    return " + ".join(partition_size)

def get_Manufacturer():
    cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
    ret = {}
    manufacturer_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in manufacturer_data.stdout.readlines():
        if "Manufacturer" in line:
            ret['manufacturers'] = line.split(': ')[1].strip()
        elif "Product Name" in line:
            ret['server_type'] = line.split(': ')[1].strip()
        elif "Serial Number" in line:
            ret['st'] = line.split(': ')[1].strip().replace(' ','')
        elif "UUID" in line:
            ret['uuid'] = line.split(': ')[1].strip()
    return ret
    #return manufacturer_data.stdout.readline().split(': ')[1].strip()

# 出厂日期
def get_rel_date():
    cmd = """/usr/sbin/dmidecode | grep -i release"""
    data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date = data.stdout.readline().split(': ')[1].strip()
    return re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',date)  

def get_os_version():
    return " ".join(platform.linux_distribution())

def get_innerIp(ipinfo):
    inner_device = ["eth0", "bond0"]
    ret = {}
    for info in ipinfo:
        if info.has_key('ip') and info.get('device', None) in inner_device:
            ret['ip'] = info['ip']
            ret['mac_address'] = info['mac']
            return  ret
    return {}

    

def run(): 
    data = {}
    res = {}
    data['hostname'] = get_hostname()
    data.update(get_innerIp(get_device_info()))
    cpuinfo = get_cpuinfo()
    data['server_cpu'] = "{cpu} {num}".format(**cpuinfo)
    data['server_disk'] = get_disk()
    data.update( get_Manufacturer())
    data['manufacture_date'] = get_rel_date()
    data['os'] = get_os_version()
    data['server_mem'] = get_Memtotal()
    if "VMware" in data['manufacturers']:
        data['vm_status'] = 0
    else:
        data['vm_status'] = 1
    res['params']=data
    res['jsonrpc'] = "2.0"
    res["id"] = 1
    res["method"]= "server.radd"
 #   print res 
 #   for k,v in data.iteritems():
 #       print k, v
    send(res)

def send(data):
    url = "http://192.168.63.182:2000/api"
    r = requests.post(url, headers=headers,json=data)
    print r.status_code
    print r.content


if __name__ == "__main__":
    run()
