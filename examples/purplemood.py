#!/usr/bin/env python2

# mostly taken from https://developer.pidgin.im/wiki/DbusHowto

import dbus, gobject, os
from dbus.mainloop.glib import DBusGMainLoop

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 

from moodlight import moodlight_get

m = moodlight_get()

def my_func(account, sender, message, conversation, flags):
  m.setRGB(0xff, 0x00, 0x00)
  m.fadeRGB(0x00, 0x00, 0x00, 8000)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

bus.add_signal_receiver(my_func,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")

loop = gobject.MainLoop()
loop.run()
