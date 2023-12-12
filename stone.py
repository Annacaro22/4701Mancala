import pygame
from random import randint
import math
import numpy as np


class Stone(pygame.sprite.Sprite):
    velocity = 5
    moving = False
    dest = None #destination

    def __init__(self, center):
        super(Stone, self).__init__()
        self.shape = (20, 20)
        # self.pos = np.array((center[0]-self.shape[0]/2, center[1]-self.shape[1]/2))
        self.pos = np.array(center)
        self.surf = pygame.Surface(self.shape)
        color = (randint(0,255),randint(0,255),randint(0,255))
        self.surf.fill(color)

    def move_to(self, dest):
        # move center to dest
        print('move stone:')
        print(dest)
        self.dest = np.array(dest)
        self.moving = True

    def jump_to(self, pos):
        # jump center to pos
        self.pos = np.array((pos[0], pos[1]))
        self.moving = True

    def draw(self, screen):
        pos = self.pos[0]-self.shape[0]/2, self.pos[1]-self.shape[1]/2
        screen.blit(self.surf, pos)
    
    def update(self):
        if self.moving:
            dist = ((self.dest - self.pos) / np.linalg.norm((self.dest - self.pos))) * self.velocity
            if np.linalg.norm((self.dest - self.pos)) < self.velocity:
                self.pos = self.dest
                self.dest = None
                self.moving = False
            else:
                self.pos = self.pos + dist