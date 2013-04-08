# views.py

from django.http import HttpResponse
from TrafficNSW import TrafficNSW

def hello(request):
    traffic_nsw = TrafficNSW()
    traffic_nsw.obtain_traffic_from_twitter()
    
    html = "<html><head>Traffic NSW</head> <body> <ol>" + str(traffic_nsw.text) + "</ol></body> </html>"
    
    result = traffic_nsw.print_events()
    
    return HttpResponse(html)