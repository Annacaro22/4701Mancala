import pygame
from stone import Stone
import numpy as np
from const import (
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  BOARD_COLOR,
  BOWL_COLOR
)


class Board():
    currently_animating = False
    state = {
        'bowl': {
            'p1': [[]]*6,
            'p2': [[]]*6
        },
        'goal': {
            'p1': [],
            'p2': []
        },
        'moving': []
    }
    turn = 'p1'

    center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    goal_width = 75
    hor_offset = 20
    board_shape = (700, 200)
    bowl_diameter = (board_shape[0] - (2*goal_width) - (9*hor_offset))/6
    ver_offset = (board_shape[1]-2*bowl_diameter)/3     
    p1_bowl_pos = []
    p2_bowl_pos = []
    p1_goal_pos = None
    p2_goal_pos = None

    def init_stones_on_bowl(self, bowl_center, bowl_index, player):
        pos = (bowl_center[0],bowl_center[1] + self.bowl_diameter/4)
        stone_1 = Stone(pos)
        pos = (bowl_center[0] + self.bowl_diameter/4,bowl_center[1])
        stone_2 = Stone(pos)
        pos = (bowl_center[0],bowl_center[1] - self.bowl_diameter/4)
        stone_3 = Stone(pos)
        pos = (bowl_center[0] - self.bowl_diameter/4,bowl_center[1])
        stone_4 = Stone(pos)
        self.state['bowl'][player][bowl_index] = [stone_1, stone_2, stone_3, stone_4]
        

    def init_stones(self):
        # initialize stones on the board
        for i in range(6):
            self.init_stones_on_bowl(self.p1_bowl_pos[i], i, 'p1')
            self.init_stones_on_bowl(self.p2_bowl_pos[i], i, 'p2')


    def __init__(self):
        self.surf = pygame.Surface(self.board_shape)
        self.surf.fill(BOARD_COLOR)
        self.pos = (self.center[0]-(self.surf.get_width()/2), self.center[1]-(self.surf.get_height()/2))

        # initialize bowl positions
        for i in range(6):
            x_pos = self.center[0] - self.surf.get_width()/2 + self.hor_offset*2 + self.goal_width + self.bowl_diameter/2 + (self.bowl_diameter+self.hor_offset)*i
            y_pos = self.center[1] - self.ver_offset/2 - self.bowl_diameter/2
            self.p2_bowl_pos.append(np.array([x_pos,y_pos]))
            y_pos += self.ver_offset + self.bowl_diameter
            self.p1_bowl_pos.append(np.array([x_pos,y_pos]))

        # initialize stones
        self.init_stones()  

    # def update(self):
    #     for bowl in self.state['bowl']['p1']:
    #         for stone in bowl:
    #             stone.update()
    #     for bowl in self.state['bowl']['p2']:
    #         for stone in bowl:
    #             stone.update()


    def draw(self, screen):
        # draw board background
        screen.blit(self.surf, self.pos)

        # draw left goal
        left = self.center[0]-(self.surf.get_width()/2) + self.hor_offset
        top = self.center[1]-(self.surf.get_height()/2) + self.ver_offset
        self.p2_goal_pos = (self.center[0]-(self.surf.get_width()/2) + self.hor_offset + self.goal_width/2, self.center[1])
        bound = pygame.Rect(left, top, self.goal_width, self.board_shape[1]-2*self.ver_offset)
        pygame.draw.ellipse(screen, BOWL_COLOR, bound)

        # draw right goal
        left = self.center[0]+(self.surf.get_width()/2) - self.hor_offset - self.goal_width
        self.p1_goal_pos = (self.center[0]+(self.surf.get_width()/2) - self.hor_offset - self.goal_width/2, self.center[1])
        bound = pygame.Rect(left, top, self.goal_width, self.board_shape[1]-2*self.ver_offset)
        pygame.draw.ellipse(screen, BOWL_COLOR, bound)

        # draw bowls
        for i in range(6):  
            pygame.draw.circle(screen, BOWL_COLOR, self.p1_bowl_pos[i], self.bowl_diameter/2)
            pygame.draw.circle(screen, BOWL_COLOR, self.p2_bowl_pos[i], self.bowl_diameter/2)

        # draw stones
        for bowl in self.state['bowl']['p1']:
            for stone in bowl:
                stone.draw(screen)
        for bowl in self.state['bowl']['p2']:
            for stone in bowl:
                stone.draw(screen)
        for stone in self.state['goal']['p1']:
            stone.draw(screen)
        for stone in self.state['goal']['p2']:
            stone.draw(screen)
        for stone in self.state['moving']:
            stone.draw(screen)

        
            

   