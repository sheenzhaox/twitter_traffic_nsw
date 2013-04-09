# test_parse_trafficnsw_twitter_entry.py

import TrafficNSW

tnsw = TrafficNSW.TrafficNSW()

print str(tnsw)

tnsw.obtain_traffic_from_twitter()

print str(tnsw)