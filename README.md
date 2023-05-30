Esse trabalho foi elaborado para a disciplina de **Computação Gráfica CK0245** da **Universidade Federal do Ceará**, ministrada pelo professor **Yuri Lenon Barbosa Nogueira**.

**Trabalho feito em dupla por:**
- Mirailton Mota Costa Filho
- Victor Medeiros Martins

O trabalho escolhido foi um jogo. Todo o jogo foi feito no braço, usando apenas o método set_at() (setpixel) do pygame para colocar um único pixel de cor RGB na matriz de tela, para assim tornar possível a criação de retas, formas geométricas diversas e renderização dos objetos na tela. Também foi utilizada a fonte do pygame para exibição de dados e o pillow para carregamento de imagens e conversão para matrizes.

RetaDDA, floodfill, scanlines: Mirailton e Victor
Reta Bresenham: Mirailton
Circunferência, Elipse: Victor
Transformações lineares (translação, escala e rotação), janela e viewport: Victor
Algoritmo de Clipping: Mirailton
Texturas utilizadas: assets do jogo Super Mario World, da Nintendo
Estrutura de classes, tela inicial: Victor
Lógica do jogo: Mirailton e Victor

A tela inicial, como solicitada pelo professor, utiliza algoritmos de baixo nível para desenho.

- Elipse (atrás do título do jogo)
- Circunferência (seletor de opção de jogar ou sair)
- Floodfill preenchendo a circunferência e a elipse
- Todas as letras foram desenhadas no braço, todas são polígonos, e preenchidas com floodfill.
    - Isso inclui as letras miúdas de jogar/sair.

A tela de jogo é exibida conforme uma janela recorta as coordenadas de mundo, e essa tela já é a viewport. O algoritmo de clipping funciona, e para ver isso acontecer, basta maximizar a janela do pygame. Todos os objetos são mapeados para a viewport e recortados.

É também exibida em tempo real as coordenadas do jogador no mundo e as coordenadas de janela, além do contador de FPS e o contador de estrelas coletadas, como um debug simples.

O jogo possui 5 estrelas coletáveis pelo mapa. E em todas elas possui ao redor requisitos que o professor solicitou para o trabalho.

- 1° estrela (x:16, y:32): um simples OI feito com cement blocks 16x16 individuais. Serve para mostrar o mapeamento de textura.
- 2° estrela (x:-260, y:-260): um bullet bill que sofre transformação linear de escala e uma leve translação a cada 15 ticks.
- 3° estrela (x:180, y:-316): um boo que gira em torno de um eixo (transformação linear de rotação).
- 4° estrela (x:435, y:280): dois pisos escritos ZOOM, um dá zoom out e outro zoom in ao pisar em cima. Servem para mostrar a transformação linear na janela e como isso acontece na viewport.
- 5° estrela (x:-330, y:240): Diversos polígonos que mostram diferentes scanlines: sólido, degradê RGB, textura de um gato e degradê laranja-ciano-roxo
- Extra: (x:0, y:350): Uma banana que sofre transformação linear de escala e translação ao pisar em cima.

A estrela por si só é um polígono, que é formado por uma estrutura de dados que armazena vértices igual qualquer outro polígono desenhado no braço dentro do jogo, porém mais complexa. Ela sofre transformação linear de rotação em torno do seu próprio eixo, e pra isso é preciso transladar para a origem, rotacionar e depois devolver para a posição original.

> Nota: a borda do jogo é o polígono vermelho/preto. Ela cobre uma região de 1000 de largura e 1000 de altura. Além desse limite nada foi colocado.

O sprite do jogador também, com inputs do usuário, translada e rotaciona. A rotação do jogador precisou ser arredondada (round()) a cada iteração, pois ao trabalhar com valores trigonométricos em float, ao mudar o sentido do player, gerava distorções em seu sprite. A janela translada, acompanhando a movimentação do sprite do jogador.

Ao coletar as 5 estrelas, o jogo termina.

### Requisitos

É necessário instalar o pygame (pip install pygame) e o pillow (pip install pillow). Ambos os comandos se utiliza no terminal.

Para executar o jogo, basta executar a main.py com o projeto aberto. Para executar no terminal, basta digitar "python3 main.py" sem aspas, na pasta do jogo.
