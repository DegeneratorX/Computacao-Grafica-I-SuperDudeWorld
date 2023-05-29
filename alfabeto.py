from screen import *

# Toda a tela inicial foi desenhada no BRAÇO. Nada de textura. Tudo é polígono, incluindo as letras, grandes e miúdas.
def desenha_titulo(desenhar_na_screen):

    # Separei em subrotinas pq tava muito grande isso aqui. Cada letra tem seu polígono.
    desenha_super(desenhar_na_screen)
    desenha_dude(desenhar_na_screen)
    desenha_world(desenhar_na_screen)
    desenha_jogar(desenhar_na_screen)
    desenha_sair(desenhar_na_screen)

    # Desenho da elipse
    desenhar_na_screen.elipse(128,75, 60, 100, Cor(0,0,0,0))
    # Floodfill da elipse
    desenhar_na_screen.flood_fill_iterativo(125, 75, Cor(170,220,255))

    # Floodfill das partes internas das letras (NÃO MEXER)
    # A parte interna são aqueles buracos que existem internamente na letra, como na leta A, D, P, O...
    desenhar_na_screen.flood_fill_iterativo(127, 39, Cor(170,220,255))
    desenhar_na_screen.flood_fill_iterativo(164, 39, Cor(170,220,255))

    desenhar_na_screen.flood_fill_iterativo(51, 77, Cor(170,220,255))
    desenhar_na_screen.flood_fill_iterativo(87, 77, Cor(170,220,255))
    
    desenhar_na_screen.flood_fill_iterativo(155, 75, Cor(170,220,255))
    desenhar_na_screen.flood_fill_iterativo(174, 75, Cor(170,220,255))
    desenhar_na_screen.flood_fill_iterativo(207, 77, Cor(170,220,255))


def desenha_super(desenhar_na_screen):
    # TitleScreen é uma classe que lida com estrutura de dados dos polígonos que formam as letras do titulo do jogo
    s = LetraTelaInicial.letra_s(82,30)
    desenhar_na_screen.desenha_poligono(s, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(83, 31, Cor(255,58,58))

    u = LetraTelaInicial.letra_u(100, 30)
    desenhar_na_screen.desenha_poligono(u, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(101, 31, Cor(0,222,255))

    p_e, p_i = LetraTelaInicial.letra_p(118, 30)
    desenhar_na_screen.desenha_poligono(p_e, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(p_i, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(119, 31, Cor(255,206,41))

    e = LetraTelaInicial.letra_e(136, 30)
    desenhar_na_screen.desenha_poligono(e, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(137, 31, Cor(0,222,255))

    r_e, r_i = LetraTelaInicial.letra_r(154, 30)
    desenhar_na_screen.desenha_poligono(r_e, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(r_i, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(155, 31, Cor(0,206,0))


def desenha_dude(desenhar_na_screen):
    d_e_1, d_i_1 = LetraTelaInicial.letra_d(42, 66)
    desenhar_na_screen.desenha_poligono(d_e_1, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(d_i_1, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(43, 67, Cor(0,222,255))
    
    u = LetraTelaInicial.letra_u(60, 66)
    desenhar_na_screen.desenha_poligono(u, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(61, 67, Cor(0,206,0))
    
    d_e_2, d_i_2 = LetraTelaInicial.letra_d(78, 66)
    desenhar_na_screen.desenha_poligono(d_e_2, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(d_i_2, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(79, 67, Cor(255,58,58))
    
    e = LetraTelaInicial.letra_e(96,66)
    desenhar_na_screen.desenha_poligono(e, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(97, 67, Cor(255,206,41))


def desenha_world(desenhar_na_screen):
    w = LetraTelaInicial.letra_w(128, 66)
    desenhar_na_screen.desenha_poligono(w, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(129, 67, Cor(255,206,41))
    
    o_e, o_i = LetraTelaInicial.letra_o(146, 66)
    desenhar_na_screen.desenha_poligono(o_e, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(o_i, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(147, 67, Cor(0,222,255))

    r_e, r_i = LetraTelaInicial.letra_r(164, 66)
    desenhar_na_screen.desenha_poligono(r_e, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(r_i, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(165, 67, Cor(0,206,0))
    
    l = LetraTelaInicial.letra_l(182,66)
    desenhar_na_screen.desenha_poligono(l, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(183, 67, Cor(255,58,58))

    d_e_2, d_i_2 = LetraTelaInicial.letra_d(198, 66)
    desenhar_na_screen.desenha_poligono(d_e_2, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(d_i_2, Cor(0,0,0,0))
    desenhar_na_screen.flood_fill_iterativo(199, 67, Cor(0,206,0))

def desenha_jogar(desenhar_na_screen):
    # Letra é uma classe que lida com as letras miúdas da tela de início do jogo, onde escolhe as opções
    j = LetraPequena.letra_j(100,150)
    desenhar_na_screen.desenha_poligono(j, Cor(0,0,0,0))

    o_e, o_i = LetraPequena.letra_o(108,150)
    desenhar_na_screen.desenha_poligono(o_e, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(o_i, Cor(0,0,0,0))

    g = LetraPequena.letra_g(116, 150)
    desenhar_na_screen.desenha_poligono(g, Cor(0,0,0,0))

    a_e, a_i = LetraPequena.letra_a(124, 150)
    desenhar_na_screen.desenha_poligono(a_e, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(a_i, Cor(0,0,0,0))

    r_e, r_i = LetraPequena.letra_r(132, 150)
    desenhar_na_screen.desenha_poligono(r_e, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(r_i, Cor(0,0,0,0))

def desenha_sair(desenhar_na_screen):
    s = LetraPequena.letra_s(100, 166)
    desenhar_na_screen.desenha_poligono(s, Cor(0,0,0,0))
    
    a_e, a_i = LetraPequena.letra_a(108, 166)
    desenhar_na_screen.desenha_poligono(a_e, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(a_i, Cor(0,0,0,0))

    i = LetraPequena.letra_i(116, 166)
    desenhar_na_screen.desenha_poligono(i, Cor(0,0,0,0))

    r_e, r_i = LetraPequena.letra_r(120, 166)
    desenhar_na_screen.desenha_poligono(r_e, Cor(0,0,0,0))
    desenhar_na_screen.desenha_poligono(r_i, Cor(0,0,0,0))

# TitleScreen é uma classe que lida com estrutura de dados dos polígonos que formam as letras do titulo do jogo
# Todas as letras são polígonos formados por uma estrutura de dados de vértices
class LetraTelaInicial:

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
    
# Letra é uma classe que lida com as letras miúdas da tela de início do jogo, onde escolhe as opções
# Todas as letras são polígonos formados por uma estrutura de dados de vértices
class LetraPequena:

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