import pygame
import time
from tetris_game import tetris_game
from tetris_gui import tetris_gui

def main():
	pygame.init()

	testGame = tetris_gui()
	clock = pygame.time.Clock()

	while not testGame.game.done:
		testGame.step()
		clock.tick(60)

if __name__=="__main__":
	main()