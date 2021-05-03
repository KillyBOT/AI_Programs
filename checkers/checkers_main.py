from checkers_game import *
from checkers_gui import *
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

	gui = Checkers_Gui(player_white = PLAYER_AI)
	#gui.game.board[3][3] = -2
	#gui.game.board[6][2] = 0

	while not gui.done:

		gui.update()

		"""for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gui.done = 2"""

	gameOverText = "Draw!"
	if gui.game.get_state() == 1:
		gameOverText = "Red wins!"
	elif gui.game.get_state() == -1:
		gameOverText = "White wins!"

	print(gameOverText)


if __name__ == "__main__":
	main()