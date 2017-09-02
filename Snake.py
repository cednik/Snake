#!/usr/bin/python3
from random import randrange as rand
from collections import deque
import pygame as pg

raster = 10
window_size = (40, 40)

pg.init()
screen = pg.display.set_mode((window_size[0] * raster, window_size[1] * raster))
pg.display.set_caption('Snake')

MOVE_EVENT = pg.USEREVENT + 1

move_period = 250
pg.time.set_timer(MOVE_EVENT, move_period)

NORTH = 1
SOUTH = 2
EAST  = 3
WEST  = 4

BLACK = pg.Color('black')
YELLOW = pg.Color('yellow')
RED = pg.Color('red')

x = int(window_size[0] / 2)
y = int(window_size[1] / 2)
dirs = deque([EAST])
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
        if e.key == pg.K_UP and dirs[-1] != SOUTH:
            dirs.append(NORTH)
        elif e.key == pg.K_DOWN and dirs[-1] != NORTH:
            dirs.append(SOUTH)
        elif e.key == pg.K_LEFT and dirs[-1] != EAST:
            dirs.append(WEST)
        elif e.key == pg.K_RIGHT and dirs[-1] != WEST:
            dirs.append(EAST)
        elif e.key == pg.K_ESCAPE:
            break
    elif e.type == MOVE_EVENT:
        if len(dirs) > 1:
            dirs.popleft()
        if dirs[0] == NORTH:
            y -= 1
        elif dirs[0] == SOUTH:
            y += 1
        elif dirs[0] == EAST:
            x += 1
        elif dirs[0] == WEST:
            x -= 1

        if x < 0:
            x = window_size[0] - 1
        elif x == window_size[0]:
            x = 0
        elif y < 0:
            y = window_size[1] - 1
        elif y == window_size[1]:
            y = 0

        coor = (x, y)
        if coor in tail:
            break

        last = tail[-1]
        for i in range(len(tail) - 1, 0, -1):
            tail[i] = tail[i-1]
        tail[0] = coor

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
