#! python3
import pygame
from random import randint
from math import sqrt
from collections import deque

pygame.init()

raster = 20
window_size = (25, 25)

playground = []
for y in range(window_size[1]):
    playground.append(window_size[0] * [None])

circle_size = raster // 2 - 1

screen = pygame.display.set_mode((window_size[0] * raster, window_size[1] * raster))

background_color = pygame.Color('black')

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1000//4)

UP    = 1
DOWN  = 3
LEFT  = 2
RIGHT = 4

class Apple:
    def __init__(self, playground):
        self.playground = playground
        self.color = pygame.Color('red')
        self.coor = None
        self.place()

    def place(self):
        while True:
            y = randint(0, len(self.playground)-1)
            x = randint(0, len(self.playground[y])-1)
            if (x, y) == self.coor:
                continue
            if self.playground[y][x] == None:
                self.playground[y][x] = self
                self.coor = (x, y)
                break

    def eat(self):
        self.playground[self.coor[1]][self.coor[0]] = None
        self.place()

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, pygame.Rect(self.coor[0] * raster, self.coor[1] * raster, raster, raster))

class Snake:
    def __init__(self, playground, start, course, color, keys):
        self.playground = playground
        self.playground[start[1]][start[0]] = self
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
        if x < 0 or y < 0 or y >= len(self.playground) or x >= len(self.playground[y]) or isinstance(self.playground[y][x], Snake):
            self.alive = False
            for x, y in self.tail:
                self.playground[y][x] = None
            return
        last = self.tail[-1]
        for i in range(len(self.tail) - 1, 0, -1):
            self.tail[i] = self.tail[i-1]
        self.tail[0] = coor
        if isinstance(self.playground[coor[1]][coor[0]], Apple):
            self.tail.append(last)
            self.score += 1
            self.playground[coor[1]][coor[0]].eat()
        else:
            self.playground[last[1]][last[0]] = None
        self.playground[coor[1]][coor[0]] = self

    def draw(self, surface):
        if not self.alive:
            return
        for coor in self.tail:
            c = (coor[0] * raster, coor[1] * raster)
            pygame.draw.rect(screen, self.color, pygame.Rect(c, (raster, raster)))

    def __bool__(self):
        return self.alive

snakes = 3
space = 3
x0 = int(window_size[0] / 2)
y = int(window_size[1] / 2)
start = [(space * x + x0 - space * snakes // 2, y) for x in range(snakes)]
keys = ((pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d),
        (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l),
        (pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6))
colors = (pygame.color.Color('yellow'),
          pygame.color.Color('cyan'),
          pygame.color.Color('magenta'))
snakes = [Snake(playground, start[i], UP, color = colors[i], keys = keys[i]) for i in range(snakes)]

apple = Apple(playground)

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
        pygame.display.set_caption('Snake' + 16 * ' ' + 'Score: {}'.format(', '.join('{:3}'.format(snake.score) for snake in snakes)))
        redraw = True

    if redraw:
        redraw = False
        screen.fill(background_color)
        for snake in snakes:
            snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

pygame.quit()
