# views.py

from django.http import HttpResponse
from TrafficNSW import TrafficNSW

def hello(request):
    tnsw = TrafficNSW()
    output = tnsw.get_traffic_from_twitter()
    html = "<html><head><b>Sydney Traffic Information.</b></head><p><body><ul>"
    # <li>%s</ul></body></html" % output
    for event in output:
        li = "<li>Event: %(time)s \tLocation %(street)s, %(suburb)s %(postcode)s \t Type: %(type)s. </li>" \
            % ({'time': str(event['time']), \
                'street': event['street'], \
                'suburb': event['suburb'], \
                'postcode': event['postcode'], \
                'type': event['type'] })
        html = html + li
    html = html + "</ul></body></html>"


    return HttpResponse(html)