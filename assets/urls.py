from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
    url(r'^idc_list/$', views.idc_list, name='idc_list'),
    url(r'^idc_operate/(?P<id>\d+)/$', views.idc_operate, name='idc_operate'),
    url(r'^server_list/$', views.server_list, name='server_list'),
    url(r'^server_operate/(?P<id>\d+)/$', views.server_operate, name='server_operate'),
    url(r'^status_change/(?P<sid>\d+)/(?P<status>\d)/$', views.status_change, name='status_change'),
    url(r'^supplier_operate/(?P<id>\d+)/$', views.supplier_operate, name='supplier_operate'),
    url(r'^supplier_operate/$', views.supplier_operate, name='supplier_add'),
    url(r'^service_list/$', views.service_list, name='service_list'),
    url(r'^service_operate/(?P<id>\d+)/$', views.service_operate, name='service_operate'),
    #url(r'^idc_add/$', views.idc_manage, name='idc_add'),
    #url(r'^idc_edit/(?P<id>\d+)/$', views.idc_manage, name='idc_edit'),
    #url(r'^idc_delete/$', views.idc_manage, name='idc_delete'),
    #url(r'^asset_list/$', views.asset_list, name='asset_list'),
    #url(r'^asset_add/$', views.asset_manage, name='asset_add'),
    #url(r'^asset_edit/(?P<id>\d+)/$', views.asset_manage, name='asset_edit'),
    #url(r'^asset_delete/$', views.asset_manage, name='asset_delete'),
    #url(r'^asset_detail/(?P<id>\d+)/$', views.asset_detail, name='asset_detail'),
    #url(r'^host_list/$', views.host_list, name='host_list'),
    #url(r'^host_add/$', views.host_manage, name='host_add'),
    #url(r'^host_update/(?P<id>\d+)/$', views.host_manage, name='host_update'),
    #url(r'^host_delete/$', views.host_manage, name='host_delete'),
]