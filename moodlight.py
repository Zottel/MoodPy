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

