import pixel_flash as flsh
from constants import *
from particle import Particle
import animation_map as ani


class ParticleProjectile(Particle):

    def __init__(self, collection, point, color):

        Particle.__init__(self, collection, point)

        self.tick = 1

        self.flashes = []
        self.color = color

        self.ani_map = None
        self.w = 0
        self.h = 0
        self.image = None
        self.rect = None

    def set_image(self):

        image = pygame.Surface((scale(self.w), scale(self.h)))
        image.set_colorkey(WHITE)
        image = image.convert()
        rect = image.get_rect()
        image.fill(WHITE)

        rect.topleft = self.point

        return image, rect

    def draw(self, surface):

        self.add_pixel_flashes()
        self.increment_tick()

        for flash in self.flashes:
            flash.draw(self.image)

        surface.blit(self.image, self.rect)

        if not self.flashes:
            self.end()

    def add_pixel_flashes(self):

        flash_coords = []

        for y in range(self.h):
            for x in range(self.w):

                if self.ani_map.map[x][y] == self.get_step():
                    tx = scale(x)
                    ty = scale(y)
                    flash_coords.append((tx, ty))

        if flash_coords:
            new = self.get_next_pixel_flash(flash_coords)

    def get_step(self):

        return self.tick/6 + 1

    def get_next_pixel_flash(self, coords):

        new = flsh.PixelFlash.get_instance(self.flashes, coords, self.color, 'flicker')

        self.flashes.append(new)
