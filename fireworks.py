import pygame
import random
import math

# 初始化 Pygame
pygame.init()

# 畫面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 粒子類
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 60  # 壽命 (約 1 秒)
        self.color = (255, 255, 255)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  # 模擬重力
        self.life -= 1
        if self.life < 30:
            self.color = (255, 165, 0)  # 變成橙色

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)

# 煙花列表
particles = []

running = True
while running:
    screen.fill((0, 0, 0))  # 清空畫面

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 按下滑鼠左鍵，產生煙花
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            for _ in range(100):
                particles.append(Particle(x, y))

    # 更新 & 畫出所有粒子
    for p in particles[:]:
        p.update()
        p.draw(screen)
        if p.life <= 0:
            particles.remove(p)

    pygame.display.flip()
    clock.tick(60)  # 限制 FPS

pygame.quit()
