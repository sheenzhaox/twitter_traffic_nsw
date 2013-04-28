#!/usr/bin/python

from geopy import geocoders

def query_postcode(query):
    ''' (str) -> str

    RETURN :    The postcode 
    This function check postcode by suburb, or check suburb by postcode.
    '''

    geo = geocoders.GoogleV3()
    find_postcode = False    

    if isinstance( query, int ):
        '''
        If query is postcode, check for suburb.
        '''

        if len(str(query))!=4:
            return "No suburb found."
        else:

            query = str(query) + ", Australia"
    else:
        find_postcode = True
        if not 'australia' in query.lower():
            query += ", Australia"

    print query

    try:
        answer = geo.geocode(query)
    except:
        answer = None

    print answer

    if answer != None:
        address = answer[0].encode("utf-8").split(',')
        # print address

        if address[-1].strip().lower()=="australia":
            zone = address[-2]
            street = address[-3]
        else:
            street = address[-2]
            zone = address[-1]

        suburb = ' '.join(zone.split()[:-2])
        state = zone.split()[-2]
        postcode = zone.split()[-1]
        cord = answer[1]

        # if find_postcode:
        #     return postcode
        # else:
        #     return ' '.join(suburb) + ", " + ' '.join(state)

        output = {'street':street, 'suburb':suburb, 'state':state, 'postcode':postcode, 'cord':cord}

        return output
    else: 
        return "Can't find it."

