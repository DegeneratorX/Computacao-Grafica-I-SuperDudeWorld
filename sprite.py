import pygame
from pygame.locals import *
from abc import ABC
from poligono import *

# Classe abstrata de Sprites. A ideia inicial era também fazer uma classe de inimigos para herdar ela aqui.
class Sprite(ABC):
    def __init__(self, pos_x, pos_y, velocidade, visivel=True) -> None:
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._velocidade = velocidade
        self._visivel = visivel


class Jogador(Sprite):
    def __init__(self, pos_x, pos_y, velocidade, visivel=True) -> None:
        super().__init__(pos_x, pos_y, velocidade, visivel)
        # Lista de vértices do polígono do jogador. O seu centro fica no meio
        # do polígono, não no primeiro vértice.
        self._jogador_lista_poligono = [
            [self._pos_x-8,self._pos_y-8,0,0],
            [self._pos_x+8,self._pos_y-8,1,0],
            [self._pos_x+8,self._pos_y+8,1,1],
            [self._pos_x-8,self._pos_y+8,0,1],
        ]
        # Instância desse polígono
        self._player_poligono_objeto = Poligono(self._jogador_lista_poligono)

        # Por padrão, ele começa olhando pra cima.
        self._direcao = "up"

    def get_posicao(self):
        return self._pos_x, self._pos_y

    def get_jogador_lista_poligono(self):
        return self._jogador_lista_poligono
    
    def get_jogador_poligono_objeto(self):
        return self._player_poligono_objeto

    # Método de inúmeras transformações lineares que translada e rotaciona o boneco pelo mapa
    # baseado em como o jogador aperta os botões.
    def mover_janela_e_jogador(self, keys, janela):
        janela_x_inicial, janela_y_inicial, janela_x_final, janela_y_final = janela
        
        # Se o jogador aperta pra esquerda...
        if keys[K_LEFT]:
            # ...e anteriormente ele estava pra cima, gira -90°
            if self._direcao == "up":
                self.__rotacionar_em_torno_do_eixo(-90)
            # gira 180° se ele tava olhando pra direita e quer ir pra esquerda
            elif self._direcao == "right":
                self.__rotacionar_em_torno_do_eixo(180)
            elif self._direcao == "down":
                self.__rotacionar_em_torno_do_eixo(90)
            # Obviamente se ele já tava olhando pra esquerda, faça nada.
            elif self._direcao == "left":
                pass

            # Finalmente, a direção dele atual é pra esquerda.
            self._direcao = "left"

            # Finalmente movo ele (transformação linear) após rotacionar em torno do próprio eixo, baseado na velocidade.
            acumulo = Poligono.mover_poligono(-self._velocidade, 0)
            self._player_poligono_objeto.aplicar_transformacao_com_acumulos(acumulo)

            # Atualizo as informações de coordenadas de janela e jogador.
            self._pos_x -= self._velocidade
            janela_x_inicial -= self._velocidade
            janela_x_final -= self._velocidade

        if keys[K_RIGHT]:
            if self._direcao == "up":
                self.__rotacionar_em_torno_do_eixo(90)
            elif self._direcao == "right":
                pass
            elif self._direcao == "down":
                self.__rotacionar_em_torno_do_eixo(-90)
            elif self._direcao == "left":
                self.__rotacionar_em_torno_do_eixo(180)
            self._direcao = "right"

            acumulo = Poligono.mover_poligono(+self._velocidade, 0)
            self._player_poligono_objeto.aplicar_transformacao_com_acumulos(acumulo)
            self._pos_x += self._velocidade
            janela_x_inicial += self._velocidade
            janela_x_final += self._velocidade
        if keys[K_UP]:
            if self._direcao == "up":
                pass
            elif self._direcao == "right":
                self.__rotacionar_em_torno_do_eixo(-90)
            elif self._direcao == "down":
                self.__rotacionar_em_torno_do_eixo(180)
            elif self._direcao == "left":
                self.__rotacionar_em_torno_do_eixo(90)
            self._direcao = "up"

            acumulo = Poligono.mover_poligono(0, -self._velocidade)
            self._player_poligono_objeto.aplicar_transformacao_com_acumulos(acumulo)
            self._pos_y -= self._velocidade
            janela_y_inicial -= self._velocidade
            janela_y_final -= self._velocidade
        if keys[K_DOWN]:
            if self._direcao == "up":
                self.__rotacionar_em_torno_do_eixo(180)
            elif self._direcao == "right":
                self.__rotacionar_em_torno_do_eixo(90)
            elif self._direcao == "down":
                pass
            elif self._direcao == "left":
                self.__rotacionar_em_torno_do_eixo(-90)
            self._direcao = "down"

            acumulo = Poligono.mover_poligono(0, +self._velocidade)
            self._player_poligono_objeto.aplicar_transformacao_com_acumulos(acumulo)
            self._pos_y += self._velocidade
            janela_y_inicial += self._velocidade
            janela_y_final += self._velocidade

        # Retorno para usar, se for o caso, os novos valores de janela.
        return [janela_x_inicial, janela_y_inicial, janela_x_final, janela_y_final]
    
    # Função simples apenas para tratar a rotação em torno do eixo: movo pra origem, rotaciono e devolvo.
    def __rotacionar_em_torno_do_eixo(self, angulo):
        acumulo = Poligono.mover_poligono(-self._pos_x,-self._pos_y)
        acumulo = Poligono.rotacionar_poligono(angulo, acumulo, player=True)
        acumulo = Poligono.mover_poligono(+self._pos_x,+self._pos_y, acumulo)
        self._player_poligono_objeto.aplicar_transformacao_com_acumulos(acumulo)
    

    def exibir_coordenadas(self, screen, janela):
        texto_coordenadasjogador_objeto = pygame.font.Font(None, 14)
        texto_coordenadasjogador_desenhar = texto_coordenadasjogador_objeto.render("x: " + str(int(self._pos_x+8)) + "  y: " + str(int(self._pos_y+8)), True, pygame.Color("black"))
        screen.get_pygame_screen().blit(texto_coordenadasjogador_desenhar, (8, 200))

        texto_coordenadasjanela_objeto = pygame.font.Font(None, 14)
        texto_coordenadasjanela_desenhar = texto_coordenadasjanela_objeto.render("Janela em x: (" + str(int(janela[0])) + "," + str(int(janela[2])) + ")  Janela em y: (" + str(int(janela[1])) + "," + str(int(janela[3])) + ")", True, pygame.Color("black"))
        screen.get_pygame_screen().blit(texto_coordenadasjanela_desenhar, (8, 209))


# Classe que guarda informações dos coletáveis pelo mapa. Também são sprites.
class Coletavel(Sprite):
    def __init__(self, pos_x, pos_y, velocidade, rotacao, visivel=True) -> None:
        super().__init__(pos_x, pos_y, velocidade, visivel)
    
        if self._visivel:
            # Se ele não foi coletado, ele aparece no mapa assim: uma estrela.
            # Esse é o conjunto de vértices da estrela.
            self._coletavel_lista_poligono = [
                [self._pos_x+0, self._pos_y+4, 0, 0],
                [self._pos_x+5, self._pos_y+4, 0, 0],
                [self._pos_x+7, self._pos_y+0, 0, 0],
                [self._pos_x+8, self._pos_y+0, 0, 0],
                [self._pos_x+10, self._pos_y+4, 0, 0],
                [self._pos_x+15, self._pos_y+4, 0, 0],
                [self._pos_x+12, self._pos_y+8, 0, 0],
                [self._pos_x+12, self._pos_y+9, 0, 0],
                [self._pos_x+15, self._pos_y+15, 0, 0],
                [self._pos_x+8, self._pos_y+12, 0, 0],
                [self._pos_x+7, self._pos_y+12, 0, 0],
                [self._pos_x+0, self._pos_y+15, 0, 0],
                [self._pos_x+4, self._pos_y+9, 0, 0],
                [self._pos_x+4, self._pos_y+8, 0, 0],
            ]
        else:
            # Se já coletou, não renderiza.
            self._coletavel_lista_poligono = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]
        # Instancio
        self._coletavel_poligono_objeto = Poligono(self._coletavel_lista_poligono)

        # Esse coletável pode ter uma rotação
        self._rotacao = rotacao

        # E rotaciono. Se não tiver rotação, essa função abaixo faz nada.
        self.__rotacionar_em_torno_do_eixo()

    def get_coletavel_lista_poligono(self):
        return self._coletavel_lista_poligono
    
    def get_coletavel_poligono_objeto(self):
        return self._coletavel_poligono_objeto
    
    def set_visivel(self, visivel: bool):
        self._visivel = visivel
    
    def __rotacionar_em_torno_do_eixo(self):
        acumulo = Poligono.mover_poligono(-self._pos_x-8, -self._pos_y-8)
        acumulo = Poligono.rotacionar_poligono(self._rotacao, acumulo)
        acumulo = Poligono.mover_poligono(+self._pos_x+8, +self._pos_y+8, acumulo)
        self._coletavel_poligono_objeto.aplicar_transformacao_com_acumulos(acumulo)

    # Esse método não precisa de instância. Ele é um factory, devolve um objeto já tratado do coletável,
    # pois há a possibilidade dele já ter sido coletado, e portanto não pode ser renderizado.
    @staticmethod
    def inserir_coletavel(id, pos_x, pos_y, rotacao, player_objeto, estrelas_coletadas):
        player_pos_x, player_pos_y = player_objeto.get_posicao()  
        if pos_x-8 < player_pos_x < pos_x+24 and pos_y-8 < player_pos_y < pos_y+24 and f"coletavel_{id}" not in estrelas_coletadas:
            estrelas_coletadas.append(f"coletavel_{id}")
        if f"coletavel_{id}" not in estrelas_coletadas:
            return Coletavel(pos_x, pos_y, 0, rotacao)
        else:
            return Coletavel(0, 0, 0, rotacao, False)
