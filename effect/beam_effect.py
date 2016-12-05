import pygame
from pygame.locals import *
from constants import *


class BeamEffect(object):

    def __init__(self, color):
        # parameters
        # width
        # splay
        # flicker
        # core
        # pulse


        self.color = color

        self.base_image = None
        self.base_rect = None
        self.scaled_image = None
        self.scaled_rect = None

        self.update = True

    def render(self, origin, end):

        self.base_image = pygame.Surface((200, 200))
        self.base_rect = self.base_image.get_rect()

        base_origin = self.get_scaled_coord(origin)
        base_end = self.get_scaled_coord(end)

        self.draw_line(base_origin, base_end, self.color, 3)

        self.scale_image()

    def get_scaled_coord(self, (x, y)):

        sx = descale(x)
        sy = descale(y)

        return sx, sy

    def scale_image(self):

        if self.scaled_rect is None:
            w = self.base_rect.w
            h = self.base_rect.h
            self.scaled_rect = pygame.Rect((0, 0), (w, h))

        b = self.base_image
        self.scaled_image = pygame.transform.scale(b, (scale(b.get_width()), scale(b.get_height())))

    def draw(self, surface):
        surface.blit(self.scaled_image, self.scaled_rect)

    def draw_line(self, origin, end, color, w):

        pygame.draw.line(self.base_image, color, origin, end, w)
