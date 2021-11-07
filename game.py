import pygame
from time import sleep
from playfield import PlayField
from player import Paddle
from ball import Ball
import numpy as np
from math import sin,cos,pi,acos,asin
from random import uniform
from final_screen import Final_Screen
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
from pygame.locals import (
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  QUIT,
  K_SPACE
)

paddle_width = 25
paddle_height = 75
network = None
playfield_margin = None
BLACK = (0,0,0)
WHITE = (255,255,255)

class Game:
    def __init__(self, screen, net) -> None:
        global network
        network = net
        self.screen = screen
        self.network = net
        self.network.client.register_event_handler("reinitGameloop", self.reinit_gameloop)
        self.network.client.register_event_handler("stopMessage", self.stop_message)
        self.network.client.register_event_handler("collisionData", self.on_collision)
        self.message_on = True
        self.message = "Game Starting"
        while network.running and list(self.network.player_match_status.values()).count(3) > 1:
            sleep(1)
            print("Game starting")
            self.gameloop()
        Final_Screen(screen,network,self.message)
        print("Exiting")

    def reinit_gameloop(self,message):
        self.running = False
        self.message = message
        self.message_on = True

    def on_collision(self, ball_position, ball_velocity):
        print("ball pos and vel:",ball_position,ball_velocity)
        self.ball.body.velocity = (ball_velocity['x'], ball_velocity['y'])
        self.ball.body.position = Vec2d(ball_position['x'], ball_position['y']) + self.margin
        self.space.step(network.client.connection.latency/2)

    def gameloop(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.network.player_num =list(self.network.player_match_status.values())[:list(self.network.player_match_status.keys()).index(self.network.connection_num)+1].count(3)
        self.running = self.network.running
        num_players = list(self.network.player_match_status.values()).count(3)
        all_sprites_list = pygame.sprite.Group()
        ball = Ball((255, 255, 255), 123, 119, self.network)
        # all_sprites_list.add(ball)
        if self.network.player_match_status[self.network.connection_num]==3:
            playfield = PlayField(color=WHITE, num_players=num_players, player_num=self.network.player_num)
            mypaddle = Paddle((255, 255, 255), paddle_width,paddle_height, playfield.my_line, "my_paddle.png")
            self.network.client.dispatch_event('paddleMove', position = (mypaddle.body.position[0]-playfield.margin_x, mypaddle.body.position[1]-playfield.margin_y))
        
        # prev_x = self.network.ball_position['x']
        # prev_y = self.network.ball_position['y']
        self.ball = ball
        self.margin = Vec2d(playfield.margin_x, playfield.margin_y)
        count, itr = 1, 1
        clock = pygame.time.Clock()  
        print(self.network.player_match_status)
        font = pygame.font.Font('font.ttf', 32) 
        heart_image = pygame.image.load('heart.png')
        heart_size = heart_image.get_rect().size
        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        space = pymunk.Space()
        self.space = space
        space.add(ball.body, ball.shape)
        
        space.add(playfield.body, *playfield.shape)
        space.add(mypaddle.body, mypaddle.shape)
        
        paddle_collision_handler = space.add_collision_handler(0, 1)
        line_collision_handler = space.add_collision_handler(0, 2)
        paddle_collision_handler.post_solve = paddle_collision
        line_collision_handler.post_solve = line_collision
        global playfield_margin
        playfield_margin = self.margin

        while self.running:
            self.screen.blit(background, (0, 0))

            heart_y = 50
            for i in self.network.player_lives.keys():
                player_text_x = 50
                heart_x = player_text_x + 160
                if self.network.player_match_status[i] in [3,4]:
                    player_text = font.render('Player ' + str(i) + ':', True, WHITE)
                    self.screen.blit(player_text, (player_text_x, heart_y))
                    for j in range(self.network.player_lives[i]):
                        self.screen.blit(heart_image,(heart_x, heart_y - 10))
                        heart_x += heart_size[0] + 5    
                    heart_y += heart_size[1]+10
                    

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                        self.network.stop()
                        pygame.quit()
                elif event.type == QUIT:
                    self.running = False
                    self.network.stop()
                    pygame.quit()

            paddles = pygame.sprite.Group()
            match_status = list(self.network.player_match_status.values())
            for i, (connection_num, status) in enumerate(self.network.player_match_status.items()):
                if(status == 3 and connection_num != self.network.connection_num):
                    x, y = self.network.paddle_position[connection_num]
                    paddle = None
                    if num_players == 2 and match_status[:i+1].count(3) == 2:
                        paddle = Paddle((255, 255, 255), 25, 75, playfield.sprites()[2],'paddle.png')   
                    else:
                        paddle = Paddle((255, 255, 255), 25, 75, playfield.sprites()[match_status[:i+1].count(3) - 1],'paddle.png')
                    paddle.body.position = (x + playfield.margin_x, y + playfield.margin_y)
                    paddles.add(paddle)

            if self.network.player_match_status[self.network.connection_num] == 3:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] or keys[K_RIGHT] : 
                    mypaddle.move(True) 
                    self.network.client.dispatch_event('paddleMove', position = (mypaddle.body.position[0]-playfield.margin_x, mypaddle.body.position[1]-playfield.margin_y))
                elif keys[pygame.K_DOWN] or keys[K_LEFT]: 
                    mypaddle.move()
                    self.network.client.dispatch_event('paddleMove', position = (mypaddle.body.position[0]-playfield.margin_x, mypaddle.body.position[1]-playfield.margin_y))
                else: mypaddle.stop()
    

                # Collision 
                # if pygame.sprite.collide_mask(myboundary, ball):
                #     self.network.client.dispatch_event("ballCollision", "line", self.network.connection_num, self.get_new_velocity(self.network.ball_velocity, myboundary), self.network.ball_position)

                # if pygame.sprite.collide_mask(mypaddle,ball):
                #     vel = self.get_new_velocity(self.network.ball_velocity, myboundary)
                #     self.network.client.dispatch_event("ballCollision", "paddle", self.network.connection_num, vel, self.network.ball_position)

            
            # x, y = self.network.ball_position['x'] + playfield.margin_x, self.network.ball_position['y'] + playfield.margin_y
            # if x != ball.rect.x: 
            #     ball.rect.x += (x - ball.rect.x) / itr
            # if y != ball.rect.y: 
            #     ball.rect.y += (y - ball.rect.y) / itr
            
            # if prev_x == x and prev_y == y:
            #     count += 1
            # else:
            #     prev_x, prev_y = x, y
            #     itr = (itr + count) / 2
            #     count = 1

            server_status = self.network.client.connection.status - 1
            if server_status < 3: 
                server_status_text = font.render('Server ' + ['Disconnected', 'Connecting', 'Connected'][server_status], True, WHITE)
                self.screen.blit(server_status_text, (7*SCREEN_WIDTH / 9, 9*SCREEN_HEIGHT / 10 - 50))
                latency_text = font.render('Latency: ' + str(round(1000* self.network.client.connection.latency)) + ' ms', True, WHITE)
                self.screen.blit(latency_text, (7*SCREEN_WIDTH / 9, 9*SCREEN_HEIGHT / 10))
            
            if self.message_on:
                message_font = pygame.font.Font('font.ttf', 60) 
                message_surface = message_font.render(self.message,True,WHITE)
                self.screen.blit(message_surface,(playfield.margin_x+200,playfield.margin_y+300))
            
            if not self.message_on: space.step(1/60)
            # ball.rect.x, ball.rect.y = pymunk.pygame_util.to_pygame((ball.body.position.x-123/2, ball.body.position.y-119/2), ball.image)
            ball.blitRotate(self.screen)
            playfield.draw(self.screen)
            all_sprites_list.draw(self.screen) 
            mypaddle.blitRotate(self.screen)
            for paddle in paddles.sprites(): paddle.blitRotate(self.screen)
            pygame.display.flip()
            clock.tick(60)

    # def get_new_velocity(self, ball_vel, line):
    #     d = np.array(list(ball_vel.values()))
    #     n = np.array([-(line.c1[1] - line.c2[1]), line.c1[0] - line.c2[0]])
    #     n_hat = n / np.linalg.norm(n)
    #     r = d - (2 * np.dot(d, n_hat)) * n_hat

    #     return {"x": r[0], "y": r[1]}
    
    def stop_message(self, velocity):
        self.ball.body.velocity = Vec2d(velocity['x'], velocity['y'])
        self.message_on = False

def limit_velocity(body, gravity, damping, dt):
    max_velocity = 1000
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    l = body.velocity.length
    if l > max_velocity:
        scale = max_velocity / l
        body.velocity = body.velocity * scale

def get_dict(v):
    return {'x': v[0], 'y': v[1]}

def paddle_collision(arbiter, space, data):
    dispatch_network_event('paddle', space)
    
def line_collision(arbiter, space, data):
    dispatch_network_event('line', space)

def dispatch_network_event(object, space):
    space_copy = space.copy()
    space_copy.step(network.client.connection.latency/2)
    network.client.dispatch_event("ballCollision", object, network.connection_num, get_dict(space_copy.bodies[0].velocity), get_dict(space_copy.bodies[0].position - playfield_margin))