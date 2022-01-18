import pygame
import time
from random import randint

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, x, y, w, h, model, isCoinBrick):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.model = model
		self.isCoinBrick = isCoinBrick

	def collisionDetection(self, a, b):
		if a.x + a.w <= b.x:
			return False
		if a.x >= b.x + b.w:
			return False
		if a.y + a.h <= b.y:
			return False
		if a.y >= b.y + b.h:
			return False
		return True

	def isBrick(self):
		return False

	def _isCoinBrick(self):
		return self.isCoinBrick

	def update(self):
		pass


class Brick(Sprite):
	def __init__(self, x, y, w, h, model, isCoinBrick):
		super().__init__(x, y, w, h, model, isCoinBrick)
		self.model = model
		self.isCoinBrick = False
		self.coinQuantity = 5
		self.isCoinBrick = isCoinBrick
		self.brickImage = pygame.image.load("brick.png")
		self.brickCoinImage = pygame.image.load("block1.png")

	def draw(self, screen):
		if self.isCoinBrick == True:
			screen.blit(self.brickCoinImage, (self.x - self.model.mario.x + self.model.mario.startMario, self.y))
			self.isCoinBrick = True
		else:
			screen.blit(self.brickImage, (self.x - self.model.mario.x + self.model.mario.startMario, self.y))

	def isBrick(self):
		return True

	def update(self):
		pass

class Coin(Sprite):
	def __init__(self, x, y, w, h, model, isCoinBrick):
		super().__init__(x, y, w, h, model, isCoinBrick)
		self.coinImage = pygame.image.load("coin.png")
		self.vert_velocity = 0
		self.model = model
		self.hori_velocity = 5

	def draw(self, screen):
		screen.blit(self.coinImage, (self.x - self.model.mario.x + self.model.mario.startMario, self.y))
	
	def update(self):
		self.vert_velocity += 2
		self.y += self.vert_velocity
		self.x += self.hori_velocity*randint(0, 11)

class Mario(Sprite):
	def __init__(self, x, y, w, h, model, isCoinBrick):
		super().__init__(x, y, w, h, model, isCoinBrick)
		self.pX = 125
		self.pY = 100
		self.h = h
		self.w = w
		self.model = model
		self.changeImage = 0
		self.startMario = 125
		self.vert_vel = 0
		self.counter = 0
		self.isRunning = False

		self.marioImageArray = []
		self.marioImageArray.append(pygame.image.load("mario1.png"))
		self.marioImageArray.append(pygame.image.load("mario2.png"))
		self.marioImageArray.append(pygame.image.load("mario3.png"))
		self.marioImageArray.append(pygame.image.load("mario4.png"))
		self.marioImageArray.append(pygame.image.load("mario5.png"))

	def draw(self, screen):
		if self.isRunning:
			self.changeImage = self.changeImage + 1
			if self.changeImage > 4:
				self.changeImage = 0
			self.isRunning = False
		screen.blit(self.marioImageArray[self.changeImage], (self.startMario, self.y))

	def update(self):
		self.vert_vel += 1.2
		self.pY = self.y
		self.y += self.vert_vel

		# Mario ground
		if self.y > 420:
			self.vert_vel = 0
			self.y = 420
			self.counter = 0

		# Mario ceiling
		if self.y < 420:
			self.counter += 1

	def collisionHandler(self, s):

		if self.x + self.w >= s.x and self.pX + self.w <= s.x:
			self.x = s.x -self.w
			self.hitBottom = False

		if self.x <= s.x + s.w and self.pX >= s.x + s.w:
			self.x = s.x + s.w
			self.hitBottom = False

		if self.y + self.h >= s.y and self.pY + self.h <= s.y:
			self.vert_vel = 0.0
			self.y = s.y - self.h
			self.counter = 0
			self.hitBottom = False

		if self.y <= s.y + s.h and self.pY >= s.y + s.h:
			self.vert_vel = 0.0
			self.y = s.y + s.h
			self.hitBottom = True
			self.counter = 444


class Model():
	def __init__(self):
		self.sprites = []
		self.coinCount = 0
		self.empty = True
		self.offset = 32
		self.mario = Mario(100, 305, 60, 95, self, False)
		self.sprites.append(self.mario)

		self.brickImage1 = Brick(150, 325, 75, 75, self, False)
		self.sprites.append(self.brickImage1)
  
		self.brickImage2 = Brick(350, 250, 75, 75, self, True)
		self.sprites.append(self.brickImage2)
  
		self.brickImage3 = Brick(590, 300, 75, 75, self, False)
		self.sprites.append(self.brickImage3)
 
		self.brickImage4 = Brick(800, 300, 75, 75, self, False)
		self.sprites.append(self.brickImage4)

		self.brickImage5 = Brick(880, 200, 75, 75, self, False)
		self.sprites.append(self.brickImage5)

	def collisionDetection(self, a, b):
		if a.x + a.w <= b.x:
			return False
		if a.x >= b.x + b.w:
			return False
		if a.y + a.h <= b.y:
			return False
		if a.y >= b.y + b.h:
			return False
		return True

	def addingCoin(self, x, y, w, h):
			self.coin = Coin(x, y, w , h, self, False)
			self.sprites.append(self.coin)
			self.coinCount += 1
		
	def update(self):
		for sprite in self.sprites:
			sprite.update()
			if sprite.isBrick():
				if self.collisionDetection(self.mario, sprite):
					self.mario.collisionHandler(sprite)
					if sprite.isCoinBrick:
						if self.coinCount <= 3 and self.mario.hitBottom:
							self.addingCoin((sprite.x+sprite.w/2)-self.offset, sprite.y, 50, 50)
						elif self.coinCount >= 3 and self.mario.hitBottom:
							self.empty = True
							sprite.isCoinBrick = False

class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.background = pygame.image.load("marioBackGround.jpg")
		self.model = model


	def update(self):
		self.screen.fill([0,0,0])
		self.screen.blit(self.background, (-(self.model.mario.x/2), 0))
		self.background = pygame.transform.smoothscale(self.background, (1000, 600)) #scale background to size of screen
		for i in range(len(self.model.sprites)):
			self.model.sprites[i].draw(self.screen)
		pygame.display.flip()

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False

		keys = pygame.key.get_pressed()
  
		self.model.mario.pX = self.model.mario.x;
		self.model.mario.pY = self.model.mario.y;
  
		if keys[K_LEFT]:
			self.model.mario.isRunning = True
			self.model.mario.x -= 5

		if keys[K_RIGHT]:
			self.model.mario.isRunning = True
			self.model.mario.x += 5

		if keys[K_SPACE]:
			if self.model.mario.counter < 5:
				self.model.mario.vert_vel -= 5

print("Use the arrow keys to move, space bar to jump. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")