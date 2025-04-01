import pygame
import random
import numpy as np
import json

def carregar_recursos():
    imagens = {
        "T": pygame.transform.scale(pygame.image.load("bau.png"), (50, 50)),
        "B": pygame.transform.scale(pygame.image.load("buraco_pirata.png"), (50, 50)),
        "P": pygame.transform.scale(pygame.image.load("powerup.png"), (50, 50)),
        "S": pygame.transform.scale(pygame.image.load("shield.png"), (50, 50)),
        "D": pygame.transform.scale(pygame.image.load("dobra.png"), (50, 50))
    }
    sons = {
        "T": pygame.mixer.Sound("tesouro.wav"),
        "B": pygame.mixer.Sound("buraco.wav"),
        "P": pygame.mixer.Sound("powerup.wav"),
        "S": pygame.mixer.Sound("shield.wav"),
        "D": pygame.mixer.Sound("dobra.wav")
    }
    return imagens, sons

def gerar_tabuleiro(tamanho, num_tesouros, num_buracos, num_powerups, num_escudos, num_dobra):
    tabuleiro = np.full((tamanho, tamanho), None)
    
    def posicionar_itens(tipo, quantidade):
        for _ in range(quantidade):
            while True:
                i, j = random.randint(0, tamanho-1), random.randint(0, tamanho-1)
                if tabuleiro[i, j] is None:
                    tabuleiro[i, j] = tipo
                    break
    
    posicionar_itens("T", num_tesouros)
    posicionar_itens("B", num_buracos)
    posicionar_itens("P", num_powerups)
    posicionar_itens("S", num_escudos)
    posicionar_itens("D", num_dobra)
    
    for i in range(tamanho):
        for j in range(tamanho):
            if tabuleiro[i, j] is None:
                tabuleiro[i, j] = str(sum(
                    1 for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
                    if 0 <= i+dx < tamanho and 0 <= j+dy < tamanho and tabuleiro[i+dx, j+dy] == "T"
                ))
    return tabuleiro

def salvar_historico(pontos):
    try:
        with open("historico.json", "r") as file:
            historico = json.load(file)
    except FileNotFoundError:
        historico = []
    
    historico.append(pontos)
    historico.sort(reverse=True)
    
    with open("historico.json", "w") as file:
        json.dump(historico, file)

def desenhar_tabuleiro(tela, tabuleiro, revelado, imagens, fonte, tamanho, lado, turno, tempo_restante):
    tela.fill((255, 255, 255))
    for i in range(tamanho):
        for j in range(tamanho):
            pygame.draw.rect(tela, (0, 0, 0), (i * lado, j * lado, lado, lado), 1)
            if revelado[i][j]:
                conteudo = tabuleiro[i, j]
                if conteudo in imagens:
                    tela.blit(imagens[conteudo], (i * lado, j * lado))
                else:
                    tela.blit(fonte.render(conteudo, True, (0, 0, 0)), (i * lado + 12, j * lado + 10))
    tela.blit(fonte.render(f"Turno: Jogador {1 if turno % 2 == 0 else 2}", True, (0, 0, 255)), (10, tamanho * lado + 10))
    tela.blit(fonte.render(f"Tempo: {int(tempo_restante)}s", True, (255, 0, 0)), (250, tamanho * lado + 10))
    pygame.display.update()

def jogar():
    pygame.init()
    pygame.mixer.init()
    
    tamanho, lado = 8, 50
    num_tesouros, num_buracos, num_powerups, num_escudos, num_dobra = 15, 8, 5, 3, 2
    tela = pygame.display.set_mode((tamanho * lado, (tamanho + 1) * lado))
    pygame.display.set_caption("Caça ao Tesouro")
    
    imagens, sons = carregar_recursos()
    fonte = pygame.font.SysFont("Comic Sans MS", 30)
    tabuleiro = gerar_tabuleiro(tamanho, num_tesouros, num_buracos, num_powerups, num_escudos, num_dobra)
    revelado = np.full((tamanho, tamanho), False)
    pontos = [0, 0]
    escudos = [0, 0]
    turno = 0
    tempo_max = 60  # segundos
    clock = pygame.time.Clock()
    combo = [0, 0]
    
    rodando = True
    while rodando and tempo_max > 0:
        clock.tick(30)
        tempo_max -= 1 / 30
        desenhar_tabuleiro(tela, tabuleiro, revelado, imagens, fonte, tamanho, lado, turno, tempo_max)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = evento.pos[0] // lado, evento.pos[1] // lado
                if y < tamanho and not revelado[x, y]:
                    revelado[x, y] = True
                    conteudo = tabuleiro[x, y]
                    jogador = turno % 2
                    if conteudo == "T":
                        combo[jogador] += 1
                        pontos[jogador] += 100 + combo[jogador] * 10
                        sons["T"].play()
                    elif conteudo == "B":
                        combo[jogador] = 0
                        if escudos[jogador] > 0:
                            escudos[jogador] -= 1
                        else:
                            pontos[jogador] = max(0, pontos[jogador] - 50)
                            sons["B"].play()
                    elif conteudo == "P":
                        pontos[jogador] += 50
                        sons["P"].play()
                    elif conteudo == "S":
                        escudos[jogador] += 1
                        sons["S"].play()
                    elif conteudo == "D":
                        pontos[jogador] *= 2
                        sons["D"].play()
                    turno += 1
                    if all(all(row) for row in revelado):
                        rodando = False
    
    salvar_historico(max(pontos))
    pygame.quit()

if __name__ == "__main__":
    jogar()
