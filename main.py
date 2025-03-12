import pygame
import os
from config import IMG_DIR, FNT_DIR, BLACK, WHITE, SND_DIR
from dinossauro import Dinossauro
from obstaculos import Obstaculo

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

# Configuracoes da tela
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino Game")

# Definindo o fundo do jogo
background_image_original = pygame.image.load(os.path.join(IMG_DIR, 'background_dino.jpeg'))
background_image = pygame.transform.scale(background_image_original, (screen_width, screen_height))

# Criando objetos do jogo
altura_chao = screen_height - 40  # Altura do chão
dino = Dinossauro(altura_chao)
obstaculos = []
obstacle_speed = 7
obstacle_frequency = 1500
last_obstacle_time = 0

score = 0
game_over = True  # Inicialmente True para mostrar o botao start
clock = pygame.time.Clock()

# Função para resetar o jogo
def reset_game():
    global score, game_over, obstaculos, obstacle_speed
    dino.y = altura_chao - dino.dino_image.get_height()
    dino.jump = False
    dino.jump_height = 0
    score = 0
    game_over = False
    obstaculos = []
    obstacle_speed = 7

# Função para desenhar o botão "Start"
def desenha_start():
    start_text = start_font.render("Start", True, WHITE)
    start_button = start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    pygame.draw.rect(screen, BLACK, start_button, 2)
    screen.blit(start_text, start_button)
    return start_button

# Loop principal do jogo
running = True
while running:
    screen.blit(background_image, (0, 0))

    # Se o jogo estiver parado, desenha o botão "Start"
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
            elif event.key == pygame.K_SPACE and not dino.ducking and not dino.jump and not game_over:
                dino.pular()
                jump_sound.play()
            elif event.key == pygame.K_DOWN and not game_over:
                dino.abaixar()
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            dino.soltar_abaixar()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            start_button = desenha_start()
            if start_button.collidepoint(mouse_pos):
                reset_game()

    if not game_over:
        dino.atualizar()

        if pygame.time.get_ticks() - last_obstacle_time > obstacle_frequency:
            obstaculos.append(Obstaculo(screen_width, altura_chao))
            last_obstacle_time = pygame.time.get_ticks()

        for obstaculo in obstaculos:
            obstaculo.mover(obstacle_speed)

        obstaculos = [ob for ob in obstaculos if ob.x > -ob.largura]

        game_over = any(dino.checa_colisao(obstaculo) for obstaculo in obstaculos)

        if game_over:
            game_over_sound.play()

        score += 1
        if score <= 3000 and score % 100 == 0:
            obstacle_speed += 1

        if score >= 5000:
            game_over = True
            game_over_sound.play()

    dino.desenhar(screen)
    for obstaculo in obstaculos:
        obstaculo.desenhar(screen)

    pygame.draw.line(screen, BLACK, (0, altura_chao), (screen_width, altura_chao), 2)

    score_text = score_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (570, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
