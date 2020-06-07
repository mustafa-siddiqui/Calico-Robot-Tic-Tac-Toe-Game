# Robot Configuration
# Initialization
from Myro import *
initialize ("/dev/tty.Fluke2-09B6-Fluke2")

import random

# Coordinate system
acConvert = [[0,0], [1,0], [2,0], [0,1], [1,1], [2,1], [0,2], [1,2], [2,2]]

def ArrytoCoor (arry):
    global acConvert
    coor = [acConvert[arry-1][0],acConvert[arry-1][1]]
    return coor

def CoortoArry (coor = []):
    global acConvert
    a = 0
    for i in acConvert:
        if i is not coor:
            pass
        if i is coor:
            a = i + 1
    return a

# Movement - Fundamental

def step_forward():
    forward(1, 1.2)

def step_backward():
    backward(1, 1.2)

def turn_right():
    turnBy(-90)

def turn_around():
    turnBy(-180)

def turn_left():
    turnBy(90)

# Movement - Applied

def move_forward(a):
    i = 0
    if (a > 0):
        b = a
    elif (a < 0):
        b = 0 - a
    while (i < b):
        if (a > 0):
            step_forward()
        elif (a < 0):
            step_backward()
        i += 1
        
def rotate(a):
    global robot_direction
    if (a == 0):
        if (robot_direction == 90):
            turn_right()
        elif (robot_direction == 180):
            turn_around()
        elif (robot_direction == 270):
            turn_left()
    elif (a == 90):
        if (robot_direction == 0):
            turn_left()
        elif (robot_direction == 180):
            turn_right()
        elif (robot_direction == 270):
            turn_around()
    elif (a == 180):
        if (robot_direction == 0):
            turn_around()
        elif (robot_direction == 90):
            turn_left()
        elif (robot_direction == 270):
            turn_right()
    elif (a == 270):
        if (robot_direction == 0):
            turn_right()
        elif (robot_direction == 90):
            turn_around()
        elif (robot_direction == 180):
            turn_left()
    robot_direction = a

def move_horizontal(x):
    global robot_position
    rotate(0)
    if (x != robot_position[0]):
        x = x - robot_position[0]
        move_forward(x)
    elif (x == robot_position[0]):
        pass
        
def move_vertical(y):
    global robot_position
    if (y != robot_position[1]):
        rotate(90)
        y = y - robot_position[1]
        move_forward(y)
    elif (y == robot_position[1]):
        pass

def move_to_position(x, y): #!!
    global robot_position
    move_horizontal(x)
    move_vertical(y)
    robot_position = [x, y]
    return robot_position

# Scan current board if current board state is unknown

def scan(position):
    global theBoard
    if theBoard[position]== " ":
        forward(1,0.3)
        if getLine(0) == 1 or getLine(1) == 1:
            theBoard[position] = "X"
            backward(1,0.3)
            return position
        else:
            backward(1,0.3)
            return 0
    else:
         return 0

# Full board scan

def move_around_board():
    pathCoor = [[1,1],[2,1],[2,2],[1,2],[0,2],[0,1],[0,0],[1,0],[2,0]]
    pathArry = [5,6,9,8,7,4,1,2,3]
    playerMove = 0
    i = 0
    while i <= 8:
        if playerMove == 0:
            move_to_position(pathCoor[i][0],pathCoor[i][1])
            playerMove = scan(pathArry[i])
        else:
            move_to_position(1,1)
            rotate(0)
            return playerMove
        i = i + 1


# Game logic

'''
def whoGoesFirst():
     if random.randint(0, 1) == 0:
         return 'computer'
     else:
         return 'player'
'''

def playAgain():
     print('Do you want to play again? (yes or no)')
     return input().lower().startswith('y')

def makeMove(board, letter, move):
     board[move] = letter

def isWinner(bo, le):
     return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
     (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
     (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
     (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
     (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
     (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
     (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
     (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopy(board):
     dupeBoard = []
     for i in board:
         dupeBoard.append(i)
     return dupeBoard

def isSpaceFree(board, move):
    if board[move] == ' ':
        return True
    else:
        return False

def chooseRandomMoveFromList(board, movesList):
     possibleMoves = []
     for i in movesList:
         if isSpaceFree(board, i):
            possibleMoves.append(i)
     if len(possibleMoves) != 0:
         print(possibleMoves)
         return random.choice(possibleMoves)
     else:
         return None

def getComputerMove(board):
     for i in range(1, 10):
         copy = getBoardCopy(board)
         if isSpaceFree(copy, i):
             makeMove(copy, "O", i)
             if isWinner(copy, "O"):
                 return i

     for i in range(1, 10):
         copy = getBoardCopy(board)
         if isSpaceFree(copy, i):
             makeMove(copy, "X", i)
         if isWinner(copy, "X"):
                 return i

     move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
     if move != None:
         return move

     if isSpaceFree(board, 5):
         return 5

def isBoardFull(board):
     for i in range(1, 10):
         if isSpaceFree(board, i):
             return False
     return True

########
# MAIN #
########

print('Welcome to Tic Tac Toe!')

# Initial variables

robot_position = [1, 1]
robot_direction = 0
theBoard = [' '] * 10
turn = 'player'
print('The ' + turn + ' will go first.')
gameIsPlaying = True
Win, Tie, Lose = False, False, False
    
# Gameplay

while gameIsPlaying:
    if turn == 'player':
        input("Press Enter to continue...")
        move = move_around_board()
        move_to_position(1,1)
        rotate(0)
        if move == None:
            move = int(input("Oops! Something went wrong. Input the square you moved on."))
        
        print (theBoard)
        print (theBoard[7], theBoard[8], theBoard[9])
        print (theBoard[4], theBoard[5], theBoard[6])
        print (theBoard[1], theBoard[2], theBoard[3])

        computermove = makeMove(theBoard, "X", move)
            
        if isWinner(theBoard, "X"):
            Win = True
            print("You've Won!")
            gameIsPlaying = False
        else:
            if isBoardFull(theBoard):
                Tie = True
                print ("It's a Tie!")

            else:
                turn = 'computer'

    else:
        move = getComputerMove(theBoard)
        move_to_position(ArrytoCoor(move)[0],ArrytoCoor(move)[1])
        beep(0.5,1000)
        move_to_position(1, 1)
        print("done moving")
        computermove = makeMove(theBoard, "O", move)
        
        if isWinner(theBoard, "O"):
            Lose = True
            print("You've Lost!")
            gameIsPlaying = False

        elif isBoardFull(theBoard):
            Tie = True
            print ("Tie")
            gameIsPlaying = False
        else:
            turn = 'player'


