import pygame


class Line(object):

    def __init__(self, color_seq, width=1, point=(0, 0)):

        x, y = point
        self.x = x
        self.y = y

        self.origin = None
        self.end = None

        self.color_seq = color_seq
        self.sequence = self.color_seq.sequence

        self.width = width
        self.color = None

        self.tick = 0
        self.set_color()

    def move_origin(self, (nx, ny)):

        self.origin = (self.x + nx, self.y + ny)

    def move_end(self, (nx, ny)):

        self.end = (self.x + nx, self.y + ny)

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.origin, self.end, self.width)

        self.increment_tick()
        self.set_color()

    def increment_tick(self):
        self.tick += 1

    def set_color(self):

        for i in sorted(self.sequence.keys()):

            if self.tick <= i:
                if self.sequence[i] in ('end', 'repeat'):
                    self.tick = 0  # beam effects shouldn't end
                    return
                color = self.sequence[i]
                if color != self.color:
                    self.color = color
                return
