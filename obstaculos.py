import pygame
import random
from config import BLACK

class Obstaculo:
    def __init__(self, largura_tela, altura_chao):
        self.x = largura_tela
        self.largura = 20
        if random.randint(0, 1) == 0:
            self.altura = random.randint(20, 40)
            self.y = altura_chao - self.altura
        else:
            self.altura = 30
            self.y = altura_chao - self.altura - 40

    def mover(self, velocidade):
        self.x -= velocidade

    def obter_retangulo(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, BLACK, self.obter_retangulo())

