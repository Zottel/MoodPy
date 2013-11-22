import logging

moodlight_logger = logging.getLogger('moodlight')
moodlight_logger.setLevel(logging.DEBUG)
moodlight_logger.addHandler(logging.StreamHandler())

from moodlight.commands import Halt, SetRGB, SetHSV, FadeRGB, FadeHSV, Goto, GotoROM
from moodlight.instance import Moodlight


# List of all available backends
moodlight_backends = {}


# USB backend
try:
	from moodlight.backends.moodusb import MoodBackUSB
	moodlight_backends['usb'] = MoodBackUSB()
except ImportError:
	moodlight_logger.exception('Could not load USB Backend')


# Returns a list
# UMI: Uniform Moodlight Identifier
# Format: <backend>://<id>
def moodlight_list():
	umis = []

	# Add all devices prepended with "<prefix>://" to the list
	# <prefix> being the (short) name of their Backend
	for b in moodlight_backends:
		umis.extend([b + '://' + dev for dev in  moodlight_backends[b].getList()])

	return umis


# Get the moodlight with a specific umi
def moodlight_get(umi = None):
	# If no UMI is given, use the first one available
	if umi is None:
		ml = moodlight_list()
		if not len(ml) > 0:
			logging.warn('Moodlight requested tho no device could be found')
			raise
		else:
			umi = ml[0]

	# Parse, get device from backend and return Moodlight instance
	params = umi.split("://", 1)
	dev = moodlight_backends[params[0]].getInstance(params[1])
	return Moodlight(dev)

