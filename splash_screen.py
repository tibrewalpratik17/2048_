import time
import math
import random, pygame, sys
from pygame.locals import *
from random import randint
import copy
pygame.init()

FPS =5
colorblank=(205,193,180)
black = [40,40,40]
LIGHT_CREAM_MORE = [255, 245, 240]
LIGHT_CREAM = [  255, 247, 225 ]
WHITE = [255,255,255]
back = [189,174,158]
front = [119,110,101]
green = [ 120,120,120]
ORANGE=(221, 118, 7)

WINDOWWIDTH = 640
WINDOWHEIGHT = 640
global FPSCLOCK, screen, BASICFONT

FPSCLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf', 24)
BASICFONT_SMALL = pygame.font.Font('freesansbold.ttf', 12)
MEDIUMFONT =   pygame.font.Font('freesansbold.ttf', 36)
MEDIUMFONT_SMALL =   pygame.font.Font('freesansbold.ttf', 18)
smallfont = pygame.font.SysFont("freesansbold.ttf", 124)



size = [WINDOWWIDTH, WINDOWHEIGHT]

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

progress = 0

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text



def howtoplay():
    cond = True
    h2p = '''The game's objective is to slide numbered tiles on a grid to combine them to create a tile with the number 2048. However, you can keep playing the game, creating tiles with larger numbers. 2048 is played on a 4X4 grid, with numbered tiles that slide smoothly when a player moves them using the four arrow keys. Every turn, a new tile will randomly appear in an empty spot on the board with a value of either 2 or 4. Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid. If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided. The resulting tile cannot merge with another tile again in the same move. Higher-scoring tiles emit a soft glow. A scoreboard on the upper-right keeps track of the user's score. The user's score starts at zero, and is incremented whenever two tiles combine, by the value of the new tile. As with many arcade games, the user's best score is shown alongside the current score. '''
    while cond:
        screen.fill(LIGHT_CREAM_MORE)
        #pygame.draw.line(screen, black, (320,0), (320,640), 2)
        #pygame.draw.line(screen, black, (0, 320), (640, 320), 2)
        
        pygame.draw.rect(screen, WHITE, [187,47,276,56])
        pygame.draw.rect(screen, front, [190,50, 270, 50])

        How2play = MEDIUMFONT.render("HOW TO PLAY", True, WHITE)
        screen.blit(How2play, [200 , 60])

        Hien = BASICFONT_SMALL.render("Hit BACKSPACE to go back", True, black)
        screen.blit(Hien, [245, 580])
        pygame.draw.rect(screen, ORANGE, [50,120,540,400])
        rect_h2p = pygame.draw.rect(screen, ORANGE, [70,140,500,380])
        drawText(screen, h2p, WHITE, rect_h2p, MEDIUMFONT_SMALL )
        for event in pygame.event.get():
            if event.type == QUIT:
                print "quit"
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    cond = False
        
        pygame.display.flip()



def terminate():
    pygame.quit()
    sys.exit()

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def loading(progress, prg):
    if progress < 100:
        text = smallfont.render(str(int(prg)), True, black )
    else:
        text = smallfont.render("2048", True, black)

    screen.blit(text, [220 , 120])

def message_to_screen(msg, color, y_displace = 0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (WINDOWWIDTH/2), (WINDOWHEIGHT/2) + y_displace
    screen.blit(textSurf, textRect)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    screen.blit(pressKeySurf, pressKeyRect)

def choose_main(last):
    active = last
    cond = True
    while cond:
        for event in pygame.event.get():
            if event.type == QUIT:
                print "quit"
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if active == 1:
                        active = 2
                        return active
                    elif active == 2:
                        active = 3
                        return active
                    elif active == 3:
                        active = 1
                        return active
            
                if event.key == pygame.K_UP:
                    if active == 1:
                        active = 3
                        return active
                    elif active == 2:
                        active = 1
                        return active
                    elif active == 3:
                        active = 2
                        return active
            
                if event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                    cond = False
                    return active+3
        return active


def keep_looping():
    win_img = pygame.image.load('wind.png')
    win_img = pygame.transform.scale2x(win_img)
    ret_choose = 1
    last = 1
    while True:
        if last == 1:
            cords = [144,234,362,92]
        elif last == 2:
            cords = [144,374,362,82]
        elif last == 3:
            cords = [144,464,362,82]
        screen.fill(LIGHT_CREAM_MORE)
        text = smallfont.render("2048", True, black)
        screen.blit(text, [220 , 120])
        pygame.draw.rect(screen, black, cords)
        pygame.draw.rect(screen, ORANGE, [150,240,350,80])
        pygame.draw.rect(screen, front, [150,380,350,70])
        pygame.draw.rect(screen, front, [150,470,350,70])
        How2play = BASICFONT.render("HOW TO PLAY", True, WHITE)
        EXIT = BASICFONT.render("EXIT", True, WHITE)
        START = MEDIUMFONT.render("START", True, WHITE)
        screen.blit(win_img, [165, 251])
        screen.blit(START, [280, 267])
        screen.blit(How2play, [242 , 403])
        screen.blit(EXIT, [288 , 493])
        
        ret_choose = choose_main(last)
        last = ret_choose

        if ret_choose == 4 :
            #start the game
            return

        elif ret_choose == 5:
            #How to play
            howtoplay()
            last = ret_choose-3

        elif ret_choose == 6:
            #exit
            terminate()

        pygame.display.flip()
        
        FPSCLOCK.tick(FPS+25)

while (progress/2) <100:
    time_count = (random.randint(1,50)/50)
    increase = random.randint(1,2)
    progress += increase
    screen.fill(LIGHT_CREAM)
    prg = math.pow(2,(progress/2)//10)
    pygame.draw.rect(screen, ORANGE, [219,239,206,50], 1)
    if (progress/2) > 100:
        pygame.draw.rect(screen, ORANGE, [222,242,200,44])
    else:
        pygame.draw.rect(screen, ORANGE, [222,242,progress,44])
    loading(progress/2, prg)
    pygame.display.flip()

    time.sleep(time_count)

time.sleep(0.5)
keep_looping()



