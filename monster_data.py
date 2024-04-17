import pygame
monster_data = {
    "bell": {"health": 15, "damage": 3, "speed": 2, "image": pygame.image.load("Enemies/Bell.png"), "image_scale": 1, "collisionrect": pygame.Rect(12,24,40,56)},
    "sax": {"health": 25, "damage": 5, "speed": 1,  "image": pygame.image.load("Enemies/Sax.png"), "image_scale": 1, "collisionrect": pygame.Rect(40,16,60,128)},
}
