import math
from pygase import GameState, Backend
from datetime import datetime


initial_game_state = GameState(ball_position={"x": 20, "y": 50}, ball_velocity={"x": 0.3, "y": 0.3}, paddle_position=[(0,0)]*6, active_players=[],ready_players=[],game_on=False)


player_id = {}

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600




last = datetime.now()

def time_step(game_state, dt):
  # global last
  # now = datetime.now()
  # print(now-last)
  # last = now
  
  # active_players = [ i.status == 3 for i in backend.server.connections.values()]
  if game_state.game_on == True:
    if game_state.ball_position['x'] >= SCREEN_WIDTH-10:
      # scoreA+=1
      game_state.ball_velocity['x'] = -game_state.ball_velocity['x']
  
    if game_state.ball_position['x'] <= 0:
      # scoreB+=1
      game_state.ball_velocity['x'] = -game_state.ball_velocity['x']
  
    if game_state.ball_position['y'] > SCREEN_HEIGHT-10:
      game_state.ball_velocity['y'] = -game_state.ball_velocity['y']
        
    if game_state.ball_position['y'] < 0:
      game_state.ball_velocity['y'] = -game_state.ball_velocity['y']     
  
    x = game_state.ball_position['x'] + game_state.ball_velocity['x'] * dt
    y = game_state.ball_position['y'] + game_state.ball_velocity['y'] * dt
    
    ready_players = game_state.ready_players
    ips = list(backend.server.connections.keys())
    for i in range(len(ready_players)):
      if(ready_players[i]):
        backend.server.dispatch_event("sendBallPosition", {"x":x,"y":y}, target_client=ips[i])
    
    # return {"ball_position": {'x': x, 'y': y}, "active_players": active_players}
    return {"ball_position": {'x': x, 'y': y}}
  else:
    return {}

def register_player(client_address, game_state, **kwargs):
  connection_num = list(backend.server.connections.keys()).index(client_address)
  print("Player Registered", connection_num, client_address)
  backend.server.dispatch_event("sendPlayerNum", connection_num, target_client = client_address)
  active_players = [ i.status == 3 for i in backend.server.connections.values()]
  ready_players = game_state.ready_players
  ready_players.append(False)
  print(game_state.ready_players)
  return {"active_players": active_players,"ready_players": ready_players}

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
  if game_state.game_on == True:
    print('game already on')
    return {}
  game_on = True
  ips = list(backend.server.connections.keys())
  l = list(backend.server.connections.values())
  ready_players = [ game_state.ready_players[i] and l[i].status == 3 for i in range(len(ips)) ]
  print(ready_players)
  paddle_position = [(0,0)]*(len(ready_players))
  for i in range(len(ready_players)):
    if(ready_players[i]):
      print(ips[i])
      backend.server.dispatch_event("gameStarted", ready_players, paddle_position, game_state.ball_position, target_client=ips[i])
  print('sent gameStarted')
  
  return {"ready_players": ready_players, "game_on": game_on,"paddle_position":paddle_position}
  

backend = Backend(initial_game_state, time_step, event_handlers={'register': register_player,'paddleMove': on_paddle_move,'playerReady':on_player_ready,'gameStart':on_game_start})
backend.run('172.31.13.86', 8080)