from django import template

def traffic_text_template(tt_output):
    ''' (dict_traffic_timeline_output) -> traffic_text_html
    
    DESC :    This function render the output from traffic_timeline into html.
    '''

    raw_html = '''
    <html>
    <head><title>Latest traffic information</title></head>

    <body>

    {% for i in events %}
    {{ i.suburb }}
    {% endfor %}

    </body>
    </html>
    '''
    
    t = template.Template(raw_html)
    
    events = template.Context(tt_output)
    
    html = t.render(events)
    
    return html
    