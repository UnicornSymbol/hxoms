from django.conf.urls import patterns, include, url
from account.views import *
from . import views

urlpatterns = [
    url(r'^operate_log$', views.operate_log, name='operate_log'),
]
