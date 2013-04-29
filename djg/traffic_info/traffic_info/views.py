from django.http import HttpResponse
from traffic_timeline import TrafficTimeline
from traffic_text_template import traffic_text_template

def hello(request):
    return HttpResponse("Hello world")


def traffic_text(request):
    ''' (str_http_request) -> http_response
    
    DESC :	    This function displays the current traffic information in text.
                It shows in format of ul.
    '''
    
    tt = TrafficTimeline()
    
    html = traffic_text_template(tt.parse_trafficnsw_twitter_entry())
    
    return HttpResponse(html)