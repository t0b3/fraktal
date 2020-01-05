import colorsys
from typing import List


class Palette(object):
    def __init__(self, colors_max: int = 256):
        colors_max = min(colors_max, 256)
        self.palette = {}

        # create a pink gradient palette
        palette: List[int] = []
        for i in range(colors_max-1):
            f = 1 - abs((float(i) / colors_max - 1) ** 15)
            r, g, b = colorsys.hsv_to_rgb(.66 + f / 3, 1 - f / 2, f)
            palette.extend([int(r * 255), int(g * 255), int(b * 255)])
        # set inf (last) to black
        palette.extend([0,0,0])
        self.palette["gradient_pink"] = palette

        # create alternating blue / green / red / yellow palette
        palette: List[int] = []
        palette.extend([0x00,0x00,0x00])
        for i in range(int(colors_max/4-1)):
            palette.extend([0x00,0x00,0xFF])
            palette.extend([0x00,0xFF,0x00])
            palette.extend([0xFF,0x00,0x00])
            palette.extend([0xFF,0xFF,0x00])
        palette.extend([0x00, 0x00, 0xFF])
        palette.extend([0x00, 0xFF, 0x00])
        palette.extend([0x00,0x00,0x00])
        self.palette["default"] = palette


    # return entire RGB palette as flat list
    def get_palette(self) -> list:
        return self.palette["default"]
