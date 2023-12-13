import pygame
from board import Board
from stone import Stone
from mechanics import *
from const import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
import humanGame
import time
import randomBot

def draw_game(screen, board):
    screen.fill(BACKGROUND_COLOR)
    board.draw(screen)
    pygame.display.flip()

# def update(board):
#     board.update()
    

def main():

    rand = False
    print("Welcome to Mancala!")
    print("Would you like to play against a human or a bot?")
    choice = input("Enter 'human' or 'bot': ")
    while choice != "human" and choice != "bot" and choice != "quit" and choice != "test":
        choice = input("Invalid input. Please try again: ")
    if choice == "human":
        game_type = 'human'
    elif choice == "bot":
        print("Would you like to play against a random bot or a smart bot?")
        choice = input("Enter 'random' or 'smart': ")
        while choice != "random" and choice != "smart" and choice != "quit":
            choice = input("Invalid input. Please try again: ")
        if choice == "random":
            game_type = 'random'
            rand = True
        elif choice == "smart":
            game_type = 'random'
            rand = False
        elif choice == "quit":
            print("Goodbye!")
    elif choice == "test":
        randomBot.runTest()
    elif choice == "quit":
        print("Goodbye!")


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
    done = False
    while running:
        clock.tick(10)
        if (board.turn=='p2' and game_type=='random') or not len(board.state['moving'])==0:
            pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        else:
            pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONUP and not done:
                pos = pygame.mouse.get_pos()
                bowl = get_bowl_intersection(board, pos) 
                if (len(board.state['moving'])==0):
                    if bowl is not None:
                        if is_valid(board, bowl):
                            board, bowl = start_moving(board, bowl)
                            if game_type == 'human':
                                if board.turn == 'p2':
                                    done = humanGame.run(5-bowl[2])
                                else:
                                    done = humanGame.run(bowl[2])
                            if game_type == 'random':
                                if not board.turn == 'p2':
                                    _, done = randomBot.run(rand, bowl[2])
                break
        if not len(board.state['moving'])==0:
            board, bowl = distribute_stones(board, bowl)
        if len(board.state['moving'])==0 and board.turn=='p2' and not done and game_type=='random':
            draw_game(screen, board)
            pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
            time.sleep(1)
            m, done = randomBot.run(rand, None)
            board, bowl = start_moving(board, ('bowl', 'p2', 5-m))
        draw_game(screen, board)
            

if __name__=="__main__":
    main()