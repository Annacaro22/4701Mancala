import random
from random import seed
import copy

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

def gameSet():
    #setup of the game board-- 4 stones in each bowl, and empty goals
    player1_bowls = [4, 4, 4, 4, 4, 4]
    player2_bowls = [4, 4, 4, 4, 4, 4]
    goal_p1 = [0]
    goal_p2 = [0]

    #current player whose turn it is
    curr_player = [1]

    game_end = [0] #0 means game should keep going, 1 means we've reached the end.

    landed_in_goal = [0] #0 means we did not land in goal, 1 means we did land in goal (so current player gets to go again)
    return player1_bowls, player2_bowls, goal_p1, goal_p2, curr_player, game_end, landed_in_goal
#run a round of the game against the random bot
def run_a_random_round():
    print_gameboard()
    if (curr_player[0] == 1):
        input_move = p1_getinput()
        make_a_move_p1(input_move, player1_bowls, player2_bowls, goal_p1, goal_p2, landed_in_goal)
    if (curr_player[0] == 2):
        input_move2 = 20
        while (0 > input_move2 or input_move2 > 5 or player2_bowls[input_move2] == 0):
            input_move2 = random.randint(0,5)
        computerplayer_print(input_move2)
        make_a_move_p2(input_move2, player1_bowls, player2_bowls, goal_p1, goal_p2, landed_in_goal)
    test_endcondition()

#run a round of the game against the minimax bot
def run_a_smart_round():
    print_gameboard()
    if (curr_player[0] == 1):
        input_move1 = p1_getinput()
        make_a_move_p1(input_move1, player1_bowls, player2_bowls, goal_p1, goal_p2, landed_in_goal)
    if (curr_player[0] == 2):
        input_move2 = alphaRunner(player1_bowls, player2_bowls, goal_p1, goal_p2)
        make_a_move_p2(input_move2, player1_bowls, player2_bowls, goal_p1, goal_p2, landed_in_goal)
    test_endcondition()
    

def alphaRunner(player1_bowls, player2_bowls, goal_p1, goal_p2):
    v = float("-inf")
    move =  None
    for i in range(6):
        p1bowls = copy.copy(player1_bowls)
        p2bowls = copy.copy(player2_bowls)
        p1goal = copy.copy(goal_p1)
        p2goal = copy.copy(goal_p2)
        if p2bowls[i] != 0:
            val = alphabeta(float("-inf"), float("inf"), False, 0, p1bowls, p2bowls, p1goal, p2goal, [0])
            if val > v:
                v = val
                move = i

    return move

def p1_getinput():
    print("It is player 1's turn. Enter player " + str(curr_player[0]) + " move: ", end = '')
    input_move = input()
    if input_move == "quit":
        game_end[0] = 1
        print("Game ended.")
        end_of_game()
    else:
        input_move = int(input_move)
        while (0 > input_move or input_move > 5 or player1_bowls[input_move] == 0):
            print("Invalid input. Please try again: ", end = '')
            input_move = input()
            if input_move == "quit":
                game_end[0] = 1
                print("Game ended.")
                end_of_game()
            else:
                input_move = int(input_move)
    return input_move

def computerplayer_print(input_move2):
    print("It is (RandomBot) player 2's turn. Player 2 selects move " + str(input_move2))

def print_gameboard():
    print(tab + str(player2_bowls[5]) + tab + str(player2_bowls[4]) + tab + str(player2_bowls[3]) + tab + str(player2_bowls[2]) + tab + str(player2_bowls[1]) + tab + str(player2_bowls[0]))
    print(str(goal_p2[0]) + tab + tab + tab + tab + tab + tab + tab + str(goal_p1[0]))
    print(tab + str(player1_bowls[0]) + tab + str(player1_bowls[1]) + tab + str(player1_bowls[2]) + tab + str(player1_bowls[3]) + tab + str(player1_bowls[4]) + tab + str(player1_bowls[5]))
    


def make_a_move_p1(chosen_move, player1_bowls, player2_bowls, goal_p1, goal_p2, landed_in_goal):
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


def make_a_move_p2(chosen_move, player1_bowls, player2_bowls, goal_p1, goal_p2, landed_in_goal):
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

# returns the number of stones in the last third of the players bowls
def getHomeBowls(bowls):
    total = 0
    for i in range(len(bowls)//3):
        total = total + bowls[i]
    return total

# returns the index of the bowl furthest from home with stones in it
def furthestBin(bowls):
    far = 0
    for i in range(len(bowls)):
        if bowls[i] > 0:
            far = i
    return far

#returns player1's score
def getScore1():
    return goal_p1[0]

#returns player2's score
def getScore2():
    return goal_p2[0]

#returns difference in scores
def getScoreDiff(goal1, goal2):
    return goal2[0] - goal1[0]

def firstValid(bowls):
    for i in range(len(bowls)):
        if bowls[i] > 0:
            return i
    return 0

def steal(p1bowls, p2bowls):
    stealmax = 0
    for x in range(len(p2bowls)):
        if p2bowls[x] == 0 and p1bowls[x] != 0:
            for y in range(len(p2bowls)):
                if p2bowls[y] + y >= x:
                    stealmax = max(stealmax, p1bowls[x])
    return stealmax

def scoreHeuristic(p1bowls, p2bowls, p1goal, p2goal):
    #score2w*p2goal[0]  + scorediffw*(p2goal[0] - p1goal[0]) + score1w*p1goal[0] 
    score1w = -0.1
    score2w = 0.1
    scorediffw = 0.3
    farbinw = 0.2
    getbinw = 0.1
    stealw = 0.2
    return stealw * steal(p1bowls, p2bowls) + score2w*p2goal[0]  + scorediffw*(p2goal[0] - p1goal[0]) + score1w*p1goal[0]

def endChecker(p1bowls, p2bowls):
    total_p1_bowls = 0
    for i in p1bowls:
        total_p1_bowls = total_p1_bowls + i
    total_p2_bowls = 0
    for i in p2bowls:
        total_p2_bowls = total_p2_bowls + i
    if (total_p1_bowls == 0) or (total_p2_bowls == 0):
        return [1]
    else:
        return [0]
    
#alphabeta pruning for minimax
def alphabeta( alpha, beta, maximizingPlayer, depth, p1bowls, p2bowls, p1goal, p2goal, landed_in_goal):
    if depth == [1]:
        print(scoreHeuristic(p1bowls, p2bowls, p1goal, p2goal))
        return scoreHeuristic(p1bowls, p2bowls, p1goal, p2goal)
    
    if maximizingPlayer:
        v = float("-inf")
        for i in range(6):
            if p2bowls[i] > 0:
                make_a_move_p2(i, p1bowls, p2bowls, p1goal, p2goal, landed_in_goal)
                val = alphabeta(alpha, beta, False, endChecker(p1bowls, p2bowls), p1bowls, p2bowls, p1goal, p2goal, landed_in_goal)
                v = max(v, val)
                if v > beta:
                    break
                alpha = max(alpha, v)
                return v
    else:
        v = float("inf")
        for i in range(6):
            if p1bowls[i] > 0:
                make_a_move_p1(i, p1bowls, p2bowls, p1goal, p2goal, landed_in_goal)
                val = alphabeta(alpha, beta, True, endChecker(p1bowls, p2bowls), p1bowls, p2bowls, p1goal, p2goal, landed_in_goal)
                v = min(v, val)
                if v < alpha:
                    break
                beta = min(beta, v)
                return v




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


def runGame(rand):
    while (game_end[0] == 0):
        if rand: 
            run_a_random_round()
        else:
            run_a_smart_round()
        if landed_in_goal[0] == 0:
            if (curr_player[0] == 1):
                curr_player[0] = 2
            else:
                if (curr_player[0] == 2):
                    curr_player[0] = 1
        test_endcondition()  
    print("Game is Finished.")


def runTest():

    p1_goals = 0
    p2_goals = 0
    ties = 0
    for x in range(100): 
        player1_bowls, player2_bowls, goal_p1, goal_p2, curr_player, game_end, landed_in_goal = gameSet()  
        while (game_end[0] == 0):
            game_end = endChecker(player1_bowls, player2_bowls)
            if (curr_player[0] == 1):
                input_move1 = 20
                while (0 > input_move1 or input_move1 > 5 or player1_bowls[input_move1] == 0):
                    input_move1 = random.randint(0,5)
                make_a_move_p1(input_move1, player1_bowls, player2_bowls, goal_p1, goal_p2, landed_in_goal)
                game_end= endChecker(player1_bowls, player2_bowls)
            if (curr_player[0] == 2) and (game_end != [1]):
                input_move2 = alphaRunner(player1_bowls, player2_bowls, goal_p1, goal_p2)
                if input_move2 == None:
                    break
                make_a_move_p2(input_move2, player1_bowls, player2_bowls, goal_p1, goal_p2, landed_in_goal)
            if landed_in_goal[0] == 0:
                if (curr_player[0] == 1):
                    curr_player[0] = 2
                else:
                    if (curr_player[0] == 2):
                        curr_player[0] = 1
            game_end = endChecker(player1_bowls, player2_bowls)
        if goal_p1[0] > goal_p2[0] :
            p1_goals = p1_goals + 1
        elif goal_p1[0] < goal_p2[0]:
            p2_goals = p2_goals + 1
        else:
            ties = ties + 1
    print("Player 1 won " + str(p1_goals) + " times.")
    print("Player 2 won " + str(p2_goals) + " times.")
    print("There were " + str(ties) + " ties.")
            
        