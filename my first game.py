import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 設定屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 顏色定義
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 玩家設定
player_size = 50
player_pos = [screen_width // 2, screen_height // 2]

# 障礙物設定
obstacle_size = 50
obstacle_pos = [random.randint(0, screen_width - obstacle_size), 0]
obstacle_speed = 10

# 計分設定
start_time = time.time()
game_over = False
clock = pygame.time.Clock()

while not game_over:
    # 計算經過的時間
    elapsed_time = int(time.time() - start_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN:  # 檢查觸控事件
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player_pos[0] = mouse_x - player_size // 2  # 將玩家移至觸控位置
            player_pos[1] = mouse_y - player_size // 2

    # 更新障礙物位置
    obstacle_pos[1] += obstacle_speed
    if obstacle_pos[1] > screen_height:
        obstacle_pos[1] = 0
        obstacle_pos[0] = random.randint(0, screen_width - obstacle_size)

    # 碰撞檢測
    if (player_pos[0] < obstacle_pos[0] < player_pos[0] + player_size or
            player_pos[0] < obstacle_pos[0] + obstacle_size < player_pos[0] + player_size) and \
            (player_pos[1] < obstacle_pos[1] < player_pos[1] + player_size or
            player_pos[1] < obstacle_pos[1] + obstacle_size < player_pos[1] + player_size):
        game_over = True

    # 畫面更新
    screen.fill(white)
    pygame.draw.rect(screen, black, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.draw.rect(screen, red, (obstacle_pos[0], obstacle_pos[1], obstacle_size, obstacle_size))

    # 顯示計分
    font = pygame.font.Font(None, 36)
    text = font.render(f'Time: {elapsed_time} seconds', True, black)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(30)

# 遊戲結束後顯示總時間
screen.fill(white)
final_text = font.render(f'Game Over! Total Time: {elapsed_time} seconds', True, black)
screen.blit(final_text, (screen_width // 2 - final_text.get_width() // 2, screen_height // 2 - final_text.get_height() // 2))
pygame.display.update()

# 等待用戶關閉窗口
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False

pygame.quit()
