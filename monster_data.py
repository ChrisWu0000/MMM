import pygame
monster_data = {
    "bell": {"health": 150, "attack_damage": 3, "speed": 2, "mass": 1, "image": pygame.image.load("Enemies/Bell.png"), "push_power": 1, "collisionrect": pygame.Rect(12,24,40,56), "spritesheet": pygame.image.load('Enemies/Bell Sprite Sheet 3.png')},
    "sax": {"health": 250, "attack_damage": 5, "speed": 1, "mass": 2, "image": pygame.image.load("Enemies/Sax.png"), "push_power": 4, "collisionrect": pygame.Rect(40,16,60,128), "spritesheet": pygame.image.load('Enemies/Bell Sprite Sheet 3.png')},
}
