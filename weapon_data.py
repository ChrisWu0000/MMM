import pygame
weapon_data = {
  #--------ENEMY-WEAPONS------
  "bell":{"type":"enemy_weapon","availible":False,"ranged":False},
  "sax":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":5,"cooldown":100,"projectiles":1,"speed":3,"max_speed":5, "duration":170,"max_duration":400,"spread":10,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.6},
  "drum":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":8,"cooldown":400,"projectiles":10,"speed":2,"max_speed":3, "duration":60,"max_duration":120,"spread":300,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.8},
  "top_brass1":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":25,"cooldown":40,"projectiles":1,"speed":4,"max_speed":9, "duration":300,"max_duration":600,"spread":0,"sprite":"Weapons/Enemy_Bullet.png","scaling":1.5},
  "top_brass2":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":15,"cooldown":450,"projectiles":8,"speed":5,"max_speed":10, "duration":200,"max_duration":400,"spread":0,"sprite":"Weapons/Enemy_Bullet.png","scaling":1.0},
  "top_brass3":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":5,"cooldown":1700,"projectiles":1,"speed":3,"max_speed":7, "duration":1000,"max_duration":2000,"spread":20,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.5},
  #--------WEAPONS-------
  "Basic":{"type":"weapon","purchased":True,"availible":False,"cost":20,"ranged":False,"damage":50,"cooldown":50,"mincooldown":5,"projectiles":1,"speed":7,"duration":80,"spread":0,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Props/Pistol Shop.png")},
  "Shotgun":{"type":"weapon","purchased":False,"availible":True,"cost":40,"ranged":False,"damage":80,"cooldown":100,"mincooldown":5,"projectiles":9,"speed":15,"duration":25,"spread":40,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Props/Shotgun Shop.png")},
  "Minigun":{"type":"weapon","purchased":False,"availible":True,"cost":60,"ranged":False,"damage":15,"cooldown":15,"mincooldown":5,"projectiles":2,"speed":10,"duration":20,"spread":25,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Props/Minigun Shop.png")},
  "Lag_Maker":{"type":"weapon","purchased":False,"availible":True,"cost":200,"ranged":False,"damage":400,"cooldown":5,"mincooldown":5,"projectiles":20,"speed":15,"duration":25,"spread":300,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Enemies/DevlinDeving.png")},
  #--------MULTI-PURCHASE-ITEMS------
  "Upgrade1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Damage Upgrade.png"),"change":"damage","value":5},
  "Upgrade1.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Damage Upgrade.png"),"change":"damage","value":5},
  "Upgrade1.2":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Damage Upgrade.png"),"change":"damage","value":5},
  "Upgrade2":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Rate Upgrade.png"),"change":"cooldown","value":0.85},
  "Upgrade2.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Rate Upgrade.png"),"change":"cooldown","value":0.85},
  "Upgrade3":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Speed Upgrade.png"),"change":"speed","value":1},
  "Upgrade3.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Speed Upgrade.png"),"change":"speed","value":1},
  "Upgrade4":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Duration Upgrade.png"),"change":"duration","value":4},
  "Upgrade4.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Duration Upgrade.png"),"change":"duration","value":4},
  "Upgrade5":{"type":"upgrade","purchased":False,"availible":True,"cost":20,"ranged":False,"image": pygame.image.load("Props/Projectiles Upgrade.png"),"change":"projectiles","value":1},
  "Upgrade5.1":{"type":"upgrade","purchased":False,"availible":True,"cost":20,"ranged":False,"image": pygame.image.load("Props/Projectiles Upgrade.png"),"change":"projectiles","value":1},
  "Upgrade6":{"type":"healing","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Healing Item.png"),"value":450},
  
  
  "refresh":{"type":"refresh","purchased":False,"availible":False,"cost":1,"ranged":False,"image": pygame.image.load("Props/Shopkeeper Sprite.png")},
}