#By Max Brauer 

from random import randint

def make_board() :
    board = []
    for x in range(10):
        board.append(["-"] * 10)
    return board

def print_board(boards):
    print "  1 2 3 4 5 6 7 8 9 10"
    alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for row in range(10):
        print alpha[row] + " " + " ".join(boards[row])

def clean(ship, board):
    for row in range(10) :
        for col in range(10):
            if board[row][col] == ship :
                board[row][col] = "-" 

def make_ship(board, num, letter):
    ship = [randint(0, len(board) - 1), randint(0, len(board[0]) - 1)]
    dirction = randint(0,1)
    if dirction == 0:
        if ship[0] <= 10-num :
            for row in range(ship[0], ship[0]+num) :
                if board[row][ship[1]] == "-" :
                    board[row][ship[1]] = letter
                else:
                    clean(letter, board)
                    make_ship(board, num, letter)
                    break
        else :
            make_ship(board, num, letter)
    else :
        if ship[1] <= 10-num :
            for col in range(ship[1], ship[1]+num) :
                if board[ship[0]][col] == "-" :
                    board[ship[0]][col] = letter
                else :
                    clean(letter, board)
                    make_ship(board, num, letter)
                    break
        else :
            make_ship(board, num, letter)

def populate_board(board) :
    make_ship(board, 5, "5")
    make_ship(board, 4, "4")
    make_ship(board, 3, "3")
    make_ship(board, 3, "2")
    make_ship(board, 2, "1")

def if_ship_alive(ship, board) :
    for row in range(10) :
        for col in range(10):
            if board[row][col] == ship :
                return True
    return False 

def ship_status(board) :
    enemyfleet = {"1" : "Patrolboat", "2" : "Cruiser", "3" : "Destoryer", "4" : "Battleship", "5" : "Aircraft Carrier"}
    for ship in enemyfleet :
        if if_ship_alive(ship, board) :
            if board == computerboard :
                print "    Enemy %s is alive" %(enemyfleet[ship])
            else :
                print "    Your %s is alive" %(enemyfleet[ship])          

def user_input(command) :
    command = command.lower()
    global test_row
    global test_col
    if len(command) == 2 or len(command) == 3 :
        try :
            alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
            for letter in alpha :
                if command[:1] == letter :
                    test_row = alpha.index(command[:1])
                    test_col = int(command[1:]) - 1 
        except :
             user_input(raw_input("Command:"))
    elif command == "exit" or command == "quit" :
        global gamestate
        gamestate = False 
    elif command == "status" :
        print "Your Fleet Status is "
        ship_status(playerboard)
        print "Enemy Fleet Status is "
        ship_status(computerboard)
        user_input(raw_input("Command:"))
    elif command == "hacker" :
        cheater()
        user_input(raw_input("Command:"))
    elif command == "help" :
        print "Attack: Enter a letter and number such as 'G6'"
        print "'Status': Displays the status of the each player's fleet"
        print "'Exit': Ends game"
        print "'Quit': Ends game"
        user_input(raw_input("Command:"))
    else :
        print "Sorry, I don't understand your command. Try typing 'help' for help."
        user_input(raw_input("Command:"))

def display() :
    print "Player's Board"
    print_board(playerboard)
    print "Computer's Board"
    print_board(visiableboard)

def cheater() :
    print "This is the Enemy's Fleet, wipe them out!"
    print_board(computerboard)

def has_won(board) :
    count = 0
    for row in range(10) :
        for col in range(10) :
            if board[row][col] == "1" or board[row][col] == "2" or board[row][col] == "3" or board[row][col] == "4" or board[row][col] == "5" :
                return False
    return True 

def process_usermove(guess_row, guess_col) :
    if (guess_row < 0 or guess_row > 9) or (guess_col < 0 or guess_col > 9):
        print "That's not even in the ocean, Sailor!"
        user_input(raw_input("Command:"))
    else :
        global player_counter
        if computerboard[guess_row][guess_col] != "-":
            computerboard[guess_row][guess_col] = "-"
            visiableboard[guess_row][guess_col] = "X"
            global user_summary
            global enemy_summary
            user_summary = "You hit the Enemy!"
            if has_won(computerboard) :
                user_summary = "You Won!!"
                enemy_summary = ""
                global gamestate
                gamestate = False 
            else :  
                ship_status(computerboard)
            player_counter += 1
        else:
            if(visiableboard[guess_row][guess_col] == "X" or visiableboard[guess_row][guess_col] == "O"):
                user_summary = "You already fired there!"
            else:
                visiableboard[guess_row][guess_col] = "O"
                user_summary =  "You missed!"
                player_counter += 1

def enemymove() :
    if user_summary != "You Won!!" :
        global gus_row
        global gus_col
        global next_ship_attack
        global enemy_counter
        gus_row = randint(0, len(playerboard) - 1) 
        gus_col = randint(0, len(playerboard[0]) - 1)
        if next_ship_attack != -1 :
            findship(next_ship_attack, playerboard)
        if (gus_row < 0 or gus_row > 9) or (gus_col < 0 or gus_col > 9) :
            enemymove()
        elif playerboard[gus_row][gus_col] == "X" or playerboard[gus_row][gus_col] == "O":
            enemymove()
        else :
            if playerboard[gus_row][gus_col] != "-":
                next_ship_attack = playerboard[gus_row][gus_col]
                playerboard[gus_row][gus_col] = "X"
                global enemy_summary
                enemy_summary = "The Enemy hit your fleet!"
                if has_won(playerboard) :
                    enemy_summary = "You Lost!!"
                    global gamestate
                    gamestate = False 
            else:
                playerboard[gus_row][gus_col] = "O"
                enemy_summary = "The Enemy missed!"
            enemy_counter += 1

def findship(ship, board) :
    for row in range(10):
        for col in range(10) :
            if board[row][col] == ship :
                global gus_row
                global gus_col
                gus_row = row
                gus_col = col 
                global next_ship_attack 
                next_ship_attack = -1

playerboard = make_board()
computerboard = make_board()
visiableboard = make_board()

populate_board(playerboard)
populate_board(computerboard)

print "Let's play Battleship!"
display()

gamestate = True 
test_row = -1
test_col = -1
user_summary = ""
enemy_summary = ""
next_ship_attack = -1

player_counter = 0
enemy_counter = 0 

while gamestate :
    user_input(raw_input("Command:"))
    if not gamestate : 
        break
    if player_counter == enemy_counter :    
        enemymove()
        process_usermove(test_row, test_col)
    elif player_counter > enemy_counter :
        enemymove()
    else :
        process_usermove(test_row, test_col)
    display()  
    print user_summary 
    print enemy_summary
    user_summary = ""
    enemy_summary = ""
    test_col = -1
    test_row = -1 