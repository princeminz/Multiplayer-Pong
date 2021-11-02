import pygame
BLACK = (0,0,0)
WHITE = (255,255,255)
from pygame.locals import (
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  QUIT,
)

class Menu:
    def __init__(self, screen, network) -> None:
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        font = pygame.font.Font('font.ttf', 35) 
        font_big = pygame.font.Font('font.ttf', 64) 
        font_title = pygame.font.Font('font.ttf', 128) 
        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        title_text = font_title.render('Multiplayer Pong', True, WHITE)
        ready_text = font_big.render('READY', True, WHITE)
        start_text = font_big.render('START', True, WHITE)
        quit_text = font_big.render('QUIT', True, WHITE)
        print('in menu')

        # button_color = (170,170,170) 
        title_x = SCREEN_WIDTH/8
        title_y = SCREEN_HEIGHT/8
        button_x = 3*SCREEN_WIDTH/5
        button_width = SCREEN_WIDTH/5
        button_height = SCREEN_HEIGHT/8
        ready_y = SCREEN_HEIGHT/3
        start_y = ready_y + button_height + 20
        quit_y = start_y + button_height + 20
        clock = pygame.time.Clock()  
        while network.menu_on:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        network.menu_on = False
                        network.stop()
                        pygame.quit()
                    if event.type == QUIT:
                        network.menu_on = False
                        network.stop()
                        pygame.quit()
                
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if button_x <= mouse[0] <= button_x + button_width:
                        if ready_y <= mouse[1] <= ready_y + button_height: 
                            print('ready')
                            network.client.dispatch_event("playerReady", network.connection_num)
                        
                        if start_y <= mouse[1] <= start_y + button_height: 
                            print('start')
                            if network.player_match_status.count(2) > 1:
                                network.client.dispatch_event("gameStart")

                        if quit_y <= mouse[1] <= quit_y + button_height: 
                            print('quit')
                            network.menu_on = False
                            network.stop()
                            pygame.quit() 

            screen.blit(background, (0, 0))
            # pygame.draw.rect(screen, button_color, [button_x, ready_y, button_width, button_height])
            # pygame.draw.rect(screen, button_color, [button_x, start_y, button_width, button_height])
            # pygame.draw.rect(screen, button_color, [button_x, quit_y, button_width, button_height])
            screen.blit(title_text, (title_x, title_y))
            screen.blit(ready_text, (button_x, ready_y))
            screen.blit(start_text, (button_x, start_y))
            screen.blit(quit_text, (button_x, quit_y))
            server_status = network.client.connection.status - 1
            if server_status < 3: 
                server_status_text = font.render('Server ' + ['Disconnected', 'Connecting', 'Connected'][server_status], True, WHITE)
                screen.blit(server_status_text, (7*SCREEN_WIDTH / 9, 9*SCREEN_HEIGHT / 10 - 50))
                latency_text = font.render('Latency: ' + str(round(1000* network.client.connection.latency)) + ' ms', True, WHITE)
                screen.blit(latency_text, (7*SCREEN_WIDTH / 9, 9*SCREEN_HEIGHT / 10))

            player_text_x = SCREEN_WIDTH / 5
            player_text_y = ready_y
            player_text_height = SCREEN_HEIGHT / 20
            # player_text_width = SCREEN_WIDTH / 5
            for i, player in enumerate(network.player_match_status):
                if(player in [1, 2]):
                    player_text = font.render('Player ' + str(i) + [': Disconnected', ': Connected', ': Ready'][player], True, WHITE)
                    # pygame.draw.rect(screen, WHITE, [player_text_x, player_text_y, player_text_width, player_text_height])
                    screen.blit(player_text, (player_text_x, player_text_y))
                    player_text_y += (player_text_height + 10)

            pygame.display.flip()
            clock.tick(60)