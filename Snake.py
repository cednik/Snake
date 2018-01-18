#! python3
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

CIRCLE_SIZE = 10
x = -CIRCLE_SIZE // 2

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1000//100)


while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        break
    elif event.type == MOVE_EVENT:
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 255, 255), (x, HEIGHT // 2), CIRCLE_SIZE)
        pygame.display.flip()
        x += 1
        if x > (WIDTH + CIRCLE_SIZE // 2):
            x = -CIRCLE_SIZE // 2

pygame.quit()
