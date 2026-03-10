import pygame
from game.game import Game


class Menu:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

    def run(self):
        game = Game()
        game.run()