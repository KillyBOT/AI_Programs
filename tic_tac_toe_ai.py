import sys
import os
import random
import copy

# 0 1 2
# 3 4 5
# 6 7 8

#This is lazy and crappy coding, but it's fine since there are only 9 squares
inds_to_check = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

board_rotations = ((0,2,8,6,0),(1,5,7,3,1))
board_flip = (0,2,3,5,6,8)

class Board():
	def __init__(self):
		self.data = [0,0,0,0,0,0,0,0,0]
		self.currentPlayer = 1

	def __str__(self):

		out = ""
		val = 0

		for y in range(3):
			for x in range(3):
				#Why are there no switch statements?
				val = self.data[y*3+x]

				if val == 0:
					out += "_ "
				elif val == 1:
					out += "X "
				else:
					out += "O "

			out += "\n"

		out += "Current player: " + ("X\n" if self.currentPlayer == 1 else "O\n")

		return out

	def __iter__(self):
		for val in self.data:
			yield val

	def do_move(self,ind):
		if not self.data[ind]:
			self.data[ind] = self.currentPlayer
			self.currentPlayer = (1 if self.currentPlayer == 2 else 2)
			return (2 if self.currentPlayer == 1 else 1)
		else:
			return 0

	def check_board_state(self):
		#0 means there are still moves to be made
		#1 means player 1 won
		#2 means player 2 won
		#3 means there's a draw

		val = 0
		hasAnyZeros = 0

		for group in inds_to_check:
			hasZeros = 0
			rowSum = 0
			for ind in group:
				val = self.data[ind]
				if not val:
					hasZeros = 1
					hasAnyZeros = 1
				else:
					rowSum += val

			if not hasZeros and not rowSum % 3:
				return rowSum // 3

		return (0 if hasAnyZeros else 3)

	def get_next_moves(self):

		moves = []

		for ind in range(9):
			if not self.data[ind]:
				moves.append(ind)

		return moves

	def __eq__(self, other):

		for ind in range(9):
			if self.data[ind] != other.data[ind]:
				return False

		return True

	def get_rotated_board(self):

		newBoard = Board()

		for rotation in board_rotations:
			for ind in range(4):
				newBoard.data[rotation[ind+1]] = self.data[rotation[ind]]

		newBoard.data[4] = self.data[4]
		newBoard.currentPlayer = self.currentPlayer
		return newBoard

	def get_flipped_board(self):
		newBoard = Board()

		for ind in range(0,6,2):
			newBoard.data[board_flip[ind]] = self.data[board_flip[ind+1]]
			newBoard.data[board_flip[ind+1]] = self.data[board_flip[ind]]

		for ind in range(1,9,3):
			newBoard.data[ind] = self.data[ind]

		newBoard.currentPlayer = self.currentPlayer

		return newBoard

	def get_board_family(self):

		boardFamily = []
		newBoard = self

		for rotations in range(4):
			boardFamily.append(newBoard)
			newBoard = newBoard.get_rotated_board()

		newBoard = self.get_flipped_board()

		if newBoard != self:
			for rotations in range(4):
				boardFamily.append(newBoard)
				newBoard = newBoard.get_rotated_board()

		return boardFamily

def get_game_num():
	frontier = [Board()]
	gameNum = 0
	xWinNum = 0
	oWinNum = 0
	drawNum = 0

	while frontier:
		current = frontier.pop()
		currentBoardState = current.check_board_state()

		if currentBoardState:
			gameNum += 1
			if currentBoardState == 1:
				xWinNum += 1
			elif currentBoardState == 2:
				oWinNum += 1
			else:
				drawNum += 1
		else:
			for move in current.get_next_moves():
				new = copy.deepcopy(current)
				new.do_move(move)
				frontier.append(new)

	return gameNum, xWinNum, oWinNum, drawNum

def get_board_num():
	frontier = [Board()]
	seen = set()
	boardNum = 0

	while frontier:
		current = frontier.pop()

		if tuple(current) not in seen:

			boardNum += 1
			seen.add(tuple(current))

			if not current.check_board_state():
				for move in current.get_next_moves():
					new = copy.deepcopy(current)
					new.do_move(move)
					frontier.append(new)

	return boardNum

def get_board_family_num():
	frontier = [Board()]
	seen = set()
	familyNum = 0

	while frontier:
		current = frontier.pop()

		if(tuple(current) not in seen and not current.check_board_state()):
			familyNum += 1

			#Add all similar boards to the seen board set
			for board in current.get_board_family():
				seen.add(tuple(board))

			#Find all boards possible from here
			for move in current.get_next_moves():
				new = copy.deepcopy(current)
				new.do_move(move)
				frontier.append(new)

	return familyNum

def main():
	"""testBoard = Board()

	while not testBoard.check_board_state():
		boardFamily = testBoard.get_board_family()
		for board in boardFamily:
			print(board)

		testBoard.do_move(random.choice(testBoard.get_next_moves()))
		print("------------------------")

	print(testBoard)
	print(testBoard.check_board_state())"""

	gameNum, xWinNum, oWinNum, drawNum = get_game_num()
	print("Number of Tic Tac Toe games:")
	print(gameNum)
	print("X wins: {}\tO wins: {}\tDraws: {}".format(xWinNum,oWinNum,drawNum))
	print("Number of Tic Tac Toe boards:")
	print(get_board_num())
	print("Number of distinct Tic Tac Toe boards:")
	print(get_board_family_num())


if __name__ == "__main__":
	main()