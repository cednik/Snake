#! python3
import pygame
from random import randint
from math import sqrt

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#print(pygame.font.get_fonts())
#text = pygame.font.SysFont('arial', 50, True)

CIRCLE_SIZE = 10

background_color = pygame.Color('black')
my_color = pygame.Color('green')
item_color = pygame.Color('white')

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1000//100)

x = WIDTH // 2
y = HEIGHT // 2
dx = 0
dy = 0
x_item = x
y_item = y
score = -1

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
        #text_surf = text.render(str(t), True, (0, 255, 0), (0, 0, 0))
        #screen.blit(text_surf, (20, 20))
        x += dx
        y += dy
        if x < CIRCLE_SIZE or x >= (WIDTH - CIRCLE_SIZE) or y < CIRCLE_SIZE or y >= (HEIGHT - CIRCLE_SIZE):
            break
        if sqrt((x - x_item) ** 2 + (y - y_item) ** 2) < 2 * CIRCLE_SIZE:
            score += 1
            x_item = None
        if x_item is None:
            x_item = randint(CIRCLE_SIZE, WIDTH - CIRCLE_SIZE)
            y_item = randint(CIRCLE_SIZE, HEIGHT - CIRCLE_SIZE)
    screen.fill(background_color)
    pygame.draw.circle(screen, my_color, (x, y), CIRCLE_SIZE)
    pygame.draw.circle(screen, item_color, (x_item, y_item), CIRCLE_SIZE)
    pygame.display.flip()

pygame.quit()
