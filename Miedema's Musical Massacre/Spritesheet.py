import pygame

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, x):
		image = pygame.Surface((width, height)).convert_alpha()
		image.fill((0,0,1))
		image.blit(self.sheet, (0, 0), ((frame * x),0, width, height))
		
		image.set_colorkey((0,0,1))
		return image