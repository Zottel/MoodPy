#!/usr/bin/env python2.7
import os
import time

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 

from moodlight import Moodlight

if __name__ == '__main__':
	mood = Moodlight()
	ip = "z0ttel.gempai.de"

	while True:
		time.sleep(1)
		if os.system("ping -c 1 -W 1 %s" % ip) == 0:
			mood.fadeHSV(0x55, 0xff, 0xff, 1000)
		else:
			mood.fadeHSV(0x00, 0xff, 0xff, 1000)


