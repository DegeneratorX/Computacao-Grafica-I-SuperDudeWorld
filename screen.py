import pygame
from poligono import *
from desenho import Cor

class Tela:
    # Construtor da classe Tela
    def __init__(self, width, height):
        self.__largura = width
        self.__altura = height
        self.__screen = pygame.display.set_mode((self.__largura, self.__altura), pygame.RESIZABLE)

    def get_largura(self):
        return self.__largura

    def get_altura(self):
        return self.__altura

    # Pego diretamente o objeto instanciado da screen do pygame
    def get_pygame_screen(self):
        return self.__screen

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

    # set_pixel. Esse método serve para tratar coordenadas que podem ser maiores que o tamanho
    # da matriz de tela. Portanto, em C++, acessaria lixo na mémória. O set_at do python
    # do pygame também deve tratar, mas por precaução, estou fazendo aqui
    # também, como forma didática.
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


# Classe que trata dados da viewport e aplica o clipping nos polígonos a partir do conjunto de dados.
class Viewport:
    def __init__(self, x_inicial, y_inical, x_final, y_final, conjunto_poligonos=None) -> None:
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

    # Método de interseção para o clipping quando o clipping ocorre na esquerda ou direita da viewport.
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

    # Método de interseção para o clipping quando o clipping ocorre em cima ou embaixo da viewport.
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

    # Método que clipa uma única aresta na borda de uma viewport.
    def __corta_aresta(self, aresta, corte, axis, cor1, cor2, bin1, bin2):
        pi, pf = aresta
        xi, yi = pi
        xf, yf = pf

        if axis == 'y':  #Se o clipping for no eixo y...
            intersecao, t = self.__intersecao_em_x(corte, pi, pf)
            if xf > xi: # Ajusta o valor de t, pois t=1 quando a aresta tiver o maior valor no eixo (convenção)
                t = 1 - t
            if t > 1 or t < 0: # No caso de não ter intesecção com o segmento de reta...
                if corte == self._largura + self._x_inicial and bin1[1] == '1' and bin2[1] == '1': # ambos estão fora para a direita
                    return ((-1, -1), (-1, -1)), -1, -1
                elif corte == self._x_inicial and bin1[3] == '1' and bin2[3] == '1': # ambos estão fora para a esquerda
                    return ((-1, -1), (-1, -1)), -1, -1
                else:
                    return (pi, pf), (bin1, bin2), (cor1, cor2) # ambos estão dentro da janela
            if len(cor1) == 2: # se forem coordenadas de textura, interpolar
                s1, t1 = cor1
                s2, t2 = cor2
                s_tex = s1 * t + s2 * (1 - t)
                t_tex = t1 * t + t2 * (1 - t)
                cor = (s_tex, t_tex)
            else: # se forem cores, interpolar
                r1, g1, b1, a1 = cor1
                r2, g2, b2, a2 = cor2
                r = r1 * t + r2 * (1 - t)
                g = g1 * t + g2 * (1 - t)
                b = b1 * t + b2 * (1 - t)
                cor = (r, g, b, a1)
            if corte == self._largura + self._x_inicial: # se o corte for na direita da janela...
                if bin1[1] == '1': # caso de "o primeiro ponto ser trazido ao eixo de corte da janela"
                    bin_a, bin_b, bin_c, bin_d = bin1
                    return ((corte, intersecao), pf), ((bin_a, '0', bin_c, bin_d), bin2), (cor, cor2)
                elif bin2[1] == '1': #caso de "o segundo ponto ser trazido ao eixo de corte da janela"
                    bin_a, bin_b, bin_c, bin_d = bin2
                    return (pi, (corte, intersecao)), (bin1, (bin_a, '0', bin_c, bin_d)), (cor1, cor)
                else:
                    return (pi, pf), (bin1, bin2), (cor1, cor2)  # ambos estão dentro da janela
            if corte == self._x_inicial: # se o corte for na esquerda da janela...
                if bin1[3] == '1': # caso de "o primeiro ponto ser trazido ao eixo de corte da janela"
                    bin_a, bin_b, bin_c, bin_d = bin1
                    return ((corte, intersecao), pf), ((bin_a, bin_b, bin_c, '0'), bin2), (cor, cor2)
                elif bin2[3] == '1': # caso de "o segundo ponto ser trazido ao eixo de corte da janela"
                    bin_a, bin_b, bin_c, bin_d = bin2
                    return (pi, (corte, intersecao)), (bin1, (bin_a, bin_b, bin_c, '0')), (cor1, cor)
                else:
                    return (pi, pf), (bin1, bin2), (cor1, cor2)  # ambos estão dentro da janela
        else: #Se o clipping for no eixo x...
            intersecao, t = self.__intersecao_em_y(corte, pi, pf)
            if yf > yi: # Ajusta o valor de t, pois t=1 quando a aresta tiver o maior valor no eixo (convenção)
                t = 1 - t
            if t > 1 or t < 0: # No caso de não ter intesecção com o segmento de reta...
                if corte == self._altura + self._y_inicial and bin1[0] == '1': # ambos estão fora para cima da janela
                    return ((-1, -1), (-1, -1)), -1, -1
                elif corte == self._y_inicial and bin1[2] == '1': # ambos estão fora para baixo da janela
                    return ((-1, -1), (-1, -1)), -1, -1
                else:
                    return (pi, pf), (bin1, bin2), (cor1, cor2) # ambos estão dentro da janela
            if len(cor1) == 2: # se forem coordenadas de textura, interpolar
                s1, t1 = cor1
                s2, t2 = cor2
                s_tex = s1 * t + s2 * (1 - t)
                t_tex = t1 * t + t2 * (1 - t)
                cor = (s_tex, t_tex)
            else: # se forem cores, interpolar
                r1, g1, b1, a1 = cor1
                r2, g2, b2, a2 = cor2
                r = r1 * t + r2 * (1 - t)
                g = g1 * t + g2 * (1 - t)
                b = b1 * t + b2 * (1 - t)
                cor = (r, g, b, a1)
            if corte == self._altura + self._y_inicial: # se o corte for em cima da janela...
                if bin1[0] == '1': # caso de o primeiro ponto ser trazido ao eixo de corte da janela
                    bin_a, bin_b, bin_c, bin_d = bin1
                    return ((intersecao, corte), pf), (('0', bin_b, bin_c, bin_d), bin2), (cor, cor2)
                elif bin2[0] == '1': # caso de o segundo ponto ser trazido ao eixo de corte da janela
                    bin_a, bin_b, bin_c, bin_d = bin2
                    return (pi, (intersecao, corte)), (bin1, ('0', bin_b, bin_c, bin_d)), (cor1, cor)
                else:
                    return (pi, pf), (bin1, bin2), (cor1, cor2)  # ambos estão dentro da janela
            if corte == self._y_inicial: # se o corte for embaixo da janela...
                if bin1[2] == '1': # caso de o primeiro ponto ser trazido ao eixo de corte da janela
                    bin_a, bin_b, bin_c, bin_d = bin1
                    return ((intersecao, corte), pf), ((bin_a, bin_b, '0', bin_d), bin2), (cor, cor2)
                elif bin2[2] == '1': # caso de o segundo ponto ser trazido ao eixo de corte da janela
                    bin_a, bin_b, bin_c, bin_d = bin2
                    return (pi, (intersecao, corte)), (bin1, (bin_a, bin_b, '0', bin_d)), (cor1, cor)
                else:
                    return (pi, pf), (bin1, bin2), (cor1, cor2)  # ambos estão dentro da janela

    # Verifica o ponto para saber em qual lado da viewport ele está e qual binário corresponde.
    def __calcula_bin(self, ponto):
        px, py = ponto
        binario_lado_inferior = '0'
        binario_lado_direito = '0'
        binario_lado_superior = '0'
        binario_lado_esquerdo = '0'

        if px < self._x_inicial:
            binario_lado_esquerdo = '1'
        elif px > self._largura + self._x_inicial:
            binario_lado_direito = '1'
        if py < self._y_inicial:
            binario_lado_superior = '1'
        elif py > self._altura + self._y_inicial:
            binario_lado_inferior = '1'

        return binario_lado_inferior, binario_lado_direito, binario_lado_superior, binario_lado_esquerdo

    # Algoritmo de clipping.
    def update_viewport(self, scanline_color=None):
        self._conjunto_poligonos_cores = []
        self._conjunto_poligonos_cortados = []

        lados_da_janela = (self._altura + self._y_inicial, self._largura + self._x_inicial, self._y_inicial, self._x_inicial)
        binarios_dos_vertices = []

        for index, pol in enumerate(self._conjunto_poligonos):
            arestas = []
            binarios_dos_vertices = []
            lista_vertices = [(linha[0], linha[1]) for linha in pol.lista_poligono_mapeado]

            for vertice in range(len(lista_vertices)): # Preenche o vetor de arestas e calcula os binários
                if vertice > 0:
                    arestas.append((lista_vertices[vertice - 1], lista_vertices[vertice]))
                    if vertice == len(lista_vertices) - 1:
                        arestas.append((lista_vertices[vertice], lista_vertices[0]))

                binarios_dos_vertices.append(self.__calcula_bin(lista_vertices[vertice]))

            if len(scanline_color[index]) == 0: # Decide se ai trabalhar com texturas ou cores
                preenchimento = [(linha[2], linha[3]) for linha in pol.lista_poligono_customizado]
            else:
                preenchimento = []
                for i in range(len(scanline_color[index])):
                    preenchimento.append(scanline_color[index][i].get_rgba())

            cores_dos_vertices = preenchimento
            array_temporario_de_cores = []
            array_temporario_de_binarios = []
            array_temporario_de_arestas = []

            # Laço for para cada lado da janela
            for inter in range(len(lados_da_janela)): 
                if inter % 2 == 0:
                    axis = 'x'
                else:
                    axis = 'y'

                for a in range(len(arestas)):
                    if a == len(arestas) - 1:
                        aresta_cortada, binarios_da_aresta, cores_da_aresta = self.__corta_aresta(arestas[a], lados_da_janela[inter], axis, cores_dos_vertices[a], cores_dos_vertices[0], binarios_dos_vertices[a], binarios_dos_vertices[0])
                    else:
                        aresta_cortada, binarios_da_aresta, cores_da_aresta = self.__corta_aresta(arestas[a], lados_da_janela[inter], axis, cores_dos_vertices[a], cores_dos_vertices[a+1], binarios_dos_vertices[a], binarios_dos_vertices[a+1])
                    
                    ponto_inicial, ponto_final = aresta_cortada
                    x_inicial, y_inicial = ponto_inicial

                    # Se o ponto é inválido, se retorna -1
                    if x_inicial != -1 and ponto_inicial != ponto_final: 
                        array_temporario_de_arestas.append(aresta_cortada)
                        array_temporario_de_binarios.append(binarios_da_aresta)
                        array_temporario_de_cores.append(cores_da_aresta)

                arestas = []

                if not array_temporario_de_arestas or len(array_temporario_de_arestas) == 1: # Polígono completamente cortado
                    break

                binarios_dos_vertices = []
                cores_dos_vertices = []

                # Essa parte trata de religar o polígono, já que as arestas estão separadas, de forma que ele volte ao corte posteriormente.
                arestas.append(array_temporario_de_arestas[0])
                bin_do_ponto_inicial, bin_do_ponto_final = array_temporario_de_binarios[0]
                binarios_dos_vertices.append(bin_do_ponto_inicial)
                cor_do_ponto_inicial, cor_do_ponto_final = array_temporario_de_cores[0]
                cores_dos_vertices.append(cor_do_ponto_inicial)

                for a in range(len(array_temporario_de_arestas)):
                    ponto_inicial, ponto_final = array_temporario_de_arestas[a]
                    x_final, y_final = ponto_final

                    bin_do_ponto_inicial, bin_do_ponto_final = array_temporario_de_binarios[a]
                    cor_do_ponto_inicial, cor_do_ponto_final = array_temporario_de_cores[a]

                    if a == len(array_temporario_de_arestas) - 1:
                        ponto_inicial_a_ser_ligado, xpf = array_temporario_de_arestas[0]
                    else:
                        ponto_inicial_a_ser_ligado, xpf = array_temporario_de_arestas[a+1]

                    x_inicial_do_ponto_a_ser_ligado, y_inicial_do_ponto_a_ser_ligado = ponto_inicial_a_ser_ligado

                    # Checa se o polígono está conectado ou não
                    if x_final != x_inicial_do_ponto_a_ser_ligado or y_final != y_inicial_do_ponto_a_ser_ligado: 
                        arestas.append(((x_final, y_final), (x_inicial_do_ponto_a_ser_ligado, y_inicial_do_ponto_a_ser_ligado))) # se não estiver, será ligado
                        binarios_dos_vertices.append(bin_do_ponto_final)
                        cores_dos_vertices.append(cor_do_ponto_final)

                    # Ligação normal
                    if a != len(array_temporario_de_arestas) - 1: 
                        arestas.append(array_temporario_de_arestas[a + 1])
                        bin_do_ponto_inicial, bin_do_ponto_final = array_temporario_de_binarios[a + 1]
                        cor_do_ponto_inicial, cor_do_ponto_final = array_temporario_de_cores[a + 1]
                        binarios_dos_vertices.append(bin_do_ponto_inicial)
                        cores_dos_vertices.append(cor_do_ponto_inicial)

                array_temporario_de_arestas = []
                array_temporario_de_binarios = []
                array_temporario_de_cores = []

            novo_poligono = Poligono()
            ultimo_eh_negativo = False
            matriz_cores = []
            if arestas: # Laço for pra preencher o novo polígono já cortado

                matriz_cores = []

                for a in range(len(arestas)):
                    ponto_inicial, ponto_final = arestas[a]
                    x_inicial, y_inicial = ponto_inicial

                    while x_inicial < 0 or y_inicial < 0: # Para checar um erro ocasional de coordenadas negativas
                        if a == len(arestas)-1:
                            ultimo_eh_negativo = True # Se a última coordenada for negativa, fecha o polígono
                            break

                        a += 1
                        ponto_inicial, ponto_final = arestas[a]
                        x_inicial, y_inicial = ponto_inicial
                    
                    if ultimo_eh_negativo:
                        break

                    if len(cores_dos_vertices[a]) == 2: # Caso trabalhemos com texturas
                        #self._conjunto_poligonos_cores.append([])
                        tx, ty = cores_dos_vertices[a]
                        novo_poligono.insere_ponto(round(x_inicial), round(y_inicial), tx, ty)

                    else: # caso trabalhemos com cores
                        r, g, b, alpha = cores_dos_vertices[a]
                        matriz_cores.append(Cor(r, g, b, alpha))
                        novo_poligono.insere_ponto(round(x_inicial), round(y_inicial), 0, 0)


            self._conjunto_poligonos_cores.append(matriz_cores)

            self._conjunto_poligonos_cortados.append(novo_poligono) # Adiciona o novo polígono à lista


# Classe que é basicamente uma pequena estrutura de dados que armazena outros 3 vetores. 
# lista_de_arestas está depreciado, pois a ideia inicial era criar um mapeamentos para viewport
# de arestas simples DDA.
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

    # Faço vários gets para pegar esses vetores por referência e dar um append neles se preciso.
    @property
    def lista_de_mapeamentos(self):
        return self._lista_de_mapeamentos
    
    @property
    def lista_de_cores(self):
        return self._lista_de_cores
    
    @property
    def lista_de_arestas(self):
        return self._lista_de_arestas