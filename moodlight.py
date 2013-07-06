import sys
import usb.core
import usb.util



class Moodlight:
	def __init__(self):
		# Find device
		self.dev = usb.core.find(idVendor=0x03eb, idProduct=0x204f)
		if self.dev is None:
			raise Exception("No matching device found")

		# Attempt to take device away from kernel
		self.reattach = False
		if self.dev.is_kernel_driver_active(0):
			reattach = True
			try:
				self.dev.detach_kernel_driver(0)
			except usb.core.USBError as e:
				raise Exception("Could not detatch kernel driver: %s" % str(e))

		#
		self.dev.set_configuration()

	def __del__(self):
		if self.reattach:
			self.dev.attach_kernel_driver(0)
		pass

	def _sendmsg(self, msg):
		print(self.dev.ctrl_transfer(0x21,0x09,0,0,msg))

	def setRGB(self, red, green, blue):
		self._sendmsg([0x10, red, green, blue])

	def setHSV(self, hue, value, saturation):
		self._sendmsg([0x11, hue, value, saturation])

	def fadeRGB(self, red, green, blue, duration):
		self._sendmsg([0x20, red, green, blue, duration / 256, duration % 256])

	def fadeHSV(self, hue, value, saturation, duration):
		self._sendmsg([0x21, hue, value, saturation, duration / 256, duration % 256])

