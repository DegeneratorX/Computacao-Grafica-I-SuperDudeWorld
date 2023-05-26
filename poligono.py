import numpy as np
from desenho import Color, Texture

class Poligono:
    def __init__(self, lista_poligono_customizado=None):
        if lista_poligono_customizado is None:
            lista_poligono_customizado = []
        self._lista_poligono_customizado = lista_poligono_customizado
        self._lista_poligono_mapeado = []

    @property
    def lista_poligono_customizado(self):
        return self._lista_poligono_customizado

    @property
    def lista_poligono_mapeado(self):
        return self._lista_poligono_mapeado

    def insere_ponto(self, x, y, tx, ty):
        self._lista_poligono_customizado.append([x, y, tx, ty])

    @staticmethod
    def get_bloco_mapeado(origem_x, origem_y, tamanho, scanline_color, pilha_de_mapeamentos):
        lista_poligono = [
            [origem_x, origem_y, 0, 0],
            [origem_x+tamanho, origem_y, 1, 0],
            [origem_x+tamanho, origem_y+tamanho, 1, 1],
            [origem_x, origem_y+tamanho, 0, 1],
        ]
        bloco_object = Poligono(lista_poligono)
        bloco_mapeado = Projecao(bloco_object.lista_poligono_customizado, pilha_de_mapeamentos.janela, pilha_de_mapeamentos.viewport)
        bloco_mapeado.get_poligono_mapeado()
        pilha_de_mapeamentos.lista_de_mapeamentos.append(bloco_mapeado)
        if isinstance(scanline_color, Color) or isinstance(scanline_color, Texture):
            pilha_de_mapeamentos.lista_de_cores.append([])
        elif isinstance(scanline_color, list):
            pilha_de_mapeamentos.lista_de_cores.append(scanline_color)
        else:
            raise AttributeError("Objeto de pintura do polígono não é de um tipo válido.")
        
        return bloco_mapeado
    
    def get_poligono_customizado_mapeado(self, scanline_color, pilha_de_mapeamentos):
        poligono_mapeado = Projecao(self.lista_poligono_customizado, pilha_de_mapeamentos.janela, pilha_de_mapeamentos.viewport)
        poligono_mapeado.get_poligono_mapeado()
        pilha_de_mapeamentos.lista_de_mapeamentos.append(poligono_mapeado)
        if isinstance(scanline_color, Color) or isinstance(scanline_color, Texture):
            pilha_de_mapeamentos.lista_de_cores.append([])
        elif isinstance(scanline_color, list):
            pilha_de_mapeamentos.lista_de_cores.append(scanline_color)
        else:
            raise AttributeError("Objeto de pintura do polígono não é de um tipo válido.")
        
        return poligono_mapeado

    # Acúmulo = matriz que acumula transformações sucessivas em uma identidade (inicialmente) para depois ser aplicada
    # ao polígono.
    @staticmethod
    def mover_poligono(translacao_x, translacao_y, acumulo=[[1,0,0],[0,1,0],[0,0,1]]):
        return multiplicacao_matrizes([
            [1, 0, translacao_x],
            [0, 1, translacao_y],
            [0, 0 ,           1]
        ], acumulo)
    
    @staticmethod
    def redimensionar_poligono(escala_x, escala_y, acumulo=[[1,0,0],[0,1,0],[0,0,1]]):
        return multiplicacao_matrizes([
            [escala_x, 0, 0],
            [0, escala_y, 0],
            [0, 0,        1]
        ], acumulo)
    
    @staticmethod
    def rotacionar_poligono(angulo, acumulo=[[1,0,0],[0,1,0],[0,0,1]], player=False):
        angulo = angulo*np.pi/180
        return multiplicacao_matrizes([
            [np.cos(angulo), -np.sin(angulo), 0],
            [np.sin(angulo), np.cos(angulo),  0],
            [0, 0,                            1]
        ], acumulo, player)
    

    def aplicar_transformacao_com_acumulos(self, acumulo):
        self._lista_poligono_customizado = np.array(self._lista_poligono_customizado)
        
        for i in range(self._lista_poligono_customizado.shape[0]):
            ponto_poligono = np.concatenate((self._lista_poligono_customizado[i, :2], [1]))
            ponto_poligono = np.transpose(ponto_poligono)
            
            ponto_poligono = np.dot(acumulo, ponto_poligono)
            
            ponto_poligono = np.transpose(ponto_poligono)
            self._lista_poligono_customizado[i, :2] = ponto_poligono[:2]
        
        return self._lista_poligono_customizado.tolist()


class Projecao(Poligono):
    def __init__(self, lista_poligono_customizado, lista_janela, lista_viewport) -> None:
        super().__init__(lista_poligono_customizado)
        self.lista_janela = lista_janela
        self.lista_viewport = lista_viewport

    def get_poligono_mapeado(self):
        x_inicial_viewport = self.lista_viewport[0]
        y_inicial_viewport = self.lista_viewport[1]

        x_final_viewport = self.lista_viewport[2]
        y_final_viewport = self.lista_viewport[3]

        x_inicial_janela = self.lista_janela[0]
        y_inicial_janela = self.lista_janela[1]

        x_final_janela = self.lista_janela[2]
        y_final_janela = self.lista_janela[3]

        a = (x_final_viewport-x_inicial_viewport)/(x_final_janela-x_inicial_janela)
        b = (y_final_viewport-y_inicial_viewport)/(y_final_janela-y_inicial_janela)

        matriz_mapeamento = [
            [a,    0,     x_inicial_viewport-a*x_inicial_janela],
            [0,    b,     y_inicial_viewport-b*y_inicial_janela],
            [0,    0,                        1                 ]
        ]
        self._lista_poligono_mapeado = self.aplicar_transformacao_com_acumulos(matriz_mapeamento)
        return self._lista_poligono_mapeado

    # DEPRECIADA: esse método é para viewport estática, o primeiro tipo que o yuri deu em sala.
    """
    def get_poligono_mapeado(self):
        largura_viewport = self.lista_viewport[0]
        altura_viewport = self.lista_viewport[1]

        x_inicial = self.lista_janela[0]
        y_inicial = self.lista_janela[1]

        x_final = self.lista_janela[2]
        y_final = self.lista_janela[3]

        matriz_mapeamento = [
            [largura_viewport/(x_final-x_inicial),                0,                   -(x_inicial*largura_viewport)/(x_final-x_inicial)],
            [               0,                    altura_viewport/(y_final-y_inicial),  -(y_inicial*altura_viewport)/(y_final-y_inicial)],
            [               0,                                    0,                                             1                      ]
        ]
        return self.aplicar_transformacao_com_acumulos(matriz_mapeamento)
        """

def transposta(matriz):
    if isinstance(matriz[0], int) or len(matriz) == 1:
        return matriz
    
    linhas = len(matriz)
    colunas = len(matriz[0])

    transposta = [[0 for _ in range(linhas)] for _ in range(colunas)]
    
    for i in range(linhas):
        for j in range(colunas):
            transposta[j][i] = matriz[i][j]
    
    return transposta

def multiplicacao_matrizes(matriz_1, matriz_2, player=False):
    linha_1, coluna_1 = len(matriz_1), len(matriz_1[0])
    linha_2, coluna_2 = len(matriz_2), len(matriz_2[0])
    
    if coluna_1 != linha_2:
        raise ValueError("O número de colunas da matriz 1 deve ser o mesmo do número de linhas da matriz 2")
    
    resultado = [[0] * coluna_2 for _ in range(linha_1)]
    
    for i in range(linha_1):
        for j in range(coluna_2):
            for k in range(coluna_1):
                if player:
                    resultado[i][j] += round(matriz_1[i][k] * matriz_2[k][j])
                else:
                    resultado[i][j] += (matriz_1[i][k] * matriz_2[k][j])
    return resultado