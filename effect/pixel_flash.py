from constants import *
from particle import Particle
import color.color_sequence as c_seq


class PixelFlash(Particle):

    blue_sweep = {0: WHITEBLUE, 9: BLUEGLOW, 19: BLUE, 29: BLACK,
                  30: 'end'}
    blue_flicker = {0: BLUE, 2: BLUEGLOW, 4: BLUE, 7: BLACK, 8: 'end'}

    @classmethod
    def get_color_sequence(cls, color, seq_type):
        sequences = {
            'flicker': (c_seq.Flicker, (10, True, True)),
            'gleam': (c_seq.Gleam, (8, True, True)),
        }
        seq = sequences[seq_type][0]
        args = sequences[seq_type][1]
        duration, clear, finite = args
        return seq(color, duration, clear, finite)

    @classmethod
    def get_instance(cls, collection, point, color, seq_type):
        pixel = cls(collection, point)
        seq = cls.get_color_sequence(color, seq_type)
        pixel.set_color_sequence(seq)
        return pixel

    def __init__(self, collection, point):

        Particle.__init__(self, collection, point)

        self.dot = pygame.Surface((SCALE, SCALE))
        self.dot.set_colorkey(WHITE)
        self.dot = self.dot.convert()
        self.rect = self.dot.get_rect()
        self.rect.topleft = self.point

        self.color_sequence = None
        self.sequence = PixelFlash.blue_sweep
        self.color = None

        self.set_color()

    def draw(self, surface):

        surface.blit(self.dot, self.rect)

        self.increment_tick()
        self.set_color()

    def set_color_sequence(self, sequence):
        self.color_sequence = sequence
        self.sequence = self.color_sequence.sequence

    def set_color(self):

        for i in sorted(self.sequence.keys()):

            if self.tick <= i:
                if self.sequence[i] == 'end':
                    self.end()
                    return
                elif self.sequence[i] == 'repeat':
                    self.tick = 0
                    return
                color = self.sequence[i]
                if color != self.color:
                    self.dot.fill(color)
                    self.color = color
                return


class PixelFlashSet(PixelFlash):

    """ Pixel Flash Set is a set of coordinates with a synchronized flash
        pattern """

    def __init__(self, collection, points):

        PixelFlash.__init__(self, collection, points[0])
        self.points = points

    def draw(self, surface):

        for point in self.points:
            self.rect.topleft = point
            surface.blit(self.dot, self.rect)

        self.increment_tick()
        self.set_color()
