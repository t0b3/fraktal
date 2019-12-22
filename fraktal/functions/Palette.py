import colorsys


class Palette:
    def __init__(self, colors_max: int = 256):
        self.colors_max = colors_max

        # create a tolerable palette in a list
        self.palette = [0] * self.colors_max
        for i in range(self.colors_max):
            f = 1 - abs((float(i) / self.colors_max - 1) ** 15)
            r, g, b = colorsys.hsv_to_rgb(.66 + f / 3, 1 - f / 2, f)
            self.palette[i] = (int(r * 255), int(g * 255), int(b * 255))
        # set inf (last) to black
        self.palette[colors_max-1] = (int(0),int(0),int(0))

    # return RGB-color tuple for unsigned integer input
    def int2color(self, input: int) -> tuple:
        return self.palette[min(input, self.colors_max - 1)]
