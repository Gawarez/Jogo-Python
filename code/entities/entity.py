class Entity:

    def __init__(self, name, surface, rect):

        self.name = name
        self.surface = surface
        self.rect = rect

    def move(self):
        pass

    def draw(self, window):
        window.blit(self.surface, self.rect)