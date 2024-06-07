import pygame
monster_data = {
    "bell": {"health": 100, "attack_damage": 6, "speed": 1.4, "mass": 1, "push_power": 1,"attack_frames":4, "spritesheet": pygame.image.load('Enemies/Bell Sprite Sheet.png'), "sprite_width": 60, "sprite_height": 60, "coin_drop_chance":1, "coin_drop":1},
    "bell2": {"health": 100, "attack_damage": 6, "speed": 1.4, "mass": 1, "push_power": 1,"attack_frames":4, "spritesheet": pygame.image.load('Enemies/Bell Sprite Sheet.png'), "sprite_width": 60, "sprite_height": 60, "coin_drop_chance":0, "coin_drop":0},
    "sax": {"health": 200, "attack_damage": 2, "speed": 0.4, "mass": 2, "push_power": 4,"attack_frames":4, "spritesheet": pygame.image.load('Enemies/Sax Sprite Sheet.png'), "sprite_width": 93, "sprite_height": 117, "coin_drop_chance":1, "coin_drop":2},
    "drum": {"health": 600, "attack_damage": 5, "speed": 0.6, "mass": 4, "push_power": 4,"attack_frames":8, "spritesheet": pygame.image.load('Enemies/Drum Sprite Sheet.png'), "sprite_width": 90, "sprite_height": 90, "coin_drop_chance":1, "coin_drop":3},
    "top_brass": {"health": 3000, "attack_damage": 8, "speed": 0.3, "mass": 10,  "push_power": 100, "spritesheet": pygame.image.load('Enemies/The Top Brass Spritesheet.png'), "sprite_width": 264, "sprite_height": 264}
}
