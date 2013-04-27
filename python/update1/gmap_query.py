# gmap_query.py

from geopy import geocoders

class GmapQuery(object):
    ''' A class to store location based on GMAP query.

    MEMBERS :
        query - (str) the input string of the location  
        country - 
        state - 
        suburb - 
        street - 
        postcode - 
    '''

    def __init__(self):
        ''' (GmapQuery, str, str, str) -> GmapQuery
        '''

        # self.query = query

        # # If the query is postcode, check for suburb
        # if isinstance( query, int ):
        #     assert len(str(query))==4, 'Postcode should be 4 digits'
        #     GmapQuery.check_suburb_by_postcode(query)
        # else:
        #     GmapQuery.check_address(query)


    @staticmethod
    def check_suburb_by_postcode(query):
        ''' (int) -> str

        RETURN :    The suburb of the corresponding postcode

        >>> GmapQuery.check_suburb_by_postcode(2121)
        'Epping'

        '''
        query = str(query) + ", Australia"

        geo = geocoders.GoogleV3()

        try:
            answer = geo.geocode(query)
        except:
            answer = None

        return answer


    def ask_gmap(self, query):
        ''' (GmapQuery, str_query) -> str_answer

        '''

        self.last_query = query

        if not 'australia' in str(query).lower():
            query = str(query) + ", Australia"

        # print query

        geo = geocoders.GoogleV3()

        try:
            answer = geo.geocode(query)
        except:
            answer = None

        return answer


    def ask_gmap_for_timeline(self, query):
        ''' (GmapQuery, str_query) -> dict_answer

        RETURN :    The dictionary including 'location', 'suburb', 'state', 
                    'postcode', 'coordinate'
        '''

        ans = self.ask_gmap(query)

        if not ans:
            return []

        # print ans

        ans_for_timeline = {'coordinate' : ans[-1]}

        # In most cases, GMap can find 'STREET, SUBURB, COUNTRY', (COORDINATE)
        if len(ans[0].split(', ')) == 3:
            ans_for_timeline['location'] = ans[0].split(', ')[0]\
                                            .encode("utf-8")

            suburb_state_postcode = ans[0].split(', ')[1]\
                                    .encode("utf-8").split()

            # print suburb_state_postcode

            ans_for_timeline['postcode'] = suburb_state_postcode[-1]
            ans_for_timeline['state'] = suburb_state_postcode[-2]
            ans_for_timeline['suburb'] = ' '.join(suburb_state_postcode[:-2])

        # Sometimes, Gmap is unable to find 'STREET'
        elif len(ans[0].split(', ')) == 2:
            ans_for_timeline['location'] = ''

            suburb_state_postcode = ans[0].split(', ')[0]\
                                    .encode("utf-8").split()
            ans_for_timeline['postcode'] = suburb_state_postcode[-1]
            ans_for_timeline['state'] = suburb_state_postcode[-2]
            ans_for_timeline['suburb'] = ' '.join(suburb_state_postcode[:-2])

        return ans_for_timeline




    # def query_postcode(query):
    # ''' (str) -> str

    # RETURN :    The postcode 
    # This function check postcode by suburb, or check suburb by postcode.
    # '''

    # geo = geocoders.GoogleV3()
    # find_postcode = False    

    # if isinstance( query, int ):
    #     '''
    #     If query is postcode, check for suburb.
    #     '''

    #     if len(str(query))!=4:
    #         return "No suburb found."
    #     else:

    #         query = str(query) + ", Australia"
    # else:
    #     find_postcode = True
    #     if not 'australia' in query.lower():
    #         query += ", Australia"

    # print query

    # try:
    #     answer = geo.geocode(query)
    # except:
    #     answer = None

    # print answer

    # if answer != None:
    #     address = answer[0].encode("utf-8").split(',')
    #     # print address

    #     if address[-1].strip().lower()=="australia":
    #         zone = address[-2]
    #         street = address[-3]
    #     else:
    #         street = address[-2]
    #         zone = address[-1]

    #     suburb = ' '.join(zone.split()[:-2])
    #     state = zone.split()[-2]
    #     postcode = zone.split()[-1]
    #     cord = answer[1]

    #     # if find_postcode:
    #     #     return postcode
    #     # else:
    #     #     return ' '.join(suburb) + ", " + ' '.join(state)

    #     output = {'street':street, 'suburb':suburb, 'state':state, 'postcode':postcode, 'cord':cord}

    #     return output
    # else: 
    #     return "Can't find it."


if __name__ == '__main__':

    gq = GmapQuery()

    # print gq.ask_gmap_for_timeline('SEVEN HILLS Prospect Hwy at Johnson Ave (Station Rd)')
    # print gq.ask_gmap_for_timeline('CLAREMONT MEADOWS M4 Mwy at Kent Rd')
    # print gq.ask_gmap_for_timeline('SEVEN HILLS Prospect Hwy at Johnson Ave (Station Rd)')
    print gq.ask_gmap_for_timeline('DRUMMOYNE Victoria Rd on Iron Cove Bridge')