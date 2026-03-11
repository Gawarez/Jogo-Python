import pygame
from settings import *


class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, numero):
        super().__init__()

        self.numero = numero
        self.state = "idle"  # idle, attack, death
        self.frame_atual = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.velocidade_animacao = 150
        self.direcao = 1
        self.velocidade = VELOCIDADE_JOGADOR
        self.atacando = False

        self.animacoes = {"idle": [], "attack": [], "death": []}
        self.carregar_animacoes()

        # Imagem inicial
        if self.animacoes["idle"]:
            self.image = self.animacoes["idle"][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - self.rect.height

    def carregar_animacoes(self):
        try:
            prefixo = f"player{self.numero}"

            # CAMINHOS CORRIGIDOS - com assets/images/
            idle = pygame.image.load(f"assets/images/{prefixo}_idle.png").convert_alpha()
            attack = pygame.image.load(f"assets/images/{prefixo}_attack.png").convert_alpha()
            death = pygame.image.load(f"assets/images/{prefixo}_death.png").convert_alpha()

            self.animacoes["idle"] = self.extrair_frames(idle, 4)
            self.animacoes["attack"] = self.extrair_frames(attack, 4)
            self.animacoes["death"] = self.extrair_frames(death, 4)

            print(f"✅ Player {self.numero} carregado")

        except Exception as e:
            print(f"❌ Player {self.numero}: {e}")
            # Fallback colorido
            cor = VERDE if self.numero == 1 else AZUL
            surf = pygame.Surface((50, 80))
            surf.fill(cor)
            self.animacoes["idle"] = [surf] * 4
            self.animacoes["attack"] = [surf] * 4
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
        agora = pygame.time.get_ticks()

        if agora - self.ultimo_update > self.velocidade_animacao:
            self.ultimo_update = agora
            self.frame_atual += 1

            frames = self.animacoes[self.state]

            if self.frame_atual >= len(frames):
                if self.state == "attack":
                    self.state = "idle"
                    self.atacando = False
                elif self.state == "death":
                    return False
                self.frame_atual = 0

            self.image = frames[self.frame_atual]

            if self.direcao == -1:
                self.image = pygame.transform.flip(self.image, True, False)

        return True

    def mover_esquerda(self):
        if self.state != "death":
            self.rect.x -= self.velocidade
            self.direcao = -1
            if self.rect.x < 0:
                self.rect.x = 0

    def mover_direita(self):
        if self.state != "death":
            self.rect.x += self.velocidade
            self.direcao = 1
            if self.rect.x > LARGURA - self.rect.width:
                self.rect.x = LARGURA - self.rect.width

    def atacar(self):
        if self.state == "idle":
            self.state = "attack"
            self.atacando = True
            self.frame_atual = 0

    def morrer(self):
        if self.state != "death":
            self.state = "death"
            self.frame_atual = 0