import pygame
import sys
from settings import *
from game import Jogo


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Jogo 2D - Animações")
    relogio = pygame.time.Clock()

    jogo = Jogo(tela)
    rodando = True

    while rodando:
        rodando = jogo.rodar()
        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()