import pygame
from random import *
from math import *
from monster_data import *
pygame.init()
class Enemy(pygame.sprite.Sprite): 
	def __init__(self, name, position):
		super().__init__()
		self.position = pygame.math.Vector2(position) 
		self.name = name

		enemy_info = monster_data[self.name]
		self.hp = enemy_info["health"]
		self.speed = enemy_info["speed"]
		self.push_power = enemy_info["push_power"]
		self.image_default = enemy_info["image"].convert_alpha()
		self.image_flipped = pygame.transform.flip(enemy_info["image"].convert_alpha(), True, False)
		self.image = self.image_default
		self.damage = enemy_info["attack_damage"]
		self.mass = enemy_info["mass"]
		#self.import_graphics(name)

		self.current_index = 0

		#self.image.set_colorkey((0,0,0))
		#self.base_zombie_image = self.image
		
		self.rect = self.image.get_rect()
		self.rect.center = position
		
		self.collisionrect = self.rect
		self.collisionrect.width = int(0.8*self.collisionrect.width)
		self.collisionrect.height = int(0.8*self.collisionrect.height)
		self.collisionrect.midbottom = self.rect.midbottom

	def check_alive(self): # checks if enemy dies
		if self.hp <= 0:
			self.kill()
			
		
						
	def check_collision(self,player):
		
		x_direction = self.direction.x
		y_direction = self.direction.y
		self.rect.y -= y_direction * self.speed
		self.collisionrect.topleft = self.rect.topleft
		self.collisionrect.move_ip(30,30)
		if self.collisionrect.colliderect(player.rect):
			self.rect.centerx = player.rect.centerx - x_direction * (player.rect.centerx - (player.rect.x - 1 - self.rect.width/2)+60)
		self.rect.y += y_direction * self.speed
		self.collisionrect.topleft = self.rect.topleft
		self.collisionrect.move_ip(30,30)
		if self.collisionrect.colliderect(player.rect):
			self.rect.centery = player.rect.centery - y_direction * (player.rect.centery - (player.rect.y - 1 - self.rect.height/2)+60)
			self.collisionrect.topleft = self.rect.topleft
			self.collisionrect.move_ip(30,30)

	"""def hunt_player(self,player):  
		self.vector = pygame.Vector2(self.rect.center)
		if 0 != pygame.Vector2.length(player.vector - self.vector):
			self.direction = round((player.vector - self.vector).normalize())
			if self.direction.x > 0:
				self.image = self.image_flipped
			if self.direction.x <0:
				self.image = self.image_default
			self.rect.center = self.rect.center + self.direction * self.speed
			self.collisionrect.midbottom = self.rect.midbottom
			if player.rect.colliderect(self.collisionrect):
				player.rect.center += self.direction * (self.push_power)"""
				
		

	def update(self,enemy_group,player):
		#self.hunt_player(player)
		self.check_collision(player)
		self.check_alive()




class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.image1 = pygame.image.load('Player/Trent.png').convert_alpha()
		self.image2 = pygame.transform.flip(pygame.image.load('Player/Trent.png').convert_alpha(), True, False)
		self.image = self.image1
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.hp = 1000000
		self.mass = 10
		self.shoot = False
		self.shoot_cooldown = 0
		self.alive = True
		self.vector = pygame.Vector2(self.rect.center)
		self.lastcollision = pygame.time.get_ticks()
		self.iframes = 1000 #iframes are measured in miliseconds
	def check_collision(self,enemy_group):
		print("hi")

	
	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w] == keys[pygame.K_s]:
			self.direction.y = 0
		elif  keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		if  keys[pygame.K_d] == keys[pygame.K_a]:
			self.direction.x = 0
		elif keys[pygame.K_d]:
			self.direction.x = 1
			self.image=self.image2
		elif keys[pygame.K_a]:
			self.direction.x = -1
			self.image=self.image1
		
		if pygame.mouse.get_pressed() == (1, 0, 0):
			self.shoot = True
			self.is_shooting()
		else:
			self.shoot=False             
		
		if event.type == pygame.KEYUP:
			if pygame.mouse.get_pressed() == (1, 0, 0):
				self.shoot = False
	def is_shooting(self):
		global meep
		self.mouse_coords = pygame.mouse.get_pos() 
		self.x_change_mouse_player = (self.mouse_coords[0] - self.rect.centerx + camera_group.camera_rect.left-camera_group.camera_borders["left"])
		self.y_change_mouse_player = (self.mouse_coords[1] - self.rect.centery + camera_group.camera_rect.top-camera_group.camera_borders["top"])
		self.angle = atan2(self.y_change_mouse_player, self.x_change_mouse_player)
		if self.shoot_cooldown == 0 and self.shoot:
			self.shoot_cooldown = 10
			spawn_bullet_pos = self.rect.center
			self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
			weapon_group.add(self.bullet)
			camera_group.add(self.bullet)
			all_sprite_group.add(self.bullet)
	def check_alive(self): # checks if self is alive
		if self.hp <= 0:
			self.alive = False
		if self.alive == False:
			self.kill()
	def update(self,enemy_group,player):
		if self.shoot_cooldown > 0: # Just shot a bullet
			self.shoot_cooldown -= 1
		if self.shoot:
			self.is_shooting()
		self.check_alive()
		self.input()
		self.rect.x += self.direction.x * self.speed
		self.rect.y += self.direction.y * self.speed
		self.vector = pygame.Vector2(self.rect.center)


class Bullet(pygame.sprite.Sprite): 
	def __init__(self, x, y, angle): 
		super().__init__()
		self.image = pygame.image.load("Weapons/Bullet.png")
		self.image = pygame.transform.rotozoom(self.image, 0, 5)
		#self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.x = x
		self.y = y
		self.speed = 10
		self.angle = angle
		self.damage = 5
		self.velx = cos(self.angle)*self.speed
		self.vely = sin(self.angle)*self.speed
		self.bullet_lifetime = 750
		self.spawn_time = pygame.time.get_ticks()
 
	def check_collision(self):
		for x in enemy_group.sprites():
			if self.rect.colliderect(x.collisionrect):
				self.kill()
				x.hp -= self.damage
				x.check_alive()
				 
	def update(self,enemy_group,player):
		self.rect.x +=self.velx
		self.rect.y +=self.vely
		self.rect.x = int(self.rect.x)
		self.rect.y = int(self.rect.y)
		self.check_collision()
		if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime: 
			self.kill()
		
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
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.bottom):
			offset_pos = sprite.rect.topleft - self.offset
			self.surface.blit(sprite.image,offset_pos)
		#pygame.draw.rect(self.surface, "red", self.surface_rect, 10)
		#pygame.draw.rect(self.surface, "red", self.bg_rect, 5)

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
camera_group = CameraGroup()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
collision_group = pygame.sprite.Group()
physics_group = pygame.sprite.Group()
all_sprite_group = pygame.sprite.Group()
player = Player((640,360))
collision_group.add(player)
player_group.add(player)
physics_group.add(player)
camera_group.add(player)
all_sprite_group.add(player)
for i in range(10):
	random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
	random_y = randint(camera_group.bg_rect.y,camera_group.background_image.get_size()[1]-200)
	extra=Enemy("sax", (random_x,random_y))
	camera_group.add(extra)
	enemy_group.add(extra)
	collision_group.add(extra)
	all_sprite_group.add(extra)
for i in range(10):
	random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
	random_y = randint(camera_group.bg_rect.y,camera_group.background_image.get_size()[1]-200)
	extra=Enemy("bell", (random_x,random_y))
	camera_group.add(extra)
	enemy_group.add(extra)
	collision_group.add(extra)
	all_sprite_group.add(extra)
meep = True
sparetimer1 = pygame.USEREVENT + 1
#pygame.time.set_timer(sparetimer1,1000)
while meep:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			meep = False
		if event.type == sparetimer1:
			print("e")
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				meep = False

	#screen.fill('#6b6b6b')
	camera_group.update(enemy_group,player)
	camera_group.custom_draw(player)
 
	pygame.display.update()
	clock.tick(120)