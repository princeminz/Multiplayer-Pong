import pygame,random
BLACK = (0,0,0)
WHITE = (255,255,255)
from pygame.locals import (
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  K_SPACE,
  QUIT,
)

class Final_Screen:
    def __init__(self, screen, network,message) -> None:
        self.message = message
        self.screen = screen
        self.network = network
        print("Entered final screen")
        clock = pygame.time.Clock() 
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        winning_sound = pygame.mixer.Sound("./sounds/Music_BG.ogg")
        losing_sound = pygame.mixer.Sound("./sounds/bgm_27.ogg")

        if self.message == "Winner":
            winning_sound.play(loops = -1)
        else:
            losing_sound.play(loops = -1)

        self.particles = []
 
        self.tile_map = {}


        while self.running:
            self.screen.blit(background, (0, 0))
            if self.message=="Winner" :
                self.fireworks()
    
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                        self.network.stop()
                        pygame.quit()
                    elif event.key==K_SPACE:
                        self.running = False
                elif event.type == QUIT:
                    self.running = False
                    self.network.stop()
                    pygame.quit()
            message_font = pygame.font.Font('font.ttf', 60) 
            message_surface = message_font.render(self.message,True,WHITE)
            self.screen.blit(message_surface,(SCREEN_WIDTH/2-100,500))
            message_surface2 = message_font.render("Press Space to return to Menu",True,(158,170,247))
            self.screen.blit(message_surface2,(500,800))
            pygame.display.flip()
            clock.tick(60)
            
        winning_sound.stop()
        print("out")

    def fireworks(self):
        TILE_SIZE = 20
        clicking, mx, my = self.mouse_simulator()
        # mx, my = pygame.mouse.get_pos()
        # Particles ---------------------------------------------- #
        if clicking:
            for i in range(10):
                self.particles.append([[mx, my], [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5], random.randint(4, 6)])
    
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            loc_str = str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE))
            if loc_str in self.tile_map:
                particle[1][0] = -0.7 * particle[1][0]
                particle[1][1] *= 0.95
                particle[0][0] += particle[1][0] * 2
            particle[0][1] += particle[1][1]
            loc_str = str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE))
            if loc_str in self.tile_map:
                particle[1][1] = -0.7 * particle[1][1]
                particle[1][0] *= 0.95
                particle[0][1] += particle[1][1] * 2
            particle[2] -= 0.035
            particle[1][1] += 0.15
            pygame.draw.circle(self.screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)
    
        # Render Tiles ------------------------------------------- #
        for tile in self.tile_map:
            pygame.draw.rect(self.screen, self.tile_map[tile][2], pygame.Rect(self.tile_map[tile][0] * TILE_SIZE, self.tile_map[tile][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))


    def mouse_simulator(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        if random.random() < .05:
            clicking = True
        else:
            clicking = False
        mx = random.randrange(0,SCREEN_WIDTH-50 )
        my = random.randrange(0, SCREEN_HEIGHT-50)
        return clicking, mx, my
