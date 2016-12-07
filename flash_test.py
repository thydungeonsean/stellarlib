import effect.pixel_flash as flsh
from constants import *


screen = pygame.display.get_surface()

flashes = []


def demo():

    global flashes

    mx, my = pygame.mouse.get_pos()

    x = (mx / 2) * 2
    y = (my / 2) * 2

    new = flsh.PixelFlash.get_instance(flashes, (x, y), BLUE, 'gleam')
    # new.flash = flsh.PixelFlash.blue_sweep
    flashes.append(new)

    for p in flashes:
        p.draw(screen)

    pygame.display.update()

clock = pygame.time.Clock()
end = False
while not end:

    demo()

    for event in pygame.event.get():
        if event.type in (KEYDOWN, QUIT):
            end = True

    clock.tick(FPS)
    #print clock.get_fps()

print len(flashes)
pygame.quit()
exit()
