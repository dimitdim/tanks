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
        self.vx=0
        self.vy=0
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
        self.y=20
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
    def __init__(self,screen_width,screen_height):
        self.phase=0 # Decides whose gets to move first.
        self.terrain=[]
        self.tanks=[]
        variance=10
        last_height=0
        self.width=10
        height=200
        for x in range(int(screen_width/self.width)):
            height=height+random.randint(0,0)
            new_dx=Terrain_dx(x*self.width,height,self.width,height)
            self.terrain.append(new_dx)
        for x in range(2):
            self.tanks.append(Player(x))
        self.projectile=Projectile(0,0,3,(255,0,0))
        draw_projectile=False
    def update(self):
        for tank in self.tanks:
            tank.x+=tank.vx
            tank.y=self.terrain[int((tank.x/self.width))].height-10
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
        #pygame.draw.rect(self.screen,pygame.Color(128,128,128),py)
        pygame.display.update()

class Controller:
    def __init__(self,model):
        self.model=model
        
    def handle_pygame_event(self,event):
        if event.type != KEYDOWN:
            return
        elif event.key == pygame.K_SPACE:
            self.model.draw_projectile=True
        elif event.key == pygame.K_LEFT:
            self.model.tanks[self.model.phase].vx=10.0
        else: return

if __name__ == '__main__':
    pygame.init()
    screen_width = 640
    screen_height = 480
    size = (screen_width,screen_height)
    screen = pygame.display.set_mode(size)
    model = Tanks_Model(screen_width,screen_height)
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
