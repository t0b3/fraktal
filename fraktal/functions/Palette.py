import colorsys
from typing import List


class Palette(object):
    def __init__(self, colors_max: int = 256):
        self.colors_max = min(colors_max, 256)
        '''
        # create a tolerable palette in a list
        self.palette: List[int] = []
        for i in range(self.colors_max-1):
            f = 1 - abs((float(i) / self.colors_max - 1) ** 15)
            r, g, b = colorsys.hsv_to_rgb(.66 + f / 3, 1 - f / 2, f)
            self.palette.extend([int(r * 255), int(g * 255), int(b * 255)])
        # set inf (last) to black
        self.palette.extend([0,0,0])
        '''
        self.palette: List[int] = []
        self.palette.extend([0x00,0x00,0x00])
        for i in range(int(self.colors_max/4-1)):
            self.palette.extend([0x00,0x00,0xFF])
            self.palette.extend([0x00,0xFF,0x00])
            self.palette.extend([0xFF,0x00,0x00])
            self.palette.extend([0xFF,0xFF,0x00])
        self.palette.extend([0x00, 0x00, 0xFF])
        self.palette.extend([0x00, 0xFF, 0x00])
        self.palette.extend([0x00,0x00,0x00])


    # return entire RGB palette as flat list
    def get_palette(self) -> list:
        return self.palette
