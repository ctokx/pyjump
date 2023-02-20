import pygame
import random

# Define constants
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
PIPE_GAP = 100
PIPE_SPEED = 2
GRAVITY = 0.2
JUMP_SPEED = -4

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load font
font = pygame.font.Font(None, 40)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define game variables
score = 0
game_over = False

# Define game objects
bird = pygame.Rect(50, 200, 30, 30)
pipes = []

# Define functions
def draw_bird():
    pygame.draw.rect(screen, WHITE, bird)

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, WHITE, pipe['top'])
        pygame.draw.rect(screen, WHITE, pipe['bottom'])

def move_pipes():
    for pipe in pipes:
        pipe['top'].x -= PIPE_SPEED
        pipe['bottom'].x -= PIPE_SPEED

def generate_pipes():
    top_height = random.randint(100, 300)
    bottom_height = SCREEN_HEIGHT - top_height - PIPE_GAP
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, 50, top_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, top_height + PIPE_GAP, 50, bottom_height)
    pipes.append({'top': top_pipe, 'bottom': bottom_pipe})

def check_collision():
    for pipe in pipes:
        if bird.colliderect(pipe['top']) or bird.colliderect(pipe['bottom']):
            return True
    if bird.y < 0 or bird.y > SCREEN_HEIGHT:
        return True
    return False

def update_score():
    global score
    for pipe in pipes:
        if pipe['top'].x + pipe['top'].width < bird.x:
            score += 1

def draw_score():
    score_surface = font.render(str(score), True, WHITE)
    screen.blit(score_surface, (SCREEN_WIDTH - score_surface.get_width() - 10, 10))

def draw_game_over():
    game_over_surface = font.render('Game Over', True, WHITE)
    screen.blit(game_over_surface, (SCREEN_WIDTH/2 - game_over_surface.get_width()/2, SCREEN_HEIGHT/2 - game_over_surface.get_height()/2))

# Game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            bird.y += JUMP_SPEED*5
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            bird.y -= JUMP_SPEED *5

    # Update game objects
    bird.y += GRAVITY
    move_pipes()
    if len(pipes) == 0 or pipes[-1]['top'].x < SCREEN_WIDTH - 150:
        generate_pipes()
    if check_collision():
        game_over = True
    update_score()

    # Draw screen
    screen.fill(BLACK)
    draw_bird()
    draw_pipes()
    draw_score()
    if game_over:
        draw_game_over()
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
