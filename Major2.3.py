from typing import Any
import pygame
from random import random, randint
from math import *

import pygame.freetype
from monster_data import *
from level_data import *
from prop_data import *
from weapon_data import *
from math import floor
import Spritesheet
pygame.init()
my_font = pygame.font.SysFont('Times', 30)
class Enemy(pygame.sprite.Sprite): 
	def __init__(self, name, position):
		super().__init__()
		self.position = pygame.math.Vector2(position) 
		self.name = name
		self.weapon = weapon_data[self.name]
		enemy_info = monster_data[self.name]
		self.sprite_sheet_image = enemy_info["spritesheet"].convert_alpha()
		self.sprite_sheet = Spritesheet.SpriteSheet(self.sprite_sheet_image)
		self.hp = enemy_info["health"]
		self.speed = enemy_info["speed"]
		self.push_power = enemy_info["push_power"]
		self.currentimage = self.sprite_sheet.get_image(0, enemy_info["sprite_width"], enemy_info["sprite_height"])
		self.image = self.currentimage
		self.damage = enemy_info["attack_damage"]
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

		self.i=0
		self.k = 0.05 # 4/self.k = #ticks for animation to loop
		self.walking=[]
		self.flippedwalking=[]
		for x in range(4):
			self.walking.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"]).convert_alpha())
			self.flippedwalking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"]).convert_alpha(), True, False))
			self.i+=1

		self.attacking=[]
		self.flippedattacking=[]
		for x in range(4):
			self.attacking.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"]).convert_alpha())
			self.flippedattacking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"]).convert_alpha(), True, False))
			self.i+=1

		self.takedamage=[]
		self.flippedtakedamage=[]
		for x in range(4):
			self.takedamage.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"]).convert_alpha())
			self.flippedtakedamage.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"]).convert_alpha(), True, False))
			self.i+=1

		self.death=[]
		self.flippeddeath=[]
		for x in range(4):
			self.death.append (self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"]).convert_alpha())
			self.flippeddeath.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, enemy_info["sprite_width"], enemy_info["sprite_height"]).convert_alpha(), True, False))
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
					Item("Coin", self.rect.center)
				self.kill()
				self.k = 0.05
				
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
						
	def take_damage(self): #checks if enemy is hit
			if self.ishit == True:
				if self.flipped == False:
					self.image = self.takedamage[floor(self.i)]
				else:
					self.image = self.flippedtakedamage[floor(self.i)]
			if self.i >=4-self.k and self.ishit == True:
				self.ishit = False			
	def attack(self,player): #checks if enemy should attack
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
				weapon_group.add(self.bullet)
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
			for enemy in enemy_group:
				if dist(self.collisionrect.center, enemy.collisionrect.center)<10 and enemy != self:
					self.rect.x = self.rect.x - self.direction.x * int(self.speed) + self.frogx+(10-20*random())
					self.rect.y = self.rect.y - self.direction.y * int(self.speed) + self.frogy+(10-20*random())
					self.collisionrect.midbottom = self.rect.midbottom
					self.speed -= 0.1
					self.check_collision(player)
				if self.rect.bottom == enemy.rect.bottom and self.rect.bottom < player.rect.bottom and (self.rect.left <= enemy.rect.right or self.rect.right >= enemy.rect.left):
					self.rect.y -=0.01
				elif self.rect.bottom == enemy.rect.bottom and self.rect.bottom > player.rect.bottom and (self.rect.left <= enemy.rect.right or self.rect.right >= enemy.rect.left):
					self.rect.y +=0.01

			if self.collisionrect.colliderect(player.rect):
					self.rect.x = self.rect.x - self.direction.x * int(self.speed) + self.frogx
					self.rect.y = self.rect.y - self.direction.y * int(self.speed) + self.frogy
					self.collisionrect.midbottom = self.rect.midbottom
					self.speed -= 0.1
					self.collision_check = True
					self.check_collision(player)
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
		
	def update(self,enemy_group,player):
		self.update_direction()
		self.check_collision(player)
		self.take_damage()
		self.attack(player)
		self.check_alive()
		self.i+=self.k
		if player.lastcollision < player.iframes:
			player.lastcollision +=1
		if self.shoot_cooldown >0:
			self.shoot_cooldown -= 1
		if(self.i>=4):
			self.i=0
		if self.hp >0:
			self.speed = monster_data[self.name]["speed"]
		else:
			self.speed = 0
		self.enemylist = []

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.sprite_sheet_image = pygame.image.load('Player/Trent Sprite Sheet.png').convert_alpha()
		self.sprite_sheet = Spritesheet.SpriteSheet(self.sprite_sheet_image)
		self.image = self.sprite_sheet.get_image(0, 88, 104).convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.collisionrect = pygame.Rect(self.rect)
		self.collisionrect.width = int(0.5*self.collisionrect.width)
		self.collisionrect.height = int(0.7*self.collisionrect.height)
		self.collisionrect.midbottom = self.rect.midbottom
		self.direction = pygame.math.Vector2()
		self.lastx = 1.0
		self.lasty = 0
		self.walklastx = 1.0
		self.speed = 5
		self.maxhp = 500
		self.hp = self.maxhp
		self.ratio = self.hp/self.maxhp
		self.mass = 10
		self.shoot = 0
		self.coin_amount = 0
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
		self.i=0
		self.k = 0.1 # 4/self.k = #ticks for animation to loop
		self.idle=[]
		self.flippedidle=[]
		self.walklastx = 0
		for x in range(4):
			self.idle.append (self.sprite_sheet.get_image(self.i, 88, 104).convert_alpha())
			self.flippedidle.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 88, 104).convert_alpha(), True, False))
			self.i+=1
		
		self.walking=[]
		self.flippedwalking=[]
		for x in range(4):
			self.walking.append (self.sprite_sheet.get_image(self.i, 88, 104).convert_alpha())
			self.flippedwalking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 88, 104).convert_alpha(), True, False))
			self.i+=1

		self.attacking=[]
		self.flippedattacking=[]
		for x in range(4):
			self.attacking.append (self.sprite_sheet.get_image(self.i, 88, 104).convert_alpha())
			self.flippedattacking.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 88, 104).convert_alpha(), True, False))
			self.i+=1

		self.takedamage=[]
		self.flippedtakedamage=[]
		for x in range(4):
			self.takedamage.append (self.sprite_sheet.get_image(self.i, 88, 104).convert_alpha())
			self.flippedtakedamage.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 88, 104).convert_alpha(), True, False))
			self.i+=1


		self.death=[]
		self.flippeddeath=[]
		for x in range(4):
			self.death.append (self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha())
			self.flippeddeath.append (pygame.transform.flip(self.sprite_sheet.get_image(self.i, 80, 80).convert_alpha(), True, False))
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
	def check_collision(self,enemy_group):
		self.rect.x += self.direction.x * self.speed
		for enemy in collision_group:
			if self.rect.colliderect(enemy.collisionrect):
				self.rect.x -= self.direction.x * self.speed
				self.speed -= 0.1
				enemy.collision_check = True
				#self.check_collision(enemy_group)
		self.rect.y += self.direction.y * self.speed
		for enemy in collision_group:
			if self.rect.colliderect(enemy.collisionrect):
				self.rect.y -= self.direction.y * self.speed
				self.speed -= 0.1
				enemy.collision_check = True
				#self.check_collision(enemy_group)
		if self.is_hit == True:
			if self.flipped == False:
					self.image = self.takedamage[floor(self.i)]
			else:
					self.image = self.flippedtakedamage[floor(self.i)]
			if self.i >=4-self.k and self.is_hit == True:
				self.is_hit = False	
		self.rect.left = max(camera_group.bg_rect.x, self.rect.left)
		self.rect.right = min(camera_group.bg_rect.right, self.rect.right)
		self.rect.top = max(camera_group.bg_rect.y, self.rect.top)
		self.rect.bottom = min(camera_group.bg_rect.bottom, self.rect.bottom)
		self.collisionrect.midbottom = self.rect.midbottom
	
	def input(self):
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
			elif(self.walklastx<0):
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
		if pygame.mouse.get_pressed() == (1, 0, 0):
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
				weapon_group.add(self.bullet)
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
				weapon_group.add(self.bullet)
				camera_group.add(self.bullet)
				all_sprite_group.add(self.bullet)
	def update(self,enemy_group,player):
		self.input()
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1
		if self.shoot == 1:
			self.is_shooting()
		elif self.shoot == 2:
			self.space_shooting()
		self.check_collision(enemy_group)
		self.check_alive()
		self.i+=self.k
		if(self.i>=4):
			self.i=0
		self.vector = pygame.Vector2(self.rect.center)
		self.speed = 5
		self.ratio = self.hp/self.maxhp
class Hp_Bar(pygame.sprite.Sprite):
	def __init__(self, player):
		super().__init__()
		self.player = player
		self.rect1 = pygame.Rect(self.player.rect.x+20, self.player.rect.y-20, 50, 10)
		self.rect2 = pygame.Rect(self.player.rect.x+20, self.player.rect.y-20, 50*self.player.ratio, 10)
		self.rect3 = pygame.Rect(self.player.rect.x+18, self.player.rect.y-22, 54, 14)
		self.rect = pygame.Rect.union(self.rect2, self.rect1)
	def update(self, enemy_group, player):
		self.rect1.topleft = (self.player.rect.x+20, self.player.rect.top - 20)-camera_group.offset
		self.rect2 = pygame.Rect(self.player.rect.x+20, self.player.rect.y+20, 50*self.player.ratio, 10)
		self.rect2.topleft = self.rect1.topleft
		self.rect3.topleft = (self.player.rect.x+18, self.player.rect.y-22)-camera_group.offset
		#self.rect2.width = 150 * self.player.ratio
		self.rect = self.rect1.union(self.rect2)
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
		if player.coin_amount >= self.item["cost"]:
			player.coin_amount -=self.item["cost"]
			wares_group.remove(self)
			camera_group.remove(self)
			if self.item["type"] == "weapon":
				self.item["purchased"]=True
				weapons_group.remove(self)
			elif self.item["type"]== "upgrade":
				for item in weapon_data:
					if weapon_data[item]["type"] == "weapon":
						weapon_data[item][self.item["change"]]+=self.item["value"]
						if weapon_data[item][self.item["change"]] <=0:
							weapon_data[item][self.item["change"]]=1
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
	def update(self, enemy_group, player):
		if self.prop["collectable"] == True:
			if dist(self.rect.center, player.rect.center)<100:
				self.vector = pygame.Vector2(self.rect.center)
				if 0 != pygame.Vector2.length(player.vector - self.vector):
					self.direction = (player.vector - self.vector).normalize()
					self.rect.center += self.direction *10	
			if dist(self.rect.center, player.rect.center)<30:
				player.coin_amount +=1	
				self.kill()
	
class Bullet(pygame.sprite.Sprite): 
	def __init__(self, x, y, angle,weapon): 
		super().__init__()
		self.weapon = weapon
		self.image = pygame.image.load(self.weapon["sprite"])
		self.image = pygame.transform.rotozoom(self.image, 0, self.weapon["scaling"])
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.x = x
		self.y = y
		self.speed = self.weapon["speed"]
		self.angle = angle
		self.damage = self.weapon["damage"]
		self.velx = cos(self.angle)*self.speed
		self.vely = sin(self.angle)*self.speed
		self.bullet_lifetime = self.weapon["duration"]
		self.spawn_time = 0
 
	def check_collision(self,player):
		if self.weapon["ranged"] == True:
			if self.rect.colliderect(player.rect):
					player.hp -= self.damage
					player.is_hit = True
					self.kill() 
		else:
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
		self.check_collision(player)
		if self.spawn_time > self.bullet_lifetime:
			self.kill()
		else:
			self.spawn_time +=1
		
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
		self.bg_rect = self.background_image.get_rect(topleft = (0,0))
		self.camera_borders = {'left': 300, 'right': 300, 'top': 200, 'bottom': 200}
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
	def custom_draw(self, player_group):
		self.text_surface = my_font.render(str(player.coin_amount), True, (0,0,0))
		self.center_target_camera(player_group)
		ground_offset = self.bg_rect.topleft - self.offset 
		self.surface.blit(self.background_image,ground_offset)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.bottom):
			offset_pos = sprite.rect.topleft - self.offset
			self.surface.blit(sprite.image,offset_pos)
		hp.update(enemy_group, player)
		pygame.draw.rect(self.surface, "red", hp.rect1)
		pygame.draw.rect(self.surface, "green", hp.rect2)
		screen.blit(prop_data["Coin"]["image"], (0,0))
		screen.blit(self.text_surface, (30,0))
		if player.hp > 0:
			pygame.draw.rect(self.surface, "black", hp.rect3)
			pygame.draw.rect(self.surface, "red", hp.rect1)
			pygame.draw.rect(self.surface, "green", hp.rect2)
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
camera_group = CameraGroup()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
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
#collision_group.add(player)
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


def new_level(num):
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
	for i in range(level_data[num]["num_bell"]):
		random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
		random_y = randint(camera_group.bg_rect.y,camera_group.background_image.get_size()[1]-200)
		if dist(player.rect.center, (random_x, random_y)) < 500:
			random_x = (camera_group.background_image.get_size()[0]-100)/2
			random_y = (camera_group.background_image.get_size()[1]-100)/2
		extra=Enemy("bell", (random_x,random_y))
		camera_group.add(extra)
		enemy_group.add(extra)
		collision_group.add(extra)
		all_sprite_group.add(extra)
	for i in range(level_data[num]["num_sax"]):
		random_x = randint(camera_group.bg_rect.x+100,camera_group.background_image.get_size()[0]-100)
		random_y = randint(camera_group.bg_rect.y,camera_group.background_image.get_size()[1]-200)
		if dist(player.rect.center, (random_x, random_y)) < 500:
			random_x = (camera_group.background_image.get_size()[0]-100)/2
			random_y = (camera_group.background_image.get_size()[1]-100)/2
		extra=Enemy("sax", (random_x,random_y))
		camera_group.add(extra)
		enemy_group.add(extra)
		collision_group.add(extra)
		all_sprite_group.add(extra)
	for i in range(level_data[num]["num_pillar"]):
		pillar= Item("Pillar", (level_data[num]["pillar_posx1"]+level_data[num]["pillar_posxjump"]*i, level_data[num]["pillar_posy1"]+level_data[num]["pillar_posyjump"]*i))
		camera_group.add(pillar)
		#collision_group.add(pillar)

def shop(num):
	global shopping
	shopping = True
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
new_level(1)
meep = True
game_pause = False
sparetimer1 = pygame.USEREVENT + 1
#pygame.time.set_timer(sparetimer1,1000)
while meep:
	#if player_group.has(player) == False: #If player dies, game ends
			#meep = False
	#if len(enemy_group) == 0: #No enemies left, game ends
		#meep = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			meep = False
		if event.type == sparetimer1:
			print("meep")
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				meep = False
			if event.key == pygame.K_TAB:
				shop(3)
			if event.key == pygame.K_e and shopping == True:
				for item in wares_group:
					if player.rect.colliderect(item.rect):
						item.purchase(player)
			if event.key == pygame.K_e and len(enemy_group)==0 and player.rect.centerx <= 1000 and player.rect.centerx >= 300 and player.rect.centery <= 700 and player.rect.centery >=450 and shopping == True:
				shopping = False
				new_level(1)
			elif event.key == pygame.K_e and len(enemy_group)==0 and player.rect.x <= 1750 and player.rect.x >= 1500 and player.rect.y <= 200 and shopping == False:
				shop(3)
			if event.key == pygame.K_p and game_pause == False:
				game_pause = True
			elif event.key == pygame.K_p and game_pause == True:
				game_pause = False		
	if game_pause == False:			
		camera_group.update(enemy_group,player)
		camera_group.custom_draw(player)
 
	pygame.display.update()
	clock.tick(120)