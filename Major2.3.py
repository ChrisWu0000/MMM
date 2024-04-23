import pygame
from random import *
from math import *
from monster_data import *
from level_data import *
from math import floor
import Spritesheet
pygame.init()
class Enemy(pygame.sprite.Sprite): 
	def __init__(self, name, position):
		super().__init__()
		self.position = pygame.math.Vector2(position) 
		self.name = name
		enemy_info = monster_data[self.name]
		self.sprite_sheet_image = enemy_info["spritesheet"].convert_alpha()
		self.sprite_sheet = Spritesheet.SpriteSheet(self.sprite_sheet_image)
		self.hp = enemy_info["health"]
		self.speed = enemy_info["speed"]
		self.push_power = enemy_info["push_power"]
		self.currentimage = self.sprite_sheet.get_image(0, 80, 80)
		self.image = self.currentimage
		self.damage = enemy_info["attack_damage"]
		self.mass = enemy_info["mass"]
		self.collision_check = False #all of these are used to detect which animation to use
		self.flipped = False
		self.ishit = False
		self.isdead = False
		self.isattacking = False
		self.current_index = 0
		
		self.rect = self.image.get_rect()
		self.rect.center = position
		
		self.collisionrect = self.rect
		self.collisionrect.width = int(0.8*self.collisionrect.width)
		self.collisionrect.height = int(0.8*self.collisionrect.height)
		self.collisionrect.midbottom = self.rect.midbottom

		self.speed_buildupy=0
		self.speed_buildupx=0
		self.frogx =0
		self.frogy =0

		self.i=0
		self.k = 0.1 # 4/self.k = #ticks for animation to loop
		self.walking=[]
		self.flippedwalking=[]
		for x in range(4):
			self.walking.append (self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha())
			self.flippedwalking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha(), True, False))
			self.i+=1

		self.attacking=[]
		self.flippedattacking=[]
		for x in range(4):
			self.attacking.append (self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha())
			self.flippedattacking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha(), True, False))
			self.i+=1

		self.takedamage=[]
		self.flippedtakedamage=[]
		for x in range(4):
			self.takedamage.append (self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha())
			self.flippedtakedamage.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha(), True, False))
			self.i+=1

		self.death=[]
		self.flippeddeath=[]
		for x in range(4):
			self.death.append (self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha())
			self.flippeddeath.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha(), True, False))
			self.i+=1
		self.i = 0
	def check_alive(self): # checks if enemy dies
		if self.hp <=0  and self.isdead == False:
			self.i = 0
			self.isdead = True
			if self.flipped == False:
				self.image = self.death[floor(self.i)]
			else:
				self.image = self.flippeddeath[floor(self.i)]
			enemy_group.remove(self)
			collision_group.remove(self)
		if self.hp <=0  and self.isdead == True:
			if self.flipped == False:
				self.image = self.death[floor(self.i)]
			else:
				self.image = self.flippeddeath[floor(self.i)]
			if self.i >= 4-self.k:
				self.kill()		
	def take_damage(self): #checks if enemy is hit
			if self.ishit == True:
				if self.flipped == False:
					self.image = self.takedamage[floor(self.i)]
				else:
					self.image = self.flippedtakedamage[floor(self.i)]
			if self.i >=4-self.k and self.ishit == True:
				self.ishit = False			
	def attack(self): #checks if enemy should attack
		if self.collision_check == True and self.isattacking == False:
			self.i = 0
			self.isattacking = True
			if self.flipped == False:
				self.image = self.attacking[floor(self.i)]
			else:
				self.image = self.flippedattacking[floor(self.i)]
		if self.isattacking == True:
			if self.flipped == False:
				self.image = self.attacking[floor(self.i)]
			else:
				self.image = self.flippedattacking[floor(self.i)]
		if self.i >=4-self.k and self.isattacking == True:
				self.isattacking = False
				self.collision_check = False	

	def check_collision(self,player): #Chris version of collision
		if self.hp >0:
			self.speed_buildupx += self.direction.x * (self.speed - int(self.speed))
			self.speed_buildupy += self.direction.y * (self.speed - int(self.speed))
			self.frogx = int(self.speed_buildupx)
			self.speed_buildupx = float(self.speed_buildupx)-int(self.speed_buildupx)
			self.frogy = int(self.speed_buildupy)
			self.speed_buildupy =  float(self.speed_buildupy)-int(self.speed_buildupy)
			self.rect.x = self.rect.x + self.direction.x * int(self.speed) + self.frogx
			self.rect.y = self.rect.y + self.direction.y * int(self.speed) + self.frogy
			if self.rect.colliderect(player.rect):
					self.rect.x = self.rect.x - self.direction.x * int(self.speed) + self.frogx
					self.rect.y = self.rect.y - self.direction.y * int(self.speed) + self.frogy
					self.speed -= 0.1
					self.collision_check = True
					self.check_collision(player)


		if self.collision_check == True and pygame.time.get_ticks()-player.lastcollision >= player.iframes and self.i >=4-self.k:
			player.hp -= self.damage
			player.lastcollision = pygame.time.get_ticks()

		self.collisionrect.center = self.rect.center
		
	def update_direction(self):
		self.vector = pygame.Vector2(self.rect.center)
		if 0 != pygame.Vector2.length(player.vector - self.vector):
			self.direction = (player.vector - self.vector).normalize()
			if self.direction.x > 0 and self.hp >=0:
				self.flipped = True
				self.image = self.flippedwalking[floor(self.i)]
			if self.direction.x <0 and self.hp>=0:
				self.flipped = False
				self.image = self.walking[floor(self.i)]			
		

	def update(self,enemy_group,player):
		self.update_direction()
		self.check_collision(player)
		self.take_damage()
		self.attack()
		self.check_alive()
		self.i+=self.k
		if(self.i>=4):
			self.i=0
		if self.hp >0:
			self.speed = monster_data[self.name]["speed"]
		else:
			self.speed = 0

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.image1 = pygame.image.load('Player/Trent.png').convert_alpha()
		self.image2 = pygame.transform.flip(pygame.image.load('Player/Trent.png').convert_alpha(), True, False)
		self.image = self.image1
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.lastx = 0
		self.lasty = 0
		self.speed = 5
		self.hp = 10000
		self.mass = 10
		self.shoot = 0
		self.shoot_cooldown = 0
		self.vector = pygame.Vector2(self.rect.center)
		self.lastcollision = pygame.time.get_ticks()
		self.iframes = 1000 #iframes are measured in miliseconds
	def check_collision(self,enemy_group):
		self.rect.x += self.direction.x * self.speed
		for enemy in enemy_group:
			if self.rect.colliderect(enemy.rect):
				self.rect.x -= self.direction.x * self.speed
				self.speed -= 0.1
				#enemy.collision_check = True
				#self.check_collision(enemy_group)
		self.rect.y += self.direction.y * self.speed
		for enemy in enemy_group:
			if self.rect.colliderect(enemy.rect):
				self.rect.y -= self.direction.y * self.speed
				self.speed -= 0.1
				#enemy.collision_check = True
				#self.check_collision(enemy_group)

	
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
		if self.direction.x !=0 or self.direction.y !=0:
			self.lastx = self.direction.x
			self.lasty = self.direction.y
		
		if pygame.mouse.get_pressed() == (1, 0, 0):
			self.shoot = 1
			#self.is_shooting()
		elif keys[pygame.K_SPACE]:
			self.shoot = 2
			#self.space_shooting()
		else:
			self.shoot=False             
		
	def is_shooting(self):
		self.mouse_coords = pygame.mouse.get_pos() 
		self.lastx = (self.mouse_coords[0] - self.rect.centerx + camera_group.camera_rect.left-camera_group.camera_borders["left"])
		self.lasty = (self.mouse_coords[1] - self.rect.centery + camera_group.camera_rect.top-camera_group.camera_borders["top"])
		self.angle = atan2(self.lasty, self.lastx)
		if self.shoot_cooldown == 0:
			self.shoot_cooldown = 30
			pygame.time.set_timer(shoot_cooldown,100,loops=1)
			spawn_bullet_pos = self.rect.center
			self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
			weapon_group.add(self.bullet)
			camera_group.add(self.bullet)
			all_sprite_group.add(self.bullet)
	def space_shooting(self):
		self.angle = atan2(self.lasty, self.lastx)
		if self.shoot_cooldown == 0:
			self.shoot_cooldown = 30
			pygame.time.set_timer(shoot_cooldown,100,loops=1)
			spawn_bullet_pos = self.rect.center
			self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
			weapon_group.add(self.bullet)
			camera_group.add(self.bullet)
			all_sprite_group.add(self.bullet)
	def check_alive(self): # checks if self is alive
		if self.hp <= 0:
			self.kill()
	def update(self,enemy_group,player):
		self.check_alive()
		self.input()
		self.check_collision(enemy_group)
		if self.shoot_cooldown > 0: # Just shot a bullet
			self.shoot_cooldown -= 1
		if self.shoot == 1:
			self.is_shooting()
		elif self.shoot == 2:
			self.space_shooting()
		self.vector = pygame.Vector2(self.rect.center)
		self.speed = 5

class Bullet(pygame.sprite.Sprite): 
	def __init__(self, x, y, angle): 
		super().__init__()
		self.image = pygame.image.load("Weapons/Bullet.png")
		self.image = pygame.transform.rotozoom(self.image, 0, 5)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.x = x
		self.y = y
		self.speed = 10
		self.angle = angle
		self.damage = 50
		self.velx = cos(self.angle)*self.speed
		self.vely = sin(self.angle)*self.speed
		self.bullet_lifetime = 750
		self.spawn_time = pygame.time.get_ticks()
 
	def check_collision(self):
		for x in enemy_group.sprites():
			if self.rect.colliderect(x.collisionrect):
				x.hp -= self.damage
				x.ishit = True
				if x.collision_check == False:
					x.i = 0
				self.kill() 
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
		self.level = level_data[1]
		self.background_image = self.level["room"].convert_alpha()
		self.bg_rect = self.background_image.get_rect(midtop = (self.half_w,0))
		self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
		l = self.camera_borders['left']
		t = self.camera_borders['top']
		w = self.surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
		h = self.surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
		self.camera_rect = pygame.Rect(l,t,w,h)

	def center_target_camera(self,target):
		if target.rect.left < self.camera_rect.left:
			self.camera_rect.left = max(target.rect.left, self.bg_rect.x, )
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
for i in range(camera_group.level["num_bell"]):
	random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
	random_y = randint(camera_group.bg_rect.y,camera_group.background_image.get_size()[1]-200)
	extra=Enemy("bell", (random_x,random_y))
	camera_group.add(extra)
	enemy_group.add(extra)
	collision_group.add(extra)
	all_sprite_group.add(extra)
for i in range(camera_group.level["num_sax"]):
	random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
	random_y = randint(camera_group.bg_rect.y,camera_group.background_image.get_size()[1]-200)
	extra=Enemy("sax", (random_x,random_y))
	camera_group.add(extra)
	enemy_group.add(extra)
	collision_group.add(extra)
	all_sprite_group.add(extra)
meep = True
sparetimer1 = pygame.USEREVENT + 1
#pygame.time.set_timer(sparetimer1,1000)
shoot_cooldown = pygame.USEREVENT + 2
#next_level = pygame.USEREVENT + 3
while meep:
	#if player_group.has(player) == False: #If player dies, game ends
			#meep = False
	#if len(enemy_group) == 0: #No enemies left, game ends
		#meep = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			meep = False
		if event.type == sparetimer1:
			print(int(7.5))
		if event.type == shoot_cooldown:
			player.shoot_cooldown = 0
		#if event.type == next_level:
			#print("yay")
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				meep = False
			if event.key == pygame.K_9 and len(enemy_group)==0 and player.rect.x <= 1750 and player.rect.x >= 1500 and player.rect.y <= 200:
				camera_group.level = level_data[2]
				camera_group.background_image = camera_group.level["room"].convert_alpha()
				camera_group.bg_rect = camera_group.background_image.get_rect(midtop = (camera_group.half_w,0))
				camera_group.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
				l = camera_group.camera_borders['left']
				t = camera_group.camera_borders['top']
				w = camera_group.surface.get_size()[0]  - (camera_group.camera_borders['left'] + camera_group.camera_borders['right'])
				h = camera_group.surface.get_size()[1]  - (camera_group.camera_borders['top'] + camera_group.camera_borders['bottom'])
				camera_group.camera_rect = pygame.Rect(l,t,w,h)
				player.rect.center = (camera_group.bg_rect[2]/2, camera_group.bg_rect[3])
				for i in range(camera_group.level["num_bell"]): #Spawns enemies
					random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
					random_y = randint(camera_group.bg_rect.y,camera_group.background_image.get_size()[1]-200)
					extra=Enemy("bell", (random_x,random_y))
					camera_group.add(extra)
					enemy_group.add(extra)
					collision_group.add(extra)
					all_sprite_group.add(extra)
				for i in range(camera_group.level["num_sax"]): #Spawns enemies
					random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
					random_y = randint(camera_group.bg_rect.y,camera_group.background_image.get_size()[1]-200)
					extra=Enemy("sax", (random_x,random_y))
					camera_group.add(extra)
					enemy_group.add(extra)
					collision_group.add(extra)
					all_sprite_group.add(extra)
			
				
	camera_group.update(enemy_group,player)
	camera_group.custom_draw(player)
 
	pygame.display.update()
	clock.tick(120)