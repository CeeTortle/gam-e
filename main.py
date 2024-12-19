
# Example file showing a basic pygame "game loop"
import pygame
import pygame.freetype
import sys
import math
import random
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1000, 900))
clock = pygame.time.Clock()
running = True
pygame.mouse.set_cursor(*pygame.cursors.broken_x)
screenW=screen.get_width()
screenH=screen.get_height()
bullets=[]
bullets.append([])
bullets.append([])
zombList=[]
zombList.append([])
zombList.append([])
def debugKey(keyList):
    for i in range(len(keyList)):
        if keyList[i]==True:
            print("True")
            print(i)
def playerMove(key):
    global playerCoords,plMvSpd
    if key[119]:#w
        playerCoords[1]=playerCoords[1]-plMvSpd
    if key[97]:#a
        playerCoords[0]=playerCoords[0]-plMvSpd
    if key[115]:#s  
        playerCoords[1]=playerCoords[1]+plMvSpd
    if key[100]:#d
        playerCoords[0]=playerCoords[0]+plMvSpd
def bulletHit(x,y,r):
    out=False
    for i in range(len(bullets[1])):
        bulletAng=bullets[0][i-1]
        bulletTime=bullets[1][i-1]
        bulletX=(math.cos(bulletAng)*bulletTime)+playerCoords[0]
        bulletY=(math.sin(bulletAng)*bulletTime)+playerCoords[1]
        dis=math.sqrt(((x-bulletX)*(x-bulletX))+((y-bulletY)*(y-bulletY)))
        if dis<r:
            out= True
            bullets[0].pop(i-1)
            bullets[1].pop(i-1)
    return out
def drawZombies(zombList):
    global playerCoords,chrSCords,zombMvSpd
    for i in range(len(zombList[0])):
        chng=1
        if bulletHit(zombList[0][i-chng],zombList[1][i-chng],40):
            zombList[0].pop(i-1)
            zombList[1].pop(i-1)
            print("hit",pygame.time.get_ticks())
            i=i-1
        else:
            zombAng=math.atan2(playerCoords[1]-zombList[1][i-chng],playerCoords[0]-zombList[0][i-chng])
            zombXMove=(zombList[0][i-chng])+math.cos(zombAng)*zombMvSpd
            zombYMove=(zombList[1][i-chng])+math.sin(zombAng)*zombMvSpd
            XValid=True
            YValid=True
            for l in range(len(zombList[0])):
                if not l==i:
                    checkX=zombList[0][l-1]
                    checkY=zombList[1][l-1]
                    trueDis=math.sqrt(((checkX-zombXMove)*(checkX-zombXMove))+((checkY-zombYMove)*(checkY-zombYMove)))
                    angToZomb=math.atan2(zombYMove-checkY,zombXMove-checkX)
                    if trueDis<80:
                        zombXMove=zombXMove+math.cos(angToZomb)*(80/trueDis)
                        zombYMove=zombYMove+math.sin(angToZomb)*(80/trueDis)
                        
            if XValid:
                zombList[0][i-chng]=zombXMove
            if YValid:
                zombList[1][i-chng]=zombYMove
            zmsX=zombList[0][i-chng]-playerCoords[0]+chrSCords[0]
            zmsY=zombList[1][i-chng]-playerCoords[1]+chrSCords[1]
            
            pygame.draw.circle(screen,"darkgreen",(zmsX,zmsY),40)
def spawnZombie(zombList,zombX,zombY):
    zombList[0].append(zombX)
    zombList[1].append(zombY)
spawnZombie(zombList,0,-500)
spawnZombie(zombList,500,500)
playerCoords=[0,0]
plMvSpd=3
zombMvSpd=2
while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")
    
    #DRAW CHAR AND BULLETS
    mousePos=pygame.mouse.get_pos()
    mousePos=[mousePos[0]-screenW/2,mousePos[1]-screenH/2]
    chrSCords=[(screenW/2)-mousePos[0]/10,(screenH/2)-mousePos[1]/10]
    mouseAngFrmChr=math.atan2(mousePos[1]+(mousePos[0]/10),mousePos[0]-(mousePos[1]/10))-0.1

    if pygame.mouse.get_pressed()[0]:
       x=x+1
       if x>1 or x==0:
            bullets[0].append(mouseAngFrmChr)
            bullets[1].append(0)
            x=0
    else:
        x=-1
    key=pygame.key.get_pressed()
    #w119,a97,s115,d100w
    playerMove(key)
    for i in range(len(bullets[1])):
        bulletTime=bullets[1][i-1]
        bulletAng=bullets[0][i-1]
        bullets[1][i-1]=bulletTime+30
        pygame.draw.circle(screen,"red",(chrSCords[0]+math.cos(bulletAng)*bulletTime,chrSCords[1]+math.sin(bulletAng)*bulletTime),5)
    #DRAW BACKGROUND
    for i in range(6):
        offset=(screenW/6)+60
        pygame.draw.line(screen,"black",(chrSCords[0]-60-screenW/2+offset*i+(-playerCoords[0])%offset,0),(chrSCords[0]-60-screenW/2+offset*i+(-playerCoords[0])%offset,screenH))
    for i in range(6):
        offset=(screenW/6)+60
        pygame.draw.line(screen,"black",(0,chrSCords[1]-60-screenH/2+offset*i+(-playerCoords[1])%offset),(screenW,chrSCords[1]-60-screenH/2+offset*i+(-playerCoords[1])%offset))
    #DRAW AND MAKE ZOMBIES
    drawZombies(zombList)
    if pygame.time.get_ticks()%1==0:
        spawnZombie(zombList,random.randint(-1000,1000),random.randint(-1000,1000))
    clock.tick(60)
    pygame.draw.line(screen,"black",chrSCords,(int(chrSCords[0]+math.cos(mouseAngFrmChr)*70),int(chrSCords[1]+math.sin(mouseAngFrmChr)*70)))
    pygame.draw.circle(screen,"darkblue",chrSCords,40)
    pygame.display.flip()

pygame.quit()
