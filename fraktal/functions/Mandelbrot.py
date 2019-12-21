from fraktal.functions.int2color import Int2Color

class Mandelbrot(object):

    def __init__(self):
        self.center = (2.2, 1.5)       # Use this for Mandelbrot set
        #self.center = (1.5, 1.5)       # Use this for Julia set
        self.iterate_max = 1000
        self.zoom = 1.0

    def get_parameters(self):
        d = {
            "center": self.center,
            "iterate_max": self.iterate_max,
            "zoom": self.zoom
        }
        return d

    def draw(self, image, height, width, param: dict):
        self.__read_params__(param)
        img = image
        d = image.load()
        scale = self.zoom / (width / 3)
        int2col = Int2Color(100)

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
                #d[x, y] = palette[int(v * (self.colors_max - 1))]
                d[x, y] = int2col.int2color(v)
        del d
        return img

    def __read_params__(self, params):
        try:
            for key, value in params.items():
                setattr(self, key, value)
        except TypeError as err:
            print(err)
            raise Exception(str(key) + " has the wrong type!")

