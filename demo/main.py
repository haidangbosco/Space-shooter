import pygame,random
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
night_raider = pygame.image.load('night-raider.png')
night_raider_img = pygame.transform.scale(night_raider,(100,100))
space_bg_img = [pygame.image.load('demo-bg.png'),pygame.image.load('demo-bg-2.jpg')]
space_bg_pos = [(0,0),(600,0)]
kill_beam_img = pygame.image.load('kill-beam.png')
#--------------------------pipe-y positions----------------
class KillBeam(object):
    def __init__(self):
        self.x = 24
        self.y = 0
        self.rect = kill_beam_img.get_rect()

    def Update(self):
        self.x = self.x + 1
        screen.blit(kill_beam_img,(self.x,self.y))

class NightRaider(object):
    def __init__(self):
        self.x = 50
        self.y = 150
        self.rect = night_raider_img.get_rect()

    def MoveUpAndDown(self,distanceY=1):
        self.y +=distanceY

    def MoveBackAndFord(self,distanceX=1):
        self.x -=distanceX

    def Update(self):
        # self.rect = self.rect.clamp(screen.get_rect())
        screen.blit(night_raider_img,(self.x,self.y))

class MainGame(object):
    def __init__(self):
        screen.fill(white)
        screen.blit(space_bg_img[0],(0,0))
        self.current_sprite = 0
        self.ride = NightRaider()
        self.kill_beam = KillBeam()
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
                    for name,value in self.keys.items():
                        self.keys[name] = False

            self.Update()
            pygame.display.update()
            clock.tick(fps)

    #demo
    def Update(self):
        screen.fill(white)
        if self.keys["up_key"]:
            self.ride.MoveUpAndDown(-1)
        elif self.keys["down_key"]:
            self.ride.MoveUpAndDown(1)
        elif self.keys["right_key"]:
            self.ride.MoveBackAndFord(-1)
        elif self.keys["left_key"]:
            self.ride.MoveBackAndFord(1)

        self.ScrollScreen(self.current_sprite)
        screen.blit(kill_beam_img,(24,0))
        self.kill_beam.Update()
        self.ride.Update()

    def SetHoldKey(self,str):
        for name,value in self.keys.items():
            if str == name:
                self.keys[name] = True
            else:
                self.keys[name] = False

    def ScrollScreen(self,current_sprite):
        if (self.ride.x - space_bg_pos[current_sprite][0] < dw):
            screen.blit(space_bg_img[current_sprite],(space_bg_pos[current_sprite][0] - self.kill_beam.x,0))
            next_sprite = current_sprite + 1;
            screen.blit(space_bg_img[next_sprite],(space_bg_pos[next_sprite][0] - self.kill_beam.x,0))

pygame.init()
demo = MainGame()
