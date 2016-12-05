from constants import *
from particle import Particle


class PixelFlash(Particle):

    blue_sweep = {0: WHITEBLUE, 9: BLUEGLOW, 19: BLUE, 29: BLACK,
                  30: 'end'}
    blue_flicker = {0: BLUE, 2: BLUEGLOW, 4: BLUE, 7: BLACK, 8: 'end'}

    def __init__(self, collection, point):

        Particle.__init__(self, collection, point)

        self.dot = pygame.Surface((SCALE, SCALE))
        self.rect = self.dot.get_rect()

        self.rect.topleft = self.point

        self.flash = PixelFlash.blue_flicker
        self.color = BLACK
        self.set_color()

    def draw(self, surface):

        surface.blit(self.dot, self.rect)

        self.increment_tick()
        self.set_color()

    def set_color(self):

        for i in sorted(self.flash.keys()):

            if self.tick <= i:
                if self.flash[i] == 'end':
                    self.end()
                    return
                color = self.flash[i]
                if color != self.color:
                    self.dot.fill(color)
                    self.color = color
                return
