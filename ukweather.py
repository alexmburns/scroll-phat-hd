#!/usr/bin/env python
#Original code by campag, updated to run on scroll-phat-hd by alexmburns.
#Additional code from dc602003, updated to operate with new BBC URLs and location codes. Added rotation for Pimoroni Scrollbot configuration. Also use pip3 and python3 to launch.

from __future__ import print_function
import subprocess
import sys
import time

try:
    import feedparser
except ImportError:
    sys.exit("This script requires the feedparser module\nInstall with: sudo pip3 install feedparser") 

import scrollphathd


scrollphathd.set_brightness(0.5)
scrollphathd.rotate(180)

# Every refresh_interval seconds we'll refresh the weather data, doesn't change too often so 30mins appropriate
pause = 0.12
ticks_per_second = 1/pause
refresh_interval = 60*30

if len(sys.argv)==2:
    location = sys.argv[1]
else:
    print("Defaulting to Colchester")
    location = "2638717" # St Neots (Enter your own Location code from BBC Weather URL between the "")

url = "http://weather-broker-cdn-api.bbci.co.uk/en/forecast/rss/3day/" + location

def get_timeout():
    return ticks_per_second * refresh_interval

def get_wet():
# Get the weather data
    print("Updating weather for", location)
    d = feedparser.parse(url)
    entries = int(len(d['entries']))
    val = "        " + d['entries'][0]['title']
    val +="        " + d['entries'][1]['title']
    val +="        " + d['entries'][2]['title']
# Tidy & shorten the message for the scroll display
    val = val.replace("Maximum", "Max")
    val = val.replace("Minimum", "Min")
    val = val.replace("Temperature: ", "")
    val = val.replace(u"\u00B0","")
    val = val.replace(",", "")
    val = val.replace("(", "")
    val = val.replace(")", "")
    return val

timeout = get_timeout()
count = 0
msg = get_wet()
scrollphathd.write_string(msg)

while True:
    try:
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(0.05)

        if(count > timeout):
            msg = get_wet()
            scrollphathd.write_string(msg)
            timeout = get_timeout()
            count = 0
        else:
            count = count+ 1
    except KeyboardInterrupt:
        scrollphathd.clear()
        sys.exit(-1)
