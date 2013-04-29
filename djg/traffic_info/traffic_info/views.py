from django.http import HttpResponse
from traffic_timeline import TrafficTimeline

def hello(request):
    return HttpResponse("Hello world")


def traffic_text(request):
    ''' (str_http_request) -> http_response
    
    DESC :	    This function displays the current traffic information in text.
                It shows in format of ul.
    '''
    
    tt = TrafficTimeline()
    
    str_tt = str(tt.parse_trafficnsw_twitter_entry())
    
    return HttpResponse(str_tt)