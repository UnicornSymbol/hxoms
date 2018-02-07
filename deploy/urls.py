from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
    url(r'^key_manager/$', views.key_manager, name='key_manager'),
    url(r'^refresh_salt_host/$', views.refresh_salt_host, name='refresh_salt_host'),
]
