import pygame
from board import Board
from stone import Stone
from mechanics import *
from const import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from humanGame import run

def draw_game(screen, board):
    screen.fill(BACKGROUND_COLOR)
    board.draw(screen)
    pygame.display.flip()

# def update(board):
#     board.update()
    

def main():
  
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # set background color
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()

    # initialize board
    board = Board()
    animation_state = None

    running = True
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                bowl = get_bowl_intersection(board, pos) 
                if (len(board.state['moving'])==0):
                    if bowl is not None:
                        if current_turn(board, bowl):
                            board, bowl = start_moving(board, bowl)
                            if board.turn == 'p2':
                                test = run(5-bowl[2])
                            else:
                                test = run(bowl[2])
                            if not test:
                                 print(board.state)
        if not len(board.state['moving'])==0:
            board, bowl = distribute_stones(board, bowl)
        draw_game(screen, board)
        

if __name__=="__main__":
    main()