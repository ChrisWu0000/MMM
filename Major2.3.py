import pygame
from random import *
pygame.init()
class Bell(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('Enemies/Bell.png').convert_alpha()
		self.rect = self.image.get_rect(midtop = pos)
		self.collisionrect = self.image.get_rect(midtop = pos)
		self.collisionrect.width -= 60
		self.collisionrect.height -= 60
		self.collisionrect.move_ip(30,30)
class Player(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('Enemies/DevlinDeving.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP] == keys[pygame.K_DOWN]:
			self.direction.y = 0
		elif keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		if keys[pygame.K_RIGHT] == keys[pygame.K_LEFT]:
			self.direction.x = 0
		elif keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
	def update(self,bells):
		
		
		self.input()
		
		
		self.rect.x += self.direction.x * self.speed
		if camera_group.bg_rect.contains(self) == False:
			self.rect.centerx = camera_group.bg_rect.centerx + self.direction.x * (camera_group.bg_rect.centerx - (camera_group.bg_rect.x + 1 + self.rect.width/2))
		self.rect.y += self.direction.y * self.speed
		for x in range(len(bells)):
			self.rect.y -= self.direction.y * self.speed
			if self.rect.colliderect(bells[x].collisionrect):
				self.rect.centerx = bells[x].rect.centerx - self.direction.x * (bells[x].rect.centerx - (bells[x].rect.x - 1 - self.rect.width/2))
			self.rect.y += self.direction.y * self.speed
			if self.rect.colliderect(bells[x].collisionrect):
				self.rect.centery = bells[x].rect.centery - self.direction.y * (bells[x].rect.centery - (bells[x].rect.y - 1 - self.rect.height/2))
		if camera_group.bg_rect.contains(self) == False:
			self.rect.centery = camera_group.bg_rect.centery + self.direction.y * (camera_group.bg_rect.centery - (camera_group.bg_rect.y + 1 + self.rect.height/2))


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.surface=pygame.display.get_surface()		
		self.offset = pygame.math.Vector2()
		self.half_w = self.surface.get_size()[0] // 2
		self.half_h = self.surface.get_size()[1] // 2
		self.background_image = pygame.image.load("Rooms/BossRoom.png").convert_alpha()
		self.bg_rect = self.background_image.get_rect(midtop = (self.half_w,-(self.half_h)))
	def center_target_camera(self,target):
				
		if target.rect.centerx <=1000 and target.rect.centerx >=360:
			self.offset.x = target.rect.centerx - self.half_w
		if target.rect.centery <=self.bg_rect.height-600 and target.rect.centery >=0:
			self.offset.y = target.rect.centery - self.half_h



	def custom_draw(self, player):
		self.center_target_camera(player)
		ground_offset = self.bg_rect.topleft - self.offset 
		self.surface.blit(self.background_image,ground_offset)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.surface.blit(sprite.image,offset_pos)
			

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
camera_group = CameraGroup()
player = Player((640,360),camera_group)
bells = []
bellshitbox=[]
for i in range(5):
	random_x = randint(140,1140)
	random_y = randint(0,1000)
	extra=Bell((random_x,random_y),camera_group)
	bells.append(extra)
meep = True
sparetimer1 = pygame.USEREVENT + 1
#pygame.time.set_timer(sparetimer1,1000)
while meep:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			meep = False
		if event.type == sparetimer1:
			print(bells[1].collisionrect,bells[1].rect,player.rect)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				meep = False


	screen.fill('#71ddee')
	camera_group.update(bells)
	camera_group.custom_draw(player)
 

	pygame.display.update()
	clock.tick(60)