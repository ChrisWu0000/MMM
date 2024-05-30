from typing import Any
import pygame
from random import random, randint
from math import *
from Difficulties import *
import pygame.freetype
from monster_data import *
from level_data import *
from prop_data import *
from weapon_data import *
from math import floor
import Spritesheet
import sys
pygame.init()
global bosspresent, wave
wave = 1
levelnum = 1
bosspresent=False

def get_font(size):
	return pygame.font.SysFont('Perpetua', size)
my_font = get_font(30)
difficulty_mult = 1
class Enemy(pygame.sprite.Sprite): 
	def __init__(self, name, position):
		super().__init__()
		self.position = pygame.math.Vector2(position) 
		self.name = name
		self.weapon = weapon_data[self.name]
		enemy_info = monster_data[self.name]
		self.sprite_sheet_image = enemy_info["spritesheet"].convert_alpha()
		self.sprite_sheet = Spritesheet.SpriteSheet(self.sprite_sheet_image)
		self.hp = int(enemy_info["health"]*difficulty_mult)
		self.speed = int(enemy_info["speed"]*difficulty_mult)
		self.push_power = enemy_info["push_power"]
		self.currentimage = self.sprite_sheet.get_image(0, enemy_info["sprite_width"], enemy_info["sprite_height"],enemy_info["sprite_width"] )
		self.image = self.currentimage
		self.damage = int(enemy_info["attack_damage"]*difficulty_mult)
		self.mass = enemy_info["mass"]
		self.collision_check = False #all of these are used to detect which animation to use
		self.flipped = False
		self.ishit = False
		self.isdead = False
		self.isattacking = False
		self.enemylist = []
		self.current_index = 0
		self.shoot_cooldown = 0
		self.coin_drop_chance = enemy_info["coin_drop_chance"]
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.collisionrect = pygame.Rect(self.rect)
		self.collisionrect.width = int(0.5*self.collisionrect.width)
		self.collisionrect.height = int(0.7*self.collisionrect.height)
		self.collisionrect.midbottom = self.rect.midbottom
		self.speed_buildupy=0
		self.speed_buildupx=0
		self.frogx =0
		self.frogy =0
		self.b = (1-2*randint(0, 1)) #for sax stuff
		self.i = 0
		self.i2 = 0
		self.j = 0
		self.k = 0.05 # 4/self.k = #ticks for animation to loop
		self.walking=[]
		self.flippedwalking=[]
		for x in range(4):
			self.walking.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha())
			self.flippedwalking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha(), True, False))
			self.i+=1

		self.attacking=[]
		self.flippedattacking=[]
		for x in range(4):
			self.attacking.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha())
			self.flippedattacking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha(), True, False))
			self.i+=1

		self.takedamage=[]
		self.flippedtakedamage=[]
		for x in range(4):
			self.takedamage.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha())
			self.flippedtakedamage.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha(), True, False))
			self.i+=1

		self.death=[]
		self.flippeddeath=[]
		for x in range(4):
			self.death.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha())
			self.flippeddeath.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha(), True, False))
			self.i+=1
		self.i = 0
	def check_alive(self): # checks if enemy dies
		if self.hp <=0  and self.isdead == False:
			self.i = 0
			self.isdead = True
			self.k =0.1
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
				if random() <= self.coin_drop_chance:
					for i in range(monster_data[self.name]["coin_drop"]):
						Item("Coin", (self.rect.centerx+30*(i**0.00001)*(-1)**i, self.rect.centery))
				self.kill()
				self.k = 0.05
				
	def update_direction(self):
			self.vector = pygame.Vector2(self.rect.center)
			if 0 != pygame.Vector2.length(player.vector - self.vector):
				self.direction = (player.vector - self.vector).normalize()
				if self.direction.x > 0 and self.hp >=0:
					self.flipped = True
					self.image = self.flippedwalking[floor(self.i)]
				if self.direction.x <=0 and self.hp>=0:
					self.flipped = False
					self.image = self.walking[floor(self.i)]	
					
	def take_damage(self): #checks if enemy is hit
			if self.ishit == True:
				mask = pygame.mask.from_surface(self.image)
				self.image = mask.to_surface()
				self.image.set_colorkey((0,0,0))

			if self.ishit == True and framenum-self.j > 24:	#can change this, #of frames of white
				self.ishit = False			
	def attack(self,player): #checks if enemy should attack
		if self.hp > 0:
			if self.weapon["ranged"]==False:
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

			elif self.weapon["ranged"]==True:
				if self.shoot_cooldown == 0 and self.isattacking == False:
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
				if self.name == 'drum' and self.i2 >=8-self.k and self.isattacking == True:
					self.isattacking = False
					self.collision_check = False
					self.aim = (player.rect.center)
					self.shoot()
				if self.i >=4-self.k and self.isattacking == True:
						self.isattacking = False
						self.collision_check = False
						self.aim = (player.rect.center)
						self.shoot()
	def shoot(self):
		projectiles = self.weapon["projectiles"]
		self.lastx = (self.aim[0] - self.rect.centerx)
		self.lasty = (self.aim[1] - self.rect.centery)
		self.angle = atan2(self.lasty, self.lastx)
		if self.shoot_cooldown == 0:
			self.shoot_cooldown = self.weapon["cooldown"] + randint(0,50)
			spawn_bullet_pos = self.rect.center
			for x in range(projectiles):
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + randint(-self.weapon["spread"],self.weapon["spread"])/100,self.weapon)
				enemy_weapon_group.add(self.bullet)
				camera_group.add(self.bullet)
				all_sprite_group.add(self.bullet)
				
	def check_collision(self,player): #Chris version of collision
		if self.hp >0:
			if self.name == "sax" and dist(self.rect.center, player.rect.center) < 1000: # SAX stuff

				a = self.b*self.direction.x
				if self.b < 0:
					self.direction.x  = self.direction.y
				else:
					self.direction.x  = -self.direction.y
				self.direction.y = a
			self.speed_buildupx += self.direction.x * (self.speed - int(self.speed))
			self.speed_buildupy += self.direction.y * (self.speed - int(self.speed))
			self.frogx = int(self.speed_buildupx)
			self.speed_buildupx = float(self.speed_buildupx)-int(self.speed_buildupx)
			self.frogy = int(self.speed_buildupy)
			self.speed_buildupy =  float(self.speed_buildupy)-int(self.speed_buildupy)
			self.rect.x = self.rect.x + self.direction.x * int(self.speed) + self.frogx
			self.rect.y = self.rect.y + self.direction.y * int(self.speed) + self.frogy
			self.collisionrect.midbottom = self.rect.midbottom
			for enemy in enemy_group:
				if dist(self.collisionrect.center, enemy.collisionrect.center)<10 and enemy != self:
					self.rect.x = self.rect.x - self.direction.x * int(self.speed) + self.frogx+2*(10-20*random())
					self.rect.y = self.rect.y - self.direction.y * int(self.speed) + self.frogy+2*(10-20*random())
					self.collisionrect.midbottom = self.rect.midbottom
					self.speed -= 0.1
					#self.check_collision(player)
				if dist(self.collisionrect.center, enemy.collisionrect.center)<50 and enemy != self:
					if self.rect.bottom == enemy.rect.bottom and self.rect.bottom < player.rect.bottom and (self.rect.left <= enemy.rect.right or self.rect.right >= enemy.rect.left):
						self.rect.y -=0.01
					elif self.rect.bottom == enemy.rect.bottom and self.rect.bottom > player.rect.bottom and (self.rect.left <= enemy.rect.right or self.rect.right >= enemy.rect.left):
						self.rect.y +=0.01

			if self.collisionrect.colliderect(player.rect) and player.dashing == False:
					self.rect.x = self.rect.x - self.direction.x * int(self.speed) + self.frogx
					self.rect.y = self.rect.y - self.direction.y * int(self.speed) + self.frogy
					self.collisionrect.midbottom = self.rect.midbottom
					self.speed -= 0.8
					self.collision_check = True
					self.check_collision(player)
			self.rect.left = max(camera_group.bg_rect.x, self.rect.left)
			self.rect.right = min(camera_group.bg_rect.right, self.rect.right)
			self.rect.top = max(camera_group.level["top wall"], self.rect.top)
			self.rect.bottom = min(camera_group.level["bottom wall"], self.rect.bottom)
			#for x in enemy_group:
				#if self.rect.y == x.rect.y and self !=x:
					#self.rect.y += 0.01		
		if self.collision_check == True and player.lastcollision >= player.iframes and self.i >=4-self.k:
			player.hp -= self.damage
			player.lastcollision = 0
	def update(self,enemy_group,player):
		self.update_direction()
		self.check_collision(player)
		self.attack(player)
		self.take_damage()
		self.check_alive()
		self.i+=self.k
		self.i2+=self.k
		if player.lastcollision < player.iframes:
			player.lastcollision +=1
		if self.shoot_cooldown >0:
			self.shoot_cooldown -= 1
		if(self.i>=4):
			self.i=0
		if(self.i2>=8 and self.type=='drum'):
			self.i2=0
		elif(self.i2>=4):
			self.i2=0
		if self.hp >0:
			self.speed = monster_data[self.name]["speed"]
		else:
			self.speed = 0
		self.enemylist = []

class Boss(pygame.sprite.Sprite):
	global bosspresent
	def __init__(self, position):
		super().__init__()
		self.position = pygame.math.Vector2(position) 
		self.name = 'top_brass'
		enemy_info = monster_data[self.name]
		self.weapon1 = weapon_data['top_brass1']
		self.weapon2 = weapon_data['top_brass2']
		self.sprite_sheet_image = enemy_info["spritesheet"].convert_alpha()
		self.sprite_sheet = Spritesheet.SpriteSheet(self.sprite_sheet_image)
		self.maxhp = enemy_info["health"]*difficulty_mult*difficulty_mult
		self.hp = self.maxhp
		self.ratio = self.hp/self.maxhp
		self.speed = enemy_info["speed"]*difficulty_mult*difficulty_mult
		self.push_power = enemy_info["push_power"]
		self.currentimage = self.sprite_sheet.get_image(0, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"])
		self.image = self.currentimage
		self.damage = enemy_info["attack_damage"]*difficulty_mult*difficulty_mult
		self.mass = enemy_info["mass"]
		self.collision_check = False #all of these are used to detect which animation to use
		self.flipped = False
		self.ishit = False
		self.isdead = False
		self.current_index = 0
		self.isattacking1 = False
		self.isattacking2 = False
		self.shoot_cooldown1 =self.weapon1["cooldown"]
		self.shoot_cooldown2 =self.weapon2["cooldown"]
		self.i1 = 0
		self.i2 = 0
		self.rect = self.image.get_rect()
		self.rect.center = position
		
		self.collisionrect = self.rect
		self.collisionrect.width = int(0.8*self.collisionrect.width)
		self.collisionrect.height = int(0.9*self.collisionrect.height)
		self.collisionrect.midbottom = self.rect.midbottom

		self.speed_buildupy=0
		self.speed_buildupx=0
		self.frogx =0
		self.frogy =0

		self.i=0
		self.k = 0.05 # 4/self.k = #ticks for animation to loop
		self.walking=[]
		self.flippedwalking=[]
		for x in range(4):
			self.flippedwalking.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha())
			self.walking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha(), True, False))
			self.i+=1

		self.attack1=[]
		self.flippedattack1=[]
		for x in range(4):
			self.flippedattack1.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha())
			self.attack1.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha(), True, False))
			self.i+=1
		
		self.attack2=[]
		self.flippedattack2=[]
		for x in range(8):
			self.flippedattack2.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha())
			self.attack2.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha(), True, False))
			self.i+=1

		self.takedamage=[]
		self.flippedtakedamage=[]
		for x in range(4):
			self.flippedtakedamage.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha())
			self.takedamage.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha(), True, False))
			self.i+=1

		self.death=[]
		self.flippeddeath=[]
		for x in range(12):
			self.flippeddeath.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha())
			self.death.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"]).convert_alpha(), True, False))
			self.i+=1
		self.i = 0

	def check_alive(self): # checks if enemy dies
		if self.hp <=0  and self.isdead == False:
			self.i = 0
			self.k = self.k*1.5
			self.isdead = True
			if self.flipped == False:
				self.image = self.death[floor(self.i)]
			else:
				self.image = self.flippeddeath[floor(self.i)]
			enemy_group.remove(self)
			bosspresent = False
			collision_group.remove(self)
		if self.hp <=0  and self.isdead == True:
			if self.flipped == False:
				self.image = self.death[floor(self.i)]
			else:
				self.image = self.flippeddeath[floor(self.i)]
			if self.i >= 12-self.k:
				self.kill()
				bosspresent = False
				player.hp = player.maxhp		
	def take_damage(self): #checks if enemy is hit
			if self.ishit == True:
				if self.flipped == False:
					self.image = self.takedamage[floor(self.i1)]
				else:
					self.image = self.flippedtakedamage[floor(self.i1)]
			if self.i >=4-self.k and self.ishit == True:
				self.ishit = False			

	def attack(self,player): #checks if enemy should attack
		if self.shoot_cooldown2 == 0 and self.isattacking2 == False and self.isattacking1 == False and self.isdead == False:
			self.i2 = 0
			self.isattacking2 = True
			if self.flipped == False:
				self.image = self.attack2[floor(self.i2)]
			else:
				self.image = self.flippedattack2[floor(self.i2)]
		elif self.shoot_cooldown1 == 0 and self.isattacking1 == False and self.isattacking2 == False and self.isdead == False:
			self.i1 = 0
			self.isattacking1 = True
			if self.flipped == False:
				self.image = self.attack1[floor(self.i1)]
			else:
				self.image = self.flippedattack1[floor(self.i1)]
		if self.isattacking1 == True:
			if self.flipped == False:
				self.image = self.attack1[floor(self.i1)]
			else:
				self.image = self.flippedattack1[floor(self.i1)]
		if self.i1 >=4-self.k and self.isattacking1 == True:
				self.isattacking1 = False
				self.aim = (player.rect.center)
				self.shoot1()
		if self.isattacking2 == True:
			if self.flipped == False:
				self.image = self.attack2[floor(self.i1)]
			else:
				self.image = self.flippedattack2[floor(self.i1)]
		if self.i2 >=8-self.k and self.isattacking2 == True:
				self.isattacking2 = False
				self.aim = (player.rect.center)
				self.shoot2()
	def shoot1(self):
		projectiles = self.weapon1["projectiles"]
		self.lastx = (self.aim[0] - self.rect.centerx)
		self.lasty = (self.aim[1] - self.rect.centery)
		self.angle = atan2(self.lasty, self.lastx)
		if self.shoot_cooldown1 == 0 and self.hp > 0:
			self.shoot_cooldown1 = self.weapon1["cooldown"]
			spawn_bullet_pos = self.rect.center
			for x in range(projectiles):
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle,self.weapon1)
				camera_group.add(self.bullet)
				all_sprite_group.add(self.bullet)
	def shoot2(self):
		projectiles = self.weapon2["projectiles"]
		base_angle = 0.08*(projectiles-1)-0.04
		self.lastx = (self.aim[0] - self.rect.centerx)
		self.lasty = (self.aim[1] - self.rect.centery)
		self.angle = atan2(self.lasty, self.lastx)
		if self.shoot_cooldown2 == 0 and self.hp >0:
			self.shoot_cooldown2 = self.weapon2["cooldown"]
			spawn_bullet_pos = self.rect.center
			for x in range(projectiles):
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + base_angle-x*0.16,self.weapon2)
				camera_group.add(self.bullet)
				all_sprite_group.add(self.bullet)

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
			self.collisionrect.midbottom = self.rect.midbottom
			self.rect.left = max(camera_group.bg_rect.x, self.rect.left)
			self.rect.right = min(camera_group.bg_rect.right, self.rect.right)
			self.rect.top = max(camera_group.bg_rect.y, self.rect.top)
			self.rect.bottom = min(camera_group.bg_rect.bottom, self.rect.bottom)
			#for x in enemy_group:
				#if self.rect.y == x.rect.y and self !=x:
					#self.rect.y += 0.01		


		if self.collision_check == True and player.lastcollision >= player.iframes and self.i >=4-self.k:
			player.hp -= self.damage
			player.lastcollision = 0
	def update_direction(self):
		self.vector = pygame.Vector2(self.rect.center)
		if 0 != pygame.Vector2.length(player.vector - self.vector):
			self.direction = (player.vector - self.vector).normalize()
			if self.direction.x > 0 and self.hp >=0:
				self.flipped = True
				self.image = self.flippedwalking[floor(self.i1)]
			if self.direction.x <0 and self.hp>=0:
				self.flipped = False
				self.image = self.walking[floor(self.i1)]			
	def update(self,enemy_group,player):
		self.update_direction()
		self.check_collision(player)
		self.take_damage()
		self.attack(player)
		self.check_alive()
		self.ratio = self.hp/self.maxhp
		if self.shoot_cooldown1>0:
			self.shoot_cooldown1-=1
		if self.shoot_cooldown2>0:
			self.shoot_cooldown2-=1
		self.i+=self.k
		self.i1 +=self.k
		self.i2 +=self.k
		if(self.i>=12):
			self.i=0
		if (self.i1 >=4):
			self.i1=0
		if (self.i2 >=8):
			self.i2=0
		if self.hp >0:
			self.speed = monster_data[self.name]["speed"]
		else:
			self.speed = 0

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.sprite_sheet_image = pygame.image.load('Player/Trent Sprite Sheet.png').convert_alpha()
		self.sprite_sheet = Spritesheet.SpriteSheet(self.sprite_sheet_image)
		self.image = self.sprite_sheet.get_image(0, 66, 78, 78).convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.collisionrect = pygame.Rect(self.rect)
		self.collisionrect.width = int(0.5*self.collisionrect.width)
		self.collisionrect.height = int(0.7*self.collisionrect.height)
		self.collisionrect.midbottom = self.rect.midbottom
		self.direction = pygame.math.Vector2()
		self.lastx = 1.0
		self.lasty = 0
		self.walklastx = 1.0
		self.speed = 4
		self.maxhp = 500
		self.hp = self.maxhp
		self.ratio = self.hp/self.maxhp
		self.mass = 10
		self.shoot = 0
		self.coin_amount = 10
		self.shoot_cooldown = 0
		self.vector = pygame.Vector2(self.rect.center)
		self.lastcollision = 200
		self.iframes = 200 #iframes are measured in miliseconds
		self.weapon = weapon_data["Basic"]
		self.collision_check = False #all of these are used to detect which animation to use
		self.flipped = False
		self.is_hit = False
		self.isdead = False
		self.isattacking = False
		self.dash = False
		self.dash_cooldown = 0
		self.dashing = False
		self.dash_duration = 0
		self.i=0
		self.j=0
		self.k = 0.1 # 4/self.k = #ticks for animation to loop
		self.idle=[]
		self.flippedidle=[]
		self.walklastx = 0
		for x in range(4):
			self.idle.append (self.sprite_sheet.get_image(self.i, 66, 78, 78).convert_alpha())
			self.flippedidle.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 66, 78, 78).convert_alpha(), True, False))
			self.i+=1
		
		self.walking=[]
		self.flippedwalking=[]
		for x in range(4):
			self.walking.append (self.sprite_sheet.get_image(self.i, 66, 78, 78).convert_alpha())
			self.flippedwalking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 66, 78, 78).convert_alpha(), True, False))
			self.i+=1

		self.attacking=[]
		self.flippedattacking=[]
		for x in range(4):
			self.attacking.append (self.sprite_sheet.get_image(self.i, 66, 78, 78).convert_alpha())
			self.flippedattacking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 66, 78, 78).convert_alpha(), True, False))
			self.i+=1


		self.death=[]
		self.flippeddeath=[]
		for x in range(4):
			self.death.append (self.sprite_sheet.get_image(self.i, 78, 78, 78).convert_alpha())
			self.flippeddeath.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 78, 78, 78).convert_alpha(), True, False))
			self.i+=1
		self.i = 0
	def check_alive(self): # checks if player dies
		if self.hp <=0  and self.isdead == False:
			self.i = 0
			self.k = self.k/2
			self.isdead = True
			if self.flipped == False:
				self.image = self.death[floor(self.i)]
			else:
				self.image = self.flippeddeath[floor(self.i)]
			collision_group.remove(self)
		if self.hp <=0  and self.isdead == True:
			if self.flipped == False:
				self.image = self.death[floor(self.i)]
			else:
				self.image = self.flippeddeath[floor(self.i)]
			if self.i >= 4-self.k:
				self.kill()
	def check_collision(self,enemy_group):
		self.rect.x += self.direction.x * self.speed
		for enemy in collision_group:
			if self.rect.colliderect(enemy.collisionrect):
				self.rect.x -= self.direction.x * self.speed
				self.speed -= 0.1
				enemy.collision_check = True
		self.rect.y += self.direction.y * self.speed
		for enemy in collision_group:
			if self.rect.colliderect(enemy.collisionrect):
				self.rect.y -= self.direction.y * self.speed
				self.speed -= 0.1
				enemy.collision_check = True
		if self.is_hit == True:
			mask = pygame.mask.from_surface(self.image)
			self.image = mask.to_surface()
			self.image.set_colorkey((0,0,0))
		if framenum-self.j > 24 and self.is_hit == True:
				self.is_hit = False	
		self.rect.left = max(camera_group.bg_rect.x, self.rect.left)
		self.rect.right = min(camera_group.bg_rect.right, self.rect.right)
		self.rect.top = max(camera_group.level["top wall"], self.rect.top)
		self.rect.bottom = min(camera_group.level["bottom wall"], self.rect.bottom)
		self.collisionrect.midbottom = self.rect.midbottom
		
	
	def input(self):
		if self.dashing == False:
			keys = pygame.key.get_pressed()

			if keys[pygame.K_w] and keys[pygame.K_s]:
				self.direction.y = 0
				if(self.lastx>0):
					self.image=self.flippedidle[floor(self.i)]
				elif(self.lastx<0):
					self.image=self.idle[floor(self.i)]
			elif  keys[pygame.K_w]:
				self.direction.y = -1

			elif keys[pygame.K_s]:
				self.direction.y = 1

			else:
				self.direction.y = 0
		
			if keys[pygame.K_d] and keys[pygame.K_a]:
				self.direction.x = 0
				if(self.lastx>0):
					self.image=self.flippedidle[floor(self.i)]
				elif(self.lastx<0):
					self.image=self.idle[floor(self.i)]
			elif keys[pygame.K_d]:
				self.direction.x = 1
			elif keys[pygame.K_a]:
				self.direction.x = -1
			else:
				self.direction.x = 0
			if self.direction.x !=0 or self.direction.y !=0:
				self.lasty = self.direction.y
				self.lastx = self.direction.x


			if self.direction.x !=0:
				self.walklastx = self.direction.x
			if(self.walklastx>0):
				self.image=self.flippedwalking[floor(self.i)]
			elif(self.walklastx<0):
				self.image=self.walking[floor(self.i)]
			if self.direction.y ==0 and self.direction.x == 0:
				if(self.walklastx>0):
					self.image=self.flippedidle[floor(self.i)]
				elif(self.walklastx<=0):
					self.image=self.idle[floor(self.i)]	
	

			if keys[pygame.K_1]:
				self.weapon = weapon_data["Basic"]
			elif keys[pygame.K_2] and weapon_data["Shotgun"]["purchased"]==True:
				self.weapon = weapon_data["Shotgun"]
			elif keys[pygame.K_3] and weapon_data["Minigun"]["purchased"]==True:
				self.weapon = weapon_data["Minigun"]
			elif keys[pygame.K_4] and weapon_data["Lag_Maker"]["purchased"]==True:
				self.weapon = weapon_data["Lag_Maker"]
			elif keys[pygame.K_5] and weapon_data["Basic"]["purchased"]==True:
				self.weapon = weapon_data["Basic"]
			elif keys[pygame.K_6] and weapon_data["Basic"]["purchased"]==True:
				self.weapon = weapon_data["Basic"]
			if pygame.mouse.get_pressed()[2] and self.dash_cooldown == 0:
				self.dash = True
			elif keys[pygame.K_x] and self.dash_cooldown == 0:
				self.dash = True
			elif pygame.mouse.get_pressed() == (1, 0, 0):
				self.shoot = 1
				#self.is_shooting()
			elif keys[pygame.K_SPACE]:
				self.shoot = 2
				#self.space_shooting()
			else:
				self.shoot=False        		
	def is_shooting(self):
		projectiles = self.weapon["projectiles"]
		base_angle=0
		fox = 0
		if self.weapon["spread"]==0:
			fox = 1
			if projectiles % 2 == 1:
				base_angle = 0.05*(projectiles-1)
			elif projectiles % 2 == 0:
				base_angle = 0.05*(projectiles-1)-0.025
		if (self.direction.x==0 and self.direction.y==0 and self.lastx<0):
			self.image=self.attacking[2] #floor(self.i)
		elif (self.direction.x==0 and self.direction.y==0 and self.lastx>0):
			self.image=self.flippedattacking[2] #floor(self.i)
		self.mouse_coords = pygame.mouse.get_pos() 
		self.lastx = (self.mouse_coords[0] - self.rect.centerx + camera_group.camera_rect.left-camera_group.camera_borders["left"])
		self.lasty = (self.mouse_coords[1] - self.rect.centery + camera_group.camera_rect.top-camera_group.camera_borders["top"])
		self.angle = atan2(self.lasty, self.lastx)
		if self.shoot_cooldown == 0:
			self.shoot_cooldown = self.weapon["cooldown"]
			if(self.lastx==1):
				self.image=self.flippedattacking[floor(self.i)]
			elif(self.lastx==-1):
				self.image=self.attacking[floor(self.i)]
			spawn_bullet_pos = self.rect.center
			for x in range(projectiles):
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + randint(-self.weapon["spread"],self.weapon["spread"])/100+base_angle-x*0.1*fox,self.weapon)
				camera_group.add(self.bullet)
				all_sprite_group.add(self.bullet)
			if(self.lastx==1):
				self.image=self.flippedattacking[floor(self.i)]
			elif(self.lastx==-1):
				self.image=self.attacking[floor(self.i)]

	def space_shooting(self):
		projectiles = self.weapon["projectiles"]
		self.angle = atan2(self.lasty, self.lastx)
		base_angle=0
		fox = 0
		if self.weapon["spread"]==0:
			fox = 1
			if projectiles % 2 == 1:
				base_angle = 0.05*(projectiles-1)
			elif projectiles % 2 == 0:
				base_angle = 0.05*(projectiles-1)-0.025
		if (self.direction.x==0 and self.direction.y==0 and self.lastx<0):
			self.image=self.attacking[2] #floor(self.i)
		elif (self.direction.x==0 and self.direction.y==0 and self.lastx>0):
			self.image=self.flippedattacking[2] #floor(self.i)
		self.angle = atan2(self.lasty, self.lastx)
		if self.shoot_cooldown == 0:
			self.shoot_cooldown = self.weapon["cooldown"]
			if(self.lastx==1):
				self.image=self.flippedattacking[floor(self.i)]
			elif(self.lastx==-1):
				self.image=self.attacking[floor(self.i)]
			spawn_bullet_pos = self.rect.center
			for x in range(projectiles):
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + randint(-self.weapon["spread"],self.weapon["spread"])/100+base_angle-x*0.1*fox,self.weapon)
				camera_group.add(self.bullet)
				all_sprite_group.add(self.bullet)
	def dash_func(self):
		self.dashing = True
		
		self.mouse_coords = pygame.mouse.get_pos() 
		self.lastx = (self.mouse_coords[0] - self.rect.centerx + camera_group.camera_rect.left-camera_group.camera_borders["left"])
		self.lasty = (self.mouse_coords[1] - self.rect.centery + camera_group.camera_rect.top-camera_group.camera_borders["top"])
		self.angle = atan2(self.lasty, self.lastx)
		self.velx = cos(self.angle)*20
		if self.velx < 0:
			self.walklastx = -1
		else:
			self.walklastx = 1
		if (self.direction.x==0 and self.direction.y==0 and self.velx<0):
			self.image=self.attacking[2] #floor(self.i)
			mask = pygame.mask.from_surface(self.image)
			self.image = mask.to_surface()
			self.image.set_colorkey((0,0,0))
		elif (self.direction.x==0 and self.direction.y==0 and self.velx>=0):
			self.image=self.flippedattacking[2] #floor(self.i)
			mask = pygame.mask.from_surface(self.image)
			self.image = mask.to_surface()
			self.image.set_colorkey((0,0,0))
		self.vely = sin(self.angle)*20
		self.dash_duration = 12
		self.dash_cooldown = 100
		if(self.lastx==1):
			self.image=self.flippedattacking[floor(self.i)]
		elif(self.lastx==-1):
			self.image=self.attacking[floor(self.i)]
	def dash_movement(self):
		self.rect.x +=self.velx
		self.rect.y +=self.vely
		self.rect.x = int(self.rect.x)
		self.rect.y = int(self.rect.y)
		if self.dash_duration <=0:
			self.dashing = False
			self.dash = False
		else:
			self.dash_duration -=1
	def update(self,enemy_group,player):
		self.input()
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1
		if self.dash_cooldown > 0:
			self.dash_cooldown -= 1
		if self.dash == True and self.dash_cooldown == 0:
			self.dash_func()
		elif self.shoot == 1:
			self.is_shooting()
		elif self.shoot == 2:
			self.space_shooting()
		if self.dashing == True:
			self.dash_movement()
		elif self.dashing == False:
			self.check_collision(enemy_group)
		self.check_alive()
		self.i+=self.k
		if(self.i>=4):
			self.i=0
		self.vector = pygame.Vector2(self.rect.center)
		self.speed = 4
		self.ratio = self.hp/self.maxhp

class Hp_Bar(pygame.sprite.Sprite):
	def __init__(self, player):
		super().__init__()
		self.player = player
		self.rect1 = pygame.Rect(self.player.rect.x+10, self.player.rect.top-20, self.player.rect.width-20, 10)
		self.rect2 = pygame.Rect(self.player.rect.x+10, self.player.rect.top-20, (self.player.rect.width-20)*self.player.ratio, 10)
		self.rect3 = pygame.Rect(self.player.rect.x+8, self.player.rect.top-22, self.player.rect.width-16, 14)
		self.rect = pygame.Rect.union(self.rect2, self.rect1)
	def update(self, enemy_group, player):
		self.rect1.topleft = (self.player.rect.x+10, self.player.rect.top - 20)-camera_group.offset
		self.rect2 = pygame.Rect(self.player.rect.x+10, self.player.rect.y+20, (self.player.rect.width-20)*self.player.ratio, 10)
		self.rect2.topleft = self.rect1.topleft
		self.rect3.topleft = (self.player.rect.x+8, self.player.rect.top-22)-camera_group.offset
		self.rect = self.rect1.union(self.rect2)
		if self.player.hp > 0:
			pygame.draw.rect(camera_group.surface, "black", self.rect3)
			pygame.draw.rect(camera_group.surface, "red", self.rect1)
			pygame.draw.rect(camera_group.surface, "green", self.rect2)
		else:
			self.kill()
class Shop_Item(pygame.sprite.Sprite):
	def __init__(self, name, position):
		super().__init__()
		self.position=pygame.math.Vector2(position)
		self.name = name
		self.item = weapon_data[self.name]
		self.image = self.item["image"].convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = position
	def purchase(self,player):
		if player.coin_amount >= floor((self.item["cost"]*difficulty_mult)/2)*2:
			player.coin_amount -=floor((self.item["cost"]*difficulty_mult)/2)*2
			wares_group.remove(self)
			camera_group.remove(self)
			if self.item["type"] == "weapon":
				self.item["purchased"]=True
				weapons_group.remove(self)
			elif self.item["type"]== "upgrade":
				for item in weapon_data:
					if weapon_data[item]["type"] == "weapon":
						if self.item["change"] == "cooldown":
							weapon_data[item][self.item["change"]] = max(int(weapon_data[item][self.item["change"]]*self.item["value"]), 5)
						else:
							weapon_data[item][self.item["change"]]+=self.item["value"]
		elif player.coin_amount <self.item["cost"]:
			print("Not enough coins")
class Item(pygame.sprite.Sprite):
	def __init__(self, name, position):
		super().__init__()
		self.position=pygame.math.Vector2(position)
		self.name = name
		self.prop = prop_data[self.name]
		self.image = self.prop["image"].convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = position
		camera_group.add(self)
		self.coin_amount = self.prop["coin_num"]
	def update(self, enemy_group, player):
		if self.prop["collectable"] == True:
			if dist(self.rect.center, player.rect.center)<100:
				self.vector = pygame.Vector2(self.rect.center)
				if 0 != pygame.Vector2.length(player.vector - self.vector):
					self.direction = (player.vector - self.vector).normalize()
					self.rect.center += self.direction *10	
			if dist(self.rect.center, player.rect.center)<30:
				player.coin_amount +=self.coin_amount	
				self.kill()

class Bullet(pygame.sprite.Sprite): 
	def __init__(self, x, y, angle,weapon): 
		super().__init__()
		self.weapon = weapon
		self.angle = angle
		self.image = pygame.image.load(self.weapon["sprite"])
		self.image = pygame.transform.rotozoom(self.image,sin(self.angle)*30, self.weapon["scaling"])
		self.rect = self.image.get_rect()
		self.collisionrect = pygame.Rect(self.rect)
		self.collisionrect.width = int(0.8*self.collisionrect.width)
		self.collisionrect.height = int(0.8*self.collisionrect.height)
		self.collisionrect.center = self.rect.center
		self.rect.center = (x, y)
		self.x = x
		self.y = y
		self.speed = self.weapon["speed"]
		self.damage = self.weapon["damage"]
		self.velx = cos(self.angle)*self.speed
		self.vely = sin(self.angle)*self.speed
		self.bullet_lifetime = self.weapon["duration"]
		self.spawn_time = 0
 
	def check_collision(self,player):
		if self.weapon["ranged"] == True:
			self.bullet_lifetime = min(self.weapon["duration"]*(sqrt(difficulty_mult)), 5000) 
			if self.collisionrect.colliderect(player.collisionrect):
					if player.dashing == False:
						player.hp -= self.damage
						if framenum - player.j > 24: #Iframes
							player.is_hit = True
							player.j = framenum
					self.kill() 
		else:
			for x in enemy_group.sprites():
				if self.rect.colliderect(x.collisionrect):
					if self.spawn_time < self.bullet_lifetime/5:
						x.hp -= self.damage*3
					else:
						x.hp -= self.damage
					x.ishit = True
					x.j = framenum
					if x.collision_check == False:
						x.i = 0
					self.kill()
			#for x in enemy_weapon_group.sprites():
				#if self.collisionrect.colliderect(x.collisionrect):
					#self.kill()
					#x.kill() 
	def update(self,enemy_group,player):
		self.rect.x +=self.velx
		if self.weapon["ranged"] == True:
			self.speed = self.weapon["speed"]*difficulty_mult
		self.rect.y +=self.vely
		self.rect.x = int(self.rect.x)
		self.rect.y = int(self.rect.y)
		self.collisionrect.center = self.rect.center
		self.check_collision(player)
		if self.spawn_time > self.bullet_lifetime:
			self.kill()
		else:
			self.spawn_time +=1
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)	
class CameraGroup(pygame.sprite.Group):
	global wave
	def __init__(self):
		super().__init__()
		self.surface=pygame.display.get_surface()	
		self.offset = pygame.math.Vector2()
		self.half_w = self.surface.get_size()[0] // 2
		self.half_h = self.surface.get_size()[1] // 2
		self.surface_rect = self.surface.get_rect(midtop = (self.half_w,0))
		self.level = level_data[1]
		self.background_image = self.level["room"].convert_alpha()
		self.bg_rect = self.background_image.get_rect(topleft = (0,0))
		self.camera_borders = {'left': 500, 'right': 500, 'top': 400, 'bottom': 400}
		l = self.camera_borders['left']
		t = self.camera_borders['top']
		w = self.surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
		h = self.surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
		self.camera_rect = pygame.Rect(l,t,w,h)
		self.ratio = (wave-1)/level_data[levelnum]["num_wave"]
	def draw_wavebar(self):
			self.rect1 = pygame.Rect(100, 20, 2*self.half_w - 200, 14)
			self.rect2 = pygame.Rect(100, 20, (2*self.half_w - 200)*self.ratio, 14)
			self.rect3 = pygame.Rect(98, 18, 2*self.half_w - 196, 18)
			pygame.draw.rect(camera_group.surface, "black", self.rect3)
			pygame.draw.rect(camera_group.surface, "white", self.rect1)
			pygame.draw.rect(camera_group.surface, "blue", self.rect2)
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
	def custom_draw(self, player_group):
		self.text_surface = my_font.render(str(player.coin_amount), True, (0,0,0))
		self.fpsdisplay = my_font.render(str(int(clock.get_fps())), True , (0,0,0))
		self.center_target_camera(player_group)
		ground_offset = self.bg_rect.topleft - self.offset 
		self.surface.blit(self.background_image,ground_offset)
		if bosspresent == True:
			self.remove(bosshp)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.bottom):
			offset_pos = sprite.rect.topleft - self.offset
			self.surface.blit(sprite.image,offset_pos)
		if bosspresent == True:
			self.add(bosshp)
		hp.update(enemy_group, player)
		self.ratio = (wave-1)/level_data[levelnum]["num_wave"]
		screen.blit(prop_data["Coin"]["image"], (0,0))
		screen.blit(self.text_surface, (30,2))
		if displayfps == True:
			screen.blit(self.fpsdisplay, (0,40))
		if wavebar == True:
			self.draw_wavebar()


screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
camera_group = CameraGroup()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_weapon_group = pygame.sprite.Group()
collision_group = pygame.sprite.Group()
physics_group = pygame.sprite.Group()
all_sprite_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
wares_group = pygame.sprite.Group()
weapons_group = pygame.sprite.Group()
player = Player((640,360))
hp = Hp_Bar(player)
player_group.add(hp)
camera_group.add(hp)
player_group.add(player)
physics_group.add(player)
camera_group.add(player)
all_sprite_group.add(player)
shopping = False
for item in weapon_data:
	if weapon_data[item]["availible"]==True:
		if weapon_data[item]["type"] == "weapon":
			weapons_group.add(Shop_Item(item,(80,815)))
		else:
			item_group.add(Shop_Item(item,(80,815)))
def checkdistance(): #makes sure that spawns are further than 500 from player
	random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
	random_y = randint(camera_group.bg_rect.y+100,camera_group.background_image.get_size()[1]-200)
	if dist(player.rect.center, (random_x, random_y)) < 340: #can be changed
			return checkdistance()
	else:
		return (random_x, random_y)
def spawn(name, x, numspawn):
	global numbell, numsax, numdrum
	if numspawn < x:
				a = checkdistance()
				extra=Enemy(name, a)
				camera_group.add(extra)
				enemy_group.add(extra)
				collision_group.add(extra)
				if name == "bell":
					numbell +=1
				if name == "sax":
					numsax +=1
				if name == "drum":
					numdrum +=1
	else:
		if name == "bell": #tells you how many bells/sax have been spawned in this wave
			numbell = -100000
		if name == "sax":
			numsax = -100000
		if name == "drum":
			numdrum = -100000
def main_menu():
	meep = True
	while meep:
		screen.blit(pygame.image.load("Rooms/TitleRoom.png"), (0, 0))

		MENU_MOUSE_POS = pygame.mouse.get_pos()

		Play_button = Button(image=pygame.image.load("Props/Play Rect.png"), pos=(400, 150), 
							text_input="PLAY", font=get_font(35), base_color="black", hovering_color="White")
		Options_button = Button(image=pygame.image.load("Props/Play Rect.png"), pos=(400, 250), 
							text_input="OPTIONS", font=get_font(35), base_color="black", hovering_color="White")
		Quit_button = Button(image=pygame.image.load("Props/Play Rect.png"), pos=(400, 350), 
							text_input="QUIT", font=get_font(35), base_color="black", hovering_color="White")

		for button in [Play_button, Options_button, Quit_button]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(screen)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if Play_button.checkForInput(MENU_MOUSE_POS):
					meep = False
					new_level(levelnum)
				if Options_button.checkForInput(MENU_MOUSE_POS):
					meep = False
					new_level(levelnum)
				if Quit_button.checkForInput(MENU_MOUSE_POS):
					pygame.quit()
					sys.exit()

		pygame.display.update()
def draw_pause(): #Continue, Options, Restart, Save and quit buttons needed
	global game_pause
	surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
	MOUSE_POS = pygame.mouse.get_pos()
	Continue_button = Button(image=None, pos=(640, 275), text_input="Continue", font=get_font(45), base_color="black", hovering_color="White")
	Quit_button = Button(image=None, pos=(640, 425), text_input="Admit Defeat", font=get_font(35), base_color="black", hovering_color="White")
	Save_button = Button(image=None, pos=(640, 475), text_input="Save and quit", font=get_font(35), base_color="black", hovering_color="White")
	if goose == 1:
		pygame.draw.rect(surface, (32, 32, 32, 150), [0, 0, 1280, 720])
		pygame.draw.rect(surface, (128, 128, 128, 250), [460, 100, 360, 450]) #Dark Pause Menu Bg  
	pygame.draw.rect(surface, (192, 192, 192, 200), [460, 115, 360, 50], 0, 10)  
	for button in [Quit_button, Save_button, Continue_button]:
			button.changeColor(MOUSE_POS)
			button.update(screen)
	screen.blit(surface, (0, 0))

	screen.blit(my_font.render('Paused', True, (0, 0, 0, 200)), (600, 125))
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if Continue_button.checkForInput(MOUSE_POS):
					game_pause = False
					
				if Save_button.checkForInput(MOUSE_POS):
					pygame.quit()
					sys.exit()
				if Quit_button.checkForInput(MOUSE_POS):
					pygame.quit()
					sys.exit()



def new_level(num):
	global wave, numbell, numsax, numdrum, wavebar
	wave = 1
	camera_group.empty()
	wares_group.empty()
	camera_group.add(player)
	camera_group.level = level_data[num]
	camera_group.background_image = camera_group.level["room"].convert_alpha()
	camera_group.bg_rect = camera_group.background_image.get_rect(midtop = (camera_group.half_w,0))
	w = camera_group.surface.get_size()[0]  - (camera_group.camera_borders['left'] + camera_group.camera_borders['right'])
	h = camera_group.surface.get_size()[1]  - (camera_group.camera_borders['top'] + camera_group.camera_borders['bottom'])
	l = camera_group.camera_borders['left']
	t = camera_group.camera_borders['top']
	camera_group.camera_rect = pygame.Rect(l,t,w,h)
	player.rect.center = (level_data[num]["spawnx"], level_data[num]["spawny"])
	for x in range( min(floor(level_data[num]["num_bell"]/level_data[num]["num_wave"]), 25)):
		spawn("bell", min(floor(level_data[num]["num_bell"]/level_data[num]["num_wave"]), 25), numbell)
	for x in range( min(floor(level_data[num]["num_sax"]/level_data[num]["num_wave"]), 25)):
		spawn("sax", min(floor(level_data[num]["num_sax"]/level_data[num]["num_wave"]), 25), numsax)
	
	for x in range( min(floor(level_data[num]["num_drum"]/level_data[num]["num_wave"]), 25)):
		spawn("drum", min(floor(level_data[num]["num_drum"]/level_data[num]["num_wave"]), 25), numdrum)
	wavebar = True
	numbell = 0
	numsax = 0
	numdrum = 0
	wave +=1
	for i in range(level_data[num]["num_pillar"]):
		pillar= Item("Pillar", (level_data[num]["pillar_posx1"]+level_data[num]["pillar_posxjump"]*i, level_data[num]["pillar_posy1"]+level_data[num]["pillar_posyjump"]*i))
		camera_group.add(pillar)
		#collision_group.add(pillar)

def shop(num):
	global shopping, wavebar
	shopping = True
	wavebar = False
	camera_group.empty()
	wares_group.empty()
	camera_group.add(player)
	camera_group.level = level_data[num]
	camera_group.background_image = camera_group.level["room"].convert_alpha()
	camera_group.bg_rect = camera_group.background_image.get_rect(midtop = (camera_group.half_w,0))
	w = camera_group.surface.get_size()[0]  - (camera_group.camera_borders['left'] + camera_group.camera_borders['right'])
	h = camera_group.surface.get_size()[1]  - (camera_group.camera_borders['top'] + camera_group.camera_borders['bottom'])
	l = camera_group.camera_borders['left']
	t = camera_group.camera_borders['top']
	camera_group.camera_rect = pygame.Rect(l,t,w,h)
	player.rect.center = (level_data[num]["spawnx"], level_data[num]["spawny"])
	if event.key == pygame.K_r:
			player.coin_amount -= 5
			shop(0)
	if len(weapons_group)>0:
		wares_group.add(weapons_group.sprites()[randint(0,len(weapons_group)-1)])
		wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
		wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
		wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
		for x in range(len(wares_group)):
			wares_group.sprites()[x].rect.center = (50+350*x,815)
	else:
		wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
		wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
		wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
		wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
		for x in range(len(wares_group)):
			wares_group.sprites()[x].rect.center = (50+350*x,815)
	camera_group.add(wares_group.sprites()[0:4])
levelnum = 1
global framenum, numbell, numsax, numdrum
framenum = 0
numbell = 0
numsax = 0
wavebar = False
numdrum = 0
main_menu()
meep = True
game_pause = False
sparetimer1 = pygame.USEREVENT + 1
j = 0
spawnbell = False
spawnsax = False
spawndrum = False
spawnenemies = False
displayfps = False
#pygame.time.set_timer(sparetimer1,1000)
while meep:
	if game_pause == False:
		difficulty_mult = float(1.2**(levelnum-1))*1.5**(max(0, levelnum-10))
		if len(enemy_group) == 0 and wave <= level_data[levelnum]["num_wave"]:
			j+=1
			if j >= 120:
					spawnbell = True 
					spawnsax = True
					spawnenemies = True
					spawndrum = True
		if framenum %12 == 0 and spawnbell == True: #makes it spawn every 12 frames
			spawn("bell", floor(level_data[levelnum]["num_bell"]/level_data[levelnum]["num_wave"]), numbell)
		if framenum %12 == 0 and spawnsax == True: #makes it spawn every 12 frames
			spawn("sax", floor(level_data[levelnum]["num_sax"]/level_data[levelnum]["num_wave"]), numsax)
		if framenum %12 == 0 and spawndrum == True: #makes it spawn every 12 frames
			spawn("drum", floor(level_data[levelnum]["num_drum"]/level_data[levelnum]["num_wave"]), numdrum)
		if numbell <= 0:
				numbell = 0
				spawnbell = False
		if numsax <=0:
				numsax = 0
				spawnsax = False
		if numdrum <=0:
				numdrum = 0
				spawndrum = False
		if numbell <= 0 and numsax <=0 and numdrum <= 0 and spawnsax == False and spawnbell == False and spawndrum == False and spawnenemies == True and framenum%12 == 0:		
				spawnenemies = False
				wave +=1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			meep = False
		if event.type == sparetimer1:
			print("meep")
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				meep = False

			if event.key == pygame.K_e and shopping == True and game_pause == False:
				for item in wares_group:
					if player.rect.colliderect(item.rect):
						item.purchase(player)

			if  len(enemy_group)==0 and bosspresent==False and wave > level_data[levelnum]["num_wave"] and levelnum %3 ==0:
				bosspresent=True
				bigboss = Boss((640, 300))
				enemy_group.add(bigboss)
				collision_group.add(bigboss)
				camera_group.add(bigboss)	
				bosshp = Hp_Bar(bigboss)
				camera_group.add(bosshp)		
			if event.key == pygame.K_e and len(enemy_group)==0 and player.rect.centerx <= 1000 and player.rect.centerx >= 300 and player.rect.centery <= 700 and player.rect.centery >=450 and shopping == True and game_pause == False:
				shopping = False
				levelnum+=1
				new_level(levelnum)		
			elif event.key == pygame.K_e and len(enemy_group)==0 and player.rect.x <= 1750 and player.rect.x >= 1500 and player.rect.y <= 200 and shopping == False and  wave > level_data[levelnum]["num_wave"] and game_pause == False:
				shopping = True
				shop(0)
			if event.key == pygame.K_p and game_pause == False:
				game_pause = True
				goose = 1
			elif event.key == pygame.K_p and game_pause == True:
				game_pause = False
			if event.key == pygame.K_BACKQUOTE and displayfps == False:
				displayfps = True
			elif event.key == pygame.K_BACKQUOTE and displayfps == True:
				displayfps = False
	if game_pause == False:
		camera_group.custom_draw(player)
		framenum +=1			
		camera_group.update(enemy_group,player)
	if game_pause == True:
		draw_pause()
		player.shoot_cooldown += 1
		goose = 0
	pygame.display.update()
	clock.tick(120)