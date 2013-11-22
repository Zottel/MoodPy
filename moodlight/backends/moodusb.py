import logging

import usb.core
import usb.util

#TODO: It may be cool to catch pyUSB exceptions
#      and raise Moodlight exceptions that are more readable.

moodusb_logger = logging.getLogger('moodlight.moodusb')

# Get all connected USB devices that match MoodLightUSB Vendor and Product IDs
def _usb_get_all():
	moodlights = usb.core.find(find_all=1, idVendor = 0x1d50, idProduct=0x6079)
	# LUFA HID demo USB IDs
	moodlights += usb.core.find(find_all=1, idVendor = 0x03eb, idProduct=0x204F)
	return moodlights


class InstanceUSB:
	def __init__(self, dev, serial, product, manufacturer):
		self.dev = dev
		self.serial = serial
		self.product = product
		self.manufacturer = manufacturer

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

		self.dev.set_configuration()

	def __del__(self):
		if self.reattach:
			self.dev.attach_kernel_driver(0)

	def getSerial(self):
		return self.serial;

	def getProduct(self):
		return self.product;

	def getManufacturer(self):
		return self.manufacturer;

	def sendMSG(self, msg):
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
		#print(self.dev.ctrl_transfer(CONTROL_REQUEST_TYPE_IN, HID_GET_REPORT, 0, 0, 128))


class MoodBackUSB:
	def getName(self):
		return "usb"

	# Returns a list of IDs corresponding to connected moodlights.
	def getList(self):
		results = []

		moodlights = _usb_get_all()
		
		for light in moodlights:
			serial = usb.util.get_string(light, 256, light.iSerialNumber)
			results.append(serial)
		return results

	def getInstance(self, serial):
		moodusb_logger.debug('usb_get_moodlight("%s")' % serial)
		moodlights = _usb_get_all()

		# If a serial number is given: Search all connected devices
		for light in moodlights:
			if serial == usb.util.get_string(light, 256, light.iSerialNumber):
				manufacturer = usb.util.get_string(light, 256, light.iManufacturer)
				product = usb.util.get_string(light, 256, light.iProduct)
				return InstanceUSB(light, serial, product, manufacturer)
		
		# Nothing found
		return None

