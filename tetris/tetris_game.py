from random import randint
from copy import deepcopy

PIECE_ID_DICT = {
	"I":1,
	"O":2,
	"T":3,
	"J":4,
	"L":5,
	"S":6,
	"Z":7
}

#Assume that 0,0 is the point of rotation
PIECE_OFFSET_DICT = {
	1:((-1,0),(0,0),(1,0),(2,0)), #I
	2:((0,0),(0,1),(1,0),(1,1)), #0
	3:((-1,0),(0,0),(0,1),(1,0)), #T
	4:((0,-1),(0,0),(0,1),(-1,1)), #J
	5:((0,-1),(0,0),(0,1),(1,1)), #L
	6:((-1,1),(0,1),(0,0),(1,0)), #S
	7:((-1,0),(0,0),(0,1),(1,1)) #Z
}

GAME_HEIGHT = 20
GAME_WIDTH = 10

def rotate_clockwise(pos):
	return (-pos[1],pos[0])

class tetris_game():
	def __init__(self, level=1):
		self.matrix = []
		for w in range(GAME_WIDTH):
			toAdd = []
			for h in range(GAME_HEIGHT):
				toAdd.append(0)
			self.matrix.append(toAdd)

		self.score = 0
		self.lines = 0
		self.level = level
		self.done = False

		self.current = randint(1,7)
		self.currentPos = [4,1]
		self.currentOffset = PIECE_OFFSET_DICT[self.current]
		self.dropType = 0 #1 for soft dropping, 2 for hard dropping
		self.canHold = True #If you already swapped what's being held with what you have, then you can't swap anymore

		#Sometimes, you can't rotate or move because there's something in the way, so you need to "push" the piece into the right place
		#self.currentPushedX = 0
		#self.currentPushedY = 0

		self.held = 0
		self.next = randint(1,7)
		while self.next == self.current:
			self.next = randint(1,7)

	def __str__(self):
		retStr = ""

		matrixToPrint = deepcopy(self.matrix)
		for offset in self.currentOffset:
			finalX = self.currentPos[0] + offset[0]
			finalY = self.currentPos[1] + offset[1]
			matrixToPrint[finalX][finalY] = self.current

		for h in range(GAME_HEIGHT):
			for w in range(GAME_WIDTH):
				retStr += "{}".format(matrixToPrint[w][h])

			retStr += "\n"
		retStr += "Score: {}\tLines: {}\tLevel: {}\n".format(self.score,self.lines,self.level)

		return retStr

	#Can the current piece be where it currently is?
	def check_if_current_valid(self):
		for offset in self.currentOffset:
			finalX = self.currentPos[0] + offset[0]
			finalY = self.currentPos[1] + offset[1]

			#First, check if inside the matrix
			if finalX < 0 or finalX >= GAME_WIDTH or finalY < 0 or finalY >= GAME_HEIGHT:
				return False

			#Then, check if inside a placed piece
			if self.matrix[finalX][finalY]:
				return False

		return True

	def get_new_current(self): #Get the next current piece

		#Get the new current piece
		self.current = self.next
		self.currentPos = [4,1]
		self.currentOffset = PIECE_OFFSET_DICT[self.current]

		#Can you even put the piece on the matrix?

		canPlace = True

		for offset in self.currentOffset:
			finalX = self.currentPos[0] + offset[0]
			finalY = self.currentPos[1] + offset[1]

			if self.matrix[finalX][finalY]:
				canPlace = False
				break

		if not canPlace: #If you can't, game over!
			self.done = True

		else:
			#Generate the next piece. Make sure you don't pick the same piece you picked last time!
			self.next = randint(1,7)
			while self.next == self.current:
				self.next = randint(1,7)

	def swap_to_held(self): #Swap to the held piece

		if self.canHold:
			self.canHold = False
			if not self.held:
				self.held = self.current
				self.get_new_current()

			else:
				oldNext = self.next

				self.next = self.held
				self.held = self.current
				self.get_new_current()
				self.next = oldNext

	def place_current(self): #Assume that setting the piece won't break any rules

		self.canHold = True

		for offset in self.currentOffset:
			finalX = self.currentPos[0] + offset[0]
			finalY = self.currentPos[1] + offset[1]

			self.matrix[finalX][finalY] = self.current

		self.get_new_current()

	def rotate_current(self):
		oldOffset = self.currentOffset
		canRotate = False

		#First, rotate clockwise
		self.currentOffset=tuple(map(rotate_clockwise,self.currentOffset))

		#Did the rotation put the piece in an invalid position? If so, move the piece to where it should be
		if not self.check_if_current_valid():
			#First, check if moving left or right fixes it
			#This is so inelegant that my eyes are bleeding

			self.currentPos[0] += 1
			if self.check_if_current_valid():
				canRotate = True
			else:
				self.currentPos[0] -= 2
				if self.check_if_current_valid():
					canRotate = True
				else:
					self.currentPos[0] += 1

					#Next, check if moving up or down fixes it

					self.currentPos[1] -= 1
					if self.check_if_current_valid():
						canRotate = True
					else:
						self.currentPos[1] += 2
						if self.check_if_current_valid():
							canRotate = True
						else:
							self.currentPos[1] -= 1

		else:
			canRotate = True

		#To avoid confusion, don't rotate O blocks
		if self.current == PIECE_ID_DICT["O"]:
			canRotate = False
		
		if not canRotate:
			self.currentOffset = oldOffset

	def move_current_left(self):

		self.currentPos[0] -= 1

		if not self.check_if_current_valid():
			self.currentPos[0] += 1

	def move_current_right(self):

		self.currentPos[0] += 1

		if not self.check_if_current_valid():
			self.currentPos[0] -= 1

	def remove_filled_rows(self):
		rowsFilled = 0
		multiplierDict = { #The multiplier for you score differs depending on how many lines you filled
			0:0,
			1:100,
			2:300,
			3:500,
			4:800
		}

		for y in range(GAME_HEIGHT):

			#First, check if there is an empty line
			hasEmpty = False

			for x in range(GAME_WIDTH):
				if not self.matrix[x][y]:
					hasEmpty = True
					break

			if not hasEmpty: #If there is a filled row...
				rowsFilled += 1

				#Move all the top rows down

				for tempY in range(y,0,-1):
					for x in range(GAME_WIDTH):
						self.matrix[x][tempY] = self.matrix[x][tempY-1]

				for x in range(GAME_WIDTH):
					self.matrix[x][0] = 0

		#Update the score and lines.
		self.lines+= rowsFilled
		self.score += multiplierDict[rowsFilled] * self.level

	def update(self):

		#print(self.currentPos)
		#print(self.currentOffset)

		#Check if moving the piece down will make the piece invalid

		self.currentPos[1] += 1

		if not self.check_if_current_valid():
			self.currentPos[1] -= 1
			self.place_current()
			self.remove_filled_rows()
		else:
			self.score += self.dropType

