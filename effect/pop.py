import pixel_flash as flsh
from constants import *
from particle_projectile import ParticleProjectile
import animation_map as ani


class Pop(ParticleProjectile):

    def __init__(self, collection, point, color):

        ParticleProjectile.__init__(self, collection, point, color)

        self.ani_map = ani.AnimationMap.get_premade_animation('pop')
        self.w = self.ani_map.w
        self.h = self.ani_map.h

        self.image, self.rect = self.set_image()

    def get_next_pixel_flash(self, coords):

        new = flsh.PixelFlash.get_instance(self.flashes, coords, self.color, 'flicker')

        return new