import pygame
import os
import random
from config import IMG_DIR, FNT_DIR, BLACK, WHITE, SND_DIR

from dinossauro import Dinossauro
from obstaculo import Obstaculo

pygame.init()

# Carregando arquivos de som
pygame.mixer.init()
background_sound = pygame.mixer.Sound(os.path.join(SND_DIR, 'game_song.ogg'))
jump_sound = pygame.mixer.Sound(os.path.join(SND_DIR, 'jump_sound.wav'))
game_over_sound = pygame.mixer.Sound(os.path.join(SND_DIR, 'game_over.wav'))

# Carrega arquivos de letra
score_font = pygame.font.Font(os.path.join(FNT_DIR, 'scorefont.ttf'), 20)
game_over_font = pygame.font.Font(os.path.join(FNT_DIR, 'scorefont.ttf'), 40)
start_font = pygame.font.Font(os.path.join(FNT_DIR, 'Daydream.ttf'), 20)

# Loop da musica de fundo
background_sound.play(-1)

# Configurações da tela
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino Game")

# Background
background_image = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, 'background_dino.jpeg')), (screen_width, screen_height)
)

# Configuração do chão
alt_visual_chao = 40
altura_chao = screen_height - alt_visual_chao

# Inicializando o dinossauro e os obstáculos
dino = Dinossauro(altura_chao)
obstacles = []
obstacle_frequency = 1500
last_obstacle_time = 0
score = 0
game_over = True

clock = pygame.time.Clock()

# Função para desenhar o botão "Start"
def desenha_start():
    start_text = start_font.render("Start", True, WHITE)
    start_button = start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    pygame.draw.rect(screen, BLACK, start_button, 2)
    screen.blit(start_text, start_button)

def desenha_chao():
    pygame.draw.line(screen, BLACK, (0, altura_chao), (screen_width, altura_chao), 2)


def mostra_score(score):
    score_text = score_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (570, 10))

def reset_game():
    global dino_y, dino_jump, jump_height, score, game_over, obstacles, obstacle_speed
    dino_y = altura_chao - 50
    dino_jump = False
    jump_height = 0
    score = 0
    game_over = False
    obstacles = []
    obstacle_speed = 7

# Loop principal
running = True
while running:
    screen.blit(background_image, (0, 0))

    if game_over:
        desenha_start()
        game_over_text = game_over_font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (250, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB and game_over:
                reset_game()
            elif event.key == pygame.K_SPACE and not game_over:
                dino.pular()
                jump_sound.play()
            elif event.key == pygame.K_DOWN:
                dino.agachar(True)
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            dino.agachar(False)
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:  # Verifica se o jogo esta parado e se o botao "Start" foi clicado
            mouse_pos = pygame.mouse.get_pos()
            start_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 + 25, 100, 50)
            if start_button.collidepoint(mouse_pos):
                reset_game()

    if not game_over:
        dino.atualizar()

        if pygame.time.get_ticks() - last_obstacle_time > obstacle_frequency:
            obstacles.append(Obstaculo(screen_width, altura_chao))
            last_obstacle_time = pygame.time.get_ticks()

        for obstacle in obstacles:
            obstacle.update_obstaculo()
            if obstacle.checa_colisao(dino):
                game_over = True
                game_over_sound.play()

        obstacles = [o for o in obstacles if not o.fora_da_tela()]

        score += 1

    dino.aloca_dino(screen)
    for obstacle in obstacles:
        obstacle.aloca_obstaculos(screen)
    desenha_chao()
    mostra_score(score)


    pygame.display.update()
    clock.tick(30)

pygame.quit()
