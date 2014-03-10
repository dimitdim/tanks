# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 21:40:07 2014

@author: kyle & dimitdim
"""

import pygame
from pygame.locals import *
import random
import math
import time

class Projectile:
    """Encapsulates state variables for a projectile"""
    def __init__(self,x,y,size,color):
        self.vx=0.0
        self.vy=0.0
        self.x=x
        self.y=y
        self.size=size
        self.color=color
    def move_projectile(self,ax,ay):
        """
        Takes the component velocities and component accelerations,
        and returns delta x,y and change in velocity x,y        
        """
        self.vx+=ax
        self.vy+=ay
        self.x+=self.vx
        self.y+=self.vy

class Tank:
    def __init__(self,number,tank_size,lives):
        self.num=number
        self.height=tank_size
        self.width=tank_size
        self.lives=lives
        self.vx=0
        self.vy=0
        self.y=0
        if number==0: self.x=50; self.color=(255,0,0)
        elif number==1: self.x=590; self.color=(0,0,255)
        elif number==2: self.x=140; self.color=(0,255,0)
        elif number==3: self.x=500; self.color=(0,255,255)
        elif number==4: self.x=230; self.color=(255,255,0)
        elif number==5: self.x=410; self.color=(255,0,255)
        elif number==6: self.x=320; self.color=(255,255,255)
        else: raise NameError('Too Many Tanks!!')
        self.oldx=self.x

class Terrain:
    """Definition for one dx of the terrain.  Terrain is generated from lots of thin slits."""
    def __init__(self,x,y,width,height,color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color


class Tanks_Model:
    """Encodes the game state"""
    def __init__(self):
        self.running = True
        self.screen_width=640 # (px)
        self.screen_height=480 # (px)

        #Terrain:
        self.width=10.0 # Terrain strip width (px)
        self.height=200.0 # Staring terrain height (px)
        self.var=20.0 # Maximum height difference btwn consecutive strips (px)
        self.sky_color=(150,150,255) # (rgb)
        self.earth_color=(75,255,75) # (rgb)
        self.terrain=[]
        for x in range(int(self.screen_width/self.width)):
            self.height=self.height+random.randint(-self.var,self.var)
            if self.height>=self.screen_height-self.var: self.height=self.screen_height-self.var
            if self.height<=self.var: self.height=self.var
            self.terrain.append(Terrain(x*self.width,self.screen_height-self.height,self.width,self.height,self.earth_color))

        #Tanks:
        self.phase=0 # Decides which tank is active
        self.num_players=int(raw_input('Number of Tanks: '))
        self.tank_size=10.0 # (px*px)
        self.lives=int(raw_input('Number of Lives (3?): ')) # Starting
        self.max_dist=5 # (self.width)
        self.text_size=15
        self.lost_text=''
        self.lost_color=(0,0,0)
        self.tanks=[]
        for player in range(self.num_players):
            self.tanks.append(Tank(player,self.tank_size,self.lives))
            self.tanks[player].y=self.terrain[int((self.tanks[player].x/self.width))].y-10

        #Projectile:
        self.draw_mouse=False # For the purpose of drawing the targetting cursor
        self.last_mouse=(0,0) # Marks the initial mousedown location to help the user target
        self.draw_projectile=False
        self.wind=random.randint(-10,10)/1000.0 # (px/(.001s^2))
        self.new_wind=False # Reset wind per tern?
        self.gravity=0.075 # (px/(.001s^2))
        self.proj_color=(255,0,0)
        self.proj_int_x=0.0 # (px)
        self.proj_int_y=0.0 # (px)
        self.proj_size=8.0 # (px*px)
        self.projectile=Projectile(self.proj_int_x,self.proj_int_y,self.proj_size,self.proj_color)

    def update(self):
        hit=False
        for tank in self.tanks:
            tank.x+=tank.vx
            if tank.x>(tank.oldx+self.max_dist*self.width): tank.x=(tank.oldx+self.max_dist*self.width)
            elif tank.x<(tank.oldx-self.max_dist*self.width): tank.x=(tank.oldx-self.max_dist*self.width)
            if tank.x>(self.screen_width-self.width): tank.x=(self.screen_width-self.width)
            elif tank.x<0: tank.x=0
            tank.y=self.terrain[int((tank.x/self.width))].y-10

        self.projectile.move_projectile(self.wind,self.gravity) #Postive ax is to the right, positive y is down.
        if self.projectile.x>(self.screen_width-self.width):
            self.projectile.x=(self.screen_width-self.width)
            if self.draw_projectile==True:
                self.draw_projectile=False
                self.phase=(self.phase+1)%self.num_players
                self.tanks[self.phase].oldx=self.tanks[self.phase].x
                if self.new_wind: self.wind=random.randint(-10,10)/1000.0
        elif self.projectile.x<0:
            self.projectile.x=0
            if self.draw_projectile==True:
                self.draw_projectile=False
                self.phase=(self.phase+1)%self.num_players
                self.tanks[self.phase].oldx=self.tanks[self.phase].x
                if self.new_wind: self.wind=random.randint(-10,10)/1000.0

        if (self.projectile.x<=(self.tanks[self.phase].x-10) or self.projectile.x>=self.tanks[self.phase].x) and self.projectile.y>=self.terrain[int((self.projectile.x/self.width))].y-10 and self.draw_projectile==True:
            self.draw_projectile=False
            for p in range(self.num_players):
                if int(self.tanks[(self.phase+p)%self.num_players].x-10)<int(self.projectile.x)<int(self.tanks[(self.phase+p)%self.num_players].x+10):
                    self.tanks[(self.phase+p)%self.num_players].lives-=1
                    if self.tanks[(self.phase+p)%self.num_players].lives<=0:
                        self.lost_text='Player '+str(self.tanks[(self.phase+p)%self.num_players].num+1)+' Lost!'
                        self.lost_color=self.tanks[(self.phase+p)%self.num_players].color
                        self.tanks.remove(self.tanks[(self.phase+p)%self.num_players])
                        self.num_players-=1
                    hit=True
            if not hit:
                self.terrain[int((self.projectile.x/self.width))].height-=10
                self.terrain[int((self.projectile.x/self.width))].y+=10
            self.phase=(self.phase+1)%self.num_players
            self.tanks[self.phase].oldx=self.tanks[self.phase].x
            if self.new_wind: self.wind=random.randint(-10,10)/1000.0
        if len(self.tanks)<=1: self.running=False

class PyGameView:
    """Renders model data to the window"""
    def __init__(self,model):
        self.model = model
        self.screen = pygame.display.set_mode((model.screen_width,model.screen_height))
        pygame.display.set_caption('Tanks!')
        self.font = pygame.font.SysFont("monospace", model.text_size)
    def draw(self):
        self.screen.fill(model.sky_color)
        for dx in self.model.terrain:
            pygame.draw.rect(self.screen,dx.color,(dx.x,dx.y,dx.width,dx.height))
        for tank in self.model.tanks:
            pygame.draw.rect(self.screen,tank.color,(tank.x,tank.y,tank.width,tank.height))
            if tank.lives==1:
                label_text='Player '+str(tank.num+1)+' has '+str(tank.lives)+' life.'
            else:
                label_text='Player '+str(tank.num+1)+' has '+str(tank.lives)+' lives.'
            label = self.font.render(label_text, 1, tank.color)
            self.screen.blit(label, (model.text_size,model.text_size*tank.num))
        pygame.draw.rect(self.screen,self.model.tanks[self.model.phase].color,(0,self.model.tanks[self.model.phase].num*model.text_size,model.text_size,model.text_size))
        if self.model.draw_projectile==True:   
            pygame.draw.rect(self.screen,pygame.Color(128,128,128),pygame.Rect(model.projectile.x,model.projectile.y,model.projectile.size,model.projectile.size))
        if self.model.draw_mouse==True:
            pygame.draw.rect(self.screen,pygame.Color(200,200,200,),pygame.Rect(pygame.mouse.get_pos()[0]-25,pygame.mouse.get_pos()[1],50,3))
            pygame.draw.rect(self.screen,pygame.Color(200,200,200,),pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]-25,3,50))
            pygame.draw.rect(self.screen,pygame.Color(200,200,200,),pygame.Rect(self.model.last_mouse[0],self.model.last_mouse[1],10,10))
        if model.wind>0: self.wind_text=str(model.wind)+' Mpx/s^2 RIGHT'
        elif model.wind<0: self.wind_text=str(-model.wind)+' Mpx/s^2 LEFT'
        else: self.wind_text=str(model.wind)+' Mpx/s^2'
        label = self.font.render(self.wind_text, 1, (0,0,0))
        self.screen.blit(label, (model.screen_width-17*model.text_size,0))
        label = self.font.render(model.lost_text, 1, model.lost_color)
        self.screen.blit(label, (model.screen_width/2-7*model.text_size,model.screen_height/2))
        pygame.display.update()

class Controller:
    def __init__(self,model):
        self.model=model
    def handle_pygame_event(self,event):
        """
        Mouse event handling is for determining shooting power.
        """
        if event.type == MOUSEBUTTONDOWN:
            self.model.draw_mouse=True
            self.i_pos=pygame.mouse.get_pos()
            self.model.last_mouse=self.i_pos
        elif event.type == MOUSEBUTTONUP:
            self.f_pos=pygame.mouse.get_pos()
            self.model.draw_projectile=True
            self.model.projectile.x=self.model.tanks[self.model.phase].x-10
            self.model.projectile.y=self.model.tanks[self.model.phase].y-10
            self.model.projectile.vx=0.05*(self.f_pos[0]-self.i_pos[0])
            self.model.projectile.vy=0.05*(self.f_pos[1]-self.i_pos[1])
            self.model.draw_mouse=False
        if event.type == KEYDOWN:
            """
            if event.key == pygame.K_SPACE:
                self.model.draw_projectile=True
                self.model.projectile.x=self.model.tanks[self.model.phase].x-10
                self.model.projectile.y=self.model.tanks[self.model.phase].y-10
                self.model.projectile.vx=2
                self.model.projectile.vy=-2 #define this negative because of how the coordinate system works.
            """
            if event.key == pygame.K_LEFT:
                self.model.tanks[self.model.phase].vx=-1.0
            elif event.key == pygame.K_RIGHT:
                self.model.tanks[self.model.phase].vx=1.0
            else: return
        elif event.type == KEYUP:
            if event.key == pygame.K_LEFT:
                self.model.tanks[self.model.phase].vx=0.0
            elif event.key == pygame.K_RIGHT:
                self.model.tanks[self.model.phase].vx=0.0
            else:  return
        else:
            return

           
if __name__ == '__main__':
    pygame.init()
    model = Tanks_Model()
    view = PyGameView(model)
    controller = Controller(model)
    while model.running:
        for event in pygame.event.get():
            if event.type == QUIT: model.running = False
            else: controller.handle_pygame_event(event)
        model.update()
        view.draw()
        time.sleep(.001)
    won_text='Player '+str(model.tanks[0].num+1)+' Won!!'
    label = view.font.render(won_text, 1, model.tanks[0].color)
    view.screen.blit(label, (model.screen_width/2-7*model.text_size,model.screen_height/2-2*model.text_size))
    pygame.display.update()
    time.sleep(4)
    pygame.quit()
