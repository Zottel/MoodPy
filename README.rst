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

