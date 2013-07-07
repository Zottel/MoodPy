======
MoodPy
======

It's a Py!
----------

About
-----
MoodPy is a python library to interface the MoodlightUSB.

Todo
----
- Functions to enumerate/get connected Moodlight devices.
  
  Each Moodlight has a unique serial number, which, when implemented in
  the library, allows application to assign specific functions to each one.
- Handling of disconnects?
  
  Try to reconnect to same serial number on interaction?
- Implement a daemon?
  
  Generic Event -> Light framework?
- Wait for MoodFirmware EEPROM Programming capability and allow applications
  to push sequences.
- Gather information on how to interface with various applications


Sequence Programming
--------------------

Applications may send whole colour changing sequences to the Moodlight.

Fade through HSV colours infinitely::

	from moodlight import Moodlight, SetHSV, FadeHSV

	m = Moodlight()

	sequence = [
		SetHSV(0x00, 0xff, 0xff),
		FadeHSV(0xff, 0xff, 0xff, 1000)
	]
	m.execute(sequence, looping = True)


Blink red thrice::

	from moodlight import Moodlight, FadeRGB

	m = Moodlight()

	sequence = [
		FadeRGB(0xff, 0x00, 0x00, 1000),
		FadeRGB(0x00, 0x00, 0x00, 1000),
		FadeRGB(0xff, 0x00, 0x00, 1000),
		FadeRGB(0x00, 0x00, 0x00, 1000),
		FadeRGB(0xff, 0x00, 0x00, 1000),
		FadeRGB(0x00, 0x00, 0x00, 1000)
	]
	m.execute(sequence)

