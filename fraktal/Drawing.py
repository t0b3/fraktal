from PIL import Image
from fraktal.functions import Julia, Mandelbrot, Palette


class Drawing(object):

	def __init__(self):
		self.height = 1080
		self.width = 1900

#	def mandelbrot(self, save=True, count: int = 1):
#		bitmap = Image.new("RGB", (self.width, self.height), "white")
#		for x in range(count):
#			m = Julia.Julia()
#			bitmap = m.draw(bitmap, count=x)
#			if save:
#				bitmap.save("mandelbrot"+str(x)+".jpg")
#			else:
#				bitmap.show()

	def mandelbrot(self, save: bool = True, count: int = 1):
		bitmap = Image.new("RGB", (self.width, self.height), "white")
		for x in range(count):
			par = {
				"center": -2.2 -1.5j,
				"iterate_max": 100,
				"zoom": 1/4.5
			}
			par["palette"] = Palette.Palette(par["iterate_max"])
			m = Mandelbrot.Mandelbrot()
			bitmap = m.draw(bitmap, par)
			if save:
				bitmap.save("mandelbrot_2"+str(x)+".jpg")
			else:
				bitmap.show()
