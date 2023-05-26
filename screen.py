import pygame
from poligono import *
from desenho import Color

class Screen:
    # Construtor da classe Screen
    def __init__(self, width, height, background_color):
        self.__screen_matrix = []
        for i in range(height):
            self.__screen_matrix.append([0]*width)
        self.__background_color = background_color
        self.__width = width
        self.__height = height
        self.__screen = pygame.display.set_mode(
            (self.__width, self.__height), pygame.RESIZABLE)

    # Método que eu pego a screen para que eu possa fazer alterações nela na main caso eu deseje.

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_screen(self):
        return self.__screen

    # Esse método serve para tratar coordenadas que podem ser maiores que o tamanho
    # da matriz. Portanto, em C++, acessaria lixo na mémória. O set_at do python
    # da lib pygame também deve tratar, mas por precaução, estou fazendo aqui
    # também, como forma didática.

    def get_pixel(self, x, y):
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x >= self.__screen.get_width():
            x = self.__screen.get_width()-1
        if y >= self.__screen.get_height():
            y = self.__screen.get_height()-1

        return self.__screen.get_at((x, y))

    def set_pixel(self, x, y, color):

        # Se as coordenadas forem negativas, passam a ser no minimo zero.
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        # Truncamento de x e y. Se for maior que o tamanho da matriz, vira as
        # coordenadas do tamanho da matriz.
        if x >= self.__screen.get_width():
            x = self.__screen.get_width()-1
        if y >= self.__screen.get_height():
            y = self.__screen.get_height()-1

        # Setpixel definitivo
        self.__screen.set_at((x, y), color.get_rgba())

    # Desenha uma senóide na matriz. O problema é que ela só itera em x, e quando
    # vai desenhar em y, pontos desenhados no mesmo x não é possível.


    # Daqui pra frente são métodos padrões da própria classe do pygame.

    def clear_screen(self):
        self.__screen.fill(self.__background_color.get_rgba())

    @staticmethod
    def update():
        pygame.display.update()


class Viewport:
    def __init__(self, x_inicial, y_inical, x_final, y_final ,conjunto_poligonos=None) -> None:
        if conjunto_poligonos == None:
            conjunto_poligonos = []
        self._conjunto_poligonos = conjunto_poligonos
        self._conjunto_poligonos_cortados = []
        self._conjunto_poligonos_cores = []
        self._x_inicial = x_inicial
        self._y_inicial = y_inical
        self._largura = x_final-x_inicial
        self._altura = y_final-y_inical

    def get_conjunto_poligonos_cortados(self, indice=0):
        return self._conjunto_poligonos_cortados[indice]

    def get_conjunto_poligonos_cortados_sem_indice(self):
        return self._conjunto_poligonos_cortados

    def get_conjunto_poligonos_cores(self, indice=0):
        return self._conjunto_poligonos_cores[indice]

    def __intersecao_em_x(self, scan, pi, pf):
        xi, yi = pi
        xf, yf = pf
        if xi == xf:
            return -1, -1
        if xi < xf:
            yi, yf = yf, yi
            xi, xf = xf, xi

        if (xf - xi) == 0:
            return -1, -1

        t = (scan - xf)/(xi - xf)

        if 1 >= t >= 0:
            poly = yf + t*(yi - yf)
            return poly, t
        else:
            return -1, t

    def __intersecao_em_y(self, scan, pi, pf):
        xi, yi = pi
        xf, yf = pf
        if yi == yf:
            return -1, -1
        if yi < yf:
            aux = yi
            yi = yf
            yf = aux
            aux = xi
            xi = xf
            xf = aux

        if (yf - yi) == 0:
            return -1, -1

        t = (scan - yf)/(yi - yf)

        if 1 >= t >= 0:
            polx = xf + t*(xi - xf)
            return polx, t
        else:
            return -1, t

    def __corta_aresta(self, aresta, corte, axis, cor1, cor2, bin1, bin2):
        pi, pf = aresta
        xi, yi = pi
        xf, yf = pf

        if axis == 'y':
            par, t = self.__intersecao_em_x(corte, pi, pf)
            if xf > xi:
                t = 1 - t
            if t > 1 or t < 0:
                if corte == self._largura + self._x_inicial and bin1[1] == '1':
                    return ((-1, -1), (-1, -1)), -1, -1
                elif corte == self._x_inicial and bin1[3] == '1':
                    return ((-1, -1), (-1, -1)), -1, -1
                else:
                    return (pi, pf), (bin1, bin2), (cor1, cor2)
            if len(cor1) == 2:
                s1, t1 = cor1
                s2, t2 = cor2
                s = s1 * t + s2 * (1 - t)
                t = t1 * t + t2 * (1 - t)
                cor = (s, t)
            else:
                r1, g1, b1, a1 = cor1
                r2, g2, b2, a2 = cor2
                r = r1 * t + r2 * (1 - t)
                g = g1 * t + g2 * (1 - t)
                b = b1 * t + b2 * (1 - t)
                cor = (r, g, b, a1)
            if corte == self._largura + self._x_inicial:
                if bin1[1] == '1':
                    a, b, c, d = bin1
                    return ((corte, par), pf), ((a, '0', c, d), bin2), (cor, cor2)
                else:
                    a, b, c, d = bin2
                    return (pi, (corte, par)), (bin1, (a, '0', c, d)), (cor1, cor)
            if corte == self._x_inicial:
                if bin1[3] == '1':
                    a, b, c, d = bin1
                    return ((corte, par), pf), ((a, b, c, '0'), bin2), (cor, cor2)
                else:
                    a, b, c, d = bin2
                    return (pi, (corte, par)), (bin1, (a, b, c, '0')), (cor1, cor)
        else:
            par, t = self.__intersecao_em_y(corte, pi, pf)
            if yf > yi:
                t = 1 - t
            if t > 1 or t < 0:
                if corte == self._altura + self._y_inicial and bin1[0] == '1':
                    return ((-1, -1), (-1, -1)), -1, -1
                elif corte == self._y_inicial and bin1[2] == '1':
                    return ((-1, -1), (-1, -1)), -1, -1
                else:
                    return (pi, pf), (bin1, bin2), (cor1, cor2)
            if len(cor1) == 2:
                s1, t1 = cor1
                s2, t2 = cor2
                s = s1 * t + s2 * (1 - t)
                t = t1 * t + t2 * (1 - t)
                cor = (s, t)
            else:
                r1, g1, b1, a1 = cor1
                r2, g2, b2, a2 = cor2
                r = r1 * t + r2 * (1 - t)
                g = g1 * t + g2 * (1 - t)
                b = b1 * t + b2 * (1 - t)
                cor = (r, g, b, a1)
            if corte == self._altura + self._y_inicial:
                if bin1[0] == '1':
                    a, b, c, d = bin1
                    return ((par, corte), pf), (('0', b, c, d), bin2), (cor, cor2)
                else:
                    a, b, c, d = bin2
                    return (pi, (par, corte)), (bin1, ('0', b, c, d)), (cor1, cor)
            if corte == self._y_inicial:
                if bin1[2] == '1':
                    a, b, c, d = bin1
                    return ((par, corte), pf), ((a, b, '0', d), bin2), (cor, cor2)
                else:
                    a, b, c, d = bin2
                    return (pi, (par, corte)), (bin1, (a, b, '0', d)), (cor1, cor)

    def __calcula_bin(self, ponto):
        px, py = ponto
        ba = '0'
        bb = '0'
        bc = '0'
        bd = '0'
        if px < self._x_inicial:
            bd = '1'
        elif px > self._largura + self._x_inicial:
            bb = '1'
        if py < self._y_inicial:
            bc = '1'
        elif py > self._altura + self._y_inicial:
            ba = '1'
        return ba, bb, bc, bd

    def update_viewport(self, scanline_color=None):
        self._conjunto_poligonos_cores = []
        self._conjunto_poligonos_cortados = []
        loop_tuple = (self._altura + self._y_inicial, self._largura + self._x_inicial, self._y_inicial, self._x_inicial)
        polbin = []

        for index, pol in enumerate(self._conjunto_poligonos):
            arestas = []
            polbin = []
            lista_vertices = [(linha[0], linha[1]) for linha in pol.lista_poligono_mapeado]
            for vertice in range(len(lista_vertices)):
                if vertice > 0:
                    arestas.append((lista_vertices[vertice - 1], lista_vertices[vertice]))
                    if vertice == len(lista_vertices) - 1:
                        arestas.append((lista_vertices[vertice], lista_vertices[0]))
                polbin.append(self.__calcula_bin(lista_vertices[vertice]))

            if len(scanline_color[index]) == 0:
                preenchimento = [(linha[2], linha[3]) for linha in pol.lista_poligono_customizado]
            else:
                preenchimento = []
                for i in range(len(scanline_color[index])):
                    preenchimento.append(scanline_color[index][i].get_rgba())

            polcores = preenchimento
            tempcores = []
            tempbin = []
            tempar = []
            for inter in range(len(loop_tuple)):
                if inter % 2 == 0:
                    axis = 'x'
                else:
                    axis = 'y'
                for a in range(len(arestas)):
                    if a == len(arestas) - 1:
                        ar, bins, cores = self.__corta_aresta(arestas[a], loop_tuple[inter], axis, polcores[a],
                                                            polcores[0], polbin[a], polbin[0])
                    else:
                        ar, bins, cores = self.__corta_aresta(arestas[a], loop_tuple[inter], axis, polcores[a],
                                                            polcores[a+1], polbin[a], polbin[a+1])
                    xp, yp = ar
                    xpi, ypi = xp
                    if xpi != -1 and xp != yp:
                        tempar.append(ar)
                        tempbin.append(bins)
                        tempcores.append(cores)
                arestas = []
                if not tempar or len(tempar) == 1:
                    break
                polbin = []
                polcores = []
                arestas.append(tempar[0])
                bin1, bin2 = tempbin[0]
                polbin.append(bin1)
                cor1, cor2 = tempcores[0]
                polcores.append(cor1)
                for a in range(len(tempar)):
                    pi, pf = tempar[a]
                    xf, yf = pf
                    bin1, bin2 = tempbin[a]
                    cor1, cor2 = tempcores[a]
                    if a == len(tempar) - 1:
                        xpi, xpf = tempar[0]
                    else:
                        xpi, xpf = tempar[a+1]
                    xxpi, yxpi = xpi
                    if xf != xxpi or yf != yxpi:
                        arestas.append(((xf, yf), (xxpi, yxpi)))
                        polbin.append(bin2)
                        polcores.append(cor2)
                    if a != len(tempar) - 1:
                        arestas.append(tempar[a + 1])
                        bin1, bin2 = tempbin[a + 1]
                        cor1, cor2 = tempcores[a + 1]
                        polbin.append(bin1)
                        polcores.append(cor1)
                tempar = []
                tempbin = []
                tempcores = []
            newpol = Poligono()

            if arestas:
                matriz_cores = []
                for a in range(len(arestas)):
                    pi, pf = arestas[a]
                    xi, yi = pi
                    if xi < 0 or yi < 0:
                        if a == len(arestas)-1:
                            break
                        a += 1
                        pi, pf = arestas[a]
                        xi, yi = pi
                        
                    if len(polcores[a]) == 2:
                        self._conjunto_poligonos_cores.append([])
                        tx, ty = polcores[a]
                        newpol.insere_ponto(round(xi), round(yi), tx, ty)
                    else:
                        r, g, b, alpha = polcores[a]
                        matriz_cores.append(Color(r, g, b, alpha))
                        newpol.insere_ponto(round(xi), round(yi), 0, 0)
                        if a == len(arestas)-1:
                            self._conjunto_poligonos_cores.append(matriz_cores)

            self._conjunto_poligonos_cortados.append(newpol)

class PilhaMapeamentos:
    def __init__(self, janela, viewport, lista_de_mapeamentos=None, lista_de_cores=None, lista_de_arestas=None) -> None:
        self._janela = janela
        self._viewport = viewport

        if lista_de_mapeamentos == None:
            lista_de_mapeamentos = []
        self._lista_de_mapeamentos = lista_de_mapeamentos

        if lista_de_cores == None:
            lista_de_cores = []
        self._lista_de_cores = lista_de_cores

        if lista_de_arestas == None:
            lista_de_arestas = []
        self._lista_de_arestas = lista_de_arestas

    @property
    def janela(self):
        return self._janela

    @property
    def viewport(self):
        return self._viewport

    @property
    def lista_de_mapeamentos(self):
        return self._lista_de_mapeamentos
    
    @property
    def lista_de_cores(self):
        return self._lista_de_cores
    
    @property
    def lista_de_arestas(self):
        return self._lista_de_arestas