from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from assets.models import Server,Service,Requisition
from django.contrib.auth.models import User

# Create your views here.
@login_required
def index(request):
    renew_count = 0
    user_count = User.objects.count()
    server_count = Server.objects.filter(status=1).count()
    service_count = Service.objects.filter(status=1).count()
    renews = Requisition.objects.filter(payment_status=3)
    for i in renews:
        try:
            ser = Server.objects.get(ip=i.asset)
        except ObjectDoesNotExist,e:
            ser = Service.objects.get(name=i.asset)
        if ser.status == 1:
            renew_count += 1
    return render(request, "index.html", {"user_count": user_count, "server_count":server_count, 
                                          "service_count":service_count, "renew_count":renew_count})
