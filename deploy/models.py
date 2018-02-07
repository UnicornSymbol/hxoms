#coding: utf-8

from __future__ import unicode_literals

from django.db import models
from assets.models import Server

key_status = (
    (1, "Accepted"),
    (2, "Unaccepted"),
    (3, "Deleted"),
)

# Create your models here.
class SaltHost(models.Model):
    node_name =  models.CharField(unique=True, max_length=50, verbose_name=u'主机名称')
    server = models.ForeignKey(Server, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'主机')
    key_status = models.IntegerField(choices=key_status, blank=True, null=True, verbose_name=u'Key状态', default=1)

    def __str__(self):
        return self.node_name
    __repr__ = __str__

    class Meta:
        verbose_name = u'salt主机管理'
        verbose_name_plural = u'salt主机管理'
