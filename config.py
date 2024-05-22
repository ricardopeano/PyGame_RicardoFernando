from os import path

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'images')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'sounds')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'fonts')

# Dados gerais do jogo.
WIDTH = 800 # Largura da tela
HEIGHT = 400 # Altura da tela
FPS = 60 # Frames por segundo

# Define tamanhos
DINO_PE_WIDTH = 50
DINO_PE_HEIGHT = 50
DINO_AGA_WIDTH = 50
DINO_AGA_HEIGHT = 35

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Estados para controle do fluxo da aplicação
INIT = 0
GAME = 1
QUIT = 2