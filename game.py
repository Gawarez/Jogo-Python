import pygame
import random
from settings import *
from player import Jogador
from enemy import Inimigo
from button import Botao


class Jogo:
    def __init__(self, tela):
        self.tela = tela
        self.estado = "MENU"
        self.player_escolhido = 1

        self.todos_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.jogador = None

        self.pontuacao = 0
        self.tempo_spawn = 0
        self.tempo_entre_spawns = 90

        # Carregar fundos com caminhos corrigidos
        self.carregar_fundos()

        # Botões
        self.botoes = [
            Botao(300, 200, 200, 50, "Player 1", VERDE),
            Botao(300, 270, 200, 50, "Player 2", AZUL),
            Botao(300, 340, 200, 50, "Iniciar Jogo", AMARELO)
        ]
        self.botao_clicado = [False, False, False]

    def carregar_fundos(self):
        try:
            self.fundo_menu = pygame.image.load("assets/images/menu_bg.png").convert()
            self.fundo_menu = pygame.transform.scale(self.fundo_menu, (LARGURA, ALTURA))
            print("✅ menu_bg.png carregado")
        except:
            self.fundo_menu = pygame.Surface((LARGURA, ALTURA))
            self.fundo_menu.fill((30, 30, 60))
            print("❌ menu_bg.png não encontrado")

        try:
            self.fundo_jogo = pygame.image.load("assets/images/background.png").convert()
            self.fundo_jogo = pygame.transform.scale(self.fundo_jogo, (LARGURA, ALTURA))
            print("✅ background.png carregado")
        except:
            self.fundo_jogo = pygame.Surface((LARGURA, ALTURA))
            self.fundo_jogo.fill((100, 150, 200))
            print("❌ background.png não encontrado")

    def processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.estado == "JOGO":
                        self.estado = "MENU"
                    else:
                        return False

                if event.key == pygame.K_r and self.estado == "GAME_OVER":
                    self.estado = "MENU"

                # Teclas de teste
                if event.key == pygame.K_m and self.jogador:
                    self.jogador.morrer()

                if event.key == pygame.K_n and self.inimigos:
                    for inimigo in self.inimigos:
                        inimigo.morrer()

        return True

    def atualizar_menu(self):
        self.tela.blit(self.fundo_menu, (0, 0))

        fonte = pygame.font.Font(None, 48)
        titulo = fonte.render("JOGO 2D", True, BRANCO)
        titulo_rect = titulo.get_rect(center=(LARGURA // 2, 100))
        self.tela.blit(titulo, titulo_rect)

        for botao in self.botoes:
            botao.desenhar(self.tela)

        fonte_media = pygame.font.Font(None, 36)
        texto_sel = fonte_media.render(f"Selecionado: Player {self.player_escolhido}", True, BRANCO)
        self.tela.blit(texto_sel, (280, 420))

        # Controles
        fonte_peq = pygame.font.Font(None, 24)
        y = 470
        controles = [
            "CONTROLES:",
            "A/D ou ←/→: Mover",
            "ESPAÇO: Atacar",
            "M: Matar jogador (teste)",
            "N: Matar inimigo (teste)",
            "R: Reiniciar",
            "ESC: Menu/Sair"
        ]
        for texto in controles:
            cor = AMARELO if texto == "CONTROLES:" else BRANCO
            surf = fonte_peq.render(texto, True, cor)
            self.tela.blit(surf, (200, y))
            y += 20

        # Cliques
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            if self.botoes[0].foi_clicado(pos) and not self.botao_clicado[0]:
                self.player_escolhido = 1
                self.botao_clicado[0] = True

            if self.botoes[1].foi_clicado(pos) and not self.botao_clicado[1]:
                self.player_escolhido = 2
                self.botao_clicado[1] = True

            if self.botoes[2].foi_clicado(pos) and not self.botao_clicado[2]:
                self.iniciar_jogo()
                self.botao_clicado[2] = True
        else:
            self.botao_clicado = [False, False, False]

    def iniciar_jogo(self):
        self.estado = "JOGO"
        self.todos_sprites.empty()
        self.inimigos.empty()

        self.jogador = Jogador(100, ALTURA - 150, self.player_escolhido)
        self.todos_sprites.add(self.jogador)

        self.pontuacao = 0
        self.tempo_spawn = 0

    def spawnar_inimigo(self):
        if len(self.inimigos) == 0:
            y = ALTURA - 150
            inimigo = Inimigo(LARGURA, y)
            self.inimigos.add(inimigo)
            self.todos_sprites.add(inimigo)

    def atualizar_jogo(self):
        if not self.jogador:
            return

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.jogador.mover_esquerda()
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.jogador.mover_direita()
        if teclas[pygame.K_SPACE]:
            self.jogador.atacar()
            self.pontuacao += 1  # Aumenta pontuação ao atacar

        for sprite in self.todos_sprites:
            if not sprite.update():
                sprite.kill()

        self.tempo_spawn += 1
        if self.tempo_spawn >= self.tempo_entre_spawns:
            self.spawnar_inimigo()
            self.tempo_spawn = 0

        for inimigo in self.inimigos:
            if inimigo.rect.right < 0:
                self.estado = "GAME_OVER"

    def desenhar_jogo(self):
        self.tela.blit(self.fundo_jogo, (0, 0))
        self.todos_sprites.draw(self.tela)

        fonte = pygame.font.Font(None, 36)
        texto_pontos = fonte.render(f"Pontos: {self.pontuacao}", True, BRANCO)
        self.tela.blit(texto_pontos, (10, 10))

        fonte_peq = pygame.font.Font(None, 20)
        self.tela.blit(fonte_peq.render("M: Matar jogador", True, AMARELO), (LARGURA - 200, 10))
        self.tela.blit(fonte_peq.render("N: Matar inimigo", True, AMARELO), (LARGURA - 200, 30))

    def desenhar_game_over(self):
        self.tela.blit(self.fundo_jogo, (0, 0))

        escuro = pygame.Surface((LARGURA, ALTURA))
        escuro.set_alpha(180)
        escuro.fill(PRETO)
        self.tela.blit(escuro, (0, 0))

        fonte_gde = pygame.font.Font(None, 48)
        fonte_med = pygame.font.Font(None, 36)

        go = fonte_gde.render("GAME OVER", True, VERMELHO)
        go_rect = go.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
        self.tela.blit(go, go_rect)

        pontos = fonte_med.render(f"Pontuação: {self.pontuacao}", True, BRANCO)
        pontos_rect = pontos.get_rect(center=(LARGURA // 2, ALTURA // 2))
        self.tela.blit(pontos, pontos_rect)

        restart = fonte_med.render("Pressione R para reiniciar", True, AMARELO)
        restart_rect = restart.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))
        self.tela.blit(restart, restart_rect)

    def rodar(self):
        if not self.processar_eventos():
            return False

        if self.estado == "MENU":
            self.atualizar_menu()
        elif self.estado == "JOGO":
            self.atualizar_jogo()
            self.desenhar_jogo()
        elif self.estado == "GAME_OVER":
            self.desenhar_game_over()

        return True