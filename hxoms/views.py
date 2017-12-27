from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from assets.models import Server,Service
from django.contrib.auth.models import User

# Create your views here.
@login_required
def index(request):
    user_count = User.objects.count()
    server_count = Server.objects.filter(status=1).count()
    service_count = Service.objects.filter(status=1).count()
    return render(request, "index.html", {"user_count": user_count, "server_count":server_count, 
                                          "service_count":service_count})
