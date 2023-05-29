import pygame
from pygame.locals import *
from desenho import *
from poligono import *
from screen import *
from sprite import *
from alfabeto import *
import shapes


def mostrar_fps(screen, clock):
    texto_fps_objeto = pygame.font.Font(None, 20)
    texto_fps_desenhar = texto_fps_objeto.render("FPS: " + str(int(clock.get_fps())), True, pygame.Color("red"))
    screen.get_pygame_screen().blit(texto_fps_desenhar, (8, 8))

def mostrar_coletados(screen, estrelas_coletadas):
    texto_coletados_objeto = pygame.font.Font(None, 16)
    texto_coletados_desenhar = texto_coletados_objeto.render("Estrelas coletadas: " + str(int(len(estrelas_coletadas)))+"/5", True, pygame.Color(255,160,0,0))
    screen.get_pygame_screen().blit(texto_coletados_desenhar, (128, 8))

def fim_de_jogo(screen):
    tela_fim_de_jogo = True
    while tela_fim_de_jogo:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(1)
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    exit(1)
        
        texto_concluido_objeto = pygame.font.Font(None, 16)
        texto_concluido_desenhar = texto_concluido_objeto.render("PARABÉNS! Você encontrou todas as estrelas." , False, pygame.Color("red"))
        screen.get_pygame_screen().blit(texto_concluido_desenhar, (2, 100))

        texto_pressioneenter_objeto = pygame.font.Font(None, 16)
        texto_pressioneenter_desenhar = texto_pressioneenter_objeto.render("Pressione ENTER para sair." , False, pygame.Color("red"))
        screen.get_pygame_screen().blit(texto_pressioneenter_desenhar, (48, 130))
        pygame.display.update()

        texto_creditos1_objeto = pygame.font.Font(None, 14)
        texto_creditos1_desenhar = texto_creditos1_objeto.render("Feito por:" , False, pygame.Color("black"))
        screen.get_pygame_screen().blit(texto_creditos1_desenhar, (4, 194))
        pygame.display.update()

        texto_creditos2_objeto = pygame.font.Font(None, 14)
        texto_creditos2_desenhar = texto_creditos2_objeto.render("MIRAILTON MOTA COSTA FILHO" , False, pygame.Color("black"))
        screen.get_pygame_screen().blit(texto_creditos2_desenhar, (4, 202))
        pygame.display.update()

        texto_creditos3_objeto = pygame.font.Font(None, 14)
        texto_creditos3_desenhar = texto_creditos3_objeto.render("VICTOR MEDEIROS MARTINS" , False, pygame.Color("black"))
        screen.get_pygame_screen().blit(texto_creditos3_desenhar, (4, 210))
        pygame.display.update()



# TODO: Colocar objetos na tela
# TODO: Mudar o nome de alguma variáveis (especialmente as que estão em inglês)
# TODO: Documentar o código

def main():
    # Possibilita o uso de fonte no pygame
    pygame.font.init()

    # Declaro as dimensões de viewport (int), mesmo tamanho da windowsize do pygame.
    viewport_x_inicial = 0
    viewport_y_inicial = 0
    viewport_x_final = 256
    viewport_y_final = 224
    VIEWPORT = [viewport_x_inicial, viewport_y_inicial, viewport_x_final, viewport_y_final]

    # Declaro as coordenadas da janela, qual recorte do mundo ela irá fazer (float)
    janela_x_inicial = 0
    janela_y_inicial = 0
    janela_x_final = 256
    janela_y_final = 224
    janela = [janela_x_inicial, janela_y_inicial, janela_x_final, janela_y_final]

    # windowsize do pygame
    PYGAME_LARGURA_JANELA = 256
    PYGAME_ALTURA_JANELA = 224

    # Crio uma classe Screen e instancio um objeto de lá.
    tela_objeto = Tela(PYGAME_LARGURA_JANELA, PYGAME_ALTURA_JANELA)
    # Título da janela do pygame
    pygame.display.set_caption("Super Dude World")

    # Vetor que guarda as opções de tela inicial
    opcoes_menu = ["Jogar", "Sair"]

    # Variável de controle para seleção do menu
    opcao_selecionada = 0

    # Carregamento de texturas e instanciação de classes que criei desse tipo
    textura_cimento = Textura("assets/cementblock.png")
    textura_zoom = Textura("assets/zoom.png")
    textura_boo = Textura("assets/boo.png")
    textura_gato = Textura("assets/gato.png")
    textura_bulletbill = Textura("assets/bulletbill.png")
    textura_banana = Textura("assets/banana.png")
    textura_player = Textura("assets/player.png")

    # Variável de controle para rotação do sprite coletável estrela
    rotacao = 0

    contador_de_movimentos_bullet_bill = 0
    bullet_esquerda = True

    tela_inicial = True
    while tela_inicial:
        # Convenções do pygame, se coloca essas linhas de código abaixo antes de qualquer jogo
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
            # Como estou na tela inicial, preciso criar um menu. Aqui recebe inputs de teclas do
            # usuário.
            if event.type == KEYDOWN:
                # Navego pelas opções "Jogar" e "Sair"
                if event.key == K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes_menu)
                elif event.key == K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes_menu)
                # Se eu aperto enter...
                elif event.key == K_RETURN:
                    # ...só tem dois casos: ou eu saí, ou eu vou jogar.
                    if opcao_selecionada == 0: # Se escolhi a opção de jogar...
                        print("Começando o jogo...")
                        # Aqui preparo definições iniciais antes de começar a lógica do jogo.

                        # Defino onde o player começa e sua velocidade
                        jogador_pos_x = 128
                        jogador_pos_y = 112
                        jogador_velocidade = 4

                        # Instancio a classe Jogador com essas propriedades
                        jogador = Jogador(jogador_pos_x, jogador_pos_y, jogador_velocidade)

                        # Crio uma lista vazia que irá armazenar todos os coletáveis do jogo.
                        # Se esse vetor atingir certo tamanho, o jogo acaba.
                        estrelas_coletadas = []
                        dentro_do_zoom_in = False
                        dentro_do_zoom_out = False
                        dentro_da_banana = False
                        tela_jogavel = True
                        ##### Aqui começa a lógica do jogo #####
                        while tela_jogavel:
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    tela_jogavel = False

                            # Precisarei desse objeto para usar as teclas de movimentação do jogador mais tarde
                            keys = pygame.key.get_pressed()

                            # Linha importantíssima. Ela faz a movimentação do jogador e da janela acompanhar juntas.
                            # Transformação linear de translação de janela e jogador.
                            janela = jogador.mover_janela_e_jogador(keys, janela)

                            # Uma pilha de mapeamentos instanciada que guarda 2 vetores: lista de mapeamentos e cores,
                            # que irão ser utilizados no clipping.
                            pilha_de_mapeamentos = PilhaMapeamentos(janela, VIEWPORT)

                            ###########################################
                            ###########################################
                            # Instanciação dos polígonos que definem o limite do mapa.

                            lim_sup_black_obj = Poligono(shapes.limite_sup_black)
                            lim_dir_black_obj = Poligono(shapes.limite_dir_black)
                            lim_inf_black_obj = Poligono(shapes.limite_inf_black)
                            lim_esq_black_obj = Poligono(shapes.limite_esq_black)

                            lim_sup_black_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)
                            lim_dir_black_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)
                            lim_inf_black_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)
                            lim_esq_black_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            lim_sup_red_obj = Poligono(shapes.limite_sup_red)
                            lim_dir_red_obj = Poligono(shapes.limite_dir_red)
                            lim_inf_red_obj = Poligono(shapes.limite_inf_red)
                            lim_esq_red_obj = Poligono(shapes.limite_esq_red)

                            lim_sup_red_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)
                            lim_dir_red_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)
                            lim_inf_red_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)
                            lim_esq_red_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            ###########################################
                            ###########################################
                            # Instanciação de polígonos diversos pelo mapa.
                            # Nesse caso aqui também estou além de instanciando, mapeando tudo para a viewport
                            # e guardando sua textura ou cores naqueles vetores da pilha de mapeamentos.

                            # Desenha o "OI" no mapa.
                            Poligono.get_bloco_mapeado(0, 0, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(16, 0, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(32, 0, 16, pilha_de_mapeamentos)

                            Poligono.get_bloco_mapeado(32, 16, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(32, 32, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(32, 48, 16, pilha_de_mapeamentos)

                            Poligono.get_bloco_mapeado(32, 64, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(16, 64, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(0, 64, 16, pilha_de_mapeamentos)

                            Poligono.get_bloco_mapeado(0, 48, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(0, 32, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(0, 16, 16, pilha_de_mapeamentos)


                            Poligono.get_bloco_mapeado(64, 0, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(80, 0, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(96, 0, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(80, 16, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(80, 32, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(80, 48, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(64, 64, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(80, 64, 16, pilha_de_mapeamentos)
                            Poligono.get_bloco_mapeado(96, 64, 16, pilha_de_mapeamentos)

                            ###########################################
                            ###########################################
                            # Instanciação do polígono que dará um zoom na janela ao pisar em cima

                            Poligono.get_bloco_mapeado(450, 300, 32, pilha_de_mapeamentos)
                            pos_x, pos_y = jogador.get_posicao()
                            if 450 < pos_x < 482 and 300 < pos_y < 332 and dentro_do_zoom_in == False:
                                janela[0] += 50
                                janela[1] += 45
                                janela[2] -= 50
                                janela[3] -= 45
                                dentro_do_zoom_in = True

                            elif ((450 >= pos_x or pos_x >= 482) or (300 >= pos_y or pos_y >= 332)) and dentro_do_zoom_in == True:
                                janela[0] -= 50
                                janela[1] -= 45
                                janela[2] += 50
                                janela[3] += 45
                                dentro_do_zoom_in = False


                            Poligono.get_bloco_mapeado(400, 300, 32, pilha_de_mapeamentos)
                            pos_x, pos_y = jogador.get_posicao()
                            if 400 < pos_x < 432 and 300 < pos_y < 332 and dentro_do_zoom_out == False:
                                janela[0] -= 100
                                janela[1] -= 90
                                janela[2] += 100
                                janela[3] += 90
                                dentro_do_zoom_out = True

                            elif ((400 >= pos_x or pos_x >= 432) or (300 >= pos_y or pos_y >= 332)) and dentro_do_zoom_out == True:
                                janela[0] += 100
                                janela[1] += 90
                                janela[2] -= 100
                                janela[3] -= 90
                                dentro_do_zoom_out = False

                            ###########################################
                            ###########################################
                            # Blocos de scanline diversos

                            retangulo_solido_obj = Poligono(shapes.retangulo_solido)
                            retangulo_solido_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            triangulo_degrade_1_obj = Poligono(shapes.triangulo_degrade_1)
                            triangulo_degrade_1_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos, shapes.triangulo_lista_cores_1)

                            retangulo_textura_obj = Poligono(shapes.retangulo_textura)
                            retangulo_textura_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            triangulo_degrade_2_obj = Poligono(shapes.triangulo_degrade_2)
                            triangulo_degrade_2_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos, shapes.triangulo_lista_cores_2)

                            ###########################################
                            ###########################################
                            # Boo no mapa

                            boo_obj = Poligono(shapes.boo)
                            acumulo = Poligono.mover_poligono(-190,+310)
                            acumulo = Poligono.rotacionar_poligono(rotacao, acumulo)
                            acumulo = Poligono.mover_poligono(+190,-310, acumulo)
                            boo_obj.aplicar_transformacao_com_acumulos(acumulo)
                            boo_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            ###########################################
                            ###########################################
                            # Bullet Bill no mapa
                            bulletbill_obj = Poligono(shapes.bulletbill)
                            
                            if contador_de_movimentos_bullet_bill < 15:
                                if bullet_esquerda:
                                    acumulo = Poligono.redimensionar_poligono(1.2, 1.2)
                                else:
                                    acumulo = Poligono.redimensionar_poligono(1.0/1.2, 1.0/1.2)
                                bulletbill_obj.aplicar_transformacao_com_acumulos(acumulo)
                                contador_de_movimentos_bullet_bill += 1
                            if contador_de_movimentos_bullet_bill == 15:
                                contador_de_movimentos_bullet_bill = 0
                                if bullet_esquerda:
                                    bullet_esquerda = False
                                else:
                                    bullet_esquerda = True
                            
                            bulletbill_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            ###########################################
                            ###########################################
                            # Instanciação da banana (easter egg)
                            banana_obj = Poligono(shapes.banana)
                            pos_x, pos_y = jogador.get_posicao()
                            if 0 < pos_x < 16 and 350 < pos_y < 366 and dentro_da_banana == False:
                                acumulo = Poligono.redimensionar_poligono(1.4, 1.4)
                                acumulo = Poligono.mover_poligono(-5, -100, acumulo)
                                banana_obj.aplicar_transformacao_com_acumulos(acumulo)
                            elif ((0 >= pos_x or pos_x >= 16) or (350 >= pos_y or pos_y >= 366)) and dentro_da_banana == True:
                                acumulo = Poligono.redimensionar_poligono(1/1.4, 1/1.4)
                                acumulo = Poligono.mover_poligono(+5, +100, acumulo)
                                banana_obj.aplicar_transformacao_com_acumulos(acumulo)

                            banana_obj.get_poligono_customizado_mapeado(pilha_de_mapeamentos)
                            ###########################################
                            ###########################################

                            # Instanciação de sprites (coletáveis) pelo mapa

                            # Propriedade que rotaciona a estrela coletável
                            if rotacao > 360:
                                rotacao = 5
                            rotacao += 5

                            # Instanciação, mapeamento (viewport) e armazenamento em vetores, além da lógica para saber se
                            # o coletável já foi coletado.
                            coletavel_0 = Coletavel.inserir_coletavel(0, 16, 32, rotacao, jogador, estrelas_coletadas)
                            coletavel_0.get_coletavel_poligono_objeto().get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            coletavel_1 = Coletavel.inserir_coletavel(1, 180, -316, rotacao, jogador, estrelas_coletadas)
                            coletavel_1.get_coletavel_poligono_objeto().get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            coletavel_2 = Coletavel.inserir_coletavel(2, 435, 280, rotacao, jogador, estrelas_coletadas)
                            coletavel_2.get_coletavel_poligono_objeto().get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            coletavel_3 = Coletavel.inserir_coletavel(3, -330, 240, rotacao, jogador, estrelas_coletadas)
                            coletavel_3.get_coletavel_poligono_objeto().get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            coletavel_4 = Coletavel.inserir_coletavel(4, -260, -260, rotacao, jogador, estrelas_coletadas)
                            coletavel_4.get_coletavel_poligono_objeto().get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            # Se todos os coletáveis foram coletados, o jogo acaba.
                            if len(estrelas_coletadas) == 5:
                                fim_de_jogo(tela_objeto)

                            ###########################################
                            ###########################################

                            # Mapeamento do player na viewport. Precisa ficar por último na lista de mapeamentos, dado que
                            # ele precisa ter prioridade na hora de desenhar (ficar por cima de tudo)
                            jogador.get_jogador_poligono_objeto().get_poligono_customizado_mapeado(pilha_de_mapeamentos)

                            ###########################################
                            ###########################################

                            # Instanciação de um objeto de viewport, para que eu possa trabalhar melhor com os dados.
                            # Isso me daria també ma possibilidade de criar múltiplas viewports.
                            viewport_objeto = Viewport(viewport_x_inicial, viewport_y_inicial, viewport_x_final, viewport_y_final, pilha_de_mapeamentos.lista_de_mapeamentos)

                            # Clipping
                            viewport_objeto.update_viewport(pilha_de_mapeamentos.lista_de_cores)

                            ###########################################
                            ###########################################
                            # Finalmente o desenho na matriz do pygame (setpixel)

                            # Renderização dos limites do mapa (linha preta)
                            for i in range(0, 4):
                                desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(i).lista_poligono_customizado, Cor(0,0,0,0), Cor(0,0,0,0))

                            # Renderização dos limites do mapa (linha vermelha)
                            for i in range(4, 8):
                                desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(i).lista_poligono_customizado, Cor(200,0,0,0), Cor(200,0,0,0))

                            # Renderização e scanline dos blocos OI
                            for i in range(8, 29):
                                desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(i).lista_poligono_customizado, Cor(180, 230, 255, 0), textura_cimento)
                            
                            # Renderização e scanline dos blocos ZOOM
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(29).lista_poligono_customizado, Cor(0,0,0,0), textura_zoom)
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(30).lista_poligono_customizado, Cor(0,0,0,0), textura_zoom)

                            # Renderização e scanline dos degradês
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(31).lista_poligono_customizado, Cor(180, 230, 255, 0), Cor(100, 0, 0, 0))
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(32).lista_poligono_customizado, Cor(180, 230, 255, 0), viewport_objeto.get_conjunto_poligonos_cores(32))
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(33).lista_poligono_customizado, Cor(180, 230, 255, 0), textura_gato)
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(34).lista_poligono_customizado, Cor(180, 230, 255, 0), viewport_objeto.get_conjunto_poligonos_cores(34))

                            # Renderização e scanline do boo
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(35).lista_poligono_customizado, Cor(180, 230, 255, 0), textura_boo)

                            # Renderização e scanline do bulletbill
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(36).lista_poligono_customizado, Cor(180, 230, 255, 0), textura_bulletbill)

                            # Renderização da banana
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(37).lista_poligono_customizado, Cor(180, 230, 255, 0), textura_banana)

                            # Renderização dos coletáveis
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(38).lista_poligono_customizado, Cor(238, 255, 0, 0), Cor(238, 255, 0, 0))
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(39).lista_poligono_customizado, Cor(238, 255, 0, 0), Cor(238, 255, 0, 0))
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(40).lista_poligono_customizado, Cor(238, 255, 0, 0), Cor(238, 255, 0, 0))
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(41).lista_poligono_customizado, Cor(238, 255, 0, 0), Cor(238, 255, 0, 0))
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(42).lista_poligono_customizado, Cor(238, 255, 0, 0), Cor(238, 255, 0, 0))

                            # Por fim, o player precisa ter prioridade, então é desenhado por último
                            desenhar_na_tela.desenha_poligono(viewport_objeto.get_conjunto_poligonos_cortados(43).lista_poligono_customizado, Cor(180,230,255,0), textura_player)

                            # Mostra o FPS do jogo
                            mostrar_fps(tela_objeto, clock)
                            mostrar_coletados(tela_objeto, estrelas_coletadas)

                            # Exibe coordenadas de jogador e janela no game
                            jogador.exibir_coordenadas(tela_objeto, janela)

                            # Mostra os desenhos na tela (transforma a matriz do pygame em pixels na tela)
                            pygame.display.update()

                            # Limpa a tela para o próximo frame.
                            for i in range(viewport_y_final):
                                for j in range(viewport_x_final):
                                    tela_objeto.get_pygame_screen().set_at((j, i), (180,230,255,0))

                            # Limite de 60 quadros por segundo.
                            clock.tick(60)

                        pygame.quit()

                    # Se a outra opção foi a de sair, sai do jogo.
                    elif opcao_selecionada == 1:
                        print("Saíndo...")
                        tela_inicial = False

        ##### Desenho da tela inicial #####
        # Preenchimento do fundo da tela inicial. Não é 100% branco!
        for i in range(PYGAME_ALTURA_JANELA):
            for j in range(PYGAME_LARGURA_JANELA):
                tela_objeto.get_pygame_screen().set_at((j, i), (230,230,230,0))

        # Instancio o objeto desenhar_na_tela e passo a tela. Assim, a partir dela, eu desenho
        # diversos algoritmos de desenho, como DDA, circunferência e scanline.
        desenhar_na_tela = Desenho(tela_objeto)

        # Se eu estiver na opção de jogar, desenha uma cirfunferência pequena preenchida
        # com flood fill vermelho.
        if opcao_selecionada == 0:
            desenhar_na_tela.circunferencia(90, 154, 6, Cor(200, 0, 0, 0))
            desenhar_na_tela.flood_fill_iterativo(
                90, 154, Cor(255, 58, 58))
        # E mudo a circunferência de lugar quando for escolher a outra opção
        else:
            desenhar_na_tela.circunferencia(90, 170, 6, Cor(200, 0, 0, 0))
            desenhar_na_tela.flood_fill_iterativo(
                90, 170, Cor(255, 58, 58))
        
        # Função para enxugar código, ela desenha o título do jogo: SUPER DUDE WORLD
        # na tela inicial, junto com a elipse e as opções de JOGAR e SAIR.
        desenha_titulo(desenhar_na_tela)

        # Joga os desenhos da matriz do pygame pra placa de vídeo
        pygame.display.update()

        # Depois de desenhado, limpo a tela.
        for i in range(viewport_y_final):
            for j in range(viewport_x_final):
                tela_objeto.get_pygame_screen().set_at((j, i), (180,230,255,0))

        # Limite de 60 quadros por segundo.
        clock.tick(60)


if __name__ == '__main__':
    main()
