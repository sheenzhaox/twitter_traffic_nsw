# views.py

from django.http import HttpResponse
from TrafficNSW import TrafficNSW

def hello(request):
    tnsw = TrafficNSW()
    tnsw.get_traffic_from_twitter()    
    
    return HttpResponse(str(tnsw))