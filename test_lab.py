import pygame
from player import Paddle
from ball import Ball
from playfield import PlayField
import numpy as np
from math import sin,cos,pi,acos,asin
from random import uniform
import pymunk
import pymunk.pygame_util
import matplotlib.pyplot as plt
import pymunk.matplotlib_util


from pygame.locals import (
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  QUIT,
)

BLACK = (0,0,0)
WHITE = (255,255,255)
player_num = 2
  
if __name__ == "__main__":
  screen = pygame.display.set_mode((1000, 1000))
  SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

  clock = pygame.time.Clock()

  running = True
  playfield = PlayField(color=WHITE, num_players=3)
  ball = Ball((255, 255, 255), 24,24)
  ball.rect.x = playfield.margin_x+400
  ball.rect.y = playfield.margin_y+400
  ball.body.position = pymunk.pygame_util.from_pygame((ball.rect.x, ball.rect.y), ball.image)
  myboundary = playfield.sprites()[player_num]
  mypaddle = Paddle((255, 255, 255), 25, 75, myboundary, "my_paddle.png")
  all_sprites_list = pygame.sprite.Group()
  all_sprites_list.add(ball)
  ball_vel_magnitude = 500
  in_angle = uniform(0,2*pi)
  count = 0 
  space = pymunk.Space()
  # space.gravity = (0, 0)
  space.add(ball.body, ball.shape)
  ball.body.velocity = (ball_vel_magnitude*cos(in_angle), ball_vel_magnitude*sin(in_angle))
  space.add(playfield.body, *playfield.shape)
  space.add(mypaddle.body, mypaddle.shape)
  fig = plt.figure(figsize=(14,10))
  ax = plt.axes(xlim=(0, 1100), ylim=(0, 1100))
  ax.set_aspect("equal")
  o = pymunk.matplotlib_util.DrawOptions(ax)
  space.debug_draw(o)
  fig.savefig("matplotlib_util_demo.png", bbox_inches="tight")

  while running:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          running = False
          pygame.quit()
        if event.type == QUIT:
          running = False
          pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[K_RIGHT] : mypaddle.move(True)
    elif keys[pygame.K_DOWN] or keys[K_LEFT]: mypaddle.move()
    else: mypaddle.stop()
    
    screen.fill(BLACK)
    
    count +=1
    
    space.step(1/60)
    ball.rect.x, ball.rect.y = pymunk.pygame_util.to_pygame((ball.body.position.x-12, ball.body.position.y-12), ball.image)
    mypaddle.rect.x, mypaddle.rect.y = pymunk.pygame_util.to_pygame((mypaddle.body.position.x, mypaddle.body.position.y), mypaddle.image)
    mypaddle.rect.x -= 75/2
    mypaddle.rect.y -= 25/2
    playfield.draw(screen)
    all_sprites_list.draw(screen) 
    mypaddle.blitRotate(screen)
    # if ball.rect.x != ball.body.position.x or ball.rect.y != ball.body.position.y: print(ball.rect.x, ball.body.position.x, ball.rect.y, ball.body.position.y)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
