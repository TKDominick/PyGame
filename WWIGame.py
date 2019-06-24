import pygame
import time
pygame.init()

win = pygame.display.set_mode((1280,700))

pygame.display.set_caption("Test Game")

Left = False
Right = False
Up = False
Down = False


bg = pygame.image.load('Background.png') # Not done yet

framecount = 0

ExplosionFramecount = 0
explosions = []
enemies = []
enemyattacks = []
bullets = []
bombs = []
BulletOnCD = False
BombOnCD = False
BombCD = 3500
BulletCD = 2000
bgx = 0
bgy = 0


clock = pygame.time.Clock()


class Player:
	def __init__(self, x,y,width,height,vel):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = vel
		self.char = pygame.image.load('RedBaron.png')
		self.flyleft = []
		self.flyright = []
		self.Left = False
		self.Right = False
		self.Up = False
		self.Down = False
		
	def Draw(self):
		win.blit(self.char, (self.x,self.y))
		
class Projectile:
	def __init__(self, x, y, projtype, sprite):
		self.x = x
		self.y = y
		
		
		if projtype == 1:
			self.damage = 3
			self.xvel = 30
			self.yvel = 00
			self.move = 1		# straight
			self.sprite = pygame.image.load(sprite)
			
		if projtype == 2:
			self.damage = 15
			self.xvel = 20
			self.yvel = 0
			self.yaccel = 5
			self.move = 2
			self.sprite = pygame.image.load(sprite)
		
		if projtype == 3:
			self.damage = 2
			self.xvel = -12
			self.yvel = -25
			self.yaccel = 5
			self.move = 3
			self.sprite = pygame.image.load(sprite)
		
		
	def Move(self):
		if self.move == 1:
			self.x += self.xvel
			self.y += self.yvel
		
		elif self.move == 2:
			self.x += self.xvel
			self.y += self.yvel
			self.yvel += self.yaccel
		
		elif self.move == 3:
			self.x += self.xvel
			self.y += self.yvel
			self.yvel += self.yaccel
			
	def Draw(self):
		win.blit(self.sprite, (self.x, self.y))
		

		
class Enemy:
	def __init__(self, x, y, health, vel, enemtype, sprite, width, height):
		
		if enemtype == 1:
			self.x = x
			self.y = y
			self.health = health
			self.vel = vel
			self.width = width
			self.height = height
			self.sprite = pygame.image.load(sprite)
			self.attacktype = 3
			self.attacksprite = 'Enemy1Grenade.png'
			self.attackCD = 1500
			self.CDMAX = 1500
			
	def Draw(self):
		win.blit(self.sprite, (self.x, self.y))
		
	def Move(self, x, y):
		if self.x < x+150:
			self.x += self.vel
		elif self.x > x+170:
			self.x -= self.vel
			
		if self.y < y - 20:
			self.y += self.vel
		elif self.y > y:
			self.y -= self.vel


def ColissionDetect(unitx, unity, unitwidth, unitheight, projectilex, projectiley):
	xrange = range(unitx, (unitx + unitwidth))
	yrange = range(unity, (unity + unitheight))

	if projectilex in xrange and projectiley in yrange:
		return True
	else:
		return False
	
		
def redrawGameWindow():
	global framecount
	win.blit(bg, (bgx, bgy))
	
	#Character animations
	'''
	if Left:
		win.blit(flyleft[framecount])
	elif Right:
		win.Blit(flyright[framecount])
	else:
	'''
	Plane.Draw()
	
	for enemy in enemies:
		enemy.Draw()
	
	for attack in enemyattacks:
		attack.Draw()
		
	for bullet in bullets:
		bullet.Draw()
	
	for bomb in bombs:
		bomb.Draw()
	
	for explosion in explosions:
		win.blit(pygame.image.load('Explosion.png'), explosion)
	
	pygame.display.update()
	
	
Plane = Player(200,500,64,64,10)
run = True
while run:
	clock.tick(20)
	
	if bgx < -2500 and len(enemies) == 0:
		Enemy1 = Enemy(1000, 350, 3, 4, 1, 'Enemy1.png', 64, 64)
		enemies.append(Enemy1)
	
	if bgx > -10230:
		bgx -= (5)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		
	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_q]:
		pass
	
	if keys[pygame.K_LEFT] and Plane.x > Plane.vel - 1:
		Plane.x -= Plane.vel
		Left = True
		Right = False
		Up = False
		Down = False
	
	elif keys[pygame.K_RIGHT] and Plane.x < 1280 - Plane.width - Plane.vel + 10:
		Plane.x += Plane.vel
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
		
	if keys[pygame.K_UP] and Plane.y > Plane.vel - 1:
		Plane.y -= Plane.vel
	
	if keys[pygame.K_DOWN] and Plane.y < 600 - Plane.height - Plane.vel + 10:
		Plane.y += Plane.vel
	
	if keys[pygame.K_q] and (framecount % 24) == 0 and BulletOnCD == False:
		if len(bullets) < 10:
			PlayerBullet = Projectile(Plane.x + 35, Plane.y + 26, 1, 'PlayerBullet.png')
			bullets.append(PlayerBullet)
		elif len(bullets) == 10:
			BulletOnCD = True
	if keys[pygame.K_e] and (framecount % 24) == 0 and BombOnCD == False:
		if len(bombs) < 3:
			PlayerBomb = Projectile(Plane.x + 20, Plane.y + 40, 2, 'PlayerBomb.png')
			bombs.append(PlayerBomb)
		elif len(bombs) == 3:
			BombOnCD = True
			
	if BulletOnCD == True:
		BulletCD -= 50
	if BulletCD <= 0:
		BulletOnCD = False
		BulletCD = 2000
	
	if BombOnCD == True:
		BombCD -= 50
	if BombCD <= 0:
		BombOnCD = False
		BombCD = 3000
	
	for bullet in bullets:
		if 0 < bullet.x < 1280:
			bullet.Move()
		else:
			bullets.pop(bullets.index(bullet))
	
	for bomb in bombs:
		if 0 < bomb.x < 1280 and bomb.y < 700:
			bomb.Move()
		else:
			bombs.pop(bombs.index(bomb))
			
	for enemy in enemies:
		enemy.Move(Plane.x,Plane.y)
		if enemy.attackCD <= 0:
			EnemyAttack = Projectile(enemy.x, enemy.y, enemy.attacktype, enemy.attacksprite)
			enemyattacks.append(EnemyAttack)
			enemy.attackCD = enemy.CDMAX
		else:
			enemy.attackCD -= 40
	
	for attack in enemyattacks:
		if 0 < attack.x < 1280 and 0 < attack.y < 700:
			attack.Move()
			attack.Draw()
		else:
			enemyattacks.pop(enemyattacks.index(attack))
	
	for bullet in bullets:
		for enemy in enemies:
			if ColissionDetect(enemy.x, enemy.y, enemy.width, enemy.height, bullet.x, bullet.y):
				Explosion = (bullet.x,bullet.y)
				explosions.append(Explosion)
				bullets.pop(bullets.index(bullet))
				
	for bomb in bombs:
		for enemy in enemies:
			if ColissionDetect(enemy.x, enemy.y, enemy.width, enemy.height, bomb.x, bomb.y):
				Explosion = (bomb.x,bomb.y)
				explosions.append(Explosion)
				bombs.pop(bombs.index(bomb))
				
	for attack in enemyattacks:
		if ColissionDetect(Plane.x, Plane.y, 64, 64, attack.x, attack.y):
			Explosion = (attack.x,attack.y)
			explosions.append(Explosion)
			enemyattacks.pop(enemyattacks.index(attack))
		for enemy in enemies:
			if ColissionDetect(enemy.x, enemy.y, enemy.width, enemy.height, attack.x, attack.y):
				Explosion = (attack.x,attack.y)
				explosions.append(Explosion)
				enemyattacks.pop(enemyattacks.index(attack))
	
	
	redrawGameWindow()
	if framecount + 1 > 24:
		framecount = 0
		
	else:
		framecount += 1
	if framecount % 4 == 0:
		explosions = []
pygame.quit()
