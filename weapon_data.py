import pygame
weapon_data = {
  #--------ENEMY-WEAPONS------
  "bell":{"type":"enemy_weapon","availible":False,"ranged":False},
  "sax":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":5,"cooldown":100,"projectiles":1,"speed":3,"duration":170,"spread":10,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.6},
  "drum":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":8,"cooldown":400,"projectiles":10,"speed":2,"duration":70,"spread":300,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.8},
  "top_brass1":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":25,"cooldown":80,"projectiles":1,"speed":5,"duration":300,"spread":0,"sprite":"Weapons/Enemy_Bullet.png","scaling":1.6},
  "top_brass2":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":15,"cooldown":100,"projectiles":8,"speed":6,"duration":200,"spread":0,"sprite":"Weapons/Enemy_Bullet.png","scaling":1.1},
  #--------WEAPONS-------
  "Basic":{"type":"weapon","purchased":True,"availible":False,"cost":25,"ranged":False,"damage":50,"cooldown":50,"projectiles":1,"speed":9,"duration":55,"spread":0,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Props/Pistol Shop.png"),"playerimage": pygame.image.load("Player/Pistol Player.png")},
  "Shotgun":{"type":"weapon","purchased":False,"availible":True,"cost":25,"ranged":False,"damage":70,"cooldown":100,"projectiles":9,"speed":15,"duration":25,"spread":55,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Props/Shotgun Shop.png"),"playerimage": pygame.image.load("Player/Shotgun Player.png")},
  "Minigun":{"type":"weapon","purchased":False,"availible":True,"cost":10,"ranged":False,"damage":10,"cooldown":15,"projectiles":3,"speed":6,"duration":35,"spread":30,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Props/Minigun Shop.png"),"playerimage": pygame.image.load("Player/Minigun Player.png")},
  "Lag_Maker":{"type":"weapon","purchased":False,"availible":True,"cost":250,"ranged":False,"damage":300,"cooldown":10,"projectiles":20,"speed":15,"duration":25,"spread":300,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Enemies/DevlinDeving.png")},
  #--------MULTI-PURCHASE-ITEMS------
  "Upgrade1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Damage Upgrade.png"),"change":"damage","value":5},
  "Upgrade1.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Damage Upgrade.png"),"change":"damage","value":5},
  "Upgrade2":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Rate Upgrade.png"),"change":"cooldown","value":0.8},
  "Upgrade2.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Rate Upgrade.png"),"change":"cooldown","value":0.8},
  "Upgrade3":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Speed Upgrade.png"),"change":"speed","value":2},
  "Upgrade3.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Speed Upgrade.png"),"change":"speed","value":2},
  "Upgrade4":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Duration Upgrade.png"),"change":"duration","value":5},
  "Upgrade4.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Duration Upgrade.png"),"change":"duration","value":5},
  "Upgrade5":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Projectiles Upgrade.png"),"change":"projectiles","value":1},
  "Upgrade5.1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Projectiles Upgrade.png"),"change":"projectiles","value":1},
  "Upgrade6":{"type":"healing","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Coin3.png"),"value":150},
  "Upgrade6.1":{"type":"healing","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Coin3.png"),"value":150},
  
  
  "refresh":{"type":"refresh","purchased":False,"availible":False,"cost":1,"ranged":False,"image": pygame.image.load("Props/Shopkeep.png")},
}