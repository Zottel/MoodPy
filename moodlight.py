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
		self._target = target
		self.bytes = [0x80, target / 256, target % 256]

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
		except usb.core.USBError as e:
			# TODO: Check for exceptions ignored even by libusb/pyusb
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

		# USB HID magic numbers
		# taken from http://www.lvr.com/hidpage.htm
		LIBUSB_ENDPOINT_IN = 0x80
		LIBUSB_ENDPOINT_OUT = 0x00
		LIBUSB_REQUEST_TYPE_CLASS = (0x01 << 5)
		LIBUSB_RECIPIENT_INTERFACE = 0x01

		CONTROL_REQUEST_TYPE_IN = LIBUSB_ENDPOINT_IN + LIBUSB_REQUEST_TYPE_CLASS + LIBUSB_RECIPIENT_INTERFACE
		CONTROL_REQUEST_TYPE_OUT = LIBUSB_ENDPOINT_OUT + LIBUSB_REQUEST_TYPE_CLASS + LIBUSB_RECIPIENT_INTERFACE

		HID_GET_REPORT = 0x01
		HID_SET_REPORT = 0x09

		# Writing message as HID report to device
		self.dev.ctrl_transfer(CONTROL_REQUEST_TYPE_OUT, HID_SET_REPORT, 0, 0, msg)
		# Reading back HID report from device
		print(self.dev.ctrl_transfer(CONTROL_REQUEST_TYPE_IN, HID_GET_REPORT, 0, 0, 128))


	def execute(self, sequence, looping = False):
		msg = [b for cmd in [x.bytes for x in sequence] for b in cmd]
		if looping:
			msg.extend([0x80, 0x00, 0x00])
		self._sendmsg(msg)

	def writeROM(self, sequence, start = 0):
		bytes = []

		for i in sequence:
			if(isinstance(i, Goto)):
				if i._target == 0:
					target = start
				else:
					target = start + sum([p.byteLength for p in sequence[:i._target - 1]])
				bytes += [0x80, target / 256, target % 256]
			else:
				bytes += i.bytes

		c = len(bytes)
		self._sendmsg([0x91, start / 256, start % 256, c] + bytes)
		return c


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

