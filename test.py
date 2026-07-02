from pygame import *

init()

window = display.set_mode((0, 0), FULLSCREEN)
size = window.get_size()

print(size)

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            run = False

    display.update()

quit()