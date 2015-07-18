# !/usr/bin/python

import pygame
import time
import sys
import random

class Score:
    score = 0
    bestScore = 0
    fileName = 'bestscore.txt'

    def __init__(self):
        try:
            f = open(self.fileName, 'r')
            self.bestScore = int(f.read())
        finally:
            try:
                f.close()
            except:
                pass

    def Clear(self):
        self.score = 0

    def Increase(self):
        self.score += 1
        if self.score > self.bestScore:
            self.bestScore = self.score
            f = open(self.fileName, 'w')
            f.write(str(self.bestScore))
            f.close()



pygame.init()
pygame.display.set_caption("Numbers")
screenSize = (350, 600)
screen = pygame.display.set_mode(screenSize, 0, 32)

screenW = screenSize[0]
headerH = 3 * (screenSize[1] - screenSize[0]) / 5
footerH = 2 * (screenSize[1] - screenSize[0]) / 5

size = 7
cellSize = screenSize[0] / size
gameTable = []
for x in range(size):
    gameTable.append([0] * size)

currentNumber = random.randint(1, size)

moveCount = 10
score = Score()

colorWhite = (255, 255, 255)
colorRed = (255, 0, 0)
colorGreen = (0, 255, 0)
colorBlue = (0, 0, 255)
colorBlack = (0, 0, 0)
palette = [(255, 51, 51), (255, 153, 51), (255, 255, 51), (0, 255, 128), (51, 153, 255), (51, 51, 255), (255, 51, 153)]

myFont = pygame.font.SysFont("Monospace", 30)
labelMove = myFont.render("Moves", 1, colorWhite)
labelScore = myFont.render("Score", 1, colorWhite)
labelRecord = myFont.render("Record", 1, colorWhite)
labelNext = myFont.render("Next", 1, colorWhite)
labelRestart = myFont.render("Restart", 1, colorWhite)
labelTutor = myFont.render("?", 1, colorWhite)
numbers = [None for i in range(size)]
for i in range(size):
    numbers[i] = myFont.render(str(i + 1), 10, colorBlack)

endGame = False
pause = False

def AddNumber(x):
    global currentNumber, moveCount
    i = int(x / cellSize)
    j = 0
    if gameTable[i][j] == 0:
        gameTable[i][j] = currentNumber
        if random.random() < 0.05:
            currentNumber = 2 * size + random.randint(1, size)
        else:
            if random.random() < 0.2:
                currentNumber = 100
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
            if gameTable[i][j] != 0 and (gameTable[i][j] == rowElCount[i] or gameTable[i][j] == colElCount[j] or gameTable[i][j] == 100):
                delTable[i][j] = 1
                notNull = True

    return notNull, delTable


def DeleteBomb(i, j):
    gameTable[i][j] = 0
    if i > 0:
        if gameTable[i - 1][j] > size:
            gameTable[i - 1][j] -= size
        else:
            gameTable[i - 1][j] = 0
            score.Increase()
    if i < size - 1:
        if gameTable[i + 1][j] > size:
            gameTable[i + 1][j] -= size
        else:
            gameTable[i + 1][j] = 0
            score.Increase()
    if j > 0:
        if gameTable[i][j - 1] > size:
            gameTable[i][j - 1] -= size
        else:
            gameTable[i][j - 1]
            score.Increase()
    if j < size - 1:
        if gameTable[i][j + 1] > size:
            gameTable[i][j + 1] -= size
        else:
            gameTable[i][j + 1] = 0
            score.Increase()


def Delete(delTable):
    global score
    for i in range(size):
        for j in range(size):
            if delTable[i][j] != 0:
                if gameTable[i][j] == 100:
                    DeleteBomb(i, j)
                else:
                    gameTable[i][j] = 0
                    if i > 0 and gameTable[i - 1][j] > size:
                        gameTable[i - 1][j] -= size
                    if i < size - 1 and gameTable[i + 1][j] > size:
                        gameTable[i + 1][j] -= size
                    if j > 0 and gameTable[i][j - 1] > size:
                        gameTable[i][j - 1] -= size
                    if j < size - 1 and gameTable[i][j + 1] > size:
                        gameTable[i][j + 1] -= size
                score.Increase()



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
    global score, moveCount, endGame
    for i in range(size):
        for j in range(size):
            gameTable[i][j] = 0
    score.Clear()
    moveCount = 10
    endGame = False


def Draw():
    screen.fill(colorBlack)
    for i in range(size):
        for j in range(size):
            pygame.draw.rect(screen, colorWhite, (i * cellSize, j * cellSize + headerH, cellSize, cellSize), 1)
            pygame.draw.rect(screen, colorBlue, (i * cellSize + 1, j * cellSize + headerH + 1, cellSize, cellSize), 1)
            if gameTable[i][j] != 0:
                if gameTable[i][j] <= size:
                    pygame.draw.rect(screen, palette[gameTable[i][j] - 1],
                                     (i * cellSize + 5, j * cellSize + headerH + 5, cellSize - 9, cellSize - 9), 0)
                    DrawElement(numbers[gameTable[i][j] - 1], pygame.Rect(i * cellSize, j * cellSize + headerH, cellSize, cellSize))

                else:
                    if gameTable[i][j] == 100:
                        pygame.draw.ellipse(screen, colorRed, (i * cellSize + 5, j * cellSize + headerH + 5, cellSize - 9, cellSize - 9), 0)
                    else:
                        if gameTable[i][j] <= 2 * size:
                            pygame.draw.rect(screen, colorWhite, (
                                i * cellSize + 5, j * cellSize + headerH + 5, cellSize - 9, cellSize - 9), 0)
                        else:
                            pygame.draw.rect(screen, colorWhite, (
                                i * cellSize + 5, j * cellSize + headerH + 5, cellSize - 9, cellSize - 9), 2)
                            pygame.draw.rect(screen, colorWhite, (
                                i * cellSize + 10, j * cellSize + headerH + 10, cellSize - 18, cellSize - 18), 0)

    DrawElement(labelMove, pygame.Rect(0, 0, screenW / 3, headerH / 3))
    textMove = myFont.render(str(moveCount), 1, colorWhite)
    DrawElement(textMove, pygame.Rect(0, headerH / 3, screenW / 3, headerH / 3))

    DrawElement(labelScore, pygame.Rect(screenW / 3, 0, screenW / 3, headerH / 3))
    textScore = myFont.render(str(score.score), 1, colorWhite)
    DrawElement(textScore, pygame.Rect(screenW / 3, headerH / 3, screenW / 3, headerH / 3))

    DrawElement(labelRecord, pygame.Rect(screenW * 2 / 3, 0, screenW / 3, headerH / 3))
    textRecord = myFont.render(str(score.bestScore), 1, colorWhite)
    DrawElement(textRecord, pygame.Rect(screenW * 2 / 3, headerH / 3, screenW / 3, headerH / 3))

    DrawElement(labelNext, pygame.Rect(0, 2 * headerH / 3, screenW / 3, headerH / 3))
    if currentNumber == 100:
        pygame.draw.rect(screen, colorWhite, (screenW / 3 + 5, 2 * headerH / 3 + 5, cellSize - 9, cellSize - 9), 2)
        pygame.draw.ellipse(screen, colorRed,(screenW / 3 + 10, 2 * headerH / 3 + 10, cellSize - 18, cellSize - 18), 0)
    else:
        if currentNumber > 2 * size:
            pygame.draw.rect(screen, colorWhite, (screenW / 3 + 5, 2 * headerH / 3 + 5, cellSize - 9, cellSize - 9), 2)
            pygame.draw.rect(screen, colorWhite, (screenW / 3 + 10, 2 * headerH / 3 + 10, cellSize - 18, cellSize - 18), 0)
        else:
            pygame.draw.rect(screen, palette[currentNumber - 1],
                             (screenW / 3 + 5, 2 * headerH / 3 + 5, cellSize - 9, cellSize - 9), 0)
            DrawElement(numbers[currentNumber - 1], pygame.Rect(screenW / 3, 2 * headerH / 3, cellSize, cellSize))

    DrawElement(labelTutor, pygame.Rect(0, screenSize[1] - footerH, screenW / 3, footerH))
    DrawElement(labelRestart, pygame.Rect(0, screenSize[1] - footerH, screenW, footerH))

    if endGame:
        DrawEndGame()

    if pause:
        DrawAbout()

    pygame.display.flip()

def DrawElement(text, rect):
    loc = text.get_rect()
    loc.center = rect.center
    screen.blit(text, loc)


def DrawEndGame():
    overlay = pygame.Surface((screenW, screenW))
    overlay.set_alpha(200)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, headerH))

    text = myFont.render("Game Over!", 1, colorBlack, colorWhite)
    loc = text.get_rect()
    loc.center = screen.get_rect().center
    screen.blit(text, loc)


def DrawAbout():
    overlay = pygame.Surface((screenW, screenW))
    overlay.set_alpha(200)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, headerH))

    text = myFont.render("Play on!", 1, colorBlack, colorWhite)
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
                if screenW / 3 < pos[0] < 2 * screenW / 3 and screenSize[1] - 2 * footerH / 3 < pos[1] < screenSize[1] - footerH / 3:
                    Restart()
                if 0 < pos[0] < screenW / 3 and screenSize[1] - 2 * footerH / 3 < pos[1] < screenSize[1] - footerH / 3:
                    pause = not pause
    Update()
    Draw()

    time.sleep(0.05)
