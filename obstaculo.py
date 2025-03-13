import pygame
import random

class Obstaculo:
    def __init__(self, screen_width, altura_chao):
        self.width = 20
        if random.randint(0, 1) == 0:
            self.height = random.randint(20, 40)
            self.y = altura_chao - self.height
        else:
            self.height = 30
            self.y = altura_chao - self.height - 40
        self.x = screen_width
        self.speed_base = 7
        self.speed = self.speed_base

    def update_obstaculo(self):
        self.x -= self.speed
        


    def aloca_obstaculos(self, screen):
        pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(self.x, self.y, self.width, self.height))

    def checa_colisao(self, dino):
        return dino.obter_retangulo_dino().colliderect(
            pygame.Rect(self.x, self.y, self.width, self.height)
        )

    def fora_da_tela(self):
        return self.x < -self.width