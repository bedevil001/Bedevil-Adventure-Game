#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, random, time, os, math, text
from datetime import datetime
import entities as e
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(24)
pygame.display.set_caption('MIGO ADVENTURE')
WINDOWWIDTH = 800
WINDOWHEIGHT = 500
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
display = pygame.Surface((400,250))
# Text ------------------------------------------------------- #
def get_text_width(text,spacing):
    global font_dat
    width = 0
    for char in text:
        if char in font_dat:
            width += font_dat[char][0] + spacing
    return width

global font_dat
font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],';':[1]}
font_0 = text.generate_font('data/font/small_font.png',font_dat,5,8,(248,248,248))
font_1 = text.generate_font('data/font/small_font.png',font_dat,5,8,(16,30,41))
# Images ----------------------------------------------------- #
def load_img(path):
    img = pygame.image.load('data/images/' + path + '.png').convert()
    img.set_colorkey((255,255,255))
    return img

island_0 = load_img('island_0')
island_1 = load_img('island_1')
island_2 = load_img('island_2')
island_0_back = load_img('island_0_back')
island_1_back = load_img('island_1_back')

dirt_img = load_img('dirt')
dirt_2_img = load_img('dirt_2')

gun_mode_back = load_img('gun_mode')
plant_mode_img = load_img('plant_mode')
kill_mode_img = load_img('kill_mode')
bullets_back_img = load_img('bullets_back')

gun_barrel_img = load_img('gun_barrel')
target_img = load_img('target')
target_2_img = load_img('target_2')

player_img = load_img('player/stand_0')
player_walking_anim = e.animation_sequence([[0,4],[1,4],[2,4],[3,4],[4,4],[5,4]],'data/images/player/walking_')
jump_anim = e.animation_sequence([[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3]],'data/images/jump_particles/jump_')

bullet_img = load_img('bullet_img')
bullet_gui_img = load_img('bullet_gui_img')

health_bar = load_img('health_bar')

slime_images = [load_img('slime/slime_0'),load_img('slime/slime_1'),load_img('slime/slime_2')]

slime_ball = load_img('slime_ball')

smoke_img = load_img('smoke')

cloud_images = [load_img('cloud_0'),load_img('cloud_1')]

tutorial_img = load_img('tutorial')
# Audio ------------------------------------------------------ #
ambience_sfx = pygame.mixer.Sound('data/sfx/ambience.wav')
ambience_sfx.set_volume(1)
grass_sfx = [pygame.mixer.Sound('data/sfx/grass_0.wav'),pygame.mixer.Sound('data/sfx/grass_1.wav'),pygame.mixer.Sound('data/sfx/grass_2.wav')]
for sound in grass_sfx:
    sound.set_volume(0.2)
pew_sfx = pygame.mixer.Sound('data/sfx/pew.wav')
pew_sfx.set_volume(0.3)
squish_sfx = pygame.mixer.Sound('data/sfx/squish.wav')
squish_sfx.set_volume(0.4)
quiet_squish_sfx = pygame.mixer.Sound('data/sfx/squish.wav')
quiet_squish_sfx.set_volume(0.15)
# Colors ----------------------------------------------------- #
#SKY = (146,244,255)
SKY = (100,223,254)
# Functions -------------------------------------------------- #
def blit_center(surf,surf2,pos):
    x = int(surf2.get_width()/2)
    y = int(surf2.get_height()/2)
    surf.blit(surf2,(pos[0]-x,pos[1]-y))

def normalize(num,amount):
    if num > amount:
        num -= amount
    elif num < -amount:
        num += amount
    else:
        num = 0
    return num

def minimum(num,amount):
    if (num < amount) and (num > 0):
        num = 0
    elif (num > -amount) and (num < 0):
        num = 0
    return num

def maximum(num,amount):
    if num > amount:
        num = amount
    if num < -amount:
        num = -amount
    return num

def points2deg(point1,point2):
    try:
        deg = (point2[0]-point1[0])/(point2[1]-point1[1])
        angle = math.degrees(math.atan(deg))
    except ZeroDivisionError:
        deg = 0
        if point2[0] < point1[0]:
            angle = 90
        else:
            angle = -90
    if point2[1] > point1[1]:
        angle += 180
    if angle <= 0:
        angle += 360
    return angle

def rate2deg(x,y):
    try:
        deg = x/y
        angle = math.degrees(math.atan(deg))
    except ZeroDivisionError:
        deg = 0
        if x < 0:
            angle = 90
        else:
            angle = -90
    if y > 0:
        angle += 180
    if angle <= 0:
        angle += 360
    return angle
# Menu ------------------------------------------------------- #
menu = ['العب','شرح','خروج']
cursor = 0
in_menu = True
while in_menu:
    display.fill((0,0,0))
    text.show_text('مغامرات ميجو',2,2,1,99999,font_0,display)
    text.show_text('محمد مجدي شيبوب',2,242,1,99999,font_0,display)
    y = 0
    for option in menu:
        cursor_text = ''
        if cursor == y:
            cursor_text = '=> '
        text.show_text(cursor_text + option,2,42+y*12,1,99999,font_0,display)
        y += 1
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_UP:
                cursor -= 1
                if cursor < 0:
                    cursor = len(menu)-1
            if event.key == K_DOWN:
                cursor += 1
                if cursor >= len(menu):
                    cursor = 0
            if (event.key == K_RETURN) or (event.key == K_x):
                if menu[cursor] == 'العب':
                    in_menu = False
                if menu[cursor] == 'شرح':
                    tutorial = True
                    while tutorial:
                        display.fill((0,0,0))
                        display.blit(tutorial_img,(0,0))
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == KEYDOWN:
                                if event.key == K_ESCAPE:
                                    pygame.quit()
                                    sys.exit()
                                if event.key == K_x:
                                    tutorial = False
                        screen.blit(pygame.transform.scale(display,(WINDOWWIDTH,WINDOWHEIGHT)),(0,0))
                        pygame.display.update()
                        mainClock.tick(60)
                if menu[cursor] == 'خروج':
                    pygame.quit()
                    sys.exit()
    screen.blit(pygame.transform.scale(display,(WINDOWWIDTH,WINDOWHEIGHT)),(0,0))
    pygame.display.update()
    mainClock.tick(60)
# Time ------------------------------------------------------- #
def ms():
    return int(round(time.time() * 1000))

def get_ms():
    global start_time
    return int(round(time.time() * 1000)) - start_time

global start_time
start_time = ms()
last_frames = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
last_frame = 0
# Variables -------------------------------------------------- #
offset = [0,0]
true_offset = [0,0]
hitboxes = [pygame.Rect(12,103,92,21),pygame.Rect(12,124,70,60),pygame.Rect(127,173,147,100),pygame.Rect(304,90,82,100)]
player = e.entity(200,156,12,16)
player.set_image(player_img)
player_momentum = [0,0]
jumps = 2
jumps_max = 2
right = False
left = False
speed = 2.5
dirts = [[127,166,0],[153,166,0],[182,166,0],[195,166,0],[208,166,0],[221,166,0],
         [256,166,0],[328,82,0],[342,82,0],[373,82,0],[15,96,0],[28,96,0],[41,96,0],
         [54,96,0],[67,96,0],[80,96,0],[93,96,0],]
for dirt in dirts:
    dirt.append(300)
gun_mode = 'plant'
gun_angle = 0
gun_target_angle = 0
gun_turn_rate = 6
bullets = []
firing = False
fire_timer = 0
bullet_speed = 5
ammo = 200
slimes = []
gun_dmg = 50
game_timer = 0
slime_rate = 240
player_flash_timer = 0
target_pos = None
show_fps = False
target_timer = 0
slime_balls = []
alerts = []
jump_particles = []
particles = []
air_time = 0
clouds = []
for i in range(random.randint(12,20)):
    # scroll multiplier, x, y, cloud_type
    clouds.append([random.randint(10,50)/100,random.randint(0,500)-50,random.randint(0,350)-50,random.randint(0,1)])
# Loop ------------------------------------------------------- #
ambience_sfx.play(-1)
pygame.mixer.music.load('data/music/new_main.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
while True:
    # Background --------------------------------------------- #
    display.fill(SKY)
    MX,MY = pygame.mouse.get_pos()
    game_timer += 1
    if game_timer/60 > 15:
        slime_rate = 200
    if game_timer/60 > 30:
        slime_rate = 170
    if game_timer/60 > 45:
        slime_rate = 150
    if game_timer/60 > 60:
        slime_rate = 130
    if game_timer/60 > 75:
        slime_rate = 100
    if game_timer/60 > 100:
        slime_rate = 80
    if game_timer/60 > 125:
        slime_rate = 70
    if game_timer/60 > 150:
        slime_rate = 60
    if game_timer/60 > 175:
        slime_rate = 50
    if game_timer/60 > 200:
        slime_rate = 40
    # Clouds ------------------------------------------------- #
    for cloud in clouds:
        display.blit(cloud_images[cloud[3]],(cloud[1]-offset[0]*cloud[0],cloud[2]-offset[1]*cloud[0]))
    # Island Decor ------------------------------------------- #
    display.blit(island_0_back,(300-offset[0],80-offset[1]))
    display.blit(island_1_back,(120-offset[0],120-offset[1]))
    # Dirtses ------------------------------------------------ #
    lost = True
    for dirt in dirts:
        if dirt[0] != 'null':
            lost = False
            if dirt[2] == 900:
                for i in range(8):
                    slime_balls.append([dirt[0]+4,dirt[1]+4,random.randint(7,12),random.randint(0,360),random.randint(0,45),[random.randint(1,100)/50-1,random.randint(1,100)/200-0.75],'smoke'])
            if dirt[2] > 900:
                display.blit(dirt_2_img,(dirt[0]-offset[0],dirt[1]-offset[1]))
                dirtR = pygame.Rect(dirt[0]+2,dirt[1],6,8)
                if dirtR.colliderect(player.obj.rect):
                    if ammo < 200:
                        dirt[2] = 0
                        amount = random.randint(6,9)
                        if ammo+amount > 200:
                            amount = 200-ammo
                        ammo += amount
                        alerts.append(['+bullets',player.x+6,player.y-5,0])
            else:
                display.blit(dirt_img,(dirt[0]-offset[0],dirt[1]-offset[1]))
            if dirt[2] != 0:
                dirt[2] += 1
            if dirt[3] < 300:
                dirt[3] += 1
            if dirt[3] <= 0:
                dirt[0] = 'null'
                dirt[2] = 1
    # Jump Particles ----------------------------------------- #
    for particle in jump_particles:
        particle[0].animation = jump_anim
        particle[0].display(display,offset)
        particle[0].change_frame(1)
        particle[1] += 1
        if particle[1] == 19:
            jump_particles.remove(particle)
    # Gun ---------------------------------------------------- #
    if gun_mode == 'plant':
        nearest = 9999
        gun_target = None
        for dirt in dirts:
            if dirt[2] == 0:
                dis_x = abs(dirt[0]-player.x)
                dis_y = abs(dirt[1]-player.y)
                dis = math.hypot(dis_x,dis_y)
                if dis < nearest:
                    nearest = dis
                    gun_target = [dirt[0]+5,dirt[1]+5]
    if gun_mode == 'kill':
        nearest = 9999
        gun_target = None
        for slime in slimes:
            dis_x = abs(slime[0][0]-player.x)
            dis_y = abs(slime[0][1]-player.y)
            dis = math.hypot(dis_x,dis_y)
            if dis < nearest:
                nearest = dis
                gun_target = [slime[0][0]+2,slime[0][1]+8]

    if gun_target != None:
        gun_target_angle = points2deg((player.x+6,player.y+5),gun_target)
    elif player.flip == False:
        gun_target_angle = -90
    else:
        gun_target_angle = 90

    if gun_target_angle-gun_angle > 180:
        gun_target_angle -= 360
    if gun_angle-gun_target_angle > 180:
        gun_target_angle += 360

    if gun_angle < gun_target_angle-gun_turn_rate:
        gun_angle += gun_turn_rate
    elif gun_angle > gun_target_angle+gun_turn_rate:
        gun_angle -= gun_turn_rate
    else:
        gun_angle = gun_target_angle
    if gun_angle > 360:
        gun_angle -= 360
    elif gun_angle < 0:
        gun_angle += 360
    if gun_target == None:
        target_pos = None
    elif target_pos == None:
        target_pos = gun_target
    else:
        dif_x = gun_target[0]-target_pos[0]
        dif_y = gun_target[1]-target_pos[1]
        if math.hypot(dif_x,dif_y) < 20:
            target_pos = gun_target.copy()
        else:
            rate_x = dif_x/(abs(dif_x) + abs(dif_y))
            rate_y = dif_y/(abs(dif_x) + abs(dif_y))
            target_pos[0] += rate_x * 15
            target_pos[1] += rate_y * 15
    # Player ------------------------------------------------- #
    player_movement = player_momentum.copy()
    player_momentum[0] = normalize(player_momentum[0],0.2)
    player_momentum[1] += 0.25
    if player_momentum[1] >= 5:
        player_momentum[1] = 5
    if right == True:
        player_movement[0] += speed
    if left == True:
        player_movement[0] -= speed
    if player_movement[0] < 0:
        player.set_flip(True)
    elif player_movement[0] > 0:
        player.set_flip(False)
    collisions = player.move(player_movement,hitboxes)
    if collisions['bottom'] == True:
        if player_movement[0] != 0:
            if random.randint(1,20) == 1:
                random.choice(grass_sfx).play()
        jumps = jumps_max
        air_time = 0
    else:
        air_time += 1
    if air_time < 6:
        for i in range(random.randint(1,2)):
            if player_movement[0] > 0:
                particles.append([player.x+6,player.y+14,random.randint(0,20)/20-1,-random.randint(1,10)/7,random.randint(10,15),random.choice([(161,239,121),(63,199,120),(0,163,131)])])
            elif player_movement[0] < 0:
                particles.append([player.x+6,player.y+14,random.randint(0,20)/20,-random.randint(1,10)/7,random.randint(10,15),random.choice([(161,239,121),(63,199,120),(0,163,131)])])
    if player_movement[0] != 0:
        player.animation = player_walking_anim
        player.set_animation_tags(['loop'])
        player.change_frame(1)
    else:
        player.animation = None
    if player_flash_timer > 0:
        player_flash_timer -= 1
        if random.randint(1,2) == 1:
            blit_center(display,pygame.transform.rotate(gun_barrel_img,gun_angle),(player.x+6-offset[0],player.y+5-offset[1]))
            player.display(display,[offset[0],offset[1]+1])
    else:
        blit_center(display,pygame.transform.rotate(gun_barrel_img,gun_angle),(player.x+6-offset[0],player.y+5-offset[1]))
        player.display(display,[offset[0],offset[1]+1])
    if player.y > 310:
        player.set_pos(200,156)
        player_flash_timer = 90
    # Slimes ------------------------------------------------- #
    if random.randint(0,slime_rate) == 0:
        pos = random.choice([[-24,random.randint(0,50)],[random.randint(0,400),-40],[400,random.randint(0,50)]])
        pick = None
        for i in range(100):
            pick = random.randint(0,len(dirts)-1)
            if dirts[pick][0] != 'null':
                break
        if pick != None:
            health = random.randint(100,200)
            # position, momentum, rotation, health, target, squish_timer
            slimes.append([pos,[0,0],0,[health,health],pick,[0,'up']])
    for slime in slimes:
        if dirts[slime[4]][0] != 'null':
            if dirts[slime[4]][0] > slime[0][0]+4-8:
                slime[1][0] += 0.2
            if dirts[slime[4]][0] < slime[0][0]-4-8:
                slime[1][0] -= 0.2
        else:
            slime[1][0] -= 0.2
        slime[1][0] = maximum(slime[1][0],1.4)
        slime[1][1] += 0.25
        if slime[1][1] > 3:
            slime[1][1] = 3
        slime_entity = e.entity(slime[0][0],slime[0][1],16,16)
        slime_collisions = slime_entity.move(slime[1],hitboxes)
        if slime_collisions['bottom'] == True:
            if slime[1][1] > 1:
                quiet_squish_sfx.play()
            slime[1][1] = -slime[1][1]-3
        if dirts[slime[4]][0] != 'null':
            if slime_entity.obj.rect.colliderect(pygame.Rect(dirts[slime[4]][0],dirts[slime[4]][1],10,8)):
                slime[1] = [0,0]
                slime[2] = 0
                dirts[slime[4]][3] -= 2
            else:
                slime[2] = rate2deg(slime[1][0],slime[1][1])
        else:
            slime[2] = rate2deg(slime[1][0],slime[1][1])
        slime[0] = [slime_entity.x,slime_entity.y]
        slime_speed = abs(slime[1][0]) + abs(slime[1][1])
        if slime_speed < 4.5:
            slime_img = slime_images[0]
        else:
            slime_img = slime_images[2]
        if slime[5][1] == 'up':
            slime[5][0] += (100-slime[5][0])/10
            if slime[5][0] > 80:
                slime[5][1] = 'down'
        else:
            slime[5][0] += (0-slime[5][0])/10
            if slime[5][0] < 20:
                slime[5][1] = 'up'
                if dirts[slime[4]][0] != 'null':
                    if slime_entity.obj.rect.colliderect(pygame.Rect(dirts[slime[4]][0],dirts[slime[4]][1],10,8)):
                        alerts.append(['nom',slime[0][0]+4,slime[0][1]-8,0])
                        quiet_squish_sfx.play()
        blit_center(display,pygame.transform.rotate(pygame.transform.scale(slime_img,(24-int(slime_speed*2),34+int(slime_speed*3)-int(slime[5][0]/5))),slime[2]),(slime[0][0]-offset[0]+2,slime[0][1]-offset[1]+8))
        for bullet in bullets:
            if bullet[4] != 'planted':
                bulletR = pygame.Rect(bullet[0]-3,bullet[1]-3,6,6)
                if bulletR.colliderect(slime_entity.obj.rect):
                    squish_sfx.play()
                    slime[3][0] -= gun_dmg
                    bullets.remove(bullet)
        if slime[3][0] != slime[3][1]:
            display.blit(health_bar,(slime[0][0]-offset[0]-8,slime[0][1]-offset[1]-4))
            if slime[3][0] > 0:
                health_surf = pygame.Surface((int(slime[3][0]/slime[3][1]*20),2))
                health_surf.fill((0,163,131))
                display.blit(health_surf,(slime[0][0]-offset[0]-7,slime[0][1]-offset[1]-3))
        if slime[3][0] <= 0:
            slimes.remove(slime)
            for i in range(30):
                # x, y, size, rotation, rotation speed, momentum
                slime_balls.append([slime[0][0]+random.randint(0,24)-4,slime[0][1]+random.randint(0,24)-8,random.randint(5,15),random.randint(0,360),random.randint(0,90)-45,[random.randint(1,100)/50-1,random.randint(1,100)/50-1,]])
        elif slime[0][1] > 300:
            slimes.remove(slime)
    # Islands ------------------------------------------------ #
    display.blit(island_0,(300-offset[0],80-offset[1]))
    display.blit(island_1,(120-offset[0],120-offset[1]))
    display.blit(island_2,(10-offset[0],100-offset[1]))
    # Particles ---------------------------------------------- #
    for particle in particles:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[3] += 0.15
        if particle[3] > 2:
            particle[3] = 2
        display.set_at((int(particle[0])-offset[0],int(particle[1])-offset[1]),particle[5])
        particle[4] -= 1
        if particle[4] <= 0:
            particles.remove(particle)
    # Slime Balls -------------------------------------------- #
    for ball in slime_balls:
        ball[0] += ball[5][0]
        ball[1] += ball[5][1]
        ball[3] += ball[4]
        if len(ball) == 6:
            blit_center(display,pygame.transform.rotate(pygame.transform.scale(slime_ball,(int(ball[2]),int(ball[2]))),ball[3]),(ball[0]-offset[0],ball[1]-offset[1]))
        else:
            blit_center(display,pygame.transform.rotate(pygame.transform.scale(smoke_img,(int(ball[2]),int(ball[2]))),ball[3]),(ball[0]-offset[0],ball[1]-offset[1]))
        ball[2] -= 0.2
        if ball[2] <= 0:
            slime_balls.remove(ball)
    # Bullets ------------------------------------------------ #
    n = 0
    for bullet in bullets:
        if bullet[4] != 'planted':
            dx = math.cos(math.radians(bullet[2]))
            dy = math.sin(math.radians(bullet[2]))
            bullet[0] += dx*bullet_speed
            bullet[1] += dy*bullet_speed
        if (bullet[4] == 'planted') or (bullet[3] >= 3):
            blit_center(display,pygame.transform.rotate(bullet_img,-bullet[2]),(int(bullet[0])-offset[0],int(bullet[1])-offset[1]))
        #display.set_at((int(bullet[0])-offset[0],int(bullet[1])-offset[1]),(247,163,6))
        bulletR = pygame.Rect(bullet[0],bullet[1],2,2)
        if bullet[4] == 'plant':
            for dirt in dirts:
                if dirt[0] != 'null':
                    dirtR = pygame.Rect(dirt[0]+2,dirt[1]+4,6,4)
                    if bulletR.colliderect(dirtR):
                        if dirt[2] == 0:
                            dirt[2] = 1
                            bullet[3] = 1
                            bullet[4] = 'planted'
                            bullet[1] = dirt[1]+4
                            if dirt[0] == 182:
                                bullet.append('')
        bullet[3] += 1
        popped = False
        if bullet[3] == 3:
            for i in range(2):
                slime_balls.append([bullet[0],bullet[1],random.randint(5,10),random.randint(0,360),random.randint(0,45),[random.randint(1,100)/50-1,random.randint(1,100)/200-0.75],'smoke'])
        if bullet[4] != 'planted':
            if bullet[3] > 200:
                bullets.remove(bullet)
                popped = True
        elif bullet[3] > 900:
            bullets.remove(bullet)
            popped = True
        if popped == False:
            for hitbox in hitboxes:
                bulletR = pygame.Rect(bullet[0],bullet[1],2,2)
                if bulletR.colliderect(hitbox):
                    try:
                        bullets.remove(bullet)
                    except ValueError:
                        pass
    # Target Image ------------------------------------------- #
    if gun_target != None:
        target_timer += 1
        if target_timer >= 60:
            target_timer = 0
        if target_timer < 30:
            display.blit(target_img,(target_pos[0]-6-offset[0],target_pos[1]-6-offset[1]))
        else:
            display.blit(target_2_img,(target_pos[0]-6-offset[0],target_pos[1]-6-offset[1]))
    # Alerts ------------------------------------------------- #
    for alert in alerts:
        alert[2] -= 0.2
        width = get_text_width(alert[0],1)
        text_surf = pygame.Surface((width,10))
        text_surf.set_colorkey((0,0,0))
        text_surf.set_alpha(255-alert[3]*255/90)
        text.show_text(alert[0],0,0,1,99999,font_1,text_surf)
        display.blit(text_surf,(alert[1]-int(width/2)-offset[0],alert[2]-offset[1]))
        alert[3] += 1
        if alert[3] == 90:
            alerts.remove(alert)
    # Offset Handling ---------------------------------------- #
    x_dif = player.x-200
    y_dif = player.y-150
    true_offset[0] += minimum(x_dif/3-true_offset[0],1)/30
    true_offset[1] += minimum(y_dif/3-true_offset[1],1)/30
    offset = [int(true_offset[0]),int(true_offset[1])]
    # GUI ---------------------------------------------------- #
    display.blit(gun_mode_back,(0,0))
    if gun_mode == 'plant':
        display.blit(plant_mode_img,(1,1))
    else:
        display.blit(kill_mode_img,(1,1))
    display.blit(bullets_back_img,(0,233))
    display.blit(bullet_gui_img,(3,240))
    text.show_text(str(ammo),8,240,1,99999,font_0,display)
    width = len(str(int(game_timer/60)))*4
    text.show_text(str(int(game_timer/60)) + ' seconds',366 - width,2,1,99999,font_1,display)
    try:
        fps = int(1000/(sum(last_frames)/20))
    except ZeroDivisionError:
        fps = 0
    if show_fps == True:
        text.show_text(str(fps) + ' fps',366,12,1,99999,font_1,display)
    # Shoot -------------------------------------------------- #
    if firing == True:
        fire_timer += 1
        if fire_timer >= 7:
            fire_timer = 0
            if ammo > 0:
                bullets.append([player.x+6,player.y+5,-(gun_angle+90),0,gun_mode])
                ammo -= 1
                pew_sfx.play()
    else:
        fire_timer = 6
    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT:
                right = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_UP:
                if jumps > 0:
                    player_momentum[1] = -5
                    jumps -= 1
                    jump_particles.append([e.entity(player.x-2,player.y+7,2,2),0])
            if event.key == K_c:
                if gun_mode == 'plant':
                    gun_mode = 'kill'
                else:
                    gun_mode = 'plant'
            if event.key == K_x:
                firing = True
            if event.key == K_f:
                if show_fps == False:
                    show_fps = True
                else:
                    show_fps = False
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                right = False
            if event.key == K_LEFT:
                left = False
            if event.key == K_x:
                firing = False
    # Update ------------------------------------------------- #
    screen.blit(pygame.transform.scale(display,(WINDOWWIDTH,WINDOWHEIGHT)),(0,0))
    pygame.display.update()
    mainClock.tick(60)
    last_frames.append(get_ms()-last_frame)
    last_frames.pop(0)
    last_frame = get_ms()
    # Handle Loss -------------------------------------------- #
    lost_time = 0
    while lost:
        if lost_time == 0:
            display_copy = display.copy()
        display.blit(display_copy,(0,0))
        black_surf = pygame.Surface((400,250))
        black_surf.set_alpha(maximum(lost_time*3,100))
        display.blit(black_surf,(0,0))
        lost_time += 1
        if lost_time > 33:
            text.show_text('The hungry slimes ate all of your dirt',110,50,1,99999,font_1,display)
            text.show_text('and you\'ve run out of space to grow bullets.',110,60,1,99999,font_1,display)
            text.show_text('You\'ve lost... Press any key to restart.',110,70,1,99999,font_1,display)
            text.show_text('You lasted ' + str(int(game_timer/60)) + ' seconds.',110,90,1,99999,font_1,display)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if lost_time > 90:
                    lost = False
                    offset = [0,0]
                    true_offset = [0,0]
                    hitboxes = [pygame.Rect(12,103,92,21),pygame.Rect(12,124,70,60),pygame.Rect(127,173,147,100),pygame.Rect(304,90,82,100)]
                    player = e.entity(200,156,12,16)
                    player.set_image(player_img)
                    player_momentum = [0,0]
                    jumps = 2
                    jumps_max = 2
                    right = False
                    left = False
                    speed = 2.5
                    dirts = [[127,166,0],[153,166,0],[182,166,0],[195,166,0],[208,166,0],[221,166,0],
                             [256,166,0],[328,82,0],[342,82,0],[373,82,0],[15,96,0],[28,96,0],[41,96,0],
                             [54,96,0],[67,96,0],[80,96,0],[93,96,0],]
                    for dirt in dirts:
                        dirt.append(300)
                    gun_mode = 'plant'
                    gun_angle = 0
                    gun_target_angle = 0
                    gun_turn_rate = 6
                    bullets = []
                    firing = False
                    fire_timer = 0
                    bullet_speed = 5
                    ammo = 200
                    slimes = []
                    gun_dmg = 50
                    game_timer = 0
                    slime_rate = 240
                    player_flash_timer = 0
                    target_pos = None
                    slime_balls = []
                    alerts = []
                    jump_particles = []
                    particles = []
                    air_time = 0
        screen.blit(pygame.transform.scale(display,(WINDOWWIDTH,WINDOWHEIGHT)),(0,0))
        pygame.display.update()
        mainClock.tick(60)
    
