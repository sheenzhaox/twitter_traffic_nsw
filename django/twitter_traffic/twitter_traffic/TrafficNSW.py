#!/usr/bin/python

import twitter
import datetime
from time import strptime
from geopy import geocoders
# from pprint import pprint


class TrafficNSW:
    def __init__(self, screen_name="TrafficNSW", expire = 3600):
        # self["name"] = screen_name
        self.id = screen_name
        self.text = []
        self.last_time_obtain_from_twitter = datetime.datetime(2000, 1, 1)
        self.expire = expire    # second

    def get_screen_name(self):
        return self.id

    def get_traffic_info(self):
        if self.text==[]:
            self.get_traffic_from_twitter()
        return self.text

    def get_latest_event(self):
        self.get_traffic_from_twitter()
        curr_status = self.text[0]
        return self.print_an_event(curr_status)

    '''
    STATIC FUNCTION     obtain_twitter_raw_data
    PARAMETER           id: the screen name of the twitter user_timeline
    RETURN              the raw timeline data got from twitter
    '''
    @staticmethod
    def obtain_twitter_raw_data(id = "TrafficNSW"):
        tw = twitter.Twitter()
        results = tw.statuses.user_timeline(screen_name = id)
        return results

    '''
    FUNCTION            parse_trafficnsw_twitter_entry
    PARAMETER           raw_data: the twitter timeline data
    RETURN              A list containing the individual event.
                        The single event is composed by a dictionary, including
                        time, location, event type.
    '''
    def parse_trafficnsw_twitter_entry(self, raw_data):
        events = []
        for status in raw_data:
            '''
            The following are the keys in TrafficNSW timeline raw data
            - u'user': user information
            - u'text': event information
            - u'created_at': event time
            '''
            str_event = status['text'].encode("utf-8")
            str_event_time = status['created_at'].encode("utf-8")

            '''
            Typical event is shown as follow
                Sydney Traffic EMERGENCY ROAD WORKS - TURRAMURRA Pacific Hwy \
                at Kissing Point Rd #sydtraffic #trafficnetwork
            Before '-', it is event type; after that, it is event location.
            I also need to remove "Sydney Traffic" and 
                "#sydtraffic #trafficnetwork" signs.
            '''
            event_type = str_event[len('Sydney Traffic '):str_event.find(' -')]

            event_location = str_event[ str_event.find('-')+2 : \
                                        str_event.find(' #')]

            ''' 
            The following part uses geopy to process location into geocode.
            '''
            geo = geocoders.GoogleV3()
            try:
                event_geo = geo.geocode(event_location)
            except:
                event_geo = None

            if event_geo != None:
                # print "%s: %.5f, %.5f" % (event_geo[0], event_geo[1][0], event_geo[1][1])
                # print event_geo
                event_street = event_geo[0].encode("utf-8").split(',')[0]
                event_suburb = event_geo[0].encode("utf-8").split(',')[1].split()[:-2]
                event_postcode = event_geo[0].encode("utf-8").split(',')[1].split()[-1]
                event_cord = event_geo[1]
            else: 
                event_suburb = ""
                for i in event_location.split():
                    if i==i.upper():
                        event_suburb += i + " "
                event_suburb.strip()        # Remove the last ' '
                event_street = event_location.lstrip(event_suburb).strip()
                event_postcode = None
                event_cord = None

            '''
            Data is shown as 
                Tue Apr 09 01:50:04 +0000 2013
            Please note it is UTC time. So, we need to convert it into local 
            (Sydney) time.
            Because striptime has a bug in parse '%z', I have to remove +0000 \
            from the string
            '''
            str_event_time = str_event_time.replace("+0000 ", "")
            utc_time = datetime.datetime.strptime(str_event_time, \
                '%a %b %d %H:%M:%S %Y')
            event_time = utc_time + datetime.timedelta(hours=10)

            event = {}
            event['time'] = event_time
            event['type'] = event_type
            event['suburb'] = event_suburb
            event['street'] = event_street
            event['postcode'] = event_postcode
            event['coordinate'] = event_cord

            events.append(event)

        return events

    """

    """
    def get_traffic_from_twitter(self):

        '''
        The following block is to test if the twitter query happened in the
        last 2 minutes. If so, just return. Otherwise, it will do a new query.
        '''
        current_time = datetime.datetime.now()
        time_diff = (current_time - self.last_time_obtain_from_twitter).seconds
        if time_diff < 120:
            # print "No change"
            return
        else:
            self.last_time_obtain_from_twitter = current_time
            # print self.last_time_obtain_from_twitter
        self.text = []

        raw_data = TrafficNSW.obtain_twitter_raw_data()
        results = self.parse_trafficnsw_twitter_entry(raw_data)

        for status in results:
            self.text.append(status)

        return results

    """

    """
    def get_traffic_in_minutes(self, minutes = 60):
        seconds = minutes * 60
        current_time = datetime.datetime.now()

        self.get_traffic_from_twitter()
        output = []

        for event in self.text:
            time_diff = (current_time - event["time"]).seconds
            if time_diff <= seconds:
                output.append(event)

        return output


    def __str__(self):
        if self.text == []:
            return "No event in record."

        return "Current event: %(time)s, %(street)s, %(suburb)s, %(type)s. " \
        % ({'time': str(self.text[0]['time']), \
            'street': self.text[0]['street'], \
            'suburb': self.text[0]['suburb'], \
            'type': self.text[0]['type'] })
