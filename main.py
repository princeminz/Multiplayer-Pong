import pygame
from player import Paddle
from ball import Ball

from playfield import PlayField

import time
import numpy as np
from network import Network
from menu import Menu


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


paddle_width = 25
paddle_height = 75





def get_new_velocity(ball_vel, line):

  d = np.array(list(ball_vel.values()))
  n = np.array([-(line.c1[1] - line.c2[1]), line.c1[0] - line.c2[0]])
  n_hat = n / np.linalg.norm(n)
  r = d - (2 * np.dot(d, n_hat)) * n_hat

  return {"x": r[0], "y": r[1]}


  
if __name__ == "__main__":
  
  pygame.init()
  screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  network = Network()
  Menu(screen, network)
  running = True

  playfield = PlayField(color=WHITE, num_players=player_match_status.count(3))
  if(player_match_status.count(3)==2 and player_num==1):
    myboundary = playfield.sprites()[2]
  else:
    myboundary = playfield.sprites()[player_num]
  mypaddle = Paddle((255, 255, 255), paddle_width,paddle_height, myboundary)
  client.dispatch_event('paddleMove', position = (mypaddle.rect.x-playfield.margin_x, mypaddle.rect.y-playfield.margin_y))
  all_sprites_list = pygame.sprite.Group()
  ball = Ball((255, 255, 255), 24, 24)
  all_sprites_list.add(ball)
  all_sprites_list.add(mypaddle)
  time.sleep(5)
  prev_x = ball_position['x']
  prev_y = ball_position['y']
  count, itr = 1, 1
  clock = pygame.time.Clock()  

  while running:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          running = False
      elif event.type == QUIT:
        running = False
    paddles = pygame.sprite.Group()
    paddle_sprite = {}
    for i in range(len(player_match_status)):
      if(player_match_status[i] == 3 and i != connection_num):
        x, y = paddle_position[i]
        paddle = None
        if player_match_status.count(3) == 2 and player_match_status[:i+1].count(3) == 2:
          paddle = Paddle((255, 255, 255), 25, 75, playfield.sprites()[2])   
        else:
          paddle = Paddle((255, 255, 255), 25, 75, playfield.sprites()[player_match_status[:i+1].count(3) - 1])
        paddle.rect.x = x + playfield.margin_x
        paddle.rect.y = y + playfield.margin_y
        paddles.add(paddle)
        paddle_sprite[i] = paddle

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      mypaddle.moveUp(5)
      client.dispatch_event('paddleMove', position = (mypaddle.rect.x-playfield.margin_x, mypaddle.rect.y-playfield.margin_y))
    if keys[pygame.K_DOWN]:
      mypaddle.moveDown(5)
      client.dispatch_event('paddleMove', position = (mypaddle.rect.x-playfield.margin_x, mypaddle.rect.y-playfield.margin_y))
    screen.fill(BLACK)


    # ball.rect.x = gamestate.ball_position['x']
    # ball.rect.y = gamestate.ball_position['y']
    # print(ready_players)
    x, y = ball_position['x'] + playfield.margin_x, ball_position['y'] + playfield.margin_y
    # print(x,y)
    if x != ball.rect.x: 
      ball.rect.x += (x - ball.rect.x) / itr
    if y != ball.rect.y: 
      ball.rect.y += (y - ball.rect.y) / itr
    
    if prev_x == x and prev_y == y:
      count += 1
    else:
      prev_x, prev_y = x, y
      itr = (itr + count) / 2
      count = 1

    # Collision 
    # for i, sprite in enumerate(playfield.sprites()):
    #     if pygame.sprite.collide_mask(ball,sprite): 
    #         print("Collided with", i)

    if pygame.sprite.collide_mask(myboundary, ball):
      client.dispatch_event("ballCollision","line",connection_num, get_new_velocity(ball_velocity, myboundary), ball_position)

    if pygame.sprite.collide_mask(mypaddle,ball):
      vel = get_new_velocity(ball_velocity, myboundary)
      # print(vel,ball_velocity)
      client.dispatch_event("ballCollision","paddle",connection_num, vel , ball_position)
    
    # print("ball_velocity: ", ball_velocity)



    playfield.draw(screen)
    all_sprites_list.draw(screen) 
    paddles.draw(screen) 
    pygame.display.flip()
    clock.tick(60)
    # print("itr: ", itr, "(x - ball.rect.x)", (x - ball.rect.x), "(y - ball.rect.y)", y - ball.rect.y)

pygame.quit()