import pygame
from player import Paddle
from ball import Ball
from pygase import Client
from playfield import PlayField
import threading
import time


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
connection_num = 0
player_num = -1
ready_players, paddle_position, ball_position = [], 0, {"x":0,"y":0}
menu_on = True

paddle_width = 25
paddle_height = 75


def get_connection_num(num):
  global connection_num
  connection_num = num
  print("Got Connection Number", num)

def get_data():
  global ready_players, paddle_position, ball_position
  while 1:
    paddle_position = client.try_to(lambda game_state: game_state.paddle_position, timeout=10.0)
    # ball_position = client.try_to(lambda game_state: game_state.ball_position, timeout=10.0)
    # ready_players = client.try_to(lambda game_state: game_state.ready_players, timeout=10.0)
    # print(ball_position)


def start_game(ready_p, paddle_p, ball_p):
  print('gameStarted')
  global menu_on, player_num, ready_players, paddle_position
  ready_players = ready_p
  paddle_position = paddle_p
  ball_position = ball_p
  player_num = sum(ready_players[:connection_num+1]) - 1
  print('menu off')
  menu_on = False

def get_ball_position(ball_pos):
  global ball_position 
  ball_position = ball_pos 

  
if __name__ == "__main__":
  client = Client()
  client.connect_in_thread(port=8080, hostname='15.207.54.25')
  client.register_event_handler("sendPlayerNum", get_connection_num)
  client.register_event_handler("gameStarted", start_game)
  client.register_event_handler("sendBallPosition", get_ball_position)
  client.dispatch_event("register")
  pygase_thread = threading.Thread(target=get_data)
  pygase_thread.start()
  pygame.init()
  screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
  
  font = pygame.font.SysFont(name='systemfont', size=35) 
  ready_text = font.render('READY', True, WHITE)
  start_text = font.render('START', True, WHITE)
  quit_text = font.render('QUIT', True, WHITE)

  button_color = (170,170,170) 
  button_x = 7*SCREEN_WIDTH/16
  button_width = SCREEN_WIDTH/8
  button_height = SCREEN_HEIGHT/8
  ready_y = SCREEN_HEIGHT/4
  start_y = ready_y + button_height + 20
  quit_y = start_y + button_height + 20

  while menu_on:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
      if event.type == QUIT:
        pygame.quit()
      
      mouse = pygame.mouse.get_pos()
      if event.type == pygame.MOUSEBUTTONDOWN: 
        if button_x <= mouse[0] <= button_x + button_width:
          if ready_y <= mouse[1] <= ready_y + button_height: 
            print('ready')
            client.dispatch_event("playerReady",connection_num)
            
          if start_y <= mouse[1] <= start_y + button_height: 
            print('start')
            client.dispatch_event("gameStart")
          if quit_y <= mouse[1] <= quit_y + button_height: 
            print('quit')
            pygame.quit() 
            exit()
    
    screen.fill((60,25,60)) 
    pygame.draw.rect(screen, button_color, [button_x, ready_y, button_width, button_height])
    pygame.draw.rect(screen, button_color, [button_x, start_y, button_width, button_height])
    pygame.draw.rect(screen, button_color, [button_x, quit_y, button_width, button_height])
    
    screen.blit(ready_text, (button_x, ready_y))
    screen.blit(start_text, (button_x, start_y))
    screen.blit(quit_text, (button_x, quit_y))
    
    pygame.display.flip()
  

  running = True
  playfield = PlayField(color=WHITE, num_players=sum(ready_players))
  if(sum(ready_players)==2 and player_num==1):
    myboundary = playfield.sprites()[2]
  else:
    myboundary = playfield.sprites()[player_num]
  mypaddle = Paddle((255, 255, 255), paddle_width,paddle_height, myboundary)
  client.dispatch_event('paddleMove', position = (mypaddle.rect.x-playfield.margin_x, mypaddle.rect.y-playfield.margin_y))
  all_sprites_list = pygame.sprite.Group()
  ball = Ball((255, 255, 255), 10, 10)
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
    for i in range(len(ready_players)):
      if(ready_players[i] and i != connection_num):
        x, y = paddle_position[i]
        if sum(ready_players)==2 and sum(ready_players[:i+1]) ==2:
          paddle = Paddle((255, 255, 255), 25, 75, playfield.sprites()[2])   
        else:
          paddle = Paddle((255, 255, 255), 25, 75, playfield.sprites()[sum(ready_players[:i+1]) - 1])
        paddle.rect.x = x + playfield.margin_x
        paddle.rect.y = y + playfield.margin_y
        paddles.add(paddle)
        paddle_sprite[i] = paddle

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      mypaddle.moveUp(3)
      client.dispatch_event('paddleMove', position = (mypaddle.rect.x-playfield.margin_x, mypaddle.rect.y-playfield.margin_y))
    if keys[pygame.K_DOWN]:
      mypaddle.moveDown(3)
      client.dispatch_event('paddleMove', position = (mypaddle.rect.x-playfield.margin_x, mypaddle.rect.y-playfield.margin_y))
    screen.fill(BLACK)

    x, y = ball_position['x'], ball_position['y']
    if x != ball.rect.x: 
      ball.rect.x += (x - ball.rect.x) / itr
    if y != ball.rect.y: 
      ball.rect.y += (y - ball.rect.y) / itr
    
    if prev_x == x and prev_y == y:
      count += 1
    else:
      itr = (itr + count) / 2
      count = 1
  
    # Collision 
    for i, sprite in enumerate(playfield.sprites()):
      if pygame.sprite.collide_mask(ball,sprite): 
        print("Collided with", i)

    playfield.draw(screen)
    all_sprites_list.draw(screen) 
    paddles.draw(screen) 
    pygame.display.flip()
    clock.tick(60)
    print("itr: ", itr, "(x - ball.rect.x)", (x - ball.rect.x), "(y - ball.rect.y)", y - ball.rect.y)

pygame.quit()