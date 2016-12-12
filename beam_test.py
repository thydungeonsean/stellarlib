import effect.beam_effect as beam
from constants import *


screen = pygame.display.get_surface()
sw = screen.get_width()/2
sh = screen.get_height()/2


be = beam.BeamEffect(BLUE, 5)


def demo():

    mx, my = pygame.mouse.get_pos()

    be.render((sw, sh), (mx+10, my-10))

    be.draw(screen)

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
