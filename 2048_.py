import random, pygame, sys
from pygame.locals import *
from random import randint
from time import sleep
import copy
import math
#defining the window size and other different specifications of the window
FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
boxsize = min(WINDOWWIDTH,WINDOWHEIGHT)//4;
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

fontSize=[100,85,70,55,40]

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

def main():
    global FPSCLOCK, screen, BASICFONT, game_over

    game_over = True
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('2048')

    while True:
        if game_over:
            showStartScreen()
            game_over = False
            TABLE = [[0 for i in range(4)] for i in range(4)]
            
            runGame(TABLE)


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
        w=randint(0,15)
        if TABLE[w//4][w%4] == 0:
            empty=True
    z=randint(1,5)
    if z==5:
        TABLE[w//4][w%4] = 4
    else:
        TABLE[w//4][w%4] = 2
    return TABLE

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    screen.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    #checking if a key is pressed or not
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def show(TABLE):
    #showing the table
    screen.fill(colorback)
    
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, dictcolor1[TABLE[i][j]], (j*boxsize+margin,
                                              i*boxsize+margin,
                                              boxsize-2*margin,
                                              boxsize-2*margin),
                                              thickness)
            if TABLE[i][j] != 0:
                order=int(math.log10(TABLE[i][j]))
                myfont = pygame.font.SysFont("Arial", fontSize[order] , bold=True)
                label = myfont.render("%4s" %(TABLE[i][j]), 1, dictcolor2[TABLE[i][j]] )
                labelRect=label.get_rect()
                labelRect.topleft=(j*boxsize+(-2+2*order)*margin, i*boxsize+(4+2*order)*margin)
                screen.blit(label, labelRect)
    pygame.display.update()

def runGame(TABLE):
    global game_over
    TABLE=randomfill(TABLE)
    TABLE=randomfill(TABLE)
    show(TABLE)
    running=True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print "quit"
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if running:
                    desired_key = None
                    if event.key == pygame.K_UP    : desired_key = "w"
                    if event.key == pygame.K_DOWN  : desired_key = "s"
                    if event.key == pygame.K_LEFT  : desired_key = "a"
                    if event.key == pygame.K_RIGHT : desired_key = "d"

                    if desired_key is None:
                        continue

                    new_table = key(desired_key, copy.deepcopy(TABLE))
                    if new_table != TABLE:
                        TABLE=randomfill(new_table)
                        show(TABLE)
                        
                    if gameOver(TABLE):
                        print 'Game over'
                        game_over=True
                        return
                        
def gameOver(TABLE):
    temp = TABLE
    k = 0
    
    for desired_key in ['w','s','a','d']:
        new_table = key(desired_key, copy.deepcopy(TABLE))
        if new_table == temp: k+=1
        
    return k==4
                        
def key(DIRECTION,TABLE):
    if   DIRECTION =='w':
        for pi in range(1,4):
            for pj in range(4):
                if TABLE[pi][pj] !=0: TABLE=moveup(pi,pj,TABLE)
    elif DIRECTION =='s':
        for pi in range(2,-1,-1):
            for pj in range(4):
                if TABLE[pi][pj] !=0: TABLE=movedown(pi,pj,TABLE)
    elif DIRECTION =='a':
        for pj in range(1,4):
            for pi in range(4):
                if TABLE[pi][pj] !=0: TABLE=moveleft(pi,pj,TABLE)
    elif DIRECTION =='d':
        for pj in range(2,-1,-1):
            for pi in range(4):
                if TABLE[pi][pj] !=0: TABLE=moveright(pi,pj,TABLE)
    return TABLE

def movedown(pi,pj,T):
    justcomb=False
    while pi < 3 and (T[pi+1][pj] == 0 or (T[pi+1][pj] == T[pi][pj] and not justcomb)):
        if T[pi+1][pj] == 0:
            T[pi+1][pj] = T[pi][pj]
        elif T[pi+1][pj]==T[pi][pj]:
            T[pi+1][pj] += T[pi][pj]
            justcomb=True
        T[pi][pj]=0
        pi+=1
    return T

def moveleft(pi,pj,T):
    justcomb=False
    while pj > 0  and (T[pi][pj-1] == 0 or (T[pi][pj-1] == T[pi][pj] and not justcomb)):
        if T[pi][pj-1] == 0:
            T[pi][pj-1] = T[pi][pj]   
        elif T[pi][pj-1]==T[pi][pj]:
            T[pi][pj-1] += T[pi][pj]
            justcomb=True
        T[pi][pj]=0
        pj-=1
    return T

def moveright(pi,pj,T):
    justcomb=False
    while pj < 3 and (T[pi][pj+1] == 0 or (T[pi][pj+1] == T[pi][pj] and not justcomb)):
        if T[pi][pj+1] == 0:
            T[pi][pj+1] = T[pi][pj]
        elif T[pi][pj+1]==T[pi][pj]:
            T[pi][pj+1] += T[pi][pj]
            justcomb=True
        T[pi][pj] = 0
        pj+=1
    return T

def moveup(pi,pj,T):
    justcomb=False
    while pi > 0 and (T[pi-1][pj] == 0 or (T[pi-1][pj] == T[pi][pj] and not justcomb)):
        if T[pi-1][pj] == 0:
            T[pi-1][pj] = T[pi][pj] 
        elif T[pi-1][pj]==T[pi][pj]:
            T[pi-1][pj] += T[pi][pj]
            justcomb=True
        T[pi][pj]=0
        pi-=1
    return T

def terminate():
    pygame.quit()
    sys.exit()

main()
