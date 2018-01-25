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
my_color = pygame.Color('green')
item_color = pygame.Color('white')

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1000//4)

x = int(window_size[0] / 2)
y = int(window_size[1] / 2)
dx = 0
dy = 0
x_item = x
y_item = y
score = 0

while True:
    
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
        elif event.key == pygame.K_DOWN:
            dx = 0
            dy = 1
        elif event.key == pygame.K_UP:
            dx = 0
            dy = -1
        elif event.key == pygame.K_RIGHT:
            dx = 1
            dy = 0
        elif event.key == pygame.K_LEFT:
            dx = -1
            dy = 0
    elif event.type == MOVE_EVENT:
        x += dx
        y += dy
        if x < 0 or x >= window_size[0] or y < 0 or y >= window_size[1]:
            break
        if x == x_item and y == y_item:
            score += 1
            x_item = None
        if x_item is None:
            x_item = randint(0, window_size[0] - 1)
            y_item = randint(0, window_size[1] - 1)
    screen.fill(background_color)
    pygame.draw.circle(screen, item_color, (x_item * raster + raster // 2, y_item * raster + raster // 2), circle_size)
    pygame.draw.circle(screen, my_color, (x * raster + raster // 2, y * raster + raster // 2), circle_size)
    pygame.display.flip()

pygame.quit()
