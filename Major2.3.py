import pygame
from random import *
pygame.init()
"""class spritedata:
  def __init__(self,width,height,x,y,speedx,speedy):
    self.w=width
    self.h=height
    self.x=float(x)
    self.y=float(y)
    self.speedx=float(speedx)
    self.speedy=float(speedy)"""
class Bell(pygame.sprite.Sprite):#Base enemy class, not Bell specifically
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('Enemies/Bell.png').convert_alpha()
		self.rect = self.image.get_rect(midtop = pos)
		self.hpmax
		self.hp
		self.damage
		self.speed
		self.tickspeed
		#Method to attack:
			#Different for each enemy
		#Method to display sprites:
			#while (y direction != 0 & x direction != 0):
				#Cycle through walking animation at tickspeed
			#while (y direction != 0 & x direction != 0):
				#Cycle through idle animation at tickspeed
			#if (hp is reduced):
				#Display damage sprite
				#Knockback
class Player(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('Enemies/DevlinDeving.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed
class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.surface=pygame.display.get_surface()		
		self.offset = pygame.math.Vector2()
		self.half_w = self.surface.get_size()[0] // 2
		self.half_h = self.surface.get_size()[1] // 2
		self.background_image = pygame.image.load("Rooms/BossRoom.png").convert_alpha()
		self.bg_rect = self.background_image.get_rect(midtop = (self.half_w,0))
	def center_target_camera(self,target):
		self.offset.x = 0
		self.offset.y = target.rect.centery - self.half_h
	def custom_draw(self, player):
		self.center_target_camera(player)
		ground_offset = self.bg_rect.topleft - self.offset 
		self.surface.blit(self.background_image,ground_offset)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.surface.blit(sprite.image,offset_pos)
"""def create_sprite(width, height, x, y,imagedata):
  sprite = pygame.sprite.Sprite()
  size = (width,height)
  position = (x,y)
  sprite.rect = pygame.Rect(position, size)
  sprite.image = pygame.image.load(imagedata)
  return sprite
def player_sprite():
  players = pygame.sprite.Sprite()
  size = (20,20)
  position = (140,90)
  players.rect = pygame.Rect(position, size)
  players.image = pygame.Surface(players.rect.size)
  players.image.fill((100,50,100))
  return players
flags = pygame.SCALED
window = pygame.display.set_mode((300, 200),flags, vsync=1)
camera = pygame.Rect(0, 0, 300, 200)
clock = pygame.time.Clock()
#---DO NOT GO OVER 500 SPRITES!!!!!!---
spritesdata = [spritedata(300,200,0,0,0,0)]
bg = pygame.image.load('Enemies/DevlinDeving.png')
bg_width = bg.get_width()
bg_height =bg.get_height()
spriterects = [create_sprite(bg_width, bg_height, 0,0,'Enemies/DevlinDeving.png')]
for x in range(1):
  for y in range(1):
    spriterects.append(create_sprite(15,20,60*x,60*y,'Enemies/Enemy1.png'))
    spritesdata.append(spritedata(15,20,60*x,60*y,0,0))
#spriterects[0].image.convert_alpha()
playersprite = player_sprite()
playerdata = spritedata(20, 20, 140, 90,0,0)


speed=0.8
running = True
fox = pygame.key.get_pressed()
cooldown=0
timer = pygame.time.Clock() 
sparetimer1 = pygame.USEREVENT + 1
pygame.time.set_timer(sparetimer1,5000)
cooldownup1 = pygame.USEREVENT + 2"""
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
camera_group = CameraGroup()
player = Player((640,360),camera_group)
for i in range(10):
	random_x = randint(140,1140)
	random_y = randint(0,1000)
	Bell((random_x,random_y),camera_group)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()


	screen.fill('#71ddee')

	camera_group.update()
	camera_group.custom_draw(player)
 

	pygame.display.update()
	clock.tick(60)