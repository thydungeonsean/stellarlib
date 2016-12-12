import effect.pop as pop
import effect.bolt as bolt
from constants import *


screen = pygame.display.get_surface()

pops = []


def new_pop():

    global pops

    mx, my = pygame.mouse.get_pos()

    x = (mx / 2) * 2
    y = (my / 2) * 2

    new = pop.Pop(pops, (x+10, y-10), RED)
    #new = bolt.Bolt(pops, (x+20, y-20), RED, 'vec')
    pops.append(new)


def demo():

    for p in pops:
        p.draw(screen)

    pygame.display.update()

end = False
while not end:

    demo()

    for event in pygame.event.get():
        if event.type in (KEYDOWN, QUIT):
            end = True
        elif event.type == MOUSEBUTTONDOWN:
            new_pop()

    pygame.time.delay(10)

pygame.quit()
exit()
