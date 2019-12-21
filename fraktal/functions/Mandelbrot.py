from fraktal.functions import Palette


class Mandelbrot(object):

    def __init__(self):
        self.center = -2.2 - 1.5j  # use this for Mandelbrot set
        self.iterate_max = 1000
        self.zoom = 1 / 4.5
        self.palette = Palette.Palette(self.iterate_max)

    def get_parameters(self) -> dict:
        return {
            "center": self.center,
            "iterate_max": self.iterate_max,
            "zoom": self.zoom,
            "palette": self.palette
        }

    def draw(self, image, param: dict):
        self.__read_params__(param)
        d = image.load()
        step = 1 / self.zoom / image.width

        # calculate the mandelbrot sequence for the point c with start value z
        def iterate_mandelbrot(c: complex, z: complex = 0) -> int:
            for n in range(self.iterate_max):
                z = z ** 2 + c
                if abs(z) > 2:
                    return n + 1
            return 0

        # draw fractal image
        for y in range(image.height):
            for x in range(image.width):
                c = self.center + complex(x, y) * step
                n = iterate_mandelbrot(c)  # use this for Mandelbrot set
                d[x, y] = self.palette.int2color(n)
        del d
        return image

    def __read_params__(self, params):
        try:
            for key, value in params.items():
                setattr(self, key, value)
        except TypeError as err:
            print(err)
            raise Exception(str(key) + " has the wrong type!")
