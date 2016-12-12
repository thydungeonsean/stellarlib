import pixel_flash as flsh
from constants import *
from particle_animation import ParticleAnimation
import animation_map as ani


class Bolt(ParticleAnimation):

    def __init__(self, collection, point, color, vector):

        ParticleAnimation.__init__(self, collection, point, color)

        self.vector = vector

        self.ani_map = ani.AnimationMap.get_premade_animation('bolt')
        self.w = self.ani_map.w
        self.h = self.ani_map.h

        self.image, self.rect = self.set_image()

        self.flash_map = [[0, 2, 0],
                          [2, 1, 2],
                          [0, 2, 0]]
        self.flash_key = {1: 'pulse',
                          2: 'trail'}

    def get_next_pixel_flash(self, coords):

        draw_key = {}

        for key in self.flash_key.keys():
            draw_key[key] = []
            for tx, ty in coords:
                x = descale(tx)
                y = descale(ty)
                if self.flash_map[x][y] == key:
                    draw_key[key].append((tx, ty))
            new = flsh.PixelFlash.get_instance(self.flashes, draw_key[key], self.color, self.flash_key[key])
            self.flashes.append(new)



