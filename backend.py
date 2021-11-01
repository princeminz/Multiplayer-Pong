from pygase import GameState, Backend
from datetime import datetime
from math import sin,cos,pi,asin,acos
from random import uniform
from datetime import datetime


try:
  
  initial_game_state = GameState(ball_position={"x": 400, "y": 400}, ball_velocity={"x": 0, "y": 0}, paddle_position=[(0,0)]*6, active_players=[],ready_players=[],game_on=False,player_lives=[])
  
  
  player_id = {}
  
  SCREEN_WIDTH = 800
  SCREEN_HEIGHT = 800
  
  last_collision = None
  
  start_time = None
  last_time_update = None
  
  ball_velocity_magnitude = 0.8
  num_players = 0
  last = 0
  def time_step(game_state, dt):
    global ball_velocity_magnitude,last_time_update,last
    game_time = datetime.now().timestamp()
    last = game_time
    
    if game_state.game_on == True and game_time - start_time > 7:
      #print(game_state.ball_position,dt)
      if game_time-last_time_update>2*60:
        last_time_update = game_time
        ball_velocity_magnitude += 0.1
        print("speed changed")
      x = game_state.ball_position['x'] + game_state.ball_velocity['x'] * dt*ball_velocity_magnitude
      y = 0
      if num_players == 2:
        if game_state.ball_position['y'] >= SCREEN_HEIGHT:
          y = SCREEN_HEIGHT - game_state.ball_velocity['y'] * dt*ball_velocity_magnitude
          return {"ball_position": {'x': x, 'y': y}, "ball_velocity": {"x": game_state.ball_velocity['x'], "y": -game_state.ball_velocity['y']}, "paddle_position": game_state.paddle_position}
        elif game_state.ball_position['y'] <= 0:
          y = -game_state.ball_velocity['y'] * dt*ball_velocity_magnitude
          return {"ball_position": {'x': x, 'y': y}, "ball_velocity": {"x": game_state.ball_velocity['x'], "y": -game_state.ball_velocity['y']}, "paddle_position": game_state.paddle_position}
        else:
          y = game_state.ball_position['y'] + game_state.ball_velocity['y'] * dt*ball_velocity_magnitude
      else:
        y = game_state.ball_position['y'] + game_state.ball_velocity['y'] * dt*ball_velocity_magnitude
      return {"ball_position": {'x': x, 'y': y}, "ball_velocity": game_state.ball_velocity, "paddle_position": game_state.paddle_position,"player_lives":game_state.player_lives}
    return {"ready_players": game_state.ready_players}
  
  def register_player(client_address, game_state, **kwargs):
    connection_num = list(backend.server.connections.keys()).index(client_address)
    print("Player Registered", connection_num, client_address)
    backend.server.dispatch_event("sendPlayerNum", connection_num, target_client = client_address)
    active_players = [ i.status == 3 for i in backend.server.connections.values()]
    ready_players = game_state.ready_players
    ready_players.append(False)
    player_lives = game_state.player_lives
    player_lives.append(3)
    print(game_state.ready_players)
    return {"active_players": active_players, "ready_players": ready_players,"player_lives":player_lives}
  
  def on_paddle_move(position, client_address, game_state, **kwargs):
    paddle_position = game_state.paddle_position
    connection_num = list(backend.server.connections.keys()).index(client_address)
    paddle_position[connection_num] = position
    return {"paddle_position": paddle_position}
    
  def on_player_ready(connection_num,game_state,**kwargs):
    ready_players = game_state.ready_players
    if sum(game_state.ready_players)<=5:
      ready_players[connection_num] = True
      
    print(ready_players) 
    return {"ready_players": ready_players}
    
  def on_game_start(game_state,**kwargs):
    global start_time, num_players,last_time_update
    start_time = datetime.now().timestamp()
    last_time_update = start_time
    if game_state.game_on == True:
      print('game already on')
      return {}
    game_on = True
    ips = list(backend.server.connections.keys())
    l = list(backend.server.connections.values())
    ready_players = [ game_state.ready_players[i] and l[i].status == 3 for i in range(len(ips)) ]
    print(ready_players)
    num_players = sum(ready_players)
    paddle_position = [(0,0)]*(len(ready_players))
    for i in range(len(ready_players)):
      if(ready_players[i]):
        print(ips[i])
        backend.server.dispatch_event("gameStarted", ready_players, paddle_position, game_state.ball_position, target_client=ips[i])
    print('sent gameStarted')
    in_angle = uniform(0, 2*pi)
    ball_vel = {"x": cos(in_angle),"y": sin(in_angle)}
    ball_pos = {"x": SCREEN_WIDTH/2, "y": SCREEN_HEIGHT/2}
    return {"ready_players": ready_players, "game_on": game_on,"paddle_position":paddle_position,"ball_velocity":ball_vel,"ball_position":ball_pos}
    
  def on_collision(collided_with,connection_num,ball_vel, ball_pos,client_address,game_state, **kwargs):
    # print("initial",ball_pos,ball_vel)
    global last_collision
    if(last_collision==client_address):
      return {}
    last_collision = client_address
    # print("after",ball_pos,ball_vel)
    if collided_with=="line":
      return {"ball_velocity": ball_vel,"ball_position": ball_pos,"player_lives":decrease_life(connection_num,client_address,game_state.player_lives)}
    else: 
      return {"ball_velocity": ball_vel,"ball_position": ball_pos}


  def decrease_life(connection_num,client_address,player_lives):
    player_lives[connection_num] -= 1
    if player_lives[connection_num]==0:
      pass
    print(player_lives)

    return player_lives
  
  
  backend = Backend(initial_game_state, time_step, event_handlers={'register': register_player, 'paddleMove': on_paddle_move, 'playerReady':on_player_ready, 'gameStart': on_game_start, 'ballCollision': on_collision})
  backend.run('172.31.7.17', 8080)
except:
  backend.shutdown()
  print("\nBackend closed\n")
