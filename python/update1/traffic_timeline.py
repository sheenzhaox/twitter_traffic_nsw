#!/usr/bin/python

from twitter_timeline import TwitterTimeline
from time import strptime
# from geopy import geocoders
# from postcode import query_postcode
from pprint import pprint



class TrafficTimeline(TwitterTimeline):
    ''' A class to read timeline from the users who publish traffic events.
        It also parses raw data into <time, location, event_type, etc.>
        The users include: TrafficNSW, LiveTrafficSyd
    '''

    def __init__(self, screen_name="TrafficNSW", expire = 60):
        ''' (TwitterTimeline, int) -> TwitterTimeline

        RETURN :    an initiated TwitterTimeline object.
        PARAMETER : 
            expire - seconds. If the last twitter query happened before 
                        expire timer, it will re-query from twitter.
        '''

        # Call parent constuctor
        TwitterTimeline.__init__(self, screen_name, expire)


    def parse_trafficnsw_twitter_entry(self):
        ''' (TwitterTimeline) -> list

        RETURN :    List of dictionary of required information.
        DESC :      This is to parse the data from TrafficNSW
        '''
        assert (self.id == 'TrafficNSW')

        # events = []
        raw_data = self.get_timelines()
        processed_data = []

        print raw_data[0].keys()

        for item in raw_data:
            '''
            The following are the keys in TrafficNSW timeline raw data
            - u'user': user information
            - u'text': event information
            - u'created_at': event time
            '''

            # The first step is to process the event time. Because the 

            event = {'time':item['created_at']}

            print event
            

        return processed_data


    def parse_livetrafficsyd_twitter_entry(self):
        ''' (TwitterTimeline) -> list

        RETURN :    List of dictionary of required information.
        DESC :      This is to parse the data from TrafficNSW
        '''
        assert (self.id == 'LiveTrafficSyd')

        # events = []
        raw_data = self.get_timelines()

        for entry in raw_data:
            
            str_event = status['text']
            str_event_time = status['created_at']

            print str_event, str_event_time

        return raw_data


        #     '''
        #     Typical event is shown as follow
        #         Sydney Traffic EMERGENCY ROAD WORKS - TURRAMURRA Pacific Hwy \
        #         at Kissing Point Rd #sydtraffic #trafficnetwork
        #     Before '-', it is event type; after that, it is event location.
        #     I also need to remove "Sydney Traffic" and 
        #         "#sydtraffic #trafficnetwork" signs.
        #     '''
        #     event_type = str_event[len('Sydney Traffic '):str_event.find(' -')]

        #     event_location = str_event[ str_event.find('-')+2 : \
        #                                 str_event.find(' #')]

        #     # ''' 
        #     # The following part uses geopy to process location into geocode.
        #     # '''
        #     # geo = geocoders.GoogleV3()
        #     # try:
        #     #     event_geo = geo.geocode(event_location)
        #     # except:
        #     #     event_geo = None

        #     # if event_geo != None:
        #     #     # print "%s: %.5f, %.5f" % (event_geo[0], event_geo[1][0], event_geo[1][1])
        #     #     # print event_geo
        #     #     event_street = event_geo[0].encode("utf-8").split(',')[0]
        #     #     event_suburb = event_geo[0].encode("utf-8").split(',')[1].split()[:-2]
        #     #     event_postcode = event_geo[0].encode("utf-8").split(',')[1].split()[-1]
        #     #     event_cord = event_geo[1]
        #     # else: 
        #     #     event_suburb = ""
        #     #     for i in event_location.split():
        #     #         if i==i.upper():
        #     #             event_suburb += i + " "
        #     #     event_suburb.strip()        # Remove the last ' '
        #     #     event_street = event_location.lstrip(event_suburb).strip()
        #     #     event_postcode = None
        #     #     event_cord = None

        #     gcode = query_postcode(event_location)

        #     '''
        #     Data is shown as 
        #         Tue Apr 09 01:50:04 +0000 2013
        #     Please note it is UTC time. So, we need to convert it into local 
        #     (Sydney) time.
        #     Because striptime has a bug in parse '%z', I have to remove +0000 \
        #     from the string
        #     '''
        #     str_event_time = str_event_time.replace("+0000 ", "")
        #     utc_time = datetime.datetime.strptime(str_event_time, \
        #         '%a %b %d %H:%M:%S %Y')
        #     event_time = utc_time + datetime.timedelta(hours=10)

        #     event = {}
        #     event['time'] = event_time
        #     event['type'] = event_type
        #     event['suburb'] = gcode['suburb']
        #     event['street'] = gcode['street']
        #     event['postcode'] = gcode['postcode']
        #     event['coordinate'] = gcode['cord']

        #     events.append(event)

        # return events

    # '''
    # FUNCTION            parse_trafficnsw_twitter_entry
    # PARAMETER           raw_data: the twitter timeline data
    # RETURN              A list containing the individual event.
    #                     The single event is composed by a dictionary, including
    #                     time, location, event type.
    # '''


    # """

    # """
    # def get_traffic_from_twitter(self):

    #     '''
    #     The following block is to test if the twitter query happened in the
    #     last 2 minutes. If so, just return. Otherwise, it will do a new query.
    #     '''
    #     current_time = datetime.datetime.now()
    #     time_diff = (current_time - self.last_time_obtain_from_twitter).seconds
    #     if time_diff < 120:
    #         # print "No change"
    #         return
    #     else:
    #         self.last_time_obtain_from_twitter = current_time
    #         # print self.last_time_obtain_from_twitter
    #     self.text = []

    #     raw_data = TrafficNSW.query_twitter_raw_data()
    #     results = self.parse_trafficnsw_twitter_entry(raw_data)

    #     for status in results:
    #         self.text.append(status)

    #     return results

    # """

    # """
    # def get_traffic_in_minutes(self, minutes = 60):
    #     seconds = minutes * 60
    #     current_time = datetime.datetime.now()

    #     self.get_traffic_from_twitter()
    #     output = []

    #     for event in self.text:
    #         time_diff = (current_time - event["time"]).seconds
    #         if time_diff <= seconds:
    #             output.append(event)

    #     return output


    def __str__(self):
        if self.text == []:
            return "No event in record."

        return "Current event: %s. " % self.text[0]


# The following part is used for test
if __name__ == '__main__':
    '''
    2 kinds of tests could be done in the following part.
    (1) doctest
        It would test every function with standard comments in the file. This
        method is not good for Class.
    (2) unitest
        It will run some written script.
    '''

    # # DOCTEST
    # import doctest
    # doctest.testmod()

    # # UNITEST
    # import unitest

    # class TestTrafficNSW(unitest.TestCase):
    #     ''' Test functions in TrafficNSW. '''

    #     # ALL test functions should start as 'test_'
    #     def test_xxx(self):
    #         # xxx
    #         actual = xxx_function
    #         expected = xxx_exp
    #         self.assertEqual(expected, actual)

    tw = TrafficTimeline()

    print tw.parse_trafficnsw_twitter_entry()

