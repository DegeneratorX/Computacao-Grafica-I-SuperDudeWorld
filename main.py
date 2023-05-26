import pygame
import time
from pygame.locals import *
from desenho import *
from poligono import *
from screen import *
from sprite import *
from alfabeto import *


def show_fps(screen, clock):
    fps_font = pygame.font.Font(None, 20)
    fps_text = fps_font.render(
        "FPS: " + str(int(clock.get_fps())), True, pygame.Color("yellow"))
    screen.get_screen().blit(fps_text, (10, 10))

# TODO: Colocar objetos na tela
# TODO: Substituir o sprite do player
# TODO: Mudar o nome de alguma variáveis (especialmente as que estão em inglês)
# TODO: Documentar o código

def main():
    pygame.font.init()

    viewport_x_inicial = 0
    viewport_y_inicial = 0
    viewport_x_final = 256
    viewport_y_final = 224
    VIEWPORT = [viewport_x_inicial, viewport_y_inicial,
                viewport_x_final, viewport_y_final]

    janela_x_inicial = 0
    janela_y_inicial = 0
    janela_x_final = 256
    janela_y_final = 224
    janela = [janela_x_inicial, janela_y_inicial,
              janela_x_final, janela_y_final]

    WINDOW_WIDTH = 256
    WINDOW_HEIGHT = 224

    screen_object = Screen(WINDOW_WIDTH, WINDOW_HEIGHT, Color(255, 255, 255))
    pygame.display.set_caption("Super Dude World")

    opcoes_menu = ["Jogar", "Sair"]
    opcao_selecionada = 0
    textura = Texture("tile.jpg")
    player_tile = Texture("player.jpg")
    running = True
    rotacao = 0
    while running:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    opcao_selecionada = (
                        opcao_selecionada - 1) % len(opcoes_menu)
                elif event.key == K_DOWN:
                    opcao_selecionada = (
                        opcao_selecionada + 1) % len(opcoes_menu)
                elif event.key == K_RETURN:
                    if opcao_selecionada == 0:
                        print("Começando o jogo...")

                        player_x = 128
                        player_y = 112
                        player_speed = 4
                        player = Player(player_x, player_y, player_speed)
                        running_game = True

                        while running_game:
                            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                            print("Bem vindo ao debug do Super Dude World!")
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    running_game = False

                            keys = pygame.key.get_pressed()
                            janela = player.mover_janela_e_player(keys, janela)
                            pilha_de_mapeamentos = PilhaMapeamentos(janela, VIEWPORT)
                            
                            ###########################################
                            
                            Poligono.get_bloco_mapeado(0, 0, 16, textura, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(16, 0, 16, textura, pilha_de_mapeamentos)

                            ###########################################
                            """
                            coletavel = [
                                [0, 4, 0, 0],
                                [5, 4, 0, 0],
                                [7, 0, 0, 0],
                                [8, 0, 0, 0],
                                [10, 4, 0, 0],
                                [15, 4, 0, 0],
                                [12, 8, 0, 0],
                                [12, 9, 0, 0],
                                [15, 15, 0, 0],
                                [8, 12, 0, 0],
                                [7, 12, 0, 0],
                                [0, 15, 0, 0],
                                [4, 9, 0, 0],
                                [4, 8, 0, 0],
                            ]

                            coletavel_objeto = Poligono(coletavel)

                            if rotacao < 360:
                                acumulo = Poligono.mover_poligono(-8, -8)
                                acumulo = Poligono.rotacionar_poligono(rotacao, acumulo)
                                acumulo = Poligono.mover_poligono(+8, +8, acumulo)
                                coletavel_objeto.aplicar_transformacao_com_acumulos(acumulo)
                            else:
                                rotacao = -1
                            rotacao += 15
                            """
                            coletavel = Coletavel(0, 0, 0, rotacao)
                            coletavel.get_coletavel_poligono_objeto().get_poligono_customizado_mapeado(Color(238, 255, 0, 0), pilha_de_mapeamentos)
                            if rotacao > 360:
                                rotacao = -1
                            rotacao += 15
                            
                            ###########################################
                            """
                            arestas = [
                                [10,10, 0, 0],
                                [50, 50, 0, 0],
                            ]
                            arestas_objeto = Poligono(arestas)
                            arestas_mapeado = Projecao(arestas_objeto.lista_poligono_customizado, janela, VIEWPORT)
                            arestas_mapeado.get_poligono_mapeado()
                            pilha_de_mapeamentos.lista_de_arestas.append(arestas_mapeado.lista_poligono_mapeado
                                                    )
                            pilha_de_mapeamentos.lista_de_cores.append([])
                            """
                            ###########################################

                            player.get_player_poligono_objeto().get_poligono_customizado_mapeado(player_tile, pilha_de_mapeamentos)

                            ###########################################

                            viewport_objeto = Viewport(
                                viewport_x_inicial, viewport_y_inicial, viewport_x_final, viewport_y_final, pilha_de_mapeamentos.lista_de_mapeamentos)
                            viewport_objeto.update_viewport(pilha_de_mapeamentos.lista_de_cores)

                            ###########################################

                            # Renderização e scanline dos blocos
                            desenhar_na_screen.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(0).lista_poligono_customizado, Color(0, 0, 0, 0), textura)
                            desenhar_na_screen.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(1).lista_poligono_customizado, Color(0, 0, 0, 0), textura)

                            # Renderização e scanline de demais objetos
                            desenhar_na_screen.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(2).lista_poligono_customizado, Color(238, 255, 0, 0), Color(238, 255, 0, 0))

                            # Por fim, o player precisa ter prioridade, então é desenhado por último
                            desenhar_na_screen.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(3).lista_poligono_customizado, Color(180,230,255,0), player_tile)

                            # desenhar_na_screen.reta_DDA(pilha_de_mapeamentos.lista_de_arestas[0][0][0], pilha_de_mapeamentos.lista_de_arestas[0][0][1], pilha_de_mapeamentos.lista_de_arestas[0][1][0], pilha_de_mapeamentos.lista_de_arestas[0][1][1], Color(255, 0, 0))

                            show_fps(screen_object, clock)

                            pygame.display.update()

                            for i in range(viewport_y_final):
                                for j in range(viewport_x_final):
                                    screen_object.get_screen().set_at((j, i), (180,230,255,0))
                            clock.tick(60)

                        pygame.quit()

                    elif opcao_selecionada == 1:
                        print("Saíndo...")
                        running = False

        screen_object.clear_screen()
        desenhar_na_screen = Desenho(screen_object)

        if opcao_selecionada == 0:
            desenhar_na_screen.circunferencia(90, 154, 6, Color(200, 0, 0, 0))
            desenhar_na_screen.flood_fill_iterativo(
                90, 154, Color(255, 58, 58))
        else:
            desenhar_na_screen.circunferencia(90, 170, 6, Color(200, 0, 0, 0))
            desenhar_na_screen.flood_fill_iterativo(
                90, 170, Color(255, 58, 58))

        desenha_titulo(desenhar_na_screen)

        screen_object.update()
        for i in range(viewport_y_final):
            for j in range(viewport_x_final):
                screen_object.get_screen().set_at((j, i), (180,230,255,0))
        clock.tick(60)


if __name__ == '__main__':
    main()
