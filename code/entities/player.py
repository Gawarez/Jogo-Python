import pygame
from entities.entity import Entity


class Player(Entity):

    def move(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5

        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if keys[pygame.K_UP]:
            self.rect.y -= 5

        if keys[pygame.K_DOWN]:
            self.rect.y += 5