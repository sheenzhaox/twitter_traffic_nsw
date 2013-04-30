#!/usr/bin/python

from twitter_timeline import TwitterTimeline
from time import strptime
import datetime
from gmap_query import GmapQuery
from auspost_api import AuspostAPI
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

        # Call parent constructor
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

        # print raw_data[0].keys()

        '''            
        The following are the keys in TrafficNSW timeline raw data
        - u'user': user information
        - u'text': event information
        - u'created_at': event time

        Typical event is shown as follow
            Sydney Traffic EMERGENCY ROAD WORKS - TURRAMURRA Pacific Hwy \
            at Kissing Point Rd #sydtraffic #trafficnetwork
        Before '-', it is event type; after that, it is event location.
        I also need to remove "Sydney Traffic" and 
            "#sydtraffic #trafficnetwork" signs.
        '''

        for entry in raw_data:
             # Process event time
            '''
            Data is shown as 
                Tue Apr 09 01:50:04 +0000 2013
            Please note it is UTC time. So, we need to convert it into local 
            (Sydney) time.
            Because striptime has a bug in parse '%z', I have to remove +0000 \
            from the string
            '''
            str_event_time = entry['created_at'].replace("+0000 ", "")
            utc_time = datetime.datetime.strptime(str_event_time, \
                '%a %b %d %H:%M:%S %Y')
            event_time = utc_time + datetime.timedelta(hours=10)

            event = {'time': event_time}

            # Process event text
            str_event = entry['text']

            event_type = str_event[len('Sydney Traffic '):str_event.find(' -')]
            event[type] = event_type

            event_location = str_event[ str_event.find('-')+2 : \
                                        str_event.find(' #')].encode("utf-8")

            # Because GMap can't return "a st" near "b st", I replace near by at
            if ' near ' in event_location:
                event_location = event_location.replace(' near ', ' at ')
            
            event['location_text'] = event_location
            # print event_location
            
            gp = GmapQuery()
            gmap_answer = gp.ask_gmap_for_timeline(event_location + ", nsw")
            if gmap_answer:
                event.update(gmap_answer)

            # Process when GMap can't find the right place
            if not 'postcode' in event.keys() or event['postcode']==None \
            or (not any(char.isdigit() for char in event['postcode'])):
                location_str = event_location.split()
                suburb = []
                for i in location_str:
                    if i==i.upper() and (not any(char.isdigit() for char in i)):
                        suburb.append(i)
                    else:
                        break
                suburb = ' '.join(suburb)
                event['suburb'] = suburb
                
                # gmap_answer = gp.ask_gmap_for_timeline(event_location + ", nsw")
                # if gmap_answer:
                #     event['postcode'] = gmap_answer['postcode']

                auspost = AuspostAPI()
                suburb = suburb + ", NSW"
                # print suburb
                postcode = auspost.search_postcode(suburb)
                # print postcode
                if postcode!= None:
                    if isinstance(postcode, list):
                        event['postcode'] = postcode[0]['postcode']
                        event['coordinate'] = (postcode[0]['latitude'], postcode[0]['longitude'])
                    elif isinstance(postcode, dict):
                        event['postcode'] = postcode['postcode']
                        event['coordinate'] = (postcode['latitude'], postcode['longitude'])
                else:
                    event['postcode'] = None
                # print postcode

                event['location'] = event_location[len(suburb)+1:]
                        

            # print event_type, event_location

            processed_data.append(event)

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

            #print str_event, str_event_time

        return raw_data


    def find_latest_traffic_events(self, provider, time):
        ''' (str_provider, int_minutes) -> list

        Return the last ``time'' minutes traffice events published by the given
        ``provider''.
        '''



    def __str__(self):
        if self.text == []:
            return "No event in record."

        return "Current event: %s. " % self.text[0]


# The following part is used for test
if __name__ == '__main__':

    tw = TrafficTimeline()

    for i in tw.parse_trafficnsw_twitter_entry():
        print i

