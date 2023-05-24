import numpy as np
from screen import Color, Texture


class Desenho:

    def __init__(self, screen):
        self.__screen = screen

    def senoide_com_distorcao(self, color):
        # Para cada x que eu estiver
        for x in range(self.__screen.get_width()):
            # Desenho um y correspondente (Exemplo do que gerará:
            # 50, 51, 52, 51, 50, 49, 48, 49, 50...)
            y = (self.__screen.get_height()/4) + \
                100*np.sin(x*0.05)  # Função seno
            # Para cada y, pode gerar um float. Coverto pra inteiro.
            y = int(y)
            self.__screen.set_pixel(x, y, color)

    def senoide_sem_distorcao(self, color):
        # Defino o ponto inicial
        x_anterior = 0
        y_anterior = (self.__screen.get_height()/2) + \
            100*np.sin(x_anterior*0.05)
        y_anterior = int(y_anterior)

        # E para cada x que produzo, seta um pixel em y, e conecto o x anterior e y_anterior ao x atual e y atual.
        for x in range(self.__screen.get_width()):
            y = (self.__screen.get_height()/2) + \
                100*np.sin(x*0.05)  # Função seno
            # Para cada y, pode gerar um float. Coverto pra inteiro.
            y = int(y)
            self.reta_DDA(x_anterior, y_anterior, x, y, color)
            x_anterior = x
            y_anterior = y

    def reta_tradicional(self, x_inicial, y_inicial, x_final, y_final, color):
        delta_x = x_final - x_inicial
        delta_y = y_final - y_inicial

        coeficiente_angular = delta_y/delta_x

        # Se a reta não for de fato variável, é um ponto
        if delta_x == 0 and delta_y == 0:
            self.__screen.set_pixel(x_inicial, y_inicial, color)

        # Preciso saber se o ângulo é maior que 45 graus. Se for, troco as
        # variáveis x e y. Obviamente se a altura (y) for maior que a largura (x),
        # trivialmente o ângulo deve ser maior que 45 graus em relação a abscissa.
        trocou = False
        if abs(delta_y) > abs(delta_x):
            delta_x, delta_y = delta_y, delta_x
            trocou = True

        # Caminhho sobre x
        for variacao_em_x in range(delta_x):

            # Delta_y_i = Delta_x_i * a
            variacao_em_y = variacao_em_x * coeficiente_angular

            # Calculo as coordenadas que será setado o pixel
            x = round(x_inicial + variacao_em_x)
            y = round(y_inicial + variacao_em_y)

            # Finalmente coloco.
            if not trocou:
                self.__screen.set_pixel(x, y, color)
            else:
                self.__screen.set_pixel(y, x, color)

    def reta_DDA(self, x_inicial, y_inicial, x_final, y_final, color, antialiasing=False):
        delta_x = x_final-x_inicial
        delta_y = y_final-y_inicial

        # Defino como passos o percorrimento da variação em x
        passos = abs(delta_x)

        # mas se a variação de y for maior, o percorrimento deve ser em y, parecido com a reta tradicional.
        if abs(delta_y) > abs(delta_x):
            passos = abs(delta_y)
        # pygame.display.update()
        if passos == 0:
            self.__screen.set_pixel(x_inicial, y_inicial, color)
            return

        # Quantidade de passos que eu vou dar em x e em y, em porcentagem.
        # Se delta_x > delta_y, então a razão será 1 passo por 1 pixel em x.
        # No caso do y não, será um float, ou seja, uma porcentagem reduzida de passos.
        # Mas se delta_y > delta_x, então a razão será 1 passo por 1 pixel em y.
        passo_x = delta_x/passos
        passo_y = delta_y/passos

        for i in range(passos):

            # Agora para cada passo i, eu multiplico pela % de passo de coordenada
            # para obter quantos pixels em x ou y andou, e depois somo com x_inicial
            # ou y_inicial para obter o segmento de reta
            x = round(x_inicial + i*passo_x)
            y = round(y_inicial + i*passo_y)

            if antialiasing == True:
                red, green, blue, alpha = color.get_rgba()
                if abs(round(passo_x)) == 1:
                    y_decimal = y - np.floor(y)
                    # TODO: Erro ao multiplicar float com classe Color. O que fazer?
                    # Preciso reduzir em % de acordo com a intensidade da cor cada cor para o antiserrilhado.

                    color_serrilhado_1 = Color(round(
                        (1-y_decimal)*red), round((1-y_decimal)*green), round((1-y_decimal)*blue), alpha)
                    color_serrilhado_2 = Color(
                        round((y_decimal)*red), round((y_decimal)*green), round((y_decimal)*blue), alpha)

                    self.__screen.set_pixel(int(round(x)), int(
                        np.floor(y)), color_serrilhado_1)
                    self.__screen.set_pixel(int(round(x)), int(
                        np.floor(y+1)), color_serrilhado_2)
                else:
                    x_decimal = x - np.floor(x)

                    color_serrilhado_1 = Color(round(
                        (1-x_decimal)*red), round((1-x_decimal)*green), round((1-x_decimal)*blue), alpha)
                    color_serrilhado_2 = Color(
                        round((x_decimal)*red), round((x_decimal)*green), round((x_decimal)*blue), alpha)

                    self.__screen.set_pixel(int(np.floor(x)), int(
                        round(y)), color_serrilhado_1)
                    self._screen.set_pixel(int(np.floor(x+1)),
                                           int(round(y)), color_serrilhado_2)

            else:
                self.__screen.set_pixel(x, y, color)

    def reta_bresenham(self, x_inicial, y_inicial, x_final, y_final, color):
        delta_x = x_final - x_inicial
        delta_y = y_final - y_inicial

        x = round(x_inicial)
        y = round(y_inicial)

        # Usado pra decrementar se a reta for da direita pra esquerda ou baixo pra cima
        if delta_x < 0:
            fator_multiplicativo_x = -1
        else:
            fator_multiplicativo_x = 1

        if delta_y < 0:
            fator_multiplicativo_y = -1
        else:
            fator_multiplicativo_y = 1

        # Condicional para tratar o caso da reta > 45°
        if abs(delta_x) >= abs(delta_y):

            # P inicial (P0), encontrado no arquivo DESENHOS.md
            p = -abs(delta_x) + (2*abs(delta_y))

            for i in range(round(abs(delta_x))):
                self.__screen.set_pixel(round(x), round(y), color)

                # Incremento (ou decremento, depende do fator) em x
                x = x + fator_multiplicativo_x

                # Se a distância d1 for >= d2 (explicado no arquivo DESENHOS.md)
                if p >= 0:
                    # Incremento (ou decremento, depende do fator) em y
                    y = y + fator_multiplicativo_y
                    p = p - (2*abs(delta_x)) + (2*abs(delta_y))
                else:
                    p = p + (2*abs(delta_y))
        else:
            p = -delta_y + (2 * abs(delta_x))

            for i in range(abs(delta_y)):
                self.__screen.set_pixel(round(x), round(y), color)

                y = y + fator_multiplicativo_y
                if p >= 0:
                    x = x + fator_multiplicativo_x
                    p = p - (2 * abs(delta_y)) + (2 * abs(delta_x))
                else:
                    p = p + (2 * abs(delta_x))

    def circunferencia(self, x_origem, y_origem, raio, color):
        # 1° Quadrante

        # Procuro guardar o x anterior igual como no alg da senóide. No caso começo o desenho em x_origem+raio.
        x_anterior = x_origem + raio
        # E começo no y de origem. Ou seja, no primeiro quadrante, é 0° que começo.
        y_anterior = y_origem
        # Percorro em x do raio até -2 (-2 é gambiarra pra fechar o circulo), dando passo pra trás (-1)
        for iterador_em_x in range(raio, -2, -1):
            x = x_origem + iterador_em_x  # E vou percorrendo em x
            # Ao mesmo tempo que produzo um resultado em y
            y = -np.sqrt(abs(raio**2 - (x - x_origem)**2)) + y_origem
            # vou desenhando ponto por ponto no percorrimento
            self.reta_DDA(x_anterior, y_anterior, x, int(y), color)
            # E assim passo o atual para o anterior, e vou desenhadno retas minúsculas aos poucos.
            x_anterior = x
            y_anterior = int(y)

        # 2° Quadrante
        x_anterior = x_origem - raio
        y_anterior = y_origem
        for iterador_em_x in range(raio, -1, -1):
            x = x_origem - iterador_em_x
            y = -np.sqrt(abs(raio**2 - (x - x_origem)**2)) + y_origem
            self.reta_DDA(x_anterior, y_anterior, x, int(y), color)
            x_anterior = x
            y_anterior = int(y)

        # 3° Quadrante
        x_anterior = x_origem - raio
        y_anterior = y_origem
        for iterador_em_x in range(raio, -2, -1):
            x = x_origem - iterador_em_x
            y = +np.sqrt(abs(raio**2 - (x - x_origem)**2)) + y_origem
            self.reta_DDA(x_anterior, y_anterior, x, int(y), color)
            x_anterior = x
            y_anterior = int(y)

        # 4° Quadrante
        x_anterior = x_origem + raio
        y_anterior = y_origem
        for iterador_em_x in range(raio, -1, -1):
            x = x_origem + iterador_em_x
            y = +np.sqrt(abs(raio**2 - (x - x_origem)**2)) + y_origem
            self.reta_DDA(x_anterior, y_anterior, x, int(y), color)
            x_anterior = x
            y_anterior = int(y)

    # Algoritmo parecido com a circunferência, porém acima de 45°, ele precisa iterar em y e desenhar em x.
    # a = altura da elipse. b = largura da elipse
    def elipse(self, x_origem, y_origem, a, b, color):
        if abs(a) >= abs(b):  # Se ângulo é maior ou igual a 45°
            b_menor_que_a = True
            self.__desenha_quadrante_elipse(
                b_menor_que_a, x_origem, y_origem, a, b, color, 1, -1)
            self.__desenha_quadrante_elipse(
                b_menor_que_a, x_origem, y_origem, a, b, color, -1, -1)
            self.__desenha_quadrante_elipse(
                b_menor_que_a, x_origem, y_origem, a, b, color, -1, 1)
            self.__desenha_quadrante_elipse(
                b_menor_que_a, x_origem, y_origem, a, b, color, 1, 1)
        else:  # Se ângulo é menor que 45°
            b_menor_que_a = False
            self.__desenha_quadrante_elipse(
                b_menor_que_a, x_origem, y_origem, a, b, color, 1, -1)
            self.__desenha_quadrante_elipse(
                b_menor_que_a, x_origem, y_origem, a, b, color, -1, -1)
            self.__desenha_quadrante_elipse(
                b_menor_que_a, x_origem, y_origem, a, b, color, -1, 1)
            self.__desenha_quadrante_elipse(
                b_menor_que_a, x_origem, y_origem, a, b, color, 1, 1)

    def __desenha_quadrante_elipse(self, b_menor_que_a, x_origem, y_origem, a, b, color, sinal_x, sinal_y):
        if b_menor_que_a:
            x_anterior = x_origem + sinal_x * b
            y_anterior = y_origem
            for iterador_em_x in range(b, -2, -1):
                x = x_origem + sinal_x * iterador_em_x
                y = sinal_y * np.sqrt(abs(a*a - (a*a)/(b*b) * (x - x_origem)
                                          * (x - x_origem))) + y_origem
                self.reta_DDA(x_anterior, y_anterior, x, int(y), color)
                x_anterior = x
                y_anterior = int(y)
        else:
            x_anterior = x_origem
            y_anterior = y_origem + sinal_y * a
            for iterador_em_y in range(int(a), -2, -1):
                y = y_origem + sinal_y * iterador_em_y
                x = sinal_x * np.sqrt(abs(b*b - (b*b)/(a*a) * (y - y_origem)
                                          * (y - y_origem))) + x_origem
                self.reta_DDA(x_anterior, y_anterior, int(x), y, color)
                x_anterior = int(x)
                y_anterior = y

    # Uso não recomendado/depreciado (causa estouro na call stack dependendo do tamanho do preenchimento)

    def flood_fill_recursivo(self, x_setar, y_setar, cor_nova, cor_inicial, primeira_vez_executando=True):
        if self.__screen.get_pixel(x_setar, y_setar) == cor_nova:
            if primeira_vez_executando:
                self.__screen.set_pixel(x_setar, y_setar, cor_nova)
            return

        self.__screen.set_pixel(x_setar, y_setar, cor_nova)
        self.flood_fill_recursivo(
            x_setar, y_setar-1, cor_nova, cor_inicial, False)
        self.flood_fill_recursivo(
            x_setar+1, y_setar, cor_nova, cor_inicial, False)
        self.flood_fill_recursivo(
            x_setar, y_setar+1, cor_nova, cor_inicial, False)
        self.flood_fill_recursivo(
            x_setar-1, y_setar, cor_nova, cor_inicial, False)

    # Dados guardados na heap. É o indicado para uso.
    def flood_fill_iterativo(self, x_setar, y_setar, cor_nova):
        # Capturo a cor que cliquei
        cor_inicial = self.__screen.get_pixel(x_setar, y_setar)
        if cor_inicial == cor_nova.get_rgba():  # Se for a mesma cor que quero colocar, faz nada.
            self.__screen.set_pixel(x_setar, y_setar, cor_nova)
            return

        pilha = [(x_setar, y_setar)]
        while pilha:
            x, y = pilha.pop()
            # Se a cor detectada do próximo da pilha for diferente, para o preenchimento.
            if self.__screen.get_pixel(x, y) != cor_inicial:
                continue
            # Se não, preenche com pixel
            self.__screen.set_pixel(x, y, cor_nova)

            # Verifico pra onde vai os próximos pixels, esquerda, direita, cima e baixo.
            if y > 0:
                pilha.append((x, y-1))
            if x < self.__screen.get_width():
                pilha.append((x+1, y))
            if y < self.__screen.get_height():
                pilha.append((x, y+1))
            if x > 0:
                pilha.append((x-1, y))
            if x == 0:
                pilha.append((x, y))
            if y == 0:
                pilha.append((x, y))

    def desenha_poligono(self, lista_poligono, color, scanline_color=None):
        if not lista_poligono:
            return
        x = lista_poligono[0][0]
        y = lista_poligono[0][1]
        for i in range(1, len(lista_poligono)):
            self.reta_DDA(
                x, y, lista_poligono[i][0], lista_poligono[i][1], color)
            x = lista_poligono[i][0]
            y = lista_poligono[i][1]
        self.reta_DDA(x, y, lista_poligono[0][0], lista_poligono[0][1], color)
        if scanline_color is not None:
            if isinstance(scanline_color, Color):
                self.__scanline_simples(lista_poligono, scanline_color)
            elif isinstance(scanline_color, list):
                self.__scanline_degrade(lista_poligono, scanline_color)
            elif isinstance(scanline_color, Texture):
                self.__scanline_texture(lista_poligono, scanline_color)

    def __intersecao(self, y_da_scanline, segmento_de_reta):
        x_inicial, y_inicial, x_final, y_final = segmento_de_reta[0][
            0], segmento_de_reta[0][1], segmento_de_reta[1][0], segmento_de_reta[1][1]

        # Se o segmento de reta for horizontal, não tem interseção (ou interseção infinita)
        if y_inicial == y_final:
            return (-1, -1)

        # Se a orientação da reta for de baixo pra cima, troca temporariamente
        if y_inicial > y_final:
            x_inicial, x_final = x_final, x_inicial
            y_inicial, y_final = y_final, y_inicial

        # Cálculo do t
        t = (y_da_scanline - y_inicial)/(y_final - y_inicial)

        # Cálculo da interseção para descobri o x que intersecciona a reta da scanline
        # com a reta do polígono
        if 0 < t <= 1:
            x = x_inicial + t*(x_final - x_inicial)
            return (x, t)

        return (-1, -1)

    def __scanline_simples(self, lista_poligono, color):
        # Capturo o valor mínimo e máximo de y de um polígono na coluna dos "y" da matriz de polígonos
        # Com esses valores, consigo determinar a altura total do polígono e saber por onde a scanline
        # deve varrer em posições y (entre y_minimo e y_maximo)
        y_minimo = min(coluna[1] for coluna in lista_poligono)
        y_maximo = max(coluna[1] for coluna in lista_poligono)

        # Para cada y de scanline, varre toda a altura do polígono
        for y_da_scanline in range(y_minimo, y_maximo):
            i = []  # Lista de pontos (x,y) de interseções

            # Aqui verifico segmentos de reta. Vejo o ponto inicial.
            ponto_inicial_x = lista_poligono[0][0]
            ponto_inicial_y = lista_poligono[0][1]

            for indice in range(1, len(lista_poligono)):

                # E aqui vejo o ponto final do segmento de um polígono.
                ponto_final_x = lista_poligono[indice][0]
                ponto_final_y = lista_poligono[indice][1]

                # Aplico o algoritmo usando o y de varredura da scanline para
                # descobrir se intersecciona em algum ponto do segmento de reta
                # do polígono. Como eu já sei onde o y da scanline está, eu só
                # preciso saber o ponto x dessa interseção.
                tupla_de_x_e_t = self.__intersecao(y_da_scanline, [
                                                   [ponto_inicial_x, ponto_inicial_y], [ponto_final_x, ponto_final_y]])
                ponto_intersecao_x = round(tupla_de_x_e_t[0])

                # Se descobriu algum ponto de interseção, então guardo esse ponto na lista de interseções.
                if ponto_intersecao_x >= 0:
                    i.append(ponto_intersecao_x)

                # Agora faço novamente o processo, só que agora transformo o que
                # era ponto final antes em inicial, assim percorro a próxima
                # aresta do polígono em sentido horário.
                ponto_inicial_x = ponto_final_x
                ponto_inicial_y = ponto_final_y

            # Terminou as arestas, agora faço uma última verificação para fechar o loop do polígono,
            # sendo agora o ponto final o primeiro vértice do polígono.
            ponto_final_x = lista_poligono[0][0]
            ponto_final_y = lista_poligono[0][1]

            tupla_de_x_e_t = self.__intersecao(y_da_scanline, [
                                               [ponto_inicial_x, ponto_inicial_y], [ponto_final_x, ponto_final_y]])
            ponto_intersecao_x = round(tupla_de_x_e_t[0])

            if ponto_intersecao_x >= 0:
                i.append(ponto_intersecao_x)

            # Encontrei todos os pontos de interseção da primeira linha de scanline,
            # ordeno o vetor de interseções, pois se ele estiver desordenado,
            # pode ocorrer que o loop interno "for pintar_pixel_em_x" não execute,
            # por exemplo, de 18 para 6, caso o 18 venha primeiro no vetor.
            i.sort()

            # Para cada ponto de interseção descoberto, eu pulo de 2 em 2, como falado no SCANLINE.md
            for ponto_intersecao in range(0, len(i), 2):

                # ==SOLUÇÃO ALTERNATIVA AO .sort() ANTERIOR==
                # x_1 = i[ponto_intersecao]
                # x_2 = i[ponto_intersecao+1]
                #
                # if x_2 < x_1:
                #   #x_2, x_1 = x_1, x_2
                # ===========================================

                # Preciso pintar todos os pixels no intervalo de um ponto de interseção ao seguinte

                for pintar_pixel_em_x in range(i[ponto_intersecao], i[ponto_intersecao+1]):
                    self.__screen.set_pixel(
                        pintar_pixel_em_x, y_da_scanline, color)

    def __scanline_degrade(self, lista_poligono, lista_cores_vertices):
        y_minimo = min(coluna[1] for coluna in lista_poligono)
        y_maximo = max(coluna[1] for coluna in lista_poligono)

        for y_da_scanline in range(y_minimo, y_maximo):
            i = []
            # Preciso linkar as cores com cada vértice de interseção
            lista_cores_intersecao = []

            ponto_inicial_x = lista_poligono[0][0]
            ponto_inicial_y = lista_poligono[0][1]

            for indice in range(1, len(lista_poligono)):

                ponto_final_x = lista_poligono[indice][0]
                ponto_final_y = lista_poligono[indice][1]
                # Pego as cores dos pontos iniciais e finais da aresta definidos pela lista passada
                ponto_inicial_cor = lista_cores_vertices[indice-1].get_rgba()
                ponto_final_cor = lista_cores_vertices[indice].get_rgba()

                tupla_de_x_e_t = self.__intersecao(y_da_scanline, [
                                                   [ponto_inicial_x, ponto_inicial_y], [ponto_final_x, ponto_final_y]])
                ponto_intersecao_x = round(tupla_de_x_e_t[0])
                # Preciso do t para fazer a interpolação de cores
                t = tupla_de_x_e_t[1]

                # Aplico a mesma regra da orientação da reta (da interseção) para cores, só que aqui mesmo
                if ponto_inicial_y > ponto_final_y:
                    ponto_final_cor, ponto_inicial_cor = ponto_inicial_cor, ponto_final_cor

                # Algoritmo de interpolação. Aqui ele vai trabalhar com % para saber qual a cor em %
                # do vértice de interseção, e depois transforma em tupla com RGBA. Cada vértice de interseção
                # com a scanline terá, portanto, sua cor. O for é apenas para trabalhar individualmente a porcentagem
                # em cada cor R G B A.
                cor_intersecao = []
                for rgba in range(4):
                    cor = int(round((ponto_final_cor[rgba]-ponto_inicial_cor[rgba])*t + ponto_inicial_cor[rgba]))
                    cor_intersecao.append(cor)
                cor_intersecao = tuple(cor_intersecao)

                # Se descobriu uma interseção, guarda a interseção na lista de interseções, e sua respectiva cor.
                if ponto_intersecao_x >= 0:
                    i.append(ponto_intersecao_x)
                    lista_cores_intersecao.append(cor_intersecao)

                # Faço a troca de cores para os respectivos vértices. Como estou percorrendo a próxima aresta,
                # preciso também mudar a cor.
                ponto_inicial_cor = ponto_final_cor
                ponto_inicial_x = ponto_final_x
                ponto_inicial_y = ponto_final_y

            # Quando o laço terminar, significa que não tem mais arestas para verificar se há interseções.
            # Portanto, verifico apenas a última aresta que liga do último vértice ao vértice que começou.
            ponto_final_x = lista_poligono[0][0]
            ponto_final_y = lista_poligono[0][1]
            ponto_final_cor = lista_cores_vertices[0].get_rgba()

            tupla_de_x_e_t = self.__intersecao(y_da_scanline, [
                                               [ponto_inicial_x, ponto_inicial_y], [ponto_final_x, ponto_final_y]])
            ponto_intersecao_x = round(tupla_de_x_e_t[0])
            t = tupla_de_x_e_t[1]

            if ponto_inicial_y > ponto_final_y:
                ponto_final_cor, ponto_inicial_cor = ponto_inicial_cor, ponto_final_cor

            cor_intersecao = []
            for rgba in range(4):
                cor = int(round((ponto_final_cor[rgba] - ponto_inicial_cor[rgba]) * t + ponto_inicial_cor[rgba]))
                cor_intersecao.append(cor)
            cor_intersecao = tuple(cor_intersecao)

            if ponto_intersecao_x >= 0:
                i.append(ponto_intersecao_x)
                lista_cores_intersecao.append(cor_intersecao)

            # Ordeno pareando a lista de interseções com suas cores respectivas
            dados_para_ordenar = list(zip(i, lista_cores_intersecao))
            dados_ordenados = sorted(dados_para_ordenar, key=lambda x: x[0])
            lista_cores_intersecao = [x[1] for x in dados_ordenados]
            i.sort()

            for ponto_intersecao in range(0, len(i), 2):
                for pintar_pixel_em_x in range(i[ponto_intersecao], i[ponto_intersecao+1]):
                    # Faço um cálculo de porcentagem agora para x, para saber o quão irá variar de cor na scanline horizontal
                    # entre uma interseção e outra.
                    porcentagem_de_cor = (
                        pintar_pixel_em_x-i[ponto_intersecao])/(i[ponto_intersecao+1]-i[ponto_intersecao])
                    # Uso a porcentagem para fazer a redução ou aumento de cor baseado na posição que o x da scanline está.
                    # O for é apenas para fazer a porcentagem aplicada a RGBA individualmente.
                    # E depois guardo o RGBA em uma tupla.
                    color = []
                    for rgba in range(4):
                        rgba_para_pintar_pixel_em_x = int(round(
                            (lista_cores_intersecao[ponto_intersecao+1][rgba]-lista_cores_intersecao[ponto_intersecao][rgba])*porcentagem_de_cor + lista_cores_intersecao[ponto_intersecao][rgba]))
                        color.append(rgba_para_pintar_pixel_em_x)
                    color = tuple(color)
                    r, g, b, a = color
                    self.__screen.set_pixel(
                        pintar_pixel_em_x, y_da_scanline, Color(r, g, b, a))

    # O algoritmo de interseção muda um pouco, pois agora precisamos passar uma estrutura de dados no formato [[xi, yi], [xf, yf]]
    # para o segmento de reta.
    def __instersecao_para_textura(self, y_da_scanline, segmento_de_reta):
        # Aqui trabalho com pontos (x,y) ao invés de individualmente, mas é a mesma coisa.
        ponto_inicial = segmento_de_reta[0]
        ponto_final = segmento_de_reta[1]

        # Se y do ponto inicial é igual o final, então a reta é horizontal.
        if ponto_inicial[1] == ponto_final[1]:
            # Retorno do (x,y) da interseção e o correspondente x da textura e y da textura)
            # [x y tx ty]
            return [-1, 0, 0, 0]
        
        # Mudança de orientação da aresta se for de baixo pra cima 
        if ponto_inicial[1] > ponto_final[1]:
            ponto_inicial, ponto_final = ponto_final, ponto_inicial

        t = (y_da_scanline - ponto_inicial[1])/(ponto_final[1] - ponto_inicial[1])

        # Calculo o x da textura e y da textura
        if t > 0 and t <= 1:
            x = int(round(ponto_inicial[0] + t*(ponto_final[0] - ponto_inicial[0])))
            x_da_textura = ponto_inicial[2] + t*(ponto_final[2] - ponto_inicial[2])
            y_da_textura = ponto_inicial[3] + t*(ponto_final[3] - ponto_inicial[3])
            return [x, y_da_scanline, x_da_textura, y_da_textura]
        return [-1, 0, 0, 0]


    def __scanline_texture(self, lista_poligono, textura):
        y_minimo = min(coluna[1] for coluna in lista_poligono)
        y_maximo = max(coluna[1] for coluna in lista_poligono)

        for y_da_scanline in range(y_minimo, y_maximo):
            i = []
            ponto_inicial = lista_poligono[0]

            for indice in range(1, len(lista_poligono)):
                ponto_final = lista_poligono[indice]

                ponto_intersecao = self.__instersecao_para_textura(y_da_scanline, [ponto_inicial, ponto_final])
                if ponto_intersecao[0] >= 0:
                    i.append(ponto_intersecao)

                ponto_inicial = ponto_final
            
            ponto_final = lista_poligono[0]
            ponto_intersecao = self.__instersecao_para_textura(y_da_scanline, [ponto_inicial, ponto_final])

            if ponto_intersecao[0] >= 0:
                i.append(ponto_intersecao)
            
            # Ordenação da lista de interseções. Como estou usando numpy.array, n uso simplesmente i.sort(), e sim
            # esse artifício, que vai ordenar os "x" de forma crescente, e ao mesmo tempo leva consigo os outros
            # números de sua lista pareados.
            i = np.array(i)
            if i.any():
                primeiro_indice_x = i[:, 0].argsort()
                i = i[primeiro_indice_x]

            for ponto_intersecao in range(0, i.shape[0], 2):
                for pintar_pixel_em_x in range(int(i[ponto_intersecao][0]), int(i[ponto_intersecao+1][0])):
                    porcentagem_de_cor = (pintar_pixel_em_x - i[ponto_intersecao][0])/(i[ponto_intersecao+1][0] - i[ponto_intersecao][0])
                    
                    x_da_textura = i[ponto_intersecao][2] + porcentagem_de_cor*(i[ponto_intersecao+1][2] - i[ponto_intersecao][2])
                    y_da_textura = i[ponto_intersecao][3] + porcentagem_de_cor*(i[ponto_intersecao+1][3] - i[ponto_intersecao][3])
                    
                    cor = textura.get_pixel_texture(x_da_textura, y_da_textura)
                    r, g, b = cor

                    self.__screen.set_pixel(pintar_pixel_em_x, y_da_scanline, Color(r, g, b))
