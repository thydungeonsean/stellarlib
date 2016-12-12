from particle_animation import ParticleAnimation
from pixel_flash import PixelFlash
from animation_map import AnimationMap
from constants import *


class ScanOutline(ParticleAnimation):

    def __init__(self, collection, point, color, outline):
        ParticleAnimation.__init__(self, collection, point, color)

        self.complete_outline = outline
        self.collection.append(self)

        self.point = self.position(point)

        self.ani_map = AnimationMap.get_scan_outline(outline)
        self.w = self.ani_map.w
        self.h = self.ani_map.h

        self.image, self.rect = self.set_image()

    def get_next_pixel_flash(self, coords):
        new = PixelFlash.get_instance(self.flashes, coords, self.color, 'gleam_persist')

        self.flashes.append(new)

    def get_step(self):

        return self.tick

    def position(self, (x, y)):
        return x-scale(2), y-scale(2)


class ScanSweep(ParticleAnimation):

    def __init__(self, collection, point, color, outline):
        ParticleAnimation.__init__(self, collection, point, color)

        self.complete_outline = outline
        self.collection.append(self)

        self.point = self.position(point)

        self.ani_map = AnimationMap.get_left_sweep(outline)
        self.w = self.ani_map.w
        self.h = self.ani_map.h

        self.image, self.rect = self.set_image()

    def get_next_pixel_flash(self, coords):
        new = PixelFlash.get_instance(self.flashes, coords, self.color, 'gleam_persist')

        self.flashes.append(new)

    def get_step(self):
        return self.tick

    def position(self, (x, y)):
        return x - scale(2), y - scale(2)
