#! python3
import pygame

pygame.init()

screen = pygame.display.set_mode((320, 240))

white = pygame.color.Color('white')

pygame.draw.circle(screen, (0, 255, 0), (160, 120), 60, 1)
pygame.draw.circle(screen, white, (160, 120), 30)

pygame.display.flip()

while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break

pygame.quit()
