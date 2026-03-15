import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 手機竪屏尺寸
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
GRAVITY = 0.5
JUMP_SPEED = -10
PIPE_SPEED = 3
PIPE_GAP = 220
PIPE_WIDTH = 60
BIRD_SIZE = 25
PIPE_FREQUENCY = 1500

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)
GROUND_BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

# 建立視窗
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mobile Flappy Bird")

class Bird:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//4, SCREEN_HEIGHT//2, BIRD_SIZE, BIRD_SIZE)
        self.speed = 0
        self.tilt = 0

    def jump(self):
        self.speed = JUMP_SPEED
        self.tilt = 30

    def move(self):
        self.speed += GRAVITY
        self.rect.y += self.speed
        self.tilt = max(min(-self.speed * 3, 30), -30)

    def draw(self):
        pygame.draw.ellipse(screen, YELLOW, self.rect)
        if abs(self.tilt) < 15:
            pygame.draw.circle(screen, BLACK, (self.rect.right-8, self.rect.top+8), 3)
        beak_width = 10 if self.speed > 0 else 15
        pygame.draw.polygon(screen, (255,165,0), [
            (self.rect.right, self.rect.centery),
            (self.rect.right+beak_width, self.rect.centery),
            (self.rect.right, self.rect.centery+3)
        ])

class Pipe:
    def __init__(self, x):
        min_gap = int(SCREEN_HEIGHT*0.25)
        self.gap_y = random.randint(min_gap, SCREEN_HEIGHT - min_gap - PIPE_GAP)
        self.top = pygame.Rect(x, 0, PIPE_WIDTH, self.gap_y)
        self.bottom = pygame.Rect(x, self.gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)
        self.passed = False

    def move(self):
        self.top.x -= PIPE_SPEED
        self.bottom.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top)
        pygame.draw.rect(screen, (0,100,0), self.top.inflate(0,15).move(0,-7))
        pygame.draw.rect(screen, GREEN, self.bottom)
        pygame.draw.rect(screen, (0,100,0), self.bottom.inflate(0,15).move(0,7))

# 初始化遊戲
bird = Bird()
pipes = []
last_pipe = pygame.time.get_ticks()
score = 0
active = True
font = pygame.font.Font(None, 40)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if active:
                bird.jump()
            else:
                bird = Bird()
                pipes = []
                score = 0
                active = True

    if active:
        if pygame.time.get_ticks() - last_pipe > PIPE_FREQUENCY:
            pipes.append(Pipe(SCREEN_WIDTH))
            last_pipe = pygame.time.get_ticks()

        bird.move()
        for pipe in pipes:
            pipe.move()

        for pipe in pipes:
            if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                active = False
        if bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
            active = False

        for pipe in pipes:
            if not pipe.passed and pipe.top.right < bird.rect.left:
                score += 1
                pipe.passed = True

    screen.fill(SKY_BLUE)
    ground_y = SCREEN_HEIGHT-50
    pygame.draw.rect(screen, GROUND_BROWN, (0, ground_y, SCREEN_WIDTH, 50))

    for pipe in pipes:
        pipe.draw()

    bird.draw()

    score_surface = font.render(f"{score}", True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH//2, 50))
    screen.blit(score_surface, score_rect)

    if not active:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        final_score_text = font.render(f"Score: {score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
        screen.blit(final_score_text, final_score_rect)

        text = font.render("Tap to Restart", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)