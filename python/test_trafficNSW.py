#!/usr/bin/python

import TrafficNSW

tnsw = TrafficNSW.TrafficNSW()

# tnsw.obtain_traffic_from_twitter()
# tnsw.obtain_traffic_from_twitter()

tnsw.get_latest_event()
tnsw.print_events()