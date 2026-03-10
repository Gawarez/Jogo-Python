import pygame
from entities.player import Player
from entities.enemy import Enemy
from entities.background import Background


class EntityFactory:

    @staticmethod
    def get_entity(entity_type: str):

        if entity_type == "player":

            surface = pygame.Surface((40, 40))
            surface.fill((0, 255, 0))
            rect = surface.get_rect(center=(200, 200))

            return Player("Player", surface, rect)

        elif entity_type == "enemy":

            surface = pygame.Surface((40, 40))
            surface.fill((255, 0, 0))
            rect = surface.get_rect(center=(400, 200))

            return Enemy("Enemy", surface, rect)

        elif entity_type == "background":

            surface = pygame.Surface((800, 600))
            surface.fill((30, 30, 30))
            rect = surface.get_rect(topleft=(0, 0))

            return Background("Background", surface, rect)

        return None