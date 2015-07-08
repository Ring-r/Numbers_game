# !/usr/bin/python

import pygame
import time
import sys
import random

pygame.init()
pygame.display.set_caption("Numbers")
screenSize = (351, 600)
screen = pygame.display.set_mode(screenSize, 0, 32)
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
colorWhite = (255, 255, 255)
colorRed = (255, 0, 0)
colorGreen = (0, 255, 0)
colorBlue = (0, 0, 255)
palette = [(255, 102, 102), (255, 178, 102), (255, 255, 102), (102, 255, 102), (102, 255, 255), (102, 102, 255), (178, 102, 255)]


endGame = False


def AddNumber(x):
    global currentNumber
    global moveCount
    i = int(x / cellSize)
    j = size - 1
    while gameTable[i][j] != 0 and j >= 0:
        j -= 1
    if gameTable[i][j] == 0:
        gameTable[i][j] = currentNumber
        currentNumber = random.randint(1, size)
        moveCount -= 1


def AddRow():
    global moveCount
    for i in range(size):
        j = 1
        while j < size:
            gameTable[i][j - 1] = gameTable[i][j]
            j += 1
        gameTable[i][size - 1] = 2 * size + random.randint(1, size)
    moveCount = 10


def EndBeforeNewRow():
    elCount = 0
    for i in range(size):
        if gameTable[i][0] != 0:
            elCount += 1
    return elCount == size


def EndAfterNewRow():
    elCount = 0
    for i in range(size):
        if gameTable[i][0] != 0:
            elCount += 1
    return elCount != 0


def Delete():
    global score
    rowElCount = [0 for i in range(size)]
    colElCount = [0 for i in range(size)]
    delTable = []
    for i in range(size):
        delTable.append([0] * size)

    for i in range(size):
        rowElCount[i] = 0
        colElCount[i] = 0
        for j in range(size):
            if gameTable[i][j] != 0:
                rowElCount[i] += 1
            if gameTable[j][i] != 0:
                colElCount[i] += 1

    for i in range(size):
        for j in range(size):
            if gameTable[i][j] != 0 and (gameTable[i][j] == rowElCount[i] or gameTable[i][j] == colElCount[j]):
                delTable[i][j] = 1

    for i in range(size):
        for j in range(size):
            if delTable[i][j] != 0:
                gameTable[i][j] = 0
                if i > 0 and gameTable[i - 1][j] > size:
                    gameTable[i - 1][j] -= size
                if i < size - 1 and gameTable[i + 1][j] > size:
                    gameTable[i + 1][j] -= size
                if j > 0 and gameTable[i][j - 1] > size:
                    gameTable[i][j - 1] -= size
                if j < size - 1 and gameTable[i][j + 1] > size:
                    gameTable[i][j + 1] -= size
                score += 1

    for j in range(size):
        i = size - 2
        while i >= 0:
            if gameTable[j][i] != 0 and gameTable[j][i + 1] == 0:
                gameTable[j][i + 1] = gameTable[j][i]
                gameTable[j][i] = 0
            i -= 1


def Restart():
    global score
    global bestScore
    global moveCount
    for i in range(size):
        for j in range(size):
            gameTable[i][j] = 0
    if score > bestScore:
        bestScore = score
    score = 0
    moveCount = 10


def Draw():
    screen.fill((0, 0, 0))
    for i in range(size):
        for j in range(size):
            pygame.draw.rect(screen, colorWhite, (i * cellSize, j * cellSize + 3 * cellSize, cellSize, cellSize),
                             2)
            if gameTable[i][j] != 0:
                if gameTable[i][j] <= size:
                    pygame.draw.rect(screen, palette[gameTable[i][j] - 1], (i * cellSize + 5, j * cellSize + 3 * cellSize + 5, cellSize - 10, cellSize - 10),
                                     0)
                    text = myFont.render(str(gameTable[i][j]), 1, colorWhite)
                else:
                    if gameTable[i][j] <= 2 * size:
                        pygame.draw.rect(screen, colorGreen, (i * cellSize + 5, j * cellSize + 3 * cellSize + 5, cellSize - 10, cellSize - 10),
                                         0)
                        text = myFont.render("!", 1, colorWhite)
                    else:
                        pygame.draw.rect(screen, colorBlue, (i * cellSize + 5, j * cellSize + 3 * cellSize + 5, cellSize - 10, cellSize - 10),
                                         0)
                        text = myFont.render("!!", 1, colorWhite)
                screen.blit(text, (i * cellSize, j * cellSize + 3 * cellSize, cellSize, cellSize))

    labelMove = myFont.render("Move", 1, colorWhite)
    screen.blit(labelMove, (0, 0, screenSize[0] / 3, cellSize))
    screen.blit(myFont.render(str(moveCount), 1, colorWhite), (0, cellSize, screenSize[0] / 3, cellSize * 2))

    labelScore = myFont.render("Score", 1, colorWhite)
    screen.blit(labelScore, (screenSize[0] / 3, 0, screenSize[0] / 3, cellSize))
    screen.blit(myFont.render(str(score), 1, colorWhite),
                (screenSize[0] / 3, cellSize, screenSize[0] / 3, cellSize * 2))

    labelRecord = myFont.render("Record", 1, colorWhite)
    screen.blit(labelRecord, (screenSize[0] * 2 / 3, 0, screenSize[0] / 3, cellSize))
    screen.blit(myFont.render(str(bestScore), 1, colorWhite),
                (screenSize[0] * 2 / 3, cellSize, screenSize[0] / 3, cellSize * 2))

    labelNext = myFont.render("Next", 1, colorWhite)
    screen.blit(labelNext, (0, cellSize * 2, screenSize[0] / 3, cellSize * 3))
    screen.blit(myFont.render(str(currentNumber), 1, colorWhite),
                (screenSize[0] / 3, cellSize * 2, cellSize, cellSize * 3))

    labelRestart = myFont.render("Restart", 1, colorWhite)
    screen.blit(labelRestart, (screenSize[0] / 3, cellSize * 10.5, screenSize[0] / 3, cellSize * 11.5))
    pygame.draw.rect(screen, colorWhite, (2 * cellSize, 10.4 * cellSize, 3 * cellSize, cellSize),
                     2)

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
            if event.button == 1:
                if 10 * cellSize > event.pos[1] > 3 * cellSize:
                    if not endGame:
                        AddNumber(event.pos[0])
                if 2 * cellSize < event.pos[0] < 5 * cellSize and 10.4 * cellSize < event.pos[1] < 11.4 * cellSize:
                    Restart()
    Delete()
    endGame = EndBeforeNewRow() or (moveCount == 0 and EndAfterNewRow())
    if not endGame and moveCount == 0:
        AddRow()
    Draw()
    time.sleep(0.05)
