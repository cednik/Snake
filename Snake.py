#! python3
import pygame
from random import randint
from math import sqrt
from collections import deque
import os

raster = 20

pygame.init()

class Wall:
    color = pygame.color.Color('blue')
        
    def draw(self, surface, x, y):
        pygame.draw.rect(surface, Wall.color, pygame.Rect(x, y, raster, raster))

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

    def draw(self, surface, x, y):
        pygame.draw.ellipse(surface, self.color, pygame.Rect(x, y, raster, raster))

class Snake:
    UP    = 1
    DOWN  = 3
    LEFT  = 2
    RIGHT = 4
    
    def __init__(self, playground, start, course, length, color, keys, started = False):
        self.playground = playground
        x, y = start
        dx, dy = ((0, 1), (1, 0), (0, -1), (-1, 0))[course-1]
        self.tail = list((x + dx * i, y + dy * i) for i in range(length))
        self.course = deque([course])
        self.color = color
        self.keys = keys
        self.score = 0
        self.started = started
        self.alive = True

    def control(self, key):
        if not (self.alive and self.started):
            return
        if key == self.keys[1] and self.course[-1] != Snake.UP:
            self.course.append(Snake.DOWN)
        elif key == self.keys[0] and self.course[-1] != Snake.DOWN:
            self.course.append(Snake.UP)
        elif key == self.keys[3] and self.course[-1] != Snake.LEFT:
            self.course.append(Snake.RIGHT)
        elif key == self.keys[2] and self.course[-1] != Snake.RIGHT:
            self.course.append(Snake.LEFT)

    def move(self):
        if not (self.alive and self.started):
            return
        x, y = self.tail[0]
        if len(self.course) > 1:
            self.course.popleft()
        if self.course[0] == Snake.UP:
            y -= 1
        elif self.course[0] == Snake.DOWN:
            y += 1
        elif self.course[0] == Snake.RIGHT:
            x += 1
        elif self.course[0] == Snake.LEFT:
            x -= 1
        coor = (x, y)
        if x < 0 or y < 0 or y >= len(self.playground) or x >= len(self.playground[y]) or isinstance(self.playground[y][x], (Snake, Wall)):
            self.alive = False
            for x, y in self.tail:
                try:
                    self.playground[y][x] = None
                except IndexError:
                    pass
            return
        last = self.tail[-1]
        for i in range(len(self.tail) - 1, 0, -1):
            self.tail[i] = self.tail[i-1]
        self.tail[0] = coor
        if isinstance(self.playground[y][x], Apple):
            self.tail.append(last)
            self.score += 1
            self.playground[y][x].eat()
        else:
            if last[1] >= 0 and last[1] < len(self.playground) and last[0] >= 0 and last[0] < len(self.playground[last[1]]):
                self.playground[last[1]][last[0]] = None
        self.playground[y][x] = self

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, self.color, pygame.Rect(x, y, raster, raster))

    def start(self):
        if self.started:
            return
        self.started = True
        x, y = self.tail[0]
        self.playground[y][x] = self

    def __bool__(self):
        return self.alive

    def __len__(self):
        return len(self.tail)

playground = []

def load_level(name, playground):
    start_course = {'U': Snake.UP, 'D': Snake.DOWN, 'L': Snake.LEFT, 'R': Snake.RIGHT}
    start = None
    del playground[:]
    name = str(name) + '.lvl'
    with open(os.path.join('levels', name)) as f:
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]
            if not line:
                continue
            row = []
            for square in line:
                if square == ' ':
                    item = None
                elif square == '#':
                    item = Wall()
                elif square in start_course:
                    start = ((len(row), len(playground)), start_course[square])
                row.append(item)
            playground.append(row)
    if start == None:
        y = len(playground) - 1
        x = len(playground[y]) // 2
        start = ((x, y), start_course['U'])
    return start

start_point, start_dir = load_level(1, playground)

circle_size = raster // 2 - 1

h = len(playground)
w = len(max(playground, key = len))
screen = pygame.display.set_mode((w * raster, h * raster))

background_color = pygame.Color('black')

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1000//4)

snakes_count = 3

keys = ((pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d),
        (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l),
        (pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6))
colors = (pygame.color.Color('yellow'),
          pygame.color.Color('cyan'),
          pygame.color.Color('magenta'))
snakes = [Snake(playground, start_point, start_dir, 4, color = colors[i], keys = keys[i]) for i in range(snakes_count)]

start_space = 2

started = 0
moves = 0
next_start = 0
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
        if moves == next_start:
            if started < snakes_count:
                snakes[started].start()
                next_start += len(snakes[started])
                started += 1
                if started != snakes_count:
                    next_start += start_space
            elif started == snakes_count:
                playground[start_point[1]][start_point[0]] = Wall()
                Apple(playground)
        pygame.display.set_caption('Snake' + 16 * ' ' + 'Score: {}'.format(', '.join('{:3}'.format(snake.score) for snake in snakes)))
        moves += 1
        redraw = True

    if redraw:
        redraw = False
        screen.fill(background_color)
        y = 0
        for line in playground:
            x = 0
            for square in line:
                if square != None:
                    square.draw(screen, x, y)
                x += raster
            y += raster
        pygame.display.flip()

pygame.quit()
