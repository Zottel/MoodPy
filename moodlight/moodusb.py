import usb.core
import usb.util

#TODO: It may be cool to catch pyUSB exceptions
#      and raise Moodlight exceptions that are more readable.

# Turn a USB device into a MoodLightUSB object
def _usb_moodlight_instance(light):
	serial = usb.util.get_string(light, 256, light.iSerialNumber)
	manufacturer = usb.util.get_string(light, 256, light.iManufacturer)
	product = usb.util.get_string(light, 256, light.iProduct)
	return MoodlightUSB(light, serial, product, manufacturer)

# Get all connected USB devices that match MoodLightUSB Vendor and Product IDs
def _usb_get_all():
	moodlights = usb.core.find(find_all=1, idVendor = 0x1d50, idProduct=0x6079)
	# LUFA HID demo USB IDs
	moodlights += usb.core.find(find_all=1, idVendor = 0x03eb, idProduct=0x204F)
	return moodlights


# Returns a list with the serial numbers of all connected USB devices
def usb_list_moodlights():
	results = []

	moodlights = _usb_get_all()
	
	for light in moodlights:
		serial = usb.util.get_string(light, 256, light.iSerialNumber)
		results.append(serial)
	return results


# Get a MoodLightUSB object - either for the first one found
# or a special serial number
# (hint: use usb_list_moodlights to choose from)
def usb_get_moodlight(serial = None):
	moodlights = _usb_get_all()

	# If no serial number is given...
	if serial != None:
		if len(moodlights) > 0:
			# ... simply take the first moodlight found
			return _usb_moodlight_instance(moodlights[0])

		else:
			return None

	# If a serial number is given: Search all connected devices
	for light in moodlights:
		if serial == usb.util.get_string(light, 256, light.iSerialNumber):
			return _usb_moodlight_instance(light)
	
	# Nothing found
	return None


class MoodlightUSB:
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
		self.sendMSG([0x20, 0x00, 0x00, 0x00, 0x04, 0x00, # RGB fade to black
		              0x11, 0x00, 0x00, 0x00,             # Correct HSV value
		              0x81, 0x00, 0x00])                  # Jump to initial ROM

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
		print(self.dev.ctrl_transfer(CONTROL_REQUEST_TYPE_IN, HID_GET_REPORT, 0, 0, 128))
