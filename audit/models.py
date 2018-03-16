#coding: utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.
class OperateLog(models.Model):
    user = models.CharField(max_length=128, verbose_name=u'用户')
    operate_time = models.DateTimeField(auto_now_add=True, verbose_name=u'操作时间')
    type = models.CharField(max_length=20, verbose_name=u'操作类型')
    action_ip = models.GenericIPAddressField(max_length=15, verbose_name=u'用户IP')
    content = models.TextField(blank=True,null=True,max_length=100,verbose_name=u'内容')

    class Meta:
        ordering = ['-operate_time']
        verbose_name = u'操作日志'
        verbose_name_plural = u'操作日志列表'
