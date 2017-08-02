#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import font5x7smoothed

print ("This is a test script")

scrollphathd.write_string(" Of Course You Can!", x=0, y=0, font=font5x7smoothed, letter_spacing=1, brightness=0.5, monospaced=False, fill_background=False)

while True:
	scrollphathd.show()
	scrollphathd.scroll()
	time.sleep(0.05)
