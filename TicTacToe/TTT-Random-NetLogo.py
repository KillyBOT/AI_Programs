# Random TTT mover for interface to NetLogo's TTT-UI

Usage = '''Usage:
python3 TTT-Random-NetLogo.py {result-filename} {board}
'''

import sys, random

Positions = ('Top-left','Top-center','Top-right','Middle-left','Middle-center',\
             'Middle-right','Bottom-left','Bottom-center','Bottom-right')

def main():
    if len(sys.argv) != 3:
        print(Usage)
        return
    outfile = sys.argv[1]
    board = sys.argv[2]
    poss = [i for i in range(9) if board[i] == '_']
    move = random.choice(poss)
    s = '%d\n' % move
    s += '%s\n' % Positions[move]
    s += "Don't know how many moves to anything...\n"
    print(s)
    f = open(outfile,'w')
    f.write(s)
    f.close()

main()

    
    
