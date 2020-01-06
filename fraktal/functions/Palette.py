import colorsys
from typing import List


def palettes(colors_max: int = 256):
    colors_max = min(colors_max, 256)

    # create alternating blue / green / red / yellow palette
    def default():
        p: List[int] = []
        p.extend([0x00,0x00,0x00])
        for i in range(int(colors_max/4-1)):
            p.extend([0x00,0x00,0xFF])
            p.extend([0x00,0xFF,0x00])
            p.extend([0xFF,0x00,0x00])
            p.extend([0xFF,0xFF,0x00])
        p.extend([0x00, 0x00, 0xFF])
        p.extend([0x00, 0xFF, 0x00])
        p.extend([0x00,0x00,0x00])
        return p

    # create rainbow palette
    def rainbow():
        r, g, b = 255, 0, 0
        p: List[int] = []
        p.extend([0,0,0])
        for g in range(0, 256, 6):
            p.extend([r, g, b])
        for r in range(255, -1, -6):
            p.extend([r, g, b])
        for b in range(0, 256, 6):
            p.extend([r, g, b])
        for g in range(255, -1, -6):
            p.extend([r, g, b])
        for r in range(0, 256, 6):
            p.extend([r, g, b])
        for b in range(255, 23, -6):
            p.extend([r, g, b])
        p.extend([0,0,0])
        return p

    # create a pink gradient palette
    def gradient_pink():
        p: List[int] = []
        for i in range(colors_max-1):
            f = 1 - abs((float(i) / colors_max - 1) ** 15)
            r, g, b = colorsys.hsv_to_rgb(.66 + f / 3, 1 - f / 2, f)
            p.extend([int(r * 255), int(g * 255), int(b * 255)])
        # set inf (last) to black
        p.extend([0,0,0])
        return p

    return {"default": default,
            "rainbow": rainbow,
            "gradient_pink": gradient_pink}

