#! python3
import pygame
from random import randint
from math import sqrt

pygame.init()

raster = 20
window_size = (25, 25)

circle_size = raster // 2 - 1

screen = pygame.display.set_mode((window_size[0] * raster, window_size[1] * raster))

background_color = pygame.Color('black')
snake_color = pygame.Color('green')
item_color = pygame.Color('white')

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1000//4)

UP    = 1
DOWN  = 3
LEFT  = 2
RIGHT = 4

x = int(window_size[0] / 2)
y = int(window_size[1] / 2)
course = RIGHT
tail = [(x, y)]
x_item = x
y_item = y

score = 0

add_apple = True
redraw = True

while True:
    
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
        elif event.key == pygame.K_DOWN:
            course = DOWN
        elif event.key == pygame.K_UP:
            course = UP
        elif event.key == pygame.K_RIGHT:
            course = RIGHT
        elif event.key == pygame.K_LEFT:
            course = LEFT
    
    elif event.type == MOVE_EVENT:
        if course == UP:
            y -= 1
        elif course == DOWN:
            y += 1
        elif course == LEFT:
            x -= 1
        elif course == RIGHT:
            x += 1
        else:
            print('Invalid direction!')
            
        if x < 0 or x >= window_size[0] or y < 0 or y >= window_size[1]:
            break
        
        coor = (x, y)
        if coor in tail:
            break
        
        last = tail[-1]
        for i in range(len(tail) - 1, 0, -1):
            tail[i] = tail[i-1]
        tail[0] = coor
        
        if coor == (x_item, y_item):
            score += 1
            pygame.display.set_caption('Snake' + 16 * ' ' + 'Score: {}'.format(score))
            add_apple = True
            tail.append(last)

        redraw = True
        
    if add_apple:
        add_apple = False
        x_item = randint(0, window_size[0])
        y_item = randint(0, window_size[1])

    if redraw:
        redraw = False
        screen.fill(background_color)
        for coor in tail:
            c = (coor[0] * raster, coor[1] * raster)
            pygame.draw.rect(screen, snake_color, pygame.Rect(c, (raster, raster)))
        c = (x_item * raster, y_item * raster)
        pygame.draw.ellipse(screen, item_color, pygame.Rect(c, (raster, raster)))
        pygame.display.flip()

pygame.quit()
