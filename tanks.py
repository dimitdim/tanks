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
        self.x=x
        self.y=y
        self.vx=0.0
        self.vy=0.0
        self.size=size
        self.color=color

    def move_projectile(self,ax,ay):
        """
        Takes the component velocities and component accelerations,
        and returns delta x,y and change in velocity x,y        
        """
        self.x+=self.vx
        self.y+=self.vy
        self.vx+=ax
        self.vy+=ay
    

class Player:
    def __init__(self,number):
        self=self
        self.height=10
        self.width=10
        self.y=0
        self.vx=0
        if number==0:
            self.x=40
            self.color=(255,0,0)
        elif number==1:
            self.x=600
            self.color=(0,0,255)
        else: raise NameError('too many tanks')

class Terrain_dx:
    """Definition for one dx of the terrain.  Terrain is generated from lots of thin slits."""
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=(255,255,255)


class Tanks_Model:
    """Encodes the game state"""
    def __init__(self,screen_width,screen_height,wind,gravity):
        self.phase=1 # Decides which tank is active.
        self.terrain=[]
        self.tanks=[]
        self.projectile=Projectile(0,0,10,(255,0,0))
        self.width=10
        self.num_players=2
        self.wind=wind
        self.gravity=gravity
        height=200
        
        self.draw_projectile=False
        self.draw_mouse=False #For the purpose of drawing the targetting cursor
        self.last_mouse=(0,0) #Marks the initial mousedown location to help the user target
        for x in range(int(screen_width/self.width)):
            height=height+random.randint(-10,10)
            new_dx=Terrain_dx(x*self.width,screen_height-height,self.width,height)
            self.terrain.append(new_dx)
        for x in range(self.num_players):
            self.tanks.append(Player(x))
        
    def update(self):
        for tank in self.tanks:
            tank.x+=tank.vx
            if tank.x>(screen_width-self.width): tank.x=(screen_width-self.width)
            elif tank.x<0: tank.x=0
            tank.y=self.terrain[int((tank.x/self.width))].height-10
        self.projectile.move_projectile(self.wind,self.gravity) #Postive ax is to the right, positive y is down.
        return

class PyGameView:
    """Renders model data to the window"""
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for dx in self.model.terrain:
            pygame.draw.rect(self.screen,dx.color,(dx.x,dx.height,dx.width,dx.height))
        for tank in self.model.tanks:
            pygame.draw.rect(self.screen,tank.color,(tank.x,tank.y,tank.width,tank.height))
        if self.model.draw_projectile==True:   
            pygame.draw.rect(self.screen,pygame.Color(128,128,128),pygame.Rect(model.projectile.x,model.projectile.y,model.projectile.size,model.projectile.size))
        if self.model.draw_mouse==True:
            pygame.draw.rect(self.screen,pygame.Color(200,200,200,),pygame.Rect(pygame.mouse.get_pos()[0]-25,pygame.mouse.get_pos()[1],50,3))
            pygame.draw.rect(self.screen,pygame.Color(200,200,200,),pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]-25,3,50))
            pygame.draw.rect(self.screen,pygame.Color(0,255,0,),pygame.Rect(self.model.last_mouse[0],self.model.last_mouse[1],10,10))
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
    screen_width = 640
    screen_height = 480
    size = (screen_width,screen_height)
    screen = pygame.display.set_mode(size)
    model = Tanks_Model(screen_width,screen_height,0.0,0.075)#the constants initalize gravity and wind.
    view = PyGameView(model,screen)
    controller = Controller(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_pygame_event(event)
        model.update()
        view.draw()
        time.sleep(.001)
    pygame.quit()
