import effect.pixel_flash as flsh
from constants import *


screen = pygame.display.get_surface()

flashes = []


def demo():

    global flashes

    mx, my = pygame.mouse.get_pos()

    x = (mx / 2) * 2
    y = (my / 2) * 2

    new = flsh.PixelFlash(flashes, (x, y))
    new.flash = flsh.PixelFlash.blue_sweep
    flashes.append(new)

    for p in flashes:
        p.draw(screen)

    pygame.display.update()

end = False
while not end:

    demo()

    for event in pygame.event.get():
        if event.type in (KEYDOWN, QUIT):
            end = True

    pygame.time.delay(10)

pygame.quit()
exit()
