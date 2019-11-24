from PIL import Image
from fraktal.functions import Mandelbrot


class Drawing(object):

	def __init__(self):
		self.height = 1080
		self.width = 1900

		self.bitmap = Image.new("RGB", (self.width, self.height), "white")

	def mandelbrot(self, save=True):
		m = Mandelbrot.draw(self.bitmap, self.height, self.width)
		if save:
			m.save("mandelbrot.jpg")

