import sys
import usb.core
import usb.util
import pprint

class Halt:
	def __init__(self):
		self.byteLength = 1
		self.bytes = [0x00]


class SetRGB:
	def __init__(self, red, green, blue):
		self.byteLength = 4
		self.bytes = [0x10, red, green, blue]
	

class SetHSV:
	def __init__(self, hue, saturation, value):
		self.byteLength = 4
		self.bytes = [0x11, hue, saturation, value]
	

class FadeRGB:
	def __init__(self, red, green, blue, duration):
		self.byteLength = 6
		self.bytes = [0x20, red, green, blue, duration / 256, duration % 256]
	

class FadeHSV:
	def __init__(self, hue, saturation, value, duration):
		self.byteLength = 6
		self.bytes = [0x21, hue, saturation, value, duration / 256, duration % 256]
	

class Goto:
	def __init__(self, target):
		self.byteLength = 3
		raise Exception("Not implemented")

class GotoROM:
	def __init__(self, target):
		self.byteLength = 3
		self.bytes = [0x81, target / 256, target % 256]
	

class Moodlight:
	def __init__(self):
		# Find device
		self.dev = usb.core.find(idVendor=0x1d50, idProduct=0x6079)
		if self.dev is None:
			raise Exception("No matching device found")

		manufacturer = usb.util.get_string(self.dev, 256, self.dev.iManufacturer)
		product = usb.util.get_string(self.dev, 256, self.dev.iProduct)
		serial = usb.util.get_string(self.dev, 256, self.dev.iSerialNumber)
		print(manufacturer, product, serial)
		print(manufacturer == u'Q-Rai')
		print(product == u'MoodLightUSB')

		# Attempt to take device away from kernel
		self.reattach = False
		try:
			if self.dev.is_kernel_driver_active(0):
				reattach = True
				try:
					self.dev.detach_kernel_driver(0)
				except usb.core.USBError as e:
					raise Exception("Could not detatch kernel driver: %s" % str(e))
		except USBError as e:
			print(e)

		#
		self.dev.set_configuration()

	def __del__(self):
		self._sendmsg([0x20, 0xcc, 0x00, 0x00, 0x10, 0x00, 0x81, 0x00, 0x00])
		if self.reattach:
			self.dev.attach_kernel_driver(0)
		pass

	def _sendmsg(self, msg):
		print(msg)
		self.dev.ctrl_transfer(0x21,0x09,0,0,msg)

	def execute(self, sequence, looping = False):
		msg = [b for cmd in [x.bytes for x in sequence] for b in cmd]
		if looping:
			msg.extend([0x80, 0x00, 0x00])
		self._sendmsg(msg)
	# Short calls for single commands:

	def setRGB(self, red, green, blue):
		self._sendmsg([0x10, red, green, blue])

	def setHSV(self, hue, value, saturation):
		self._sendmsg([0x11, hue, value, saturation])

	def fadeRGB(self, red, green, blue, duration):
		self._sendmsg([0x20, red, green, blue, duration / 256, duration % 256])

	def fadeHSV(self, hue, value, saturation, duration):
		self._sendmsg([0x21, hue, value, saturation, duration / 256, duration % 256])

	def gotoROM(self, destination):
		self._sendmsg([0x81, destination / 256, destination % 256])

