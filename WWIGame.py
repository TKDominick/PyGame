import pygame
import random

pygame.init()

win = pygame.display.set_mode((1280,700))

pygame.display.set_caption("Test Game")

Left = False
Right = False
Up = False
Down = False


bg = pygame.image.load('Airfield1.png')
print(bg)
bg2 = pygame.image.load('Airfield2.png')
bg3 = pygame.image.load('Industrial.png')
prevbackground = 'Industrial.png'

bgx = 0
bg2x = 1280
bg3x = 2560

framecount = 0

ExplosionFramecount = 0
explosions = []
enemies = []
enemyattacks = []
bullets = []
bombs = []
BombCD = 3500
BulletCD = 2000


killed = {}

clock = pygame.time.Clock()


class Player:
	def __init__(self, x, y, width, height, vel):
		self.health = 20
		self.healthsprites =['Health0.png', 'Health1.png', 'Health2.png', 'Health3.png', 'Health4.png', 'Health5.png',
						 'Health6.png', 'Health7.png', 'Health8.png', 'Health9.png', 'Health10.png',
						 'Health11.png', 'Health12.png', 'Health13.png', 'Health14.png', 'Health15.png',
						 'Health16.png', 'Health17.png', 'Health18.png', 'Health19.png', 'Health20.png']
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = vel
		self.char = pygame.image.load('PlayerPlane.png')
		self.flyleft = []
		self.flyright = []
		self.hitbox = (self.x, self.y + (64 - self.height), self.width, self.height)
		self.Left = False
		self.Right = False
		self.Up = False
		self.Down = False
		
	def Draw(self):
		win.blit(self.char, (self.x,self.y))
		pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
	def DrawHealth(self):
		healthchar = pygame.image.load(self.healthsprites[self.health])
		win.blit(healthchar, (560, 75))
	
		
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
			self.damage = 10
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
			self.name = 'Small Observer Balloon'
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
			self.hitbox = (self.x, self.y, self.width, self.height)
			
	def Draw(self):
		win.blit(self.sprite, (self.x, self.y))
		pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
		
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

def GetBackground(killed):
	global prevbackground
	output = 'Field1.png'
	
	fields = ['Field1.png', 'Field2.png', 'Field3.png', 'Field4.png']
	general = ['Field1.png', 'Field2.png', 'Field3.png', 'Field4.png', 'Village.png', 'City1.png', 'EnemyCamp.png', 'Airfield1.png']

	if prevbackground == 'Industrial.png':
		output = random.choice(general)
	
	if prevbackground == 'Airfield1.png':
		output = 'Airfield2.png'
	if prevbackground == 'City1.png':
		output = 'City2.png'
	if prevbackground == 'City2.png':
		output = 'City3.png'
	if prevbackground == 'City3.png':
		output = random.choice(general)
	
	if prevbackground == 'Village.png':
		output = random.choice(fields)
		
	if prevbackground == 'Field1.png' or prevbackground == 'Field2.png' or prevbackground == 'Field3.png' or prevbackground == 'Field4.png':
		if len(killed) >= 100:
			output = 'EnemyBase1.png'
		else:
			output = random.choice(general)
	
	if prevbackground == 'EnemyBase1.png':
		output = 'EnemyBase2.png'
	if prevbackground == 'EnemyBase2.png':
		output = 'EnemyHangar.png'
	if prevbackground == 'EnemyHangar.png':
		output = 'Sky1.png'
	if prevbackground == 'Sky1.png':
		output = 'Sky2.png'
	
	prevbackground = output
	return output
	
def BackgroundRunner():
	global killed
	global bg
	global bg2
	global bg3
	global bgx
	global bg2x
	global bg3x
	
	bgx -= 5
	bg2x -= 5
	bg3x -= 5
	
	if bg2x == 0:
		bg = bg2
		bgx = 0
		bg2 = bg3
		bg2x = 1280
		bg3 = pygame.image.load((GetBackground(killed)))
		print(type(bg3))
		bg3x = 2560
	
def redrawGameWindow():
	global framecount
	win.blit(bg, (bgx, 0))
	win.blit(bg2, (bg2x, 0))
	win.blit(bg3, (bg3x, 0))
	#Character animations
	'''
	if Left:
		win.blit(flyleft[framecount])
	elif Right:
		win.Blit(flyright[framecount])
	else:
	'''
	Plane.Draw()
	Plane.DrawHealth()
	
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
	
def GetWave(killed):
	pass
	
Plane = Player(200, 500, 64, 54, 10)
run = True
while run:
	clock.tick(20)
	
	#if 6500 <bg2x < 10000 and len(enemies) == 0:
	#	Enemy1 = Enemy(1000, 350, 25, 4, 1, 'Enemy1.png', 64, 64)
	#	enemies.append(Enemy1)
	#if bg2x < 6000 and killed['Small Observer Balloon'] >= 5 and len(enemies) == 0:
	#	Enemy1 = Enemy(1000, 150, 20, 4, 1, 'Enemy1.png', 64, 64)
	#	enemies.append(Enemy1)
	#	Enemy2 = Enemy(1000, 350, 20, 4, 1, 'Enemy1.png', 64, 64)
	#	enemies.append(Enemy2)
	#	Enemy3 = Enemy(1000, 550, 20, 4, 1, 'Enemy1.png', 64, 64)
	#	enemies.append(Enemy3)
	
	#if bgx > -10294:
	#	bgx -= 5
	#	bg2x -= 5
	
	BackgroundRunner()
	GetWave(killed)
		
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
		
		
	if keys[pygame.K_UP] and Plane.y > Plane.vel - 1:
		Plane.y -= Plane.vel
	
	if keys[pygame.K_DOWN] and Plane.y < 600 - Plane.height - Plane.vel + 10:
		Plane.y += Plane.vel
	
	if keys[pygame.K_q] and BulletCD == 0:
		if len(bullets) < 10:
			PlayerBullet = Projectile(Plane.x + 35, Plane.y + 26, 1, 'PlayerBullet.png')
			bullets.append(PlayerBullet)
			BulletCD += 300
		elif len(bullets) == 10:
			BulletCD += 3500
	if keys[pygame.K_e] and BombCD == 0:
		if len(bombs) < 3:
			PlayerBomb = Projectile(Plane.x + 20, Plane.y + 40, 2, 'PlayerBomb.png')
			bombs.append(PlayerBomb)
			BombCD += 600
		elif len(bombs) == 3:
			BombCD += 4000
			
	if BulletCD != 0:
		BulletCD -= 50
	if BombCD != 0:
		BombCD -= 50
	
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
		enemy.hitbox = (enemy.x, enemy.y, enemy.width, enemy.height)
	
	for attack in enemyattacks:
		if 0 < attack.x < 1280 and 0 < attack.y < 700:
			attack.Move()
			attack.Draw()
		else:
			enemyattacks.pop(enemyattacks.index(attack))
		
	for enemy in enemies:
		for bullet in bullets:
			if ColissionDetect(enemy.x, enemy.y, enemy.width, enemy.height, bullet.x, bullet.y):
				enemy.health -= 3
				Explosion = (bullet.x,bullet.y)
				explosions.append(Explosion)
				bullets.pop(bullets.index(bullet))
		
	for enemy in enemies:
		for bomb in bombs:
			if ColissionDetect(enemy.x, enemy.y, enemy.width, enemy.height, bomb.x, bomb.y):
				enemy.health -= 10
				Explosion = (bomb.x,bomb.y)
				explosions.append(Explosion)
				bombs.pop(bombs.index(bomb))
				
	for attack in enemyattacks:
		if ColissionDetect(Plane.x, Plane.y, Plane.width, Plane.height, attack.x, attack.y):
			Plane.health -= 2
			Explosion = (attack.x,attack.y)
			explosions.append(Explosion)
			enemyattacks.pop(enemyattacks.index(attack))
	
	Plane.hitbox = (Plane.x, Plane.y + (64 - Plane.height), Plane.width, Plane.height)
	
	for enemy in enemies:
		if enemy.health <= 0:
			if enemy.name not in killed:
				killed[enemy.name] = 0
			killed[enemy.name] += 1
			enemies.pop(enemies.index(enemy))
	
	
	if framecount + 1 > 24:
		framecount = 0

	if framecount % 6 == 0:
		explosions = []
	framecount += 1
	redrawGameWindow()
pygame.quit()
