import numpy as np
from PIL import Image
from fraktal.functions import Palette


class Mandelbrot(object):

    def __init__(self):
        self.center = 0 + 0j
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
        #d = image.load()
        step = 1 / self.zoom / image.width

        # calculate the mandelbrot sequence for the point c with start value z
        #def iterate_mandelbrot(c: complex, z: complex = 0) -> int:
        #    for n in range(self.iterate_max):
        #        z = z ** 2 + c
        #        if abs(z) > 2:
        #            return n + 1
        #    return 0
        #
        # draw fractal image
        #for y in range(image.height):
        #    for x in range(image.width):
        #        c = self.center + complex(x, y) * step
        #        n = iterate_mandelbrot(c)  # use this for Mandelbrot set
        #        d[x, y] = self.palette.int2color(n)
        #del d
        #return image

        # draw fractal image
        real = np.linspace(self.center.real - 1/2/self.zoom, self.center.real + 1/2/self.zoom, num=image.width, endpoint=False)
        imag = np.linspace(self.center.imag + 1/2/self.zoom/(image.width/image.height), self.center.imag - 1/2/self.zoom/(image.width/image.height), num=image.height, endpoint=False)
        #print("real: ", real[0], "...", real[-1], " - ", len(real), " > ", real[1]-real[0])
        #print("imag: ", imag[0], "...", imag[-1], " - ", len(imag), " > ", imag[1]-imag[0])
        r, i = np.meshgrid(real, imag, sparse=True)
        C = r + i * 1j
        #print(C[0,0], "...", C[-1,-1])
        Z = np.zeros_like(C)
        T = np.zeros(C.shape)
        #
        for k in range(self.iterate_max):
            M = abs(Z) < 2
            Z[M] = Z[M] ** 2 + C[M]
            T[M] = k + 1
        #print(np.min(T,None))
        #print(np.max(T,None))
        new_image = Image.fromarray(T.astype('uint8'), mode="P")
        self.palette.get_palette()
        new_image.putpalette(self.palette.get_palette())
        #del d
        return new_image
        #for y in range(image.height):
        #    for x in range(image.width):
        #        d[x, y] = self.palette.int2color(int(T[y, x]))
        #del d
        #return image

    def __read_params__(self, params):
        try:
            for key, value in params.items():
                setattr(self, key, value)
        except TypeError as err:
            print(err)
            raise Exception(str(key) + " has the wrong type!")
