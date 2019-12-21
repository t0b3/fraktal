import colorsys

class Int2Color:
        def __init__(self, colors_max = 100):
            self.colors_max = colors_max

            self.palette = [0] * self.colors_max
            for i in range(1, self.colors_max):
                f = 1 - abs((float(i) / self.colors_max - 1) ** 15)
                r, g, b = colorsys.hsv_to_rgb(.66 + f / 3, 1 - f / 2, f)
                self.palette[i] = (int(r * 255), int(g * 255), int(b * 255))

        def int2color(self, input):
            return self.palette[int(input * (self.colors_max - 1))]

