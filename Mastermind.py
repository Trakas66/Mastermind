import pygame
import random
import time
import json

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.flip()

Black = pygame.Color(0, 0, 0)
White = pygame.Color(255, 255, 255)
DarkGrey = pygame.Color(20, 20, 20)
MediumGrey = pygame.Color(70, 70, 70)
Grey = pygame.Color(100, 100, 100)

Red = pygame.Color(255, 0, 0)
Green = pygame.Color(0, 255, 0)
Blue = pygame.Color(0, 0, 255)
Purple = pygame.Color(148, 0, 211)
Pink = pygame.Color(255, 51, 255)
Yellow = pygame.Color(255, 255, 0)
Orange = pygame.Color(255, 128, 0)
Cyan = pygame.Color(0, 255, 255)

colours = [Red, Green, Blue, Purple, Pink, Yellow, Orange, Cyan]
colourNames = {'Red':True, 'Green':True, 'Blue':True,
               'Purple':True, 'Pink':True, 'Yellow':True,
               'Orange':True, 'Cyan':True}
players = 1

settings = {'colours':colourNames, 'players':players}

file = open(r'C:\Users\jason\Python projects\Mastermind\Settings.txt', 'r')
settings = json.load(file)

font = pygame.font.SysFont(None, 30)
smallFont = pygame.font.SysFont('ARIAL', 20)
bigFont = pygame.font.SysFont('TIMESNEWROMAN', 60)
gamestatus = 'play'

def Menu():
    global gamestatus
    title = 'MASTERMIND'
    titlePos = [(230, 200), (290, 200), (340, 200), (380, 200),
                (420, 200), (470, 200), (520, 200), (580, 200),
                (610, 200), (660, 200)]
    currentTitle = []
    counter = 0
    playButton = pygame.Rect(450, 350, 100, 50)
    while gamestatus == 'menu':
        screen.fill(Black)
        if counter == 0:
            currentTitle = []
            for i in range(len(title)):
                text = bigFont.render(f'{title[i]}', True, random.choice(colours))
                screen.blit(text, (titlePos[i][0] + 40, titlePos[i][1]))
                currentTitle.append(text)
            counter += 1
        else:
            for i in range(len(currentTitle)):
                screen.blit(currentTitle[i], (titlePos[i][0] + 40, titlePos[i][1]))
            counter += 1
            if counter == 1000:
                counter = 0

        pygame.draw.rect(screen, DarkGrey, (playButton.x - 5, playButton.y - 5, playButton.width + 10, playButton.height + 10))
        pygame.draw.rect(screen, Grey, playButton)

        pygame.display.flip()

class Spot:
    button = pygame.Rect(0, 0, 0, 0)
    color = None

    def __init__(self, pos):
        self.button = pygame.Rect(pos[0], pos[1], 50, 50)
        self.color = None

    def edit(self):
        color = EditColor()
        if color != None:
            self.color = color

class ColourButton:
    button = pygame.Rect(0, 0, 0, 0)
    color = None

    def __init__(self, pos, colour):
        self.button = pygame.Rect(pos[0], pos[1], 40, 40)
        self.color = colour

def InitializeGame():
    global board
    global hints
    width, height = 5, 13
    board = [[0 for i in range(width)] for j in range(height)]
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = Spot((50 * j + 200, 50 * i + 100))

    width, height = 5, 13
    hints = [[None for i in range(width)] for j in range(height)]

def DrawBoard(show = False, update = True):
    screen.fill(Black)
    pygame.draw.rect(screen, DarkGrey, (180, 100, len(board[0]) * 50 + 20 + len(hints[0]) * 30, len(board) * 50 + 20))
    pygame.draw.rect(screen, Grey, (200, 100, len(board[0]) * 50 + len(hints[0]) * 30, len(board) * 50))
    for i in range(len(board)):
        for j in range(len(board[0])):
            pygame.draw.circle(screen, DarkGrey, (50 * j + 225, 50 * i + 125), 15)
            if show == False and i == 0:
                continue
            else:
                if board[i][j].color != None:
                    pygame.draw.circle(screen, board[i][j].color, (50 * j + 225, 50 * i + 125), 13)

    for i in range(len(hints)):
        for j in range(len(hints[0])):
            pygame.draw.circle(screen, MediumGrey, (30 * j + 465, 50 * i + 125), 8)
            if hints[i][j] != None:
                pygame.draw.circle(screen, hints[i][j], (30 * j + 465, 50 * i +125), 7)

    pygame.draw.rect(screen, Grey, (450, 100, 150, 50))

    if show == False:
        pygame.draw.rect(screen, Grey, (200, 100, 250, 50))
        text = font.render('CODE HIDDEN', True, White)
        screen.blit(text, (250, 115))

    doneButton = pygame.Rect(275, len(board) * 50 + 150, 75, 40)
    pygame.draw.rect(screen, DarkGrey, (doneButton.x - 5, doneButton.y - 5, doneButton.width + 10, doneButton.height + 10))
    pygame.draw.rect(screen, Grey, doneButton)
    text = font.render('Done', True, Black)
    screen.blit(text, (doneButton.x + 15, doneButton.y + 10))

    if update:
        pygame.display.flip()
    return doneButton

def DrawColors():
    positions = [(360, 415), (420, 415), (480, 415),
                 (540, 415), (600, 415), (360, 485),
                 (420, 485), (480, 485), (540, 485),
                 (600, 485)]
    buttons = []
    pygame.draw.rect(screen, DarkGrey, (345, 395, 310, 210))
    pygame.draw.rect(screen, Grey, (350, 400, 300, 200))
    for i in range(len(colours)):
        button = ColourButton(positions[i], colours[i])
        buttons.append(button)
        pygame.draw.rect(screen, button.color, button.button)
    backButton = pygame.Rect(360, 565, 60, 30)
    pygame.draw.rect(screen, DarkGrey, (358, 563, 64, 34))
    pygame.draw.rect(screen, Grey, backButton)
    text = smallFont.render('Cancel', True, White)
    screen.blit(text, (365, 570))
    pygame.display.flip()
    return buttons, backButton

def EditColor():
    loop = True
    while loop:
        buttons, cancel = DrawColors()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.button.collidepoint(event.pos):
                        return button.color
                if cancel.collidepoint(event.pos):
                    return None

    return None

def PickCode1P():
    global code
    code = []
    for i in range(5):
        color = random.choice(colours)
        code.append(color)
        board[0][i].color = color
    #print(code)

def RevealCodeAnim(win):
    x = 200
    y = 100
    x2 = 625
    y2 = -62
    if win:
        text = bigFont.render('YOU WIN', True, White)
    else:
        text = bigFont.render('YOU LOSE', True, White)
    for i in range(76):
        DrawBoard(True, False)
        pygame.draw.rect(screen, Grey, (x, y, 250, 50))
        screen.blit(text, (x2, y2))
        pygame.display.flip()
        y -= 2
        y2 += 7
        time.sleep(0.015)

def CheckFilled(line):
    for i in range(5):
        if line[i].color == None:
            return False
    return True

def CheckWin(line):
    for i in range(5):
        if line[i].color != code[i]:
            return False
    return True

def FindColorName(color):
    if color == Black:
        return 'black'
    elif color == White:
        return 'white'
    elif color == Red:
        return 'red'
    elif color == Blue:
        return 'blue'
    elif color == Green:
        return 'green'
    elif color == Purple:
        return 'purple'
    elif color == Pink:
        return 'pink'
    elif color == Yellow:
        return 'yellow'
    elif color == Orange:
        return 'orange'
    elif color == Cyan:
        return 'cyan'

def CheckLine(line, lineNum):
    total = {}
    checkList = []
    codeColors = {}
    hintLine = []
    for i in range(5):
        color = FindColorName(line[i].color)
        if not color in total:
            total[color] = 0
        total[color] += 1
        checkList.append(line[i].color)

    for i in range(5):
        color = FindColorName(code[i])
        if not color in codeColors:
            codeColors[color] = 0
        codeColors[color] += 1

    for i in range(5):
        if checkList[i] == code[i]:
            color = FindColorName(checkList[i])
            hintLine.append(Black)
            total[color] -= 1
            codeColors[color] -= 1
            checkList[i] = 0

    for i in range(5):
        if checkList[i] != 0:
            color = FindColorName(checkList[i])
            if color in codeColors:
                if codeColors[color] > 0:
                    hintLine.append(White)
                    total[color] -= 1
                    codeColors[color] -= 1
                    checkList[i] = 0

    while len(hintLine) < 5:
        hintLine.append(None)

    hints[lineNum] = hintLine

def Turn():
    line = 0
    lineNum = 0
    for i in range(len(board)):
        if board[i][0].color != None and i != 0:
            line = board[i - 1]
            lineNum = i - 1
            break

    if line == 0:
        line = board[len(board) - 1]
        lineNum = len(board) - 1

    loop = True
    while loop:
        doneButton = DrawBoard()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for spot in line:
                    if spot.button.collidepoint(event.pos):
                        spot.edit()
                        board[lineNum] = line
                        break
                if doneButton.collidepoint(event.pos):
                    if CheckFilled(line):
                        loop = False
                        break
    return line, lineNum

def Game1():
    global gamestatus
    InitializeGame()
    PickCode1P()
    loop = True
    while loop:
        line, lineNum = Turn()
        if CheckWin(line):
            RevealCodeAnim(True)
            gamestatus = 'Win'
            break
        elif lineNum == 1:
            RevealCodeAnim(False)
            gamestatus = 'Lose'
            break
        CheckLine(line, lineNum)

def main():
    loop = True
    while loop:
        if gamestatus == 'menu':
            Menu()
        elif gamestatus == 'play':
            Game1()


main()
