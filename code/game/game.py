import pygame
from level.level import Level


class Game:

    def __init__(self):
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Mountain Shooter")

        self.levels = []
        self.levels.append(Level(self.window, "Level 1"))

    def run(self):

        for level in self.levels:
            level.run()



            print('setup started')
            pygame.init()
            window = pygame.display.set_mode((800, 600))
            print('setup ended')

            print('loop started')
            while True:
                # check for all events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # close window
                        quit()  # end pygame