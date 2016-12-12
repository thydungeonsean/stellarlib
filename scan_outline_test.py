import effect.pixel_map as pixel_map
from constants import *
import effect.outline_map as outline_map
import effect.animation_map as ani_map
from effect.scan_outline import ScanOutline, ScanSweep


screen = pygame.display.get_surface()

flashes = []


pm = pixel_map.PixelMap.load_image('assets/ship2.png')
out = outline_map.OutlineMap(pm)
out.color = BLUE
out.update_image()
out.position((0, 0))

out2 = outline_map.OutlineMap.get_filled_outline(pm)
out2.print_map()


effects = []
scan = ScanSweep(effects, (0, 0), BLUE, out)
# scan = ScanOutline(effects, (0, 0), BLUE, out)


def demo():

    pm.draw(screen)
    out.draw(screen)

    for effect in effects:
        effect.draw(screen)
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
