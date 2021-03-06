import os
from io import BytesIO
from PIL import Image
import numpy as np
from fraktal.functions.Palette import palettes
from fraktal.functions.Fractal import formulas


def filter_dict(d: dict, keys: list):
	return {k: v for k, v in d.items() if k in keys}


# return an image based on min-max coordinates, size, iterations, palette
def render_image(xmin: float, xmax: float, ymin: float, ymax: float, width: int, height: int,
				 palette: callable, formula: callable, verbose=False) -> Image.Image:
	# create matrix containing complex plane values
	real = np.linspace(xmin, xmax, num=width, endpoint=False, dtype=np.float64)
	imag = np.linspace(ymax, ymin, num=height, endpoint=False, dtype=np.float64) * 1j
	C = np.ravel(real + imag[:, np.newaxis]).astype(np.complex128)
	if (verbose):
		import time
		start_main = time.time()
	# calc mandelbrot set
	T = formula(C)
	if (verbose):
		end_main = time.time()
		secs = end_main - start_main
		print(secs)
	# convert values to image
	image: Image.Image = Image.fromarray(T.reshape(height, width).astype('uint8'), mode="P")
	image.putpalette(palette())
	return image


# image as png stream
def image2png(image: Image) -> bytes:
	f = BytesIO()
	image.save(f, "PNG")
	image.close()
	png = f.getvalue()
	f.close()
	return png


# generate WMS image
def generate_image_wms(p: dict) -> bytes:

	# p["fractal"]
	# p["style"]
	# p["width"]
	# p["height"]
	# p["xmin"]
	# p["xmax"]
	# p["ymin"]
	# p["ymax"]
	# and maybe
	# p["c"]

	# TODO: use smart choice for iterate_max
	p["iterate_max"] = 2560

	palette = palettes(p["iterate_max"])[p["style"]]

	accepted_args = formulas[p["fractal"]]().get_parameters().keys()
	# returns something like ('iterate_max', 'c')
	p2 = filter_dict(p, accepted_args)
	formula = formulas[p["fractal"]](**p2).calc_fractal

	# calculate rendering parameters i.e. min-max coordinates
	img = render_image(xmin=p["xmin"],
		xmax=p["xmax"],
		ymin=p["ymin"],
		ymax=p["ymax"],
		width=p["width"],
		height=p["height"],
		palette=palette,
		formula=formula)

	return image2png(img)


# generate WMTS tile
def generate_image_wmts_tile(p: dict) -> bytes:
	BASERANGE_Y = 2.0
	TILEWIDTH = 256
	TILEHEIGHT = 256

	# p["fractal"]
	# p["style"]
	# p["x_row"]
	# p["y_row"]
	# p["zoomlevel"]
	# and maybe
	# p["c"]

	# TODO: use smart choice for iterate_max
	p["iterate_max"] = 2560
	if p["zoomlevel"] > 16:
		p["iterate_max"] *= 10
	if p["zoomlevel"] > 23:
		p["iterate_max"] *= 3
	if p["zoomlevel"] > 32:
		p["iterate_max"] *= 4
	if p["zoomlevel"] > 41:
		p["iterate_max"] *= 6

	palette = palettes(p["iterate_max"])[p["style"]]

	y_range = BASERANGE_Y / (2 ** p["zoomlevel"])
	x_range = y_range * (TILEWIDTH / TILEHEIGHT)

	accepted_args = formulas[p["fractal"]]().get_parameters().keys()
	# returns something like ('iterate_max', 'c')
	p2 = filter_dict(p, accepted_args)
	formula = formulas[p["fractal"]](**p2).calc_fractal

	# calculate rendering parameters i.e. min-max coordinates
	img = render_image(xmin=p["x_row"] * x_range,
		xmax=(p["x_row"] + 1) * x_range,
		ymin=(-p["y_row"] - 1) * y_range,
		ymax=-p["y_row"] * y_range,
		width=TILEWIDTH,
		height=TILEHEIGHT,
		palette=palette,
		formula=formula)

	return image2png(img)


# render image tile(s)
def generate_image_using_center_point(p: dict) -> Image.Image:
	BASERANGE_Y = 8.0

	# p["fractal"]
	# p["center"]
	# p["width"]
	# p["height"]
	# p["zoomlevel"]
	# p["style"]
	# p["iterate_max"]
	# and maybe
	# p["c"]

	palette = palettes(p["iterate_max"])[p["style"]]

	yrange = BASERANGE_Y / (2 ** p["zoomlevel"])
	xrange = yrange * (p["width"] / p["height"])

	accepted_args = formulas[p["fractal"]]().get_parameters().keys()
	# returns something like ('iterate_max', 'c')
	p2 = filter_dict(p, accepted_args)
	formula = formulas[p["fractal"]](**p2).calc_fractal

	# calculate rendering parameters i.e. min-max coordinates
	return render_image(xmin=p["center"].real - xrange / 2,
						xmax=p["center"].real + xrange / 2,
						ymin=p["center"].imag - yrange / 2,
						ymax=p["center"].imag + yrange / 2,
						width=p["width"],
						height=p["height"],
						palette=palette,
						formula=formula)

# draw fractal images for scenes
def draw_scenes(scenes: dict = None, save: bool = True, OUTPUT_PATH = "output", verbose = False):

	# loop over list of scenes (each one contains a scene)
	for i in range(len(scenes)):
		if (verbose):
			import time
			start_main = time.time()
		image = generate_image_using_center_point(scenes[i])
		if save:
			if not (os.path.isdir(OUTPUT_PATH)):
				os.mkdir(OUTPUT_PATH)
			image.save(OUTPUT_PATH+"/"+"fractal_"+str(i)+".png")
			print("image saved:", i)
		else:
			image.show()
		image.close()
		if (verbose):
			end_main = time.time()
			secs = end_main - start_main
			print(secs)


class Drawing(object):
	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height

		# set param to some smart default values
		self.center = -0.8 - 0.1550000000291j
		self.iterate_max = 2560
		self.zoomlevel = 0
		self.style = "default"
		self.fractal = formulas["mandelbrot"]()
		#self.c = -0.79+0.135j

	def get_parameters(self) -> dict:
		return {
			"center": self.center,
			"zoomlevel": self.zoomlevel,
			"style": self.style,
			"fractal": self.fractal,
			"width": self.width,
			"height": self.height,
			**self.fractal.get_parameters()
		}

	#def __read_params__(self, params: dict):
	#	try:
	#		for key, value in params.items():
	#			setattr(self, key, value)
	#	except TypeError as err:
	#		print(err)
	#		raise Exception(str(key) + " has the wrong type!")
