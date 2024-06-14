import pygame
weapon_data = {
  #--------ENEMY-WEAPONS------
  "bell":{"type":"enemy_weapon","availible":False,"ranged":False},
  "bell2":{"type":"enemy_weapon","availible":False,"ranged":False},
  "sax":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":5,"cooldown":100,"projectiles":1,"speed":3,"max_speed":5, "duration":170,"max_duration":400,"spread":10,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.6},
  "sax2":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":5,"cooldown":50,"projectiles":1,"speed":3,"max_speed":5, "duration":170,"max_duration":400,"spread":10,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.6},
  "drum":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":15,"cooldown":400,"projectiles":8,"speed":2,"max_speed":3, "duration":40,"max_duration":100,"spread":280,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.8},
  "drum2":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":15,"cooldown":400,"projectiles":8,"speed":2,"max_speed":3, "duration":40,"max_duration":100,"spread":280,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.8},
  "top_brass1":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":20,"cooldown":35,"projectiles":1,"speed":4,"max_speed":9, "duration":300,"max_duration":600,"spread":0,"sprite":"Weapons/Enemy_Bullet.png","scaling":1.5},
  "top_brass2":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":13,"cooldown":450,"projectiles":8,"speed":5,"max_speed":10, "duration":200,"max_duration":400,"spread":0,"sprite":"Weapons/Enemy_Bullet.png","scaling":1.0},
  "top_brass3":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":5,"cooldown":1700,"projectiles":1,"speed":3,"max_speed":7, "duration":800,"max_duration":1600,"spread":35,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.5},

  #--------WEAPONS-------
  "Basic":{"type":"weapon","name":"Basic","purchased":True,"availible":False,"cost":20,"ranged":False,"damage":80,"cooldown":60,"mincooldown":20,"projectiles":1,"maxprojectiles":10,"speed":7,"maxspeed":15,"duration":80,"maxduration":160,"spread":0,"sprite":"Weapons/Pistol Bullet.png","scaling":1.2,"image": pygame.image.load("Props/Pistol Shop.png"),"playerimage": pygame.image.load("Player/Pistol Player Fixed.png")},
  "Shotgun":{"type":"weapon","name":"Shotgun","purchased":False,"availible":True,"cost":40,"ranged":False,"damage":50,"cooldown":120,"mincooldown":50,"projectiles":9,"maxprojectiles":25,"speed":20,"maxspeed":40,"duration":10,"maxduration":25,"spread":45,"sprite":"Weapons/Shotgun Bullet.png","scaling":1.2,"image": pygame.image.load("Props/Shotgun Shop.png"),"playerimage": pygame.image.load("Player/Shotgun Player Fixed.png")},
  "Minigun":{"type":"weapon","name":"Minigun","purchased":False,"availible":True,"cost":75,"ranged":False,"damage":40,"cooldown":20,"mincooldown":10,"projectiles":2,"maxprojectiles":8,"speed":15,"maxspeed":25,"duration":25,"maxduration":75,"spread":30,"sprite":"Weapons/Bullet.png","scaling":2.4,"image": pygame.image.load("Props/Minigun Shop.png"),"playerimage": pygame.image.load("Player/Minigun Player Fixed.png")},
  "Lag_Maker":{"type":"weapon","name":"Lag_Maker","purchased":False,"availible":False,"cost":180,"ranged":False,"damage":200,"cooldown":10,"mincooldown":1,"projectiles":15,"maxprojectiles":1000,"speed":15,"maxspeed":1000,"duration":25,"maxduration":1000,"spread":300,"sprite":"Enemies/DevlinDeving.png","scaling":1,"image": pygame.image.load("Enemies/DevlinDeving.png"),"playerimage": pygame.image.load("Enemies/DevlinDeving.png")},

  #--------MULTI-PURCHASE-ITEMS------
  "Upgrade1":{"type":"upgrade","purchased":False,"availible":True,"cost":7,"ranged":False,"image": pygame.image.load("Props/Damage Upgrade.png"),"change":"damage","value":5},
  "Upgrade1.1":{"type":"upgrade","purchased":False,"availible":True,"cost":7,"ranged":False,"image": pygame.image.load("Props/Damage Upgrade.png"),"change":"damage","value":5},
  "Upgrade1.2":{"type":"upgrade","purchased":False,"availible":True,"cost":7,"ranged":False,"image": pygame.image.load("Props/Damage Upgrade.png"),"change":"damage","value":5},
  "Upgrade2":{"type":"upgrade","purchased":False,"availible":True,"cost":15,"ranged":False,"image": pygame.image.load("Props/Rate Upgrade.png"),"change":"cooldown","value":0.85},
  "Upgrade2.1":{"type":"upgrade","purchased":False,"availible":True,"cost":15,"ranged":False,"image": pygame.image.load("Props/Rate Upgrade.png"),"change":"cooldown","value":0.85},
  "Upgrade3":{"type":"upgrade","purchased":False,"availible":True,"cost":12,"ranged":False,"image": pygame.image.load("Props/Speed Upgrade.png"),"change":"speed","value":1},
  "Upgrade3.1":{"type":"upgrade","purchased":False,"availible":True,"cost":12,"ranged":False,"image": pygame.image.load("Props/Speed Upgrade.png"),"change":"speed","value":1},
  "Upgrade4":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Duration Upgrade.png"),"change":"duration","value":2},
  "Upgrade4.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Duration Upgrade.png"),"change":"duration","value":2},
  "Upgrade5":{"type":"upgrade","purchased":False,"availible":True,"cost":18,"ranged":False,"image": pygame.image.load("Props/Projectiles Upgrade.png"),"change":"projectiles","value":1},
  "Upgrade5.1":{"type":"upgrade","purchased":False,"availible":True,"cost":18,"ranged":False,"image": pygame.image.load("Props/Projectiles Upgrade.png"),"change":"projectiles","value":1},
  "Upgrade6":{"type":"healing","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Healing Item.png"),"value":450},
  
  
  "refresh":{"type":"refresh","purchased":False,"availible":False,"cost":1,"ranged":False,"image": pygame.image.load("Props/Shopkeeper Sprite.png")},
}