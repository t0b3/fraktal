import numpy as np
from PIL import Image

# abstract class: DO NOT USE! - use child classes instead
class Fractal(object):
    def __init__(self):
        self.iterate_max = 100

    # return an image based on min-max coordinates, size, iterations, palette
    def render_image(self, xmin: float, xmax: float, width: int,
                     ymin: float, ymax: float, height: int,
                     iterate_max: int, palette: list) -> Image.Image:
        # create matrix containing complex plane values
        real = np.linspace(xmin, xmax, num=width, endpoint=False)
        imag = np.linspace(ymax, ymin, num=height, endpoint=False)
        r, i = np.meshgrid(real, imag, sparse=True)
        C = r + i * 1j
        # calc mandelbrot set
        T = self.fractal_matrix(C, {"iterate_max": iterate_max})
        # convert values to image
        image: Image.Image = Image.fromarray(T.astype('uint8'), mode="P")
        image.putpalette(palette)
        return image

    def get_parameters(self) -> dict:
        return {
            "iterate_max": self.iterate_max,
        }

    def __read_params__(self, params: dict):
        try:
            for key, value in params.items():
                setattr(self, key, value)
        except TypeError as err:
            print(err)
            raise Exception(str(key) + " has the wrong type!")


class Mandelbrot(Fractal):

    # return mandelbrot set i.e. depth values as matrix
    def fractal_matrix(self, C: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

        # init helper matrices
        Z = np.zeros_like(C)
        T = np.zeros(C.shape)
        # calculate fractal image values
        for k in range(self.iterate_max):
            M = abs(Z) < 2
            Z[M] = Z[M] ** 2 + C[M]
            T[M] = k
        return T

class Julia(Fractal):
    def __init__(self):
        super().__init__()
        self.c = -0.8+0.155j

    # return julia set i.e. depth values as matrix
    def fractal_matrix(self, Z: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

        # init helper matrices
        T = np.zeros(Z.shape)
        # calculate fractal image values
        for k in range(self.iterate_max):
            M = abs(Z) < 2
            Z[M] = Z[M] ** 2 + self.c
            T[M] = k
        return T

    def get_parameters(self) -> dict:
        d = super().get_parameters()
        d["c"] = self.c
        return d
