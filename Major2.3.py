import pygame
from random import *
pygame.init()
class Enemy(pygame.sprite.Sprite):
	def __init(self, pos, *group):
		super().__init__(*group)
		self.pos = pos
		
class Bell(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
		self.image1 = pygame.image.load('Enemies/Sax.png').convert_alpha()
		self.image2 = pygame.transform.flip(pygame.image.load('Enemies/Sax.png').convert_alpha(), True, False)
		self.image = self.image1
		self.rect = self.image.get_rect(midtop = pos)
		self.collisionrect = self.image.get_rect(midtop = pos)
		self.collisionrect.width -= 60
		self.collisionrect.height -= 60
		self.collisionrect.move_ip(30,30)
	


class Player(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image1 = pygame.image.load('Player/DevlinDeving.png').convert_alpha()
		self.image2 = pygame.transform.flip(pygame.image.load('Player/DevlinDeving.png').convert_alpha(), True, False)
		self.image = self.image1
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
			self.image=self.image2
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.image=self.image1
	def update(self,bells):
		
		
		self.input()
		
		
		self.rect.x += self.direction.x * self.speed
		self.rect.y += self.direction.y * self.speed
		for x in range(len(bells)):
			self.rect.y -= self.direction.y * self.speed
			if self.rect.colliderect(bells[x].collisionrect):
				self.rect.centerx = bells[x].rect.centerx - self.direction.x * (bells[x].rect.centerx - (bells[x].rect.x - 1 - self.rect.width/2)-30)
			self.rect.y += self.direction.y * self.speed
			if self.rect.colliderect(bells[x].collisionrect):
				self.rect.centery = bells[x].rect.centery - self.direction.y * (bells[x].rect.centery - (bells[x].rect.y - 1 - self.rect.height/2)-30)


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.surface=pygame.display.get_surface()	
		self.offset = pygame.math.Vector2()
		self.half_w = self.surface.get_size()[0] // 2
		self.half_h = self.surface.get_size()[1] // 2
		self.surface_rect = self.surface.get_rect(midtop = (self.half_w,0))
		self.background_image = pygame.image.load("Rooms/Level1.png").convert_alpha()
		self.bg_rect = self.background_image.get_rect(midtop = (self.half_w,0))
		self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
		l = self.camera_borders['left']
		t = self.camera_borders['top']
		w = self.surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
		h = self.surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
		self.camera_rect = pygame.Rect(l,t,w,h)

	def center_target_camera(self,target):
		if target.rect.left < self.camera_rect.left:
			self.camera_rect.left = max(target.rect.left, min(self.bg_rect.x, 10000))
			target.rect.left = self.camera_rect.left
			self.camera_rect.left = max(target.rect.left, self.bg_rect.x+self.camera_borders['left'])
			if self.bg_rect.x > target.rect.left:
				target.rect.left = self.camera_rect.left- self.camera_borders['left']
		if target.rect.right > self.camera_rect.right:
			self.camera_rect.right = min(target.rect.right, self.bg_rect.right)
			target.rect.right = self.camera_rect.right
			self.camera_rect.right = min(target.rect.right, self.bg_rect.right-self.camera_borders['right'])
			if self.bg_rect.right < target.rect.right:
				target.rect.right = self.camera_rect.right + self.camera_borders['right']
		if target.rect.top < self.camera_rect.top:
			self.camera_rect.top = max(target.rect.top, self.bg_rect.y)
			target.rect.top = self.camera_rect.top
			self.camera_rect.top = max(target.rect.top, self.bg_rect.y+self.camera_borders['top'])
			if self.bg_rect.y > target.rect.top:
				target.rect.top = self.camera_rect.top-self.camera_borders['top']
		if target.rect.bottom > self.camera_rect.bottom:
			self.camera_rect.bottom = min(target.rect.bottom, self.bg_rect.bottom)
			target.rect.bottom = self.camera_rect.bottom
			
			self.camera_rect.bottom = min(target.rect.bottom, self.bg_rect.bottom-self.camera_borders['bottom'])
			if self.bg_rect.bottom < target.rect.bottom:
				target.rect.bottom = self.camera_rect.bottom + self.camera_borders['bottom']
				
		self.offset.x = self.camera_rect.left - self.camera_borders['left']
		self.offset.y = self.camera_rect.top - self.camera_borders['top']
	def custom_draw(self, player):
		self.center_target_camera(player)
		ground_offset = self.bg_rect.topleft - self.offset 
		self.surface.blit(self.background_image,ground_offset)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.surface.blit(sprite.image,offset_pos)
		#pygame.draw.rect(self.surface, "red", self.surface_rect, 10)
		#pygame.draw.rect(self.surface, "red", self.bg_rect, 5)

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
camera_group = CameraGroup()
player = Player((640,360),camera_group)
bells = []
for i in range(50):
	random_x = randint(camera_group.bg_rect.x,camera_group.background_image.get_size()[0])
	random_y = randint(camera_group.bg_rect.y,camera_group.background_image.get_size()[1])
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
			print(camera_group.bg_rect.height,player.rect.y)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				meep = False


	#screen.fill('#6b6b6b')
	camera_group.update(bells)
	camera_group.custom_draw(player)
 

	pygame.display.update()
	clock.tick(120)