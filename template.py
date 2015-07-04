# !/usr/bin/python

import pygame
import time
import sys

pygame.init()
pygame.display.set_caption("title")
screen = pygame.display.set_mode((600, 600), 0, 32)

x0 = [0, 0]
x1 = [10, 10]


def update():
    x0[0] += 1
    x1[0] += 1


def draw():
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 255, 255), x0, x1)
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit(0)
    update()
    draw()
    time.sleep(0.05)

