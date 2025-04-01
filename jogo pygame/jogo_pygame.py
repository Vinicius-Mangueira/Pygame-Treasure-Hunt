import pygame
import random

def main():
    pygame.init()

    preto = (0, 0, 0)
    branco = (255, 255, 255)
    vermelho = (255, 0, 0)
    verde = (0, 255, 0)
    azul = (0, 0, 255)

    lado_celula = 50
    num_linhas = 4
    num_buracos = 3
    num_tesouros = 6

    tela = pygame.display.set_mode((num_linhas * lado_celula, (num_linhas + 1) * lado_celula))
    pygame.display.set_caption("Caça ao Tesouro")
    tela.fill(branco)

    img_tesouro = pygame.image.load("bau.png")
    img_tesouro = pygame.transform.scale(img_tesouro, (50, 50))

    img_buraco = pygame.image.load("buraco_pirata.png")
    img_buraco = pygame.transform.scale(img_buraco, (50, 50))

    fonte = pygame.font.SysFont("Comic Sans MS", 30)
    
    for i in range(0, num_linhas):
        for j in range(0, num_linhas):
            pygame.draw.rect(tela, preto, (i * lado_celula, j * lado_celula, lado_celula, lado_celula), 1)
    
    pygame.display.update()

    conteudo_celula = [[None for _ in range(num_linhas)] for _ in range(num_linhas)]
    celula_revelada = [[False for _ in range(num_linhas)] for _ in range(num_linhas)]

    def gerar_itens(tipo, quantidade):
        count = 0
        while count < quantidade:
            i, j = random.randint(0, num_linhas - 1), random.randint(0, num_linhas - 1)
            if conteudo_celula[i][j] is None:
                conteudo_celula[i][j] = tipo
                count += 1
    
    gerar_itens("T", num_tesouros)
    gerar_itens("B", num_buracos)

    def contar_tesouros_vizinhos():
        for i in range(num_linhas):
            for j in range(num_linhas):
                if conteudo_celula[i][j] is None:
                    conteudo_celula[i][j] = str(sum(1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                                                      if 0 <= i + dx < num_linhas and 0 <= j + dy < num_linhas 
                                                      and conteudo_celula[i + dx][j + dy] == "T"))
    
    contar_tesouros_vizinhos()

    pontuacao_jogador1 = 0
    pontuacao_jogador2 = 0
    turno = 0
    jogo_cancelado = False
    jogo_terminado = False

    def desenhar_texto(texto, x, y, cor):
        texto_render = fonte.render(texto, True, cor)
        tela.blit(texto_render, (x, y))

    while not jogo_cancelado and not jogo_terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_cancelado = True
                break

            tela_mudou = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                celula_x, celula_y = mouse_x // lado_celula, mouse_y // lado_celula
                if celula_y > num_linhas - 1:
                    continue

                if not celula_revelada[celula_x][celula_y]:
                    tela_mudou = True
                    celula_revelada[celula_x][celula_y] = True
                    turno += 1

                    if conteudo_celula[celula_x][celula_y] == "T":
                        tela.blit(img_tesouro, (celula_x * lado_celula, celula_y * lado_celula))
                        if turno % 2 != 0:
                            pontuacao_jogador1 += 100
                        else:
                            pontuacao_jogador2 += 100

                    elif conteudo_celula[celula_x][celula_y] == "B":
                        tela.blit(img_buraco, (celula_x * lado_celula, celula_y * lado_celula))
                        if turno % 2 != 0:
                            pontuacao_jogador1 = max(0, pontuacao_jogador1 - 50)
                        else:
                            pontuacao_jogador2 = max(0, pontuacao_jogador2 - 50)
                    else:
                        desenhar_texto(conteudo_celula[celula_x][celula_y], celula_x * lado_celula + 12, celula_y * lado_celula + 10, preto)

                    if all(all(row) for row in celula_revelada):
                        jogo_terminado = True
        
        if tela_mudou:
            pygame.display.update()
    
    if jogo_terminado:
        tela.fill(branco)
        if pontuacao_jogador1 > pontuacao_jogador2:
            mensagem_vencedor = "Jogador 1 venceu!"
        elif pontuacao_jogador2 > pontuacao_jogador1:
            mensagem_vencedor = "Jogador 2 venceu!"
        else:
            mensagem_vencedor = "Empate!"
        desenhar_texto(mensagem_vencedor, 100, 60, preto)
        desenhar_texto(f"Jogador 1: {pontuacao_jogador1}", 100, 120, verde)
        desenhar_texto(f"Jogador 2: {pontuacao_jogador2}", 100, 180, azul)
        pygame.display.update()
        pygame.time.wait(5000)

    pygame.quit()

if __name__ == "__main__":
    main()
