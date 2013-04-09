# test_parse_trafficnsw_twitter_entry.py

import TrafficNSW

tnsw = TrafficNSW.TrafficNSW()

events = tnsw.parse_trafficnsw_twitter_entry(TrafficNSW.TrafficNSW.obtain_twitter_raw_data())
for event in events:
    print event.values()