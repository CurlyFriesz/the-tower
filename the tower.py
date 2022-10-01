from pygame import *
from math import *
init()
print(font.get_fonts())
def dist(x1,y1,x2,y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)

def move(mp, wall):
    keys = key.get_pressed()
    if keys[K_w] and hitObstacle(playerRect[x], playerRect[y]-3, wall)==True:
        mp[1] += 3
        player[ROW]=3
    elif keys[K_s] and hitObstacle(playerRect[x], playerRect[y]+3, wall)==True:
        mp[1] -= 3
        player[ROW]=0
    elif keys[K_a] and hitObstacle(playerRect[x]-3, playerRect[y], wall)==True:
        mp[0] += 3
        player[ROW]=1
    elif keys[K_d] and hitObstacle(playerRect[x]+3, playerRect[y], wall)==True:
        mp[0] -= 3
        player[ROW]=2
    else:
        player[COL]=player[COL]-0.07
        
    player[COL]=player[COL]+0.07

    if player[COL]>=len(pics[ROW]):
            player[COL]=1

def moveEnemy(enemy, speed, player):
    for e in enemy:
        if dist(player[x]-mapp[0], player[y]-mapp[1], e[x], e[y]) <= r1+r2:
            if e[x] < player[x]-mapp[0]:
                e[x] += speed
            if e[x] > player[x]-mapp[0]:
                e[x] -= speed
            if e[y] < player[y]-mapp[1]:
                e[y] += speed
            if e[y] > player[y]-mapp[1]:
                e[y] -= speed

def makeRects(mywalls):
    myRects = []
    y = 0
    for row in range(len(mywalls)):
        for col in range(len(mywalls[row])):
            if mywalls[row][col]==1:
                myRects.append(Rect(col * 32 + mapp[0] + 210, row * 32 - mapp[1] - 780, 32, 32))
            if mywalls[row][col]==2 or mywalls[row][col]==3 or mywalls[row][col]==4:             
                screen.blit(floor, (col * 32 + mapp[0] + 210, row * 32 + mapp[1] - 780))
    return myRects

def drawScene(screen,player,p,walls,piclist,lev,enemy,targ):
    screen.fill(0)
    row = p[ROW]
    col = int(p[COL])
    pic = piclist[row][col]
    for w in walls:
        w=w.move(mapp[0],mapp[1])
        screen.blit(wall, w)

    makeRects(lev)
    for e in enemy:
        e=e.move(mapp[0],mapp[1])
        screen.blit(slime,(e[x],e[y]))
    if score < targ:
        screen.blit(portal, (608+mapp[0]+210,32+mapp[1]-780))
    else:
        screen.blit(port1, (608+mapp[0]+210,32+mapp[1]-780))
    health()
    screen.blit(heal, (0,550))
    scores = pix.render(str(score),True,(255,255,255))
    screen.blit(scores, (10,10))
    screen.blit(pic,(player[x],player[y]))
    display.flip()

def hitObstacle(x,y,walls):
    playerRect = Rect(x,y,32,32)

    for w in walls:
        w=w.move(mapp[0],mapp[1])
        if playerRect.colliderect(w):
            return False #there is collision
    return True #there is no collision

def attack(targ,hp,mb,direc,p):
    global score
    r = (999,999,0,0)
    
    if mb[0]==1:
        if direc[ROW] == 3: #up
            r = Rect(p[x]-20,p[y]-40,66,40)
##            draw.rect(screen,BLUE,r)
            screen.blit(slashup, (p[x]-20,p[y]-40))
            slashFx.play()
        elif direc[ROW] == 0: #down
            r = Rect(p[x]-20,p[y]+33,66,40)
##            draw.rect(screen,BLUE,r)
            screen.blit(slashdown, (p[x]-20, p[y]+33))
            slashFx.play()
        elif direc[ROW] == 1: #left
            r = Rect(p[x]-40,p[y],40,33)
##            draw.rect(screen,BLUE,r)
            screen.blit(slashleft, (p[x]-40,p[y]))
            slashFx.play()
        elif direc[ROW] == 2: #right
            r = Rect(p[x]+26,p[y],40,33)
            screen.blit(slashright, (p[x]+20,p[y]))
##            draw.rect(screen,BLUE,r)
            slashFx.play()
        r = r.move(-mapp[0],-mapp[1])  #this should be done only once
        for t in targ:
            #print(mapp,r,t)
            if r.colliderect(t):
                hp -= 5
                print(hp)
                if hp <= 0:
                    if t in targ:
                        targ.remove(t)
                    hp = 25
                    score += 200
                break
    return hp

def hitPlayer(p,enemy,hp):
    p = p.move(-mapp[0],-mapp[1])
    for e in enemy:
        if e.colliderect(p):
            hp -= 2
            print("p:", hp)
            if hp <= 0:
                action = "game over"
    return hp

def health():
    for h in range(php):
        draw.rect(screen, RED, (25+h*10,570,10,20))

def levelCompleted(targ):
    pr = portalRect.move(mapp[0],mapp[1])
    if score == targ and playerRect.colliderect(pr):
        print("level completed")
        return True

def gameOver(hp):
    if hp <= 0:
        return True

def menu(action):
    
    while action == "menu":
        for evt in event.get():
            if evt.type==QUIT:
                action = ""
        screen.fill(0)
        screen.blit(menuRe, (0,0))
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
##        for b in buttons:
##            draw.rect(screen,GREEN,b)
        
        screen.blit(playImg, (270, 300))
        screen.blit(instImg, (270, 355))
        screen.blit(credImg, (270, 410))
        screen.blit(title, (40, 0))
        
        if mb[0]==1:
            if buttons[0].collidepoint(mx,my):
                clickFx.play()
                levels("levels")
            if buttons[1].collidepoint(mx,my):
                clickFx.play()
                tutorial("tutor")
            if buttons[2].collidepoint(mx,my):
                clickFx.play()
                credits("cred")


       
        display.flip()
        clock.tick(60)

def levels(action):
    global mapp
    global go
    while action == "levels":
        php = 30
        click = False
        for evt in event.get():
            if evt.type==QUIT:
                action = "menu"
            if evt.type==MOUSEBUTTONDOWN:
                click = True
        screen.fill((107,107,107))   
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        
##        for l in level:
##            draw.rect(screen, GREEN, l)
        screen.blit(lev1Img, (10,10))
        screen.blit(lev2Img, (320, 10))

       
        if click:
            if level[0].collidepoint(mx,my):
                clickFx.play()
                mapp=[0,0]
                level1("lev1")
            if level[1].collidepoint(mx,my):
                clickFx.play()
                mapp=[0,0]
                level2("lev2")
       
        display.flip()

def level1(action):
    global delay
    global delay2
    global hp
    global php
    global mapp
    global go
    while action == "lev1":
        click = False
        for evt in event.get():
            if evt.type==QUIT:
                action = "end"
            if evt.type==MOUSEBUTTONDOWN:
                click = True
                
        screen.fill(0)  
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
##        if mb[0]==1:
##            click = True
        move(mapp, walls1)
        moveEnemy(enemies, 1, playerRect)
        drawScene(screen,playerRect,player,walls1,pics,lev1,enemies,1400)

        if delay < 30:
            delay+=1

        if click and delay == 30:
            hp=attack(enemies,hp,mb,player,playerRect)
            delay = 0

        if delay2 < 35:
            delay2 += 1

        if delay2 == 35:
            php = hitPlayer(playerRect, enemies, php)
            delay2 = 0

        if levelCompleted(1400) == True:
            action = "level"

        if php <= 0:
            php = 30
            screen.blit(GO, (200, 120))
            display.flip()
            time.wait(3000)

            return "menu"
                    
        display.flip()
        clock.tick(60)

def level2(action):
    global delay
    global delay2
    global hp
    global php
    global mapp
    global mapp
    
    while action == "lev2":
        click=False
        for evt in event.get():
            if evt.type==QUIT:
                action = levels
            if evt.type==MOUSEBUTTONDOWN:
                click = True
        screen.fill(0)      
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
##        if mb[0]==1:
##            click = True
        move(mapp, walls2)
        moveEnemy(enemies2, 1, playerRect)
        drawScene(screen,playerRect,player,walls2,pics,lev2,enemies2,1400)



        print("delay=",delay)
        if delay < 30:
            delay+=1

        if click and delay == 30:
            hp = attack(enemies2,hp,mb,player,playerRect)
            delay = 0

        if delay2 < 35:
            delay2 += 1

        if delay2 == 35:
            php = hitPlayer(playerRect, enemies2, php)
            delay2 = 0

        if levelCompleted(3000) == True:
            action = "level"

        if php <= 0:
            php = 30
            screen.blit(GO, (200, 120))
            display.flip()
            time.wait(3000)

            return "menu"
            
        print(score)
        display.flip()
        clock.tick(60)


def credits(action):
    while action == "cred":
        for evt in event.get():
            if evt.type==QUIT:
                action = "menu"
        screen.fill(GREY)   
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        
        screen.blit(cred, (0,0))  
       
        display.flip()
        clock.tick(60)

def tutorial(action):
    while action == "tutor":
        for evt in event.get():
            if evt.type==QUIT:
                action = "menu"
        screen.fill(YELLOW)   
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        screen.blit(tutor, (0,0))
       
        display.flip()
        clock.tick(60)

def gameOver(action):
    while action == "game over":
        click = False
        for evt in event.get():
            if evt.type==QUIT:
                action = "menu"
            if evt.type==MOUSEBUTTONDOWN:
                click = True
        screen.fill(0)   
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        screen.blit(GO, (200, 20))

        r = Rect(200, 300, 400, 100)
##        draw.rect(screen, GREEN, r)
        screen.blit(ret, (200, 300))

        if click == True and r.collidepoint(mx,my):
            menu("menu")
        
        display.flip()
        clock.tick(60)
          

def addPics(name, start, end):
    mypics = []
    for i in range(start,end+1):
        mypics.append(image.load("images/player/%s%00d.png" %(name, i)))
    return mypics

pics=[]
pics.append(addPics("player",1,3))
pics.append(addPics("player",4,6))
pics.append(addPics("player",7,9))
pics.append(addPics("player",10,12))

rate = 0

width,height=800,600
screen=display.set_mode((width,height))
display.set_caption("M.o.T")
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)

playerRect=Rect(400,300,24,33)

x = 0
y = 1
ROW = 2
COL = 3

r1 = 100
r2 = 32

player = [400, 300, 0, 0]

slashFx = mixer.Sound("music/slash.wav")
clickFx = mixer.Sound("music/click.wav")
bgm = mixer.Sound("music/bgm.wav")

pix = font.Font("fonts/pixel.ttf",30)

menuBg = image.load("images/menu.png")
menuRe = transform.scale(menuBg, (800,600))
playImg = image.load("images/button0.png")
playImg = transform.scale(playImg, (250,40))
inst = image.load("images/button1.png")
instImg = transform.scale(inst, (250, 40))
cred = image.load("images/button2.png")
credImg = transform.scale(cred, (250,40))
lev1Img = image.load("images/level1.png")
lev1Img = transform.scale(lev1Img, (300, 400))
lev2Img = image.load("images/level2.png")
lev2Img = transform.scale(lev2Img, (300, 400))
wall = image.load("images/wall.png")
wall = transform.scale(wall, (32, 32))
floor = image.load("images/floor.png")
floor = transform.scale(floor, (32,32))
title = image.load("images/title.png")
portal = image.load("images/portal.png")
portal = transform.scale(portal, (64,64))
port1 = image.load("images/portal/portal1.gif")
port1 = transform.scale(port1, (64,64))
port2 = image.load("images/portal/portal2.gif")
port2 = transform.scale(port2, (64,64))
port3 = image.load("images/portal/portal3.gif")
port3 = transform.scale(port3, (64,64))
port4 = image.load("images/portal/portal4.gif")
port4 = transform.scale(port4, (64,64))
slime = image.load("images/slime.png")
slime = transform.scale(slime, (32,32))
slash = image.load("images/slash.png")
slashleft = transform.scale(slash, (66,40))
slashright = transform.flip(slashleft, True, True)
slash2 = image.load("images/slash2.png")
slashup = transform.scale(slash2, (66,40))
slashdown = transform.flip(slashup, True, True)
GO = image.load("images/game over.jpg")
GO = transform.scale(GO, (400, 300))
cred = image.load("images/cred.png")
tutor = image.load("images/tutor.png")
tutor = transform.scale(tutor, (800,600))
ret = image.load("images/return.png")
heal = image.load("images/health.png")
heal = transform.scale(heal, (50,50))
heal = transform.flip(heal, True, False)

lev1 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,4,4,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,4,4,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,2,2,2,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [1,2,2,3,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,3,2,2,2,2,2,1,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [1,2,2,2,2,2,2,2,3,2,2,2,2,2,2,2,2,2,2,2,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,2,2,1,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,2,2,2,2,2,1,0,0],
        [1,2,2,2,2,2,2,3,2,2,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,3,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [1,1,1,1,2,2,2,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,2,2,2,2,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

lev2 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,3,2,2,2,2,2,2,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,3,2,2,2,2,2,3,2,1,1,1,1,2,2,2,2,2,2,2,2,3,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,3,2,2,2,2,2,2,2,2,2,2,2,2,3,2,2,2,2,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,3,2,2,2,2,2,2,2,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,2,2,2,2,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,3,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2,3,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,2,2,2,2,2,2,2,2,2,1,0,0,1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

buttons=[Rect(270,300+y*55,250,40) for y in range(3)]
butImg = [playImg]
level = [Rect(10+x*310,10,300,400) for x in range(2)]

clock = time.Clock()
running=True
mapp = [0,0]
walls1 = makeRects(lev1)
walls2 = makeRects(lev2)
enemies = [Rect(128+mapp[0]+210,512+mapp[1]-780,32,32),Rect(224+mapp[0]+210,704+mapp[1]-780,32,32), Rect(256+mapp[0]+210,576+mapp[1]-780,32,32), Rect(608+mapp[0]+210,736+mapp[1]-780,32,32),Rect(640+mapp[0]+210,576+mapp[1]-780,32,32),Rect(1056+mapp[0]+210,672+mapp[1]-780,32,32),Rect(1056+mapp[0]+210,512+mapp[1]-780,32,32)]
enemies2 = [Rect(640+mapp[0]+210,1152+mapp[1]-780,32,32),Rect(704+mapp[0]+210,960+mapp[1]-780,32,32),Rect(640+mapp[0]+210,672+mapp[1]-780,32,32),Rect(544+mapp[0]+210,544+mapp[1]-780,32,32), Rect(736+mapp[0]+210,544+mapp[1]-780,32,32),Rect(960+mapp[0]+210,736+mapp[1]-780,32,32),Rect(992+mapp[0]+210,512+mapp[1]-780,32,32),Rect(1184+mapp[0]+210,544+mapp[1]-780,32,32)]
delay = 0
delay2 = 0
hp = 25
php = 30
portalRect = Rect(608+mapp[0]+210,32+mapp[1]-780,64,64)
score = 0 

go=False

##Main program
bgm.play()
menu("menu")
print(mapp)
quit()
