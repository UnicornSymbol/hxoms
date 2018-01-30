from django.shortcuts import render,render_to_response,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth

# Create your views here.
def login(request):
    #print(request.POST)
    username=request.POST.get("username",'')
    password=request.POST.get("password",'')
    user=auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        #return render(request, "base.html", locals())
        return redirect(reverse("index"))
    return render(request, "login.html", {})

def logout(request):
    auth.logout(request)
    response =  HttpResponseRedirect('/')
    #response.delete_cookie("SpryMedia_DataTables_DataTables_Table_0_")
    return response
