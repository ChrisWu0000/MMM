import pygame
monster_data = {
    "bell": {"health": 150, "attack_damage": 3, "speed": 1.1, "mass": 1, "push_power": 1, "spritesheet": pygame.image.load('Enemies/Bell Sprite Sheet.png'), "sprite_width": 60, "sprite_height": 60, "coin_drop_chance":0.6},
    "sax": {"health": 250, "attack_damage": 5, "speed": 0.6, "mass": 2, "push_power": 4, "spritesheet": pygame.image.load('Enemies/Sax Sprite Sheet.png'), "sprite_width": 93, "sprite_height": 117, "coin_drop_chance":0.9},
    "drum": {"health": 750, "attack_damage": 8, "speed": 0.8, "mass": 4, "push_power": 4, "spritesheet": pygame.image.load('Enemies/Drum Sprite Sheet.png'), "sprite_width": 90, "sprite_height": 90, "coin_drop_chance":1.0},
    "top_brass": {"health": 5000, "attack_damage": 10, "speed": 0.6, "mass": 10,  "push_power": 100, "spritesheet": pygame.image.load('Enemies/The Top Brass Spritesheet.png'), "sprite_width": 264, "sprite_height": 264}
}
