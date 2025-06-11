import random
import time
import shutil
from collections import defaultdict
from datetime import datetime
import os
import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Game constants
BOARD_SIZE = 15
CELL_SIZE = 60
BOARD_PADDING = 50
WINDOW_SIZE = BOARD_PADDING * 2 + CELL_SIZE * (BOARD_SIZE - 1)
BUTTON_HEIGHT = 40
INFO_HEIGHT = 80
TOTAL_HEIGHT = WINDOW_SIZE + BUTTON_HEIGHT + INFO_HEIGHT

# Color definitions
BACKGROUND = (220, 179, 92)
LINE_COLOR = (0, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 150, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)
INFO_BG = (50, 50, 50)

# Create window
screen = pygame.display.set_mode((WINDOW_SIZE, TOTAL_HEIGHT))
pygame.display.set_caption("Gomoku Game")

# Fonts
font = pygame.font.SysFont(None, 24)
title_font = pygame.font.SysFont(None, 36)

# Piece scoring rules - enhanced version
PATTERN_SCORES = {
    'FIVE': 1000000,
    'LIVE_FOUR': 100000,
    'FOUR': 10000,
    'LIVE_THREE': 5000,
    'THREE': 500,
    'LIVE_TWO': 100,
    'TWO': 50,
    'ONE': 10,
    'BLOCKED_THREE': 300,
    'BLOCKED_FOUR': 3000
}

# Direction vectors
DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

class Game:
    def __init__(self):
        self.board = self.reset_board()
        self.current_player = 'X'
        self.history = []
        self.win_probability = {'X': 0, 'O': 0}
        self.move_history = []
        self.start_time = None
        self.game_record = {
            'metadata': {
                'date': '',
                'players': {'X': 'Player', 'O': 'Computer'},
                'result': 'Unfinished',
                'difficulty': 'Strong AI'
            },
            'moves': []
        }
        self.game_over = False
        self.winner = None
        self.message = "Welcome to Gomoku!"
        self.hover_pos = None
        self.buttons = {
            'undo': {'rect': pygame.Rect(20, WINDOW_SIZE + 10, 80, BUTTON_HEIGHT), 'text': 'Undo'},
            'save': {'rect': pygame.Rect(120, WINDOW_SIZE + 10, 80, BUTTON_HEIGHT), 'text': 'Save Game'},
            'replay': {'rect': pygame.Rect(220, WINDOW_SIZE + 10, 80, BUTTON_HEIGHT), 'text': 'Restart'},
            'exit': {'rect': pygame.Rect(320, WINDOW_SIZE + 10, 80, BUTTON_HEIGHT), 'text': 'Exit'}
        }
        self.ai_thinking = False
        self.ai_thinking_time = 0
        self.ai_depth = 2
        self.last_move = None

    def reset_board(self):
        # Reset board
        return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def draw_board(self):
        # Draw board background
        screen.fill(BACKGROUND)
        
        # Draw board grid
        for i in range(BOARD_SIZE):
            # Horizontal lines
            pygame.draw.line(screen, LINE_COLOR, 
                             (BOARD_PADDING, BOARD_PADDING + i * CELL_SIZE), 
                             (BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE), 
                             2)
            # Vertical lines
            pygame.draw.line(screen, LINE_COLOR, 
                             (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING), 
                             (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE), 
                             2)
        
        # Draw five points on the board
        points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        for point in points:
            x, y = point
            pygame.draw.circle(screen, BLACK, 
                               (BOARD_PADDING + x * CELL_SIZE, BOARD_PADDING + y * CELL_SIZE), 
                               5)
        
        # Draw pieces
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 'X':
                    pygame.draw.circle(screen, BLACK, 
                                       (BOARD_PADDING + j * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE), 
                                       CELL_SIZE // 2 - 2)
                elif self.board[i][j] == 'O':
                    pygame.draw.circle(screen, WHITE, 
                                       (BOARD_PADDING + j * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE), 
                                       CELL_SIZE // 2 - 2)
                    pygame.draw.circle(screen, BLACK, 
                                       (BOARD_PADDING + j * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE), 
                                       CELL_SIZE // 2 - 2, 1)
        
        # Draw last move marker
        if self.last_move:
            row, col, player = self.last_move
            pygame.draw.circle(screen, RED if player == 'X' else BLUE, 
                               (BOARD_PADDING + col * CELL_SIZE, BOARD_PADDING + row * CELL_SIZE), 
                               5)
        
        # Draw mouse hover position
        if self.hover_pos and not self.game_over:
            row, col = self.hover_pos
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == '.':
                pygame.draw.circle(screen, GREEN, 
                                   (BOARD_PADDING + col * CELL_SIZE, BOARD_PADDING + row * CELL_SIZE), 
                                   5)
    
    def draw_info_panel(self):
        # Draw info panel background
        pygame.draw.rect(screen, INFO_BG, (0, WINDOW_SIZE, WINDOW_SIZE, BUTTON_HEIGHT + INFO_HEIGHT))
        
        # Draw buttons
        for name, button in self.buttons.items():
            color = BUTTON_HOVER if button['rect'].collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
            pygame.draw.rect(screen, color, button['rect'], border_radius=5)
            text = font.render(button['text'], True, WHITE)
            screen.blit(text, (button['rect'].centerx - text.get_width() // 2, 
                               button['rect'].centery - text.get_height() // 2))
        
        # Draw game info
        status_text = f"Current Player: {'Player(X)' if self.current_player == 'X' else 'Computer(O)'}"
        if self.game_over:
            if self.winner == 'X':
                status_text = "Player Wins!"
            elif self.winner == 'O':
                status_text = "Computer Wins!"
            else:
                status_text = "Game Over!"
        elif self.ai_thinking:
            status_text = "Computer Thinking..."
        
        status_surf = font.render(status_text, True, WHITE)
        screen.blit(status_surf, (420, WINDOW_SIZE + 15))
        
        # Draw win probability info
        prob_text = f"Win Probability: Player {self.win_probability['X']}% - Computer {self.win_probability['O']}%"
        prob_surf = font.render(prob_text, True, WHITE)
        screen.blit(prob_surf, (420, WINDOW_SIZE + 45))
        
        # Draw message
        msg_surf = font.render(self.message, True, GREEN)
        screen.blit(msg_surf, (20, WINDOW_SIZE + BUTTON_HEIGHT + 20))
        
        # Show AI thinking time
        if self.ai_thinking:
            think_time = f"Thinking Time: {self.ai_thinking_time:.1f}s"
            think_surf = font.render(think_time, True, WHITE)
            screen.blit(think_surf, (20, WINDOW_SIZE + BUTTON_HEIGHT + 45))

    def check_win(self, row, col, player):
        # Check four directions for five in a row
        for dr, dc in DIRECTIONS:
            count = 1
            # Forward check
            for i in range(1, 5):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                    count += 1
                else:
                    break
            # Backward check
            for i in range(1, 5):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def evaluate_pattern(self, count, open_ends, blocked_ends=0):
        # Enhanced pattern evaluation
        if count >= 5:
            return PATTERN_SCORES['FIVE']
        if count == 4:
            if open_ends == 2:
                return PATTERN_SCORES['LIVE_FOUR']
            elif open_ends == 1:
                return PATTERN_SCORES['FOUR']
            elif blocked_ends == 1:
                return PATTERN_SCORES['BLOCKED_FOUR']
        if count == 3:
            if open_ends == 2:
                return PATTERN_SCORES['LIVE_THREE']
            elif open_ends == 1:
                return PATTERN_SCORES['THREE']
            elif blocked_ends == 1:
                return PATTERN_SCORES['BLOCKED_THREE']
        if count == 2:
            if open_ends == 2:
                return PATTERN_SCORES['LIVE_TWO']
            elif open_ends == 1:
                return PATTERN_SCORES['TWO']
        if count == 1:
            return PATTERN_SCORES['ONE']
        return 0

    def evaluate_line(self, line, player):
        # Evaluate a line pattern
        score = 0
        opponent = 'X' if player == 'O' else 'O'
        length = len(line)
        
        # Use sliding window to check patterns
        window_size = 5
        for i in range(length - window_size + 1):
            window = line[i:i+window_size]
            
            # Count player pieces and empty spaces in window
            player_count = window.count(player)
            empty_count = window.count('.')
            opponent_count = window.count(opponent)
            
            # Skip windows with opponent pieces
            if opponent_count > 0:
                continue
                
            # Count open ends
            open_ends = 0
            if i > 0 and line[i-1] == '.':
                open_ends += 1
            if i + window_size < length and line[i+window_size] == '.':
                open_ends += 1
                
            # Score based on piece count and open ends
            if player_count == 5:
                score += PATTERN_SCORES['FIVE']
            elif player_count == 4 and open_ends > 0:
                if open_ends == 2:
                    score += PATTERN_SCORES['LIVE_FOUR']
                else:
                    score += PATTERN_SCORES['FOUR']
            elif player_count == 3 and open_ends > 0:
                if open_ends == 2:
                    score += PATTERN_SCORES['LIVE_THREE']
                else:
                    score += PATTERN_SCORES['THREE']
            elif player_count == 2 and open_ends == 2:
                score += PATTERN_SCORES['LIVE_TWO']
        
        return score

    def evaluate_board(self, player):
        # Evaluate the entire board for the specified player
        score = 0
        opponent = 'X' if player == 'O' else 'O'
        
        # Evaluate all rows
        for i in range(BOARD_SIZE):
            row = self.board[i]
            score += self.evaluate_line(row, player)
        
        # Evaluate all columns
        for j in range(BOARD_SIZE):
            col = [self.board[i][j] for i in range(BOARD_SIZE)]
            score += self.evaluate_line(col, player)
        
        # Evaluate diagonals (top-left to bottom-right)
        for k in range(-BOARD_SIZE+1, BOARD_SIZE):
            diag = []
            for i in range(max(0, -k), min(BOARD_SIZE, BOARD_SIZE - k)):
                j = i + k
                if 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
                    diag.append(self.board[i][j])
            score += self.evaluate_line(diag, player)
        
        # Evaluate diagonals (top-right to bottom-left)
        for k in range(0, 2*BOARD_SIZE-1):
            diag = []
            for i in range(max(0, k - BOARD_SIZE + 1), min(BOARD_SIZE, k + 1)):
                j = k - i
                if 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
                    diag.append(self.board[i][j])
            score += self.evaluate_line(diag, player)
        
        # Subtract opponent's score
        opponent_score = self.evaluate_board(opponent) if opponent == 'X' else 0
        return score - opponent_score * 0.7

    def get_valid_moves(self):
        # Get all valid moves (only consider areas around existing pieces)
        moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == '.':
                    # Check if there are pieces nearby
                    has_neighbor = False
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE:
                                if self.board[ni][nj] != '.':
                                    has_neighbor = True
                                    break
                        if has_neighbor:
                            break
                    if has_neighbor or not self.history:  # First move can be anywhere
                        moves.append((i, j))
        return moves

    def minimax(self, depth, alpha, beta, is_maximizing):
        # Minimax algorithm implementation with alpha-beta pruning
        # Check if game is over or max depth reached
        if depth == 0:
            return self.evaluate_board('O'), None
        
        if is_maximizing:
            # AI player (O)
            max_eval = float('-inf')
            best_move = None
            moves = self.get_valid_moves()
            
            # Sort by centrality to improve pruning efficiency
            moves.sort(key=lambda pos: abs(pos[0]-7) + abs(pos[1]-7))
            
            for move in moves:
                row, col = move
                # Try move
                self.board[row][col] = 'O'
                
                # Check if wins
                if self.check_win(row, col, 'O'):
                    self.board[row][col] = '.'  # Undo move
                    return float('inf'), move
                
                eval_score, _ = self.minimax(depth-1, alpha, beta, False)
                # Undo move
                self.board[row][col] = '.'
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta pruning
            
            return max_eval, best_move
        else:
            # Human player (X)
            min_eval = float('inf')
            best_move = None
            moves = self.get_valid_moves()
            
            # Sort by centrality to improve pruning efficiency
            moves.sort(key=lambda pos: abs(pos[0]-7) + abs(pos[1]-7))
            
            for move in moves:
                row, col = move
                # Try move
                self.board[row][col] = 'X'
                
                # Check if wins
                if self.check_win(row, col, 'X'):
                    self.board[row][col] = '.'  # Undo move
                    return float('-inf'), move
                
                eval_score, _ = self.minimax(depth-1, alpha, beta, True)
                # Undo move
                self.board[row][col] = '.'
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha pruning
            
            return min_eval, best_move

    def ai_move(self):
        if self.game_over:
            return
        
        self.ai_thinking = True
        start_time = time.time()
        
        # Use Minimax to select best move
        _, best_move = self.minimax(self.ai_depth, float('-inf'), float('inf'), True)
        
        self.ai_thinking_time = time.time() - start_time
        self.ai_thinking = False
        
        if best_move:
            row, col = best_move
            self.board[row][col] = 'O'
            self.history.append((row, col))
            self.move_history.append(('O', row, col))
            self.last_move = (row, col, 'O')
            self.message = f"Computer move ({row+1}, {col+1}) | Thinking Time: {self.ai_thinking_time:.2f}s"
            
            if self.check_win(row, col, 'O'):
                self.game_over = True
                self.winner = 'O'
                self.message = "Computer Wins!"
                self.game_record['metadata']['result'] = 'Computer Wins'
            else:
                self.current_player = 'X'
        else:
            # If no best move found, choose randomly
            valid_moves = self.get_valid_moves()
            if valid_moves:
                row, col = random.choice(valid_moves)
                self.board[row][col] = 'O'
                self.history.append((row, col))
                self.move_history.append(('O', row, col))
                self.last_move = (row, col, 'O')
                self.message = f"Computer random move ({row+1}, {col+1})"
                
                if self.check_win(row, col, 'O'):
                    self.game_over = True
                    self.winner = 'O'
                    self.message = "Computer Wins!"
                    self.game_record['metadata']['result'] = 'Computer Wins'
                else:
                    self.current_player = 'X'

    def player_move(self, pos):
        if self.game_over:
            self.message = "Game is over, cannot move"
            return False
        
        row, col = pos
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            self.message = "Invalid move position"
            return False
        
        if self.board[row][col] != '.':
            self.message = "Position already occupied"
            return False
        
        self.board[row][col] = 'X'
        self.history.append((row, col))
        self.move_history.append(('X', row, col))
        self.last_move = (row, col, 'X')
        self.message = f"Player move ({row+1}, {col+1})"
        
        if self.check_win(row, col, 'X'):
            self.game_over = True
            self.winner = 'X'
            self.message = "Congratulations! Player Wins!"
            self.game_record['metadata']['result'] = 'Player Wins'
        else:
            self.current_player = 'O'
            # AI move
            self.ai_move()
        
        return True

    def undo(self):
        if len(self.history) < 2:
            self.message = "Cannot undo"
            return
        
        # Undo two moves (player and computer)
        last_o = self.history.pop()
        self.board[last_o[0]][last_o[1]] = '.'
        last_x = self.history.pop()
        self.board[last_x[0]][last_x[1]] = '.'
        
        # Remove from move record
        if self.move_history:
            self.move_history.pop()
        if self.move_history:
            self.move_history.pop()
        
        self.current_player = 'X'
        self.last_move = None if not self.history else (self.history[-1][0], self.history[-1][1], 'X')
        self.message = "Undo successful"
        self.game_over = False
        self.winner = None

    def save_game_record(self):
        if not self.move_history:
            self.message = "No game record to save"
            return
        
        # Fill in date
        self.game_record['metadata']['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.game_record['moves'] = [{'player': p, 'row': r, 'col': c} for p, r, c in self.move_history]
        
        # Create save directory
        if not os.path.exists("game_records"):
            os.makedirs("game_records")
        
        # Generate filename
        filename = f"game_records/Gomoku-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.game_record, f, ensure_ascii=False, indent=2)
        
        self.message = f"Game record saved as {filename}!"

    def reset_game(self):
        self.board = self.reset_board()
        self.current_player = 'X'
        self.history.clear()
        self.move_history.clear()
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.message = "Game restarted"
        self.win_probability = {'X': 0, 'O': 0}
        self.ai_thinking = False

    def handle_click(self, pos):
        x, y = pos
        
        # Check button clicks
        for name, button in self.buttons.items():
            if button['rect'].collidepoint(pos):
                if name == 'undo':
                    self.undo()
                elif name == 'save':
                    self.save_game_record()
                elif name == 'replay':
                    self.reset_game()
                elif name == 'exit':
                    pygame.quit()
                    sys.exit()
                return

        # Player move
        if self.game_over or self.current_player != 'X' or self.ai_thinking:
            return

        # Calculate board coordinates
        col = round((x - BOARD_PADDING) / CELL_SIZE)
        row = round((y - BOARD_PADDING) / CELL_SIZE)
        
        # Ensure coordinates are valid
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.player_move((row, col))

    def update_hover(self, pos):
        x, y = pos
        col = round((x - BOARD_PADDING) / CELL_SIZE)
        row = round((y - BOARD_PADDING) / CELL_SIZE)
        
        # Ensure coordinates are valid
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.hover_pos = (row, col)
        else:
            self.hover_pos = None

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                game.update_hover(event.pos)

        game.draw_board()
        game.draw_info_panel()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()