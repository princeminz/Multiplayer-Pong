import pygame
import pymunk
import math
from pymunk.vec2d import Vec2d
BLACK = (0, 0, 0)
SIDE_LENGTH = 1000
paddle_width = 25
paddle_height = 75


class PlayField(pygame.sprite.Group):
  def __init__(self, color, num_players, player_num = -1):
    super().__init__()
    coordinates = self.get_coordinates(num_players)
    self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
    self.body.position = 0, 0
    self.draw_polygon(color, coordinates)
    self.create_shape()
    if(num_players == 2 and player_num == 2):
      self.shape[2].collision_type = 2
      self.my_line = self.sprites()[2]
    elif player_num != -1:
      self.shape[player_num - 1].collision_type = 2
      self.my_line = self.sprites()[player_num - 1]
  
  def create_shape(self):
    self.shape = [  pymunk.Segment(self.body, 
                    pymunk.pygame_util.from_pygame(line.c1, line.image), 
                    pymunk.pygame_util.from_pygame(line.c2, line.image), 
                    10) for line in self.sprites() ]
    for segment in self.shape: segment.elasticity = 1

  def get_coordinates(self, n):
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    self.margin_x = (SCREEN_WIDTH - SIDE_LENGTH) / 2
    altitude = 0.86602*SIDE_LENGTH
    if n in [2, 4]:
      self.margin_y = (SCREEN_HEIGHT - SIDE_LENGTH) / 2
      return [(self.margin_x, SCREEN_HEIGHT-self.margin_y), (self.margin_x, self.margin_y), (SCREEN_WIDTH-self.margin_x, self.margin_y), (SCREEN_WIDTH-self.margin_x, SCREEN_HEIGHT-self.margin_y)]
    if n == 3:
      self.margin_y = (SCREEN_HEIGHT - altitude) / 2
      return [(self.margin_x, SCREEN_HEIGHT-self.margin_y), (SCREEN_WIDTH-self.margin_x, SCREEN_HEIGHT-self.margin_y), (SCREEN_WIDTH / 2, self.margin_y)]
  
  def distance(self, coordinate1, coordinate2):
    return ( (coordinate1[0] - coordinate2[0])**2 + (coordinate1[1] - coordinate2[1])**2 ) ** 0.5
  
  def draw_polygon(self, color, coordinates):
    print(coordinates)
    for coordinate1, coordinate2 in zip(coordinates, coordinates[1:] + coordinates[:1]):
      line = pygame.sprite.Sprite()
      surface_x = min(coordinate1[0], coordinate2[0]) 
      surface_y = min(coordinate1[1], coordinate2[1])
      line.image = pygame.Surface([abs(coordinate1[0] - coordinate2[0])+10, abs(coordinate1[1] - coordinate2[1])+10], pygame.SRCALPHA)
      pygame.draw.line(line.image, color, (coordinate1[0]-surface_x, coordinate1[1]-surface_y), (coordinate2[0]-surface_x, coordinate2[1]-surface_y),10)
      line.rect = line.image.get_rect()
      line.rect.x = surface_x
      line.rect.y = surface_y
      line.mask = pygame.mask.from_surface(line.image)
      
      line.slope = float("inf")
      v_x = coordinate1[0] - coordinate2[0] 
      v_y = coordinate1[1] - coordinate2[1]
      if v_x != 0: line.slope = v_y / v_x
      line.length = self.distance(coordinate1, coordinate2)
      
      if v_y == 0: v_x = abs(v_x)
      if v_x == 0: v_y = abs(v_y)
      
      if line.slope > 0: v_x, v_y = -v_x, -v_y

      line.v_hat = Vec2d(v_x / line.length, v_y / line.length)
      line.min_x = min(coordinate1[0], coordinate2[0])
      line.min_y = min(coordinate1[1], coordinate2[1])
      line.max_x = max(coordinate1[0], coordinate2[0])
      line.max_y = max(coordinate1[1], coordinate2[1])
      line.midpoint = Vec2d((coordinate1[0] + coordinate2[0]) / 2, (coordinate1[1] + coordinate2[1]) / 2)
      line.c1 = coordinate1
      line.c2 = coordinate2
      
      self.add(line)
      