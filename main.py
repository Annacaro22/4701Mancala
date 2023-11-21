# Main program to run Mancala game and select playing options
import humanGame
import randomBot
print("Welcome to Mancala!")
print("Would you like to play against a human or a bot?")
choice = input("Enter 'human' or 'bot': ")
while choice != "human" and choice != "bot" and choice != "quit" and choice != "test":
    choice = input("Invalid input. Please try again: ")
if choice == "human":
    humanGame.runGame()
elif choice == "bot":
    print("Would you like to play against a random bot or a smart bot?")
    choice = input("Enter 'random' or 'smart': ")
    while choice != "ransom" and choice != "smart" and choice != "quit":
        choice = input("Invalid input. Please try again: ")
    if choice == "random":
        randomBot.runGame(True)
    elif choice == "smart":
        randomBot.runGame(False)
    elif choice == "quit":
        print("Goodbye!")
elif choice == "test":
    randomBot.runTest()
elif choice == "quit":
    print("Goodbye!")
    
