#! python3
import pygame
from random import randint
from math import sqrt
from collections import deque

pygame.init()

raster = 20
window_size = (25, 25)

circle_size = raster // 2 - 1

screen = pygame.display.set_mode((window_size[0] * raster, window_size[1] * raster))

background_color = pygame.Color('black')
apple_color = pygame.Color('green')

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1000//4)

UP    = 1
DOWN  = 3
LEFT  = 2
RIGHT = 4

class Snake:
    def __init__(self, start, course, color, keys):
        self.tail = [start]
        self.course = deque([course])
        self.color = color
        self.keys = keys
        self.score = 0
        self.alive = True

    def control(self, key):
        if not self.alive:
            return
        if key == self.keys[1] and self.course[-1] != UP:
            self.course.append(DOWN)
        elif key == self.keys[0] and self.course[-1] != DOWN:
            self.course.append(UP)
        elif key == self.keys[3] and self.course[-1] != LEFT:
            self.course.append(RIGHT)
        elif key == self.keys[2] and self.course[-1] != RIGHT:
            self.course.append(LEFT)

    def move(self):
        if not self.alive:
            return
        x, y = self.tail[0]
        if len(self.course) > 1:
            self.course.popleft()
        if self.course[0] == UP:
            y -= 1
        elif self.course[0] == DOWN:
            y += 1
        elif self.course[0] == RIGHT:
            x += 1
        elif self.course[0] == LEFT:
            x -= 1
        coor = (x, y)
        if coor in self.tail or x < 0 or y < 0 or x >= window_size[0] or y >= window_size[1]:
            self.alive = False
        self.last = self.tail[-1]
        for i in range(len(self.tail) - 1, 0, -1):
            self.tail[i] = self.tail[i-1]
        self.tail[0] = coor

    def check_apple(self, apple):
        if not self.alive:
            return
        if self.tail[0] == apple:
            self.tail.append(self.last)
            self.score += 1
            return True
        return False

    def draw(self, surface):
        if not self.alive:
            return
        for coor in self.tail:
            c = (coor[0] * raster, coor[1] * raster)
            pygame.draw.rect(screen, self.color, pygame.Rect(c, (raster, raster)))

    def __bool__(self):
        return self.alive

x = int(window_size[0] / 2)
y = int(window_size[1] / 2)
start = [(x + 1, y) for x in range(3)]
keys = ((pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d),
        (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l),
        (pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6))
colors = (pygame.color.Color('yellow'),
          pygame.color.Color('cyan'),
          pygame.color.Color('magenta'))
snakes = [Snake(start[i], UP, color = colors[i], keys = keys[i]) for i in range(3)]

x_apple = x
y_apple = y

add_apple = True
redraw = True

while True:
    
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
        for snake in snakes:
            snake.control(event.key)
    
    elif event.type == MOVE_EVENT:
        for snake in snakes:
            snake.move()
        if not any(snakes):
            break
        for snake in snakes:
            if snake.check_apple((x_apple, y_apple)):
                score = ', '.join('{:3}'.format(snake.score) for snake in snakes)
                pygame.display.set_caption('Snake' + 16 * ' ' + 'Score: {}'.format(score))
                add_apple = True
                break
        redraw = True
        
    if add_apple:
        add_apple = False
        x_apple = randint(0, window_size[0])
        y_apple = randint(0, window_size[1])

    if redraw:
        redraw = False
        screen.fill(background_color)
        for s in snakes:
            s.draw(screen)
        c = (x_apple * raster, y_apple * raster)
        pygame.draw.ellipse(screen, apple_color, pygame.Rect(c, (raster, raster)))
        pygame.display.flip()

pygame.quit()
