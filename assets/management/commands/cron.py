from django.core.management.base import BaseCommand, CommandError
from assets.models import Server,Service,Requisition
import datetime
from django.core.exceptions import ObjectDoesNotExist
    
class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.datetime.now()
        expire = datetime.timedelta(days=7)
        reqs = Requisition.objects.filter(payment_status=2)
        print(now)
        for req in reqs:
            try:
                ser = Server.objects.get(ip=req.asset)
            except ObjectDoesNotExist:
                ser = Service.objects.get(name=req.asset)
            if ser.status == 2:
                continue
            if req.end_date:
                end_date = datetime.datetime.strptime(req.end_date.strftime("%Y/%m/%d"),"%Y/%m/%d")
                if end_date >= (now-datetime.timedelta(days=1)) and now >= (end_date-expire):
                    req.payment_status = 3
                    req.save()
