from PIL import Image
from fraktal.functions import Palette, Fractal


class Drawing(object):

	def __init__(self, screen_width: int, screen_height: int):
		self.BASERANGE_Y = 8.0
		self.width = int(screen_width / 2)
		self.height = screen_height
		self.center = -0.8 - 0.1550000000291j
		#self.c = -0.79+0.135j
		self.iterate_max = 2560
		self.zoom = 0
		self.palette = Palette.Palette(self.iterate_max).get_palette()
		self.fractal = Fractal.Mandelbrot()

	def get_parameters(self) -> dict:
		return {
			"center": self.center,
			"iterate_max": self.iterate_max,
			"zoom": self.zoom,
			"palette": self.palette,
			"fractal": self.fractal
		}

	# draw fractal images for selected params
	def draw(self, save: bool = True, params: dict = None):

		# render image tile(s)
		def render_perspective(par: dict) -> Image.Image:
			self.__read_params__(par)

			yrange = self.BASERANGE_Y / (2 ** self.zoom)
			xrange = yrange * (self.width / self.height)

			# calculate rendering parameters i.e. min-max coordinates
			return self.fractal.render_image(xmin=self.center.real - xrange / 2,
											 xmax=self.center.real + xrange / 2,
											 ymin=self.center.imag - yrange / 2,
											 ymax=self.center.imag + yrange / 2,
											 width=self.width,
											 height=self.height,
											 iterate_max=self.iterate_max,
											 palette=self.palette)

		# list of default params
		if params is None:
			params = list()
			for i in range(47):
				self.zoom = i
				params.append(self.get_parameters())

			self.fractal = Fractal.Julia(c = -0.79+0.135j)
			self.center = +0.4938793215408734 - 0.15j
			for i in range(47):
				self.zoom = i
				params.append(self.get_parameters())

			self.fractal = Fractal.Mandelbrot4()
			for i in range(8):
				self.zoom = i
				params.append(self.get_parameters())

			self.fractal = Fractal.Julia4(c = -0.78+0.115j)
			for i in range(8):
				self.zoom = i
				params.append(self.get_parameters())


		# loop over list of params (each one contains a scene)
		for i in range(len(params)):
			image = render_perspective(params[i])
			if save:
				image.save("fractal_"+str(i)+".png")
				print("image saved:", i)
			else:
				image.show()

	def __read_params__(self, params: dict):
		try:
			for key, value in params.items():
				setattr(self, key, value)
		except TypeError as err:
			print(err)
			raise Exception(str(key) + " has the wrong type!")
