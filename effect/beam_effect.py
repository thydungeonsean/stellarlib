import pygame
from pygame.locals import *
from constants import *
import line
import color.color_sequence as col_seq


class BeamEffect(object):

    def __init__(self, color, width):
        # parameters
        # width
        # splay
        # flicker
        # core
        # pulse

        self.color = color
        self.width = width

        self.line_cluster = self.set_line_cluster()

        self.base_image, self.base_rect = self.set_base_image()
        self.scaled_image = None
        self.scaled_rect = None

        self.update = True

    def set_line_cluster(self):

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        cluster = [line.Line(col_seq.Solid(WHITE))]

        i = self.width-1
        for dx, dy in directions:
            cluster.append(line.Line(col_seq.Flicker(BLUE, clear=False, finite=False), point=(dx*i, dy*i)))

        cluster.reverse()

        return cluster

    def set_base_image(self):

        screen = pygame.display.get_surface()
        w = screen.get_width() / 2
        h = screen.get_height() / 2

        image = pygame.Surface((w, h))
        rect = image.get_rect()

        return image, rect

    def render(self, origin, end):

        self.base_image.fill(BLACK)

        base_origin = self.get_scaled_coord(origin)
        base_end = self.get_scaled_coord(end)

        for line in self.line_cluster:
            line.move_origin(base_origin)
            line.move_end(base_end)
            line.draw(self.base_image)

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
