# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 21:40:07 2014

@author: kyle
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
        self.spawn_delay=spawn_delay#Some forward thinking for varied projectiles
        self.child_projectile=child_projectile #Amount of projectiles spawned

class Player:
    def __init__(self):
        self=self

class Terrain_dx:
    """Definition for one dx of the terrain.  Terrain is generated from lots of thin slits."""
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height


class Tanks_Model:
    """Encodes the game state"""
    def __init__(self):
        self.phase=1 # Decides whose gets to move first.
        self.terrain=[]
        variance=10
        last_height=0
        width=10
        for x in range(640/width):
            height=random.randint(200,200)
            new_dx=Terrain_dx(x*width,480-height,width,height)
            self.terrain.append(new_dx)
    def update(self):
        return
            
class PyGameView:
    """Renders model data to the window"""
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for dx in self.model.terrain:
            pygame.draw.rect(self.screen,pygame.Color(255,255,255),pygame.Rect(dx.x,480-dx.height,dx.width,dx.height))
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
