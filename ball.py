import pygame
 
BLACK = (0, 0, 0)
 
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        image = pygame.image.load('ball.png')
        self.image = pygame.Surface([width, height],pygame.SRCALPHA)
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        # pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.image.blit(image, (0,0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        