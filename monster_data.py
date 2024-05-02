import pygame
monster_data = {
    "bell": {"health": 150, "attack_damage": 3, "speed": 2, "mass": 1, "push_power": 1, "collisionrect": pygame.Rect(12,24,40,56), "spritesheet": pygame.image.load('Enemies/Bell Sprite Sheet.png'), "sprite_width": 80, "sprite_height": 80},
    "sax": {"health": 250, "attack_damage": 5, "speed": 1, "mass": 2, "push_power": 4, "collisionrect": pygame.Rect(40,16,60,128), "spritesheet": pygame.image.load('Enemies/Sax Sprite Sheet.png'), "sprite_width": 124, "sprite_height": 156}, 
    "top_brass": {"health": 1000, "attack_damage": 10, "speed": 0.75, "mass": 10,  "push_power": 100, "collisionrect": pygame.Rect(1,1,1,1), "spritesheet": pygame.image.load('Enemies/Top Brass Sprite Sheet.png'), "sprite_width": 264, "sprite_height": 264}
}
