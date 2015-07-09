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
for x in range(size):
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
colorBlack = (0, 0, 0)
palette = [(255, 51, 51), (255, 153, 51), (255, 255, 51), (0, 255, 128), (51, 153, 255), (51, 51, 255), (255, 51, 153)]

endGame = False


def AddNumber(x):
    global currentNumber, moveCount
    i = int(x / cellSize)
    j = 0
    if gameTable[i][j] == 0:
        gameTable[i][j] = currentNumber
        if score > 0 and score % 10 == 0:
            currentNumber = 2 * size + random.randint(1, size)
        else:
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


def CreateDelTable():
    notNull = False
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
                notNull = True

    return notNull, delTable


def Delete(delTable):
    global score
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


def ShiftDown():
    repeat = False
    for j in range(size):
        i = size - 2
        while i >= 0:
            if gameTable[j][i] != 0 and gameTable[j][i + 1] == 0:
                gameTable[j][i + 1] = gameTable[j][i]
                gameTable[j][i] = 0
                repeat = True
            i -= 1
    return repeat


def Restart():
    global score, bestScore, moveCount, endGame
    for i in range(size):
        for j in range(size):
            gameTable[i][j] = 0
    if score > bestScore:
        bestScore = score
    score = 0
    moveCount = 10
    endGame = False


def Draw():
    screen.fill(colorBlack)
    for i in range(size):
        for j in range(size):
            pygame.draw.rect(screen, colorWhite, (i * cellSize, j * cellSize + 3 * cellSize, cellSize, cellSize),
                             2)
            if gameTable[i][j] != 0:
                if gameTable[i][j] <= size:
                    pygame.draw.rect(screen, palette[gameTable[i][j] - 1],
                                     (i * cellSize + 5, j * cellSize + 3 * cellSize + 5, cellSize - 9, cellSize - 9),
                                     0)
                    text = myFont.render(str(gameTable[i][j]), 1, colorWhite)
                    screen.blit(text, (i * cellSize, j * cellSize + 3 * cellSize, cellSize, cellSize))
                else:
                    if gameTable[i][j] <= 2 * size:
                        pygame.draw.rect(screen, colorWhite, (
                            i * cellSize + 5, j * cellSize + 3 * cellSize + 5, cellSize - 9, cellSize - 9),
                                         0)

                    else:
                        pygame.draw.rect(screen, colorWhite, (
                            i * cellSize + 5, j * cellSize + 3 * cellSize + 5, cellSize - 9, cellSize - 9),
                                         2)
                        pygame.draw.rect(screen, colorWhite, (
                            i * cellSize + 10, j * cellSize + 3 * cellSize + 10, cellSize - 18, cellSize - 18),
                                         0)

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
    if currentNumber > 2 * size:
        pygame.draw.rect(screen, colorWhite, (screenSize[0] / 3 + 5, cellSize * 2 + 5, cellSize - 9, cellSize - 9),
                         2)
        pygame.draw.rect(screen, colorWhite, (screenSize[0] / 3 + 10, cellSize * 2 + 10, cellSize - 18, cellSize - 18),
                         0)
    else:
        pygame.draw.rect(screen, palette[currentNumber - 1],
                         (screenSize[0] / 3 + 5, cellSize * 2 + 5, cellSize - 9, cellSize - 9),
                         0)
        screen.blit(myFont.render(str(currentNumber), 1, colorWhite),
                    (screenSize[0] / 3, cellSize * 2, cellSize, cellSize))

    labelRestart = myFont.render("Restart", 1, colorWhite)
    screen.blit(labelRestart, (screenSize[0] / 3, cellSize * 10.5, screenSize[0] / 3, cellSize * 11.5))
    pygame.draw.rect(screen, colorWhite, (2 * cellSize, 10.4 * cellSize, 3 * cellSize, cellSize),
                     2)

    if endGame:
        DrawEndGame()

    pygame.display.flip()


def DrawEndGame():
    overlay = pygame.Surface((351, 200))
    overlay.set_alpha(200)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, screenSize[1] / 3))

    text = myFont.render("Game Over!", 1, colorBlack, colorWhite)
    loc = text.get_rect()
    loc.center = screen.get_rect().center
    screen.blit(text, loc)


Update = None
pos = None


def UpdateAdd():
    global Update, pos
    if pos is not None:
        if 10 * cellSize > pos[1] > 3 * cellSize:
            if not endGame:
                AddNumber(pos[0])
                Update = UpdateShift
    pos = None


def UpdateDel():
    global Update
    isDel = CreateDelTable()
    if isDel[0]:
        Delete(isDel[1])
        Update = UpdateShift
    else:
        Update = UpdateRow


def UpdateRow():
    global Update, endGame
    endGame = EndBeforeNewRow() or (moveCount == 0 and EndAfterNewRow())
    if not endGame and moveCount == 0:
        AddRow()
        Update = UpdateDel
    else:
        Update = UpdateAdd


def UpdateShift():
    global Update
    if not ShiftDown():
        Update = UpdateDel


Update = UpdateAdd
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
                e = True
                pos = event.pos
                if 2 * cellSize < event.pos[0] < 5 * cellSize and 10.4 * cellSize < event.pos[1] < 11.4 * cellSize:
                    Restart()
    Update()
    Draw()

    time.sleep(0.05)
