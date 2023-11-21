import random

tab = "\t"
nl = "\n"

#setup of the game board-- 4 stones in each bowl, and empty goals
player1_bowls = [4, 4, 4, 4, 4, 4]
player2_bowls = [4, 4, 4, 4, 4, 4]
goal_p1 = [0]
goal_p2 = [0]

#current player whose turn it is
curr_player = [1]

game_end = [0] #0 means game should keep going, 1 means we've reached the end.

landed_in_goal = [0] #0 means we did not land in goal, 1 means we did land in goal (so current player gets to go again)


def run_a_round():
    print_gameboard()
    print("It is player " + str(curr_player[0]) + "'s turn. Enter player " + str(curr_player[0]) + " move: ", end = '')
    input_move = int(input())
    if (curr_player[0] == 1):
        make_a_move_p1(input_move)
    if (curr_player[0] == 2):
        make_a_move_p2(input_move)
    test_endcondition()




def print_gameboard():
    print(tab + str(player2_bowls[5]) + tab + str(player2_bowls[4]) + tab + str(player2_bowls[3]) + tab + str(player2_bowls[2]) + tab + str(player2_bowls[1]) + tab + str(player2_bowls[0]))
    print(str(goal_p2[0]) + tab + tab + tab + tab + tab + tab + tab + str(goal_p1[0]))
    print(tab + str(player1_bowls[0]) + tab + str(player1_bowls[1]) + tab + str(player1_bowls[2]) + tab + str(player1_bowls[3]) + tab + str(player1_bowls[4]) + tab + str(player1_bowls[5]))
    


def make_a_move_p1(chosen_move):
    num_stones = player1_bowls[chosen_move]
    player1_bowls[chosen_move] = 0
    for i in range(num_stones): #0 through num_stones-1
        j = i+1 #to make the loop essentially 1 through num_stones
        if ((chosen_move+j) % 13 <= 5): #if current bowl is on p1 side of the board
            player1_bowls[(chosen_move+j) % 13] = player1_bowls[(chosen_move+j) % 13] + 1
        else:
            if ((chosen_move+j) % 13 == 6): # if current bowl is p1 goal
                goal_p1[0] = goal_p1[0] + 1
            else:
                if((chosen_move+j) % 13 >= 7): #if current bowl is on p2 side of the board
                    player2_bowls[(chosen_move+j-7) % 13] = player2_bowls[(chosen_move+j-7) % 13] + 1
    end_bowl = (chosen_move + num_stones) % 13
    if (end_bowl == 6):
        landed_in_goal[0] = 1
    if ((end_bowl <= 5) and (player1_bowls[end_bowl] == 1)): #if you land in one of your own empty bowls
        goal_p1[0] = goal_p1[0] + player1_bowls[end_bowl] + player2_bowls[5 - end_bowl] #then you get to take the contents of that bowl and the opposite player's bowl
        player1_bowls[end_bowl] = 0
        player2_bowls[5 - end_bowl] = 0


def make_a_move_p2(chosen_move):
    num_stones = player2_bowls[chosen_move]
    player2_bowls[chosen_move] = 0
    for i in range(num_stones): #0 through num_stones-1
        j = i+1 #to make the loop essentially 1 through num_stones
        if ((chosen_move+j) % 13 <= 5): #if current bowl is on p2 side of the board
            player2_bowls[(chosen_move+j) % 13] = player2_bowls[(chosen_move+j) % 13] + 1
        else:
            if ((chosen_move+j) % 13 == 6): # if current bowl is p2 goal
                goal_p2[0] = goal_p2[0] + 1
            else:
                if((chosen_move+j) % 13 >= 7): #if current bowl is on p1 side of the board
                    player1_bowls[(chosen_move+j-7) % 13] = player1_bowls[(chosen_move+j-7) % 13] + 1
    end_bowl = (chosen_move + num_stones) % 13
    if (end_bowl == 6):
        landed_in_goal[0] = 1
    if ((end_bowl <= 5) and (player2_bowls[end_bowl] == 1)): #if you land in one of your own empty bowls
        goal_p2[0] = goal_p2[0] + player2_bowls[end_bowl] + player1_bowls[5 - end_bowl] #then you get to take the contents of that bowl and the opposite player's bowl
        player2_bowls[end_bowl] = 0
        player1_bowls[5 - end_bowl] = 0



def test_endcondition():
    total_p1_bowls = 0
    for i in player1_bowls:
        total_p1_bowls = total_p1_bowls + i
    total_p2_bowls = 0
    for i in player2_bowls:
        total_p2_bowls = total_p2_bowls + i
    if (total_p1_bowls == 0 or total_p2_bowls == 0): #one [or both] player[s] has run out of stones to play, game should end.
        goal_p1[0] = goal_p1[0] + total_p1_bowls
        goal_p2[0] = goal_p2[0] + total_p2_bowls
        for i in range(6):
            player1_bowls[i] = 0
            player2_bowls[i] = 0
        game_end[0] = 1
        end_of_game()


def end_of_game():
    print_gameboard()
    if goal_p1[0] > goal_p2[0] :
        print("Player 1 wins.")
    else:
        if goal_p1[0] < goal_p2[0]:
            print ("Player 2 wins.")
        else:
            print("It's a tie!")


def runGame():
    while (game_end[0] == 0):
        landed_in_goal[0] = 0
        run_a_round()
        if landed_in_goal[0] == 0:
            if (curr_player[0] == 1):
                curr_player[0] = 2
            else:
                if (curr_player[0] == 2):
                    curr_player[0] = 1

    print("Game is Finished.")


