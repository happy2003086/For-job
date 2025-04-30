import pygame
import sys
import random
import math

# 初始化pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("弹球与收缩边框")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 球的属性
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

# 初始隨機速度與方向
initial_speed = random.uniform(5, 8)
angle = random.uniform(0, 2 * math.pi)
ball_speed_x = initial_speed * math.cos(angle)
ball_speed_y = initial_speed * math.sin(angle)

# 边框属性
border_radius = min(WIDTH, HEIGHT) // 2 - 50
border_thickness = 5
border_shrink_amount = 5
min_border_radius = 50

# 加速設定
is_accelerating = False
normal_speed = 1.0
boost_speed = 2.0

# 加速按鈕（虛擬A鍵）
a_button_rect = pygame.Rect(50, HEIGHT - 100, 80, 50)

# 遊戲時鐘
clock = pygame.time.Clock()

# 遊戲主循環
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if a_button_rect.collidepoint(event.pos):
                is_accelerating = True

        elif event.type == pygame.MOUSEBUTTONUP:
            is_accelerating = False

    # 設定速度倍數
    speed_multiplier = boost_speed if is_accelerating else normal_speed

    # 更新球的位置
    ball_x += ball_speed_x * speed_multiplier
    ball_y += ball_speed_y * speed_multiplier

    # 計算與中心距離
    dx = ball_x - WIDTH // 2
    dy = ball_y - HEIGHT // 2
    distance = math.sqrt(dx**2 + dy**2)

    # 撞到邊框
    if distance + ball_radius > border_radius:
        nx = dx / distance
        ny = dy / distance

        dot_product = ball_speed_x * nx + ball_speed_y * ny
        ball_speed_x = ball_speed_x - 2 * dot_product * nx
        ball_speed_y = ball_speed_y - 2 * dot_product * ny

        ball_speed_x += random.uniform(-0.5, 0.5)
        ball_speed_y += random.uniform(-0.5, 0.5)

        speed = math.sqrt(ball_speed_x**2 + ball_speed_y**2)
        if speed > 8:
            ball_speed_x = ball_speed_x / speed * 8
            ball_speed_y = ball_speed_y / speed * 8
        elif speed < 3:
            ball_speed_x = ball_speed_x / speed * 3
            ball_speed_y = ball_speed_y / speed * 3

        if border_radius > min_border_radius:
            border_radius -= border_shrink_amount
            border_radius = max(border_radius, min_border_radius)

            if distance + ball_radius > border_radius:
                ratio = (border_radius - ball_radius) / distance
                ball_x = WIDTH // 2 + dx * ratio
                ball_y = HEIGHT // 2 + dy * ratio

    # 清屏
    screen.fill(BLACK)

    # 畫邊框
    pygame.draw.circle(screen, BLUE, (WIDTH // 2, HEIGHT // 2), border_radius, border_thickness)

    # 畫球
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    # 畫加速按鈕
    pygame.draw.rect(screen, BLUE, a_button_rect)
    font = pygame.font.SysFont(None, 36)
    text = font.render("A", True, WHITE)
    screen.blit(text, (a_button_rect.x + 25, a_button_rect.y + 10))

    # 更新畫面
    pygame.display.flip()
    clock.tick(60)

# 離開遊戲
pygame.quit()
sys.exit()
