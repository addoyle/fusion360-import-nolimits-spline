# Denotes a structure that can be colored
class Colorable:
    class RGB:
        r: float = 0
        g: float = 0
        b: float = 0
    colormode_mainspine: bool = False
    colormode_catwalk: bool = False
    colormode_unpaintedmetal: bool = False
    colormode_handrails: bool = False
    colormode_support: bool = True
    colormode_custom: RGB