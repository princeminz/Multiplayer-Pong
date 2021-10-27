import pygame
from player import Paddle
from ball import Ball
from pygase import Client
from playfield import PlayField
import threading
import time
import numpy as np
from math import sin,cos,pi,acos,asin
from random import uniform


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
ready_players = [True, True, True]
  
if __name__ == "__main__":
  screen = pygame.display.set_mode((1900, 1060))
  SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

  clock = pygame.time.Clock()

  running = True
  playfield = PlayField(color=WHITE, num_players=4)
  ball = Ball((255, 255, 255), 24,24)
  ball.rect.x = playfield.margin_x+400
  ball.rect.y = playfield.margin_y+400
  myboundary = playfield.sprites()[player_num]
  mypaddle = Paddle((255, 255, 255), 25, 75, myboundary)
  all_sprites_list = pygame.sprite.Group()
  all_sprites_list.add(ball)
  all_sprites_list.add(mypaddle)
  ball_vel_magnitude = 8
  in_angle = uniform(0,2*pi)
  ball_vel = {"x":cos(in_angle),"y":sin(in_angle)}
  count = 0 
  while running:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            running = False
      elif event.type == QUIT:
        running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      mypaddle.moveUp(5)
    if keys[pygame.K_DOWN]:
      mypaddle.moveDown(5)
    screen.fill(BLACK)

    for line in playfield.sprites():
      if  pygame.sprite.collide_mask(ball,line) and count!=1:
        #  𝑟 = 𝑑 − 2𝑑 ⋅ 𝑛 / (‖𝑛‖^2) 𝑛
        d = np.array(list(ball_vel.values()))

        n = np.array([-(line.c1[1] - line.c2[1]), line.c1[0] - line.c2[0]])
        n_hat = n / np.linalg.norm(n)
        
        r = d - (2 * np.dot(d, n_hat)) * n_hat
        # print("prev", ball_vel, d, n, n_hat)
        ball_vel["x"] = r[0]
        ball_vel["y"] = r[1]
        # print("after", ball_vel, d, n, n_hat)
        count = 0
    

    count +=1
    ball.rect.x += ball_vel["x"]*ball_vel_magnitude
    ball.rect.y += ball_vel["y"]*ball_vel_magnitude
    # print(ball.rect.x,ball.rect.y)

    playfield.draw(screen)
    all_sprites_list.draw(screen) 
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
