import pygame
from math import degrees, asin, acos
BLACK = (0,0,0)


class Paddle(pygame.sprite.Sprite):
  def __init__(self, color, width, height, line):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill(BLACK)
    self.image.set_colorkey(BLACK)
    pygame.draw.rect(self.image, color, [0, 0, width, height])
    self.rect = self.image.get_rect()
    self.line = line
    # print(self.line.sin,"sin")
    angle = 90 - round( degrees( asin( self.line.sin ) ), -1)
    if line.slope < 0: angle *=-1
    self.image = pygame.transform.rotate(self.image, angle )
    # print(angle) 
    self.width = width
    self.height = height
    self.rect.x = (self.line.max_x + self.line.min_x)/2 - self.width*self.line.sin/2
    self.rect.y = (self.line.max_y + self.line.min_y)/2 - self.width*abs(self.line.cos)/2
    

  def moveUp(self, pixels):
    if self.line.c2[0]!=self.line.c1[0]:
      slope = (self.line.c2[1] - self.line.c1[1]) / (self.line.c2[0] - self.line.c1[0])
      self.rect.x += pixels * self.line.cos
      c = self.line.c1[1] - slope*self.line.c1[0]
      y = slope * self.rect.x + c
      self.rect.y = y
    else:
      self.rect.y -= pixels
    

    if self.rect.x < self.line.min_x:
      self.rect.x = self.line.min_x
    if self.rect.y < self.line.min_y:
      self.rect.y = self.line.min_y
    
    if self.rect.x > self.line.max_x-self.height*abs(self.line.cos):
      self.rect.x = self.line.max_x-self.height*abs(self.line.cos)
    if self.rect.y > self.line.max_y-self.height*self.line.sin:
      self.rect.y = self.line.max_y-self.height*self.line.sin

    self.rect.x -= self.width*self.line.sin/2
    self.rect.y -= self.width*abs(self.line.cos)/2

  def moveDown(self, pixels):
    # self.rect.y += self.line.sin*pixels
    # self.rect.x -= self.line.cos*pixels
    if self.line.c2[0]!=self.line.c1[0]:
      slope = (self.line.c2[1] - self.line.c1[1]) / (self.line.c2[0] - self.line.c1[0])
      self.rect.x -= pixels * self.line.cos
      c = self.line.c1[1] - slope*self.line.c1[0]
      y = slope * self.rect.x + c
      self.rect.y = y
    else:
      self.rect.y += pixels
    
    if self.rect.x < self.line.min_x:
      self.rect.x = self.line.min_x
    if self.rect.y < self.line.min_y:
      self.rect.y = self.line.min_y
    
    if self.rect.x > self.line.max_x-self.height*abs(self.line.cos):
      self.rect.x = self.line.max_x-self.height*abs(self.line.cos)
      # print(self.rect.x,"x")
    if self.rect.y > self.line.max_y-self.height*self.line.sin:
      self.rect.y = self.line.max_y-self.height*self.line.sin
      # print(self.rect.y,"y")

    self.rect.x -= self.width*self.line.sin/2
    self.rect.y -= self.width*abs(self.line.cos)/2
      
