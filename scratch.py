import pygame
import time
pygame.init()

win = pygame.display.set_mode((1280,700))

pygame.display.set_caption("Test Game")

Left = False
Right = False
Up = False
Down = False

flyleft = []
flyright = []
bg = pygame.image.load('Background.png') # Not done yet

char = pygame.image.load('RedBaron.png') # Temporary
framecount = 0

bgx = 0
bgy = 0
x=200
y=500
width = 64
height = 64
vel = 15
isJump = False
jumpCount = 10
clock = pygame.time.Clock()

class Enemy:
	def __init__(self, enemtype):
		
		if enemtype == 1:
			self.x = 1000
			self.y = 350
			self.health = 3
			self.sprite = pygame.image.load('Balloon1.png')

	def Display(self):
		win.blit()

def redrawGameWindow():
	global framecount
	win.blit(bg, (bgx, bgy))
	
	#win.fill((135, 206, 250))
	
	if framecount + 1 >= 12:
		framecount = 0
		
	#Character animations
	'''
	if Left:
		win.blit(flyleft[framecount])
	elif Right:
		win.Blit(flyright[framecount])
	else:
	'''
	win.blit(char, (x,y))
	
	
	pygame.display.update()
	



run = True
while run:
	clock.tick(30)
	
	if bgx > -10230:
		bgx -= (vel - 5)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		
	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_LEFT] and x > vel - 1:
		x -= vel
		Left = True
		Right = False
		Up = False
		Down = False
	elif keys[pygame.K_RIGHT] and x < 1280 - width - vel + 10:
		x += vel
		Left = False
		Right = True
		Up = False
		Down = False
	else:
		Left = False
		Right = False
		Up = False
		Down = False
		framecount = 0
		
	# Remove Jump Function
	if not(isJump):
		if keys[pygame.K_UP] and y > vel - 1:
			y -= vel
		if keys[pygame.K_DOWN] and y < 700 - height - vel + 10:
			y+= vel
		if keys[pygame.K_SPACE]:
			isJump = True
	else:
		if jumpCount >= -10:
			neg = 1
			if jumpCount < 0:
				neg = -1
			y -= (jumpCount ** 2) * 0.75 * neg
			jumpCount -= 1
		else:
			isJump = False
			jumpCount = 10
		
	redrawGameWindow()
pygame.quit()