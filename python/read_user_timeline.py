#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-user-timeline
#  - displays a user's current timeline.
#-----------------------------------------------------------------------

from twitter import *
from datetime import *
from pytz import *

# this is the user we're going to query.
user = "TrafficNSW"

# create twitter API object
twitter = Twitter()

# query the user timeline
# twitter API docs: https://dev.twitter.com/docs/api/1/get/statuses/user_timeline
results = twitter.statuses.user_timeline(screen_name = user)

print results[0]
print "(%s %s) %s" % (results[0]["created_at"], results[0]["user"]["time_zone"], results[0]["text"])

# loop through each of my statuses, and print its content
# for status in results:
#     # print "(%s) %s" % (status["created_at"], status["text"])
#     print status