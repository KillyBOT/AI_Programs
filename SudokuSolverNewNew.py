#! /usr/bin/python3

import sys
import os
import copy
import time

BOARD_LEN = 9

#Hard coding should make things faster
CLIQUE_GROUPS=[[0,1,2,3,4,5,6,7,8],
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

gSeen = set()
gBacktracks = 0

#Again, more hardcoded values. I found these using a simple function.
VAL_CLIQUE_DICT = {0: [0, 9, 18], 1: [0, 10, 18], 2: [0, 11, 18], 3: [0, 12, 19], 4: [0, 13, 19], 5: [0, 14, 19], 6: [0, 15, 20], 7: [0, 16, 20], 8: [0, 17, 20], 9: [1, 9, 18], 10: [1, 10, 18], 11: [1, 11, 18], 12: [1, 12, 19], 13: [1, 13, 19], 14: [1, 14, 19], 15: [1, 15, 20], 16: [1, 16, 20], 17: [1, 17, 20], 18: [2, 9, 18], 19: [2, 10, 18], 20: [2, 11, 18], 21: [2, 12, 19], 22: [2, 13, 19], 23: [2, 14, 19], 24: [2, 15, 20], 25: [2, 16, 20], 26: [2, 17, 20], 27: [3, 9, 21], 28: [3, 10, 21], 29: [3, 11, 21], 30: [3, 12, 22], 31: [3, 13, 22], 32: [3, 14, 22], 33: [3, 15, 23], 34: [3, 16, 23], 35: [3, 17, 23], 36: [4, 9, 21], 37: [4, 10, 21], 38: [4, 11, 21], 39: [4, 12, 22], 40: [4, 13, 22], 41: [4, 14, 22], 42: [4, 15, 23], 43: [4, 16, 23], 44: [4, 17, 23], 45: [5, 9, 21], 46: [5, 10, 21], 47: [5, 11, 21], 48: [5, 12, 22], 49: [5, 13, 22], 50: [5, 14, 22], 51: [5, 15, 23], 52: [5, 16, 23], 53: [5, 17, 23], 54: [6, 9, 24], 55: [6, 10, 24], 56: [6, 11, 24], 57: [6, 12, 25], 58: [6, 13, 25], 59: [6, 14, 25], 60: [6, 15, 26], 61: [6, 16, 26], 62: [6, 17, 26], 63: [7, 9, 24], 64: [7, 10, 24], 65: [7, 11, 24], 66: [7, 12, 25], 67: [7, 13, 25], 68: [7, 14, 25], 69: [7, 15, 26], 70: [7, 16, 26], 71: [7, 17, 26], 72: [8, 9, 24], 73: [8, 10, 24], 74: [8, 11, 24], 75: [8, 12, 25], 76: [8, 13, 25], 77: [8, 14, 25], 78: [8, 15, 26], 79: [8, 16, 26], 80: [8, 17, 26]}

class Board():
    def __init__(self):
        self.data = []

        for y in range(BOARD_LEN):
            row = []
            for x in range(BOARD_LEN):
                row.append(0)
            self.data.append(row)

    def to_tuple(self):
        retTuple = []

        for ind in range(BOARD_LEN**2):
            retTuple.append(self.get_val(ind))

        return tuple(retTuple)

    def from_tuple(self,boardTuple):

        for ind in range(BOARD_LEN**2):
            self.set_val(ind,boardTuple[ind])

    def copy(self):
        newBoard = Board()

        for ind in range(BOARD_LEN**2):
            newBoard.set_val(ind,self.get_val(ind))

        return newBoard

    def get_val_xy(self,x,y):
        return self.data[y][x]

    def get_val(self,n):
        return self.data[n//BOARD_LEN][n%BOARD_LEN]

    def set_val_xy(self,x,y,val):
        self.data[y][x] = val

    def set_val(self,n,val):
        self.set_val_xy(n%BOARD_LEN,n//BOARD_LEN,val)

    def __str__(self):
        out = ""
        for y in range(BOARD_LEN):
            strRow = []
            for x in range(BOARD_LEN):
                strRow.append(str(self.get_val_xy(x,y)))
            out = out + ",".join(strRow)
            out = out + '\n'

        return out

    def get_cliques(self):

        cliques = []

        for cliqueGroup in CLIQUE_GROUPS:
            clique = []
            for val in cliqueGroup:
                clique.append(self.get_val(val))
            cliques.append(clique)

        return cliques

    def is_valid(self):

        for clique in self.get_cliques():
            if not clique_is_valid(clique):
                return False

        return True

    def is_move_valid(self,n,val):

        cliques = self.get_cliques()

        for relevantClique in VAL_CLIQUE_DICT[n]:
            if val in cliques[relevantClique]:
                return False

        return True


    def is_complete(self):

        for clique in self.get_cliques():
            if not clique_is_complete(clique):
                return False

        return True

    def get_moves(self):

        cliques = self.get_cliques()
        moves = []

        for n in range(BOARD_LEN**2):
            if self.get_val(n) == 0:
                for val in range(1,BOARD_LEN+1):
                    canAdd = True

                    for relevantClique in VAL_CLIQUE_DICT[n]:
                        if val in cliques[relevantClique]:
                            canAdd = False
                            break

                    if canAdd:
                        moves.append((n,val))

        return moves



    def get_moves_dict(self):

        cliques = self.get_cliques()
        moves = dict()
        
        for n in range(BOARD_LEN**2):
            if self.get_val(n) == 0:
                movesToAdd = []
                for val in range(1,BOARD_LEN+1):
                    canAdd = True

                    for relevantClique in VAL_CLIQUE_DICT[n]:
                        if val in cliques[relevantClique]:
                            canAdd = False
                            break

                    if canAdd:
                        movesToAdd.append(val)
                if movesToAdd:
                    moves[n] = movesToAdd
                    
        return moves
        

def clique_is_valid(clique):
    vals = set()
    for val in clique:
        if val != 0 and val in vals:
            return False
        else:
            vals.add(val)

    return True

def clique_is_complete(clique):
    sortedClique = clique[:]
    sortedClique.sort()

    sortedCliqueStr = ""
    for num in sortedClique:
        sortedCliqueStr += str(num)

    return sortedCliqueStr == "123456789"

#Assume the values are already swapped
def find_swapped_vals(board):

    seen = set()

    for i1 in range(BOARD_LEN**2):
        for i2 in range(BOARD_LEN**2):
            if i1 != i2 and (i1,i2) not in seen:
                seen.add((i2,i1))
                seen.add((i1,i2))


                temp = board.get_val(i1)
                board.set_val(i1,board.get_val(i2))
                board.set_val(i2,temp)


                if board.is_complete():
                    temp = board.get_val(i1)
                    board.set_val(i1,board.get_val(i2))
                    board.set_val(i2,temp)
                    return (i1,i2)
                temp = board.get_val(i1)
                board.set_val(i1,board.get_val(i2))
                board.set_val(i2,temp)

    return -1

def has_zeros(board):

    for ind in range(BOARD_LEN**2):
        if not board.get_val(ind):
            return True

    return False

def solve_board(board):

    frontier = []
    backtracks = 0
    seen = set()

    frontier.append(board)

    while len(frontier):
        current = frontier.pop()
        currentTuple = current.to_tuple()
        
        if currentTuple not in seen:
            seen.add(currentTuple)

            #os.system("clear")
            #print(current)
            #print(len(seen))

            if not has_zeros(current):
                print(backtracks)
                return current

            movesDict = current.get_moves_dict()
            #print(movesDict)
            #print(movesDict.items())

            if movesDict:

                hasSingleMove = True

                #First check if there are any easy moves
                
                while hasSingleMove:
                    hasSingleMove = False
                    for ind,moves in movesDict.items():
                        if len(moves) == 1:
                            current.set_val(ind,moves[0])
                            seen.add(current.to_tuple())
                            hasSingleMove = True
                            break

                    movesDict = current.get_moves_dict()

                if current.is_complete():
                    print(backtracks)
                    return current

                if not movesDict:
                    backtracks += 1
                    #print(backtracks)
                    #print(current)
                else:
                
                    #Then do the other moves
                    currentMoveSet = list(movesDict.items())[0]

                    for move in currentMoveSet[1]:
                        new = current.copy()
                        new.set_val(currentMoveSet[0],move)
                        frontier.append(new)



            else:
                backtracks += 1
                #print(backtracks)
                #print(current)
        #print(frontier)

    return None

def solve_board_recursive(board,moves):

    global gSeen
    global gBacktracks

    boardTuple = board.to_tuple()

    if not has_zeros(board):
        return board

    else:

        if boardTuple not in gSeen:
            gSeen.add(boardTuple)

            #print(board)

            if moves:

                retVal = None
                currentInd = moves[-1][0]
                movesToTry = []

                while moves and moves[-1][0] == currentInd:
                    movesToTry.append(moves.pop())

                for move in movesToTry:
                    new = board.copy()
                    if new.is_move_valid(move[0],move[1]):
                        new.set_val(move[0],move[1])
                        retVal = solve_board_recursive(new,moves[:])
                        if retVal != None:
                            return retVal

                gBacktracks += 1
                return None
            else:
                gBacktracks += 1
                return None
        else:
            return None


def main():

    fIn = open(sys.argv[1],'r')
    fOut = open(sys.argv[2],'w')
    boardName = sys.argv[3]

    lines = fIn.read().split('\n')
    board = Board()
    boardInitialized = False
   
    for lineNum in range(len(lines)):
        line = lines[lineNum]
        if line == boardName:
            for boardRow in range(BOARD_LEN):
                row = lines[lineNum+boardRow+1].split(',')
                for boardCol in range(BOARD_LEN):
                    if row[boardCol] != '0':
                        board.set_val_xy(boardCol,boardRow,int(row[boardCol]))
            boardInitialized = True
            break

    if boardInitialized:
        boardNameList = boardName.split(",")
        fOut.write(",".join([boardNameList[0],boardNameList[1],"solved"]))
        fOut.write("\n")
        #fOut.write(str(solve_board(board)))
        startTime = time.time_ns() / 1e6
        fOut.write(str(solve_board_recursive(board,board.get_moves())))
        endTime = time.time_ns() / 1e6
        print("Backtracks: " + str(gBacktracks))
        print("Time elapsed: " + str(endTime-startTime) + " ms")

        #print(board.is_complete())
        #print(board.get_cliques_with_ind())
        #fOut.write(",".join([str(x) for x in find_swapped_vals(board)]))
        #fOut.write("\n")
        #print(find_swapped_vals(board))
    else:
        print(boardName + " not found in " + sys.argv[1])
    #fOut.write("\n")

    #print(boardDict["A1-1"])
    #print(boardDict["A1-1"].get_cliques())
    #print(boardDict["A1-1"].get_moves_dict())
    #print(solve_board(boardDict["A2-1"]))
    #print(solve_board(boardDict["A3-1"]))
   
    fIn.close()
    fOut.close()
   
if __name__ == "__main__":
    main()