from checkers_game import *
from checkers_gui import *

import pygame
import time

def main():

	pygame.init()

	gui = Checkers_Gui(player_dark = PLAYER_AI_MCTS, player_light = PLAYER_AI_RANDOM)

	while not gui.done:
		gui.update()

	gui.draw(draw_game_over="True")

	running = True

	while running:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

if __name__ == "__main__":
	main()