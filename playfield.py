import pygame
import math
BLACK = (0, 0, 0)
SIDE_LENGTH = 800
paddle_width = 25
paddle_height = 75


class PlayField(pygame.sprite.Group):
  def __init__(self, color, num_players):
    super().__init__()
    coordinates = self.get_coordinates(num_players)
    # self.image = screen
    # self.image = pygame.Surface([width, height])
    # self.image.fill(BLACK)
    # self.image.set_colorkey(BLACK)
    # pygame.draw.polygon(self.image, color, coordinates, width)
    # self.rect = self.image.get_rect()
    # self.color = color
    self.draw_polygon(color, self.get_coordinates(num_players))

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
      line.image = pygame.Surface([abs(coordinate1[0] - coordinate2[0])+5, abs(coordinate1[1] - coordinate2[1])+5], pygame.SRCALPHA)
      pygame.draw.line(line.image, color, (coordinate1[0]-surface_x, coordinate1[1]-surface_y), (coordinate2[0]-surface_x, coordinate2[1]-surface_y),5)
      line.rect = line.image.get_rect()
      line.rect.x = surface_x
      line.rect.y = surface_y
      line.mask = pygame.mask.from_surface(line.image)
      dist = self.distance(coordinate1,coordinate2)

      line.min_x = min(coordinate1[0], coordinate2[0])
      line.min_y = min(coordinate1[1], coordinate2[1])
      line.max_x = max(coordinate1[0], coordinate2[0])
      line.max_y = max(coordinate1[1], coordinate2[1])
      line.c1 = coordinate1
      line.c2 = coordinate2
      
      line.sin = abs((coordinate1[1] - coordinate2[1]) / dist)
      line.cos = abs((coordinate1[0] - coordinate2[0]) / dist)
      line.slope = float("inf")
      
      if coordinate1[0] != coordinate2[0]:
        line.slope = (coordinate1[1] - coordinate2[1])/ (coordinate1[0] - coordinate2[0])
        if(line.slope > 0): line.cos *= -1
      
      self.add(line)
      