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
                        player_speed = 5
                        player = Player(player_x, player_y, player_speed, player_tile)
                        running_game = True

                        while running_game:
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    running_game = False

                            keys = pygame.key.get_pressed()
                            janela = player.mover_janela_e_player(keys, janela)

                            lista_de_mapeamentos = list()
                            lista_de_cores = list()
                            lista_de_arestas = list()
                            
                            ###########################################
                            
                            bloco = [
                                [0, 0, 0, 0],
                                [32, 0, 1, 0],
                                [32, 32, 1, 1],
                                [0, 32, 0, 1],
                            ]

                            degrade = [
                                Color(255, 0, 0, 0),
                                Color(0, 255, 0, 0),
                                Color(0, 0, 255, 0),
                                Color(255, 255, 255, 0),
                            ]

                            bloco_object = Poligono(bloco)
                            bloco_mapeado = Projecao(bloco_object.lista_poligono_customizado, janela, VIEWPORT)
                            bloco_mapeado.get_poligono_mapeado()
                            lista_de_mapeamentos.append(bloco_mapeado)
                            lista_de_cores.append(degrade)
                            

                            ###########################################

                            trapezio = [
                                [50, 50, 0, 0],
                                [70, 50, 1, 0],
                                [90, 70, 1, 1],
                                [30, 70, 0, 1],
                            ]

                            trapezio_objeto = Poligono(trapezio)

                            if rotacao < 360:
                                acumulo = Poligono.mover_poligono(-60, -60)
                                acumulo = Poligono.rotacionar_poligono(rotacao, acumulo)
                                acumulo = Poligono.mover_poligono(+60, +60, acumulo)
                                trapezio_objeto.aplicar_transformacao_com_acumulos(acumulo)
                            else:
                                rotacao = -1
                            rotacao += 1

                            trapezio_objeto_mapeado = Projecao(trapezio_objeto.lista_poligono_customizado, janela,
                                                                VIEWPORT)
                            trapezio_objeto_mapeado.get_poligono_mapeado()
                            lista_de_mapeamentos.append(trapezio_objeto_mapeado)
                            lista_de_cores.append([])

                            
                            ###########################################

                            player_sprite_mapeado = Projecao(player.get_player_poligono_objeto().lista_poligono_customizado, janela, VIEWPORT)
                            player_sprite_mapeado.get_poligono_mapeado()
                            lista_de_mapeamentos.append(player_sprite_mapeado)
                            lista_de_cores.append([])

                            ###########################################

                            arestas = [
                                [10,10, 0, 0],
                                [50, 50, 0, 0],
                            ]
                            arestas_objeto = Poligono(arestas)
                            arestas_mapeado = Projecao(arestas_objeto.lista_poligono_customizado, janela, VIEWPORT)
                            arestas_mapeado.get_poligono_mapeado()
                            lista_de_arestas.append(arestas_mapeado.lista_poligono_mapeado
                                                    )
                            lista_de_cores.append([])

                            ###########################################

                            viewport_objeto = Viewport(
                                viewport_x_inicial, viewport_y_inicial, viewport_x_final, viewport_y_final, lista_de_mapeamentos)
                            viewport_objeto.update_viewport(lista_de_cores)

                            ###########################################

                            desenhar_na_screen.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(0).lista_poligono_customizado, Color(0, 0, 0, 0), viewport_objeto.get_conjunto_poligonos_cores(0))
                            desenhar_na_screen.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(1).lista_poligono_customizado, Color(255, 255, 255), textura)
                            desenhar_na_screen.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(2).lista_poligono_customizado, Color(180,230,255,0), player_tile)
                            desenhar_na_screen.reta_DDA(lista_de_arestas[0][0][0], lista_de_arestas[0][0][1], lista_de_arestas[0][1][0], lista_de_arestas[0][1][1], Color(255, 0, 0))

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
            desenhar_na_screen.circunferencia(90, 154, 4, Color(200, 0, 0, 0))
            desenhar_na_screen.flood_fill_iterativo(
                90, 154, Color(255, 58, 58))
        else:
            desenhar_na_screen.circunferencia(90, 170, 4, Color(200, 0, 0, 0))
            desenhar_na_screen.flood_fill_iterativo(
                90, 170, Color(255, 58, 58))

        desenha_titulo(desenhar_na_screen)

        screen_object.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
