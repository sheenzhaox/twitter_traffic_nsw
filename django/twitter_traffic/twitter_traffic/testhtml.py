from TrafficNSW import TrafficNSW

tnsw = TrafficNSW()
output = tnsw.get_traffic_from_twitter()
html = "<html><head><b>Sydney Traffic Information.</b></head><p><body><ul>"
# <li>%s</ul></body></html" % output
for event in output:
    li = "<li>Current event: %(time)s, %(street)s, %(suburb)s, %(type)s.</li>"\
        % ({'time': str(event['time']), \
            'street': event['street'], \
            'suburb': event['suburb'], \
            'type': event['type'] })
    html = html + li
html = html + "</ul></body></html>"

print html