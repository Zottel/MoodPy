from moodlight import moodlight_list, moodlight_get

from gtk import Window, ColorSelection, main


def makeChanger(moodlight):
	def cChanged(c):
		colour = c.get_current_color()
		r, g, b = (colour.red >> 8, colour.green >> 8, colour.blue >> 8)
		#print("(%s, %s, %s)" % (r, g, b))
		moodlight.setRGB(r, g, b)
	return cChanged


for umi in moodlight_list():
	moodlight = moodlight_get(umi)
	w = Window()
	w.set_title(umi)
	c = ColorSelection()
	c.connect('color-changed', makeChanger(moodlight))
	w.add(c)
	w.show_all()

# Enter mainloop
main()