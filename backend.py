from pygase import GameState, Backend
from datetime import datetime
from math import sin,cos,pi,asin,acos,sqrt
from random import uniform,choice
from datetime import datetime
#disconnected = 0
#Connected = 1
#ready = 2
#active = 3
#lost = 4

try:
  
  initial_game_state = GameState(ball_position={"x": 400, "y": 400}, ball_velocity={"x": 0, "y": 0}, paddle_position={}, game_on=False, player_lives={}, player_match_status={})
  player_id = {}
  SCREEN_WIDTH = 1000
  SCREEN_HEIGHT = 1000
  ball_width = 25
  last_collision = None

  start_time = None
  last_time_update = None
  
  initial_ball_velocity = 300
  ball_velocity_magnitude = 300
  num_players = 0
  last = 0
  velocity_magnitude = 300

  just_started = False

  def time_step(game_state, dt):
    global ball_velocity_magnitude,last_time_update,last,just_started
    game_time = datetime.now().timestamp()
    # dt = game_time-last
    # last = game_time
    # print(dt*1000)
    ips = list(backend.server.connections.keys())
    if game_state.game_on == True and game_time - start_time > 5:
      if just_started==False:
        for c_num, status in game_state.player_match_status.items():
          if status in [3,4]:
            backend.server.dispatch_event("stopMessage", game_state.ball_velocity, target_client=ips[c_num])   
        just_started = True
        last_time_update = game_time
      #print(game_state.ball_position,dt)
      # if game_time-last_time_update>2*10:
      #   last_time_update = game_time
      #   factor_increase = 2
      #   print("speed changed")
      #   for c_num, status in game_state.player_match_status.items():
      #     if status in [3,4]:
      #       backend.server.dispatch_event("increaseSpeed", factor_increase, target_client=ips[c_num])
     
      return {"ball_position": game_state.ball_position, "ball_velocity": game_state.ball_velocity, "paddle_position": game_state.paddle_position,"player_lives": game_state.player_lives, "player_match_status": game_state.player_match_status,"game_on":game_state.game_on}
    elif game_state.game_on == False:

      ball_velocity_magnitude = initial_ball_velocity
      player_match_status = game_state.player_match_status
      connections = list(backend.server.connections.values())
      player_match_status = { i:(0 if connections[i].status in [1, 2] else v) for i, v in player_match_status.items() }
      just_started = False
      # return {"player_match_status": player_match_status}
      return {"player_match_status": player_match_status, "paddle_position": game_state.paddle_position,"ball_velocity": game_state.ball_velocity,"paddle_position": game_state.paddle_position,"ball_position":game_state.ball_position,"game_on":game_state.game_on}
    else:
      just_started = False
      return {"player_match_status": game_state.player_match_status, "paddle_position": game_state.paddle_position,"ball_velocity": game_state.ball_velocity,"paddle_position": game_state.paddle_position,"ball_position":game_state.ball_position,"game_on":game_state.game_on}

    
  
  def register_player(client_address, game_state, **kwargs):
    connection_num = list(backend.server.connections.keys()).index(client_address)
    print("Player Registered", connection_num, client_address)
    backend.server.dispatch_event("sendPlayerNum", connection_num, target_client = client_address)
    player_match_status = game_state.player_match_status
    paddle_position = game_state.paddle_position
    player_match_status[connection_num] = 1
    paddle_position[connection_num] = (0, 0)
    print(player_match_status)
    return {"player_match_status": player_match_status, "paddle_position": paddle_position,"ball_velocity": game_state.ball_velocity,"paddle_position": game_state.paddle_position,"ball_position":game_state.ball_position,"game_on":game_state.game_on}
  
  def on_paddle_move(position, client_address, game_state, **kwargs):
    paddle_position = game_state.paddle_position
    connection_num = list(backend.server.connections.keys()).index(client_address)
    paddle_position[connection_num] = position
    return {"paddle_position": paddle_position}
    
  def on_player_ready(connection_num,game_state,**kwargs):
    player_match_status = game_state.player_match_status
    if list(player_match_status.values()).count(2) <= 3:
      player_match_status[connection_num] = 2

    return {"player_match_status": player_match_status}
    
  def on_game_start(game_state,**kwargs):
    global start_time, num_players, last_time_update, last_collision,velocity_magnitude
    last_collision = None
    start_time = datetime.now().timestamp()
    last_time_update = start_time
    if game_state.game_on == True:
      print('game already on')
      return {}
    game_on = True
    ips = list(backend.server.connections.keys())
    backend_connections = list(backend.server.connections.values())
    player_match_status = game_state.player_match_status
    player_lives = game_state.player_lives
    for c_num, status in player_match_status.items():
      if status == 2 and backend_connections[c_num].status == 3: 
        player_match_status[c_num] = 3
        player_lives[c_num] = 3
      elif backend_connections[c_num].status != 3: 
        player_match_status[c_num] = 0
    print("status",player_match_status)
    num_players = list(player_match_status.values()).count(3)
    velocity_magnitude = 300
    ball_vel, ball_pos = get_initial_ball_velandpos(velocity_magnitude)
    # for i in player_match_status.keys():
    #   if player_match_status[i] == 3:
    #     backend.server.dispatch_event("gameStarted", player_match_status, game_state.paddle_position, game_state.ball_position, target_client=ips[i])
    print('sent gameStarted')
    
    return {"game_on": game_on, "ball_velocity":ball_vel, "ball_position":ball_pos, "player_match_status":player_match_status, "player_lives": player_lives,"paddle_position":game_state.paddle_position}
    
  def on_collision(collided_with, connection_num, ball_vel, ball_pos, client_address, game_state, **kwargs):
    global last_collision, start_time, num_players,velocity_magnitude
    # if(last_collision==client_address):
    #   return {}
    # if last_collision==client_address: print("twice collision")
    last_collision = client_address
    
    ips = list(backend.server.connections.keys())
    # print("ball pos and vel:",ball_pos,ball_vel)
    for c_num, status in game_state.player_match_status.items():
      if c_num != connection_num and status in [3,4]:   
        backend.server.dispatch_event("collisionData", ball_pos, ball_vel, target_client=ips[c_num])   

    if collided_with=="line":
      player_lives = decrease_life(connection_num,client_address,game_state)
      player_match_status = game_state.player_match_status
      game_on = True
      if player_lives[connection_num]==0:     
        player_match_status[connection_num] = 4
        num_players -= 1
        velocity_magnitude *= 1.5
        ball_vel,ball_pos = get_initial_ball_velandpos(velocity_magnitude)
        start_time = datetime.now().timestamp()
        messages = {3:"Next Round",4:"You are Eliminated"}
        if num_players==1:
          messages = {3:"Winner",4:"You Lost"}
          print(messages)
        
        for c_num, status in player_match_status.items():
          if status in [3,4]:   
            backend.server.dispatch_event("reinitGameloop",messages[status], target_client=ips[c_num])  

        if num_players==1:
          game_on = False
          player_match_status = { k:int(bool(v)) for k, v in player_match_status.items() } 
      return {"ball_velocity": ball_vel,"ball_position": ball_pos,"player_lives": player_lives,"player_match_status":player_match_status,"game_on":game_on}
    else: 
      return {"ball_velocity": ball_vel,"ball_position": ball_pos}

  def decrease_life(connection_num, client_address, game_state):
    player_lives = game_state.player_lives
    player_lives[connection_num] -= 1 
    print("lives:",player_lives)

    return player_lives


  def get_initial_ball_velandpos(velocity_magnitude):
    
    x = choice([-1,1])*uniform(0.708,1)
    y = choice([-1,1])*sqrt(1-x**2)
    ball_vel = {"x": velocity_magnitude*x,"y": velocity_magnitude*y}
    ball_pos = {"x": SCREEN_WIDTH/2, "y": SCREEN_HEIGHT/2}
    return [ball_vel,ball_pos]

  backend = Backend(initial_game_state, time_step, event_handlers={'register': register_player, 'paddleMove': on_paddle_move, 'playerReady':on_player_ready, 'gameStart': on_game_start, 'ballCollision': on_collision})
  backend.run('localhost', 8080)
except:
  backend.shutdown()
  print("\nBackend closed\n")