import logging

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
