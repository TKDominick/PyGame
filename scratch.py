import pygame
pygame.init()

win = pygame.display.set_mode((1000,1000))

pygame.display.set_caption("Test Game")

x=0
y=0
width = 40
height = 60
vel = 15
isJump = False
jumpCount = 10

run = True
while run:
	pygame.time.delay(20)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		
	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_LEFT] and x > vel - 1:
		x -= vel
	if keys[pygame.K_RIGHT] and x < 1000 - width - vel + 10:
		x += vel
	if not(isJump):
		if keys[pygame.K_UP] and y > vel - 1:
			y -= vel
		if keys[pygame.K_DOWN] and y < 1000 - height - vel + 10:
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
		
		
		
	win.fill  ((0,0,255))
	pygame.draw.rect(win, (255,0,0), (x,y, width, height))
	pygame.display.update()

pygame.quit()