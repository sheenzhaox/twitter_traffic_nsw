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
        
        <table border="1">
        
        <th> Time </th>
        <th> Suburb </th>
        <th> Location </th>
        <th> Type </th>
        {% for i in events %}
            <tr>
            <td>{{i.time}}</td>
            <td>{{i.suburb}}</td>
            <td>{{i.location}}</td>
            <td>{{i.type}}</td>
            </tr>
        {% endfor %}
        </table>
        
    </body>
    </html>
    '''
    
    t = template.Template(raw_html)
    
    for i in range(len(tt_output)):
        tt_output[i]['time'] = str(tt_output[i]['time'])
    
    events = template.Context({'events':tt_output})
    
    html = t.render(events)
    
    return html
    