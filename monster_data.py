import pygame
monster_data = {
    "bell": {"health": 150, "attack_damage": 3, "speed": 1.3, "mass": 1, "push_power": 1, "spritesheet": pygame.image.load('Enemies/Bell Sprite Sheet.png'), "sprite_width": 80, "sprite_height": 80},
    "sax": {"health": 250, "attack_damage": 5, "speed": 0.8, "mass": 2, "push_power": 4, "spritesheet": pygame.image.load('Enemies/Sax Sprite Sheet.png'), "sprite_width": 124, "sprite_height": 156}, 
    "top_brass": {"health": 1000, "attack_damage": 10, "speed": 0.6, "mass": 10,  "push_power": 100, "spritesheet": pygame.image.load('Enemies/Top Brass Sprite Sheet.png'), "sprite_width": 264, "sprite_height": 264}
}
