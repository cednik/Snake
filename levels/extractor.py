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
    ( 1,  0),
    ( 0,  1),
    (-1,  0),
    ( 0, -1)
)

rasterize = lambda v: int(ceil(v/raster))
wm = rasterize(w)
hm = rasterize(h)
walls_matrix = [[False for x in range(wm)] for y in range(rasterize(hm))]

file_buff_len = (wm + len(linesep)) * hm

pg.init()

area = pg.Rect(l, t, w, h)

screen = pg.display.set_mode((w*2, h))

playground = pg.Surface((w, h), pg.SRCALPHA)
walls = pg.Surface((w, h), pg.SRCALPHA)

wall_color_int = walls.map_rgb(wall_color)

quit = False
pg.time.set_timer(pg.USEREVENT, 0)

to_raster = lambda l: [[int((p[i] + (0.5, 0.25)[i]) * raster) for i in range(2)] for p in l] 

for level in range(27, 31):
    pg.display.set_caption('{} / 30'.format(level))

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

    lines = []
    for y in range(hm):
        for x in range(wm):
            if not walls_matrix[y][x]:
                continue
            #walls_matrix[y][x] = False
            line = [(x, y)]
            pg.draw.circle(screen, pg.Color(0, 255, 0, 192), *to_raster(line), raster // 4)
            dir = 0
            turns = 0
            flipped = False
            while True:
                last = (x, y)
                x += delta[dir][0]
                y += delta[dir][1]
                if x < 0 or x == wm or y < 0 or y == hm or not walls_matrix[y][x]:
                    (x, y) = last
                    if line[-1] != last:
                        line.append(last)
                        pg.draw.circle(screen, pg.Color(255, 0, 255, 192), *to_raster([last]), raster // 4)
                    else:
                        pg.draw.circle(screen, pg.Color(255, 255, 0, 192), *to_raster([(x, y)]), raster // 4)
                    dir += 1
                    if dir == 4:
                        dir = 0
                    turns += 1
                    if turns == 8:
                        pg.draw.circle(screen, pg.Color(255, 0, 0, 192), *to_raster([(x, y)]), raster // 4)
                        if line[0] != line[-1]:
                            walls_matrix[line[0][1]][line[0][0]] = False
                        pg.display.flip()
                        if not flipped:
                            flipped = True
                            turns = 0
                            dir = 1
                            (x, y) = line[0]
                            line.reverse()
                        else:
                            break
                else:
                    walls_matrix[y][x] = False
                    turns = 0
                    pg.draw.circle(screen, pg.Color(255, 255, 255, 192), *to_raster([(x, y)]), raster // 4)
                pg.display.flip()
                e = pg.event.poll()
                if e.type == pg.QUIT:
                    quit = True
                    break
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        quit = True
                        break
                pg.time.wait(200)
            lines.append(line)
            if quit: break
        if quit: break
    print(len(lines)-1)
    for l in lines:
        if len(l) == 1:
            pg.draw.circle(screen, pg.Color(255, 255, 255, 128), *to_raster(l), raster // 4)
        else:
            pg.draw.lines(screen, pg.Color(255, 255, 255, 128), False, to_raster(l), raster // 2)
    # for p in points:
    #     pg.draw.circle(walls, pg.Color(255, 0, 0, 128), *to_raster([p]), raster // 4)

    

    pg.display.flip()

    while not quit:
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
            pg.display.set_caption('{} / 30: [{}, {}]: {}'.format(level,
                                                                  e.pos[0],
                                                                  e.pos[1],
                                                                  screen.get_at(e.pos)))
    if quit:
        break

pg.quit()
