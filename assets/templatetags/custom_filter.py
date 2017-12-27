# ~*~ coding: utf-8 ~*~

import os
import datetime
from django import template
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe
from assets.models import Server,Service
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter
def basename(path):
    return os.path.basename(str(path))

@register.filter
def costformat(cost, unit):
    if unit == 1:
        value = "RMB ￥\n{:.2f}".format(float(cost))
    elif unit == 2:
        value = "H.K.$\n{:.2f}".format(float(cost))
    elif unit == 3:
        value = "U.S.$\n{:.2f}".format(float(cost))
    return mark_safe(linebreaks(value))

@register.filter
def payformat(info, payment):
    if payment == 1:
        bank,bank_name = info.split("\n")
        value = "<strong>银行账号：</strong>{}\n<strong>支付银行：</strong>{}".format(bank,bank_name)
    elif payment == 2:
        alipay = info
        value = "<strong>支付宝账号：</strong>{}".format(alipay)
    return mark_safe(linebreaks(value))

@register.filter
def asset_info(asset, edit=False):
    try:
        ser = Server.objects.get(ip=asset)
        if edit:
            asset = ""
        if ser.status == 1:
            value = "{}\n<strong>机房：</strong>{}\n<strong>作用：</strong>{}".format(asset,ser.idc.name,ser.use).strip()
        else:
            value = "{}\n<strong>机房：</strong>{}\n<strong>作用：</strong>{}\n<span style='color:red;font-weight:bold'><strong>(已停用！)</strong></span>".format(asset,ser.idc.name,ser.use).strip()
        return mark_safe(linebreaks(value))
    except ObjectDoesNotExist,e:
        pass
    try:
        ser = Service.objects.get(name=asset)
        if edit:
            asset = ""
        if ser.status == 1:
            value = "{}\n<strong>供应商：</strong>{}\n<strong>作用：</strong>{}".format(asset,ser.supplier.name,ser.use).strip()
        else:
            value = "{}\n<strong>供应商：</strong>{}\n<strong>作用：</strong>{}\n<span style='color:red;font-weight:bold'><strong>(已停用！)</strong></span>".format(asset,ser.supplier.name,ser.use).strip()
        return mark_safe(linebreaks(value))
    except ObjectDoesNotExist,e:
        pass
    return asset

@register.filter
def end_date(datestr, expire=7):
    if datestr:
        now = datetime.datetime.now()
        end_date = datetime.datetime.strptime(datestr,"%Y/%m/%d")
        expire = datetime.timedelta(days=expire)
        if end_date >= (now-datetime.timedelta(days=1)) and now >= (end_date-expire):
            value = "<span style='color:red;font-weight:bold'>{}</span>".format(datestr)
            return mark_safe(linebreaks(value))
    return datestr
