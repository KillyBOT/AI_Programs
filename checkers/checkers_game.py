import random
import copy

PLAYER_DARK = 1
PLAYER_LIGHT = -1
BOARD_LEN = 8

PIECE_DARK = 1
PIECE_LIGHT = -1
PIECE_KING_DARK = 2
PIECE_KING_LIGHT = -2

MAX_DEPTH = 5

class Checkers_Game:
	def __init__(self, setup_pieces = True):

		self.board = []
		self.current_player = PLAYER_DARK
		self.captured_by_dark_num = 0
		self.captured_by_light_num = 0

		for row in range(BOARD_LEN):
			toAdd = []
			for col in range(BOARD_LEN):
				toAdd.append(0)

			self.board.append(toAdd)

		if setup_pieces:
			self.setup_pieces()

	def __str__(self):
		out = ""

		for row in range(BOARD_LEN-1,-1,-1):
			for col in range(BOARD_LEN):
				toPrint = " " if (row+col) % 2 else "#"
				if self.board[row][col] == PIECE_DARK:
					toPrint = "d"
				elif self.board[row][col] == PIECE_LIGHT:
					toPrint = "l"
				elif self.board[row][col] == PIECE_KING_DARK:
					toPrint = "D"
				elif self.board[row][col] == PIECE_KING_LIGHT:
					toPrint = "L"

				out += toPrint

			out += "\n"

		out += "Current player: " + ("Dark" if self.current_player == PLAYER_DARK else "Light") + "\n"

		return out

	def setup_pieces(self):
		for n in range(BOARD_LEN//2):
			self.board[0][2*n] = PIECE_DARK
			self.board[1][2*n+1] = PIECE_DARK
			self.board[2][2*n] = PIECE_DARK

			self.board[BOARD_LEN-1][2*n+1] = PIECE_LIGHT
			self.board[BOARD_LEN-2][2*n] = PIECE_LIGHT
			self.board[BOARD_LEN-3][2*n+1] = PIECE_LIGHT

	def __iter__(self):
		for row in range(BOARD_LEN):
			for col in range(BOARD_LEN):
				yield self.board[row][col]

	def get_piece_moves(self,row,col,alreadyHopped):
		if not self.board[row][col]:
			return []

		piece_moves = []
		piece_col = PLAYER_DARK if self.board[row][col] > 0 else PLAYER_LIGHT


		for rowOffset in range(-1,2,2):

			if self.board[row][col] == PIECE_DARK and rowOffset == -1:
				continue
			elif self.board[row][col] == PIECE_LIGHT and rowOffset == 1:
				continue

			for colOffset in range(-1,2,2):

				finalRow = row+rowOffset
				finalCol = col+colOffset

				if not alreadyHopped and finalRow >= 0 and finalRow < BOARD_LEN and finalCol >= 0 and finalCol < BOARD_LEN:
					if not self.board[finalRow][finalCol]:
						piece_moves.append( ((finalRow,finalCol),) )
						continue

				if finalRow > 0 and finalRow < BOARD_LEN-1 and finalCol > 0 and finalCol < BOARD_LEN-1:

					#print(self,row,col,finalRow,finalCol,self.board[finalRow][finalCol],self.board[finalRow+rowOffset][finalCol+colOffset])

					if self.board[finalRow][finalCol] and self.board[finalRow][finalCol]*piece_col < 0 and not self.board[finalRow+rowOffset][finalCol+colOffset]:
						#print("Jump")
						toAdd = ((finalRow + rowOffset, finalCol + colOffset),)

						self.board[finalRow + rowOffset][finalCol + colOffset] = self.board[row][col]
						nextMoves = self.get_piece_moves(finalRow + rowOffset, finalCol + colOffset, True)
						self.board[finalRow + rowOffset][finalCol + colOffset] = 0

						if nextMoves:
							for move in nextMoves:
								piece_moves.append(toAdd + move)
						else:
							piece_moves.append(toAdd)

				

		return piece_moves

	def get_moves(self):

		moves = []
		mustJump = False

		for row in range(BOARD_LEN):
			for col in range(BOARD_LEN):
				if self.current_player*self.board[row][col] > 0:
					for piece_move in self.get_piece_moves(row,col,False):
						moves.append(((row,col),piece_move))
						if not mustJump and (row-piece_move[-1][0])**2 > 1:
							mustJump = True

		if mustJump:
			moves = list(filter(lambda x: (x[0][0]-x[1][-1][0])**2 > 1 , moves))

		return moves

	def do_move(self,move_info):
		pos = move_info[0]
		moves = move_info[1]

		for move in moves:

			if abs(pos[0] - move[0]) > 1: #Did you do any captures?

				capturedPos = ((pos[0]+move[0])//2,(pos[1]+move[1])//2)
				captured = self.board[capturedPos[0]][capturedPos[1]]

				if captured > 0:
					self.captured_by_light_num += captured
				elif captured < 0:
					self.captured_by_dark_num -= captured

				self.board[capturedPos[0]][capturedPos[1]] = 0

			self.board[move[0]][move[1]] = self.board[pos[0]][pos[1]]
			self.board[pos[0]][pos[1]] = 0
			pos = move

		#Check if you should king the current piece
		#I don't think that it's possible to have another move after being kinged, so it should be fine to put it outside the for loop

		if self.board[pos[0]][pos[1]] == PIECE_DARK and pos[0] == BOARD_LEN-1:
			self.board[pos[0]][pos[1]] = PIECE_KING_DARK
		elif self.board[pos[0]][pos[1]] == PIECE_LIGHT and pos[0] == 0:
			self.board[pos[0]][pos[1]] = PIECE_KING_LIGHT

		self.current_player = -self.current_player

	def get_state(self):
		#0 if the game is still going
		#1 if dark won, -1 if light won

		hasDark = False
		hasLight = False

		for row in range(BOARD_LEN):
			for col in range(BOARD_LEN):
				if self.board[row][col] > 0:
					hasDark = True
				elif self.board[row][col] < 0:
					hasLight = True

				if hasDark and hasLight:
					return 0

		if hasDark and not hasLight:
			return PLAYER_DARK
		elif hasLight and not hasDark:
			return PLAYER_LIGHT
		else:
			return 0 #This should never happen

	def get_player_score(self,player):

		score = self.captured_by_dark_num - self.captured_by_light_num

		for row in range(BOARD_LEN):
			for col in range(BOARD_LEN):
				score += self.board[row][col]

		if player == PLAYER_LIGHT:
			score = -score

		return score

def get_best_move(game):
	moveScores = []

	for move in game.get_moves():
		new = copy.deepcopy(game)
		new.do_move(move)
		moveScores.append((minimax(new,game.current_player,1,-1),move))

	return max(moveScores)[1]

def minimax(game,player,depth,isMax):

	if depth > MAX_DEPTH or game.get_state():
		return game.get_player_score(player)
	else:

		moveScores = []

		for move in game.get_moves():
			new = copy.deepcopy(game)
			new.do_move(move)
			moveScores.append(minimax(new,player,depth+1,-isMax))

		if isMax > 0:
			return max(moveScores)
		else:
			return min(moveScores)


