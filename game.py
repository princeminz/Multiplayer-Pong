import pygame
from playfield import PlayField
from player import Paddle
from ball import Ball
import numpy as np
from pygame.locals import (
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  QUIT,
)
paddle_width = 25
paddle_height = 75
BLACK = (0,0,0)
WHITE = (255,255,255)

class Game:
    def __init__(self, screen, network) -> None:
        playfield = PlayField(color=WHITE, num_players=network.player_match_status.count(3))
        if(network.player_match_status.count(3)==2 and network.player_num==1):
            myboundary = playfield.sprites()[2]
        else:
            myboundary = playfield.sprites()[network.player_num]
        mypaddle = Paddle((255, 255, 255), paddle_width,paddle_height, myboundary)
        network.client.dispatch_event('paddleMove', position = (mypaddle.rect.x-playfield.margin_x, mypaddle.rect.y-playfield.margin_y))
        all_sprites_list = pygame.sprite.Group()
        ball = Ball((255, 255, 255), 24, 24)
        all_sprites_list.add(ball)
        all_sprites_list.add(mypaddle)
        prev_x = network.ball_position['x']
        prev_y = network.ball_position['y']
        count, itr = 1, 1
        clock = pygame.time.Clock()  
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                        running = False
            paddles = pygame.sprite.Group()
            paddle_sprite = {}
            for i in range(len(network.player_match_status)):
                if(network.player_match_status[i] == 3 and i != network.connection_num):
                    x, y = network.paddle_position[i]
                    paddle = None
                    if network.player_match_status.count(3) == 2 and network.player_match_status[:i+1].count(3) == 2:
                        paddle = Paddle((255, 255, 255), 25, 75, playfield.sprites()[2])   
                    else:
                        paddle = Paddle((255, 255, 255), 25, 75, playfield.sprites()[network.player_match_status[:i+1].count(3) - 1])
                        paddle.rect.x = x + playfield.margin_x
                        paddle.rect.y = y + playfield.margin_y
                        paddles.add(paddle)
                        paddle_sprite[i] = paddle

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                mypaddle.moveUp(5)
                network.client.dispatch_event('paddleMove', position = (mypaddle.rect.x-playfield.margin_x, mypaddle.rect.y-playfield.margin_y))
            if keys[pygame.K_DOWN]:
                mypaddle.moveDown(5)
                network.client.dispatch_event('paddleMove', position = (mypaddle.rect.x-playfield.margin_x, mypaddle.rect.y-playfield.margin_y))
            screen.fill(BLACK)

            x, y = network.ball_position['x'] + playfield.margin_x, network.ball_position['y'] + playfield.margin_y
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
            if pygame.sprite.collide_mask(myboundary, ball):
                network.client.dispatch_event("ballCollision", "line", network.connection_num, self.get_new_velocity(network.ball_velocity, myboundary), network.ball_position)

            if pygame.sprite.collide_mask(mypaddle,ball):
                vel = self.get_new_velocity(network.ball_velocity, myboundary)
                network.client.dispatch_event("ballCollision", "paddle", network.connection_num, vel, network.ball_position)
            
            playfield.draw(screen)
            all_sprites_list.draw(screen) 
            paddles.draw(screen) 
            pygame.display.flip()
            clock.tick(60)

    def get_new_velocity(self, ball_vel, line):
        d = np.array(list(ball_vel.values()))
        n = np.array([-(line.c1[1] - line.c2[1]), line.c1[0] - line.c2[0]])
        n_hat = n / np.linalg.norm(n)
        r = d - (2 * np.dot(d, n_hat)) * n_hat

        return {"x": r[0], "y": r[1]}