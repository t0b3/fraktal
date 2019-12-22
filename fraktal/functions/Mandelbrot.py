import numpy as np
from PIL import Image
from fraktal.functions import Palette


class Mandelbrot(object):

    def __init__(self):
        self.center = 0 + 0j
        self.iterate_max = 100
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

        # create matrix containing complex plane values
        real = np.linspace(self.center.real - 1/2/self.zoom, self.center.real + 1/2/self.zoom, num=image.width, endpoint=False)
        imag = np.linspace(self.center.imag + 1/2/self.zoom/(image.width/image.height), self.center.imag - 1/2/self.zoom/(image.width/image.height), num=image.height, endpoint=False)
        r, i = np.meshgrid(real, imag, sparse=True)
        C = r + i * 1j

        # return mandelbrot set i.e. depth values as matrix
        def mandelbrot_matrix(C):
            # init helper matrices
            Z = np.zeros_like(C)
            T = np.zeros(C.shape)
            # calculate fractal image values
            for k in range(self.iterate_max):
                M = abs(Z) < 2
                Z[M] = Z[M] ** 2 + C[M]
                T[M] = k
            return T

        T = mandelbrot_matrix(C)
        # convert values to image
        new_image = Image.fromarray(T.astype('uint8'), mode="P")
        new_image.putpalette(self.palette.get_palette())
        return new_image

    def __read_params__(self, params):
        try:
            for key, value in params.items():
                setattr(self, key, value)
        except TypeError as err:
            print(err)
            raise Exception(str(key) + " has the wrong type!")
