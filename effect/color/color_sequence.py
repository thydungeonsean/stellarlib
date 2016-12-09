from constants import *
from color_effects import *


class ColorSequence(object):

    def __init__(self, base, duration=1, clear=True, finite=True):
        self.base = base
        self.duration = duration
        self.clear = clear
        self.finite = finite

        self.clear_color = BLACK

        self.sequence = self.set_sequence()

    def set_sequence(self):

        seq = self.get_raw_seq()

        finished_seq = self.format_sequence(seq)

        return finished_seq

    def format_sequence(self, seq):

        length = len(seq)
        finished_sequence = {}

        for i in range(length):
            frame = i * self.duration
            finished_sequence[frame] = seq[i]

        frame = length * self.duration

        if self.clear:
            finished_sequence[frame] = self.clear_color
            frame += 1

        if self.finite:
            finished_sequence[frame] = 'end'
        elif not self.finite:
            finished_sequence[frame] = 'repeat'

        return finished_sequence

    def get_raw_seq(self):
        return []

    def lerp(self, percent):
        return lerp_color(self.base, WHITE, percent)


class Solid(ColorSequence):

    def __init__(self, base):
        ColorSequence.__init__(self, base, clear=False, finite=False)

    def get_raw_seq(self):
        seq = [self.base]
        return seq


class Gleam(ColorSequence):

    def __init__(self, base, duration=10, clear=True, finite=True):

        ColorSequence.__init__(self, base, duration, clear, finite)

    def get_raw_seq(self):
        seq = [
               self.lerp(.9),
               self.lerp(.65),
               self.lerp(.5),
               self.base
              ]
        return seq


class Flicker(ColorSequence):

    def __init__(self, base, duration=10, clear=True, finite=True):

        ColorSequence.__init__(self, base, duration, clear, finite)

    def get_raw_seq(self):
        seq = [
               self.base,
               self.lerp(.65),
               self.base,
               self.lerp(.5)
              ]
        return seq


class Pulse(ColorSequence):

    def __init__(self, base, duration=1, clear=True, finite=True):

        ColorSequence.__init__(self, base, duration, clear, finite)

    def get_raw_seq(self):
        edge = self.base
        core = self.lerp(.7)
        seq = [
               edge,
               core,
               core,
               core,
               core,
               core,
               edge
              ]
        return seq


class Trail(ColorSequence):

    def __init__(self, base, duration=1, clear=True, finite=True):

        ColorSequence.__init__(self, base, duration, clear, finite)

    def get_raw_seq(self):
        trail = self.base
        gleam = self.lerp(.7)
        seq = [trail,
               trail,
               trail,
               trail,
               trail,
               trail,
               trail
               ]
        return seq