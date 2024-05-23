import pygame
weapon_data = {
  "bell":{"type":"enemy_weapon","availible":False,"ranged":False},
  "sax":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":5,"cooldown":100,"projectiles":1,"speed":3,"duration":200,"spread":5,"sprite":"Weapons/Enemy_Bullet.png","scaling":0.6},
  "top_brass1":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":15,"cooldown":80,"projectiles":1,"speed":5,"duration":300,"spread":0,"sprite":"Weapons/Enemy_Bullet.png","scaling":1.6},
  "top_brass2":{"type":"enemy_weapon","availible":False,"ranged":True,"damage":5,"cooldown":100,"projectiles":8,"speed":6,"duration":200,"spread":0,"sprite":"Weapons/Enemy_Bullet.png","scaling":1.1},
  #--------
  "Basic":{"type":"weapon","purchased":True,"availible":False,"cost":25,"ranged":False,"damage":50,"cooldown":30,"projectiles":1,"speed":9,"duration":55,"spread":0,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Enemies/Bell.png")},
  "Shotgun":{"type":"weapon","purchased":False,"availible":True,"cost":25,"ranged":False,"damage":35,"cooldown":60,"projectiles":9,"speed":15,"duration":25,"spread":60,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Enemies/Sax.png")},
  "Minigun":{"type":"weapon","purchased":False,"availible":True,"cost":10,"ranged":False,"damage":10,"cooldown":15,"projectiles":3,"speed":6,"duration":35,"spread":30,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Player/Trent.png")},
  "Lag_Maker":{"type":"weapon","purchased":False,"availible":True,"cost":400,"ranged":False,"damage":200,"cooldown":10,"projectiles":20,"speed":15,"duration":25,"spread":300,"sprite":"Weapons/Bullet.png","scaling":3,"image": pygame.image.load("Enemies/DevlinDeving.png")},
  #--------
  "Upgrade1":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Coin.png"),"change":"damage","value":5},
  "Upgrade2":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Weapons/Bullet.png"),"change":"cooldown","value":0.85},
  "Upgrade3":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Player/DevlinDeving.png"),"change":"speed","value":2},
  "Upgrade4":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Weapons/Enemy_Bullet.png"),"change":"duration","value":5},
  "Upgrade5":{"type":"upgrade","purchased":False,"availible":True,"cost":10,"ranged":False,"image": pygame.image.load("Props/Column.png"),"change":"projectiles","value":1}
}