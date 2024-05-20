import pygame
import os
from config import IMG_DIR, SND_DIR, FNT_DIR, DINO_PE_WIDTH, DINO_PE_HEIGHT, DINO_AGA_WIDTH, DINO_AGA_HEIGHT

BACKGROUND = 'background'
DINO_PE_IMG = 'dino_pe_img'
DINO_AGACHADO_IMG = 'dino_agachado_img'
OBS1_IMG = 'obs1_img'
SCORE_FONT = 'score_font'
JUMP_SOUND = 'jump_sound'
DEATH_SOUND = 'death_sound'
BACKGROUND_SOUND = 'background_sound'

dino_image_original = pygame.image.load(os.path.join(IMG_DIR, 'de_pe.png'))
dino_ducked_image_original = pygame.image.load(os.path.join(IMG_DIR, 'agachado.png'))
background_image_original = pygame.image.load(os.path.join(IMG_DIR, 'background_dino.jpeg'))
score_font = pygame.font.Font(os.path.join(FNT_DIR, 'scorefont.TTF'), 28)

def load_assets():
    assets = {}
    assets[BACKGROUND] = pygame.image.load(os.path.join(IMG_DIR, 'background_dino.jpeg')).convert()
    assets[DINO_PE_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'de_pe.png')).convert_alpha()
    assets[DINO_AGACHADO_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'agachado.png')).convert_alpha()
    assets[DINO_AGACHADO_IMG] = pygame.transform.scale(assets['ship_img'], (SHIP_WIDTH, SHIP_HEIGHT))
    assets[SCORE_FONT] = pygame.font.Font(os.path.join(FNT_DIR, 'scorefont.TTF'), 28)
    assets[DINO_PE_IMG] = pygame.transform.scale(assets['dino_pe_img'], (60, 60))  
    assets[DINO_AGACHADO_IMG] = pygame.transform.scale(assets['dino_agachado_img'], (60, 60))  
    assets[BACKGROUND] = pygame.transform.scale(assets['background'], (800, 400))  

    

    # Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SND_DIR, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
    pygame.mixer.music.set_volume(0.4)
    assets[BOOM_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'expl3.wav'))
    assets[DESTROY_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'expl6.wav'))
    assets[PEW_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'pew.wav'))
    return assets
