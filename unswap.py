#! /usr/bin/python3

import sys

BOARD_LEN = 9

class Board():
    def __init__(self):
        self.data = []

        for y in range(BOARD_LEN):
            row = []
            for x in range(BOARD_LEN):
                row.append(-1)
            self.data.append(row)

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
            for x in range(BOARD_LEN):
                out = out + str(self.get_val_xy(x,y)) + " "
            out = out + '\n'

        return out

    """
    def get_cliques(self):

        
        Group areas:
        0 1 2
        3 4 5
        6 7 8
        

        cliques = dict()

        #Get rows and cols
        #I assume the boards will always be nxn
        for y in range(BOARD_LEN):
            rowClique = []
            colClique = []
            for x in range(BOARD_LEN):
                rowClique.append(self.get_val_xy(x,y))
                colClique.append(self.get_val_xy(y,x))

            cliques[(CLIQUE_TYPE.ROW,y)] = rowClique
            cliques[(CLIQUE_TYPE.COL,y)] = colClique

        #Get smaller groups

        for groupY in range(0,BOARD_LEN,BOARD_LEN//3):
            for groupX in range(0,BOARD_LEN,BOARD_LEN//3):
                clique = []

                for x in range(groupX,groupX+3):
                    for y in range(groupY,groupY+3):
                        clique.append(self.get_val_xy(x,y))

                cliques[(CLIQUE_TYPE.GROUP,groupY+groupX//3)] = clique

        return cliques"""
    def get_cliques(self):

        cliques = []

        for y in range(BOARD_LEN):
            rowClique = []
            colClique = []
            for x in range(BOARD_LEN):
                rowClique.append(self.get_val_xy(x,y))
                colClique.append(self.get_val_xy(y,x))

            cliques.append(rowClique)
            cliques.append(colClique)

        #Get smaller groups

        for groupY in range(0,BOARD_LEN,BOARD_LEN//3):
            for groupX in range(0,BOARD_LEN,BOARD_LEN//3):
                clique = []

                for x in range(groupX,groupX+3):
                    for y in range(groupY,groupY+3):
                        clique.append(self.get_val_xy(x,y))

                cliques.append(clique)

        return cliques

    def check_if_valid(self):

        for clique in self.get_cliques():
            if not check_if_clique_valid(clique):
                return False

        return True

def check_if_clique_valid(clique):
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


                if board.check_if_valid():
                    temp = board.get_val(i1)
                    board.set_val(i1,board.get_val(i2))
                    board.set_val(i2,temp)
                    return (i1,i2)
                temp = board.get_val(i1)
                board.set_val(i1,board.get_val(i2))
                board.set_val(i2,temp)

    return -1

def main():
    fIn = open(sys.argv[1],'r')
    fOut = open(sys.argv[2],'w')

    lines = fIn.read().split('\n')
    boards = []
   
    for lineNum in range(len(lines)):
        line = lines[lineNum]
        if line and (line[0] not in ["1","2","3","4","5","6","7","8","9"]):
            board = Board()
            for boardRow in range(BOARD_LEN):
                row = lines[lineNum+boardRow+1].split(',')
                for boardCol in range(BOARD_LEN):
                    board.set_val_xy(boardCol,boardRow,int(row[boardCol]))

            boards.append(board)
            lineNum += 9

    for board in boards:
        #print(board.check_if_valid())
        #print(board.get_cliques_with_ind())
        fOut.write(",".join([str(x) for x in find_swapped_vals(board)]))
        fOut.write("\n")
        #print(find_swapped_vals(board))
    fOut.write("\n")
   
    fIn.close()
    fOut.close()
   
if __name__ == "__main__":
    main()