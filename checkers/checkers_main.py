from checkers_game import *
from checkers_gui import *

import pygame
import time

def main():

	pygame.init()

	gui = Checkers_Gui(player_dark = PLAYER_AI_ALPHABETA, player_light = PLAYER_AI_MCTS)

	while not gui.done:
		gui.update()

	gameOverText = "Game exited"
	if gui.game.get_state() == 1:
		gameOverText = "Red wins!"
	elif gui.game.get_state() == -1:
		gameOverText = "White wins!"
	elif gui.game.get_state() == 2:
		gameOverText = "Draw!"

	print(gameOverText)

if __name__ == "__main__":
	main()