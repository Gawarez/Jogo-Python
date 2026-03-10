from entities.entity import Entity


class Enemy(Entity):

    def move(self):
        self.rect.x += 2