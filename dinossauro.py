import pygame
import os
from config import IMG_DIR, BLACK

class Dinossauro:
    def __init__(self, altura_chao):
        self.x = 50
        self.altura_chao = altura_chao
        self.dino_image = pygame.image.load(os.path.join(IMG_DIR, 'de_pe.png'))
        self.dino_ducked_image = pygame.image.load(os.path.join(IMG_DIR, 'agachado.png'))
        
        self.dino_image = pygame.transform.scale(self.dino_image, (50, 50))
        self.dino_ducked_image = pygame.transform.scale(self.dino_ducked_image, (50, 35))
        
        self.y = self.altura_chao - self.dino_image.get_height()
        self.jump = False
        self.jump_height = 0
        self.initial_jump_height = 10
        self.gravity = 1
        self.ducking = False

    def pular(self):
        if not self.jump:
            self.jump = True
            self.jump_height = self.initial_jump_height

    def abaixar(self):
        self.ducking = True

    def soltar_abaixar(self):
        self.ducking = False

    def atualizar(self):
        if self.jump:
            self.y -= self.jump_height
            self.jump_height -= self.gravity
            if self.y > self.altura_chao - self.dino_image.get_height():
                self.y = self.altura_chao - self.dino_image.get_height()
                self.jump = False
                self.jump_height = 0

    def obter_retangulo(self):
        effective_dino_height = self.dino_ducked_image.get_height() if self.ducking else self.dino_image.get_height()
        effective_dino_y = self.y + 20 if self.ducking else self.y
        return pygame.Rect(self.x, effective_dino_y, self.dino_image.get_width(), effective_dino_height)

    def checa_colisao(self, obstaculo):
        return self.obter_retangulo().colliderect(obstaculo.obter_retangulo())

    def desenhar(self, tela):
        if self.ducking:
            tela.blit(self.dino_ducked_image, (self.x, self.y + 20))
        else:
            tela.blit(self.dino_image, (self.x, self.y))

