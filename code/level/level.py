import pygame
import sys
from factory.entity_factory import EntityFactory


class Level:

    def __init__(self, window, name):

        self.window = window
        self.name = name
        self.entity_list = []

        self.entity_list.append(EntityFactory.get_entity("background"))
        self.entity_list.append(EntityFactory.get_entity("player"))
        self.entity_list.append(EntityFactory.get_entity("enemy"))

    def run(self):

        clock = pygame.time.Clock()

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for entity in self.entity_list:
                entity.move()

            for entity in self.entity_list:
                entity.draw(self.window)

            pygame.display.update()
            clock.tick(60)