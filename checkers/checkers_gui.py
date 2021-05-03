from checkers_game import *

import pygame

class Checkers_Gui():

	def __init__(self, cell_size = 80):
		self.cell_size = cell_size

		self.screen_width = cell_size * 11
		self.screen_height = cell_size * 11

		self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))

		self.color_background = (196,196,196)
		self.color_checkerboard_light = (64,196,64)
		self.color_checkerboard_dark = (64,128,64)
		self.color_piece_dark = (255,0,0)
		self.color_piece_light = (255,255,255)
		self.color_king = (255,255,0)

		self.update_screen = True
		self.selected_piece = None
		self.selected_piece_moves = []

		self.game = Checkers_Game()
		self.done = False

		self.draw()

	def get_input(self):

		mousePos = pygame.mouse.get_pos()

		row = int(-((mousePos[1] - self.cell_size*1.5) // self.cell_size + 1 - BOARD_LEN))
		col = int((mousePos[0] - self.cell_size*1.5) // self.cell_size)

		self.update_screen = False

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				self.done = 2

			elif event.type == pygame.MOUSEBUTTONDOWN:

				self.update_screen = True

				if row >= 0 and col >= 0 and row < BOARD_LEN and col < BOARD_LEN:
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

			initPos = moveInfo[0]
			prevPos = moveInfo[0]
			moves = moveInfo[1]

			for move in moves:
				x1 = prevPos[1] * self.cell_size + self.cell_size*2
				y1 = (BOARD_LEN-prevPos[0]-1) * self.cell_size + self.cell_size*2
				x2 = move[1] * self.cell_size + self.cell_size*2
				y2 = (BOARD_LEN-move[0]-1) * self.cell_size + self.cell_size*2

				pygame.draw.line(lineSurface,(0,0,0),(x1,y1),(x2,y2),width=5)

				prevPos = move

			self.draw_piece(self.game.board[initPos[0]][initPos[1]],moves[-1][0],moves[-1][1],True)

		self.screen.blit(lineSurface,(0,0))


	def draw_board(self):
		#Draw checkerboard pattern

		checkerboardSurface = pygame.Surface((self.screen_width,self.screen_height))

		pygame.draw.rect(checkerboardSurface,self.color_background,pygame.Rect(0,0,self.screen_width,self.screen_height))

		for yOffset in range(BOARD_LEN):
			for xOffset in range(BOARD_LEN):
				color = self.color_checkerboard_dark if ((yOffset+xOffset) % 2) else self.color_checkerboard_light

				x = xOffset * self.cell_size + self.cell_size*1.5
				y = yOffset * self.cell_size + self.cell_size*1.5

				pygame.draw.rect(checkerboardSurface,color,pygame.Rect(x,y,self.cell_size,self.cell_size))

		self.screen.blit(checkerboardSurface,(0,0))

		#Draw pieces

		for row in range(BOARD_LEN):
			for col in range(BOARD_LEN):
				if self.game.board[row][col]:
					self.draw_piece(self.game.board[row][col],row,col,False)

		self.draw_piece(self.game.current_player,8,3.5,False)

		if self.selected_piece:
			self.draw_moves()

	def draw(self):
		self.draw_board()

		pygame.display.flip()

	def update(self):

		if self.game.current_player != PLAYER_DARK:
			self.game.do_move(get_best_move(self.game))
			self.update_screen = True
		else:
			self.get_input()

		if self.update_screen:
			self.draw()
			self.done = self.game.get_state()
			self.update_screen = False