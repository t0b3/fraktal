
class Julia(object):

	def __init__(self):
		self.zoom = 1
		self.step = 0.00001
		self.count = 1
		self.maxIter = 255

	def get_parameters(self):
		d = {
			"center": self.step,
			"count": self.count,
			"maxIter": self.maxIter,
			"zoom": self.zoom
		}
		return d

	def draw(self, image, height, width, param: dict):

		# setting the width, height and zoom
		# of the image to be created
		w = width
		h = height

		# creating the new image in RGB mode
		bitmap = image

		# Allocating the storage for the image and
		# loading the pixel data.
		pix = bitmap.load()

		# setting up the variables according to
		# the equation to  create the fractal
		cX, cY = -0.7, (0.27015 +(self.step * self.count))
		print(str(cY))
		moveX, moveY = 0.0, 0.0

		for x in range(w):
			for y in range(h):
				zx = 1.5 * (x - w / 2) / (0.5 * self.zoom * w) + moveX
				zy = 1.0 * (y - h / 2) / (0.5 * self.zoom * h) + moveY
				i = self.maxIter
				while zx * zx + zy * zy < 4 and i > 1:
					tmp = zx * zx - zy * zy + cX
					zy, zx = 2.0 * zx * zy + cY, tmp
					i -= 1

				# convert byte to RGB (3 bytes), kinda
				# magic to get nice colors
				pix[x, y] = (i << 21) + (i << 10) + i * 8

		# to display the created fractal
		return bitmap

	def __read_params__(self, params):
		try:
			for key, value in params.items():
				setattr(self, key, value)
		except TypeError as err:
			print(err)
			raise Exception(str(key) + " has the wrong type!")