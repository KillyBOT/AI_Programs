''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# layouts look like "_x_ox__o_"

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {} # this is a dictionary with key = a layout, and value = its corresponding BoardNode

class BoardNode:
	def __init__(self,layout):
		self.layout = layout
		self.endState = None # if this is a terminal board, endState == 'x' or 'o' for wins, of 'd' for draw, else None
		self.children = [] # all layouts that can be reached with a single move

	def print(self):
		print ('layout:',self.layout, 'endState:',self.endState)
		print ('children:',self.children)

def CreateAllBoards(layout,parent):

	global xWins, oWins, draws, notEnds

	# recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary

	boardNode = BoardNode(layout)

	#Check if the game is won

	hasZeros = False
	gameIsOver = False

	checkChildren = False

	for win in Wins:
		lineSum = 0
		for ind in win:
			if not layout[ind]:
				hasZeros = True
			lineSum += layout[ind]

		if lineSum == 3:
			boardNode.endState = 'x'
			break
		elif lineSum == -3:
			boardNode.endState = 'o'
			break

	if not hasZeros:
		boardNode.endState = 'd'

	if not boardNode.endState:

		#Find the current player

		currentPlayer = 0
		xNum = oNum = 0

		for ind in layout:
			if ind == 1:
				xNum += 1
			elif ind == -1:
				oNum += 1

		currentPlayer = 1 if xNum == oNum else -1

		#Create all children

		for ind in range(9):
			if not layout[ind]:
				newLayout = list(layout)[:]
				newLayout[ind] = currentPlayer
				newLayout = tuple(newLayout)

				CreateAllBoards(newLayout,layout)
				boardNode.children.append(newLayout)


	AllBoards[layout] = boardNode

def main():
	CreateAllBoards((0,0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0,0))

	xWins = oWins = draws = intermediate = 0

	for board in AllBoards.keys():
		hasZeros = False
		gameIsOver = False

		for win in Wins:
			lineSum = 0
			for ind in win:
				if not board[ind]:
					hasZeros = True
				lineSum += board[ind]

			if lineSum == 3:
				xWins += 1
				gameIsOver = True
				break
			elif lineSum == -3:
				oWins += 1
				gameIsOver = True
				break

		if not hasZeros and not gameIsOver:
			draws += 1
		elif not gameIsOver:
			intermediate += 1

	print(len(AllBoards),xWins,oWins,draws,intermediate)

if __name__ == "__main__":
	main()

