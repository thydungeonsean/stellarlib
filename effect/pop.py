import pixel_flash as flsh
from constants import *
from particle import Particle


class Pop(Particle):

    animation = [[0, 0, 0, 4, 4, 0, 0, 0],
                 [0, 4, 0, 3, 3, 0, 4, 0],
                 [0, 0, 3, 2, 2, 3, 0, 0],
                 [4, 3, 2, 1, 1, 2, 3, 4],
                 [4, 3, 2, 1, 1, 2, 3, 4],
                 [0, 0, 3, 2, 2, 3, 0, 0],
                 [0, 4, 0, 3, 3, 0, 4, 0],
                 [0, 0, 0, 4, 4, 0, 0, 0]]
    w = len(animation[0])
    h = len(animation)

    def __init__(self, collection, point):

        Particle.__init__(self, collection, point)

        self.tick = 1

        self.flashes = []

        self.image = pygame.Surface((scale(Pop.w), scale(Pop.h)))
        self.rect = self.image.get_rect()
        self.image.fill(BLACK)

        self.rect.topleft = self.point

    def draw(self, surface):

        self.add_flashes()
        self.increment_tick()

        for flash in self.flashes:
            flash.draw(self.image)

        surface.blit(self.image, self.rect)

        if not self.flashes:
            self.end()

    def add_flashes(self):

        for y in range(Pop.h):
            for x in range(Pop.w):

                if Pop.animation[x][y] == self.get_step():
                    tx = scale(x)
                    ty = scale(y)
                    new = flsh.PixelFlash(self.flashes, (tx, ty))
                    self.flashes.append(new)

    def get_step(self):

        return self.tick/6 + 1
