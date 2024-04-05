import pygame
pygame.init()
hihiiiiiiiiiiiiiiiiii=0
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
#---DO NOT GO OVER 500 SPRITES!!!!!!---
spritesdata = [spritedata(300,200,0,0,0,0)]
bg = pygame.image.load('Enemies/DevlinDeving.png')
bg_width = bg.get_width()
bg_height =bg.get_height()
spriterects = [create_sprite(bg_width, bg_height, 0,0,'Enemies/DevlinDeving.png')]
for x in range(1):
  for y in range(1):
    spriterects.append(create_sprite(15,20,60*x,60*y,'Enemies/DevlinDeving.png'))
    spritesdata.append(spritedata(15,20,60*x,60*y,0,0))
#spriterects[0].image.convert_alpha()
playersprite = player_sprite()
playerdata = spritedata(20, 20, 140, 90,0,0)


speed=0.8
running = True
fox = pygame.key.get_pressed()
cooldown=0
timer = pygame.time.Clock() 
sparetimer1 = pygame.USEREVENT + 1
pygame.time.set_timer(sparetimer1,5000)
cooldownup1 = pygame.USEREVENT + 2

while running:
  clock.tick(120)
  for event in pygame.event.get():
    if event.type == sparetimer1:
      spritesdata[1].speedx=0
      spritesdata[1].speedy=0
    if event.type == cooldownup1:
      cooldown=0
    if event.type == pygame.QUIT:
      running = False

    #-----PLAYER INPUTS-----

    if event.type == pygame.KEYDOWN:
      playersprite.image.fill((0,50,0))
      if event.key == pygame.K_ESCAPE:
        running=False
      if event.key == pygame.K_DOWN and cooldown!=1:
        pygame.time.set_timer(cooldownup1, 1, loops=1)
        spritesdata[1].speedy+=0.1
        cooldown=1
      if event.key == pygame.K_e and cooldown!=1:
        pygame.time.set_timer(cooldownup1, 1, loops=1)
        speed+=0.1
        cooldown=1
      if event.key == pygame.K_UP and cooldown!=1:
        pygame.time.set_timer(cooldownup1, 1, loops=1)
        spritesdata[1].speedy-=0.1
        cooldown=1
      if event.key == pygame.K_RIGHT and cooldown!=1:
        pygame.time.set_timer(cooldownup1, 1, loops=1)
        spritesdata[1].speedx+=0.1
        cooldown=1
      if event.key == pygame.K_LEFT and cooldown!=1:
        pygame.time.set_timer(cooldownup1, 1, loops=1)
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
  
  if playerdata.x+20 > spritesdata[0].x + bg_width or playerdata.x < spritesdata[0].x:
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

  if playerdata.y+20 > spritesdata[0].y + bg_height or playerdata.y < spritesdata[0].y:
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
  
  playersprite.rect.x=playerdata.x
  playersprite.rect.y=playerdata.y
  for x in range(len(spriterects)):
    spriterects[x].rect.x=spritesdata[x].x
    spriterects[x].rect.y=spritesdata[x].y
  camera.center = playersprite.rect.center
  window.fill((0,)*3)
  window.blit(spriterects[0].image,(spriterects[0].rect.x-camera.x,spriterects[0].rect.y-camera.y))
  for sprite in spriterects[1:]:
    window.blit(sprite.image, (sprite.rect.x - camera.x, sprite.rect.y - camera.y))
  window.blit(playersprite.image,(140,90))
  pygame.display.flip()