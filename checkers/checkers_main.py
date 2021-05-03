from checkers_game import *
from checkers_gui import Checkers_Gui
from copy import deepcopy

import pygame

def main():

	pygame.init()

	"""testGame = Checkers_Game(setup_pieces = False)
	testGame.board[1][5] = 1
	testGame.board[2][4] = -1
	testGame.board[4][4] = -2
	testGame.board[6][6] = -1
	testGame.board[6][4] = -1


	print(testGame)

	print(testGame.get_moves())

	testGame.do_move(testGame.get_moves()[1])

	print(testGame,testGame.get_player_score(1))"""

	gui = Checkers_Gui()
	#gui.game.board[3][3] = -2
	#gui.game.board[6][2] = 0

	while not gui.done:
		gui.update()

	print("{} wins!".format("White" if gui.game.get_state() == -1 else "Red"))


if __name__ == "__main__":
	main()