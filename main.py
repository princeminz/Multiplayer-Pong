import pygame
from network import Network
from menu import Menu
from game import Game
  
if __name__ == "__main__":
  pygame.init()
  screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  network = Network()
  Menu(screen, network)
  Game(screen, network)
  network.pygase_thread.join()