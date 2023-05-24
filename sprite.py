import pygame
from pygame.locals import *

class Sprite:
    pass

class Player(Sprite):
    def __init__(self, origem_x, origem_y, velocidade) -> None:
        super().__init__()
        self._origem_x = origem_x
        self._origem_y = origem_y
        self._velocidade = velocidade
        self._player_sprite = [
            [self._origem_x-8,self._origem_y-8,0,0],
            [self._origem_x+8,self._origem_y-8,1,0],
            [self._origem_x+8,self._origem_y+8,1,1],
            [self._origem_x-8,self._origem_y+8,0,1],
        ]

    def get_player_sprite(self):
        return self._player_sprite

    def mover(self, keys, janela):
        janela_x_inicial, janela_y_inicial, janela_x_final, janela_y_final = janela
        print(F"COORDENADAS JANELA: {janela_x_inicial}, {janela_y_inicial}, {janela_x_final}, {janela_y_final}")
        print(f"COORDENADAS PLAYER: {self._origem_x}, {self._origem_y}")
        print(self._velocidade)
        if keys[K_LEFT]:
            self._origem_x -= self._velocidade
            janela_x_inicial -= self._velocidade
            janela_x_final -= self._velocidade
        if keys[K_RIGHT]:
            self._origem_x += self._velocidade
            janela_x_inicial += self._velocidade
            janela_x_final += self._velocidade
        if keys[K_UP]:
            self._origem_y -= self._velocidade
            janela_y_inicial -= self._velocidade
            janela_y_final -= self._velocidade
        if keys[K_DOWN]:
            self._origem_y += self._velocidade
            janela_y_inicial += self._velocidade
            janela_y_final += self._velocidade

        self._player_sprite = [
            [self._origem_x-8,self._origem_y-8,0,0],
            [self._origem_x+8,self._origem_y-8,1,0],
            [self._origem_x+8,self._origem_y+8,1,1],
            [self._origem_x-8,self._origem_y+8,0,1],
        ]

        return [janela_x_inicial, janela_y_inicial, janela_x_final, janela_y_final]