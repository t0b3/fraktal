import os
from PIL import Image
from fraktal.functions import Palette, Fractal


# generate WMTS tile
def generate_image_wmts_tile(p: dict) -> Image.Image:
    BASERANGE_Y = 2.0
    TILEWIDTH = 256
    TILEHEIGHT = 256

    # TODO: fractal = p["fractal"]
    fractal = Fractal.Mandelbrot()
    # p["x_row"]
    # p["y_row"]
    # p["zoomlevel"]
    # p["style"]

    # TODO: use smart choice for iterate_max
    iterate_max = 2560
    if p["zoomlevel"] > 16:
        iterate_max *= 10
    if p["zoomlevel"] > 23:
        iterate_max *= 3
    if p["zoomlevel"] > 32:
        iterate_max *= 4
    if p["zoomlevel"] > 41:
        iterate_max *= 6

    palette = Palette.palettes(iterate_max)[p["style"]]

    y_range = BASERANGE_Y / (2 ** p["zoomlevel"])
    x_range = y_range * (TILEWIDTH / TILEHEIGHT)

    # calculate rendering parameters i.e. min-max coordinates
    return fractal.render_image(xmin=p["x_row"] * x_range,
                                xmax=(p["x_row"] + 1) * x_range,
                                ymin=(-p["y_row"] - 1) * y_range,
                                ymax=-p["y_row"] * y_range,
                                width=TILEWIDTH,
                                height=TILEHEIGHT,
                                iterate_max=iterate_max,
                                palette=palette)



class Drawing(object):

	def __init__(self, width: int, height: int):
		self.OUTPUT_PATH = "output"
		self.BASERANGE_Y = 8.0
		self.width = width
		self.height = height
		self.center = -0.8 - 0.1550000000291j
		#self.c = -0.79+0.135j
		self.iterate_max = 2560
		self.zoom = 0
		self.style = "default"
		self.fractal = Fractal.Mandelbrot()

	def get_parameters(self) -> dict:
		return {
			"center": self.center,
			"iterate_max": self.iterate_max,
			"zoom": self.zoom,
			"style": self.style,
			"fractal": self.fractal
		}

	# draw fractal images for selected params
	def draw(self, save: bool = True, params: dict = None):

		# render image tile(s)
		def render_perspective(par: dict) -> Image.Image:
			self.__read_params__(par)

			palette = Palette.palettes(self.iterate_max)[self.style]

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
											 palette=palette)

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
				if not (os.path.isdir(self.OUTPUT_PATH)):
					os.mkdir(self.OUTPUT_PATH)
				image.save(self.OUTPUT_PATH+"/"+"fractal_"+str(i)+".png")
				print("image saved:", i)
			else:
				image.show()
			image.close()

	def __read_params__(self, params: dict):
		try:
			for key, value in params.items():
				setattr(self, key, value)
		except TypeError as err:
			print(err)
			raise Exception(str(key) + " has the wrong type!")
