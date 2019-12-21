from PIL import Image
from fraktal.functions import Julia, Mandelbrot


class Drawing(object):

	def __init__(self):
		self.height = 1080
		self.width = 1900

	def mandelbrot(self, save=True, count: int = 1, step: float = 0.001):
		bitmap = Image.new("RGB", (self.width, self.height), "white")
		for x in range(1, count):
			m = Julia.Julia()
			bitmap = m.draw(bitmap, self.height, self.width, count=x, step=step)
			if save:
				bitmap.save("mandelbrot"+str(x)+".jpg")
			else:
				bitmap.show()

	def mandelbrot2(self, save=True, count: int = 1, step: float = 0.001):
		bitmap = Image.new("RGB", (self.width, self.height), "white")
		for x in range(0, count):
			d = {
				"center": (1.5, 1.5),
				"iterate_max": 100,
				"colors_max": 50,
				"zoom": 1.5
			}
			m = Mandelbrot.Mandelbrot()
			bitmap = m.draw(bitmap, self.height, self.width, d)
			if save:
				bitmap.save("mandelbrot_2"+str(x)+".jpg")
			else:
				bitmap.show()
