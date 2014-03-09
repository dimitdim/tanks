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
    def __init__(self,x,y,radius,blast_radius,color,child_projectile,spawn_delay):
        self.x=x
        self.y=y
        self.radius=radius
        self.blast_radius=blast_radius
        self.color=color
        self.spawn_delay=spawn_delay #Some forward thinking for varied projectiles
        self.child_projectile=child_projectile #Amount of projectiles spawned

class Player:
    def __init__(self,number):
        self=self
        self.height=10
        self.width=10
        self.y=20
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
    def __init__(self):
        self.phase=1 # Decides whose gets to move first.
        self.terrain=[]
        self.tanks=[]
        variance=10
        last_height=0
        self.width=10
        height=200
        for x in range(640/self.width):
            height=height+random.randint(0,0)
            new_dx=Terrain_dx(x*self.width,480-height,self.width,height)
            self.terrain.append(new_dx)
        for x in range(2):
            self.tanks.append(Player(x))
    def update(self):
        for tank in self.tanks:
            tank.y=self.terrain[(tank.x/self.width)].height-10
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
        pygame.display.update()

class Controller:
    def __init__(self,model):
        self.model=model
        
    def handle_pygame_event(self,event):
        return

if __name__ == '__main__':
    pygame.init()
    size=(640,480)
    screen=pygame.display.set_mode(size)
    model = Tanks_Model()
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
