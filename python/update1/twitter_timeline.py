    #!/usr/bin/python

# The twitter module is from https://pypi.python.org/pypi/twitter
import twitter

from datetime import datetime


class TwitterTimeline(object):
    ''' A class to read timeline from a given twitter user.
    '''


    def __init__(self, screen_name="TrafficNSW", expire = 60):
        ''' (TrafficNSW, str, int) -> TrafficNSW

        RETURN :    an initiated TrafficNSW object.
        PARAMETER : 
            screen_name - the username in twitter
            expire - seconds. If the last twitter query happened before 
                        expire timer, it will re-query from twitter.
        '''

        # The id of the user
        self.id = screen_name

        # The expiry timer
        self.expire = expire

        # The timeline entries obtained from twitter
        self.text = []

        # The last timestamp to enquiry timeline information from twitter
        self.last_query_time = datetime(2000, 1, 1)


    def get_screen_name(self):
        ''' (TrafficNSW) -> str

        RETURN :    the id of the user
        '''
        return self.id


    def get_timelines(self):
        ''' (TwitterTimeline) -> list

        RETURN :    The timeline got from twitter.
        DESC :      If the last query happened beyond the expire timer or 
                    no timeline found previously, the program will perform a 
                    query_timeline_raw_data() function and store the output in 
                    self.text, and update self.last_query_time.
        '''

        current_time = datetime.now()

        if self.text==[] or \
        (current_time - self.last_query_time).seconds >= self.expire :
            self.text = TwitterTimeline.query_timeline_raw_data(self.id)
            self.last_query_time = current_time

        return self.text


    def get_latest_timeline(self):
        ''' (TwitterTimeline) -> dictionary

        RETURN :    The 1st timeline got from twitter.
        '''

        self.get_timelines()
        
        if self.text != []:
            return self.text[0]

        return None


    @staticmethod
    def query_timeline_raw_data(id):
        ''' (str) -> list
        RETURN :    The timeline of a given user in format of raw data (list).
        PARAMETER :
            id - (str) user id.
        '''

        tw = twitter.Twitter(api_version='1')
        results = tw.statuses.user_timeline(screen_name = id)

        return results


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

    tw = TwitterTimeline()

    tw.get_timelines()
    print str(tw)
