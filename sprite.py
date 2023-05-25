import pygame
from pygame.locals import *
from abc import ABC
from poligono import *

class Sprite(ABC):
    def __init__(self, pos_x, pos_y, velocidade, gfx) -> None:
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._velocidade = velocidade
        self._gfx = gfx


class Player(Sprite):
    def __init__(self, pos_x, pos_y, velocidade, gfx) -> None:
        super().__init__(pos_x, pos_y, velocidade, gfx)
        self._player_sprite = [
            [self._pos_x-8,self._pos_y-8,0,0],
            [self._pos_x+8,self._pos_y-8,1,0],
            [self._pos_x+8,self._pos_y+8,1,1],
            [self._pos_x-8,self._pos_y+8,0,1],
        ]
        self._player_poligono_objeto = Poligono(self._player_sprite)
        self._direcao = "up"

    def get_position(self):
        return self._pos_x, self._pos_y

    def get_player_sprite(self):
        return self._player_sprite
    
    def get_player_poligono_objeto(self):
        return self._player_poligono_objeto

    def mover_janela_e_player(self, keys, janela):
        janela_x_inicial, janela_y_inicial, janela_x_final, janela_y_final = janela
        #print(F"COORDENADAS JANELA: {janela_x_inicial}, {janela_y_inicial}, {janela_x_final}, {janela_y_final}")
        print(f"COORDENADAS PLAYER: {self._pos_x}, {self._pos_y}")
        #print(self._velocidade)
        if keys[K_LEFT]:
            if self._direcao == "up":
                self.__rotacionar_em_torno_do_eixo(-90)
            elif self._direcao == "right":
                self.__rotacionar_em_torno_do_eixo(180)
            elif self._direcao == "down":
                self.__rotacionar_em_torno_do_eixo(90)
            elif self._direcao == "left":
                pass
            self._direcao = "left"

            acumulo = Poligono.mover_poligono(-self._velocidade, 0)
            self._player_poligono_objeto.aplicar_transformacao_com_acumulos(acumulo)
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

        return [janela_x_inicial, janela_y_inicial, janela_x_final, janela_y_final]
    
    def __rotacionar_em_torno_do_eixo(self, angulo):
        acumulo = Poligono.mover_poligono(-self._pos_x,-self._pos_y)
        acumulo = Poligono.rotacionar_poligono(angulo, acumulo, player=True)
        acumulo = Poligono.mover_poligono(+self._pos_x,+self._pos_y, acumulo)
        self._player_poligono_objeto.aplicar_transformacao_com_acumulos(acumulo)