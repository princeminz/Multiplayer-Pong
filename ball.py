import pygame
import pymunk
 
BLACK = (0, 0, 0)
 
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        image = pygame.image.load('ball.png')
        self.image = pygame.Surface([width, height],pygame.SRCALPHA)
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.image.blit(image, (0,0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.body = pymunk.Body()
        self.body.position = self.rect.x, self.rect.y
        self.shape = pymunk.Circle(self.body, width/2)
        self.shape.density = 1
        self.shape.friction = 1
        self.shape.elasticity = 1
        