import pygame
from settings import *


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.state = "idle"
        self.frame_atual = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.velocidade_animacao = 150
        self.velocidade = VELOCIDADE_INIMIGO

        self.animacoes = {"idle": [], "death": []}
        self.carregar_animacoes()

        if self.animacoes["idle"]:
            self.image = self.animacoes["idle"][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - self.rect.height

    def carregar_animacoes(self):
        try:
            # CAMINHOS CORRIGIDOS
            idle = pygame.image.load("assets/images/enemy_idle.png").convert_alpha()
            death = pygame.image.load("assets/images/enemy_death.png").convert_alpha()

            self.animacoes["idle"] = self.extrair_frames(idle, 4)
            self.animacoes["death"] = self.extrair_frames(death, 4)

            print("✅ Inimigo carregado")

        except Exception as e:
            print(f"❌ Inimigo: {e}")
            surf = pygame.Surface((40, 60))
            surf.fill(VERMELHO)
            self.animacoes["idle"] = [surf] * 4
            self.animacoes["death"] = [surf] * 4

    def extrair_frames(self, sheet, num_frames):
        frames = []
        largura = sheet.get_width() // num_frames
        altura = sheet.get_height()

        for i in range(num_frames):
            frame = sheet.subsurface((i * largura, 0, largura, altura))
            frame = pygame.transform.scale(frame, (largura, altura))
            frames.append(frame)
        return frames

    def update(self):
        if self.state == "idle":
            self.rect.x -= self.velocidade

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.velocidade_animacao:
            self.ultimo_update = agora
            self.frame_atual += 1

            frames = self.animacoes[self.state]

            if self.frame_atual >= len(frames):
                if self.state == "death":
                    return False
                self.frame_atual = 0

            self.image = frames[self.frame_atual]

        return True

    def morrer(self):
        if self.state != "death":
            self.state = "death"
            self.frame_atual = 0
            return True
        return False