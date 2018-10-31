import pygame,random
import pdb
from copy import *
from pygame import *

red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
white=(255,255,255)
orange=(255,128,0)
black=(0,0,0)
dw=600
dh=400
fps=60
screen=pygame.display.set_mode([dw,dh])
pygame.display.set_caption("Space Shooter")
clock=pygame.time.Clock()
#-------------------sounds-----------------------------------
#-------------------images-----------------------------------
# bbirdimg=[ pygame.image.load('bb'+str(i)+'.png') for i in range(1,4)]
# ybirdimg=[ pygame.image.load('yb'+str(i)+'.png') for i in range(1,4)]
# rbirdimg=[ pygame.image.load('rb'+str(i)+'.png') for i in range(1,4)]
# bottompipeimg=pygame.image.load('bottompipe.png')
# nightbg=pygame.image.load('bg1.png')
# daybg=pygame.image.load('bg2.png')
# base=pygame.image.load('base.png')
# daybgicon=pygame.image.load('daybg.png')
# nightbgicon=pygame.image.load('nightbg.png')
# bw,bh=nightbg.get_rect().size
# basew,baseh=base.get_rect().size
explosion_sheet =  pygame.image.load('explosion.png')
explosion_img = []
for i in range(0,3):
    for j in range(0,5):
        explosion_img.append(explosion_sheet.subsurface(126*j,131*i,126,131))

night_raider = pygame.image.load('night-raider.png')
night_raider_img = pygame.transform.scale(night_raider,(100,100))
space_bg_img = [pygame.image.load('demo-bg.png'),pygame.image.load('demo-bg-3.jpg')]
space_bg_pos = [(0,0),(600,0)]
kill_beam_img = pygame.image.load('kill-beam.png')
#--------------------------------------------------------
class KillBeam(object):
    def __init__(self):
        self.x = 24
        self.y = 0
        self.img = kill_beam_img
        self.rect = kill_beam_img.get_rect()

    def Update(self,distance=0):
        self.x = (self.x + 1 + distance) if self.x > -400 else -400
        screen.blit(self.img,(self.x,self.y))

    def Eliminate(self,obj_list):
        for obj in obj_list:
            if type(obj) == NightRider:
                kill_point = obj.x if obj.x < 250 else 250
                if (self.x == kill_point):
                    obj.explode = True

class NightRider(object):
    def __init__(self,x_pos=50,y_pos=150):
        self.x = x_pos
        self.y = y_pos
        self.onscreen_x = self.x
        self.onscreen_y = self.y
        self.kill = False
        self.explode = False
        self.imgs = [night_raider_img] + explosion_img
        self.index_img = 0
        self.rect = night_raider_img.get_rect()

    def MoveUpAndDown(self,distanceY=1):
        temp =  self.y + distanceY
        self.y = temp if temp <= 400 and temp >= 0 else self.y
    def MoveBackAndFord(self,distanceX=1):
        self.x -=distanceX

    def Update(self):
        # self.rect = self.rect.clamp(screen.get_rect())
        if self.explode == False and self.kill == False:
            self.onscreen_x = self.x if self.x < 250 else 250
            self.onscreen_y = self.y
            screen.blit(self.imgs[self.index_img],(self.onscreen_x,self.y))

        else:
            # import pdb; pdb.set_trace()
            if self.kill is not True:
                self.index_img = self.index_img + 1
                screen.blit(self.imgs[self.index_img],(self.onscreen_x,self.y))
                self.kill = True if self.index_img == len(self.imgs) - 1 else False

class MainGame(object):
    def __init__(self):
        screen.fill(white)
        screen.blit(space_bg_img[0],(0,0))
        self.bg_sprite_counter = 0
        self.current_sprite = 0
        self.ride = NightRider()
        self.kill_beam = KillBeam()
        self.camera = self.ride
        self.camera_offset = 50
        self.keys = {"up_key": False,
        "down_key": False,
        "left_key": False,
        "right_key": False}
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.SetHoldKey("up_key")
                    elif event.key == pygame.K_DOWN:
                        self.SetHoldKey("down_key")
                    elif event.key == pygame.K_RIGHT:
                        self.SetHoldKey("right_key")
                    elif event.key == pygame.K_LEFT:
                        self.SetHoldKey("left_key")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.keys["up_key"] = False
                    elif event.key == pygame.K_DOWN:
                        self.keys["down_key"] = False
                    elif event.key == pygame.K_RIGHT:
                        self.keys["right_key"] = False
                    elif event.key == pygame.K_LEFT:
                        self.keys["left_key"] = False

            self.Update()
            pygame.display.update()
            clock.tick(fps)

    #demo
    def Update(self):
        screen.fill(white)
        move_from_kill_beam = 0
        if self.keys["up_key"]:
            self.ride.MoveUpAndDown(-2)
        if self.keys["down_key"]:
            self.ride.MoveUpAndDown(2)
            print("hello")
        if self.keys["right_key"] or self.ride.kill == True:
            self.ride.MoveBackAndFord(-2)
            move_from_kill_beam = -2
        if self.keys["left_key"]:
            self.ride.MoveBackAndFord(1)
            move_from_kill_beam = 1

        self.ScrollScreen(self.current_sprite)
        self.kill_beam.Update(move_from_kill_beam)
        # check for impact
        temp_list = [self.ride]
        obj_list = [item for item in temp_list if item is not None ]
        self.kill_beam.Eliminate(obj_list)
        # update night rider
        self.ride.Update()
        if self.ride.kill == True:
            self.NewNightRider()

    def SetHoldKey(self,str):
        for name,value in self.keys.items():
            if str == name:
                self.keys[name] = True

    def ScrollScreen(self,current_sprite):
        if (self.camera.x - space_bg_pos[self.bg_sprite_counter][0] > dw + 50):
            self.bg_sprite_counter = self.bg_sprite_counter + 1
            bg_pos_counter = len(space_bg_pos) - 1
            current_sprite = 0 if current_sprite == len(space_bg_img) - 1 else current_sprite + 1
            self.current_sprite = current_sprite

            if (current_sprite == len(space_bg_img) - 1):
                for i in range(0,len(space_bg_img)):
                    space_bg_pos.append(((bg_pos_counter + 1)*600,0))
                    bg_pos_counter = bg_pos_counter + 1
            # pdb.set_trace()

        screen.blit(space_bg_img[current_sprite],(space_bg_pos[self.bg_sprite_counter][0] - self.camera.x + self.camera_offset,0))
        next_sprite = 0 if current_sprite == len(space_bg_img) - 1 else current_sprite + 1
        screen.blit(space_bg_img[next_sprite],(space_bg_pos[self.bg_sprite_counter + 1][0] - self.camera.x + self.camera_offset,0))
        # print(space_bg_pos[self.bg_sprite_counter][0] - self.kill_beam.x + 24)
        # print(space_bg_pos[self.bg_sprite_counter + 1][0] - self.kill_beam.x + 24)
        # print(self.kill_beam.x)
        # input()

    def NewNightRider(self):
        if self.ride.kill == True:
            # import pdb; pdb.set_trace()
            # print(self.camera.x%250)
            if (self.camera.x%250 == 0):
                self.ride = NightRider(self.camera.x,150)
                self.camera = self.ride

pygame.init()
demo = MainGame()
