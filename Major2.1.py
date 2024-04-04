import pygame
from random import random
pygame.init()

class spritedata:
  def __init__(self,width,height,x,y,speedx,speedy):
    self.w=width
    self.h=height
    self.x=float(x)
    self.y=float(y)
    self.speedx=float(speedx)
    self.speedy=float(speedy)





def create_sprite(width, height, x, y,imagedata):
  sprite = pygame.sprite.Sprite()
  size = (width,height)
  position = (x,y)
  sprite.rect = pygame.Rect(position, size)
  sprite.surface = pygame.Surface(sprite.rect.size)
  sprite.surface.fill((200,200,200))
  sprite.image = pygame.image.load(imagedata)
  return sprite
def player_sprite():
  players = pygame.sprite.Sprite()
  size = (20,20)
  position = (140,90)
  players.rect = pygame.Rect(position, size)
  players.image = pygame.Surface(players.rect.size)
  players.image.fill((100,50,100))
  return players
flags = pygame.SCALED
window = pygame.display.set_mode((300, 200),flags, vsync=1)
camera = pygame.Rect(0, 0, 300, 200)
clock = pygame.time.Clock()
bossroom = pygame.image.load('Rooms/Boss Room.png').convert()
#---DO NOT GO OVER 500 SPRITES!!!!!!---
spritesdata = [spritedata(300,200,0,0,0,0)]
spriterects = [create_sprite(300,200,0,0,bossroom)]
for x in range(1):
  spriterects.append(create_sprite(20,20,5*x,5*x))
  spritesdata.append(spritedata(20,20,5*x,5*x,0,0))
  
playersprite = player_sprite()
playerdata = spritedata(20, 20, 140, 90,0,0)
speed=0.5
running = True
fox = pygame.key.get_pressed()
cooldown=0
timer = pygame.time.Clock() 
infoprint = pygame.USEREVENT + 1
pygame.time.set_timer(infoprint, 2000)
cooldownup = pygame.USEREVENT + 2

while running:
  for event in pygame.event.get():
    #if event.type == infoprint:
      #print(pygame.mouse.get_pos())
    if event.type == cooldownup:
      #spritesdata.speedx=0
      #spritesdata.speedy=0
      #spritesdata[1].x=0
      #spritesdata[1].y=0
      cooldown=0
    if event.type == pygame.QUIT:
      running = False
   
    #-----PLAYER INPUTS-----
    if event.type == pygame.KEYDOWN:
      playersprite.image.fill((0,50,0))
      if event.key == pygame.K_ESCAPE:
        running=False
      if event.key == pygame.K_DOWN and cooldown!=1:
        pygame.time.set_timer(cooldownup, 1, loops=1)
        spritesdata[1].speedy+=0.1
        cooldown=1
      if event.key == pygame.K_UP and cooldown!=1:
        pygame.time.set_timer(cooldownup, 1, loops=1)
        spritesdata[1].speedy-=0.1
        cooldown=1
      if event.key == pygame.K_RIGHT and cooldown!=1:
        pygame.time.set_timer(cooldownup, 1, loops=1)
        spritesdata[1].speedx+=0.1
        cooldown=1
      if event.key == pygame.K_LEFT and cooldown!=1:
        pygame.time.set_timer(cooldownup, 1, loops=1)
        spritesdata[1].speedx-=0.1
        cooldown=1
      if event.key == pygame.K_w:
        playerdata.speedy -= speed
        speedcheckw=speed
      if event.key == pygame.K_s:
        playerdata.speedy += speed
        speedchecks=speed
      if event.key == pygame.K_a:
        playerdata.speedx -= speed
        speedchecka=speed
      if event.key == pygame.K_d:
        playerdata.speedx += speed
        speedcheckd=speed
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_w:
        playerdata.speedy += speedcheckw
      if event.key == pygame.K_s:
        playerdata.speedy -= speedchecks
      if event.key == pygame.K_a:
        playerdata.speedx += speedchecka
      if event.key == pygame.K_d:
        playerdata.speedx -= speedcheckd
      if pygame.key.get_pressed() == fox:
        playersprite.image.fill((100,50,100))
  
  #-----COLLISION-----
  playerdata.x += playerdata.speedx
  
  if playerdata.x+20 > spritesdata[0].x + 300 or playerdata.x < spritesdata[0].x:
    if playerdata.x > spritesdata[0].x:
      playerdata.x = spritesdata[0].x+(playerdata.x-spritesdata[0].x)-speed
    elif playerdata.x < spritesdata[0].x:
      playerdata.x = spritesdata[0].x+(playerdata.x-spritesdata[0].x)+speed
  for x in range(1,len(spritesdata)):
    spritesdata[x].x+=spritesdata[x].speedx
    if playerdata.x < spritesdata[x].x + spritesdata[x].w and playerdata.x + playerdata.w > spritesdata[x].x and playerdata.y < spritesdata[x].y + spritesdata[x].h and playerdata.y + playerdata.h > spritesdata[x].y:
      if playerdata.x > spritesdata[x].x:
        playerdata.x = spritesdata[x].x+(playerdata.x-spritesdata[x].x)+spritesdata[x].speedx
      elif playerdata.x < spritesdata[x].x:
        playerdata.x = spritesdata[x].x+(playerdata.x-spritesdata[x].x)+spritesdata[x].speedx
      playerdata.x -= playerdata.speedx

  playerdata.y += playerdata.speedy

  if playerdata.y+20 > spritesdata[0].y + 200 or playerdata.y < spritesdata[0].y:
    if playerdata.y > spritesdata[0].y:
      playerdata.y = spritesdata[0].y+(playerdata.y-spritesdata[0].y)-speed
    elif playerdata.y < spritesdata[0].y:
      playerdata.y = spritesdata[0].y+(playerdata.y-spritesdata[0].y)+speed
  for x in range(1,len(spritesdata)):
    spritesdata[x].y+=spritesdata[x].speedy
    if playerdata.x < spritesdata[x].x + spritesdata[x].w and playerdata.x + playerdata.w > spritesdata[x].x and playerdata.y < spritesdata[x].y + spritesdata[x].h and playerdata.y + playerdata.h > spritesdata[x].y:
      if playerdata.y > spritesdata[x].y:
        playerdata.y = spritesdata[x].y+(playerdata.y-spritesdata[x].y)+spritesdata[x].speedy
      elif playerdata.y < spritesdata[x].y:
        playerdata.y = spritesdata[x].y+(playerdata.y-spritesdata[x].y)+spritesdata[x].speedy
      playerdata.y -= playerdata.speedy
  
  #-----UPDATES-----
  
  playersprite.rect.x=round(playerdata.x)
  playersprite.rect.y=round(playerdata.y)
  for x in range(len(spriterects)):
    spriterects[x].rect.x=round(spritesdata[x].x)
    spriterects[x].rect.y=round(spritesdata[x].y)
  camera.center = playersprite.rect.center
  window.fill((0,)*3)
  window.blit(spriterects[0].image.load('Rooms/Boss Room.png').convert(), (spriterects[0].rect.x - camera.x, spriterects[0].rect.y - camera.y))
  for sprite in spriterects:
    window.blit(sprite.surface, (sprite.rect.x - camera.x, sprite.rect.y - camera.y))
  
  window.blit(playersprite.image,(140,90))
  pygame.time.Clock().tick(150)
  pygame.display.flip()