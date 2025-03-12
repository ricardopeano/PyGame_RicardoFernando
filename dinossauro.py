import pygame
import os
from config import IMG_DIR

class Dinossauro:
    def __init__(self, altura_chao):
        self.dino_x = 50
        self.dino_y = altura_chao -  50
        self.altura_chao = altura_chao
        self.dino_jump = False
        self.jump_height = 0
        self.initial_jump_height = 10
        self.gravity = 1
        self.ducking = False

        # Carregando as imagens do dinossauro
        self.dino_image = pygame.transform.scale(
            pygame.image.load(os.path.join(IMG_DIR, 'de_pe.png')), (50, 50)
        )
        self.dino_ducked_image = pygame.transform.scale(
            pygame.image.load(os.path.join(IMG_DIR, 'agachado.png')), (50, 35)
        )

    def pular(self):
        if not self.dino_jump and not self.ducking:
            self.dino_jump = True
            self.jump_height = self.initial_jump_height

    def agachar(self, estado):
        self.ducking = estado

    def atualizar(self):
        if self.dino_jump:
            self.dino_y -= self.jump_height
            self.jump_height -= self.gravity
            if self.dino_y > self.altura_chao - 50:
                self.dino_y = self.altura_chao - 50
                self.dino_jump = False
                self.jump_height = 0

    def aloca_dino(self, screen):
        if self.ducking:
            screen.blit(self.dino_ducked_image, (self.dino_x, self.dino_y + 20))
        else:
            screen.blit(self.dino_image, (self.dino_x, self.dino_y))

    def obter_retangulo_dino(self):
        effective_dino_height = self.dino_ducked_image.get_height() if self.ducking else self.dino_image.get_height()
        effective_dino_y = self.dino_y + 20 if self.ducking else self.dino_y
        return pygame.Rect(self.dino_x, effective_dino_y, self.dino_image.get_width(), effective_dino_height)
