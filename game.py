import pygame
from board import Board
from stone import Stone
from mechanics import *
from const import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR

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

    turn = 'p1'

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                bowl = get_bowl_intersection(board, pos) 
                if bowl is not None:
                    # capture_bowl(board, bowl, 'p1')
                    board, bowl = start_moving(board, bowl)
        if not len(board.state['moving'])==0:
            board, bowl = distribute_stones(board, bowl)
        # update game state/positions
        # update(board)
        # draw game state
        draw_game(screen, board)
        




if __name__=="__main__":
    main()