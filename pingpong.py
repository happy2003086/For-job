import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

# 球的屬性
x, y = 250, 100
radius = 20
speed_y = 10  # 初始速度
gravity = -0.5  # 減少速度模擬摩擦
running = True

while running:
    screen.fill((0, 0, 0))  # 黑色背景
    pygame.draw.circle(screen, (255, 0, 0), (x, int(y)), radius)  # 畫紅色球

    # 更新球的垂直位置
    y += speed_y
    speed_y -= gravity  # 模擬重力影響

    # 碰到底部時反彈
    if y + radius >= 500:
        y = 500 - radius
        speed_y = -speed_y * 0.8  # 每次反彈時速度減小

        # 速度足夠小時停止彈跳
        if abs(speed_y) < 1:
            speed_y = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)  # 控制動畫幀率

pygame.quit()
