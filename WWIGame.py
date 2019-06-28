import pygame
import random
import time

pygame.init()

win = pygame.display.set_mode((1280,700))

pygame.display.set_caption("Plane Shooter Game")

Left = False
Right = False
Up = False
Down = False

score = 0
bg = pygame.image.load('Airfield1.png')
print(bg)
bg2 = pygame.image.load('Airfield2.png')
bg3 = pygame.image.load('Industrial.png')
bgcount = 1
prevbackground = 'Industrial.png'

bgx = 0
bgy = 0
bg2x = 1280
bg2y = 0
bg3x = 2560
bg3y = 0

paused = True
won = False

#bulletsound = pygame.mixer.Sound('')
#bombsound = pygame.mixer.Sound('')
framecount = 0
bossspawned = False
initializefight = False
ExplosionFramecount = 0
explosions = []
enemies = []
enemyattacks = []
bullets = []
bombs = []
BombCD = 3500
BulletCD = 2000
font = pygame.font.SysFont('sitkasmallsitkatextitalicsitkasubheadingitalicsitkaheadingitalicsitkadisplayitalicsitkabanneritalic.ttf', 42)
font2 = pygame.font.SysFont('sitkasmallsitkatextitalicsitkasubheadingitalicsitkaheadingitalicsitkadisplayitalicsitkabanneritalic.ttf', 242)
killed = []

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
		# pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
	def DrawHealth(self):
		healthchar = pygame.image.load(self.healthsprites[self.health])
		win.blit(healthchar, (480, 75))
	
		
class Projectile:
	def __init__(self, x, y, projtype):
		self.x = x
		self.y = y
		
		if projtype == 1:
			self.damage = 3
			self.xvel = 30
			self.xaccel = 0
			self.yvel = 0
			self.move = 1		# straight
			self.sprite = pygame.image.load('PlayerBullet.png')
			
		if projtype == 2:
			self.damage = 10
			self.xvel = 20
			self.xaccel = 0
			self.yvel = 0
			self.yaccel = 5
			self.move = 2
			self.sprite = pygame.image.load("PlayerBomb.png")
		
		if projtype == 3: #Baloon 1 Bullet
			self.damage = 2
			self.xvel = -12
			self.yvel = -25
			self.yaccel = 5
			self.move = 3
			self.sprite = pygame.image.load('Bullet.png')
		
		if projtype == 4: #Tank projectile
			self.damage = 5
			self.move = 3
			self.yvel = -100
			self.yaccel = 15
			self.xvel = -50
			self.xaccel = 0
			self.sprite = pygame.image.load('Bullet.png')
		
		if projtype == 5: # Cannon projectile
			self.damage = 3
			self.move = 3
			self.yvel = -75
			self.yaccel = 10
			self.xvel = -40
			self.xaccel =0
			self.sprite = pygame.image.load('Bullet.png')
		if projtype == 11:
			self.damage = 1
			self.move = 5
			self.yvel = 0
			self.yaccel = 0
			self.xvel = -30
			self.xaccel = 0
			self.sprite = pygame.image.load('FBBullet.png')
		
		if projtype == 12:
			self.damage = 2
			self.move = 3
			self.yvel = -40
			self.yaccel = 5
			self.xvel = -20
			self.xaccel = 0
			self.sprite = pygame.image.load('FBBullet.png')
		if projtype == 13:
			self.x = x+54
			self.damage = 2
			self.move = 12
			self.yvel = 3
			self.yaccel = 0
			self.xvel = 5
			self.xaccel = 0
			self.sprite = pygame.image.load('FBMissile.png')
			pass
		if projtype == 14:
			self.damage = 0
			self.move = 99
			Bossplane = Enemy(1300, 450, 9)
			enemies.append(Bossplane)
			Bossplane2 = Enemy(1450, 450, 9)
			enemies.append(Bossplane2)
			Bossplane3 = Enemy(1600, 450, 9)
			enemies.append(Bossplane3)
			self.sprite = pygame.image.load('BossProjectile.png')
			
		
	def Move(self, targetx, targety):
		if self.move == 1: # player bullet
			self.x += self.xvel
			self.y += self.yvel
		
		elif self.move == 2: #player bomb
			self.x += self.xvel
			self.y += self.yvel
			self.yvel += self.yaccel
		
		elif self.move == 3: # arc shape
			self.x += self.xvel
			self.y += self.yvel
			self.yvel += self.yaccel
		
		elif self.move == 4: #Straight Down Bomb
			self.y += self.yvel
			self.y += self.yaccel
		
		elif self.move == 5: #Straight bullet
			self.x += self.xvel
			self.xvel += self.xaccel
			
		elif self.move == 12: # targeting missile
			if self.x < targetx + 32:
				self.x += self.xvel
			if self.x > targetx + 32:
				self.x -= self.xvel
			if self.y < targety + 32:
				self.y += self.yvel
			if self.y > targety + 32:
				self.y -= self.yvel
		
		elif self.move == 99:
			pass
	def Draw(self):
		win.blit(self.sprite, (self.x, self.y))
		
		
class Enemy:
	def __init__(self, x, y, enemtype):
		
		if enemtype == 1:        # Balloon 1
			#self.sound = pygame.mixer.Sound('')
			self.type = 1
			self.name = 'Small Observer Balloon'
			self.score = 3
			self.x = x
			self.y = y
			self.health = 21
			self.vel = 4
			self.width = 31
			self.height = 47
			self.sprite = pygame.image.load('Balloon1.png')
			self.attacktype = 3
			self.attacksprite = pygame.image.load('Enemy1Grenade.png')
			self.attackCD = 1500
			self.CDMAX = 1500
			self.movetype = 1
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 2: #Balloon 2
			self.type = 2
			self.name = 'Small Dirigible'
			self.score = 2
			self.x = x
			self.y = y
			self.health = 45
			self.vel = 9
			self.width = 64
			self.height = 64
			self.sprite = pygame.image.load('Balloon2.png')
			self.attacktype = 6
			self.attacksprite = pygame.image.load('Bullet.png')
			self.attackCD = 4000
			self.CDMAX = 4000
			self.movetype = 5
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 3: #Plane 1
			self.type = 3
			self.name = 'Small Shooter'
			self.score = 1
			self.x = x
			self.y = y
			self.health = 30
			self.vel = 17
			self.width = 64
			self.height = 64
			self.sprite = pygame.image.load('Plane1.png')
			self.attacktype = 7
			self.attacksprite = pygame.image.load('Bullet.png')
			self.attackCD = 450
			self.CDMAX = 500
			self.movetype = 3
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 4: #Plane 2
			self.type = 4
			self.name = 'Small Bomber'
			self.score = 2
			self.x = x
			self.y = y
			self.health = 50
			self.vel = 11
			self. width = 64
			self.height = 64
			self.sprite = pygame.image.load('Plane2.png')
			self.attacktype = 8
			self.attacksprite = pygame.image.load('Bomb.png')
			self.attackCD = 1200
			self.CDMAX = 1200
			self.movetype = 5
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 5: #Plane 3
			self.type = 5
			self.name = 'Big Shooter'
			self.score = 3
			self.x = x
			self.y = y
			self.health = 40
			self.vel = 8
			self.width = 64
			self.height = 64
			self.sprite = pygame.image.load('Plane3.png')
			self.attacktype = 9
			self.attacksprite = pygame.image.load('Bullet.png')
			self.attackCD = 200
			self.CDMAX = 200
			self.movetype = 3
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 6: #Plane 4
			self.type = 6
			self.name = 'Big Bomber'
			self.score = 2
			self.x = x
			self.y = y
			self.health = 75
			self.vel = 7
			self.width = 128
			self.height = 64
			self.sprite = pygame.image.load('Plane4.png')
			self.attacktype = 10
			self.attacksprite = pygame.image.load('Bomb.png')
			self.attackCD = 3000
			self.CDMAX = 5000
			self.movetype = 5
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 7: #Cannon
			#self.sound = pygame.mixer.Sound('')
			self.type = 7
			self.name = 'Enemy Cannon'
			self.score = 1
			self.x = x
			self.y = y
			self.health = 30
			self.vel = 5
			self.width = 64
			self.height = 64
			self.sprite = pygame.image.load('Cannon.png')
			self.attacktype = 5
			self.attacksprite = pygame.image.load('Bullet.png')
			self.attackCD = 500
			self.CDMAX = 650
			self.movetype = 3
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 8: #Tank
			#self.sound = pygame.mixer.Sound('')
			self.type = 8
			self.name = 'Enemy Tank'
			self.score = 2
			self.x = x
			self.y = y
			self.health = 200
			self.vel = 2
			self. width = 64
			self.height = 64
			self.sprite = pygame.image.load('Tank.png')
			self.attacktype = 4
			self.attacksprite = pygame.image.load('Bullet.png')
			self.attackCD = 1000
			self.CDMAX = 1000
			self.movetype = 2
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 9: #Final Boss Plane
			#self.sound = pygame.mixer.Sound('')
			self.type = 9
			self.score = 4
			self.name = 'Aurora 1A'
			self.x = x
			self.y = y
			self.health = 15
			self.vel = 10
			self. width = 64
			self.height = 64
			self.sprite = pygame.image.load('FinalBossPlane.png')
			self.attacktype = 11
			self.attacksprite = pygame.image.load('FBBullet.png')
			self.attackCD = 500
			self.CDMAX = 500
			self.movetype = 6
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 10: #Final Boss Cannon
			#self.sound = pygame.mixer.Sound('')
			self.type = 10
			self.score = 10
			self.name = 'Aurora Cannon'
			self.x = x
			self.y = y
			self.health = 125
			self.vel = 5
			self.width = 36
			self.height = 28
			self.sprite = pygame.image.load('BossCannon.png')
			self.attacktype = 12
			self.attacksprite = pygame.image.load('FBBullet.png')
			self.attackCD = 1000
			self.CDMAX = 1000
			self.movetype = 97
			self.hitbox = (self.x, self.y, self.width, self.height)
		if enemtype == 11: #Final Boss Missiles
			#self.sound = pygame.mixer.Sound('')
			self.type = 11
			self.score = 20
			self.name = 'Aurora Missiles'
			self.x = x
			self.y = y
			self.health = 100
			self.vel = 5
			self.width = 32
			self.height = 46
			self.sprite = pygame.image.load('BossMissiles.png')
			self.attacktype = 13
			self.attacksprite = pygame.image.load('FBMissile.png')
			self.attackCD = 5000
			self.CDMAX = 5000
			self.movetype = 98
			self.hitbox = (self.x , self.y, self.width, self.height)
		if enemtype == 12: #Final Boss
			#self.sound = pygame.mixer.Sound('')
			self.type = 12
			self.score = 100
			self.name = 'The Aurora'
			self.x = x
			self.y = y
			self.health = 250
			self.vel = 5
			self.width = 600
			self.height = 163
			self.sprite = pygame.image.load('FinalBossBlimp.png')
			self.attacktype = 14
			self.attacksprite = pygame.image.load('FinalBossPlane.png')
			self.attackCD = 8000
			self.CDMAX = 12000
			self.movetype = 99
			self.hitbox = (self.x , self.y, self.width, self.height)
		
	def Draw(self):
		win.blit(self.sprite, (self.x, self.y))
		# pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
		
	def Move(self, x, y):
		if self.movetype == 1: #Balloon 1
			if self.x <= x+150:
				self.x += self.vel
			elif self.x >= x+170:
				self.x -= self.vel
				
			if self.y >= y - 20:
				self.y -= self.vel
			elif self.y <= y - 50:
				self.y += self.vel
			
		if self.movetype == 2: # Tank
			if self.x > 850:
				self.x -= self.vel
			if self.x < 800:
				self.x += self.vel
		
		if self.movetype == 3: #Cannon
			if self.x > 600:
				self.x -= self.vel
			if self.x < 550:
				self.x += self.vel
		
		if self.movetype == 4:
			pass
		
		if self.movetype == 5:
			pass
		
		if self.movetype == 6:
			if self.y < y - 20:
				self.y += self.vel
			if self.y > y + 20:
				self.y -= self.vel
			if self.x < x + 250:
				self.x += self.vel
			if self.x > x + 275:
				self.x -= self.vel
		
		if self.movetype == 7:
			pass
				
		if self.movetype == 8:
			pass
		
		if self.movetype == 9:
			pass
		if self.movetype == 97:
			if self.x >=950:
				self.x -= self.vel
		if self.movetype == 98:
			if self.x >= 1065:
				self.x-= self.vel
		if self.movetype == 99:
			if self.x >= 900:
				self.x -= self.vel
		
		
def ColissionDetect(unitx, unity, unitwidth, unitheight, projectilex, projectiley):
	xrange = range(unitx, (unitx + unitwidth))
	yrange = range(unity, (unity + unitheight))

	if projectilex in xrange and projectiley in yrange:
		return True
	else:
		return False


def GetBackground():
	global prevbackground
	global bgcount
	bgcount += 1
	output = 'Field1.png'
	
	fields = ['Field1.png', 'Field2.png', 'Field3.png', 'Field4.png']
	general = ['Field1.png', 'Field2.png', 'Field3.png', 'Field4.png', 'Village.png', 'City1.png', 'EnemyCamp.png', 'Airfield1.png', 'Industrial.png']

	if prevbackground == 'Industrial.png':
		output = random.choice(general)
	
	if prevbackground == 'Airfield1.png':
		output = 'Airfield2.png'
	if prevbackground == 'Airfield2.png':
		output = 'Industrial.png'
	if prevbackground == 'City1.png':
		output = 'City2.png'
	if prevbackground == 'City2.png':
		output = 'City3.png'
	if prevbackground == 'City3.png':
		output = random.choice(general)
	
	if prevbackground == 'Village.png':
		output = random.choice(fields)
		
	if prevbackground == 'Field1.png' or prevbackground == 'Field2.png' or prevbackground == 'Field3.png' or prevbackground == 'Field4.png':
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
	global initializefight
	global killed
	global bg
	global prevbackground
	global bg2
	global bg3
	global bgx
	global bg2x
	global bg3x
	global bgy
	global bg2y
	global bg3y

	if prevbackground != 'bossfight':
		bgx -= 5
		bg2x -= 5
		bg3x -= 5
	
		if bg2x <= 0:
			bg = bg2
			bgx = 0
			bg2 = bg3
			bg2x = 1280
			bg3 = pygame.image.load(GetBackground())
			bg3x = 2560
	
	else:
		if bg3x <= 0:
			global bg2y
			if initializefight == True:
				bg3x = 0
				bg3y = 0
				bg = pygame.image.load('Sky1.png')
				bgx = 0
				bgy = -700
				bg2 = pygame.image.load('Sky2.png')
				bg2x = 0
				bg2y = -1400
				initializefight = False
			elif bg2y > 0:
				bgy += 5
				bg2y += 5
				bg3y += 5
		else:
			bgx -= 5
			bg2x -= 5
			bg3x -= 5
	if score > 100:
		prevbackground = 'bossfight'
		bg3 =pygame.image.load('EnemyHangar.png')
		initializefight = True
		
		
def redrawGameWindow():
	global framecount
	win.blit(bg, (bgx, bgy))
	win.blit(bg2, (bg2x, bg2y))
	win.blit(bg3, (bg3x, bg3y))
	
	# midline = pygame.Rect(639, -2, 3, 705)
	# pygame.draw.rect(win, (0, 0, 0), midline)
	
	textplate = font.render(str(score), True, (0, 0, 0))
	if len(str(score)) == 1:
		win.blit(textplate, (633, 25))
	if len(str(score)) == 2:
		win.blit(textplate, (624, 25))
	if len(str(score)) == 3:
		win.blit(textplate, (617, 25))
	
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
	
	pygame.display.flip()
	
def GetWave():
	global killed
	global bossspawned
	global score
	global enemies
	if score <= 100:
		if len(enemies) == 0 and  10 > bgcount >= 2:
			SmolBalloon = Enemy(1350, 350, 1)
			Cannon = Enemy(1350, 570, 7)
			enemies.append(SmolBalloon)
			enemies.append(Cannon)
		if len(enemies) == 0 and 20 > bgcount >= 12:
			Cannon = Enemy(1350, 620, 7)
			enemies.appesnd(Cannon)
		if len(enemies) == 0 and 40 > bgcount >= 20:
			Tank = Enemy(1350, 620, 8)
			enemies.append(Tank)
	
	if score > 100 and prevbackground == 'bossfight' and not bossspawned:
		Aurora = Enemy(1280, 82, 12)
		AuroraCannon = Enemy(1330, 77, 10)
		AuroraMissiles = Enemy(1450, 266, 11)
		enemies.append(Aurora)
		enemies.append(AuroraCannon)
		enemies.append(AuroraMissiles)
		bossspawned = True
		
Plane = Player(200, 500, 64, 54, 10)
run = True
while run:
	clock.tick(20)
	keys = pygame.key.get_pressed()
	
	if paused:
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				
		pausedscreen = pygame.image.load('PausedScreen.png')
		win.blit(pausedscreen, (140, 50))
		textplate = font2.render(str(score), True, (0, 0, 0))
		if len(str(score)) == 1:
			win.blit(textplate, (800, 220))
		if len(str(score)) == 2:
			win.blit(textplate, (750, 220))
		if len(str(score)) == 3:
			win.blit(textplate, (700, 220))
		
		pygame.display.flip()
		
		if keys[pygame.K_SPACE]:
			paused = False
			time.sleep(0.1)
		
	else:
		
		BackgroundRunner()
		GetWave()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		
		while True:

			if keys[pygame.K_a] and Plane.x > Plane.vel - 1:
				Plane.x -= Plane.vel
			elif keys[pygame.K_d] and Plane.x < 1280 - Plane.width - Plane.vel + 10:
				Plane.x += Plane.vel
			if keys[pygame.K_w] and Plane.y > Plane.vel - 1:
				Plane.y -= Plane.vel
			if keys[pygame.K_s] and Plane.y < 600 - Plane.height - Plane.vel + 10:
				Plane.y += Plane.vel
			if keys[pygame.K_EQUALS] and score < 100: # Cheat, Goes Straight to boss
				for enemy in enemies:
					enemies.pop(enemies.index(enemy))
					score += 101
					break
					
			if keys[pygame.K_q] and BulletCD == 0:
				if len(bullets) < 10:
					PlayerBullet = Projectile(Plane.x + 35, Plane.y + 26, 1)
					bullets.append(PlayerBullet)
					#bulletsound.play()
					BulletCD += 150
				elif len(bullets) == 10:
					BulletCD += 3500
			if keys[pygame.K_e] and BombCD == 0:
				if len(bombs) < 5:
					PlayerBomb = Projectile(Plane.x + 20, Plane.y + 40, 2)
					bombs.append(PlayerBomb)
					#bombsound.play()
					BombCD += 400
				if len(bombs) >= 2:
					BombCD += 5000
			break     #Key Presses
			
		if BulletCD != 0:
			BulletCD -= 50
		if BombCD != 0:
			BombCD -= 50
		
		for bullet in bullets:
			if 0 < bullet.x < 1280:
				bullet.Move(Plane.x, Plane.y)
			else:
				bullets.pop(bullets.index(bullet))
		
		for bomb in bombs:
			if 0 < bomb.x < 1280 and bomb.y < 700:
				bomb.Move(Plane.x, Plane.y)
			else:
				bombs.pop(bombs.index(bomb))
				
		for enemy in enemies:
			enemy.Move(Plane.x,Plane.y)
			if enemy.attackCD <= 0:
				EnemyAttack = Projectile(enemy.x, enemy.y, enemy.attacktype)
				enemyattacks.append(EnemyAttack)
				enemy.attackCD = enemy.CDMAX
				#(enemy.sound).play()
			else:
				enemy.attackCD -= 40
			if enemy.type < 12:
				enemy.hitbox = (enemy.x, enemy.y, enemy.width, enemy.height)
			else:
				enemy.hitbox = (enemy.x, enemy.y + 23, enemy.width, enemy.height)
			
			while True:
				if enemy.type < 12:
					for bullet in bullets:
						if ColissionDetect(enemy.x, enemy.y, enemy.width, enemy.height, bullet.x, bullet.y):
							enemy.health -= 3
							Explosion = (bullet.x,bullet.y)
							explosions.append(Explosion)
							bullets.pop(bullets.index(bullet))
				
					for bomb in bombs:
						if ColissionDetect(enemy.x, enemy.y, enemy.width, enemy.height, bomb.x, bomb.y):
							enemy.health -= 10
							Explosion = (bomb.x,bomb.y)
							explosions.append(Explosion)
							bombs.pop(bombs.index(bomb))
				else:
					for bullet in bullets:
						if ColissionDetect(enemy.x, enemy.y + 23, enemy.width, enemy.height, bullet.x, bullet.y):
							enemy.health -= 3
							Explosion = (bullet.x, bullet.y)
							explosions.append(Explosion)
							bullets.pop(bullets.index(bullet))
					
					for bomb in bombs:
						if ColissionDetect(enemy.x, enemy.y + 23, enemy.width, enemy.height, bomb.x, bomb.y):
							enemy.health -= 10
							Explosion = (bomb.x, bomb.y)
							explosions.append(Explosion)
							bombs.pop(bombs.index(bomb))
				
				break
			
			if enemy.type < 12:
				if enemy.health <= 0:
					killed.append(enemy.name)
					score += enemy.score
					enemies.pop(enemies.index(enemy))
			else:
				if enemy.health <= 0:
					killed.append(enemy.name)
					score += enemy.score
					run = False
					won = True
					enemies.pop(enemies.index(enemy))
				
		
		for attack in enemyattacks:
			if 0 < attack.x < 1280 and attack.y < 700:
				attack.Move(Plane.x, Plane.y)
				attack.Draw()
			else:
				enemyattacks.pop(enemyattacks.index(attack))
			
			if ColissionDetect(Plane.x, Plane.y, Plane.width, Plane.height, attack.x, attack.y):
				Plane.health -= attack.damage
				Explosion = (attack.x,attack.y)
				explosions.append(Explosion)
				enemyattacks.pop(enemyattacks.index(attack))
		
		Plane.hitbox = (Plane.x, Plane.y + (64 - Plane.height), Plane.width, Plane.height)
		
		if framecount + 1 > 24:
			framecount = 0
	
		if framecount % 6 == 0:
			explosions = []
		framecount += 1
		redrawGameWindow()
		if Plane.health <= 0:
			run = False
			won = False
		
		if keys[pygame.K_SPACE]:
			paused = True

while True:
	clock.tick(40)
	keys = pygame.key.get_pressed()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			
			
	if won:
		winscreen = pygame.image.load('WinScreen.png')
		win.blit(winscreen, (140, 50))
		textplate = font2.render(str(score), True, (0, 0, 0))
		if len(str(score)) == 1:
			win.blit(textplate, (800, 220))
		if len(str(score)) == 2:
			win.blit(textplate, (750, 220))
		if len(str(score)) == 3:
			win.blit(textplate, (700, 220))
		
		pygame.display.flip()
	else:
		lossscreen = pygame.image.load('LossScreen.png')
		win.blit(lossscreen, (140, 50))
		textplate = font2.render(str(score), True, (0, 0, 0))
		if len(str(score)) == 1:
			win.blit(textplate, (800, 220))
		if len(str(score)) == 2:
			win.blit(textplate, (750, 220))
		if len(str(score)) == 3:
			win.blit(textplate, (700, 220))
		
		pygame.display.flip()
	
pygame.quit()
