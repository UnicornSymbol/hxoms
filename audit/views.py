#coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse,HttpResponseBadRequest,StreamingHttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from audit.models import OperateLog

# Create your views here.
@login_required
def operate_log(request):
    logs = OperateLog.objects.all()
    return render(request, 'operate_log.html', locals())
