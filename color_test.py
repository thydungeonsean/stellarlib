import effect.color.color_effects as col
from constants import *


screen = pygame.display.get_surface()

test_col = BLUE
colors = [
          col.lerp_color(test_col, WHITE, .9),
          col.lerp_color(test_col, WHITE, .65),
          col.lerp_color(test_col, WHITE, 0)]

im = []

for i in range(len(colors)):
    image = pygame.Surface((30, 30))
    image.fill(colors[i])
    rect = image.get_rect()
    rect.topleft = (i*30, 0)

    im.append((image, rect))



def demo():

    for i, r in im:
        screen.blit(i, r)

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
