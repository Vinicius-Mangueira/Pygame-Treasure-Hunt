import pygame
import random
import numpy as np
import json
import os

def carregar_recursos():
    """Carrega imagens e sons com verificação de arquivos."""
    caminho_base = os.path.dirname(__file__)

    def carregar_imagem(nome, tamanho=(50, 50)):
        caminho = os.path.join(caminho_base, nome)
        if os.path.exists(caminho):
            return pygame.transform.scale(pygame.image.load(caminho), tamanho)
        else:
            print(f"[AVISO] Imagem {nome} não encontrada.")
            return None

    def carregar_som(nome):
        caminho = os.path.join(caminho_base, nome)
        if os.path.exists(caminho):
            return pygame.mixer.Sound(caminho)
        else:
            print(f"[AVISO] Som {nome} não encontrado.")
            return None

    imagens = {
        "T": carregar_imagem("bau.png"),
        "B": carregar_imagem("buraco_pirata.png"),
        "P": carregar_imagem("powerup.jpeg"),
        "S": carregar_imagem("shield.png"),
        "D": carregar_imagem("dobra.jpeg"),
    }
    
    sons = {
        "T": carregar_som("tesouro.wav"),
        "B": carregar_som("buraco.wav"),
        "P": carregar_som("powerup.wav"),
        "S": carregar_som("shield.wav"),
        "D": carregar_som("dobra.wav"),
    }

    return imagens, sons

def jogar():
    """Inicializa o jogo e controla a lógica principal."""
    pygame.init()
    pygame.mixer.init()

    tamanho, lado = 8, 50
    tela = pygame.display.set_mode((tamanho * lado, (tamanho + 1) * lado))
    pygame.display.set_caption("Caça ao Tesouro")

    imagens, sons = carregar_recursos()
    fonte = pygame.font.SysFont("Comic Sans MS", 30)
    clock = pygame.time.Clock()
    tempo_max = 60  # segundos

    rodando = True
    while rodando and tempo_max > 0:
        clock.tick(30)
        tempo_max = max(0, tempo_max - 1 / 30)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if "T" in sons and sons["T"] is not None:
                    sons["T"].play()

    pygame.quit()

if __name__ == "__main__":
    jogar()
