#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks/N-queens problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

import sys


# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    if Q == "nrook":
        return "\n".join([ " ".join([ "R" if col == 1 else "X" if col==2 else "_" for col in row ]) for row in board])
    elif Q == "nqueen":
        return "\n".join([ " ".join([ "Q" if col == 1 else "X" if col==2 else "_" for col in row ]) for row in board])
# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]


#checks for object in the leftmost column
#below 4 lines of code is discussed with Aravind Parappil
def find_left_col(board):
     for c in range(0,N):
        if(count_on_col(board,c) == 0):
            return c
            
# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

def successors2(board):
    tempList = [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N)]
    mainList=[]
    #collects a list of boards which don't have N+1 rooks and boards which don't have any rooks at all
    for i in tempList:
        if i !=board and count_pieces(i)<(N+1) and all( [ count_on_col(i, c) <= 1 for c in range(0, N) ] ) and all( [ count_on_row(i, r) <= 1 for r in range(0, N) ] ) :
            mainList.append(i)
    return mainList
    

def successors3(board):
    leftmost_col = find_left_col(board)
    #adds piece to leftmost column and not in "unavailable" positions
    tempList = [ add_piece(board, r, leftmost_col) for r in range(0, N) if[r,leftmost_col] not in cancel ]

    mainList=[]
    for i in tempList:
        #checks for no of pieces <= N and no duplicate boards are present in the list
        if i !=board and count_pieces(i)<(N+1) and all( [ count_on_col(i, c) <= 1 for c in range(0, N) ] ) and all( [ count_on_row(i, r) <= 1 for r in range(0, N) ] ) :
            mainList.append(i)
    #Check condition for queens
    if Q=="nqueen":
        diagonalList=[]
        for i in mainList:
            if diagonalCheck(i):
                diagonalList.append(i)
        return diagonalList
    else:
        return mainList
         
#queens
def diagonalCheck(board):
    x_coordinate=[]
    y_coordinate=[]
    #takes the coordinates of board where queen is present and stores it in a list of x and y coordinates
    for i in range(0,len(board)):
        for j in range(0,len(board)):
            if board[i][j]==1:
                x_coordinate.append(i)
                y_coordinate.append(j)
                

    #finds the absolute distance between two coordinates, if difference between x and y coordinates are same it means that two queens lie on the same diagonal, hence return False
    #logic below is referred from https://stackoverflow.com/questions/44082712/checking-diagonally-in-nqueen?rq=1
    for i in range(0,len(x_coordinate)):
        for j in range(0,len(y_coordinate)):
            if(i!=j):
                if abs(y_coordinate[i]-y_coordinate[j])==abs(x_coordinate[i]-x_coordinate[j]):
                    return False
                    break
            
    return True
                


# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
         
    return False

#Argument for rooks or queens
Q= sys.argv[1]
# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[2])
#no of unavailable positions
pos = int(sys.argv[3])

A=3
#lists for taking coordinates of unavailable positions
X_coordinates=[]
Y_coordinates=[]
#appends x and y coordinates of unavailable positions to X_coordinates list and Y_coordinates list
for i in range(0,pos):
    x=int(sys.argv[A+i+1])
    y=int(sys.argv[A+i+2])
    x-=1
    y-=1
    X_coordinates.append(x)
    Y_coordinates.append(y)
    A+=1

cancel=[]
#stores coordinates in one list
for i in range(0,len(X_coordinates)):
    c=[X_coordinates[i],Y_coordinates[i]]
    cancel.append(c)

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.

initial_board = [[0]*N]*N
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
solution = solve(initial_board)

for x in range(0,pos):
    solution [X_coordinates[x]][Y_coordinates[x]] =2
    
print (printable_board(solution) if solution else "Sorry, no solution found. :(")




