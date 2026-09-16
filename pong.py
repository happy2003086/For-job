import pygame
import random

# Initialize pygame
pygame.init()

# Get screen size for Android device
info = pygame.display.Info()
# 将屏幕大小缩小至80%
width = int(info.current_w * 0.8)
height = int(info.current_h * 0.8)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the paddle and ball
paddle_width, paddle_height = 15, 90
ball_width = 20
paddle_speed = 30
ball_speed_x = 20
ball_speed_y = 20

# Font for score
font = pygame.font.SysFont('Arial', 30)

# Set up paddles and ball
player1_x, player1_y = 30, height // 2 - paddle_height // 2
player2_x, player2_y = width - 30 - paddle_width, height // 2 - paddle_height // 2
ball_x, ball_y = width // 2 - ball_width // 2, height // 2 - ball_width // 2
ball_dx, ball_dy = random.choice([-1, 1]) * ball_speed_x, random.choice([-1, 1]) * ball_speed_y

# Initialize scores
score1, score2 = 0, 0

# Game loop
running = True
while running:
    screen.fill(black)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Touch controls for paddles
    touch_events = pygame.mouse.get_pos()
    player1_y = touch_events[1] - paddle_height // 2
    
    # 确保左球拍不超出屏幕边界
    if player1_y < 0:
        player1_y = 0
    elif player1_y > height - paddle_height:
        player1_y = height - paddle_height

    # Player 2 movement (auto or touch-based for two players)
    if player2_y < ball_y - paddle_height // 2:
        player2_y += paddle_speed
    elif player2_y > ball_y - paddle_height // 2:
        player2_y -= paddle_speed
    
    # 确保右球拍不超出屏幕边界
    if player2_y < 0:
        player2_y = 0
    elif player2_y > height - paddle_height:
        player2_y = height - paddle_height

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # 球的顶部和底部碰撞，防止球打出屏幕
    if ball_y <= 0:
        ball_y = 0
        ball_dy = -ball_dy
    # 球的底部碰撞检测，防止球打出屏幕下面
    if ball_y >= height - ball_width:
        ball_y = height - ball_width
        ball_dy = -ball_dy

    # Collision with paddles
    if (ball_x <= player1_x + paddle_width and player1_y < ball_y + ball_width and player1_y + paddle_height > ball_y):
        ball_dx = -ball_dx
        # 防止球卡在球拍里
        ball_x = player1_x + paddle_width
    if (ball_x + ball_width >= player2_x and player2_y < ball_y + ball_width and player2_y + paddle_height > ball_y):
        ball_dx = -ball_dx
        # 防止球卡在球拍里
        ball_x = player2_x - ball_width

    # Ball out of bounds (scoring)
    if ball_x <= 0:
        score2 += 1
        ball_x, ball_y = width // 2 - ball_width // 2, height // 2 - ball_width // 2
        ball_dx, ball_dy = random.choice([-1, 1]) * ball_speed_x, random.choice([-1, 1]) * ball_speed_y

    if ball_x >= width - ball_width:
        score1 += 1
        ball_x, ball_y = width // 2 - ball_width // 2, height // 2 - ball_width // 2
        ball_dx, ball_dy = random.choice([-1, 1]) * ball_speed_x, random.choice([-1, 1]) * ball_speed_y

    # Draw paddles and ball
    pygame.draw.rect(screen, white, (player1_x, player1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (player2_x, player2_y, paddle_width, paddle_height))
    pygame.draw.ellipse(screen, white, (ball_x, ball_y, ball_width, ball_width))

    # Display score
    score_text = font.render(f"{score1} - {score2}", True, white)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit pygame
pygame.quit()