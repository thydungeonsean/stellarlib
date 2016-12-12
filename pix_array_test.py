import effect.pixel_map as pixel_map
from constants import *
import effect.outline_map as outline_map
import effect.animation_map as ani_map
from effect.scan_outline import ScanOutline


screen = pygame.display.get_surface()

flashes = []


pm = pixel_map.PixelMap.load_image('assets/ship2.png')
out = outline_map.OutlineMap(pm)
out.color = RED
out.update_image()
out.position((0, 0))

ani = ani_map.AnimationMap.get_scan_outline(out)


def demo():

    pm.draw(screen)
    out.draw(screen)
    pygame.display.update()

clock = pygame.time.Clock()
end = False
while not end:

    demo()

    for event in pygame.event.get():
        if event.type in (KEYDOWN, QUIT):
            end = True

    clock.tick(FPS)
    # print clock.get_fps()

pygame.quit()
exit()
