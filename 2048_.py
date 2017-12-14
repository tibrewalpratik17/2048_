import random, pygame, sys
from pygame.locals import *
from random import randint
import copy
import shelve
#defining the window size and other different specifications of the window
FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
margin = 5
thickness = 0
#defining the RGB for various colours used 
WHITE= (255, 255, 255)
BLACK= (  0,   0,   0)
RED = (255,   0,   0)
GREEN= (  0, 255,   0)
DARKGREEN= (  0, 155,   0)
DARKGRAY= ( 40,  40,  40)
LIGHTSALMON=(255, 160, 122)
ORANGE=(221, 118, 7)
LIGHTORANGE=(227,155,78)
CORAL=(255, 127, 80)
colorback=(189,174,158)
colorblank=(205,193,180)
colorlight=(249,246,242)
colordark=(119,110,101)

dictcolor1={
0:colorblank,
2:(238,228,218),
4:(237,224,200),
8:(242,177,121),
16:(245,149,99),
32:(246,124,95),
64:(246,95,59),
128:(237,207,114),
256:(237,204,97),
512:(237,200,80),
1024:(237,197,63),
2048:(237,194,46) }

dictcolor2={
2:colordark,
4:colordark,
8:colorlight,
16:colorlight,
32:colorlight,
64:colorlight,
128:colorlight,
256:colorlight,
512:colorlight,
1024:colorlight,
2048:colorlight }
BGCOLOR = LIGHTORANGE
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
LEVEL = 0
boxsize = 100
TABLE = [[]]
backupTABLE = [[]]
Score = 0
highScore = 0
def main():
    global FPSCLOCK, screen, BASICFONT, highScore
    highScoreStorage = shelve.open('score.txt')
    try:
        highScore = highScoreStorage['highscore']
    except Exception as e:
        print ('Could not fetch highScore from storage')
        highScore = 0
        
    highScoreStorage.close()
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('2048')

    showStartScreen()

    while True:
        runGame(TABLE)
        gameover()


def showStartScreen():
#the start screen
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('2048', True, WHITE, ORANGE)
    drawPressKeyMsg()   

    while True:
        screen.fill(BGCOLOR)
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        screen.blit(display_rect, rectangle)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def randomfill(TABLE):
    # search for zero in the game table and randomly fill the places
    flatTABLE = sum(TABLE,[])
    if 0 not in flatTABLE:
        return TABLE
    empty=False
    w=0
    while not empty:
        w=randint(0,LEVEL*LEVEL-1)
        if TABLE[w//LEVEL][w%LEVEL] == 0:
            empty=True
    z=randint(1,5)
    if z==5:
        TABLE[w//LEVEL][w%LEVEL] = 4
    else:
        TABLE[w//LEVEL][w%LEVEL] = 2
    return TABLE

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Enter the level you want to play ( 3 - 7 )', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (5, WINDOWHEIGHT - 30)
    screen.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():

    global LEVEL,boxsize, TABLE

    #checking if a key is pressed or not
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None

    keyDownEvents = pygame.event.get(KEYDOWN)
   
    LEVEL = 3

    for event in keyDownEvents :
        try:
            LEVEL = int(event.unicode)
        except Exception as e:
            print('Non-numeric data entered')
            LEVEL = 3

    # boxsize = min(WINDOWWIDTH,WINDOWHEIGHT)//LEVEL;
    TABLE = [[0 for x in range(LEVEL)] for y in range(LEVEL)]

    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def show(TABLE):
    #showing the table
    screen.fill(colorback)
    myfont = pygame.font.SysFont("Arial", 100, bold=True)
    for i in range(LEVEL):
        for j in range(LEVEL):
            pygame.draw.rect(screen, dictcolor1[TABLE[i][j]], (j*boxsize+margin,
                                              i*boxsize+margin,
                                              boxsize-2*margin,
                                              boxsize-2*margin),
                                              thickness)
            if TABLE[i][j] != 0:
                label = myfont.render("%s" %(TABLE[i][j]), 1, dictcolor2[TABLE[i][j]] )
                screen.blit(label, (j*boxsize+margin, i*boxsize+margin))

    myfont = pygame.font.SysFont("Arial", 50)
    label = myfont.render('Score '+str(Score), 1, RED,WHITE )
    screen.blit(label, (0, LEVEL*boxsize+2*margin))
    label = myfont.render('High Score '+str(highScore), 1, RED,WHITE )
    screen.blit(label, (0, 50 + LEVEL*boxsize+4*margin))
    pygame.display.update()

def runGame(TABLE):
    global Score, highScore
    TABLE=randomfill(TABLE)
    TABLE=randomfill(TABLE)
    show(TABLE)
    backupTABLE = TABLE
    running=True
    backspaceOnceHit = True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print ("quit")
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if running:
                    desired_key = None
                    if event.key == pygame.K_UP    : desired_key = "w"
                    if event.key == pygame.K_DOWN  : desired_key = "s"
                    if event.key == pygame.K_LEFT  : desired_key = "a"
                    if event.key == pygame.K_RIGHT : desired_key = "d"
                    if event.key == pygame.K_BACKSPACE: desired_key = "backspace"

                    if desired_key is "backspace":
                        if not backspaceOnceHit:
                            TABLE = backupTABLE
                            backspaceOnceHit = True
                            show(TABLE)
                        continue

                    if desired_key is None:
                        continue

                    new_table = key(desired_key, copy.deepcopy(TABLE))
                    if Score > highScore :
                        highScore = Score
                        highScoreStorage = shelve.open('score.txt')
                        highScoreStorage['highscore'] = highScore
                        highScoreStorage.close()

                    if new_table != TABLE:
                        backspaceOnceHit = False
                        backupTABLE = TABLE
                        TABLE=randomfill(new_table)
                        show(TABLE)
 
def key(DIRECTION,TABLE):
    if   DIRECTION =='w':
        for pi in range(1,LEVEL):
            for pj in range(LEVEL):
                if TABLE[pi][pj] !=0: TABLE=moveup(pi,pj,TABLE)
    elif DIRECTION =='s':
        for pi in range(LEVEL-2,-1,-1):
            for pj in range(LEVEL):
                if TABLE[pi][pj] !=0: TABLE=movedown(pi,pj,TABLE)
    elif DIRECTION =='a':
        for pj in range(1,LEVEL):
            for pi in range(LEVEL):
                if TABLE[pi][pj] !=0: TABLE=moveleft(pi,pj,TABLE)
    elif DIRECTION =='d':
        for pj in range(LEVEL-2,-1,-1):
            for pi in range(LEVEL):
                if TABLE[pi][pj] !=0: TABLE=moveright(pi,pj,TABLE)
    return TABLE

def movedown(pi,pj,T):
    global Score
    justcomb=False
    while pi < LEVEL-1 and (T[pi+1][pj] == 0 or (T[pi+1][pj] == T[pi][pj] and not justcomb)):
        if T[pi+1][pj] == 0:
            T[pi+1][pj] = T[pi][pj]
            T[pi][pj]=0
            pi+=1
        elif T[pi+1][pj]==T[pi][pj]:
            T[pi+1][pj] += T[pi][pj]
            Score += T[pi+1][pj]
            T[pi][pj] = 0
            pi+=1
            justcomb=True
    return T

def moveleft(pi,pj,T):
    global Score
    justcomb=False
    while pj > 0 and (T[pi][pj-1] == 0 or (T[pi][pj-1] == T[pi][pj-1] and not justcomb)):
        if T[pi][pj-1] == 0:
            T[pi][pj-1] = T[pi][pj]
            T[pi][pj]=0
            pj-=1
        elif T[pi][pj-1]==T[pi][pj]:
            T[pi][pj-1] += T[pi][pj]
            Score += T[pi][pj-1]
            T[pi][pj] = 0
            pj-=1
            justcomb=True
    return T

def moveright(pi,pj,T):
    global Score
    justcomb=False
    while pj < LEVEL-1 and (T[pi][pj+1] == 0 or (T[pi][pj+1] == T[pi][pj+1] and not justcomb)):
        if T[pi][pj+1] == 0:
            T[pi][pj+1] = T[pi][pj]
            T[pi][pj]=0
            pj+=1
        elif T[pi][pj+1]==T[pi][pj]:
            T[pi][pj+1] += T[pi][pj]
            Score += T[pi][pj+1]
            T[pi][pj] = 0
            pj+=1
            justcomb=True
    return T

def moveup(pi,pj,T):
    global Score
    justcomb=False
    while pi > 0 and (T[pi-1][pj] == 0 or (T[pi-1][pj] == T[pi][pj] and not justcomb)):
        if T[pi-1][pj] == 0:
            T[pi-1][pj] = T[pi][pj]
            T[pi][pj]=0
            pi-=1
        elif T[pi-1][pj]==T[pi][pj]:
            T[pi-1][pj] += T[pi][pj]
            Score += T[pi-1][pj]
            T[pi][pj] = 0
            pi-=1
            justcomb=True
    return T
        
def terminate():
    pygame.quit()
    sys.exit()

main()