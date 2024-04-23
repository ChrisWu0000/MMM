import pygame
import Spritesheet
from math import floor

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 500

#BG = (50, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('Enemies/Bell Sprite Sheet 3.png').convert_alpha()
sprite_sheet = Spritesheet.SpriteSheet(sprite_sheet_image)

i=0

walking=[]
for x in range(4):
    #for y in range (12):
    walking.append (sprite_sheet.get_image(i, 80, 80).convert_alpha())
    i+=1

attacking=[]
for x in range(4):
    #for y in range (12):
    attacking.append (sprite_sheet.get_image(i, 80, 80).convert_alpha())
    i+=1

damage=[]
for x in range(4):
    #for y in range (12):
    damage.append (sprite_sheet.get_image(i, 80, 80).convert_alpha())
    i+=1

death=[]
for x in range(4):
    #for y in range (12):
    death.append (sprite_sheet.get_image(i, 80, 80).convert_alpha())
    i+=1

i=0
j=0

run = True
while run:

    #update background
    #screen.fill(BG)
    screen.blit(pygame.image.load("Rooms/Level1.png").convert_alpha(), (0, 0))
    screen.blit(walking[floor(i)], (80,80))
   # screen.blit(attacking[floor(i)], (160,80))
    #screen.blit(damage[floor(i)], (240,80))
   # screen.blit(death[floor(i)], (320,80))
    #screen.blit(sprite_sheet_image, (0,0))
    #i+=.1
    #if(i>=4):
        #i=0

	#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    pygame.time.Clock().tick(120)
pygame.quit()