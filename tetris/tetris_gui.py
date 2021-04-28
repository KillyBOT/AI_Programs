import pygame
from tetris_game import tetris_game, GAME_HEIGHT, GAME_WIDTH, PIECE_OFFSET_DICT

COLOR_ID_DICT = {
	1:(0,255,255),
	2:(255,255,0),
	3:(255,0,255),
	4:(0,0,255),
	5:(255,128,0),
	6:(0,255,0),
	7:(255,0,0),
	8:(224,224,224) #Ghost piece
}

CELL_LENGTH = 40
BORDER_PADDING = CELL_LENGTH//4
PIECE_PADDING = CELL_LENGTH//8

SCREEN_WIDTH = CELL_LENGTH * int((GAME_WIDTH * 1.5)) + BORDER_PADDING
SCREEN_HEIGHT = (CELL_LENGTH * GAME_HEIGHT) + BORDER_PADDING*2

DAS_TIME = 15
AUTO_REPEAT_RATE = 5

FONT_SIZE = 36

def draw_good_border_rect(surface,color,x,y,width,height,padding):
	pygame.draw.rect(surface,color,pygame.Rect(x-padding,y-padding,width+padding*2,padding))
	pygame.draw.rect(surface,color,pygame.Rect(x-padding,y-padding,padding,height+padding*2))
	pygame.draw.rect(surface,color,pygame.Rect(x+width,y-padding,padding,height+padding*2))
	pygame.draw.rect(surface,color,pygame.Rect(x,y+height,width,padding))

def draw_piece(surface,color,x,y):
	pygame.draw.rect(surface,color,pygame.Rect(CELL_LENGTH * (5 + x), CELL_LENGTH * y + BORDER_PADDING, CELL_LENGTH, CELL_LENGTH))

	lightColor = darkColor = color
	lightColor = tuple(map(lambda x: 128 if x == 0 else x, lightColor))
	darkColor = tuple(map(lambda x: x//2, darkColor))

	pygame.draw.rect(surface,lightColor,pygame.Rect(CELL_LENGTH * (5+x), CELL_LENGTH*y + BORDER_PADDING, PIECE_PADDING, CELL_LENGTH))
	pygame.draw.rect(surface,darkColor,pygame.Rect(CELL_LENGTH * (5+x), CELL_LENGTH*(y+1) + BORDER_PADDING - PIECE_PADDING, CELL_LENGTH, PIECE_PADDING))
	pygame.draw.rect(surface,darkColor,pygame.Rect(CELL_LENGTH * (6+x) - PIECE_PADDING, CELL_LENGTH*y + BORDER_PADDING, PIECE_PADDING, CELL_LENGTH))
	pygame.draw.rect(surface,lightColor,pygame.Rect(CELL_LENGTH * (5+x), CELL_LENGTH*y + BORDER_PADDING, CELL_LENGTH, PIECE_PADDING))


class tetris_gui():
	def __init__(self, level=1):

		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		self.surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
		self.game = tetris_game(level)
		self.get_appropriate_update_time()
		
		self.pressed = {
		"left":0,
		"right":0,
		"rotate_clockwise":0,
		"rotate_counterclockwise":0,
		"soft_drop":0,
		"hard_drop":0,
		"hold":0
		}

		self.font = pygame.font.Font(None,36)

	def get_appropriate_update_time(self):
		if self.game.level <= 8:
			self.timeBetweenUpdates = 48 - 5*self.game.level
		elif self.game.level <= 18:
			self.timeBetweenUpdates = 6 - (self.game.level - 7)//3
		elif self.game.level <= 28:
			self.timeBetweenUpdates = 2
		else:
			self.timeBetweenUpdates = 1

	def get_input(self):

		"""self.game.dropType = 0

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				self.game.done = True

			elif event.type == pygame.KEYDOWN:

				if event.key == pygame.K_UP:
					self.game.rotate_current()

				if event.key == pygame.K_c:
					self.game.swap_to_held()

				if event.key == pygame.K_SPACE:
					self.game.dropType = 2

		keys = pygame.key.get_pressed()

		if keys[pygame.K_DOWN]:
			self.game.dropType = 1

		if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
			if not self.ticks_left or (self.ticks_left > DAS_TIME and not self.ticks_left % AUTO_REPEAT_RATE):
				self.game.move_current_left()

			self.ticks_left += 1
		else:
			self.ticks_left = 0

		if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
			if not self.ticks_right or (self.ticks_right >= DAS_TIME and not self.ticks_right % AUTO_REPEAT_RATE):
				self.game.move_current_right()

			self.ticks_right += 1
		else:
			self.ticks_right = 0"""

		finalButtons = {
			"left":0,
			"right":0,
			"rotate_clockwise":0,
			"rotate_counterclockwise":0,
			"soft_drop":0,
			"hard_drop":0,
			"hold":0
			}

		buttonMapping = {
			"left":pygame.K_LEFT,
			"right":pygame.K_RIGHT,
			"rotate_clockwise":pygame.K_UP,
			"rotate_counterclockwise":pygame.K_w,
			"soft_drop":pygame.K_DOWN,
			"hard_drop":pygame.K_SPACE,
			"hold":pygame.K_c
			}

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				self.game.done = True

		keys = pygame.key.get_pressed()

		for label,button in buttonMapping.items():

			if keys[button]:
				if not self.pressed[label]:
					finalButtons[label] = 1
					self.pressed[label] = 1
				else:
					finalButtons[label] = 2
			else:
				self.pressed[label] = 0

		self.game.get_input(finalButtons)


	def draw(self):

		#Draw background
		pygame.draw.rect(self.surface,(255,255,255),pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
		
		#Draw borders
		borderColor = (100,100,100)
		pygame.draw.rect(self.surface,borderColor,pygame.Rect(CELL_LENGTH*5-BORDER_PADDING,0,BORDER_PADDING,SCREEN_HEIGHT))
		
		draw_good_border_rect(self.surface,borderColor,BORDER_PADDING,BORDER_PADDING,SCREEN_WIDTH-BORDER_PADDING*2,SCREEN_HEIGHT-BORDER_PADDING*2,BORDER_PADDING)

		#Draw placed tetronimos
		pieceBorderColor = (255,255,255)
		for y in range(GAME_HEIGHT):
			for x in range(GAME_WIDTH):
				if self.game.matrix[x][y]:
					#pygame.draw.rect(self.surface,COLOR_ID_DICT[self.game.matrix[x][y]],pygame.Rect(CELL_LENGTH * (5 + x), CELL_LENGTH*y + BORDER_PADDING, CELL_LENGTH, CELL_LENGTH))
					draw_piece(self.surface,COLOR_ID_DICT[self.game.matrix[x][y]],x,y)
				else:
					color = (200,200,200) if (x+y)%2 else (255,255,255)
					pygame.draw.rect(self.surface,color,pygame.Rect(CELL_LENGTH * (5 + x), CELL_LENGTH * y + BORDER_PADDING, CELL_LENGTH, CELL_LENGTH))

		#Draw ghost tetronimo
		ghostPos = self.game.currentPos[:]
		ghostOffset = self.game.currentOffset
		canMoveDown = True

		while canMoveDown:
			for offset in ghostOffset:
				finalX = ghostPos[0] + offset[0]
				finalY = ghostPos[1] + offset[1]

				if finalX < 0 or finalX >= GAME_WIDTH or finalY < 0 or finalY >= GAME_HEIGHT or self.game.matrix[finalX][finalY]:
					canMoveDown = False
					break

			if canMoveDown:
				ghostPos[1] += 1
			
		ghostPos[1] -= 1
		for offset in ghostOffset:
			finalX = ghostPos[0] + offset[0]
			finalY = ghostPos[1] + offset[1]

			draw_piece(self.surface,COLOR_ID_DICT[8],finalX,finalY)

		#Draw current tetronimo

		for offset in self.game.currentOffset:
			finalX = self.game.currentPos[0] + offset[0]
			finalY = self.game.currentPos[1] + offset[1]

			draw_piece(self.surface,COLOR_ID_DICT[self.game.current],finalX,finalY)

		#Draw next and held tetronimos
		if self.game.next:
			for offset in PIECE_OFFSET_DICT[self.game.next]:
				finalX = -3.5 + offset[0]
				finalY = 12 + offset[1]

				draw_piece(self.surface,COLOR_ID_DICT[self.game.next],finalX,finalY)

		if self.game.held:
			for offset in PIECE_OFFSET_DICT[self.game.held]:
				finalX = -3.5 + offset[0]
				finalY = 7 + offset[1]

				draw_piece(self.surface,COLOR_ID_DICT[self.game.held],finalX,finalY)

		#Finally, blit all polygons to the screen
		self.screen.blit(self.surface,(0,0))

		#Draw score, lines, and level

		textColor = (0,0,0)

		scoreLabel = self.font.render("Score",True,textColor)
		scoreText = self.font.render("{}".format(self.game.score),True,textColor)
		
		linesLabel = self.font.render("Lines",True,textColor)
		linesText = self.font.render("{}".format(self.game.lines),True,textColor)
		
		levelLabel = self.font.render("Level".format(self.game.level),True,textColor)
		levelText = self.font.render("{}".format(self.game.level),True,textColor)

		nextLabel = self.font.render("Next",True,textColor)
		heldLabel = self.font.render("Held",True,textColor)

		self.screen.blit(scoreLabel,(BORDER_PADDING*2,BORDER_PADDING*2))
		self.screen.blit(scoreText,(BORDER_PADDING*2,BORDER_PADDING*2 + FONT_SIZE//1.5))

		self.screen.blit(linesLabel,(BORDER_PADDING*2,BORDER_PADDING*8))
		self.screen.blit(linesText,(BORDER_PADDING*2,BORDER_PADDING*8 + FONT_SIZE//1.5))

		self.screen.blit(levelLabel,(BORDER_PADDING*2,SCREEN_HEIGHT - BORDER_PADDING*4 - FONT_SIZE//1.5))
		self.screen.blit(levelText,(BORDER_PADDING*2,SCREEN_HEIGHT - BORDER_PADDING*4))

		self.screen.blit(heldLabel,(BORDER_PADDING*2,BORDER_PADDING + CELL_LENGTH * 5))
		self.screen.blit(nextLabel,(BORDER_PADDING*2,BORDER_PADDING + CELL_LENGTH * 10))

		pygame.display.flip()

	def step(self):
		self.get_input()

		self.game.update()

		self.draw() #Draw the screen