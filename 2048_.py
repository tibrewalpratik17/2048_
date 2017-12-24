import random, pygame, sys
from pygame.locals import *
from random import randint
import copy
import math
#defining the window size and other different specifications of the window
FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 695
boxsize = min(WINDOWWIDTH,WINDOWHEIGHT)//4
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
BTNBG = (41,37,34)
BTNHLT = (41,37,60)
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

TABLE=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

def main():
    global FPSCLOCK, screen, BASICFONT

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
    myfont = pygame.font.SysFont("Arial", 60, bold=True)
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, dictcolor1[TABLE[i][j]], (j*boxsize+margin,
                                              50+margin+i*boxsize+margin,
                                              boxsize-2*margin,
                                              boxsize-2*margin),
                                              thickness)
            if TABLE[i][j] != 0:
                label = myfont.render("%4s" %(TABLE[i][j]), 1, dictcolor2[TABLE[i][j]] )
                screen.blit(label, (j*boxsize+4*margin, 70+margin+i*boxsize+5*margin))
                
    pygame.display.update()

def runGame(TABLE):
    TABLE=randomfill(TABLE)
    TABLE=randomfill(TABLE)
    show(TABLE)
    running=True
    
    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if margin+100 > mouse[0] > margin and margin+50 > mouse[1] > margin:
            pygame.draw.rect(screen, BTNHLT,(margin,margin,100,50))
            
            if click[0] == 1 and not clicked:
                desired_key, s = dfs(TABLE,0,4)
                new_table = key(desired_key, copy.deepcopy(TABLE))
                
                if desired_key is None:
                    print "No more movements possible"
                    return
                
                if new_table != TABLE:
                    TABLE=randomfill(new_table)
                    show(TABLE)
                    
                clicked = True
                
            if not click[0]: clicked = False
            
        else:
            pygame.draw.rect(screen, BTNBG,(margin,margin,100,50))
            
        myfont = pygame.font.SysFont("Arial", 24, bold=True)
        label = myfont.render("Hint", 1, colorblank)
        screen.blit(label, (5*margin, 4*margin))
    
        for event in pygame.event.get():
            if event.type == QUIT:
                print "quit"
                pygame.quit()
                sys.exit()
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
                        
        pygame.display.update()
 
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
            T[pi][pj]=0
            pi+=1
        elif T[pi+1][pj]==T[pi][pj]:
            T[pi+1][pj] += T[pi][pj]
            T[pi][pj] = 0
            pi+=1
            justcomb=True
    return T

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
    
def isuppossible(vec, n):
    for i in range(n-1,0,-1):
        for j in range(0,n):
            if (vec[i][j]!=0 and vec[i-1][j]==0)or(vec[i][j]!=0  and vec[i][j]==vec[i-1][j]):
                return 1

    return 0
def isdownpossible(vec, n):
    for i in range(n-2,-1,-1):
        for j in range(0,n):
            if (vec[i][j]!=0 and vec[i+1][j]==0)or(vec[i][j]!=0 and vec[i][j]==vec[i+1][j]):
                return 1

    return 0
def isleftpossible(vec, n):
    for i in range(0,n):
       for j in range(n-1,0,-1):
            if (vec[i][j]!=0 and vec[i][j-1]==0)or(vec[i][j]!=0 and vec[i][j]==vec[i][j-1]):
                return 1
    return 0
def isrightpossible(vec, n):
    for i in range(0,n):
       for j in range(n-2,-1,-1):
            if (vec[i][j]!=0 and vec[i][j+1]==0)or(vec[i][j]!=0  and vec[i][j]==vec[i][j+1]):
                return 1
    return 0 
def leftmoment( vec, n):
    for i in range(0,n):
        m=-1
        for j in range(0,n):
            if(vec[i][j]!=0):
                if(m==-1):
                    temp1=vec[i][j]
                    vec[i][j]=0
                    m=m+1
                    vec[i][m]=temp1
                else:
                    if(j!=m and vec[i][m]==vec[i][j]):
                        vec[i][j]=0
                        vec[i][m]=vec[i][m]*2
                    else:
                        temp=vec[i][j]
                        vec[i][j]=0
                        m=m+1
                        vec[i][m]=temp
    
    return vec
    
def rightmoment( vec, n):
    for i in range(0,n):
        m=n
        for j in range(n-1,-1,-1):
            if(vec[i][j]!=0):
                if(m==n):
                    temp1=vec[i][j]
                    vec[i][j]=0
                    m=m-1
                    vec[i][m]=temp1
                else:
                    if(j!=m and vec[i][m]==vec[i][j]):
                        vec[i][j]=0
                        vec[i][m]=vec[i][m]*2
                    else:
                        temp=vec[i][j]
                        vec[i][j]=0
                        m=m-1
                        vec[i][m]=temp
    
    return vec

def downmoment( vec, n):
    for j in range(0,n):
        m=n
        for i in range(n-1,-1,-1):
            if(vec[i][j]!=0):
                if(m==n):
                    temp1=vec[i][j]
                    vec[i][j]=0
                    m=m-1
                    vec[m][j]=temp1
                else:
                    if(i!=m and vec[m][j]==vec[i][j]):
                        vec[i][j]=0
                        vec[m][j]=vec[m][j]*2
                    else:
                        temp=vec[i][j]
                        vec[i][j]=0
                        m=m-1
                        vec[m][j]=temp
    
    return vec
def upmoment( vec, n):
    for j in range(0,n):
        m=-1
        for i in range(0,n):
            if(vec[i][j]!=0):
                if(m==-1):
                    temp1=vec[i][j]
                    vec[i][j]=0
                    m=m+1
                    vec[m][j]=temp1
                else:
                    if(i!=m and vec[m][j]==vec[i][j]):
                        vec[i][j]=0
                        vec[m][j]=vec[m][j]*2
                    else:
                        temp=vec[i][j]
                        vec[i][j]=0
                        m=m+1
                        vec[m][j]=temp
    
    return vec    


def status(vec,n):
        temp=0
        n1=int(math.ceil(n/2))
        for m in range(0,n1):
            a=1
            for i in range(0,n):
                for j in range(0,n):
                    if((i==m or i==n-1-m  or j==m or j==n-1-m) and vec[i][j]!=0):
                        a=a*vec[i][j]
            temp=temp-(m*m*a)
        return temp

def dfs(vecty, depth, n):
    flag1=isuppossible(vecty,n)
    flag2=isdownpossible(vecty,n)
    flag3=isleftpossible(vecty,n)
    flag4=isrightpossible(vecty,n)
    if((not flag1) and (not flag2) and (not flag3 )and  (not flag4)):
        return None,-630000000
    
    if(depth==3):
        return None,0
    temp1=0
    temp2=0
    temp3=0
    temp4=0
    u=0.00001
    l=00.00001
    d=00.00001
    r=00.00001
    if(flag1):
        vec=[[vecty[0][0],vecty[0][1],vecty[0][2],vecty[0][3]],[vecty[0][0],vecty[1][1],vecty[1][2],vecty[1][3]],
        [vecty[2][0],vecty[2][1],vecty[2][2],vecty[2][3]],[vecty[3][0],vecty[3][1],vecty[3][2],vecty[3][3]]]
        vectemp=upmoment(vec,n)
        for i in range(0,n):
            for j in range(0,n):
                if(vectemp[i][j]==0):
                    vectemp[i][j]=2
                    tas,second=dfs(vectemp,depth+1,n)
                    a=status(vectemp,n)+second
                    vectemp[i][j]=4
                    b=status(vectemp,n)+second
                    temp1=temp1+a+b
                    u=u+2
                    vectemp[i][j]=0

    if(flag2):
        vec=[[vecty[0][0],vecty[0][1],vecty[0][2],vecty[0][3]],[vecty[0][0],vecty[1][1],vecty[1][2],vecty[1][3]],
        [vecty[2][0],vecty[2][1],vecty[2][2],vecty[2][3]],[vecty[3][0],vecty[3][1],vecty[3][2],vecty[3][3]]]
        vectemp=downmoment(vec,n)
        for i in range(0,n):
            for j in range(0,n):
                if(vectemp[i][j]==0):
                    vectemp[i][j]=2
                    tas,second=dfs(vectemp,depth+1,n)
                    a=status(vectemp,n)+second
                    vectemp[i][j]=4
                    tas,second=dfs(vectemp,depth+1,n)
                    b=status(vectemp,n)+second
                    temp2=temp2+a+b
                    d=d+2
                    vectemp[i][j]=0
            

    
    
    if(flag3):
        vec=[[vecty[0][0],vecty[0][1],vecty[0][2],vecty[0][3]],[vecty[0][0],vecty[1][1],vecty[1][2],vecty[1][3]],
        [vecty[2][0],vecty[2][1],vecty[2][2],vecty[2][3]],[vecty[3][0],vecty[3][1],vecty[3][2],vecty[3][3]]]
        vectemp=leftmoment(vec,n)
        for i in range(0,n):
            for j in range(0,n):
                if(vectemp[i][j]==0):
                        vectemp[i][j]=2
                        tas,second=dfs(vectemp,depth+1,n)
                        a=status(vectemp,n)+second
                        vectemp[i][j]=4
                        tas,second=dfs(vectemp,depth+1,n)
                        b=status(vectemp,n)+second
                        temp3=temp3+a+b
                        l=l+2

                        vectemp[i][j]=0
            
   
    if(flag4):
        vec=[[vecty[0][0],vecty[0][1],vecty[0][2],vecty[0][3]],[vecty[0][0],vecty[1][1],vecty[1][2],vecty[1][3]],
        [vecty[2][0],vecty[2][1],vecty[2][2],vecty[2][3]],[vecty[3][0],vecty[3][1],vecty[3][2],vecty[3][3]]]
        vectemp=rightmoment(vec,n)
        for i in range(0,n):
                for j in range(0,n):
                    if(vectemp[i][j]==0):
                        vectemp[i][j]=2
                        tas,second=dfs(vectemp,depth+1,n)
                        a=status(vectemp,n)+second
                        vectemp[i][j]=4
                        tas,second=dfs(vectemp,depth+1,n)
                        b=status(vectemp,n)+second
                        temp4=temp4+a+b
                        r=r+2

                        vectemp[i][j]=0
            
    if((not temp1==0) and (temp1/u>=temp2/d or temp2==0) and (temp1/u>=temp3/l or temp3/l==0) and (temp1/u>=temp4/r or temp4/r==0)):
        return 'w',temp1
    
    if((not temp2==0) and (temp2/d>=temp1/u or temp1==0) and (temp2/d>=temp3/l or temp3/l==0) and (temp2/d>=temp4/r or temp4/r==0) and temp2/d!=0):
        return 's',temp2
    
    if((not temp4==0) and (temp4/r>=temp2/d or temp2==0) and (temp4/r>=temp3/l or temp3/l==0) and (temp4/r>=temp1/u or temp1==0) and temp4/r!=0):
        return 'd',temp4
    if((not temp3==0) and (temp3/l>=temp2/d or temp2==0) and (temp3/l>=temp1/u or temp1==0) and (temp3/l>=temp4/r or temp4/r==0) and temp3!=0):
        return 'a',temp3
        
    
def terminate():
    pygame.quit()
    sys.exit()

main()
