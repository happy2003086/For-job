import pygame
import random

# Initialize Pygame
pygame.init()

# 獲取全螢幕解析度
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Brick Breaker")

# 基礎解析度（原始設計尺寸）
base_width = 800
base_height = 600
scale_x = screen_width / base_width
scale_y = screen_height / base_height

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Paddle dimensions (根據螢幕比例調整)
paddle_width = int(300 * scale_x)  # 將底板寬度調寬
paddle_height = int(15 * scale_y)

# 將打板位置調高 100 像素
paddle_y = screen_height - paddle_height - int(110 * scale_y)  # 調整為更高的 110
paddle_x = (screen_width - paddle_width) // 2

# Ball dimensions and initial speed (根據螢幕比例調整)
ball_radius = int(10 * scale_x)
ball_x = screen_width // 2
ball_y = paddle_y - ball_radius
ball_speed_x = int(5 * scale_x)
ball_speed_y = int(-5 * scale_y)

# Brick properties (動態調整磚塊尺寸)
brick_cols = 8
brick_rows = 5
brick_padding_base = 10  # 基礎間距
brick_width_base = (base_width - (brick_cols + 1) * brick_padding_base) // brick_cols
brick_height_base = 20

# 按比例縮放後的磚塊尺寸
brick_padding = int(brick_padding_base * scale_x)
brick_width = int(brick_width_base * scale_x)
brick_height = int(brick_height_base * scale_y)
bricks = []

# Create bricks (動態計算位置)
for i in range(brick_rows):
    row = []
    for j in range(brick_cols):
        brick_x = j * (brick_width + brick_padding) + brick_padding
        brick_y = i * (brick_height + brick_padding) + int(50 * scale_y)
        row.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))
    bricks.append(row)

# Function to move paddle based on touch
def move_paddle(touch_x):
    global paddle_x
    if touch_x >= 0 and touch_x <= screen_width:
        paddle_x = touch_x - paddle_width // 2
        if paddle_x < 0:
            paddle_x = 0
        elif paddle_x > screen_width - paddle_width:
            paddle_x = screen_width - paddle_width

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # 按ESC退出全螢幕
                running = False
        elif event.type == pygame.MOUSEMOTION:
            touch_x, touch_y = event.pos
            move_paddle(touch_x)

    # Move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball-wall collision
    if ball_x <= ball_radius or ball_x >= screen_width - ball_radius:
        ball_speed_x = -ball_speed_x
    if ball_y <= ball_radius:
        ball_speed_y = -ball_speed_y

    # Ball-paddle collision
    if (
        ball_y + ball_radius >= paddle_y
        and ball_x >= paddle_x
        and ball_x <= paddle_x + paddle_width
    ):
        ball_speed_y = -ball_speed_y

    # Ball-brick collision
    for i in range(brick_rows):
        for j in range(brick_cols):
            if bricks[i][j] and bricks[i][j].colliderect(
                pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
            ):
                bricks[i][j] = None
                ball_speed_y = -ball_speed_y

    # Game over
    if ball_y > screen_height:
        running = False

    # Draw everything
    screen.fill(black)
    pygame.draw.rect(screen, white, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, white, (int(ball_x), int(ball_y)), ball_radius)

    # Draw bricks
    for i in range(brick_rows):
        for j in range(brick_cols):
            if bricks[i][j]:
                pygame.draw.rect(screen, red, bricks[i][j])

    pygame.display.flip()

pygame.quit()
