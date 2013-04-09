#!/usr/bin/python

import twitter
import datetime
from time import strptime
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
        return self.text

    def get_latest_event(self):
        self.obtain_traffic_from_twitter()
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
            event_suburb = ""
            for i in event_location.split():
                if i==i.upper():
                    event_suburb += i + " "
            event_suburb.strip()        # Remove the last ' '
            event_street = event_location.lstrip(event_suburb).strip()
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

            events.append(event)
            
        return events


    def obtain_traffic_from_twitter(self):

        '''
        The following block is to test if the twitter query happened in the
        last 10 minutes. If so, just return. Otherwise, it will do a new query.
        '''
        current_time = datetime.datetime.now()
        time_diff = (current_time - self.last_time_obtain_from_twitter).seconds
        if time_diff < 5:
            # print "No change"
            return
        else:
            self.last_time_obtain_from_twitter = current_time
            # print self.last_time_obtain_from_twitter
        self.text = []

        tw = twitter.Twitter()
        results = tw.statuses.user_timeline(screen_name = self.id)
        # print results

        for status in results:
            # process event_time
            date = status["created_at"].encode("utf-8").split()
            year = int(date[5])
            month = int(strptime(date[1],'%b').tm_mon)
            day = int(date[2])
            hour = int(date[3][0:2])
            minute = int(date[3][3:5])
            second = int(date[3][6:])
            event_time = datetime.datetime(year, month, day, hour, minute, second) + datetime.timedelta(hours=11)
            # print (current_time - event_time).seconds
            if (current_time - event_time).seconds > self.expire:
                return

            # process event content
            event_content = status["text"].encode("utf-8")

            event_type = event_content[len("Sydney Traffic ") : event_content.find(' -')]
            event_location = event_content[event_content.find('-')+2 : event_content.find('#')]
            event_suburb = ""
            for i in event_location.split():
                if i==i.upper():
                    if event_suburb=="":
                        event_suburb += i
                    else:
                        event_suburb += " " + i
            event_road1 = event_location[event_location.find(event_suburb)+len(event_suburb) : event_location.find("at")].strip()
            event_road2 = event_location[event_location.find("at")+3 : ].strip()

            event = {"time":event_time, "suburb":event_suburb, "type":event_type, "road1":event_road1, "road2":event_road2}
            self.text.append(event)

            # for item in self.text:
            #     print item
            # print date

        return results

    def print_events(self):
        self.obtain_traffic_from_twitter()

        for event in self.text:
            self.print_an_event(event)
            
        return

    def print_an_event(self, an_event):

        event = an_event["time"].strftime("%Y-%m-%d %H:%M:%S") + '\t' + an_event["suburb"] + '\t' + an_event["type"] + '\t' + an_event["road1"] + " x " + an_event["road2"]
        print event
        return event

    def __str__(self):
        if self.text == []:
            return "None"

        text = "[\n"
        for event in self.text:
            text = text + '\t' + event +'\n'
        text = text + ']'

        return text
