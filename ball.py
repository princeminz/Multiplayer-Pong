from math import degrees
import pygame
import pymunk
 
BLACK = (0, 0, 0)
 
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height, network):
        super().__init__()
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.width = width
        self.height = height
        self.network = network
        image = pygame.image.load('lazer_ball.png')
        self.image = pygame.Surface([width, height],pygame.SRCALPHA)
        self.image.blit(image, (0,0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.body = pymunk.Body()
        self.body.position = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
        self.shape = pymunk.Circle(self.body, 14)
        self.shape.density = 1
        self.shape.friction = 1
        self.shape.elasticity = 1
        self.shape.collision_type = 0
    
    def blitRotate(self, surf):
        image_rect = self.image.get_rect(topleft = (self.body.position.x - self.width/2, self.body.position.y-self.height/2))
        offset_center_to_pivot = pygame.math.Vector2(self.body.position) - image_rect.center
        angle = -self.body.velocity.angle_degrees
        rotated_offset = offset_center_to_pivot.rotate(angle)

        rotated_image_center = (self.body.position.x  - rotated_offset.x, self.body.position.y - rotated_offset.y)
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        surf.blit(rotated_image, rotated_image_rect)