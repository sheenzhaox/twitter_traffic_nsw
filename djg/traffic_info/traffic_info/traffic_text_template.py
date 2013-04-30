from django import template

def traffic_text_template(tt_output):
    ''' (dict_traffic_timeline_output) -> traffic_text_html
    
    DESC :    This function render the output from traffic_timeline into html.
    '''

    raw_html = '''
    <html>
    
    <head><title>Latest traffic information</title></head>

    <body>
    
        <h1>Latest traffic information</h1>
    
        <ul>
        {% for i in events %}
            <li>{{ i.suburb }}</li>
        {% endfor %}
        </ul>
        
        <table border="1">
        {% for i in events %}
            <tr>
            <td>i.suburb</td>
            <td>i.location</td>
            <td>i.type</td>
            <td>i.postcode</td>
            </tr>
        {% endfor %}
        </table>
        
    </body>
    </html>
    '''
    
    t = template.Template(raw_html)
    
    events = template.Context({'events':tt_output})
    
    html = t.render(events)
    
    return html
    