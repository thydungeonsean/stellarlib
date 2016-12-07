from random import *


class ColorPalette(object):

    def __init__(self, num, variance=30):

        self.num = num
        self.variance = variance
        self.base = set_random_color()
        self.palette = self.set_palette()

    def set_palette(self):

        palette = {
                   1: self.base,
                   2: self.vary_color(self.base),
                   3: self.lighten_color(self.base),
                   4: self.darken_color(self.base),
                  }

        return palette

    def get_color(self):
        return choice(self.palette.keys())

    def vary_color(self, base_color):
        return vary_color(base_color, self.variance)

    def lighten_color(self, base_color):
        return lighten_color(base_color, self.variance)

    def darken_color(self, base_color):
        return darken_color(base_color, self.variance)


def verify_color(col):

    verified = []

    for v in col:
        if v > 255:
            v = 255
        if v < 0:
            v = 0
        verified.append(v)
    return tuple(verified)


def vary_color((r, g, b), variance):

    r_var = randint(-variance, variance)
    g_var = randint(-variance, variance)
    b_var = randint(-variance, variance)

    new = r + r_var, g + g_var, b + b_var

    return verify_color(new)


def lighten_color((r, g, b), variance):

    r_var = randint(0, variance)
    g_var = randint(0, variance)
    b_var = randint(0, variance)

    new = r + r_var, g + g_var, b + b_var

    return verify_color(new)


def darken_color((r, g, b), variance):

    r_var = randint(-variance, 0)
    g_var = randint(-variance, 0)
    b_var = randint(-variance, 0)

    new = r + r_var, g + g_var, b + b_var

    return verify_color(new)


def set_random_color():

    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)

    return r, g, b


def add_colors((ar, ag, ab), (br, bg, bb)):
    nr = ar + br
    ng = ag + bg
    nb = ab + bb
    return verify_color((nr, ng, nb))


def lerp_color(base_col, end_col, percent):

    br, bg, bb = base_col
    er, eg, eb = end_col

    diff_r = int((er - br) * percent)
    diff_g = int((eg - bg) * percent)
    diff_b = int((eb - bb) * percent)

    lerp = add_colors((diff_r, diff_g, diff_b), base_col)

    return verify_color(lerp)
