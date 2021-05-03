from checkers_game import *
from checkers_ai import *
import time

import pygame

PLAYER_HUMAN = 0
PLAYER_AI_ALPHABETA = 1
PLAYER_AI_MCTS = 2
PLAYER_AI_RANDOM = 3

class Checkers_Gui():

	def __init__(self, cell_size = 80, player_dark = PLAYER_HUMAN, player_light = PLAYER_HUMAN, current_player = PLAYER_DARK):
		self.cell_size = cell_size

		self.screen_width = cell_size * 11
		self.screen_height = cell_size * 11

		self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
		pygame.display.set_caption("Checkers")

		self.color_background = (196,196,196)
		self.color_checkerboard_light = (64,196,64)
		self.color_checkerboard_dark = (64,128,64)
		self.color_checkerboard_last_move = (255,128,0)
		self.color_piece_dark = (255,0,0)
		self.color_piece_light = (255,255,255)
		self.color_king = (255,255,0)
		self.font_size = 36
		self.font = pygame.font.Font(None,self.font_size)

		self.update_screen = True
		self.selected_piece = None
		self.selected_piece_moves = []
		self.last_click_pos = None
		self.last_move = None

		self.game = Checkers_Game()
		self.player_type_dark = player_dark
		self.player_type_light = player_light
		self.done = False

		self.draw()

	def get_input(self):

		mousePos = pygame.mouse.get_pos()

		row = int(-((mousePos[1] - self.cell_size*1.5) // self.cell_size + 1 - BOARD_LEN))
		col = int((mousePos[0] - self.cell_size*1.5) // self.cell_size)

		self.update_screen = False

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				self.done = 3

			elif event.type == pygame.MOUSEBUTTONDOWN:

				self.update_screen = True

				if row >= 0 and col >= 0 and row < BOARD_LEN and col < BOARD_LEN:

					if self.last_click_pos and self.last_click_pos == (row,col):
						self.last_click_pos = None
					else:
						self.last_click_pos = (row,col)

					if not self.selected_piece and self.game.board[row][col]:
						self.selected_piece = (self.game.board[row][col],row,col)
						self.selected_piece_moves.clear()

						for move in self.game.get_moves():
							if move[0] == (row,col):
								self.selected_piece_moves.append(move)

						if not self.selected_piece_moves:
							self.selected_piece = None

					else:

						for move in self.selected_piece_moves:
							if (row,col) == move[1][-1]:
								self.game.do_move(move)
								self.last_move = move
								self.done = self.game.get_state()
								break

						self.selected_piece = None
						self.selected_piece_moves.clear()

	def draw_piece(self,piece_type,row,col,isGhost):

		x = col * self.cell_size + self.cell_size*1.5
		y = (BOARD_LEN-row-1) * self.cell_size + self.cell_size*1.5

		pieceColor = self.color_piece_dark if piece_type > 0 else self.color_piece_light

		pieceSurface = pygame.Surface((self.cell_size,self.cell_size),pygame.SRCALPHA)

		if isGhost:
			pieceSurface.set_alpha(128)

		pieceRadiusOuter = (self.cell_size / 2) * 0.80
		pieceRadiusInner = (self.cell_size / 2) * 0.75
		pieceRadiusKing = (self.cell_size / 2) * 0.5

		if piece_type ** 2 == 4: #Draw king piece
			pygame.draw.circle(pieceSurface,(0,0,0),(self.cell_size/2,self.cell_size/2),pieceRadiusOuter)
			pygame.draw.circle(pieceSurface,self.color_king,(self.cell_size/2,self.cell_size/2),pieceRadiusInner)
			pygame.draw.circle(pieceSurface,pieceColor,(self.cell_size/2,self.cell_size/2),pieceRadiusKing)

		else:
			pygame.draw.circle(pieceSurface,(0,0,0),(self.cell_size/2,self.cell_size/2),pieceRadiusOuter)
			pygame.draw.circle(pieceSurface,pieceColor,(self.cell_size/2,self.cell_size/2),pieceRadiusInner)

		self.screen.blit(pieceSurface,(x,y))

	def draw_moves(self):

		lineSurface = pygame.Surface((self.screen_width,self.screen_height),pygame.SRCALPHA)

		for moveInfo in self.selected_piece_moves:
			self.draw_move(moveInfo)

		if self.last_move:
			#self.draw_piece(self.game.board[self.last_move[1][-1][0]][self.last_move[1][-1][1]], self.last_move[0][0], self.last_move[0][1], True)
			self.draw_move(self.last_move,should_draw_piece = False)
			

	def draw_move(self,move_info,should_draw_piece = True):
		lineSurface = pygame.Surface((self.screen_width,self.screen_height),pygame.SRCALPHA)
		initPos = move_info[0]
		prevPos = move_info[0]
		moves = move_info[1]

		for move in moves:
			x1 = prevPos[1] * self.cell_size + self.cell_size*2
			y1 = (BOARD_LEN-prevPos[0]-1) * self.cell_size + self.cell_size*2
			x2 = move[1] * self.cell_size + self.cell_size*2
			y2 = (BOARD_LEN-move[0]-1) * self.cell_size + self.cell_size*2

			pygame.draw.line(lineSurface,(0,0,0),(x1,y1),(x2,y2),width=5)

			prevPos = move

		if should_draw_piece:
			self.draw_piece(self.game.board[initPos[0]][initPos[1]],moves[-1][0],moves[-1][1],True)
		self.screen.blit(lineSurface,(0,0))



	def draw(self):
		#Draw checkerboard pattern

		checkerboardSurface = pygame.Surface((self.screen_width,self.screen_height))

		pygame.draw.rect(checkerboardSurface,self.color_background,pygame.Rect(0,0,self.screen_width,self.screen_height))

		for yOffset in range(BOARD_LEN):
			for xOffset in range(BOARD_LEN):
				color = self.color_checkerboard_dark if ((yOffset+xOffset) % 2) else self.color_checkerboard_light

				x = xOffset * self.cell_size + self.cell_size*1.5
				y = yOffset * self.cell_size + self.cell_size*1.5

				pygame.draw.rect(checkerboardSurface,color,pygame.Rect(x,y,self.cell_size,self.cell_size))

		if self.last_click_pos:
			x = self.last_click_pos[1] * self.cell_size + self.cell_size*1.5
			y = (BOARD_LEN-self.last_click_pos[0]-1) * self.cell_size + self.cell_size*1.5

			pygame.draw.rect(checkerboardSurface,self.color_checkerboard_last_move,pygame.Rect(x,y,self.cell_size,self.cell_size))

		self.screen.blit(checkerboardSurface,(0,0))


		#Draw text

		horTextList = ["a","b","c","d","e","f","g","h"]

		for offset in range(BOARD_LEN):
			
			vertX = self.cell_size * 1.25
			vertY = self.cell_size * (offset + 2) - self.font_size/4

			horX = self.cell_size * (offset + 2) - self.font_size/4
			horY = self.cell_size * 9.5

			verText = str(offset+1)
			horText = horTextList[offset]
			vertLabel = self.font.render(verText,True,(0,0,0))
			horLabel = self.font.render(horText,True,(0,0,0))

			self.screen.blit(vertLabel,(vertX,vertY))
			self.screen.blit(horLabel,(horX,horY))

		currentPlayerLabel = self.font.render("Current player:",True,(0,0,0))
		self.screen.blit(currentPlayerLabel, (self.screen_width/2 - self.font_size*2.5,self.font_size/2))

		darkScoreLabel = self.font.render("Red score: {}".format(self.game.get_player_score(PLAYER_DARK)),True,(0,0,0))
		self.screen.blit(darkScoreLabel, (self.cell_size * 2, self.cell_size*10))
		lightScoreLabel = self.font.render("White score: {}".format(self.game.get_player_score(PLAYER_LIGHT)),True,(0,0,0))
		self.screen.blit(lightScoreLabel, (self.cell_size * 2, self.cell_size*10 + self.font_size))

		#Draw pieces

		for row in range(BOARD_LEN):
			for col in range(BOARD_LEN):
				if self.game.board[row][col]:
					self.draw_piece(self.game.board[row][col],row,col,False)

		self.draw_piece(self.game.current_player,8,3.5,False)
		self.draw_moves()

		pygame.display.flip()

	def update(self):

		currentPlayerType = self.player_type_dark if self.game.current_player == PLAYER_DARK else self.player_type_light

		if currentPlayerType == PLAYER_HUMAN:
			self.get_input()
		else:
			if currentPlayerType == PLAYER_AI_ALPHABETA:
				move = get_best_move_alphabeta(self.game)
			elif currentPlayerType == PLAYER_AI_MCTS:
				move = get_best_move_mcts(self.game)
			elif currentPlayerType == PLAYER_AI_RANDOM:
				move = get_random_move(self.game)

			if move:
				self.last_click_pos = move[1][-1]
				self.last_move = move

			self.game.do_move(move)
			self.update_screen = True

		if self.update_screen:
			self.draw()
			self.done = self.game.get_state()
			self.update_screen = False