#!/usr/bin/python

import twitter
import datetime
from time import strptime
# from pprint import pprint


class TrafficNSW:
    def __init__(self, screen_name="TrafficNSW"):
        # self["name"] = screen_name
        self.id = screen_name
        self.text = []
        self.last_time_obtain_from_twitter = datetime.datetime(2000, 1, 1)

    def get_screen_name(self):
        return self.id

    def get_traffic_info(self):
        return self.text

    def get_latest_event(self):
        self.obtain_traffic_from_twitter()
        curr_status = self.text[0]
        return self.print_an_event(curr_status)

    def obtain_traffic_from_twitter(self):

        '''
        The following block is to test if the twitter query happened in the
        last 10 minutes. If so, just return. Otherwise, it will do a new query.
        '''
        current_time = datetime.datetime.now()
        time_diff = (current_time - self.last_time_obtain_from_twitter).seconds
        if time_diff < 1800:
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
            month  = int(strptime(date[1],'%b').tm_mon)
            day = int(date[2])
            hour = int(date[3][0:2])
            minute = int(date[3][3:5])
            second = int(date[3][6:])
            event_time = datetime.datetime(year, month, day, hour, minute, second) + datetime.timedelta(hours=11)
            # print (current_time - event_time).seconds
            if (current_time - event_time).seconds > 3600:
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

    # @staticmethod
    def print_an_event(self, an_event):
        print an_event["time"].strftime("%Y-%m-%d %H:%M:%S") + '\t' + an_event["suburb"] + '\t' + an_event["type"] + '\t' + an_event["road1"] + " x " + an_event["road2"]

