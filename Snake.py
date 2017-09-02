#!/usr/bin/python3
from random import randrange as rand
import pygame as pg

raster = 10
window_size = (40, 40)

pg.init()
screen = pg.display.set_mode((window_size[0] * raster, window_size[1] * raster))
pg.display.set_caption('Snake')

MOVE_EVENT = pg.USEREVENT + 1

pg.time.set_timer(MOVE_EVENT, 250)

NORTH = 1
SOUTH = 2
EAST  = 3
WEST  = 4

BLACK = pg.Color('black')
YELLOW = pg.Color('yellow')
RED = pg.Color('red')

x = int(window_size[0] / 2)
y = int(window_size[1] / 2)
dir = EAST
tail = [(x, y)]
apples = []

add_apple = True
redraw = True

score = 0

while True:
    e = pg.event.wait()
    if e.type == pg.QUIT:
        break
    elif e.type == pg.KEYDOWN:
        if e.key == pg.K_UP and dir != SOUTH:
            dir = NORTH
        if e.key == pg.K_DOWN and dir != NORTH:
            dir = SOUTH
        if e.key == pg.K_LEFT and dir != EAST:
            dir = WEST
        if e.key == pg.K_RIGHT and dir != WEST:
            dir = EAST
        if e.key == pg.K_ESCAPE:
            break
    elif e.type == MOVE_EVENT:
        if dir == NORTH:
            y -= 1
        elif dir == SOUTH:
            y += 1
        elif dir == EAST:
            x += 1
        elif dir == WEST:
            x -= 1
        coor = (x, y)
        if x < 0 or x >= window_size[0] or y < 0 or y >= window_size[1] or coor in tail:
            break

        last = tail[-1]
        for i in range(len(tail) - 1, 0, -1):
            tail[i] = tail[i-1]
        tail[0] = (x, y)

        if coor in apples:
            tail.append(last)
            apples.remove(coor)
            add_apple = True
            score += 1
            pg.display.set_caption('Snake' + 16 * ' ' + 'Score: {}'.format(score))
        redraw = True

    if add_apple:
        add_apple = False
        while True:
            ax = rand(window_size[0])
            ay = rand(window_size[1])
            coor = (ax, ay)
            if coor in tail or coor in apples:
                continue
            apples.append(coor)
            break

    if redraw:
        redraw = False
        screen.fill(BLACK)
        for k in tail:
            c = (k[0] * raster, k[1] * raster)
            pg.draw.rect(screen, YELLOW, pg.Rect(c, (raster, raster)))
        for k in apples:
            c = (k[0] * raster, k[1] * raster)
            pg.draw.ellipse(screen, RED, pg.Rect(c, (raster, raster)))
        pg.display.flip()

pg.quit()
