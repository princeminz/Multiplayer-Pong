import pygame
from math import degrees, asin, acos

WHITE = (255, 255, 255)
BLACK = (0,0,0)


class Paddle(pygame.sprite.Sprite):
  def __init__(self, color, width, height, line):
    super().__init__()
    image = pygame.image.load('paddle.png')
    self.image = pygame.Surface([width, height],pygame.SRCALPHA)
    self.image.fill(BLACK)
    
    # self.image.set_colorkey(BLACK)
    pygame.draw.rect(self.image, color, [0, 0, width, height])

    for y in range(0, height, image.get_rect().size[1]):
      for x in range(0, width, image.get_rect().size[0]):
        self.image.blit(image, (x,y))

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
    # self.rect.x = (self.line.max_x + self.line.min_x)/2
    # self.rect.y = (self.line.max_y + self.line.min_y)/2
    self.x = self.rect.x
  def moveUp(self, pixels):
    xx = self.x
    yy = self.rect.y
    if self.line.c2[0] != self.line.c1[0]:
      # self.rect.x += self.width*self.line.sin/2
      self.x += pixels * self.line.cos
      self.rect.x = self.x
      c = self.line.c1[1] - self.line.slope*self.line.c1[0]
      y = self.line.slope * self.x + c

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
    self.rect.y -= self.width*self.line.cos/2
    # print("up",(self.x-xx)**2+(self.rect.y-yy)**2)

  def moveDown(self, pixels):
    xx = self.x
    yy = self.rect.y
    # self.rect.y += self.line.sin*pixels
    # self.rect.x -= self.line.cos*pixels
    if self.line.c2[0]!=self.line.c1[0]:
      # self.rect.x += self.width*self.line.sin/2   
      
      self.x -= (pixels * self.line.cos)
      self.rect.x = self.x
      c = self.line.c1[1] - self.line.slope*self.line.c1[0]
      # print("down", pixels,pixels*self.line.cos, self.rect.x-xx)

      
      y = self.line.slope * self.x + c
      self.rect.y = y
    else:
      self.rect.y += pixels
    
    if self.rect.x < self.line.min_x:
      self.rect.x = self.line.min_x
    if self.rect.y < self.line.min_y:
      self.rect.y = self.line.min_y
    
    if self.rect.x > self.line.max_x-self.height*abs(self.line.cos):
      self.rect.x = self.line.max_x-self.height*abs(self.line.cos)
    if self.rect.y > self.line.max_y-self.height*self.line.sin:
      self.rect.y = self.line.max_y-self.height*self.line.sin

    self.rect.x -= self.width*self.line.sin/2
    self.rect.y -= self.width*self.line.cos/2
    # print("down",(self.x-xx)**2+(self.rect.y-yy)**2)

      
