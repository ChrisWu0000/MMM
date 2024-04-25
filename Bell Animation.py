import pygame
import Spritesheet

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 500

BG = (50, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('Player/Trent Sprite Sheet.png').convert_alpha()
sprite_sheet = Spritesheet.SpriteSheet(sprite_sheet_image)

i=0

walking=[]
for x in range(4):
    walking.append (sprite_sheet.get_image(i, 88, 104).convert_alpha())
    i+=1

attacking=[]
for x in range(4):
    attacking.append (sprite_sheet.get_image(i, 88, 104).convert_alpha())
    i+=1

damage=[]
for x in range(2):
    damage.append (sprite_sheet.get_image(i, 88, 104).convert_alpha())
    i+=1
for x in range(2):
    damage.append (sprite_sheet.get_image(i-2, 88, 104).convert_alpha())
    i+=1

death=[]
for x in range(4):
    death.append (sprite_sheet.get_image(i, 104, 104).convert_alpha())
    i+=1

i=0
j=0
takingdamage=False
#if damage is taken, regardless of remaining hp, set j to 4 and i to 0

run = True
while run:

    #update background
    screen.fill(BG)

    screen.blit(walking[i], (88,80))
    screen.blit(attacking[i], (176,80))
    screen.blit(damage[i], (264,80))
    screen.blit(death[i], (352,80))
    i+=0.1
    if(i>=4):
        i=0
	#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()