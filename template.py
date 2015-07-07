# !/usr/bin/python

import pygame
import time
import sys
import random

pygame.init()
pygame.display.set_caption("Numbers")
screen = pygame.display.set_mode((351, 600), 0, 32)
size = 7
cellSize = 50
gameTable = []
for i in range(size):
    gameTable.append([0] * size)
currentNumber = random.randint(1, size)
moveCount = 10
score = 0
bestScore = 0
myFont = pygame.font.SysFont("Monospace", 30)


def update():
    return


def draw():
    screen.fill((0, 0, 0))
    for i in range(size):
        for j in range(size):
            pygame.draw.rect(screen, (255, 255, 255), (i * cellSize, j * cellSize + 3 * cellSize, cellSize, cellSize),
                             2)
            text = myFont.render(str(gameTable[i][j]), 1, (250, 250, 250))
            screen.blit(text, (i * cellSize, j * cellSize + 3 * cellSize, cellSize, cellSize))

    labelMove = myFont.render("Move", 1, (250, 250, 250))
    screen.blit(labelMove, (0, 0, 351 / 3, cellSize))
    screen.blit(myFont.render(str(moveCount), 1, (250, 250, 250)), (0, cellSize, 351 / 3, cellSize * 2))

    labelScore = myFont.render("Score", 1, (250, 250, 250))
    screen.blit(labelScore, (351 / 3, 0, 351 / 3, cellSize))
    screen.blit(myFont.render(str(score), 1, (250, 250, 250)), (351 / 3, cellSize, 351 / 3, cellSize * 2))

    labelRecord = myFont.render("Record", 1, (250, 250, 250))
    screen.blit(labelRecord, (351 * 2 / 3, 0, 351 / 3, cellSize))
    screen.blit(myFont.render(str(bestScore), 1, (250, 250, 250)), (351 * 2 / 3, cellSize, 351 / 3, cellSize * 2))

    labelNext = myFont.render("Next", 1, (250, 250, 250))
    screen.blit(labelNext, (0, cellSize * 2, 351 / 3, cellSize * 3))
    screen.blit(myFont.render(str(currentNumber), 1, (250, 250, 250)), (351 / 3, cellSize * 2, cellSize, cellSize * 3))

    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < 10 * cellSize and event.pos[1] > 3 * cellSize:
                i = (int) (event.pos[0] / cellSize)
                j = size - 1
                while gameTable[i][j] != 0 and j >= 0:
                    j -= 1
                if gameTable[i][j] == 0:
                    gameTable[i][j] = currentNumber
                    currentNumber = random.randint(1, size)
                    moveCount -= 1


    update()
    draw()
    time.sleep(0.05)
