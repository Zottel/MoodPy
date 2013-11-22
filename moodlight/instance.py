
from moodlight.commands import Halt, SetRGB, SetHSV, FadeRGB, FadeHSV, Goto, GotoROM

class Moodlight:
	def __init__(self, device):
		self.dev = device

	def __del__(self):
		#self.sendMSG([0x20, 0x00, 0x00, 0x00, 0x04, 0x00, # RGB fade to black
		#              0x11, 0x00, 0x00, 0x00,             # Correct HSV value
		#              0x81, 0x00, 0x00])                  # Jump to initial ROM
		self.execute([FadeRGB(0x00, 0x00, 0x00, 1000),
		              SetHSV(0x00, 0x00, 0x00),
		              GotoROM(0)])

	def sendMSG(self, msg):
		self.dev.sendMSG(msg)

	def execute(self, sequence, looping = False):
		msg = [b for cmd in [x.bytes for x in sequence] for b in cmd]
		if looping:
			msg.extend([0x80, 0x00, 0x00])
		self.sendMSG(msg)

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
		self.sendMSG([0x91, start / 256, start % 256, c] + bytes)
		return c


	# Short calls for single commands:

	def setRGB(self, red, green, blue):
		self.sendMSG([0x10, red, green, blue])

	def setHSV(self, hue, value, saturation):
		self.sendMSG([0x11, hue, value, saturation])

	def fadeRGB(self, red, green, blue, duration):
		self.sendMSG([0x20, red, green, blue, duration / 256, duration % 256])

	def fadeHSV(self, hue, value, saturation, duration):
		self.sendMSG([0x21, hue, value, saturation, duration / 256, duration % 256])

	def gotoROM(self, destination):
		self.sendMSG([0x81, destination / 256, destination % 256])
