import pygame
from pygase import Client, gamestate
import threading

class Network:
    def get_connection_num(self, num):
        self.connection_num = num
        print("Got Connection Number", num)

    def get_data(self):
        clock = pygame.time.Clock()  
        while self.running:
            try:
                self.paddle_position = self.client.try_to(lambda game_state: game_state.paddle_position)
                self.ball_position = self.client.try_to(lambda game_state: game_state.ball_position)
                self.ball_velocity = self.client.try_to(lambda game_state: game_state.ball_velocity)
                self.player_match_status = self.client.try_to(lambda game_state: game_state.player_match_status)
            except:
                print('fetch failed!')
            clock.tick(60)


    def start_game(self, player_match_stat, paddle_p, ball_p):
        print('gameStarted')
        self.player_match_status = player_match_stat
        self.paddle_position = paddle_p
        self.ball_position = ball_p
        self.player_num = self.player_match_status[:self.connection_num+1].count(3) - 1
        print('menu off')
        self.menu_on = False

    def stop(self):
        self.running = False
        self.pygase_thread.join()
        self.client.disconnect()
    
    def __init__(self) -> None:
        self.connection_num = 0
        self.player_num = -1
        self.player_match_status, self.paddle_position, self.ball_position, self.ball_velocity = [], 0, {"x":0,"y":0}, {"x":0,"y":0}
        self.menu_on = True
        self.client = Client()
        self.client.connect_in_thread(port=8080, hostname='pong.samarpitminz.com')
        self.client.register_event_handler("sendPlayerNum", self.get_connection_num)
        self.client.register_event_handler("gameStarted", self.start_game)
        self.client.dispatch_event("register")
        self.running = True
        self.pygase_thread = threading.Thread(target=self.get_data)
        self.pygase_thread.start()
        print("network started")



