import sys, os
import random
import copy
import math
import pickle
import time

# 0 1 2
# 3 4 5
# 6 7 8

#This is lazy and crappy coding, but it's fine since there are only 9 squares
inds_to_check = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

board_rotations = ((0,2,8,6,0),(1,5,7,3,1))
board_flip = (0,2,3,5,6,8)

MAX_DEPTH = 9

MINMAX_MIN = -1
MINMAX_MAX = 1

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

	def load_from_tuple(self,tup):
		self.data = list(tup)

		xNum = 0
		oNum = 0

		for ind in self.data:
			if ind == 1:
				xNum += 1
			elif ind == 2:
				oNum += 1

		if xNum > oNum:
			self.currentPlayer = 2
		else:
			self.currentPlayer = 1

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

		hasAnyZeros = False

		for group in inds_to_check:
			hasZeros = False
			rowSum = 0
			for ind in group:
				val = self.data[ind]
				if not val:
					hasZeros = True
					hasAnyZeros = True
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

class MCTS_Node():

	def __init__(self,board,parent):
		self.board = board
		self.boardTuple = tuple(board)
		self.children = []
		self.parent = parent
		self.s = 0
		self.w = 0

	def is_leaf(self):
		if self.board.check_board_state():
			return True
		return False

	def ucb1(self):
		return self.w/self.s + math.sqrt(2) * math.sqrt(math.log(self.parent.s)/self.s)

	def select(self):

		if self.is_leaf() or len(self.children) < len(self.board.get_next_moves()):
			return self
		else:
			maxScore = -1
			bestChild = self.children[0]

			for child in self.children:
				if child.ucb1() > maxScore:
					bestNode = child

			return bestNode.select()

	def expand(self):

		board = copy.deepcopy(self.board)
		origBoardTuple = tuple(self.board)

		childBoards = []

		for child in self.children:
			childBoards.append(tuple(child.board))

		for move in self.board.get_next_moves():
			board.do_move(move)

			if tuple(board) not in childBoards:
				unexplored = MCTS_Node(board,self)
				self.children.append(unexplored)
				return unexplored

			board.load_from_tuple(origBoardTuple)

	def simulate(self):

		board = copy.deepcopy(self.board)

		while not board.check_board_state():
			board.do_move(random.choice(board.get_next_moves()))

		return board.check_board_state()

	def backprop(self,start,winner):

		current = start
		#print("Backpropagating...")

		while current != self.parent:

			#print(current.board,current.w,current.s)

			current.s += 1

			if winner < 3 and current.board.currentPlayer != winner:
				current.w += 1

			"""if winner == 3:
				current.w += 0.5
			elif current.board.currentPlayer != winner:
				current.w += 1"""

			current = current.parent

	def do_search(self):

		#print("Current board:")
		#print(self.board)

		searchNode = self.select()
		winner = searchNode.board.check_board_state()

		#print("Selected board:")
		#print(searchNode.board)

		if not winner:

			unexplored = searchNode.expand()

			winner = unexplored.simulate()

			searchNode = unexplored

		self.backprop(searchNode,winner)

	def pick_best_move_robust(self):

		#print("Picking best move...")

		#print("Current board")
		#print(self.board)

		maxSims = 0
		bestChild = self.children[0]

		#print("Children:")
		for child in self.children:

			#print(child.board)

			if child.s > maxSims:
				maxSims = child.s
				bestChild = child

		board = copy.deepcopy(self.board)

		for move in self.board.get_next_moves():
			board.do_move(move)
			if tuple(bestChild.board) == tuple(board):
				return move

			board = copy.deepcopy(self.board)

	def pick_best_move_max(self):
		maxWinrate = 0
		bestChild = self.children[0]

		#print("Children:")
		for child in self.children:

			#print(child.board)

			if child.w/child.s > maxWinrate:
				maxWinrate = child.w/child.s
				bestChild = child

		board = copy.deepcopy(self.board)

		for move in self.board.get_next_moves():
			board.do_move(move)
			if tuple(bestChild.board) == tuple(board):
				return move

			board = copy.deepcopy(self.board)

	def get_corresponding_child_node(self,board):
		if not self.children:
			print("Error: No children here! You should search more")
		for child in self.children:
			if tuple(board) == tuple(child.board):
				return child

	def get_topmost_node(self):
		if self.parent == 0:
			return self
		else:
			return self.parent.get_topmost_node()

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

		if tuple(current) not in seen:
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

def minmax(board,currentPlayer,depth,minmax_type):

	if board.check_board_state():

		if board.check_board_state() == 3:
			return 0
		elif board.check_board_state() == currentPlayer:
			return 1
		else:
			return -1

	else:

		moves = []
		for move in board.get_next_moves():
			new = copy.deepcopy(board)
			new.do_move(move)
			moves.append(minmax(new,currentPlayer,depth+1,-minmax_type))

		if minmax_type == MINMAX_MAX:
			return max(moves)
		else:
			return min(moves)

def get_best_move(board):

	moves = []

	for move in board.get_next_moves():
		new = copy.deepcopy(board)
		new.do_move(move)
		score = minmax(new,board.currentPlayer,1,MINMAX_MIN)
		moves.append((score,move))

	return max(moves)[1]

def main():

	"""gameNum, xWinNum, oWinNum, drawNum = get_game_num()
	print("Number of Tic Tac Toe games:")
	print(gameNum)
	print("X wins: {}\tO wins: {}\tDraws: {}".format(xWinNum,oWinNum,drawNum))
	print("Number of Tic Tac Toe boards:")
	print(get_board_num())
	print("Number of distinct Tic Tac Toe boards:")
	print(get_board_family_num())"""

	#AI playing against random player

	board = Board()

	while not board.check_board_state():		
		print("\nRandom turn:")
		print(board)
		board.do_move(random.choice(board.get_next_moves()))
		print(board)

		if board.check_board_state():
			break

		print("\nAI turn:")
		print(board)
		move = get_best_move(board)
		board.do_move(get_best_move(board))
		print(board)

	print(board)

	#Building Monte Carlo Tree
	#mcts_build_tree(Board())

	#AI playing against random player using MCTS

	"""board = Board()
	timeout_time = 5
	search_num = 300

	trial_num = 10000

	optimalMoveDict = {} #If you've already found the optimal move for this location, use this instead

	xWins = 0
	oWins = 0
	draws = 0

	for n in range(trial_num):

		board.load_from_tuple((0,0,0,0,0,0,0,0,0))

		while not board.check_board_state():
			#print("Random turn")
			#print(board)

			if tuple(board) not in optimalMoveDict:

				root = MCTS_Node(board,0)
				for x in range(search_num):
					root.do_search()

				optimalMoveDict[tuple(board)] = root.pick_best_move_max()

			board.do_move(optimalMoveDict[tuple(board)])

			if board.check_board_state():
				break

			#print("AI turn")
			#print(board)

			board.do_move(random.choice(board.get_next_moves()))



			
		print("Game " + str(n))
		print(board)
		if board.check_board_state() == 1:
			xWins += 1
		elif board.check_board_state() == 2:
			oWins += 1
		else:
			draws += 1

		print("X wins: {}\tO wins: {}\t Draws: {}\t Win percentage:{}".format(xWins,oWins,draws,xWins*100/(xWins+oWins+draws)))
	"""


if __name__ == "__main__":
	main()