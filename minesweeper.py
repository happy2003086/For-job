import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_SIZE = 600  # Smaller window size
GRID_SIZE = 10
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
MINE_COUNT = 15
MARGIN = 2
LONG_PRESS_TIME = 0.5  # seconds threshold for long primport pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_SIZE = 600  # Smaller window size
GRID_SIZE = 10
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
MINE_COUNT = 15
MARGIN = 2
LONG_PRESS_TIME = 0.5  # seconds threshold for long press

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
COLORS = [
    None, BLUE, GREEN, RED, (0, 0, 128), (128, 0, 0),
    (0, 128, 128), BLACK, DARK_GRAY
]

# Create game window
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Touch Minesweeper (Long press to flag)")

# Font setup
font = pygame.font.SysFont('Arial', CELL_SIZE // 2)

class Minesweeper:
    def __init__(self):
        self.reset_game()
        self.press_start_time = 0
        self.press_pos = None
    
    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.flagged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.game_over = False
        self.win = False
        self.first_click = True
        self.place_mines()
    
    def place_mines(self):
        if not self.first_click:
            mines_placed = 0
            while mines_placed < MINE_COUNT:
                x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    self.grid[y][x] = -1
                    mines_placed += 1

                    # Update numbers around mines
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.grid[ny][nx] != -1:
                                self.grid[ny][nx] += 1
    
    def reveal(self, x, y):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE) or self.revealed[y][x] or self.flagged[y][x]:
            return
        
        if self.first_click:
            self.first_click = False
            self.place_mines()
        
        self.revealed[y][x] = True
        
        if self.grid[y][x] == -1:  # Hit a mine
            self.game_over = True
            self.reveal_all_mines()
        elif self.grid[y][x] == 0:  # Empty cell, auto reveal neighbors
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    self.reveal(x + dx, y + dy)
        
        self.check_win()
    
    def reveal_all_mines(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == -1:
                    self.revealed[y][x] = True
    
    def toggle_flag(self, x, y):
        if not self.revealed[y][x] and not self.game_over:
            self.flagged[y][x] = not self.flagged[y][x]
    
    def check_win(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    return
        self.game_over = True
        self.win = True
    
    def draw(self):
        screen.fill(BLACK)
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(
                    x * CELL_SIZE + MARGIN,
                    y * CELL_SIZE + MARGIN,
                    CELL_SIZE - 2 * MARGIN,
                    CELL_SIZE - 2 * MARGIN
                )
                
                if self.revealed[y][x]:
                    pygame.draw.rect(screen, GRAY, rect)
                    if self.grid[y][x] > 0:
                        text = font.render(str(self.grid[y][x]), True, COLORS[self.grid[y][x]])
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                    elif self.grid[y][x] == -1:
                        pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE // 4)  # white mine
                else:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    if self.flagged[y][x]:
                        pygame.draw.polygon(screen, RED, [
                            (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 2),
                            (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 4),
                            (x * CELL_SIZE + 3 * CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 2),
                            (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + 3 * CELL_SIZE // 4)
                        ])
        
        # Show press instructions
        help_text = font.render("Tap: Reveal  Long press: Flag", True, WHITE)
        screen.blit(help_text, (10, SCREEN_SIZE - 30))
        
        if self.game_over:
            overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            message = "You Win!" if self.win else "Game Over!"
            text = font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
            screen.blit(text, text_rect)
            
            restart_text = font.render("Click to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 + CELL_SIZE))
            screen.blit(restart_text, restart_rect)

# Create game instance
game = Minesweeper()

# Main game loop
running = True
while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left button down
                game.press_pos = (event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE)
                game.press_start_time = current_time
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and game.press_pos:  # Left button up
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                press_duration = current_time - game.press_start_time
                
                # Check if released on the same cell
                if (x, y) == game.press_pos:
                    if game.game_over:
                        game.reset_game()  # Restart game after over
                    elif press_duration >= LONG_PRESS_TIME:
                        game.toggle_flag(x, y)  # Long press flag
                    else:
                        game.reveal(x, y)  # Short tap reveal
                
                game.press_pos = None
    
    # Draw everything
    game.draw()
    
    # Highlight flag on long press
    if game.press_pos and (current_time - game.press_start_time) > LONG_PRESS_TIME:
        x, y = game.press_pos
        pygame.draw.rect(screen, RED, (
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        ), 3)
    
    pygame.display.flip()

pygame.quit()
sys.exit()



# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
COLORS = [
    None, BLUE, GREEN, RED, (0, 0, 128), (128, 0, 0),
    (0, 128, 128), BLACK, DARK_GRAY
]

# Create game window
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Touch Minesweeper (Long press to flag)")

# Font setup
font = pygame.font.SysFont('Arial', CELL_SIZE // 2)

class Minesweeper:
    def __init__(self):
        self.reset_game()
        self.press_start_time = 0
        self.press_pos = None
    
    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.flagged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.game_over = False
        self.win = False
        self.first_click = True
        self.place_mines()
    
    def place_mines(self):
        if not self.first_click:
            mines_placed = 0
            while mines_placed < MINE_COUNT:
                x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    self.grid[y][x] = -1
                    mines_placed += 1

                    # Update numbers around mines
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.grid[ny][nx] != -1:
                                self.grid[ny][nx] += 1
    
    def reveal(self, x, y):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE) or self.revealed[y][x] or self.flagged[y][x]:
            return
        
        if self.first_click:
            self.first_click = False
            self.place_mines()
        
        self.revealed[y][x] = True
        
        if self.grid[y][x] == -1:  # Hit a mine
            self.game_over = True
            self.reveal_all_mines()
        elif self.grid[y][x] == 0:  # Empty cell, auto reveal neighbors
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    self.reveal(x + dx, y + dy)
        
        self.check_win()
    
    def reveal_all_mines(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == -1:
                    self.revealed[y][x] = True
    
    def toggle_flag(self, x, y):
        if not self.revealed[y][x] and not self.game_over:
            self.flagged[y][x] = not self.flagged[y][x]
    
    def check_win(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    return
        self.game_over = True
        self.win = True
    
    def draw(self):
        screen.fill(BLACK)
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(
                    x * CELL_SIZE + MARGIN,
                    y * CELL_SIZE + MARGIN,
                    CELL_SIZE - 2 * MARGIN,
                    CELL_SIZE - 2 * MARGIN
                )
                
                if self.revealed[y][x]:
                    pygame.draw.rect(screen, GRAY, rect)
                    if self.grid[y][x] > 0:
                        text = font.render(str(self.grid[y][x]), True, COLORS[self.grid[y][x]])
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                    elif self.grid[y][x] == -1:
                        pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE // 4)  # white mine
                else:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    if self.flagged[y][x]:
                        pygame.draw.polygon(screen, RED, [
                            (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 2),
                            (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 4),
                            (x * CELL_SIZE + 3 * CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 2),
                            (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + 3 * CELL_SIZE // 4)
                        ])
        
        # Show press instructions
        help_text = font.render("Tap: Reveal  Long press: Flag", True, WHITE)
        screen.blit(help_text, (10, SCREEN_SIZE - 30))
        
        if self.game_over:
            overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            message = "You Win!" if self.win else "Game Over!"
            text = font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
            screen.blit(text, text_rect)
            
            restart_text = font.render("Click to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 + CELL_SIZE))
            screen.blit(restart_text, restart_rect)

# Create game instance
game = Minesweeper()

# Main game loop
running = True
while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left button down
                game.press_pos = (event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE)
                game.press_start_time = current_time
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and game.press_pos:  # Left button up
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                press_duration = current_time - game.press_start_time
                
                # Check if released on the same cell
                if (x, y) == game.press_pos:
                    if game.game_over:
                        game.reset_game()  # Restart game after over
                    elif press_duration >= LONG_PRESS_TIME:
                        game.toggle_flag(x, y)  # Long press flag
                    else:
                        game.reveal(x, y)  # Short tap reveal
                
                game.press_pos = None
    
    # Draw everything
    game.draw()
    
    # Highlight flag on long press
    if game.press_pos and (current_time - game.press_start_time) > LONG_PRESS_TIME:
        x, y = game.press_pos
        pygame.draw.rect(screen, RED, (
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        ), 3)
    
    pygame.display.flip()

pygame.quit()
sys.exit()

