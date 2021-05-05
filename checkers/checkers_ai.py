from checkers_game import *
import math
import copy
import random

MAX_DEPTH = 7
SEARCH_NUM = 1000

current_node = None

EXPLORATION_PARAMETER = math.sqrt(2)

#MAX_DEPTH = 4

class MCTS_Node:
	def __init__(self,game,parent=None):
		self.game = game
		self.w = 0
		self.s = 0
		self.parent = parent
		self.children = []

		self.upperChildBound = len(self.game.get_moves())

	def is_leaf(self):
		if self.game.get_state():
			return True

		return False

	def ucb1(self):
		return self.w/self.s + EXPLORATION_PARAMETER * math.sqrt(math.log(self.parent.s)/self.s)

	def select(self):
		if self.is_leaf() or self.upperChildBound > len(self.children):
			return self
		else:
			bestNode = self.children[0]
			maxScore = -1

			for child in self.children:
				if child.ucb1() > maxScore:
					maxScore = child.ucb1()
					bestNode = child

			return bestNode.select()

	def expand(self):

		for move in self.game.get_moves():
			new = copy.deepcopy(self.game)
			new.do_move(move)
			notInChildren = True #This is a dirty variable name lol
			for child in self.children:
				if new == child.game:
					notInChildren = False
					break

			if notInChildren:
				newChild = MCTS_Node(new,parent=self)
				self.children.append(newChild)
				return newChild

	def simulate(self):

		new = copy.deepcopy(self.game)

		while not new.get_state():
			"""moves = new.get_moves()
			if moves:
				new.do_move(random.choice(moves))
			else:
				new.do_move(None)"""
			new.do_move(random.choice(new.get_moves()))

		return new.get_state()

	def backprop(self,winner):
		self.s += 1

		if winner == 2:
			self.w += 0.5
		elif winner == -self.game.current_player:
			self.w += 1

		if self.parent:
			self.parent.backprop(winner)

	def do_search(self):

		searchNode = self.select()
		winner = searchNode.game.get_state()

		if not winner:

			unexplored = searchNode.expand()
			winner = searchNode.simulate()
			searchNode = unexplored

		searchNode.backprop(winner)

	def pick_best_move_max(self):

		maxWinrate = -1
		bestChild = self.children[0]

		moves = self.game.get_moves()
		if len(moves) == 1:
			return moves[0], bestChild

		#print("Children:")
		for child in self.children:

			if child.w/child.s > maxWinrate:
				maxWinrate = child.w/child.s
				bestChild = child

		for move in moves:
			new = copy.deepcopy(self.game)
			new.do_move(move)

			if new == bestChild.game:
				return move, bestChild

	def pick_best_move_robust(self):

		global current_node

		maxSimulations = -1
		bestChild = self.children[0]

		#print("Children:")
		for child in self.children:

			if child.s > maxSimulations:
				maxSimulations = child.s
				bestChild = child

		for move in self.game.get_moves():
			new = copy.deepcopy(self.game)
			new.do_move(move)

			if new == bestChild.game:
				return move, bestChild

def get_random_move(game):

	moves = game.get_moves()

	if not moves:
		return None
	else:
		return random.choice(moves)

def get_best_move_minimax(game):
	moveScores = []

	moves = game.get_moves()

	if not moves:
		return None
	elif len(moves) == 1:
		return moves[0]
	else:
		for move in moves:
			new = copy.deepcopy(game)
			new.do_move(move)
			moveScores.append((minimax(new,game.current_player,1,-1),move))

		return max(moveScores)[1]

def get_best_move_alphabeta(game):
	moveScores = []

	moves = game.get_moves()

	if not moves:
		return None
	elif len(moves) == 1:
		return moves[0]
	else:
		for move in moves:
			new = copy.deepcopy(game)
			new.do_move(move)
			#moveScores.append((minimax(new,game.current_player,1,-1),move))
			moveScores.append((alphabeta(new,game.current_player,1,-1,-99999,99999),move))

		return max(moveScores)[1]

def get_best_move_mcts(game):

	global current_node

	if not current_node:
		current_node = MCTS_Node(game)
	else:
		for child in current_node.children:

			if child.game == game:
				current_node = child
				break

	for x in range(SEARCH_NUM):
		current_node.do_search()

	#print(current_node.children)
	#return node.pick_best_move_robust()

	bestMove, bestChild = current_node.pick_best_move_max()
	current_node = bestChild

	return bestMove

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

def alphabeta(game,player,depth,isMax,alpha,beta):

	if depth > MAX_DEPTH or game.get_state():
		return game.get_player_score(player)
	else:

		if isMax > 0:
			bestVal = -99999
		else:
			bestVal = 99999

		for move in game.get_moves():
			new = copy.deepcopy(game)
			new.do_move(move)

			score = alphabeta(new,player,depth+1,-isMax,alpha,beta)

			if isMax > 0:
				bestVal = max(score,bestVal)
				alpha = max(bestVal,alpha)

			else:
				bestVal = min(score,bestVal)
				beta = min(bestVal,beta)

			if alpha >= beta:
				break

		return bestVal