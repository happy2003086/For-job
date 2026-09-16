import pygame
import random
import sys
import time

pygame.init()

# 1. 自動取得手機/螢幕嘅實際解像度
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# 如果係喺 PC 測試，想要固定比例，可以改用以下（或保持全螢幕模式）：
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper (Mobile Auto-Fit)")

GRID_SIZE = 10  # 10x10 網格

# 2. 動態計算格子大小：確保棋盤能完整放入螢幕寬度內（並留少許 Margin）
CELL_WIDTH = SCREEN_WIDTH // GRID_SIZE
CELL_HEIGHT = CELL_WIDTH  # 保持正方形

# 計算棋盤總高寬，並讓棋盤在螢幕居中（垂直/水平 offset）
BOARD_WIDTH = CELL_WIDTH * GRID_SIZE
BOARD_HEIGHT = CELL_HEIGHT * GRID_SIZE
OFFSET_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 3  # 偏上一點，留下方空間給手勢或UI

MARGIN = 2
MINE_COUNT = 10
LONG_PRESS_TIME = 0.5

COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GRAY': (192, 192, 192),
    'DARK_GRAY': (60, 60, 60),
    'RED': (255, 50, 50),
    'TEXT_COLORS': [
        (0, 0, 0),          # 0 唔顯示
        (0, 122, 255),      # 1 藍
        (52, 199, 89),      # 2 綠
        (255, 59, 48),      # 3 紅
        (88, 86, 214),      # 4 紫
        (255, 149, 0),      # 5 橙
        (90, 200, 250),     # 6 青
        (0, 0, 0),          # 7 黑
        (142, 142, 147)     # 8 灰
    ]
}

font = pygame.font.SysFont('Arial', int(CELL_WIDTH * 0.5), bold=True)

class Minesweeper:
    def __init__(self):
        self.reset_game()
        self.press_start_time = 0
        self.press_pos = None

    def reset_game(self):
        self.grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.revealed = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.flagged = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.game_over = False
        self.win = False
        self.first_click = True

    def place_mines(self, exclude_x, exclude_y):
        safe_zone = [(exclude_x+dx, exclude_y+dy) 
                    for dx in (-1,0,1) for dy in (-1,0,1)
                    if 0 <= exclude_x+dx < GRID_SIZE and 0 <= exclude_y+dy < GRID_SIZE]
        
        candidates = [(x,y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)
                     if (x,y) not in safe_zone]
        
        mine_spots = random.sample(candidates, MINE_COUNT)
        for x,y in mine_spots:
            self.grid[y][x] = -1
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if self.grid[ny][nx] != -1:
                            self.grid[ny][nx] += 1

    def reveal(self, x, y):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return
        if self.revealed[y][x] or self.flagged[y][x]:
            return
            
        if self.first_click:
            self.place_mines(x, y)
            self.first_click = False
            
        self.revealed[y][x] = True
        
        if self.grid[y][x] == -1:
            self.game_over = True
            self.reveal_all_mines()
        elif self.grid[y][x] == 0:
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    if (dx, dy) != (0, 0):
                        self.reveal(x+dx, y+dy)
        self.check_win()

    def reveal_all_mines(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == -1:
                    self.revealed[y][x] = True

    def toggle_flag(self, x, y):
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            if not self.revealed[y][x] and not self.game_over:
                self.flagged[y][x] ^= True
        self.check_win()

    def check_win(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == -1 and not self.flagged[y][x]:
                    return
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    return
        self.game_over = True
        self.win = True

    def draw(self):
        buffer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        buffer.fill(COLORS['BLACK'])
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                # 結合 OFFSET 畫出置中的網格
                rect = pygame.Rect(
                    OFFSET_X + x*CELL_WIDTH + MARGIN, 
                    OFFSET_Y + y*CELL_HEIGHT + MARGIN,
                    CELL_WIDTH - 2*MARGIN,
                    CELL_HEIGHT - 2*MARGIN
                )
                                 
                if self.revealed[y][x]:
                    pygame.draw.rect(buffer, COLORS['GRAY'], rect, border_radius=4)
                    if self.grid[y][x] > 0:
                        val = self.grid[y][x]
                        color = COLORS['TEXT_COLORS'][val] if val < len(COLORS['TEXT_COLORS']) else COLORS['WHITE']
                        text = font.render(str(val), True, color)
                        buffer.blit(text, text.get_rect(center=rect.center))
                    elif self.grid[y][x] == -1:
                        pygame.draw.circle(buffer, COLORS['BLACK'], rect.center, min(CELL_WIDTH, CELL_HEIGHT)//4)
                else:
                    pygame.draw.rect(buffer, COLORS['DARK_GRAY'], rect, border_radius=4)
                    if self.flagged[y][x]:
                        # 畫菱形旗子
                        cx, cy = rect.center
                        r = CELL_WIDTH // 4
                        pygame.draw.polygon(buffer, COLORS['RED'], [
                            (cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)
                        ])

        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,200))
            buffer.blit(overlay, (0,0))
            
            msg = "You Win!" if self.win else "Game Over!"
            text = font.render(msg, True, COLORS['WHITE'])
            sub_text = pygame.font.SysFont('Arial', int(CELL_WIDTH * 0.3)).render("Tap anywhere to restart", True, COLORS['GRAY'])
            
            buffer.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))
            buffer.blit(sub_text, sub_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))
            
        screen.blit(buffer, (0,0))
        pygame.display.flip()

# 轉換螢幕點擊座標為棋盤格陣列 (x, y)
def get_grid_pos(pos):
    px, py = pos
    gx = (px - OFFSET_X) // CELL_WIDTH
    gy = (py - OFFSET_Y) // CELL_HEIGHT
    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
        return gx, gy
    return None

game = Minesweeper()

while True:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            grid_pos = get_grid_pos(event.pos)
            if grid_pos:
                game.press_pos = grid_pos
                game.press_start_time = current_time
            elif game.game_over:
                game.reset_game()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if game.game_over:
                game.reset_game()
            elif game.press_pos:
                grid_pos = get_grid_pos(event.pos)
                if grid_pos == game.press_pos:
                    x, y = grid_pos
                    if current_time - game.press_start_time >= LONG_PRESS_TIME:
                        game.toggle_flag(x, y)
                    else:
                        game.reveal(x, y)
                game.press_pos = None
    
    game.draw()
    pygame.time.wait(30)
