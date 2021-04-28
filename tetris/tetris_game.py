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

BUTTON_EMPTY = 0
BUTTON_PRESSED = 1
BUTTON_HELD = 2
BUTTON_RELEASED = 3

DROP_NORMAL = 0
DROP_SOFT = 1
DROP_HARD = 2

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

		self.ticks = 0
		self.ticks_DAS = 0
		self.input = {
		"left":BUTTON_EMPTY,
		"right":BUTTON_EMPTY,
		"rotate_clockwise":BUTTON_EMPTY,
		"rotate_counterclockwise":BUTTON_EMPTY,
		"soft_drop":BUTTON_EMPTY,
		"hard_drop":BUTTON_EMPTY,
		"hold":BUTTON_EMPTY
		}

		self.score = 0
		self.lines = 0
		self.level = level
		self.done = False

		self.current = randint(1,7)
		self.currentPos = [4,1]
		self.currentOffset = PIECE_OFFSET_DICT[self.current]
		self.dropType = 0 #1 for soft dropping, 2 for hard dropping
		self.canHold = True #If you already swapped what's being held with what you have, then you can't swap anymore
		
		self.touchedFloor = False
		self.lockTimeRequired = 30
		self.lockTime = 0 #Once the tetris piece touches the floor, wait some amount of ticks before locking
		self.auto_repeat_rate = 4
		self.DAS_time = self.auto_repeat_rate * 3
		self.get_appropriate_update_time()

		self.soft_drop_speed = 8

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

	def get_appropriate_update_time(self):
		if self.level <= 8:
			self.timeBetweenUpdates = 48 - 5*self.level
		elif self.level <= 18:
			self.timeBetweenUpdates = 6 - (self.level - 7)//3
		elif self.level <= 28:
			self.timeBetweenUpdates = 2
		else:
			self.timeBetweenUpdates = 1

		if self.dropType == 1:
			self.timeBetweenUpdates //= self.soft_drop_speed

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
		self.lines += rowsFilled
		self.score += multiplierDict[rowsFilled] * self.level

		#Update the level based on how many lines cleared
		#This is based on the original NES tetris' algorithm
		if self.lines >= (self.level * 10) + 10 or self.lines >= max(100, (self.level * 10) - 50):
			self.level += 1

	def get_input(self,buttons):
		self.input = buttons
		self.dropType = DROP_NORMAL

		if self.input["rotate_clockwise"] == BUTTON_PRESSED:
			self.rotate_current()
		if self.input["hold"] == BUTTON_PRESSED:
			self.swap_to_held()
		if self.input["hard_drop"] == BUTTON_PRESSED:
			self.dropType = DROP_HARD

		if self.input["soft_drop"]:
			self.dropType = DROP_SOFT

		if self.input["left"] and not self.input["right"]:

			if not self.ticks_DAS or (self.ticks_DAS > self.DAS_time and not (self.ticks_DAS % self.auto_repeat_rate)):
				self.move_current_left()
			self.ticks_DAS += 1

		elif self.input["right"] and not self.input["left"]:

			if not self.ticks_DAS or (self.ticks_DAS > self.DAS_time and not (self.ticks_DAS % self.auto_repeat_rate)):
				self.move_current_right()
			self.ticks_DAS += 1

		else:
			self.ticks_DAS = 0

	def move_current_down(self):
		self.currentPos[1] += 1

		if not self.check_if_current_valid(): #Did you touch the floor?
			self.currentPos[1] -= 1

			self.touchedFloor = True

			if self.lockTime >= self.lockTimeRequired: #Only lock once self.lockTimeRequired ticks have passed
				self.place_current()
				self.remove_filled_rows()
				self.lockTime = 0
				self.touchedFloor = False
		else:
			self.score += self.dropType

	def update(self):

		#print(self.currentPos)
		#print(self.currentOffset)

		self.get_appropriate_update_time()

		if self.touchedFloor:
			self.lockTime += 1

		if self.dropType == DROP_HARD:
			current = self.current
			while self.current == current:

				if self.touchedFloor:
					self.lockTime += 1
				self.move_current_down()

		elif self.ticks and not self.ticks % self.timeBetweenUpdates: #Should you move the piece down?
			self.move_current_down()

		self.ticks += 1 #Update one tick
