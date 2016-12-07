from constants import *
from color_effects import *


class ColorSequence(object):

    def __init__(self, base, duration, clear=True, finite=True):
        self.base = base
        self.duration = duration
        self.clear = clear
        self.finite = finite

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
            finished_sequence[frame] = WHITE
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
               self.base
              ]
        return seq

