from PIL import Image
from fraktal.functions import Palette, Fractal


class Drawing(object):

	def __init__(self, screen_width: int, screen_height: int):
		self.width = screen_width / 2
		self.height = screen_height
		self.center = -0.8 - 0.155j
		self.iterate_max = 2560
		self.zoom = 24 / 4.5
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

			# calculate rendering parameters i.e. min-max coordinates
			return self.fractal.render_image(width=self.width,
											 height=self.height,
											 xmin=self.center.real - 1 / 2 / self.zoom,
											 xmax=self.center.real + 1 / 2 / self.zoom,
											 ymin=self.center.imag - 1 / 2 / self.zoom / (self.width / self.height),
											 ymax=self.center.imag + 1 / 2 / self.zoom / (self.width / self.height),
											 iterate_max=self.iterate_max,
											 palette=self.palette)

		# list of default params (in fact it's a nested dict)
		if params is None:
			#self.fractal = Fractal.Julia()
			params = { "0": self.get_parameters(),
					   "1": self.get_parameters(),
					   "2": self.get_parameters(),
					   "3": self.get_parameters(),
					   "4": self.get_parameters(),
					   "5": self.get_parameters(),
					   "6": self.get_parameters(),
					   "7": self.get_parameters(),
					   "8": self.get_parameters(),
					   "9": self.get_parameters(),
					   "10": self.get_parameters(),
					   "11": self.get_parameters(),
					   "12": self.get_parameters(),
					   "13": self.get_parameters(),
					   "14": self.get_parameters(),
					   "100": self.get_parameters(),
					   "101": self.get_parameters(),
					   "102": self.get_parameters(),
					   "103": self.get_parameters(),
					   "104": self.get_parameters(),
					   "105": self.get_parameters(),
					   "106": self.get_parameters(),
					   "107": self.get_parameters(),
					   "108": self.get_parameters(),
					   "109": self.get_parameters(),
					   "110": self.get_parameters(),
					   "111": self.get_parameters(),
					   "112": self.get_parameters(),
					   "113": self.get_parameters(),
					   "114": self.get_parameters() }
			params["0"]["zoom"] = 1 / 4.5
			params["1"]["zoom"] = 2 / 4.5
			params["2"]["zoom"] = 4 / 4.5
			params["3"]["zoom"] = 8 / 4.5
			params["4"]["zoom"] = 16 / 4.5
			params["5"]["zoom"] = 32 / 4.5
			params["6"]["zoom"] = 64 / 4.5
			params["7"]["zoom"] = 128 / 4.5
			params["8"]["zoom"] = 256 / 4.5
			params["9"]["zoom"] = 512 / 4.5
			params["10"]["zoom"] = 1024 / 4.5
			params["11"]["zoom"] = 2048 / 4.5
			params["12"]["zoom"] = 4096 / 4.5
			params["13"]["zoom"] = 8192 / 4.5
			params["14"]["zoom"] = 16284 / 4.5
			params["100"]["zoom"] = 1 / 4.5
			params["101"]["zoom"] = 2 / 4.5
			params["102"]["zoom"] = 4 / 4.5
			params["103"]["zoom"] = 8 / 4.5
			params["104"]["zoom"] = 16 / 4.5
			params["105"]["zoom"] = 32 / 4.5
			params["106"]["zoom"] = 64 / 4.5
			params["107"]["zoom"] = 128 / 4.5
			params["108"]["zoom"] = 256 / 4.5
			params["109"]["zoom"] = 512 / 4.5
			params["110"]["zoom"] = 1024 / 4.5
			params["111"]["zoom"] = 2048 / 4.5
			params["112"]["zoom"] = 4096 / 4.5
			params["113"]["zoom"] = 8192 / 4.5
			params["114"]["zoom"] = 16284 / 4.5
			params["100"]["fractal"] = Fractal.Julia()
			params["101"]["fractal"] = Fractal.Julia()
			params["102"]["fractal"] = Fractal.Julia()
			params["103"]["fractal"] = Fractal.Julia()
			params["104"]["fractal"] = Fractal.Julia()
			params["105"]["fractal"] = Fractal.Julia()
			params["106"]["fractal"] = Fractal.Julia()
			params["107"]["fractal"] = Fractal.Julia()
			params["108"]["fractal"] = Fractal.Julia()
			params["109"]["fractal"] = Fractal.Julia()
			params["110"]["fractal"] = Fractal.Julia()
			params["111"]["fractal"] = Fractal.Julia()
			params["112"]["fractal"] = Fractal.Julia()
			params["113"]["fractal"] = Fractal.Julia()
			params["114"]["fractal"] = Fractal.Julia()


		# loop over "list" of params (each one contains a scene)
		for i, par in params.items():
			image = render_perspective(par)
			if save:
				image.save("fractal_"+i+".png")
				print("image saved: "+i)
			else:
				image.show()

	def __read_params__(self, params: dict):
		try:
			for key, value in params.items():
				setattr(self, key, value)
		except TypeError as err:
			print(err)
			raise Exception(str(key) + " has the wrong type!")
