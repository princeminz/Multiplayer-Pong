import pygame
import pymunk
from pymunk.vec2d import Vec2d
from math import degrees, asin, acos, pi, radians

WHITE = (255, 255, 255)
BLACK = (0,0,0)


class Paddle(pygame.sprite.Sprite):
  def __init__(self, color, width, height, line, image_name):
    super().__init__()
    image = pygame.image.load(image_name)
    self.image = pygame.Surface([width, height],pygame.SRCALPHA)
    self.image.fill(BLACK)
    
    # self.image.set_colorkey((150,0,0))
    pygame.draw.rect(self.image, color, [0, 0, width, height])

    for y in range(0, height, image.get_rect().size[1]):
      for x in range(0, width, image.get_rect().size[0]):
        self.image.blit(image, (x,y))

    self.rect = self.image.get_rect()
    self.line = line

    self.angle = 90 - round( degrees( asin( abs(self.line.v_hat.y) ) ), -1)
    if line.slope < 0: self.angle *= -1
    self.width = width
    self.height = height
    self.translated_mid = self.translate_to_middle(self.line.midpoint)
    self.velocity_magnitude = 400
    self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
    x, y = self.translate_to_middle(self.line.midpoint)
    self.body.position = pymunk.pygame_util.from_pygame((x, y), self.image)
    self.shape = pymunk.Segment(self.body, (0, -height/2), (0, height/2), width/2)
    self.body.angle = -radians(self.angle)
    self.shape.friction = 0
    self.shape.elasticity = 1
    self.shape.collision_type = 1
    self.shape.density = 50

  def move(self, reverse=False):
    # self.translate_to_middle(self.line.midpoint).get_distance(self.body.position) + self.height / 2 < self.line.length
    
    if reverse and (self.translated_mid - 5*self.line.v_hat).get_distance(self.body.position) + self.height / 2 < self.line.length / 2:
      self.body.velocity = self.velocity_magnitude * self.line.v_hat
    elif reverse == False and (self.translated_mid + 5*self.line.v_hat).get_distance(self.body.position) + self.height / 2 < self.line.length / 2:
      self.body.velocity = -self.velocity_magnitude * self.line.v_hat
    else:
      self.body.velocity = 0, 0

  def stop(self):
      self.body.velocity = 0, 0
  
  def blitRotate(self, surf):

    image_rect = self.image.get_rect(topleft = (self.body.position.x - self.width/2, self.body.position.y-self.height/2))
    offset_center_to_pivot = pygame.math.Vector2(self.body.position) - image_rect.center
    
    rotated_offset = offset_center_to_pivot.rotate(-self.angle)

    rotated_image_center = (self.body.position.x  - rotated_offset.x, self.body.position.y - rotated_offset.y)
    rotated_image = pygame.transform.rotate(self.image, self.angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    surf.blit(rotated_image, rotated_image_rect)
  
  def translate_to_middle(self, v):
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    n_hat = self.line.v_hat.perpendicular_normal()
    if (v + (self.width/2+10)*n_hat).get_distance(Vec2d(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) < (v - (self.width/2+10)*n_hat).get_distance(Vec2d(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)):
      return v + self.width/2*n_hat
    else:
      return v - self.width/2*n_hat

  