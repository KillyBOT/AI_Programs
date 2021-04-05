#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 16:19:56 2018
@author: edwar
"""

import sys
import copy

sIn = None
out = None
startPoint = ""

unsolvedBoards = []
solvedBoards = []

cliques=[[0,1,2,3,4,5,6,7,8],
[9,10,11,12,13,14,15,16,17],
[18,19,20,21,22,23,24,25,26],
[27,28,29,30,31,32,33,34,35],
[36,37,38,39,40,41,42,43,44],
[45,46,47,48,49,50,51,52,53],
[54,55,56,57,58,59,60,61,62],
[63,64,65,66,67,68,69,70,71],
[72,73,74,75,76,77,78,79,80,],
[0,9,18,27,36,45,54,63,72],
[1,10,19,28,37,46,55,64,73],
[2,11,20,29,38,47,56,65,74],
[3,12,21,30,39,48,57,66,75],
[4,13,22,31,40,49,58,67,76],
[5,14,23,32,41,50,59,68,77],
[6,15,24,33,42,51,60,69,78],
[7,16,25,34,43,52,61,70,79],
[8,17,26,35,44,53,62,71,80],
[0,1,2,9,10,11,18,19,20],
[3,4,5,12,13,14,21,22,23],
[6,7,8,15,16,17,24,25,26],
[27,28,29,36,37,38,45,46,47],
[30,31,32,39,40,41,48,49,50],
[33,34,35,42,43,44,51,52,53],
[54,55,56,63,64,65,72,73,74],
[57,58,59,66,67,68,75,76,77],
[60,61,62,69,70,71,78,79,80]]

cliqueDict = {}
cliqueDictTuple = {}

for row in range(9):
    for column in range(9):
        cliqueDict[(row,column)] = []
        for clique in cliques:
            for num in clique:
                if (row * 9) + column == num:
                    cliqueDict[(row,column)].append(clique)

for num in range(81):
    cliqueDictTuple[num] = []
    for clique in cliques:
        for item in clique:
            if item == num:
                cliqueDictTuple[num].append(clique)

def printBoard(board):
    for row in range(9):
        for column in range(9):
            print(board[(row * 9) + column],end=" ")
        print("")
    print("")

def findBoard(rawIn, boardName):
    position = 0
    for line in rawIn:
        if line == boardName:
            break
        position += 1

    returnList = []
    for row in rawIn[position+1:position+10]:
        toInsert = []
        for num in row:
            if num != ",":
                if num == "_":
                    toInsert.append(0)
                else:
                    toInsert.append(int(num))
        returnList.append(toInsert)

    return returnList

def checkMove(board, num, row, column):

    if board[(row * 9) + column] != 0:
        return False

    for clique in cliqueDict[(row,column)]:
        for nums in clique:
            if num == board[nums]:
                return False
    return True

def boardToTuple(board):
    returnTup = []
    for row in board:
        for column in row:
            returnTup.append(column)

    return tuple(returnTup)

def tupToBoard(tup):
    returnBoard = []
    for row in range(9):
        toAdd = []
        for column in range(9):
            toAdd.append(tup[(row * 9)+column])
        returnBoard.append(toAdd)

    return returnBoard

def doMove(board, num, row, column):
    newBoard = list(board)
    newBoard[(row * 9) + column] = num
    return tuple(newBoard)

def findFirstEmpty(board):
    for num in range(len(board)):
        if board[num] == 0:
            return (num // 9, num % 9)

    return False

def findEmpty(board):
    emptySpots = []
    for num in range(len(board)):
        if board[num] == 0:
            emptySpots.append((num // 9, num % 9))

    return emptySpots

def findEmptyTuple(board):
    empties = []
    for num in range(len(board)):
        if board[num] == 0:
            empties.append(num)

    return empties

def anyForced(board):
    for empty in findEmpty(board):
        possibleNums = 0
        for num in range(1,10):
            if checkMove(board, num, empty[0], empty[1]):
                possibleNums += 1
        if possibleNums == 1:
            return True
    return False

def findMoves(board):
    moves = {}
    if findEmpty(board) != False:
        for empty in findEmpty(board):
            movesToAdd = []
            for num in range(1,10):
                if checkMove(board, num, empty[0], empty[1]):
                    movesToAdd.append(num)
            if len(movesToAdd) > 0:
                moves[empty] = movesToAdd

    return moves

def findMovesTuple(board):
    moves = {}
    empties = findEmptyTuple(board)
    if not empties:
        for empty in empties:
            movesToAdd = []
            for num in range(1,10):
                if checkMove(board, num, empty // 9, empty % 9):
                    movesToAdd.append(num)
            if len(movesToAdd) != 0:
                moves[empty] = movesToAdd
    return moves

def findMovesClique(board, clique):
    moves = {}
    for cliquePos in clique:
        toAppend = []
        if board[cliquePos] == 0:
            for num in range(1,10):
                if checkMove(board, num, cliquePos // 9, cliquePos % 9):
                    toAppend.append(num)
        if len(toAppend) > 0:
            moves[(cliquePos // 9, cliquePos % 9)] = toAppend

    #print(moves)
    for move in moves:
        if len(moves[move]) > 0:
            anyNakeds = False
            numOfNakeds = 0
            for otherMoves in moves:
                if moves[otherMoves] != moves[move] and set(moves[move]).issubset(set(moves[otherMoves])):
                    anyNakeds = True
                    #print(set(moves[move]), set(moves[otherMoves]), set(moves[move]).issubset(set(moves[otherMoves])))
                elif moves[otherMoves] == moves[move] and otherMoves != move:
                    #print(move, otherMoves, moves[move], moves[otherMoves])
                    numOfNakeds += 1
            if anyNakeds and numOfNakeds == 1:
                for otherMoves in moves:
                    if moves[otherMoves] != moves[move]:
                        moves[otherMoves] = list(set(moves[otherMoves]).difference(set(moves[move])))
                #print(clique, moves,end="\n\n")

    return moves

def findMovesCliques(board):
    empties = findEmpty(board)
    moves = {}
    for clique in cliques:
        moves.update(findMovesClique(board,clique))

    return moves

def checkValidity(board):
    for num in range(1,10):
        for row in range(9):
            for column in range(9):
                if board[(row * 9) + column] == 0:
                    return False
                for clique in cliqueDict[(row, column)]:
                    timesNumSeen = 0
                    for currentNum in clique:
                        if num == board[currentNum]:
                            timesNumSeen += 1
                    if timesNumSeen != 1:
                        return False
    return True

def findEmptyMoves(board, moves):
    retMoves = []
    for empty in findEmpty(board):
        if empty in moves:
            retMoves.append(empty)

    return retMoves

def solveBoard(board, solvedBoard):
    frontier = []
    currentBoard = board
    timesBacktracked = 0
    while checkValidity(currentBoard) == False:
        printBoard(currentBoard)
        moves = findMovesCliques(currentBoard)
        if len(moves) <= 0:
            timesBacktracked += 1
        else:
            while anyForced(currentBoard):
                for move in moves:
                    if len(moves[move]) == 1:
                        currentBoard = doMove(currentBoard, moves[move][0], move[0], move[1])
                moves = findMovesCliques(currentBoard)
            if checkValidity(currentBoard):
                break

            allEmpty = findEmptyMoves(currentBoard, moves)
            if len(allEmpty) > 0:
                spotToDo = min(allEmpty, key= lambda k: len(k))
                for move in moves[spotToDo]:
                    frontier.insert(0,doMove(currentBoard, move, spotToDo[0], spotToDo[1]))

        currentBoard = frontier.pop(0)
        print(len(frontier))
        #break
    print(timesBacktracked)
    return currentBoard

if __name__ == "__main__":
    if len(sys.argv) > 3:
        sIn = open(str(sys.argv[1]),"r")
        out = open(str(sys.argv[2]),"w")
        startPoint = str(sys.argv[3])
    else:
        sIn = open("Sudoku-boards.txt","r")
        out = open("s-1.txt","w")
        startPoint = "A2-1,Medium-NYTimes,unsolved"
    endPoint = startPoint.replace("unsolved","solved")

    sudokuInList = []
    for line in sIn.readlines():
        if line != "\n":
            sudokuInList.append(line.split("\n")[0])

    board = boardToTuple(findBoard(sudokuInList,startPoint))
    endBoard = boardToTuple(findBoard(sudokuInList,endPoint))
    solvedBoard = tupToBoard(solveBoard(board, endBoard))

    out.write(endPoint + "\n")
    for row in solvedBoard:
        rowString = []
        for num in row:
            rowString.append(str(num))
        out.write(",".join(rowString) + "\n")
    sIn.close()
out.close()
