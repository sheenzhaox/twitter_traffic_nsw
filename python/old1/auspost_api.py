import json
import urllib
import urllib2
import urlparse


class AuspostAPI(object):
    ''' The class to query location from Auspost.
    The api is from Auspost http://auspost.com.au/devcentre/

    The file came from https://bitbucket.org/goodtune/python-auspost
    I did some change and comments. The first change is the module of json, 
    because json has replaced anyjson in python standard lib.

    The example of Auspost API JSON output is shown as follows
    {
        "localities" :
        {
            "locality" : [
                {
                    "category" : "Delivery Area",
                    "id" : 7348,
                    "latitude" : -36.755513000000001,
                    "location" : "BENDIGO",
                    "longitude" : 144.28426300000001,
                    "postcode" : 3550,
                    "state" : "VIC"
                },
                {
                    "category" : "Delivery Area",
                    "id" : 7349,
                    "latitude" : -36.755513000000001,
                    "location" : "BENDIGO SOUTH",
                    "longitude" : 144.28426300000001,
                    "postcode" : 3550,
                    "state" : "VIC"
                }
            ]
        }
    }
    '''

    def __init__(self, dest = 'https://auspost.com.au/api/', \
                    api_key = '1bd02277-66a4-435a-95fe-fa9e02125cf6', \
                    format = 'json'):
        ''' (str) -> AuspostAPI
        '''

        self.dest = dest
        self.headers = {'AUTH-KEY': api_key}
        self.format = 'json'


    def _transform_content(self, content):
        ''' (JSON_string) -> python data structure

        RETURN :    the python data structure
        DESC :      Use the ``json.loads'' function to decode it. Loads takes
                    a JSON string and returns a Python data structure.
        '''

        return json.loads(content)


    def _request(self, path, format = 'json', parameters={}, headers={}):
        ''' (question, format, parameters, headers) -> reply
        '''

        url = urlparse.urljoin(self.dest, path)
        url += '.' + format
        url += '?' + urllib.urlencode(parameters)

        request = urllib2.Request(url)
        request.add_header('AUTH-KEY', self.headers['AUTH-KEY'])

        reply = urllib2.urlopen(request).read()

        return self._transform_content(reply)


    def _postcode_query(self, q, format = 'json', state = None, excl_pb_flag = None):
        ''' (q, state, excl_pb_flag) -> postcode/suburb

        Search the collection of Postcode records for potential matches. The 
        search criterion is location name or postcode with an optional state 
        filter. Request must be a HTTPS GET.
        URL: 
            https://auspost.com.au/api/postcode/search.{format}
        Formats: 
            xml, json (Default to xml if format not provided)
        Requires Authorisation: 
            True (API Key)
        Parameters: 
            1. [q]: Required. The search criterion used to drive the search 
                query. This parameter will hold either the location name or 
                postcode
            2. [state]: Optional. Used to filter possible search results. Must 
                be formatted using an Auspost accepted abbreviation (i.e. VIC 
                for Victoria, QLD for Queensland)
            3. [excludePostBoxFlag]: Optional. Set value to true, if post boxes
                should be excluded from search results. That is useful for PAC.
        '''

        parameters = {'q': q}

        if state:
            parameters['state'] = state

        if excl_pb_flag:
            parameters['excludePostBoxFlag'] = excl_pb_flag
        else:
            parameters['excludePostBoxFlag'] = 'true'

        return self._request('postcode/search', format = format, parameters=parameters)


    def search_postcode(self, q):
        ''' (query) -> postcode or suburb

        RETURN :    postcode(s) or suburb(s)
        DESC :      If q is a postcode, the function finds the corresponding
                    suburbs;
                    If q is a suburb, the function finds postcode. The Auspost
                    API does the generally search. This means that the search
                    finds all suburbs includes the string(q). For example,
                        search_postcode('epping')
                    it returns 4 suburbs. 2 Epping in NSW and VIC, North Epping
                    in NSW and Epping. So the last two are not the answer we 
                    want. It is necessary to filter them. Besides, to increase
                    the accuracy, it would be better to add state into query.
        '''

        # If q_is_postcode, find corresponding suburb(s). If multiple suburbs
        try:
            q = int(q)
        except:
            ''' q is not a postcode '''

        q_is_postcode = isinstance( q, int )
        if q_is_postcode:
            q = str(q)

        # The following is to process whether the state has been provided.
        if len(q.split(',')) == 2:
            q0 = q.split(',')[0]
            q1 = q.split(',')[1]
            r = self._postcode_query(q0, state = q1)['localities']['locality']
        else:
            q0 = q
            r = self._postcode_query(q0)['localities']['locality']

        # The following is to filter multiple answers
        if not q_is_postcode:
            for i in sorted(r, reverse=True):
                if i['location'] != q0.upper():
                    r.remove(i)

        return r
        

    # def countries(self):
    #     return self._make_request('postage/country')

    # def domestic_letter_thickness(self):
    #     return self._make_request('postage/letter/domestic/thickness')

    # def domestic_letter_weight(self):
    #     return self._make_request('postage/letter/domestic/weight')

    # def domestic_letter_envelope_size(self):
    #     return self._make_request('postage/letter/domestic/size')

    # def international_letter_weight(self):
    #     return self._make_request('postage/letter/international/weight')

    # def international_parcel_weight(self):
    #     return self._make_request('postage/parcel/international/weight')

    # def domestic_parcel_weight(self):
    #     return self._make_request('postage/parcel/domestic/weight')

    # def domestic_parcel_box_type(self):
    #     return self._make_request('postage/parcel/domestic/type')

    # def domestic_parcel_box_size(self):
    #     return self._make_request('postage/parcel/domestic/size')

    # def domestic_letter_service_list(self, length, width, thickness, weight):
    #     """
    #     @length: Length of the letter in millimetres (max 260mm)
    #     @width: Width of the letter in millimetres (max 360mm)
    #     @thickness: Thickness of the letter in millimetres (max 20mm)
    #     @weight: Weight of the letter in grams (max 500g)
    #     """
    #     parameters = {
    #         'length': length,
    #         'width': width,
    #         'thickness': thickness,
    #         'weight': weight,
    #         }
    #     return self._make_request('postage/letter/domestic/service', parameters=parameters)

    # def domestic_parcel_service_list(self, from_postcode, to_postcode, length, width, height, weight):
    #     """
    #     @from_postcode: Postcode from which the parcel will be sent
    #     @to_postcode: Postcode to which the parcel will be sent
    #     @length: Length of the parcel in centimetres
    #     @width: Width of the parcel in centimetres
    #     @height: Height of the parcel in centimetres
    #     @weight: Weight of the parcel in kilograms
    #     """
    #     parameters = {
    #         'from_postcode': from_postcode,
    #         'to_postcode': to_postcode,
    #         'length': length,
    #         'width': width,
    #         'height': height,
    #         'weight': weight,
    #         }
    #     return self._make_request('postage/parcel/domestic/service', parameters=parameters)

    # def international_letter_service_list(self, country_code, weight):
    #     raise NotImplementedError

    # def international_parcel_service_list(self, country_code, weight):
    #     raise NotImplementedError

    # def postcode_search(self, q, state=None, exclude_post_box=None):
    #     parameters = {'q': q}

    #     if state:
    #         parameters['state'] = state

    #     if exclude_post_box:
    #         parameters['excludePostBoxFlag'] = 'true'

    #     return self._make_request('postcode/search', parameters=parameters)

    # def domestic_letter_postage_calculation(self, service_code, weight, option_code=None, suboption_code=None, extra_cover=None):
    #     """
    #     @service_code: Code retrieved from domestic_letter_service_list
    #     @weight: Weight of the letter in grams (max 500g)
    #     @option_code: Code retrieved from domestic_letter_service_list
    #     @suboption_code: Code retrieved from domestic_letter_service_list
    #     @extra_cover: Monetary value of extra cover, integer only
    #     """
    #     parameters = {
    #         'service_code': service_code,
    #         'weight': weight,
    #         }
    #     if option_code:
    #         parameters['option_code'] = option_code
    #     if suboption_code:
    #         parameters['suboption_code'] = suboption_code
    #     if extra_cover:
    #         assert suboption_code == "AUS_SERVICE_OPTION_EXTRA_COVER"
    #         parameters['extra_cover'] = extra_cover
    #     return self._make_request('postage/letter/domestic/calculate', parameters=parameters)

    # def domestic_parcel_postage_calculation(self, from_postcode, to_postcode, length, width, height, weight, service_code, option_code=None, suboption_code=None, extra_cover=None):
    #     """
    #     @from_postcode: Postcode from which the parcel will be sent
    #     @to_postcode: Postcode to which the parcel will be sent
    #     @length: Length of the parcel in centimetres
    #     @width: Width of the parcel in centimetres
    #     @height: Height of the parcel in centimetres
    #     @weight: Weight of the parcel in kilograms
    #     """
    #     parameters = {
    #         'from_postcode': from_postcode,
    #         'to_postcode': to_postcode,
    #         'length': length,
    #         'width': width,
    #         'height': height,
    #         'weight': weight,
    #         'service_code': service_code,
    #         }
    #     if option_code:
    #         parameters['option_code'] = option_code
    #     if suboption_code:
    #         parameters['suboption_code'] = suboption_code
    #     if extra_cover:
    #         parameters['extra_cover'] = extra_cover
    #     return self._make_request('postage/parcel/domestic/calculate', parameters=parameters)

    # def international_letter_postage_calculation(self, country_code, service_code, weight=None, option_code=None, suboption_code=None, extra_cover=None):
    #     raise NotImplementedError

    # def international_parcel_postage_calculation(self, country_code, service_code, weight, option_code=None, extra_cover=None):
    #     raise NotImplementedError


if __name__ == '__main__':
    auspost_api = AuspostAPI()
    print auspost_api.search_postcode('epping, nsw')

