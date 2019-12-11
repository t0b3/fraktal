#!/usr/bin/python
import colorsys


class Mandelbrot(object):

    def __init__(self):
        self.center = (2.2, 1.5)       # Use this for Mandelbrot set
        #self.center = (1.5, 1.5)       # Use this for Julia set
        self.iterate_max = 1000
        self.colors_max = 100
        self.zoom = 1.0

    def get_parameters(self):
        d = {
            "center": self.center,
            "iterate_max": self.iterate_max,
            "colors_max": self.colors_max,
            "zoom": self.zoom
        }
        return d

    def draw(self, image, height, width, param: dict):
        self.__read_params__(param)
        img = image
        d = image.load()
        scale = self.zoom / (width / 3)

        # Calculate a tolerable palette
        palette = [0] * self.colors_max
        for i in range(1, self.colors_max):
            f = 1-abs((float(i)/self.colors_max-1)**15)
            r, g, b = colorsys.hsv_to_rgb(.66+f/3, 1-f/2, f)
            palette[i] = (int(r*255), int(g*255), int(b*255))

        # Calculate the mandelbrot sequence for the point c with start value z
        def iterate_mandelbrot(c, z = 0):
            for n in range(1, self.iterate_max + 1):
                z = z*z +c
                if abs(z) > 2:
                    return n
            return None

        # Draw our image
        for y in range(1, height):
            for x in range(1, width):
                c = complex(x * scale - self.center[0], y * scale - self.center[1])

                n = iterate_mandelbrot(c)            # Use this for Mandelbrot set
                #n = iterate_mandelbrot(complex(0.3, 0.6), c)  # Use this for Julia set

                if n is None:
                    v = 1
                else:
                    v = n/100.0

                #d.point((x, y), fill = palette[int(v * (self.colors_max-1))])
                d[x, y] = palette[int(v * (self.colors_max - 1))]
        del d
        return img

    def __read_params__(self, params):
        try:
            for key, value in params.items():
                setattr(self, key, value)
        except TypeError as err:
            print(err)
            raise Exception(str(key) + " has the wrong type!")

