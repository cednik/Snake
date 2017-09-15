#!/usr/bin/python3

from math import ceil
from os import linesep

import pygame as pg

l = 1
t = 91
w = 264 - l
h = 354 - t
raster = 8

wall_color = (0, 0, 255, 255)

delta = (
    ( 0, -1),
    ( 1,  0),
    ( 0,  1),
    (-1,  0)
)

rasterize = lambda v: int(ceil(v/raster))
wm = rasterize(w)
hm = rasterize(h)
walls_matrix = [[False for x in range(wm)] for y in range(rasterize(hm))]

file_buff_len = (wm + len(linesep)) * hm

pg.init()

area = pg.Rect(l, t, w, h)

screen = pg.display.set_mode((w*2, h))

playground = pg.Surface((w, h))
walls = pg.Surface((w, h))

wall_color_int = walls.map_rgb(wall_color)

quit = False
pg.time.set_timer(pg.USEREVENT, 100)

for level in range(1, 31):
    img = pg.image.load('{}.png'.format(level))

    playground.blit(img, (0, 0), area)

    pg.transform.threshold(walls,          # DestSurface
                           playground,     # Surface
                           wall_color,     # color
                           (0, 0, 128, 0)) # threshold

    pixels = pg.PixelArray(walls)

    for y in range(h):
        for x in range(w):
            single = True
            for d in delta:
                X = x + d[0]
                Y = y + d[1]
                if X < 0 or X == w or Y < 0 or Y == h:
                    continue
                if pixels[X, Y] == wall_color_int:
                    single = False
                    break
            if single:
                pixels[x, y] = (0, 0, 0)

    walls_matrix = [[pixels[x*raster, y*raster] == wall_color_int for x in range(wm)] for y in range(hm)]

    del pixels

    with open('{}.txt'.format(level), 'w', file_buff_len) as f:
        for l in walls_matrix:
            for b in l:
                f.write('#' if b else ' ')
            f.write('\n')

    screen.blit(playground, (w, 0))
    screen.blit(walls, (0, 0))

    pg.display.flip()

    while True:
        e = pg.event.wait()
        if e.type == pg.QUIT:
            quit = True
            break
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                quit = True
            break
        elif e.type == pg.MOUSEBUTTONDOWN:
            break
        elif e.type == pg.USEREVENT:
            break
        elif e.type == pg.MOUSEMOTION:
            pg.display.set_caption('[{}, {}]: {}'.format(e.pos[0],
                                                         e.pos[1],
                                                         screen.get_at(e.pos)))
    if quit:
        break

pg.quit()
