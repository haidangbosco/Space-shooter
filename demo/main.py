import pygame,random
import pdb
from copy import *
import numpy
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
bullet_img = [pygame.image.load('bullet.png'),pygame.image.load('double-bullet.png')]
for item in bullet_img:
    item.set_colorkey(black)
#--------------------------------------------------------
class NightRiderBullet(pygame.sprite.Sprite):
    def __init__(self,bullet_type,x_pos=50,y_pos=150):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_pos
        self.y = y_pos
        self.img = bullet_img[bullet_type] # change bullet type
        self.rect = self.img.get_rect()

    def update(self,distance=20):
        self.x = self.x + distance
        screen.blit(self.img,(self.x,self.y))
        self.erase()

    def erase(self):
        if self.x > dw:
            # print(self.x)
            self.kill()

class KillBeam(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 15
        self.y = 0
        self.img = kill_beam_img
        self.rect = kill_beam_img.get_rect()

    def update(self,distance=0):
        self.x = (self.x + 1 + distance) if self.x > -400 else -400
        screen.blit(self.img,(self.x,self.y))
        self.GetRect()

    def GetRect(self):
        self.rect = pygame.Rect(self.x,self.y,self.rect.width,self.rect.height)

    def CheckCollision(self,obj_list):
        for obj in obj_list:
            if type(obj) != None:
            #     kill_point = obj.x if obj.x < 250 else 250
            #     if (self.x == kill_point):
            #         obj.explode = True
                obj.explode = pygame.sprite.collide_rect(obj,self)
            #
            # print(obj.explode)
            # print(obj.rect)
            # print(self.rect)

class NightRider(pygame.sprite.Sprite):
    def __init__(self,x_pos=60,y_pos=150):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_pos
        self.y = y_pos
        self.onscreen_x = 60
        self.onscreen_y = copy(self.y)
        self.kill = False
        self.explode = False
        self.imgs = [night_raider_img] + explosion_img
        self.index_img = 0
        self.upgrade_level = 1 # different level different bullet type
        self.rect = night_raider_img.get_rect()

    def MoveUpAndDown(self,distanceY=1):
        temp =  self.y + distanceY
        self.y = temp if temp <= 400 and temp >= 0 else self.y
        self.onscreen_y = self.y

    def MoveFordward(self,distanceX=1):
        self.x -=distanceX

    def GetRect(self):
        self.rect =  pygame.Rect(self.onscreen_x,self.onscreen_y,self.rect.width,self.rect.height)

    def ShootBullet(self,sprite_gr):
        if len(sprite_gr) == 0:
            if self.upgrade_level == 0:
                bullet = NightRiderBullet(self.upgrade_level,self.onscreen_x + 50,self.onscreen_y + 10)
            elif self.upgrade_level == 1:
                bullet = NightRiderBullet(self.upgrade_level,self.onscreen_x + 50,self.onscreen_y + 30)
            sprite_gr.add(bullet)

    def update(self):
        # self.rect = self.rect.clamp(screen.get_rect())
        if self.explode == False:
            self.onscreen_y = copy(self.y)
            screen.blit(self.imgs[self.index_img],(self.onscreen_x,self.y))
            self.GetRect()
        else:
            # import pdb; pdb.set_trace()
            if self.kill is not True:
                self.index_img = self.index_img + 1
                screen.blit(self.imgs[self.index_img],(self.onscreen_x,self.onscreen_y))
                # import pdb; pdb.set_trace()
                self.GetRect()
                self.kill = True if self.index_img == len(self.imgs) - 1 else False

class MainGame(object):
    def __init__(self):
        screen.fill(white)
        screen.blit(space_bg_img[0],(0,0))
        self.revive_counter = 0
        self.bg_sprite_counter = 0
        self.current_sprite = 0
        self.ride = NightRider()
        self.kill_beam = KillBeam()
        self.bullet_gr = pygame.sprite.Group()
        self.camera = self.ride
        self.camera_offset = 60
        self.keys = {"up_key": False,
        "down_key": False,
        "right_key": False,
        "a_key":False}
        while (True):
            # pdb.set_trace()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.ride.kill == False:
                    if event.key == pygame.K_UP:
                        self.SetHoldKey("up_key")
                    elif event.key == pygame.K_DOWN:
                        self.SetHoldKey("down_key")
                    elif event.key == pygame.K_RIGHT:
                        self.SetHoldKey("right_key")
                    elif event.key == pygame.K_a:
                        self.SetHoldKey("a_key")

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.keys["up_key"] = False
                    elif event.key == pygame.K_DOWN:
                        self.keys["down_key"] = False
                    elif event.key == pygame.K_RIGHT:
                        self.keys["right_key"] = False
                    elif event.key == pygame.K_a:
                        self.keys["a_key"] = False

            self.Update()
            pygame.display.update()
            clock.tick(fps)

    #demo
    def Update(self):
        screen.fill(white)
        move_from_kill_beam = 0
        if self.ride.explode == True:
            for name,val in self.keys.items():
                self.keys[name] = False
        if self.ride.kill == False:
            if self.keys["up_key"]:
                self.ride.MoveUpAndDown(-2)
            if self.keys["down_key"]:
                self.ride.MoveUpAndDown(2)
            if self.keys["right_key"]:
                self.ride.MoveFordward(-2)
                move_from_kill_beam = -2
            if self.keys["a_key"]:
                self.ride.ShootBullet(self.bullet_gr)
        else:
            self.ride.MoveFordward(-2)
            move_from_kill_beam = -2

        self.ScrollScreen(self.current_sprite)
        self.kill_beam.update(move_from_kill_beam)
        # update night rider
        self.ride.update()
        # update bullets
        # pdb.set_trace()
        self.bullet_gr.update()
        # print(self.bullet_gr)
        # # check for impact
        temp_list = [self.ride]
        obj_list = [item for item in temp_list if item.explode == False]
        self.kill_beam.CheckCollision(obj_list)
        if self.ride.kill == True:
            self.NewNightRider()

    def SetHoldKey(self,str):
        for name,value in self.keys.items():
            if str == name:
                self.keys[name] = True

    def ScrollScreen(self,current_sprite):
        if (self.camera.x - space_bg_pos[self.bg_sprite_counter][0] > dw + self.camera_offset):
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
        self.revive_counter += clock.get_time()/1000
        if self.revive_counter > 3:
            # import pdb; pdb.set_trace()
            # print(self.camera.x%250)
            self.revive_counter = 0
            self.ride = NightRider(self.camera.x,150)
            self.camera = self.ride

pygame.init()
demo = MainGame()
