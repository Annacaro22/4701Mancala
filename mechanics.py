import pygame
import math
from random import randint
import random
import numpy as np


def start_moving(board, bowl):
    # get stones and set to moving 
    (type, player, index) = bowl
    if type == 'bowl':
        stones = board.state[type][player][index]
        board.state[type][player][index] = []
    else:
        stones = board.state[type][player]
        board.state[type][player] = []
    board.state['moving'] = stones
    return board, (type, player, index)


def bowl_center(board, type, player, index):
    if type == 'bowl' and player == 'p1':
        return board.p1_bowl_pos[index]
    elif type == 'bowl' and player == 'p2':
        return board.p2_bowl_pos[index]
    elif type == 'goal' and player == 'p1':
        return board.p1_goal_pos
    else:
        return board.p2_goal_pos
    
def bowl_radius(board, type):
    if type == 'bowl':
        return board.bowl_diameter/2
    else:
        return board.goal_width/2
    
def rand_point(pos, range):
    # random pos in circle with center pos and radius range
    omega = 2 * math.pi * random.random()
    radius = range * random.random()
    x_pos = radius * math.cos(omega) + pos[0]
    y_pos = radius * math.sin(omega) + pos[1]
    return (x_pos, y_pos)



def move_to_bowl(board, type, player, index, stone):
    center = bowl_center(board, type, player, index)
    radius = bowl_radius(board, type) / math.sqrt(2)
    pos = rand_point(center, radius)
    stone.jump_to(pos)

def capture_bowl(board, bowl, player):
    (t, p, i) = bowl
    stones = board.state['bowl'][p][i]
    board.state['bowl'][p][i] = []
    for stone in stones:
        move_to_bowl(board, 'goal', player, -1, stone)
        board.state['goal'][p].append(stone)
    return board



def drop_stone(board, type, player, index):
    # drop one moving stone in bowl (type, player, index) instantaneously
    last = board.state['moving'][-1]
    board.state['moving'] = board.state['moving'][:-1]
    center = bowl_center(board, type, player, index)
    radius = bowl_radius(board, type) / math.sqrt(2)
    pos = rand_point(center, radius)
    last.jump_to(pos)
    if type == 'bowl':
        board.state[type][player][index].append(last)
    else:
        board.state[type][player].append(last)
    # if last stone
    if len(board.state['moving']) == 0:
        # if in empty bowl, capture
        if type=='bowl' and player==board.turn: 
            if len(board.state[type][player][index])==1:
                board = capture_bowl(board, (type, 'p1', index), board.turn)
                board = capture_bowl(board, (type, 'p2', index), board.turn)
        # if not in goal, change turn
        if type=='bowl':
            board.turn = 'p1' if board.turn=='p2' else 'p2'
        if not any(board.state['bowl']['p1']):
            for i in range(6):
                board = capture_bowl(board, ('bowl', 'p2', i), 'p2')
        elif not any(board.state['bowl']['p2']):
            for i in range(6):
                board = capture_bowl(board, ('bowl', 'p1', i), 'p1')
    return board


def next_bowl(board, type, player, index):
    if type == 'bowl' and player == 'p2' and index > 0:
        index -= 1
    elif type == 'bowl' and player == 'p2' and index == 0 and board.turn=='p1':
        player = 'p1'
    elif type == 'bowl' and player == 'p2':
        type = 'goal'
    elif type == 'bowl' and player == 'p1' and index < 5:
        index +=1
    elif type == 'bowl' and player == 'p1' and index == 5 and board.turn=='p2':
        player = 'p2'
    elif type == 'bowl' and player == 'p1':
        type = 'goal'
    elif type == 'goal' and player == 'p2':
        type = 'bowl'
        player = 'p1'
        index = 0
    else:
        type = 'bowl'
        player = 'p2'
        index = 5
    return (type, player, index)
    



def distribute_stones(board, bowl):
    # move stones to next bowl and drop one in bowl
    (type, player, index) = bowl
    stones = board.state['moving']
    if type=='bowl' and ((player=='p2' and index>0) or (player=='p1' and index<5)):
        dir = -1 if player=='p2' else 1
        offset = (board.bowl_diameter + board.hor_offset)*dir
        x_offset = offset
        y_offset = 0
    elif type=='bowl' and (player=='p2' and index==0) and board.turn=='p1':
        x_offset = 0
        y_offset = (board.bowl_diameter + board.ver_offset)
    elif type=='bowl' and (player=='p1' and index==5) and board.turn=='p2':
        x_offset = 0
        y_offset = -(board.bowl_diameter + board.ver_offset)
    else:
        x_cond = (type=='goal' and player=='p2') or (type=='bowl' and player=='p1')
        x_dir = 1 if x_cond else -1
        y_dir = 1 if (player=='p2') else -1
        x_offset = (board.bowl_diameter/2 + board.hor_offset + board.goal_width/2)*x_dir
        y_offset = (board.bowl_diameter + board.ver_offset)*y_dir/2
    for stone in stones:
        new_pos = (stone.pos[0] + x_offset, stone.pos[1] + y_offset)
        stone.jump_to(new_pos)
    (type, player, index) = next_bowl(board, type, player, index)
    board = drop_stone(board, type, player, index)
    # if last stone, check for capture
    return board, (type, player, index)
    


def intersects_bowl(board, pos, bowl):
    # whether pos intersects bowl
    (type, player, index) = bowl
    center = bowl_center(board, type, player, index)
    radius = bowl_radius(board, type)
    return np.linalg.norm(pos - center) < radius
    
def get_bowl_intersection(board, pos):
    # get the bowl that pos intersects with
    for i in range(len(board.p1_bowl_pos)):
        if intersects_bowl(board, pos, ('bowl', 'p1', i)):
            return ('bowl', 'p1', i)
    for i in range(len(board.p2_bowl_pos)):
        if intersects_bowl(board, pos, ('bowl', 'p2', i)):
            return ('bowl', 'p2', i)
    return None


def current_turn(board, bowl):
    (type, player, index) = bowl
    return board.turn==player
        


def get_player(bowl):
    return bowl[1]