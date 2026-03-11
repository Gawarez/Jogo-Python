import pygame
from settings import *


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, cor_texto=PRETO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_texto = cor_texto
        self.fonte = pygame.font.Font(None, 36)
        self.clicado = False

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=10)
        pygame.draw.rect(tela, PRETO, self.rect, 3, border_radius=10)
        texto_surf = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)

    def foi_clicado(self, pos):
        return self.rect.collidepoint(pos)