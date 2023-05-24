from desenho import Desenho
from screen import *

def desenha_titulo(desenhar_na_screen):
    desenha_super(desenhar_na_screen)
    desenha_dude(desenhar_na_screen)
    desenha_world(desenhar_na_screen)
    desenha_jogar(desenhar_na_screen)
    desenha_sair(desenhar_na_screen)

    desenhar_na_screen.elipse(128,75, 60, 100, Color(0,0,0,0))
    # Floodfill da elipse
    desenhar_na_screen.flood_fill_iterativo(125, 75, Color(170,220,255))

    # Floodfill das partes internas das letras (NÃO MEXER)
    desenhar_na_screen.flood_fill_iterativo(127, 39, Color(170,220,255))
    desenhar_na_screen.flood_fill_iterativo(164, 39, Color(170,220,255))

    desenhar_na_screen.flood_fill_iterativo(51, 77, Color(170,220,255))
    desenhar_na_screen.flood_fill_iterativo(87, 77, Color(170,220,255))
    
    desenhar_na_screen.flood_fill_iterativo(155, 75, Color(170,220,255))
    desenhar_na_screen.flood_fill_iterativo(174, 75, Color(170,220,255))
    desenhar_na_screen.flood_fill_iterativo(207, 77, Color(170,220,255))



def desenha_super(desenhar_na_screen):
    s = TitleScreen.letra_s(82,30)
    desenhar_na_screen.desenha_poligono(s, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(83, 31, Color(255,58,58))

    u = TitleScreen.letra_u(100, 30)
    desenhar_na_screen.desenha_poligono(u, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(101, 31, Color(0,222,255))

    p_e, p_i = TitleScreen.letra_p(118, 30)
    desenhar_na_screen.desenha_poligono(p_e, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(p_i, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(119, 31, Color(255,206,41))

    e = TitleScreen.letra_e(136, 30)
    desenhar_na_screen.desenha_poligono(e, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(137, 31, Color(0,222,255))

    r_e, r_i = TitleScreen.letra_r(154, 30)
    desenhar_na_screen.desenha_poligono(r_e, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(r_i, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(155, 31, Color(0,206,0))


def desenha_dude(desenhar_na_screen):
    d_e_1, d_i_1 = TitleScreen.letra_d(42, 66)
    desenhar_na_screen.desenha_poligono(d_e_1, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(d_i_1, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(43, 67, Color(0,222,255))
    
    u = TitleScreen.letra_u(60, 66)
    desenhar_na_screen.desenha_poligono(u, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(61, 67, Color(0,206,0))
    
    d_e_2, d_i_2 = TitleScreen.letra_d(78, 66)
    desenhar_na_screen.desenha_poligono(d_e_2, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(d_i_2, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(79, 67, Color(255,58,58))
    
    e = TitleScreen.letra_e(96,66)
    desenhar_na_screen.desenha_poligono(e, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(97, 67, Color(255,206,41))


def desenha_world(desenhar_na_screen):
    w = TitleScreen.letra_w(128, 66)
    desenhar_na_screen.desenha_poligono(w, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(129, 67, Color(255,206,41))
    
    o_e, o_i = TitleScreen.letra_o(146, 66)
    desenhar_na_screen.desenha_poligono(o_e, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(o_i, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(147, 67, Color(0,222,255))

    r_e, r_i = TitleScreen.letra_r(164, 66)
    desenhar_na_screen.desenha_poligono(r_e, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(r_i, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(165, 67, Color(0,206,0))
    
    l = TitleScreen.letra_l(182,66)
    desenhar_na_screen.desenha_poligono(l, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(183, 67, Color(255,58,58))

    d_e_2, d_i_2 = TitleScreen.letra_d(198, 66)
    desenhar_na_screen.desenha_poligono(d_e_2, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(d_i_2, Color(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(199, 67, Color(0,206,0))

def desenha_jogar(desenhar_na_screen):
    j = Letra.letra_j(100,150)
    desenhar_na_screen.desenha_poligono(j, Color(0,0,0,0))

    o_e, o_i = Letra.letra_o(108,150)
    desenhar_na_screen.desenha_poligono(o_e, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(o_i, Color(0,0,0,0))

    g = Letra.letra_g(116, 150)
    desenhar_na_screen.desenha_poligono(g, Color(0,0,0,0))

    a_e, a_i = Letra.letra_a(124, 150)
    desenhar_na_screen.desenha_poligono(a_e, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(a_i, Color(0,0,0,0))

    r_e, r_i = Letra.letra_r(132, 150)
    desenhar_na_screen.desenha_poligono(r_e, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(r_i, Color(0,0,0,0))

def desenha_sair(desenhar_na_screen):
    s = Letra.letra_s(100, 166)
    desenhar_na_screen.desenha_poligono(s, Color(0,0,0,0))
    
    a_e, a_i = Letra.letra_a(108, 166)
    desenhar_na_screen.desenha_poligono(a_e, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(a_i, Color(0,0,0,0))

    i = Letra.letra_i(116, 166)
    desenhar_na_screen.desenha_poligono(i, Color(0,0,0,0))

    r_e, r_i = Letra.letra_r(120, 166)
    desenhar_na_screen.desenha_poligono(r_e, Color(0,0,0,0))
    desenhar_na_screen.desenha_poligono(r_i, Color(0,0,0,0))


class TitleScreen:

    @staticmethod
    def letra_d(x_origem, y_origem):
        lista_poligono_externo = [
            [x_origem, y_origem, 0,0],
            [x_origem+14, y_origem, 0,0],
            [x_origem+14, y_origem+2, 0,0],
            [x_origem+16, y_origem+2, 0,0],
            [x_origem+16, y_origem+30, 0,0],
            [x_origem+14, y_origem+30, 0,0],
            [x_origem+14, y_origem+32, 0,0],
            [x_origem, y_origem+32, 0,0],
        ]

        lista_poligono_interno = [
            [x_origem+6, y_origem+6, 0,0],
            [x_origem+8, y_origem+6, 0,0],
            [x_origem+8, y_origem+8, 0,0],
            [x_origem+10, y_origem+8, 0,0],
            [x_origem+10, y_origem+24, 0,0],
            [x_origem+8, y_origem+24, 0,0],
            [x_origem+8, y_origem+26, 0,0],
            [x_origem+6, y_origem+26, 0,0],
        ]
        return lista_poligono_externo, lista_poligono_interno

    @staticmethod
    def letra_e(x_origem, y_origem):
        lista_poligono = [
            [x_origem, y_origem, 0,0],
            [x_origem+16, y_origem, 0,0],
            [x_origem+16, y_origem+6, 0,0],
            [x_origem+6, y_origem+6, 0,0],
            [x_origem+6, y_origem+12, 0,0],
            [x_origem+12, y_origem+12, 0,0],
            [x_origem+12, y_origem+18, 0,0],
            [x_origem+6, y_origem+18, 0,0],
            [x_origem+6, y_origem+24, 0,0],
            [x_origem+16, y_origem+24, 0,0],
            [x_origem+16, y_origem+32, 0,0],
            [x_origem, y_origem+32, 0,0],
        ]
        return lista_poligono

    @staticmethod
    def letra_l(x_origem, y_origem):
        lista_poligono = [
            [x_origem, y_origem, 0,0],
            [x_origem+6, y_origem, 0,0],
            [x_origem+6, y_origem+26, 0,0],
            [x_origem+16, y_origem+26, 0,0],
            [x_origem+16, y_origem+32, 0,0],
            [x_origem, y_origem+32, 0,0],
        ]
        return lista_poligono

    @staticmethod
    def letra_o(x_origem, y_origem):
        lista_poligono_externo = [
            [x_origem, y_origem, 0,0],
            [x_origem+16, y_origem, 0,0],
            [x_origem+16, y_origem+32, 0,0],
            [x_origem, y_origem+32, 0,0],
        ]
        lista_poligono_interno = [
            [x_origem+6, y_origem+6, 0,0],
            [x_origem+10, y_origem+6, 0,0],
            [x_origem+10, y_origem+26, 0,0],
            [x_origem+6, y_origem+26, 0,0],
        ]
        return lista_poligono_externo, lista_poligono_interno

    @staticmethod
    def letra_p(x_origem, y_origem):
        lista_poligono_externo = [
            [x_origem, y_origem, 0,0],
            [x_origem+16, y_origem, 0,0],
            [x_origem+16, y_origem+16, 0,0],
            [x_origem+6, y_origem+16, 0,0],
            [x_origem+6, y_origem+32, 0,0],
            [x_origem+0, y_origem+32, 0,0],
        ]

        lista_poligono_interno = [
            [x_origem+6, y_origem+6, 0,0],
            [x_origem+12, y_origem+6, 0,0],
            [x_origem+12, y_origem+10, 0,0],
            [x_origem+6, y_origem+10, 0,0],
        ]
        return lista_poligono_externo, lista_poligono_interno
    

    @staticmethod
    def letra_r(x_origem, y_origem):
        lista_poligono_externo = [
            [x_origem, y_origem, 0,0],
            [x_origem+16, y_origem, 0,0],
            [x_origem+16, y_origem+16, 0,0],
            [x_origem+13, y_origem+16, 0,0],
            [x_origem+16, y_origem+32, 0,0],
            [x_origem+10, y_origem+32, 0,0],
            [x_origem+8, y_origem+16, 0,0],
            [x_origem+6, y_origem+16, 0,0],
            [x_origem+6, y_origem+32, 0,0],
            [x_origem, y_origem+32, 0,0],
        ]

        lista_poligono_interno = [
            [x_origem+6, y_origem+6, 0,0],
            [x_origem+12, y_origem+6, 0,0],
            [x_origem+12, y_origem+10, 0,0],
            [x_origem+6, y_origem+10, 0,0],
        ]
        return lista_poligono_externo, lista_poligono_interno
    

    @staticmethod
    def letra_s(x_origem, y_origem):
        lista_poligono = [
            [x_origem, y_origem, 0, 0],
            [x_origem+16, y_origem, 0, 0],
            [x_origem+16, y_origem+8, 0, 0],
            [x_origem+4, y_origem+8, 0, 0],
            [x_origem+4, y_origem+12, 0, 0],
            [x_origem+16, y_origem+12, 0, 0],
            [x_origem+16, y_origem+32, 0, 0],
            [x_origem+0, y_origem+32, 0, 0],
            [x_origem+0, y_origem+24, 0, 0],
            [x_origem+12, y_origem+24, 0, 0],
            [x_origem+12, y_origem+20, 0, 0],
            [x_origem+0, y_origem+20, 0, 0],
        ]
        return lista_poligono
    @staticmethod
    def letra_u(x_origem, y_origem):
        lista_poligono = [
            [x_origem, y_origem, 0, 0],
            [x_origem+6, y_origem, 0, 0],
            [x_origem+6, y_origem+24, 0, 0],
            [x_origem+10, y_origem+24, 0, 0],
            [x_origem+10, y_origem, 0, 0],
            [x_origem+16, y_origem, 0, 0],
            [x_origem+16, y_origem+32, 0, 0],
            [x_origem, y_origem+32, 0, 0],
        ]
        return lista_poligono
    
    @staticmethod
    def letra_w(x_origem, y_origem):
        lista_poligono = [
            [x_origem, y_origem, 0, 0],
            [x_origem+4, y_origem, 0, 0],
            [x_origem+6, y_origem+20, 0, 0],
            [x_origem+8, y_origem+14, 0, 0],
            [x_origem+10, y_origem+20, 0, 0],
            [x_origem+12, y_origem, 0, 0],
            [x_origem+16, y_origem, 0, 0],
            [x_origem+14, y_origem+32, 0, 0],
            [x_origem+10, y_origem+32, 0, 0],
            [x_origem+8, y_origem+28, 0, 0],
            [x_origem+6, y_origem+32, 0, 0],
            [x_origem+2, y_origem+32, 0, 0],
        ]
        return lista_poligono
    

class Letra:

    @staticmethod
    def letra_a(x_origem, y_origem):
        lista_poligono_externo = [
            [x_origem+1, y_origem, 0, 0],
            [x_origem+6, y_origem, 0, 0],
            [x_origem+7, y_origem+1, 0, 0],
            [x_origem+7, y_origem+7, 0, 0],
            [x_origem+4, y_origem+7, 0, 0],
            [x_origem+4, y_origem+5, 0, 0],
            [x_origem+3, y_origem+5, 0, 0],
            [x_origem+3, y_origem+7, 0, 0],
            [x_origem+0, y_origem+7, 0, 0],
            [x_origem+0, y_origem+1, 0, 0],
        ]
        lista_poligono_interno = [
            [x_origem+3, y_origem+2, 0, 0],
            [x_origem+4, y_origem+2, 0, 0],
            [x_origem+4, y_origem+3, 0, 0],
            [x_origem+3, y_origem+3, 0, 0],
        ]
        return lista_poligono_externo, lista_poligono_interno


    def letra_g(x_origem, y_origem):
        lista_poligono = [
            [x_origem+1, y_origem, 0, 0],
            [x_origem+6, y_origem, 0, 0],
            [x_origem+7, y_origem+1, 0, 0],
            [x_origem+7, y_origem+3, 0, 0],
            [x_origem+4, y_origem+3, 0, 0],
            [x_origem+4, y_origem+2, 0, 0],
            [x_origem+3, y_origem+2, 0, 0],
            [x_origem+3, y_origem+5, 0, 0],
            [x_origem+4, y_origem+5, 0, 0],
            [x_origem+3, y_origem+5, 0, 0],
            [x_origem+3, y_origem+3, 0, 0],
            [x_origem+7, y_origem+3, 0, 0],
            [x_origem+7, y_origem+6, 0, 0],
            [x_origem+6, y_origem+7, 0, 0],
            [x_origem+1, y_origem+7, 0, 0],
            [x_origem+0, y_origem+6, 0, 0],
            [x_origem+0, y_origem+1, 0, 0],
        ]
        return lista_poligono
    
    @staticmethod
    def letra_i(x_origem, y_origem):
        lista_poligono = [
            [x_origem, y_origem, 0,0],
            [x_origem+3, y_origem, 0,0],
            [x_origem+3, y_origem+7, 0,0],
            [x_origem, y_origem+7, 0,0],
        ]
        return lista_poligono

    @staticmethod
    def letra_j(x_origem, y_origem):
        lista_poligono = [
            [x_origem+4, y_origem, 0, 0],
            [x_origem+7, y_origem, 0, 0],
            [x_origem+7, y_origem+5, 0, 0],
            [x_origem+5, y_origem+7, 0, 0],
            [x_origem+2, y_origem+7, 0, 0],
            [x_origem, y_origem+5, 0, 0],
            [x_origem, y_origem+3, 0, 0],
            [x_origem+3, y_origem+3, 0, 0],
            [x_origem+3, y_origem+5, 0, 0],
            [x_origem+4, y_origem+5, 0, 0],
        ]
        return lista_poligono
    
    @staticmethod
    def letra_o(x_origem, y_origem):
        lista_poligono_externo = [
            [x_origem+2, y_origem, 0, 0],
            [x_origem+5, y_origem, 0, 0],
            [x_origem+7, y_origem+2, 0, 0],
            [x_origem+7, y_origem+5, 0, 0],
            [x_origem+5, y_origem+7, 0, 0],
            [x_origem+2, y_origem+7, 0, 0],
            [x_origem, y_origem+5, 0, 0],
            [x_origem, y_origem+2, 0, 0],
        ]

        lista_poligono_interno = [
            [x_origem+3, y_origem+2],
            [x_origem+4, y_origem+2],
            [x_origem+4, y_origem+5],
            [x_origem+3, y_origem+5],
        ]
        return lista_poligono_externo, lista_poligono_interno
    
    @staticmethod
    def letra_r(x_origem, y_origem):
        lista_poligono_externo = [
            [x_origem, y_origem, 0, 0],
            [x_origem+5, y_origem, 0, 0],
            [x_origem+7, y_origem+2, 0, 0],
            [x_origem+7, y_origem+3, 0, 0],
            [x_origem+6, y_origem+4, 0, 0],
            [x_origem+7, y_origem+5, 0, 0],
            [x_origem+7, y_origem+7, 0, 0],
            [x_origem+4, y_origem+7, 0, 0],
            [x_origem+4, y_origem+5, 0, 0],
            [x_origem+3, y_origem+5, 0, 0],
            [x_origem+3, y_origem+7, 0, 0],
            [x_origem+0, y_origem+7, 0, 0],
        ]

        lista_poligono_interno = [
            [x_origem+3, y_origem+2, 0, 0],
            [x_origem+4, y_origem+2, 0, 0],
            [x_origem+4, y_origem+3, 0, 0],
            [x_origem+3, y_origem+3, 0, 0],
        ]
        return lista_poligono_externo, lista_poligono_interno
    
    @staticmethod
    def letra_s(x_origem, y_origem):
        lista_poligono = [
            [x_origem+1, y_origem, 0, 0],
            [x_origem+6, y_origem, 0, 0],
            [x_origem+7, y_origem+1, 0, 0],
            [x_origem+7, y_origem+2, 0, 0],
            [x_origem+3, y_origem+2, 0, 0],
            [x_origem+7, y_origem+2, 0, 0],
            [x_origem+7, y_origem+6, 0, 0],
            [x_origem+6, y_origem+7, 0, 0],
            [x_origem+1, y_origem+7, 0, 0],
            [x_origem+0, y_origem+6, 0, 0],
            [x_origem+0, y_origem+5, 0, 0],
            [x_origem+4, y_origem+5, 0, 0],
            [x_origem+4, y_origem+4, 0, 0],
            [x_origem+0, y_origem+4, 0, 0],
            [x_origem+0, y_origem+1, 0, 0],
        ]
        return lista_poligono