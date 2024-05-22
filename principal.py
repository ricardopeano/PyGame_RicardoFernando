import pygame
import random
import os
from config import IMG_DIR, FNT_DIR, BLACK, WHITE, SND_DIR, WIDTH, HEIGHT, FPS

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

# Definindo os assets
dino_image_original = pygame.image.load(os.path.join(IMG_DIR, 'de_pe.png'))
dino_ducked_image_original = pygame.image.load(os.path.join(IMG_DIR, 'agachado.png'))
background_image_original = pygame.image.load(os.path.join(IMG_DIR, 'background_dino.jpeg'))

# Configuracoes da tela
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino Game")

# Ajuste do tamanho das imagens
dino_image = pygame.transform.scale(dino_image_original, (50, 50))  # Redimensiona o dinossauro para 50x50 pixels
dino_ducked_image = pygame.transform.scale(dino_ducked_image_original, (50, 35))  # Redimensiona o dinossauro agachado para 50x35 pixels
background_image = pygame.transform.scale(background_image_original, (screen_width, screen_height))  # Ajusta o background para cobrir a tela

alt_visual_chao = 40  # Altura visual do chao a partir da parte inferior da tela
altura_chao = screen_height - alt_visual_chao  

# Definicao de variaveis 

dino_x = 50
dino_y = altura_chao - dino_image.get_height()
dino_jump = False
initial_jump_height = 10  
jump_height = 0
gravity = 1
ducking = False
score = 0
game_over = True  # Inicialmente True para mostrar o botao start
obstacles = []
obstacle_speed = 7
obstacle_frequency = 1500
last_obstacle_time = 0

clock = pygame.time.Clock()

# Funcao para colocar o dinossauro na tela
def aloca_dino(x, y, ducking):
    if ducking:
        screen.blit(dino_ducked_image, (x, y + 20))  # Ajusta a posicao em y quando agachado
    else:
        screen.blit(dino_image, (x, y))

# Funcao para desenhar o chao
def desenha_chao():
    pygame.draw.line(screen, BLACK, (0, altura_chao), (screen_width, altura_chao), 2)

# Funcao para desenhar obstaculos
def aloca_obstaculos(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))

# Funcao para atualizar obstaculos
def update_obstaculos(obstacles, speed):
    for obstacle in obstacles:
        obstacle[0] -= speed
    obstacles[:] = [ob for ob in obstacles if ob[0] > -ob[2]]

# Funcao para colocar os obstaculos no jogo
def add_obstaculo():
    if random.randint(0, 1) == 0:
        height = random.randint(20, 40)
        y_pos = altura_chao - height 
    else:
        height = 30
        y_pos = altura_chao - height - 40
    width = 20
    obstacles.append([screen_width, y_pos, width, height])

# Funcao para verificar colisoes
def checa_colisao(obstacles, dino_x, dino_y, dino_width, dino_height, ducking):
    effective_dino_height = dino_ducked_image.get_height() if ducking else dino_height
    effective_dino_y = dino_y + 20 if ducking else dino_y  
    dino_rect = pygame.Rect(dino_x, effective_dino_y, dino_width, effective_dino_height)
    for obstacle in obstacles:
        if dino_rect.colliderect(pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3])):
            return True
    return False

# Funcao para mostrar o score
def mostra_score(score):
    score_text = score_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (570, 10))

def reset_game():
    global dino_y, dino_jump, jump_height, score, game_over, obstacles, obstacle_speed
    dino_y = altura_chao - dino_image.get_height()
    dino_jump = False
    jump_height = 0
    score = 0
    game_over = False
    obstacles = []
    obstacle_speed = 7

# Funcao para desenhar o botao "Start"
def desenha_start():
    font = pygame.font.Font(None, 60)
    start_text = start_font.render("Start", True, WHITE)
    start_button = start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    pygame.draw.rect(screen, BLACK, start_button, 2)
    screen.blit(start_text, start_button)


# Loop principal do jogo
running = True
while running:
    screen.blit(background_image, (0, 0))

    # Se o jogo estiver parado, desenha o botao "Start"
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
            elif event.key == pygame.K_SPACE and not ducking and not dino_jump and not game_over:
                dino_jump = True
                jump_height = initial_jump_height
                jump_sound.play()  
            elif event.key == pygame.K_DOWN and not game_over:
                ducking = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            ducking = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:  # Verifica se o jogo esta parado e se o botao "Start" foi clicado
            mouse_pos = pygame.mouse.get_pos()
            start_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 + 25, 100, 50)
            if start_button.collidepoint(mouse_pos):
                reset_game()

    if not game_over:
        if dino_jump:
            dino_y -= jump_height
            jump_height -= gravity
            if dino_y > altura_chao - dino_image.get_height():
                dino_y = altura_chao - dino_image.get_height()
                dino_jump = False
                jump_height = 0

        if pygame.time.get_ticks() - last_obstacle_time > obstacle_frequency:
            add_obstaculo()
            last_obstacle_time = pygame.time.get_ticks()

        update_obstaculos(obstacles, obstacle_speed)
        game_over = checa_colisao(obstacles, dino_x, dino_y, dino_image.get_width(), dino_image.get_height(), ducking)

        if game_over:
            game_over_sound.play()  

        score += 1
        if score <= 3000:
            if score % 100 == 0:
                obstacle_speed += 1

        # Condicao de vitoria do jogo:
        if score >= 5000:
            game_over = True
            game_over_sound.play()  

    aloca_dino(dino_x, dino_y, ducking)
    aloca_obstaculos(obstacles)
    desenha_chao()
    mostra_score(score)

    pygame.display.update()
    clock.tick(30)

pygame.quit()