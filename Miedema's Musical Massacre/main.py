from typing import Any
import pygame
from random import random, randint
from math import *
from monster_data import *
from level_data import *
from prop_data import *
from weapon_data import *
from math import floor, ceil
import Spritesheet
import sys
import ast
import re
import os
pygame.init()
wave = 1
levelnum = 1
bosspresent=False
refreshes=0
pygame.mixer.music.load("Level.mp3")
pygame.mixer.music.load("Main.mp3")
def get_font(size):
	return pygame.font.SysFont('Verdana', size)
my_font = get_font(24)
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
		self.hp = enemy_info["health"]*difficulty_mult
		self.speed = enemy_info["speed"]
		self.defaultspeed = self.speed
		self.push_power = enemy_info["push_power"]
		self.currentimage = self.sprite_sheet.get_image(0, enemy_info["sprite_width"], enemy_info["sprite_height"],enemy_info["sprite_width"] )
		self.image = self.currentimage
		self.damage = int(enemy_info["attack_damage"]+2*levelnum-2)
		self.mass = enemy_info["mass"]
		self.collision_check = False #all of these are used to detect which animation to use
		self.flipped = False
		self.ishit = False
		self.isdead = False
		self.isattacking = False
		self.enemylist = []
		self.current_index = 0
		self.shoot_cooldown = 0 + randint(0,150)
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
		self.attackframes = enemy_info["attack_frames"]
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
		for x in range(self.attackframes):
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
					self.i2 = 0
					self.i = 0
					self.isattacking = True
					if self.flipped == False:
						self.image = self.attacking[floor(self.i2)]
					else:
						self.image = self.flippedattacking[floor(self.i2)]
				if self.isattacking == True:
					if self.flipped == False:
						self.image = self.attacking[floor(self.i2)]
					else:
						self.image = self.flippedattacking[floor(self.i2)]
				if self.i2 >=self.attackframes-self.k and self.isattacking == True:
						self.isattacking = False
						self.collision_check = False
						if self.rect.colliderect(player.rect) and player.lastcollision >= player.iframes and player.dashing == False:
							player.hp -= self.damage
							player.lastcollision = 0


			elif self.weapon["ranged"]==True:
				if self.shoot_cooldown == 0 and self.isattacking == False:
					self.i2 = 0
					self.i = 0
					self.isattacking = True
					if self.flipped == False:
						self.image = self.attacking[floor(self.i2)]
					else:
						self.image = self.flippedattacking[floor(self.i2)]
				if self.isattacking == True:
					if self.flipped == False:
						self.image = self.attacking[floor(self.i2)]
					else:
						self.image = self.flippedattacking[floor(self.i2)]
				if self.i2 >=self.attackframes-self.k and self.isattacking == True:
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
			self.shoot_cooldown = self.weapon["cooldown"] + randint(0,150)
			spawn_bullet_pos = self.rect.center
			for x in range(projectiles):
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + randint(-self.weapon["spread"],self.weapon["spread"])/100,self.weapon)
				enemy_weapon_group.add(self.bullet)
				camera_group.add(self.bullet)
				all_sprite_group.add(self.bullet)
				
	def check_collision(self,player): #Chris version of collision
		if self.hp >0:
			if self.name == "sax" and dist(self.rect.center, player.rect.center) < 500:
				self.direction.x = -self.direction.x
				self.direction.y = -self.direction.y
			elif self.name == "sax" and dist(self.rect.center, player.rect.center) < 1000: # SAX stuff

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
		#if self.collision_check == True and player.lastcollision >= player.iframes and self.i >=2:
			#player.hp -= self.damage
			#self.collision_check == False
			#player.lastcollision = 0
	def update(self,enemy_group,player):
		self.update_direction()
		self.check_collision(player)
		self.attack(player)
		self.take_damage()
		self.check_alive()
		self.i+=self.k
		self.i2+=self.k
		if self.shoot_cooldown >0:
			self.shoot_cooldown -= 1
		if self.i>=4:
			self.i=0
		if self.i2>=self.attackframes:
			self.i2=0
		if self.hp >0:
			self.speed = self.defaultspeed
		else:
			self.speed = 0
		self.enemylist = []

class Boss(pygame.sprite.Sprite):
	global levelnum
	def __init__(self, position):
		super().__init__()
		self.position = pygame.math.Vector2(position) 
		self.name = 'top_brass'
		enemy_info = monster_data[self.name]
		self.weapon1 = weapon_data['top_brass1']
		self.weapon2 = weapon_data['top_brass2']
		self.weapon3 = weapon_data['top_brass3']
		self.sprite_sheet_image = enemy_info["spritesheet"].convert_alpha()
		self.sprite_sheet = Spritesheet.SpriteSheet(self.sprite_sheet_image)
		self.maxhp = enemy_info["health"]*(difficulty_mult**2)
		self.hp = self.maxhp
		self.ratio = self.hp/self.maxhp
		self.healing = False
		self.healed = 0
		self.speed = min(enemy_info["speed"]*(difficulty_mult*0.6),1.2)
		self.defaultspeed = self.speed
		self.push_power = enemy_info["push_power"]
		self.currentimage = self.sprite_sheet.get_image(0, enemy_info["sprite_width"], enemy_info["sprite_height"], enemy_info["sprite_width"])
		self.image = self.currentimage
		self.damage = int(enemy_info["attack_damage"]*(1+levelnum))
		self.mass = enemy_info["mass"]
		self.collision_check = False #all of these are used to detect which animation to use
		self.flipped = False
		self.ishit = False
		self.isdead = False
		self.current_index = 0
		self.isattacking1 = False
		self.isattacking2 = False
		self.isattacking3 = False
		self.totalattacks = 0
		self.shoot_cooldown1 =self.weapon1["cooldown"]
		self.shoot_cooldown2 =self.weapon2["cooldown"]
		self.shoot_cooldown3 =self.weapon3["cooldown"]
		self.i1 = 0
		self.i2 = 0
		self.rect = self.image.get_rect()
		self.rect.center = position
		
		self.collisionrect = pygame.Rect(self.rect)
		self.collisionrect.width = int(0.6*self.collisionrect.width)
		self.collisionrect.height = int(0.8*self.collisionrect.height)
		self.collisionrect.midbottom = self.rect.midbottom

		self.speed_buildupy=0
		self.speed_buildupx=0
		self.frogx =0
		self.frogy =0
		self.direction = pygame.Vector2(1, 0)

		self.i=0
		self.z = 0
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
		global bosspresent
		if self.hp <=0  and self.isdead == False:
			self.i = 0
			self.k = self.k*1.5
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
			if self.i >= 12-self.k:
				self.kill()
				main_counter = 0
				bosspresent = False
				player.hp = player.maxhp		
	def take_damage(self): #checks if enemy is hit
			if self.ishit == True:
				if self.flipped == False:
					self.image = self.takedamage[floor(self.i1)]
				else:
					self.image = self.flippedtakedamage[floor(self.i1)]
				mask = pygame.mask.from_surface(self.image)
				self.image = mask.to_surface()
				self.image.set_colorkey((0,0,0))
			if self.i >=4-self.k and self.ishit == True:
				self.ishit = False			

	def attack(self,player): #checks if enemy should attack
		if self.shoot_cooldown3 == 0 and self.isattacking3 == False and self.isattacking2 == False and self.isattacking1 == False and self.isdead == False:
			self.i2 = 0
			self.isattacking3 = True
			if self.flipped == False:
				self.image = self.attack1[floor(self.i2)]
			else:
				self.image = self.flippedattack1[floor(self.i2)]
		if self.shoot_cooldown2 == 0 and self.isattacking2 == False and self.isattacking3 == False and self.isattacking1 == False and self.isdead == False:
			self.i2 = 0
			self.isattacking2 = True
			if self.flipped == False:
				self.image = self.attack2[floor(self.i2)]
			else:
				self.image = self.flippedattack2[floor(self.i2)]
		elif self.shoot_cooldown1 == 0 and self.isattacking1 == False and self.isattacking3 == False and self.isattacking2 == False and self.isdead == False:
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
		if self.isattacking3 == True:
			if self.flipped == False:
				self.image = self.attack1[floor(self.i1)]
			else:
				self.image = self.flippedattack1[floor(self.i1)]
		if self.isattacking3 == True:
				self.totalattacks +=1
				if self.totalattacks >= 200+self.healed*50:
					self.shoot_cooldown3 = self.weapon3["cooldown"]-self.healed*200
					self.totalattacks = 0
					self.isattacking3 = False
				self.aim = (player.rect.center)
				self.shoot3()
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
		base_angle = 0.07*(projectiles-1)-0.035
		self.lastx = (self.aim[0] - self.rect.centerx)
		self.lasty = (self.aim[1] - self.rect.centery)
		self.angle = atan2(self.lasty, self.lastx)
		if self.shoot_cooldown2 == 0 and self.hp >0:
			self.shoot_cooldown2 = self.weapon2["cooldown"]
			spawn_bullet_pos = self.rect.center
			for x in range(projectiles):
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + base_angle-x*0.14,self.weapon2)
				camera_group.add(self.bullet)
				all_sprite_group.add(self.bullet)
	def shoot3(self):
		projectiles = self.weapon3["projectiles"]
		self.lastx = (self.aim[0] - self.rect.centerx)
		self.lasty = (self.aim[1] - self.rect.centery)
		self.angle = atan2(self.lasty, self.lastx)
		if self.shoot_cooldown3 == 0 and self.hp > 0 and self.totalattacks%2==0:
			spawn_bullet_pos = self.rect.center
			for x in range(projectiles):
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle+randint(-self.weapon3["spread"],self.weapon3["spread"])/100,self.weapon3)
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
			


			if self.collisionrect.colliderect(player.rect) and player.dashing == False:
				self.rect.x = self.rect.x - self.direction.x * int(self.speed) + self.frogx
				self.rect.y = self.rect.y - self.direction.y * int(self.speed) + self.frogy
				self.collisionrect.midbottom = self.rect.midbottom
				self.speed -= 0.8
				self.check_collision(player)
				self.collision_check = True
			self.rect.left = max(camera_group.bg_rect.x, self.rect.left)
			self.rect.right = min(camera_group.bg_rect.right, self.rect.right)
			self.rect.top = max(camera_group.bg_rect.y, self.rect.top)
			self.rect.bottom = min(camera_group.bg_rect.bottom, self.rect.bottom)
		#if self.collision_check == True and player.lastcollision >= player.iframes and player.dashing == False:
			#player.hp -= self.damage
			#self.collision_check = False
			#player.lastcollision = 0
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
		global framenum,levelnum
		self.update_direction()
		self.check_collision(player)
		
		self.collision_check = False
		if self.healing == True:
			self.z += 1
			if self.flipped == False:
				self.image = self.death[floor(6)]
			else:
				self.image = self.flippeddeath[floor(6)]
			if (self.hp <= 0 or self.hp >=self.maxhp/(1.5+self.healed/2)) or self.z > 2400:
				self.healing = False
				self.healed += 1
				self.z = 1
			if framenum%10==0 and self.hp >0 :
				self.hp+=self.maxhp/(70+self.healed*5)
			if framenum%(40/ceil(self.z/1000))==0 and self.hp >0:
				spawn("bell2", 2, 1)
				if levelnum > 3:
					spawn("sax2", 2, 1)
				if levelnum > 9:
					spawn("drum2", 2, 1)
		else:
			self.attack(player)
		#self.take_damage()
		self.check_alive()
		if self.hp < self.maxhp/(3+self.healed) and self.hp >0 and self.healed < int(levelnum/3) and self.healing == False:
			self.healing = True
		self.ratio = self.hp/self.maxhp
		if self.shoot_cooldown1>0:
			self.shoot_cooldown1-=1
		if self.shoot_cooldown2>0:
			self.shoot_cooldown2-=1
		if self.shoot_cooldown3>0:
			self.shoot_cooldown3-=1
		if self.healing == False:
			self.i+=self.k
		self.i1 +=self.k
		self.i2 +=self.k
		if(self.i>=12):
			self.i=0
		if (self.i1 >=4):
			self.i1=0
		if (self.i2 >=8):
			self.i2=0
		if self.hp >0 and self.healing == False and self.isattacking2==False and self.isattacking3 == False:
			self.speed = self.defaultspeed
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
		self.notmouse = False
		self.maxhp = 500
		self.hp = self.maxhp
		self.ratio = self.hp/self.maxhp
		self.mass = 10
		self.shoot = 0
		self.coin_amount = 10
		self.coin_magnet = 100
		self.shoot_cooldown = 0
		self.vector = pygame.Vector2(self.rect.center)
		self.mouse_coords = pygame.mouse.get_pos() 
		self.lastcollision = 200
		self.iframes = 120
		self.weapon = weapon_data["Basic"]
		self.angle = 0  # Initial angle
		self.flipped = False  # Initial flipped state
		self.screen_coord = (self.rect.centerx - camera_group.camera_rect.left+camera_group.camera_borders["left"], self.rect.centery + camera_group.camera_rect.top-camera_group.camera_borders["top"])
		self.collision_check = False #all of these are used to detect which animation to use
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
				player_group.empty()
				gun.kill()
				self.isdead = False
	def check_collision(self,collision_group):
		if self.dashing == True:
					self.rect.x += self.velx
		else:
					self.rect.x += self.direction.x * self.speed
		for enemy in collision_group:
			if self.rect.colliderect(enemy.collisionrect):
				if self.dashing == True:
					self.rect.x -= self.velx
				else:
					self.rect.x -= self.direction.x * self.speed
				self.speed -= 0.1
				enemy.collision_check = True
		if self.dashing == True:
					self.rect.y += self.vely
		else:
					self.rect.y += self.direction.y * self.speed
		for enemy in collision_group:
			if self.rect.colliderect(enemy.collisionrect):
				if self.dashing == True:
					self.rect.y -= self.vely
				else:
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
			if self.walklastx>0 or self.flipped == True:
				self.image=self.flippedwalking[floor(self.i)]
				self.flipped = True
			if self.walklastx<0 or self.flipped == False:
				self.image=self.walking[floor(self.i)]
				self.flipped = False
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
				self.notmouse = False
			elif (keys[pygame.K_LSHIFT] or keys[pygame.K_f])and self.dash_cooldown == 0:
				self.notmouse = True
				self.dash = True
			elif pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_m]:
				self.shoot = 1
			elif keys[pygame.K_SPACE]:
				self.shoot = 2
			else:
				self.shoot=False        		
	def is_shooting(self):
		projectiles = self.weapon["projectiles"]
		base_angle=0
		fox = 0
		if self.weapon["spread"]==0:
			fox = 1
			if projectiles % 2 == 1:
				base_angle = 0.04*(projectiles-1)
			elif projectiles % 2 == 0:
				base_angle = 0.04*(projectiles-1)-0.02
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
			spawn_bullet_pos = gun.rect.center
			for x in range(projectiles):
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + randint(-self.weapon["spread"],self.weapon["spread"])/100+base_angle-x*0.08*fox,self.weapon)
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
				base_angle = 0.04*(projectiles-1)
			elif projectiles % 2 == 0:
				base_angle = 0.04*(projectiles-1)-0.02
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
				self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + randint(-self.weapon["spread"],self.weapon["spread"])/100+base_angle-x*0.08*fox,self.weapon)
				camera_group.add(self.bullet)
				all_sprite_group.add(self.bullet)
	def dash_func(self):
		self.dashing = True
		if self.notmouse == False:
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
		self.dash_cooldown = 80
		if(self.lastx==1):
			self.image=self.flippedattacking[floor(self.i)]
		elif(self.lastx==-1):
			self.image=self.attacking[floor(self.i)]
	def dash_movement(self):
		#self.rect.x +=self.velx
		#self.rect.y +=self.vely
		self.rect.x = int(self.rect.x)
		self.rect.y = int(self.rect.y)
		if self.dash_duration <=0:
			self.dashing = False
			self.dash = False
		else:
			self.dash_duration -=1
	def update(self,enemy_group,player):
		self.input()
		self.screen_coord = (self.rect.centerx - camera_group.camera_rect.left+camera_group.camera_borders["left"], self.rect.centery + camera_group.camera_rect.top-camera_group.camera_borders["top"])
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1
		if self.dash_cooldown > 0:
			self.dash_cooldown -= 1
		if self.dash == True and self.dash_cooldown == 0:
			self.dash_func()
		elif self.shoot == 1 and shopping == False:
			self.is_shooting()
		elif self.shoot == 2 and shopping == False:
			self.space_shooting()
		if self.dashing == True:
			self.dash_movement()
			self.check_collision(self.prop)
		elif self.dashing == False:
			self.check_collision(collision_group)
		self.check_alive()
		if self.lastcollision < self.iframes:
			self.lastcollision +=1
		self.i+=self.k
		if(self.i>=4):
			self.i=0
		self.vector = pygame.Vector2(self.rect.center)
		self.speed = 4
		self.ratio = self.hp/self.maxhp
		self.prop = [x for x in collision_group if x not in enemy_group]

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
class Gun_Sprite(pygame.sprite.Sprite):
	def __init__(self, player, weapon):
		super().__init__()
		self.player = player
		self.weapon = weapon
		self.image_original = self.weapon["playerimage"]
		self.angle = 0  # Initial angle
		self.flipped = False  # Initial flipped state
		self.image = self.image_original  # Initialize the gun image
		self.rect = self.image.get_rect()
		self.precompute_images() 
	def rot_center(self, image, angle, x, y):
	
		rotated_image = pygame.transform.rotate(image, angle)
		new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

		return rotated_image, new_rect
	def precompute_images(self):
		self.rotated_image, self.rect = self.rot_center(self.image_original, self.angle, self.rect.centerx, self.rect.centery)
		self.flipped_image = pygame.transform.flip(self.rotated_image, True, False)
	def update_image(self, new_angle, flipped):
			self.weapon = player.weapon
			self.image_original = self.weapon["playerimage"]
			self.image = self.image_original 
			self.rect = self.image.get_rect()
			self.angle = new_angle
			self.flipped = flipped

			if self.flipped:
				self.image = self.flipped_image
				self.angle = 180-new_angle
			else:
				self.image = self.rotated_image
			self.precompute_images()
			self.rect.center = player.rect.center
	
	def update(self, enemy_group, p):
		self.mouse_coords = pygame.mouse.get_pos() 
		self.lastx = (self.mouse_coords[0] - self.rect.centerx + camera_group.camera_rect.left-camera_group.camera_borders["left"])
		self.lasty = (self.mouse_coords[1] - self.rect.centery + camera_group.camera_rect.top-camera_group.camera_borders["top"])
		self.angle = (180/pi)*-atan2(self.lasty, self.lastx) #converts from deg to rad
		if self.mouse_coords[0] < player.screen_coord[0]:
			self.flipped = True
			
		else:
			self.flipped = False

		self.update_image(self.angle, self.flipped)
		self.rect.center = player.rect.center
		self.rect.centery += 10
class Shop_Item(pygame.sprite.Sprite):
	def __init__(self, name, position):
		super().__init__()
		self.position=pygame.math.Vector2(position)
		self.name = name
		self.item = weapon_data[self.name]
		self.image = self.item["image"].convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.cost_display = my_font.render(str(self.item["cost"]+refreshes*2), True, (0,0,0))
	def purchase(self,player):
		global refreshes, guns
		if player.coin_amount >= floor(self.item["cost"]*difficulty_mult)+refreshes*2:
			player.coin_amount -=floor(self.item["cost"]*difficulty_mult)+refreshes*2
			if self.item["type"] == "refresh":
				refreshes+=1
				camera_group.remove(wares_group)
				wares_group.empty()
				wares_group.add(shopkeep)
				if len(weapons_group)>0:
					wares_group.add(weapons_group.sprites()[randint(0,len(weapons_group)-1)])
					while len(wares_group.sprites())<=4:
						wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
					for x in range(len(wares_group)-1):
						wares_group.sprites()[x+1].rect.center =  (100+331*x+max(x-1, 0)*41-max(x-2, 0)*24+20*(x-max(x-1, 0)),560)
						wares_group.sprites()[x+1].cost_display = my_font.render(str(floor(wares_group.sprites()[x+1].item["cost"]*difficulty_mult)+refreshes*2), True, (0,0,0))
				else:
					while len(wares_group.sprites())<=4:
						wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
					for x in range(len(wares_group)-1):
						wares_group.sprites()[x+1].rect.center =  (100+331*x+max(x-1, 0)*41-max(x-2, 0)*24+20*(x-max(x-1, 0)),560)
						wares_group.sprites()[x+1].cost_display = my_font.render(str(floor(wares_group.sprites()[x+1].item["cost"]*difficulty_mult)+refreshes*2), True, (0,0,0))
				wares_group.sprites()[0].cost_display = my_font.render(str(floor(wares_group.sprites()[0].item["cost"]*difficulty_mult)+refreshes*2), True, (0,0,0))
				camera_group.add(wares_group.sprites()[0:5])
			elif self.item["type"] == "weapon":
				wares_group.remove(self)
				camera_group.remove(self)
				self.item["purchased"]=True
				guns += 1
				weapons_group.remove(self)
			elif self.item["type"] == "healing":
				wares_group.remove(self)
				camera_group.remove(self)
				player.hp += self.item["value"]
				if player.hp >= player.maxhp:
					player.hp = 500
			elif self.item["type"]== "upgrade":
				wares_group.remove(self)
				camera_group.remove(self)
				for item in weapon_data:
					if weapon_data[item]["type"] == "weapon":
						if self.item["change"] == "cooldown":
							if weapon_data[item]["cooldown"] == weapon_data[item]["mincooldown"]:
								weapon_data[item]["damage"] += 6
							else:
								weapon_data[item]["cooldown"] = max(int(weapon_data[item]["cooldown"]*self.item["value"]), weapon_data[item]["mincooldown"])
						elif self.item["change"] == "projectiles":
							if weapon_data[item]["projectiles"] == weapon_data[item]["maxprojectiles"]:
								weapon_data[item]["damage"] += 10
							else:
								weapon_data[item]["projectiles"] = min(int(weapon_data[item]["projectiles"]+self.item["value"]), weapon_data[item]["maxprojectiles"])
						elif self.item["change"] == "speed":
							if weapon_data[item]["speed"] == weapon_data[item]["maxspeed"]:
								weapon_data[item]["damage"] += 5
							else:
								weapon_data[item]["speed"] = min(int(weapon_data[item]["speed"]+self.item["value"]), weapon_data[item]["maxspeed"])
						elif self.item["change"] == "duration":
							if weapon_data[item]["duration"] == weapon_data[item]["maxduration"]:
								if weapon_data[item]["name"] == "Shotgun":
									weapon_data[item]["damage"] += 10
								weapon_data[item]["damage"] += 5
							else:
								weapon_data[item]["duration"] = min(int(weapon_data[item]["duration"]+self.item["value"]), weapon_data[item]["maxduration"])
						else:
							weapon_data[item][self.item["change"]]+=self.item["value"]

class Item(pygame.sprite.Sprite):
	def __init__(self, name, position):
		super().__init__()
		self.position=pygame.math.Vector2(position)
		self.name = name
		self.prop = prop_data[self.name]
		self.image = self.prop["image"].convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.midleft = position
		camera_group.add(self)
		self.coin_amount = self.prop["coin_num"]
	def update(self, enemy_group, player):
		if self.prop["collectable"] == True:
			if dist(self.rect.center, player.rect.center)<player.coin_magnet:
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
		self.bullet_lifetime = self.weapon["duration"]
		if self.weapon["ranged"] == True:
			self.speed = min(self.weapon["speed"]+(sqrt(difficulty_mult)-1), self.weapon["max_speed"])
			self.bullet_lifetime = min(self.weapon["duration"]*(sqrt(difficulty_mult)), self.weapon["max_duration"]) 
		elif self.weapon["name"] == "Shotgun":
			self.speed+=randint(-5,5)
		self.damage = self.weapon["damage"]
		self.velx = cos(self.angle)*self.speed
		self.vely = sin(self.angle)*self.speed
		self.spawn_time = 0
 
	def check_collision(self,player):
		if self.weapon["ranged"] == True:
			if self.collisionrect.colliderect(player.collisionrect):
					if player.dashing == False and player.lastcollision >= player.iframes:
						player.hp -= self.damage
						player.lastcollision = 0
						if framenum - player.j > 24: #Iframes
							player.is_hit = True
							player.j = framenum
					self.kill() 
		else:
			for x in enemy_group.sprites():
				if self.rect.colliderect(x.collisionrect):
					if self.spawn_time < self.bullet_lifetime/5 and self.weapon["name"] != "Minigun":
						x.hp -= self.damage*2
					else:
						x.hp -= self.damage
						x.ishit = True
						x.j = framenum
					if x.collision_check == False:
						x.i = 0
					self.kill()
	def update(self,enemy_group,player):
		self.x +=self.velx
		self.y +=self.vely
		self.rect.centerx = int(self.x)
		self.rect.centery = int(self.y)
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
		if self.rect.collidepoint(position):
			return True
		return False

	def changeColor(self, position):
		if self.rect.collidepoint(position):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
	
class CameraGroup(pygame.sprite.Group):
	global wave, levelnum, tutorial, guns
	def __init__(self):
		super().__init__()
		self.purchase_text = get_font(32).render("Press E to buy item", True, (0,0,0))
		self.refresh_text = get_font(32).render("Press E to refresh shop", True, (0,0,0))
		self.open_door = get_font(32).render("Press E to open door", True, (0,0,0))
		self.tutorial1 = my_font.render(("WASD to move"), True , (0,0,0))
		self.tutorial2 = my_font.render(("Space/Left Click to shoot"), True , (0,0,0))
		self.tutorial3 = my_font.render(("F/LShift/Right Click to dash"), True , (0,0,0))
		self.tutorial4 = my_font.render(("1/2/3 to swap weapons"), True , (0,0,0))
		self.surface=pygame.display.get_surface()	
		self.offset = pygame.math.Vector2()
		self.half_w = self.surface.get_size()[0] // 2
		self.half_h = self.surface.get_size()[1] // 2
		self.surface_rect = self.surface.get_rect(midtop = (self.half_w,0))
		self.level = level_data[1]
		self.background_image = self.level["room"].convert_alpha()
		self.bg_rect = self.background_image.get_rect(topleft = (0,0))
		self.camera_borders = {'left': 500, 'right': 500, 'top': 500, 'bottom': 280}
		l = self.camera_borders['left']
		t = self.camera_borders['top']
		w = self.surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
		h = self.surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
		self.camera_rect = pygame.Rect(l,t,w,h)
		self.last_left = self.camera_rect.left
		self.last_top = self.camera_rect.top
		self.ratio = (wave-2)/level_data[levelnum]["num_wave"]
	def draw_wavebar(self):
			self.ratio = (wave-2)/level_data[levelnum]["num_wave"]
			self.rect1 = pygame.Rect(90, 20, 2*self.half_w - 200, 14)
			self.rect2 = pygame.Rect(90, 20, (2*self.half_w - 200)*self.ratio, 14)
			self.rect3 = pygame.Rect(88, 18, 2*self.half_w - 196, 18)
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
		if self.camera_rect.left != self.last_left:
			self.offset.x  = self.camera_rect.left - self.camera_borders["left"]
			self.last_left = self.camera_rect.left
			new_screen_coord = (player.rect.centerx - self.offset.x, player.screen_coord[1])
			player.screen_coord = new_screen_coord

		if self.camera_rect.top != self.last_top:
			self.offset.y = self.camera_rect.top - self.camera_borders["top"]
			self.last_top = self.camera_rect.top		
			new_screen_coord = (player.screen_coord[0], player.rect.centery - self.offset.y)
			player.screen_coord = new_screen_coord

	def custom_draw(self, player_group):
		self.text_surface = my_font.render(str(player.coin_amount), True, (0,0,0))
		self.levelnum_surface = my_font.render(("Level "+ str(levelnum)), True, (0,0,0))
		self.fpsdisplay = my_font.render(str(int(clock.get_fps())*2), True , (0,0,0))
		self.center_target_camera(player_group)
		ground_offset = self.bg_rect.topleft - self.offset 
		self.surface.blit(self.background_image,ground_offset)
		if bosspresent == True:
			self.remove(bosshp)
			#if levelnum == 15:
				#self.remove(bosshp2)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.bottom):
			offset_pos = sprite.rect.topleft - self.offset
			self.surface.blit(sprite.image,offset_pos)
			if wares_group.has(sprite):
				self.surface.blit(prop_data["Coin"]["image"], offset_pos+(0,sprite.rect.height))
				self.surface.blit(sprite.cost_display,offset_pos+(30,sprite.rect.height))
		if bosspresent == True:
			self.add(bosshp)
			#if levelnum == 15:
				#self.add(bosshp2)
		hp.update(enemy_group, player)
		#gun.update()
		self.ratio = (wave-2)/level_data[levelnum]["num_wave"]
		screen.blit(prop_data["Coin"]["image"], (0,10))
		screen.blit(self.text_surface, (30,10))
		screen.blit(self.levelnum_surface, (1180,10))
		if displayfps == True:
			screen.blit(self.fpsdisplay, (0,40))
		if wavebar == True:
			self.draw_wavebar()
		if interact == True:
			screen.blit(self.open_door, (400, 600))
		elif refreshinteract == True:
			screen.blit(self.refresh_text, (400, 600))
		elif shopinteract == True:
			screen.blit(self.purchase_text, (400, 600))
		elif tutorial == 1:
			screen.blit(self.tutorial1, (480,600))
		elif tutorial == 2:
			screen.blit(self.tutorial2, (480,600))
		elif tutorial == 3:
			screen.blit(self.tutorial3, (480,600))
		elif guns == 1:
			screen.blit(self.tutorial4, (480,600))
class HourRect(pygame.sprite.Sprite):
	def __init__(self, rect):
		super().__init__()
		self.collisionrect = rect

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
gun = Gun_Sprite(player, player.weapon)
player_group.add(hp)
camera_group.add(hp)
player_group.add(gun)
camera_group.add(gun)
all_sprite_group.add(gun)
player_group.add(player)
physics_group.add(player)
camera_group.add(player)
all_sprite_group.add(player)
shopping = False
shopkeep = Shop_Item("refresh",(846,240))

def save():
	global levelnum, shopping
	savecoinamount = player.coin_amount
	savehp = int(player.hp)
	with open("save_data.txt", "w") as s:
		try:
			s.write("%s\n"%(levelnum))
			s.write("%s\n"%(int(savehp)))
			s.write("%s\n"%(int(savecoinamount)))
			s.write("%s\n"%(shopping))
			s.write("%s\n"%(weapon_data["Basic"]))
			s.write("%s\n"%(weapon_data["Shotgun"]))
			s.write("%s\n"%(weapon_data["Minigun"]))
			s.write("%s\n"%(weapon_data["Lag_Maker"]))
			enemy_group.empty()
			collision_group.empty()
		except:
			open('save_data.txt', 'w').close()
def load_save():
	global levelnum, shopping, difficulty_mult,bosspresent
	if bosspresent == True:
		bosshp.kill()
	bosspresent = False
	with open("save_data.txt", "r") as s:
		levelnum = int(s.readline())
		difficulty_mult = float(1.2**(levelnum-1))*1.1**(max(0, levelnum-10))
		player.hp = int(s.readline())
		player.coin_amount = int(s.readline())
		shop1 = s.readline()
		for item in [weapon_data["Basic"],weapon_data["Shotgun"], weapon_data["Minigun"], weapon_data["Lag_Maker"] ]:
			i = str(s.readline())
			i_sanitized = re.sub(r'<Surface\([^)]+\)>', '"Surface"', i)
			j = ast.literal_eval(i_sanitized)
			item["damage"] += int(j["damage"])-item["damage"]
			item["cooldown"] = int(item["cooldown"]*(j["cooldown"]/item["cooldown"]))
			item["projectiles"] += int(j["projectiles"])-item["projectiles"]
			item["speed"] += int(j["speed"])-item["speed"]
			item["duration"] += int(j["duration"])-item["duration"]
			item["purchased"] = j["purchased"]
		weapons_group.empty()
		for item in weapon_data:
			if weapon_data[item]["availible"]==True and weapon_data[item]["purchased"] == False:
				if weapon_data[item]["type"] == "weapon":
					weapons_group.add(Shop_Item(item,(125,900)))
				else:
					item_group.add(Shop_Item(item,(125,900)))
	if shop1 == "True\n":
		shop(0)
		shopping = True
	else:
		new_level(levelnum)
def restart():
	global levelnum, game_pause, spawnbell, spawndrum, spawnsax, spawnenemies, displayfps, boss_spawned, bosspresent, options, test, j, goose, jellyfish, deathcounter, game_mute, interact, shopinteract, refreshinteract, difficulty_mult
	camera_group.empty()
	player_group.empty() 
	enemy_group.empty() 
	enemy_weapon_group.empty() 
	collision_group.empty()
	physics_group.empty() 
	all_sprite_group.empty()
	item_group.empty()
	wares_group.empty() 
	weapons_group.empty()
	levelnum = 1
	difficulty_mult = float(1.2**(levelnum-1))*1.1**(max(0, levelnum-10))
	player.maxhp = 500
	player.hp = player.maxhp
	player.coin_amount = 10
	player.weapon = weapon_data["Basic"]
	open('save_data.txt', 'w').close()
	with open("save_data.txt", "w") as s:
		s.write("%s\n"%(levelnum))
		s.write("%s\n"%(player.hp))
		s.write("%s\n"%(player.coin_amount))
		s.write("%s\n"%(False))
		s.write("%s\n"%({"type":"weapon","name":"Basic","purchased":True,"availible":False,"cost":20,"ranged":False,"damage":80,"cooldown":60,"mincooldown":20,"projectiles":1,"maxprojectiles":10,"speed":7,"maxspeed":15,"duration":80,"maxduration":160,"spread":0,"sprite":"Weapons/Pistol Bullet.png","scaling":1.2,"image": pygame.image.load("Props/Pistol Shop.png"),"playerimage": pygame.image.load("Player/Pistol Player Fixed.png")}))
		s.write("%s\n"%({"type":"weapon","name":"Shotgun","purchased":False,"availible":True,"cost":40,"ranged":False,"damage":50,"cooldown":120,"mincooldown":50,"projectiles":9,"maxprojectiles":25,"speed":20,"maxspeed":40,"duration":10,"maxduration":25,"spread":45,"sprite":"Weapons/Shotgun Bullet.png","scaling":1.2,"image": pygame.image.load("Props/Shotgun Shop.png"),"playerimage": pygame.image.load("Player/Shotgun Player Fixed.png")}))
		s.write("%s\n"%({"type":"weapon","name":"Minigun","purchased":False,"availible":True,"cost":75,"ranged":False,"damage":40,"cooldown":20,"mincooldown":10,"projectiles":2,"maxprojectiles":8,"speed":15,"maxspeed":25,"duration":25,"maxduration":75,"spread":30,"sprite":"Weapons/Bullet.png","scaling":2.4,"image": pygame.image.load("Props/Minigun Shop.png"),"playerimage": pygame.image.load("Player/Minigun Player Fixed.png")}))
		s.write("%s\n"%({"type":"weapon","name":"Lag_Maker","purchased":False,"availible":False,"cost":180,"ranged":False,"damage":200,"cooldown":10,"mincooldown":1,"projectiles":15,"maxprojectiles":1000,"speed":15,"maxspeed":1000,"duration":25,"maxduration":1000,"spread":300,"sprite":"Enemies/DevlinDeving.png","scaling":1,"image": pygame.image.load("Enemies/DevlinDeving.png"),"playerimage": pygame.image.load("Enemies/DevlinDeving.png")}))
	hp = Hp_Bar(player)
	player_group.add(hp)
	camera_group.add(hp)
	player_group.add(player)
	physics_group.add(player)
	camera_group.add(player)
	all_sprite_group.add(player)
	game_pause = False
	j = 0
	spawnbell = False
	spawnsax = False
	spawndrum = False
	spawnenemies = False
	displayfps = False
	if bosspresent == True:
		bosshp.kill()
	bosspresent=False
	boss_spawned = False
	options = False
	test = 0
	goose = 0
	jellyfish = 0
	for item in weapon_data:
		if weapon_data[item]["availible"]==True:
			if weapon_data[item]["type"] == "weapon":
				weapons_group.add(Shop_Item(item,(125,900)))
			else:
				item_group.add(Shop_Item(item,(125,900)))
	deathcounter = 0
	game_mute = False
	interact = False
	shopinteract = False
	refreshinteract = False
	pygame.mixer.music.set_volume(1)
	pygame.mixer.music.rewind()
for item in weapon_data:
	if weapon_data[item]["availible"]==True:
		if weapon_data[item]["type"] == "weapon":
			weapons_group.add(Shop_Item(item,(125,900)))
		else:
			item_group.add(Shop_Item(item,(125,900)))
def checkdistance(): #makes sure that spawns are further than 500 from player
	random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
	random_y = randint(camera_group.bg_rect.y+200,camera_group.background_image.get_size()[1]-50)
	if dist(player.rect.center, (random_x, random_y)) < 300: #can be changed
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
	global main_counter,bosspresent
	pygame.mixer.music.load("Main.mp3")
	pygame.mixer.music.play(-1)
	global game_pause
	if bosspresent == True:
		bosshp.kill()
	bosspresent=False
	meep = True
	game_pause = False
	while meep:
		screen.blit(pygame.image.load("Rooms/TitleRoom.png"), (0, 0))

		MENU_MOUSE_POS = pygame.mouse.get_pos()

		Play_button = Button(image=pygame.image.load("Props/Play Rect.png"), pos=(400, 200), 
							text_input="PLAY", font=get_font(28), base_color="black", hovering_color="White")
		Quit_button = Button(image=pygame.image.load("Props/Play Rect.png"), pos=(400, 300), 
							text_input="QUIT", font=get_font(28), base_color="black", hovering_color="White")

		for button in [Play_button, Quit_button]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(screen)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if Play_button.checkForInput(MENU_MOUSE_POS):
					meep = False
					main_menu2()
				if Quit_button.checkForInput(MENU_MOUSE_POS):
					pygame.quit()
					sys.exit()

		pygame.display.update()
def main_menu2():
	global levelnum, shopping
	meep2 = True
	with open("save_data.txt", "r") as s:
		levelnum = s.readline()
	while meep2:
		screen.blit(pygame.image.load("Rooms/TitleRoom.png"), (0, 0))

		MENU_MOUSE_POS = pygame.mouse.get_pos()

		New_button = Button(image=pygame.image.load("Props/Play Rect.png"), pos=(400, 200), 
							text_input="NEW GAME", font=get_font(28), base_color="black", hovering_color="White")
		if levelnum != 1 and levelnum != '1\n' and os.stat("save_data.txt").st_size != 0:
			Continue_button = Button(image=pygame.image.load("Props/Play Rect.png"), pos=(400, 300), 
							text_input="CONTINUE", font=get_font(28), base_color="black", hovering_color="White")
			for button in [New_button,Continue_button]:
				button.changeColor(MENU_MOUSE_POS)
				button.update(screen)
		
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if New_button.checkForInput(MENU_MOUSE_POS):
						meep2 = False
						pygame.mixer.music.load("Level.mp3")
						pygame.mixer.music.play(-1)
						restart()
						load_save()
					if Continue_button.checkForInput(MENU_MOUSE_POS):
						pygame.mixer.music.load("Level.mp3")
						pygame.mixer.music.play(-1)
						load_save()
						meep2 = False
		else:
			for button in [New_button]:
				button.changeColor(MENU_MOUSE_POS)
				button.update(screen)
		
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if New_button.checkForInput(MENU_MOUSE_POS):
						meep2 = False
						pygame.mixer.music.load("Level.mp3")
						pygame.mixer.music.play(-1)
						restart()
						load_save()
		pygame.display.update()
def draw_pause(): #Continue, Options, Restart, Save and quit buttons needed
	global game_pause, options, test, goose, game_mute
	if game_mute == False:
		pygame.mixer.music.set_volume(0.2)
	if options == False:
		surface = pygame.Surface((1280, 720), pygame.SRCALPHA)

		if goose == 1:
			pygame.draw.rect(surface, (32, 32, 32, 150), [0, 0, 1280, 720])		
		Continue_button = Button(image=None, pos=(640, 275), text_input="Continue", font=get_font(28), base_color="black", hovering_color="White")
		Option_button = Button(image=None, pos=(640, 325), text_input="Controls", font=get_font(28), base_color="black", hovering_color="White")
		Mute_button = Button(image=None, pos=(640, 375), text_input="Mute/Unmute", font=get_font(28), base_color="black", hovering_color="White")
		Quit_button = Button(image=None, pos=(640, 425), text_input="Give Up", font=get_font(28), base_color="black", hovering_color="White")
		Save_button = Button(image=None, pos=(640, 475), text_input="Save and Quit", font=get_font(28), base_color="black", hovering_color="White")
		pygame.draw.rect(surface, (128, 128, 128, 250), [460, 100, 360, 450]) #Dark Pause Menu Bg  
		pygame.draw.rect(surface, (192, 192, 192, 200), [460, 115, 360, 50], 0, 10)  
		screen.blit(surface, (0, 0))
		MOUSE_POS = pygame.mouse.get_pos()

		for button in [Quit_button, Save_button, Continue_button, Option_button, Mute_button]:
				button.changeColor(MOUSE_POS)
				button.update(screen)

		screen.blit(my_font.render('Paused', True, (0, 0, 0, 200)), (600, 125))
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if Continue_button.checkForInput(MOUSE_POS):
						game_pause = False
						pygame.mixer.music.set_volume(1)
						player.shoot_cooldown += 1
					elif Option_button.checkForInput(MOUSE_POS):
						option_menu()
						options = True
					elif Save_button.checkForInput(MOUSE_POS):
						main_menu()
					elif Quit_button.checkForInput(MOUSE_POS):
						game_pause = False
						player.hp = 0
					elif Mute_button.checkForInput(MOUSE_POS):
						if game_mute == True:
							game_mute = False
						else:
							game_mute = True
						
		pygame.display.update()
		
	else:
		option_menu()
def option_menu():
	global options, test
	if options : 
		test+=1
		surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
		if test == 1:
			pygame.draw.rect(surface, (32, 32, 32, 150), [0, 0, 1280, 720])
		pygame.draw.rect(surface, (128, 128, 128, 250), [460, 100, 360, 450])
		font = get_font(24)  
		instructions = [
			'WASD to move',
			'Space/Left Click to shoot',
			'E to interact',
			'F/LSHIFT/Right Click to dash',
			'1/2/3 to change weapons'
		]
		y_offset = 140  
		line_height = 60  

		for line in instructions:
			text_surface = font.render(line, True, (0, 0, 0, 255)) 
			text_rect = text_surface.get_rect(center=(640, y_offset))  
			surface.blit(text_surface, text_rect)
			y_offset += line_height 
		screen.blit(surface, (0, 0))
		Save_button = Button(image=None, pos=(640, 475), text_input="Back", font=get_font(28), base_color="black", hovering_color="White")
		Save_button.changeColor(pygame.mouse.get_pos())
		Save_button.update(screen)
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if Save_button.checkForInput(pygame.mouse.get_pos()):
						options = False
		pygame.display.update()
def death_screen():
	with open("save_data.txt", "w") as s:
		s.write("%s\n"%(1))
		s.write("%s\n"%(500))
		s.write("%s\n"%(10))
		s.write("%s\n"%(False))
		s.write("%s\n"%({"type":"weapon","name":"Basic","purchased":True,"availible":False,"cost":20,"ranged":False,"damage":80,"cooldown":60,"mincooldown":20,"projectiles":1,"maxprojectiles":10,"speed":7,"maxspeed":15,"duration":80,"maxduration":160,"spread":0,"sprite":"Weapons/Pistol Bullet.png","scaling":1.2,"image": pygame.image.load("Props/Pistol Shop.png"),"playerimage": pygame.image.load("Player/Pistol Player Fixed.png")}))
		s.write("%s\n"%({"type":"weapon","name":"Shotgun","purchased":False,"availible":True,"cost":40,"ranged":False,"damage":30,"cooldown":120,"mincooldown":50,"projectiles":9,"maxprojectiles":25,"speed":20,"maxspeed":40,"duration":10,"maxduration":20,"spread":25,"sprite":"Weapons/Shotgun Bullet.png","scaling":1.2,"image": pygame.image.load("Props/Shotgun Shop.png"),"playerimage": pygame.image.load("Player/Shotgun Player Fixed.png")}))
		s.write("%s\n"%({"type":"weapon","name":"Minigun","purchased":False,"availible":True,"cost":75,"ranged":False,"damage":40,"cooldown":20,"mincooldown":10,"projectiles":2,"maxprojectiles":8,"speed":15,"maxspeed":25,"duration":25,"maxduration":75,"spread":35,"sprite":"Weapons/Bullet.png","scaling":2,"image": pygame.image.load("Props/Minigun Shop.png"),"playerimage": pygame.image.load("Player/Minigun Player Fixed.png")}))
		s.write("%s\n"%({"type":"weapon","name":"Lag_Maker","purchased":False,"availible":False,"cost":180,"ranged":False,"damage":200,"cooldown":10,"mincooldown":1,"projectiles":15,"maxprojectiles":1000,"speed":15,"maxspeed":1000,"duration":25,"maxduration":1000,"spread":300,"sprite":"Enemies/DevlinDeving.png","scaling":1,"image": pygame.image.load("Enemies/DevlinDeving.png"),"playerimage": pygame.image.load("Enemies/DevlinDeving.png")}))
	pygame.mixer.music.set_volume(0)
	global deathcounter
	surface = pygame.Surface((1280, 720), pygame.SRCALPHA)

	if deathcounter == 1:
			pygame.draw.rect(surface, (255, 32, 32, 150), [0, 0, 1280, 720])
			deathcounter += 1		
	Quit_button = Button(image=None, pos=(640, 325), text_input="Restart", font=get_font(28), base_color="black", hovering_color="White")
	Save_button = Button(image=None, pos=(640, 375), text_input="Quit", font=get_font(28), base_color="black", hovering_color="White")
	pygame.draw.rect(surface, (255, 128, 128, 250), [460, 100, 360, 450]) #Dark Pause Menu Bg  
	pygame.draw.rect(surface, (255, 192, 192, 200), [460, 115, 360, 50], 0, 10)  
	screen.blit(surface, (0, 0))
	MOUSE_POS = pygame.mouse.get_pos()
	for button in [Quit_button, Save_button]:
				button.changeColor(MOUSE_POS)
				button.update(screen)
	screen.blit(my_font.render('You Died', True, (0, 0, 0, 200)), (580, 125))
	for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if Save_button.checkForInput(MOUSE_POS):
						restart()
						main_menu()
					elif Quit_button.checkForInput(MOUSE_POS):
						restart()
						load_save()
def new_level(num):
	global wave, numbell, numsax, numdrum, wavebar, savecoinamount, savehp,bosspresent
	save()
	wave = 1
	player.coin_magnet = 100
	bosspresent = False
	camera_group.empty()
	wares_group.empty()
	camera_group.add(player)
	camera_group.add(gun)
	camera_group.level = level_data[num]
	camera_group.background_image = camera_group.level["room"].convert_alpha()
	camera_group.bg_rect = camera_group.background_image.get_rect(midtop = (camera_group.half_w,0))
	w = camera_group.surface.get_size()[0]  - (camera_group.camera_borders['left'] + camera_group.camera_borders['right'])
	h = camera_group.surface.get_size()[1]  - (camera_group.camera_borders['top'] + camera_group.camera_borders['bottom'])
	l = camera_group.camera_borders['left']
	t = camera_group.camera_borders['top']
	camera_group.camera_rect = pygame.Rect(l,t,w,h)
	player.rect.center = (level_data[num]["spawnx"], level_data[num]["spawny"])
	for x in range(floor(level_data[num]["num_bell"]/level_data[num]["num_wave"])):
		spawn("bell", floor(level_data[num]["num_bell"]/level_data[num]["num_wave"]), numbell)
	for x in range( floor(level_data[num]["num_sax"]/level_data[num]["num_wave"])):
		spawn("sax", floor(level_data[num]["num_sax"]/level_data[num]["num_wave"]), numsax)
	
	for x in range( floor(level_data[num]["num_drum"]/level_data[num]["num_wave"])):
		spawn("drum", floor(level_data[num]["num_drum"]/level_data[num]["num_wave"]), numdrum)
	wavebar = True
	numbell = 0
	numsax = 0
	numdrum = 0
	wave +=1
	try:
		for i in range(level_data[num]["num_pillar"]):
			pillar= Item("Pillar", (level_data[num]["pillar_posx1"]+level_data[num]["pillar_posxjump"]*i, level_data[num]["pillar_posy1"]+level_data[num]["pillar_posyjump"]*i))
			camera_group.add(pillar)
	except:
			pass
	try:
		for rect in level_data[num]["collision rects"]:
			bg_rect = HourRect(rect)
			collision_group.add(bg_rect)
	except: 
		pass

def win_screen():
		global jellyfish
		surface = pygame.Surface((1280, 720), pygame.SRCALPHA)

		if jellyfish == 1:
			pygame.draw.rect(surface, (32, 32, 32, 150), [0, 0, 1280, 720])
			jellyfish += 1		
	
		Quit_button = Button(image=None, pos=(640, 425), text_input="Main Menu", font=get_font(28), base_color="black", hovering_color="White")
		Save_button = Button(image=None, pos=(640, 475), text_input="Quit", font=get_font(28), base_color="black", hovering_color="White")
		pygame.draw.rect(surface, (128, 128, 128, 250), [260, 100, 760, 450])
		pygame.draw.rect(surface, (192, 192, 192, 200), [460, 115, 360, 50], 0, 10)  
		font = get_font(24)  
		instructions = [
			'Game design by Chris, Sid and Ethan',
			'Main character inspired by Trent',
			'Music from Celeste Strawberry Jam and Noah Giesler',
		]
		y_offset = 240  
		line_height = 60  

		for line in instructions:
			text_surface = font.render(line, True, (0, 0, 0, 255)) 
			text_rect = text_surface.get_rect(center=(640, y_offset))  
			surface.blit(text_surface, text_rect)
			y_offset += line_height 
		
		screen.blit(surface, (0, 0))
		
		MOUSE_POS = pygame.mouse.get_pos()

		for button in [Quit_button, Save_button]:
				button.changeColor(MOUSE_POS)
				button.update(screen)

		screen.blit(my_font.render('YOU WIN!', True, (0, 0, 0, 200)), (580, 125))
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if Save_button.checkForInput(MOUSE_POS):
						quit()
					elif Quit_button.checkForInput(MOUSE_POS):
						restart()
						main_menu()
		pygame.display.update()
		
def shop(num):
	global shopping, wavebar, refreshes
	shopping = True
	refreshes = 0
	save()
			
	wavebar = False
	camera_group.empty()
	wares_group.empty()
	wares_group.add(shopkeep)
	camera_group.add(player)
	camera_group.add(shopkeep)
	camera_group.level = level_data[num]
	camera_group.background_image = camera_group.level["room"].convert_alpha()
	camera_group.bg_rect = camera_group.background_image.get_rect(midtop = (camera_group.half_w,0))
	w = camera_group.surface.get_size()[0]  - (camera_group.camera_borders['left'] + camera_group.camera_borders['right'])
	h = camera_group.surface.get_size()[1]  - (camera_group.camera_borders['top'] + camera_group.camera_borders['bottom'])
	l = camera_group.camera_borders['left']
	t = camera_group.camera_borders['top']
	camera_group.camera_rect = pygame.Rect(l,t,w,h)
	player.rect.center = (level_data[num]["spawnx"], level_data[num]["spawny"])
	if len(weapons_group)>0:
		wares_group.add(weapons_group.sprites()[randint(0,len(weapons_group)-1)])
		while len(wares_group.sprites())<=4:
			wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
		for x in range(len(wares_group)-1):
			wares_group.sprites()[x+1].rect.center = (100+331*x+max(x-1, 0)*41-max(x-2, 0)*24+20*(x-max(x-1, 0)),560)
			wares_group.sprites()[x+1].cost_display = my_font.render(str(floor(wares_group.sprites()[x+1].item["cost"]*difficulty_mult)), True, (0,0,0))
	else:
		while len(wares_group.sprites())<=4:
			wares_group.add(item_group.sprites()[randint(0,len(item_group)-1)])
		for x in range(len(wares_group)-1):
			wares_group.sprites()[x+1].rect.center =  (100+331*x+max(x-1, 0)*41-max(x-2, 0)*24+20*(x-max(x-1, 0)),560)
			wares_group.sprites()[x+1].cost_display = my_font.render(str(floor(wares_group.sprites()[x+1].item["cost"]*difficulty_mult)), True, (0,0,0))
	wares_group.sprites()[0].cost_display = my_font.render(str(floor(wares_group.sprites()[0].item["cost"]*difficulty_mult)), True, (0,0,0))
	camera_group.add(wares_group.sprites()[0:5])
	try:
		for rect in level_data[0]["collision rects"]:
			bg_rect = HourRect(rect)
			collision_group.add(bg_rect)
	except: 
		pass
	
levelnum = 1
global framenum, numbell, numsax, numdrum
framenum = 0
numbell = 0
numsax = 0
wavebar = False
numdrum = 0
savecoinamount = player.coin_amount
savehp = player.hp
main_counter = 0
bosspresent = False
main_menu()
meep = True
game_pause = False
sparetimer1 = pygame.USEREVENT + 1
#pygame.time.set_timer(sparetimer1, 1000)
j = 0
spawnbell = False
spawnsax = False
spawndrum = False
spawnenemies = False
displayfps = False
boss_spawned = False
options = False
test = 0
deathcounter = 0
game_mute = False
interact = False
shopinteract = False
refreshinteract = False
tutorial = 0
guns = 0

while meep:
	if framenum ==1 and levelnum == 1:
		tutorial = 1
	elif framenum == 600 and levelnum == 1:
		tutorial = 2
	elif framenum == 1200 and levelnum == 1:
		tutorial = 3
	elif framenum > 1800 and levelnum == 1:
		tutorial = 0
	if guns == 1:
		j+=1
		if j > 600:
			guns += 1
	if len(player_group) == 0:
		deathcounter +=1
		death_screen()
	elif game_pause == False:
		bruh = 0
		difficulty_mult = float(1.2**(levelnum-1))*1.1**(max(0, levelnum-10))
		if len(enemy_group) == 0 and wave <= level_data[levelnum]["num_wave"] and shopping == False:
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
				boss_spawned = False
		if wave - level_data[levelnum]["num_wave"] == 1 and len(enemy_group) == 0 and shopping == False:
			wave += 1
			player.coin_magnet = 10000
		if (len(enemy_group)==0 and player.rect.colliderect(level_data[levelnum]["exit rect"]) and shopping == False and  wave > level_data[levelnum]["num_wave"] and bosspresent == False) or (len(enemy_group)==0 and player.rect.colliderect(level_data[0]["exit rect"]) and shopping == True) : #Text on screen when able to open door and continue to next level
			interact = True
		else:
			interact = False
		if shopping == True and game_pause == False:
				bruh = 0
				for item in wares_group:
					if item.name == "refresh" and player.rect.colliderect(item.rect):
						refreshinteract = True
					elif item.name == "refresh" and player.rect.colliderect(item.rect) == False:
						refreshinteract = False
					if item.name != "refresh" and player.rect.colliderect(item.rect):
						bruh += 1
				if bruh == 1:
						shopinteract = True
				else:
					shopinteract = False
		if shopping == False:
			refreshinteract = False
			shopinteract = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			meep = False
		if event.type == pygame.KEYDOWN:


			if event.key == pygame.K_e and shopping == True and game_pause == False:
				for item in wares_group:
					if player.rect.colliderect(item.rect):
						item.purchase(player)

			if len(enemy_group)==0 and boss_spawned==False and bosspresent==False and wave > level_data[levelnum]["num_wave"] and levelnum %3 ==0:
				bosspresent=True
				boss_spawned = True
				if levelnum == 15:
					pygame.mixer.music.unload()
					pygame.mixer.music.load("Tuba.mp3")
					pygame.mixer.music.play(-1)
					bigboss = Boss((640, 185))
				else: 
					bigboss = Boss((640, 300))
				enemy_group.add(bigboss)
				collision_group.add(bigboss)
				camera_group.add(bigboss)	
				bosshp = Hp_Bar(bigboss)
				camera_group.add(bosshp)
	
			if event.key == pygame.K_e and len(enemy_group)==0 and player.rect.colliderect(level_data[0]["exit rect"]) and shopping == True and game_pause == False:
				shopping = False
				levelnum+=1
				new_level(levelnum)		
			elif event.key == pygame.K_e and len(enemy_group)==0 and player.rect.colliderect(level_data[levelnum]["exit rect"]) and shopping == False and  wave > level_data[levelnum]["num_wave"] and game_pause == False and bosspresent == False: #I'll generalize it later
				shopping = True
				shop(0)
			if (event.key == pygame.K_p or  event.key == pygame.K_ESCAPE) and game_pause == False:
				game_pause = True
				goose = 1
			elif (event.key == pygame.K_p or  event.key == pygame.K_ESCAPE) and game_pause == True:
				game_pause = False
				pygame.mixer.music.set_volume(1)
				options = False
				test = 0
				player.shoot_cooldown +=1
			if event.key == pygame.K_BACKQUOTE and displayfps == False:
				displayfps = True
			elif event.key == pygame.K_BACKQUOTE and displayfps == True:
				displayfps = False
	if game_mute == True and player.hp > 0:
		pygame.mixer.music.set_volume(0)
	elif game_mute == False and player.hp > 0:
		pygame.mixer.music.set_volume(1)
	if len(player_group) > 0:
		if game_pause == False:
			camera_group.custom_draw(player)
			framenum +=1			
			camera_group.update(enemy_group,player)
		if levelnum == 15 and boss_spawned == True and len(enemy_group) == 0:
			jellyfish = 1
			win_screen()
			game_pause = True	
		elif game_pause == True:
			draw_pause()
			goose = 0
	pygame.display.update()
	clock.tick(120)