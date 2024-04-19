import pygame
import Spritesheet

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 500

BG = (50, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('Enemies/Bell Sprite Sheet 3.png').convert_alpha()
sprite_sheet = Spritesheet.SpriteSheet(sprite_sheet_image)

i=0

walking=[]
for x in range(4):
    walking.append (sprite_sheet.get_image(i, 80, 80).convert_alpha())
    i+=1

attacking=[]
for x in range(4):
    attacking.append (sprite_sheet.get_image(i, 80, 80).convert_alpha())
    i+=1

damage=[]
for x in range(4):
    attacking.append (sprite_sheet.get_image(i, 80, 80).convert_alpha())
    i+=1

death=[]
for x in range(4):
    death.append (sprite_sheet.get_image(i, 80, 80).convert_alpha())
    i+=1

i=0
j=0

run = True
while run:

    #update background
    screen.fill(BG)

    screen.blit(walking[i], (80,80))
    screen.blit(attacking[i], (160,80))
    screen.blit(damage[i], (240,80))
    screen.blit(death[i], (320,80))
    i+=1
    if(i>=4):
        i=0

	#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()