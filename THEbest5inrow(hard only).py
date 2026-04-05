import random
import time
import shutil
from collections import defaultdict
from datetime import datetime
import os
import pygame
import sys
import math
import json

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
BOARD_SIZE = 15
CELL_SIZE = 60
BOARD_PADDING = 50
WINDOW_SIZE = BOARD_PADDING * 2 + CELL_SIZE * (BOARD_SIZE - 1)
BUTTON_HEIGHT = 55  # 增大按钮高度
INFO_HEIGHT = 140   # 增加信息面板高度以容纳更大的按钮
TOTAL_HEIGHT = WINDOW_SIZE + BUTTON_HEIGHT + INFO_HEIGHT

# Color definitions - Modern color scheme
BACKGROUND = (44, 62, 80)  # Dark blue-gray
BOARD_COLOR = (236, 240, 241)  # Light gray-white
LINE_COLOR = (52, 73, 94)  # Dark gray
BLACK = (44, 62, 80)  # Dark blue-gray
WHITE = (236, 240, 241)  # White
RED = (231, 76, 60)  # Red
BLUE = (52, 152, 219)  # Blue
GREEN = (46, 204, 113)  # Green
ORANGE = (230, 126, 34)  # Orange
PURPLE = (155, 89, 182)  # Purple
BUTTON_COLOR = (52, 152, 219)  # Button color
BUTTON_HOVER = (41, 128, 185)  # Button hover color
BUTTON_CLICK = (21, 67, 96)  # Button click color
INFO_BG = (52, 73, 94)  # Info panel background
HOVER_COLOR = (241, 196, 15)  # Hover indicator color

# Create window
screen = pygame.display.set_mode((WINDOW_SIZE, TOTAL_HEIGHT))
pygame.display.set_caption("Gomoku - Smart AI Battle")
pygame.display.set_icon(pygame.Surface((32, 32)))

# Fonts
font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 20)
button_font = pygame.font.Font(None, 24)  # 增大按钮字体

# Enhanced pattern scoring with more nuanced values
PATTERN_SCORES = {
    'FIVE': 10000000,
    'LIVE_FOUR': 500000,
    'FOUR': 100000,
    'LIVE_THREE': 50000,
    'THREE': 8000,
    'LIVE_TWO': 2000,
    'TWO': 300,
    'ONE': 50,
    'BLOCKED_THREE': 4000,
    'BLOCKED_FOUR': 50000,
    'DOUBLE_THREE': 80000,
    'DOUBLE_FOUR': 300000,
}

DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

class Particle:
    """Particle effect class"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 1.0
        self.color = color
        self.size = random.randint(2, 4)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity
        self.life -= 0.02
        return self.life > 0
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * self.life)
            color = (*self.color, alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class Button:
    """Modern button class with larger size"""
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR, hover_color=BUTTON_HOVER):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        self.is_clicked = False
        self.click_animation = 0
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.current_color = self.hover_color if self.is_hovered else self.color
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_clicked = True
                self.click_animation = 5
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False
            
        return False
        
    def update(self):
        if self.click_animation > 0:
            self.click_animation -= 1
            
    def draw(self, screen):
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=10)
        
        # Draw button background
        color = self.current_color
        if self.click_animation > 0:
            color = BUTTON_CLICK
            
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255, 80), self.rect, 2, border_radius=10)
        
        # Draw text
        text_surf = button_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class PatternMatcher:
    """Pattern recognition class"""
    @staticmethod
    def get_pattern_name(pattern):
        pattern_str = ''.join(pattern)
        
        if pattern_str == '01110':
            return 'LIVE_FOUR'
        if pattern_str in ['01110', '11110', '01111', '10111', '11011', '11101']:
            return 'FOUR'
        if pattern_str in ['01110', '010110', '011010']:
            return 'LIVE_THREE'
        if pattern_str in ['0011100', '011100', '001110', '0111000', '010110', '011010']:
            return 'THREE'
        if pattern_str in ['001100', '0110', '01010']:
            return 'LIVE_TWO'
        if pattern_str in ['0001100', '0010100', '010010']:
            return 'TWO'
        return None

class EnhancedAIPlayer:
    """Enhanced AI player with smart evaluation"""
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.difficulty_settings = {
            'easy': {'depth': 1, 'randomness': 0.3, 'aggression': 0.7},
            'medium': {'depth': 2, 'randomness': 0.15, 'aggression': 1.0},
            'hard': {'depth': 3, 'randomness': 0.05, 'aggression': 1.2},
            'expert': {'depth': 4, 'randomness': 0.02, 'aggression': 1.5}
        }
        
    def get_move(self, game, board, player):
        """Get the best move for AI"""
        settings = self.difficulty_settings[self.difficulty]
        moves = self.get_candidate_moves(board)
        
        if not moves:
            return None
            
        scored_moves = []
        for move in moves:
            row, col = move
            score = self.evaluate_move(board, row, col, player)
            score = self.add_strategic_weight(board, row, col, player, score, settings['aggression'])
            scored_moves.append((score, move))
        
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        
        if random.random() < settings['randomness']:
            top_count = max(1, len(scored_moves) // 10)
            top_moves = scored_moves[:top_count]
            return random.choice(top_moves)[1]
        
        return scored_moves[0][1] if scored_moves else None
    
    def get_candidate_moves(self, board):
        """Get candidate moves near existing pieces"""
        moves = []
        radius = 2
        
        occupied_positions = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] != '.':
                    occupied_positions.append((i, j))
        
        if not occupied_positions:
            return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
        
        for i, j in occupied_positions:
            for di in range(-radius, radius + 1):
                for dj in range(-radius, radius + 1):
                    ni, nj = i + di, j + dj
                    if (0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE and 
                        board[ni][nj] == '.' and 
                        (ni, nj) not in moves):
                        moves.append((ni, nj))
        
        return moves
    
    def evaluate_move(self, board, row, col, player):
        """Evaluate a single move"""
        board[row][col] = player
        score = self.evaluate_position(board, row, col, player)
        opponent = 'X' if player == 'O' else 'O'
        defense_score = self.evaluate_position(board, row, col, opponent) * 0.8
        score += defense_score
        board[row][col] = '.'
        return score
    
    def evaluate_position(self, board, row, col, player):
        """Evaluate position for a specific player"""
        score = 0
        for dr, dc in DIRECTIONS:
            count = 1
            open_left = 0
            open_right = 0
            
            for step in range(1, 6):
                r, c = row + step * dr, col + step * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] == player:
                        count += 1
                    elif board[r][c] == '.':
                        open_right += 1
                        break
                    else:
                        break
                else:
                    break
            
            for step in range(1, 6):
                r, c = row - step * dr, col - step * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] == player:
                        count += 1
                    elif board[r][c] == '.':
                        open_left += 1
                        break
                    else:
                        break
                else:
                    break
            
            score += self.score_pattern(count, open_left + open_right)
        return score
    
    def score_pattern(self, count, open_ends):
        """Score pattern based on count and open ends"""
        if count >= 5:
            return PATTERN_SCORES['FIVE']
        if count == 4:
            if open_ends >= 2:
                return PATTERN_SCORES['LIVE_FOUR']
            elif open_ends == 1:
                return PATTERN_SCORES['FOUR']
        if count == 3:
            if open_ends >= 2:
                return PATTERN_SCORES['LIVE_THREE']
            elif open_ends == 1:
                return PATTERN_SCORES['THREE']
        if count == 2:
            if open_ends >= 2:
                return PATTERN_SCORES['LIVE_TWO']
            elif open_ends == 1:
                return PATTERN_SCORES['TWO']
        if count == 1:
            return PATTERN_SCORES['ONE']
        return 0
    
    def add_strategic_weight(self, board, row, col, player, base_score, aggression):
        """Add strategic weight to the score"""
        center = BOARD_SIZE // 2
        distance_to_center = abs(row - center) + abs(col - center)
        center_bonus = (BOARD_SIZE - distance_to_center) * 50
        
        edge_penalty = 0
        if row == 0 or row == BOARD_SIZE - 1 or col == 0 or col == BOARD_SIZE - 1:
            edge_penalty = -100
        elif row <= 2 or row >= BOARD_SIZE - 3 or col <= 2 or col >= BOARD_SIZE - 3:
            edge_penalty = -50
        
        aggression_bonus = base_score * (aggression - 1)
        return base_score + center_bonus + edge_penalty + aggression_bonus

class WinRateTracker:
    """Win rate tracker"""
    def __init__(self):
        self.total_games = 0
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0
        self.current_game_moves = []
        self.winrate_history = []
        self.move_times = []
        
    def add_game_result(self, winner):
        """Add game result"""
        self.total_games += 1
        if winner == 'X':
            self.player_wins += 1
        elif winner == 'O':
            self.computer_wins += 1
        else:
            self.draws += 1
            
        if self.current_game_moves:
            self.winrate_history.append({
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'winner': winner,
                'moves': self.current_game_moves.copy(),
                'final_winrate': self.current_game_moves[-1] if self.current_game_moves else {},
                'avg_thinking_time': sum(self.move_times) / len(self.move_times) if self.move_times else 0
            })
            self.current_game_moves.clear()
            self.move_times.clear()
    
    def add_move_winrate(self, winrate, thinking_time=0):
        """Record winrate after each move"""
        self.current_game_moves.append({
            'move_number': len(self.current_game_moves) + 1,
            'player_winrate': winrate['X'],
            'computer_winrate': winrate['O'],
            'thinking_time': thinking_time
        })
        if thinking_time > 0:
            self.move_times.append(thinking_time)
    
    def get_player_win_rate(self):
        """Get player win rate"""
        if self.total_games == 0:
            return 0
        return round((self.player_wins / self.total_games) * 100, 1)
    
    def get_computer_win_rate(self):
        """Get computer win rate"""
        if self.total_games == 0:
            return 0
        return round((self.computer_wins / self.total_games) * 100, 1)
    
    def calculate_current_winrate(self, board, current_player):
        """Calculate current winrate for the position"""
        if not board:
            return {'X': 50.0, 'O': 50.0}
        
        player_score = 0
        computer_score = 0
        
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 'X':
                    player_score += self.evaluate_position_advanced(board, i, j, 'X')
                elif board[i][j] == 'O':
                    computer_score += self.evaluate_position_advanced(board, i, j, 'O')
        
        total_score = player_score + computer_score
        if total_score == 0:
            return {'X': 50.0, 'O': 50.0}
        
        player_winrate = (player_score / total_score) * 100
        computer_winrate = 100 - player_winrate
        
        if current_player == 'O':
            computer_winrate = min(99, computer_winrate + 5)
            player_winrate = 100 - computer_winrate
        
        return {
            'X': round(player_winrate, 1),
            'O': round(computer_winrate, 1)
        }
    
    def evaluate_position_advanced(self, board, row, col, player):
        """Advanced position evaluation"""
        score = 0
        for dr, dc in DIRECTIONS:
            count = 1
            open_ends = 0
            blocked_ends = 0
            
            for step in range(1, 6):
                r, c = row + step * dr, col + step * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] == player:
                        count += 1
                    elif board[r][c] == '.':
                        open_ends += 1
                        break
                    else:
                        blocked_ends += 1
                        break
                else:
                    blocked_ends += 1
                    break
            
            for step in range(1, 6):
                r, c = row - step * dr, col - step * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] == player:
                        count += 1
                    elif board[r][c] == '.':
                        open_ends += 1
                        break
                    else:
                        blocked_ends += 1
                        break
                else:
                    blocked_ends += 1
                    break
            
            if count >= 5:
                score += PATTERN_SCORES['FIVE']
            elif count == 4:
                if open_ends >= 2:
                    score += PATTERN_SCORES['LIVE_FOUR']
                elif open_ends == 1:
                    score += PATTERN_SCORES['FOUR']
                else:
                    score += PATTERN_SCORES['BLOCKED_FOUR']
            elif count == 3:
                if open_ends >= 2:
                    score += PATTERN_SCORES['LIVE_THREE']
                elif open_ends == 1:
                    score += PATTERN_SCORES['THREE']
                else:
                    score += PATTERN_SCORES['BLOCKED_THREE']
            elif count == 2:
                if open_ends >= 2:
                    score += PATTERN_SCORES['LIVE_TWO']
                elif open_ends == 1:
                    score += PATTERN_SCORES['TWO']
            elif count == 1:
                score += PATTERN_SCORES['ONE']
        
        return score
    
    def save_stats(self, filename="winrate_stats.json"):
        """Save statistics to file"""
        stats = {
            'total_games': self.total_games,
            'player_wins': self.player_wins,
            'computer_wins': self.computer_wins,
            'draws': self.draws,
            'player_win_rate': self.get_player_win_rate(),
            'computer_win_rate': self.get_computer_win_rate(),
            'history': self.winrate_history,
            'avg_thinking_time': sum(self.move_times) / len(self.move_times) if self.move_times else 0
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    
    def load_stats(self, filename="winrate_stats.json"):
        """Load statistics from file"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                    self.total_games = stats.get('total_games', 0)
                    self.player_wins = stats.get('player_wins', 0)
                    self.computer_wins = stats.get('computer_wins', 0)
                    self.draws = stats.get('draws', 0)
                    self.winrate_history = stats.get('history', [])
            except:
                pass

class Game:
    def __init__(self):
        self.board = self.reset_board()
        self.current_player = 'X'
        self.history = []
        self.win_probability = {'X': 50.0, 'O': 50.0}
        self.move_history = []
        self.start_time = None
        self.game_record = {
            'metadata': {
                'date': '',
                'players': {'X': 'Player', 'O': 'Computer'},
                'result': 'Unfinished',
                'difficulty': 'Hard'
            },
            'moves': []
        }
        self.game_over = False
        self.winner = None
        self.message = "Welcome to Gomoku!"
        self.hover_pos = None
        self.ai_thinking = False
        self.ai_thinking_time = 0
        self.last_move = None
        self.difficulty = 'hard'
        self.difficulty_options = ['easy', 'medium', 'hard', 'expert']
        self.difficulty_index = 2
        
        # Create modern buttons - 调整位置和大小
        button_width = 95
        button_spacing = 8
        start_x = 20
        
        self.buttons = {
            'undo': Button(start_x, WINDOW_SIZE + 12, button_width, BUTTON_HEIGHT, '↩ Undo'),
            'save': Button(start_x + button_width + button_spacing, WINDOW_SIZE + 12, button_width, BUTTON_HEIGHT, '💾 Save'),
            'replay': Button(start_x + (button_width + button_spacing) * 2, WINDOW_SIZE + 12, button_width, BUTTON_HEIGHT, '🔄 Restart'),
            'stats': Button(start_x + (button_width + button_spacing) * 3, WINDOW_SIZE + 12, button_width, BUTTON_HEIGHT, '📊 Stats'),
            'difficulty': Button(start_x + (button_width + button_spacing) * 4, WINDOW_SIZE + 12, button_width + 10, BUTTON_HEIGHT, '⚙️ Difficulty'),
            'exit': Button(start_x + (button_width + button_spacing) * 5 + 10, WINDOW_SIZE + 12, button_width, BUTTON_HEIGHT, '✖ Exit')
        }
        
        # Create AI player
        self.ai_player = EnhancedAIPlayer(self.difficulty)
        
        # Win rate tracker
        self.win_tracker = WinRateTracker()
        self.win_tracker.load_stats()
        self.show_stats = False
        self.show_difficulty_menu = False
        
        # Animation effects
        self.particles = []
        self.move_count = 0
        self.fade_alpha = 0
        self.flash_effect = False
        self.flash_timer = 0
        
        # Move indicators
        self.move_indicators = []
        
    def reset_board(self):
        return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    def add_particle_effect(self, x, y, color):
        """Add particle effect"""
        for _ in range(15):
            self.particles.append(Particle(x, y, color))
    
    def update_win_probability(self):
        """Update win probability for current position"""
        self.win_probability = self.win_tracker.calculate_current_winrate(self.board, self.current_player)
        if not self.game_over:
            self.win_tracker.add_move_winrate(self.win_probability, self.ai_thinking_time)
    
    def draw_board(self):
        """Draw the game board"""
        # Draw gradient background
        for i in range(TOTAL_HEIGHT):
            color_ratio = i / TOTAL_HEIGHT
            color = (
                int(BACKGROUND[0] * (1 - color_ratio) + BOARD_COLOR[0] * color_ratio),
                int(BACKGROUND[1] * (1 - color_ratio) + BOARD_COLOR[1] * color_ratio),
                int(BACKGROUND[2] * (1 - color_ratio) + BOARD_COLOR[2] * color_ratio)
            )
            pygame.draw.line(screen, color, (0, i), (WINDOW_SIZE, i))
        
        # Draw board background
        board_bg = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        board_bg.fill(BOARD_COLOR)
        board_bg.set_alpha(200)
        screen.blit(board_bg, (0, 0))
        
        # Draw grid lines
        for i in range(BOARD_SIZE):
            # Horizontal lines
            pygame.draw.line(screen, LINE_COLOR, 
                           (BOARD_PADDING, BOARD_PADDING + i * CELL_SIZE), 
                           (BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE), 2)
            # Vertical lines
            pygame.draw.line(screen, LINE_COLOR, 
                           (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING), 
                           (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE), 2)
        
        # Draw star points
        star_points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        for point in star_points:
            x, y = point
            pygame.draw.circle(screen, LINE_COLOR, 
                             (BOARD_PADDING + x * CELL_SIZE, BOARD_PADDING + y * CELL_SIZE), 6)
            pygame.draw.circle(screen, BOARD_COLOR, 
                             (BOARD_PADDING + x * CELL_SIZE, BOARD_PADDING + y * CELL_SIZE), 4)
        
        # Draw pieces
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 'X':
                    pos = (BOARD_PADDING + j * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE)
                    pygame.draw.circle(screen, BLACK, pos, CELL_SIZE // 2 - 2)
                    # Add highlight effect
                    highlight_pos = (pos[0] - 5, pos[1] - 5)
                    pygame.draw.circle(screen, (100, 100, 100), highlight_pos, 5)
                elif self.board[i][j] == 'O':
                    pos = (BOARD_PADDING + j * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE)
                    pygame.draw.circle(screen, WHITE, pos, CELL_SIZE // 2 - 2)
                    pygame.draw.circle(screen, BLACK, pos, CELL_SIZE // 2 - 2, 2)
                    # Add highlight effect
                    highlight_pos = (pos[0] - 5, pos[1] - 5)
                    pygame.draw.circle(screen, (200, 200, 200), highlight_pos, 5)
        
        # Draw last move marker
        if self.last_move:
            row, col, player = self.last_move
            pos = (BOARD_PADDING + col * CELL_SIZE, BOARD_PADDING + row * CELL_SIZE)
            pygame.draw.circle(screen, RED if player == 'X' else BLUE, pos, 8, 2)
            
            # Add flash effect
            if self.flash_timer > 0:
                flash_alpha = int(128 * (self.flash_timer / 10))
                flash_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                flash_surf.fill((255, 255, 0, flash_alpha))
                screen.blit(flash_surf, (pos[0] - CELL_SIZE//2, pos[1] - CELL_SIZE//2))
                self.flash_timer -= 1
        
        # Draw hover indicator
        if self.hover_pos and not self.game_over and self.current_player == 'X':
            row, col = self.hover_pos
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == '.':
                pos = (BOARD_PADDING + col * CELL_SIZE, BOARD_PADDING + row * CELL_SIZE)
                pygame.draw.circle(screen, HOVER_COLOR, pos, CELL_SIZE // 2 - 2, 2)
        
        # Draw move indicators
        for indicator in self.move_indicators:
            if indicator['timer'] > 0:
                pos = (BOARD_PADDING + indicator['col'] * CELL_SIZE, 
                      BOARD_PADDING + indicator['row'] * CELL_SIZE)
                alpha = int(100 * (indicator['timer'] / 30))
                pygame.draw.circle(screen, GREEN, pos, CELL_SIZE // 3, 2)
                indicator['timer'] -= 1
        
        # Update and draw particle effects
        self.particles = [p for p in self.particles if p.update()]
        for particle in self.particles:
            particle.draw(screen)
    
    def draw_info_panel(self):
        """Draw the info panel"""
        # Draw info panel background
        info_rect = pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, BUTTON_HEIGHT + INFO_HEIGHT)
        pygame.draw.rect(screen, INFO_BG, info_rect)
        
        # Draw separator line
        pygame.draw.line(screen, (100, 100, 100), (0, WINDOW_SIZE), (WINDOW_SIZE, WINDOW_SIZE), 3)
        
        # Update and draw buttons
        for button in self.buttons.values():
            button.update()
            button.draw(screen)
        
        # Draw game status
        status_text = ""
        if self.game_over:
            if self.winner == 'X':
                status_text = "🎉 Player Wins! 🎉"
            elif self.winner == 'O':
                status_text = "🤖 Computer Wins! 🤖"
            else:
                status_text = "🤝 Draw! 🤝"
        elif self.ai_thinking:
            status_text = "🤔 AI Thinking..."
        else:
            status_text = f"🎮 Current: {'Player (Black)' if self.current_player == 'X' else 'AI (White)'}"
        
        status_surf = title_font.render(status_text, True, (255, 255, 255))
        screen.blit(status_surf, (WINDOW_SIZE - status_surf.get_width() - 20, WINDOW_SIZE + 15))
        
        # Draw win rate bar
        winrate_x = 20
        winrate_y = WINDOW_SIZE + 80  # 向下移动以容纳更大的按钮
        bar_width = 400
        bar_height = 28
        
        # Background bar
        pygame.draw.rect(screen, (100, 100, 100), (winrate_x, winrate_y, bar_width, bar_height))
        
        # Player win rate bar
        player_width = int(bar_width * (self.win_probability['X'] / 100))
        pygame.draw.rect(screen, GREEN, (winrate_x, winrate_y, player_width, bar_height))
        
        # AI win rate bar
        pygame.draw.rect(screen, BLUE, (winrate_x + player_width, winrate_y, 
                                       bar_width - player_width, bar_height))
        
        # Win rate text
        winrate_text = f"Win Rate: Player {self.win_probability['X']}%  |  AI {self.win_probability['O']}%"
        winrate_surf = font.render(winrate_text, True, (255, 255, 255))
        screen.blit(winrate_surf, (winrate_x, winrate_y - 22))
        
        # Draw historical win rate
        total_text = f"Total Games: {self.win_tracker.total_games} | Player Win Rate: {self.win_tracker.get_player_win_rate()}%"
        total_surf = small_font.render(total_text, True, (200, 200, 200))
        screen.blit(total_surf, (winrate_x, winrate_y + bar_height + 5))
        
        # Draw difficulty info
        diff_text = f"Difficulty: {self.difficulty.upper()}"
        diff_surf = font.render(diff_text, True, ORANGE)
        screen.blit(diff_surf, (winrate_x + bar_width + 20, winrate_y + 5))
        
        # Draw message
        msg_surf = font.render(self.message, True, GREEN)
        screen.blit(msg_surf, (20, WINDOW_SIZE + BUTTON_HEIGHT + 15))
        
        # Draw AI thinking time
        if self.ai_thinking_time > 0:
            time_text = f"Thinking Time: {self.ai_thinking_time:.2f}s"
            time_surf = font.render(time_text, True, (200, 200, 200))
            screen.blit(time_surf, (20, WINDOW_SIZE + BUTTON_HEIGHT + 40))
        
        # Draw difficulty selection menu
        if self.show_difficulty_menu:
            self.draw_difficulty_menu()
        
        # Draw statistics popup
        if self.show_stats:
            self.draw_stats_popup()
    
    def draw_difficulty_menu(self):
        """Draw difficulty selection menu"""
        menu_width = 200
        menu_height = 220
        menu_x = self.buttons['difficulty'].rect.x
        menu_y = self.buttons['difficulty'].rect.y - menu_height - 5
        
        # Draw shadow
        shadow_rect = pygame.Rect(menu_x + 3, menu_y + 3, menu_width, menu_height)
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=12)
        
        # Draw menu background
        pygame.draw.rect(screen, (60, 60, 70), (menu_x, menu_y, menu_width, menu_height), border_radius=12)
        pygame.draw.rect(screen, (100, 100, 120), (menu_x, menu_y, menu_width, menu_height), 2, border_radius=12)
        
        # Draw title
        title_surf = small_font.render("Select Difficulty", True, (255, 255, 255))
        screen.blit(title_surf, (menu_x + menu_width//2 - title_surf.get_width()//2, menu_y + 12))
        
        # Draw options
        self.diff_rects = []
        for i, diff in enumerate(self.difficulty_options):
            y_offset = menu_y + 48 + i * 38
            text = diff.upper()
            text_surf = font.render(text, True, (255, 255, 255))
            
            # Mark current difficulty
            if diff == self.difficulty:
                pygame.draw.circle(screen, GREEN, (menu_x + menu_width - 28, y_offset + 12), 6)
                text_surf = font.render(text, True, GREEN)
            
            screen.blit(text_surf, (menu_x + 20, y_offset))
            
            # Save click area
            rect = pygame.Rect(menu_x, y_offset - 5, menu_width, 35)
            self.diff_rects.append((rect, diff))
    
    def draw_stats_popup(self):
        """Draw statistics popup window"""
        popup_width = 580
        popup_height = 480
        popup_x = (WINDOW_SIZE - popup_width) // 2
        popup_y = (WINDOW_SIZE - popup_height) // 2
        
        # Draw semi-transparent background
        s = pygame.Surface((WINDOW_SIZE, TOTAL_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (0, 0))
        
        # Draw popup background
        pygame.draw.rect(screen, (50, 50, 60), (popup_x, popup_y, popup_width, popup_height), border_radius=15)
        pygame.draw.rect(screen, (100, 100, 120), (popup_x, popup_y, popup_width, popup_height), 2, border_radius=15)
        
        # Title
        title = title_font.render("Game Statistics", True, (255, 255, 255))
        screen.blit(title, (popup_x + (popup_width - title.get_width()) // 2, popup_y + 18))
        
        # Statistics
        y_offset = popup_y + 70
        stats = [
            f"📊 Total Games: {self.win_tracker.total_games}",
            f"🏆 Player Wins: {self.win_tracker.player_wins}",
            f"🤖 AI Wins: {self.win_tracker.computer_wins}",
            f"🤝 Draws: {self.win_tracker.draws}",
            f"📈 Player Win Rate: {self.win_tracker.get_player_win_rate()}%",
            f"📉 AI Win Rate: {self.win_tracker.get_computer_win_rate()}%"
        ]
        
        for stat in stats:
            text = font.render(stat, True, (220, 220, 220))
            screen.blit(text, (popup_x + 35, y_offset))
            y_offset += 38
        
        # Average thinking time
        if self.win_tracker.move_times:
            avg_time = sum(self.win_tracker.move_times) / len(self.win_tracker.move_times)
            time_text = f"⏱️ Avg Thinking Time: {avg_time:.2f}s"
            text = font.render(time_text, True, (220, 220, 220))
            screen.blit(text, (popup_x + 35, y_offset))
            y_offset += 38
        
        # Recent games
        if self.win_tracker.winrate_history:
            y_offset += 10
            recent_text = small_font.render("Recent Games:", True, (255, 255, 255))
            screen.blit(recent_text, (popup_x + 35, y_offset))
            y_offset += 28
            
            for i, game in enumerate(self.win_tracker.winrate_history[-5:]):
                winner = "Player" if game['winner'] == 'X' else "AI" if game['winner'] == 'O' else "Draw"
                winrate_info = f"{i+1}. {game['date'][:10]} - {winner} Victory"
                text = small_font.render(winrate_info, True, (150, 200, 150))
                screen.blit(text, (popup_x + 50, y_offset))
                y_offset += 24
        
        # Close button
        close_rect = pygame.Rect(popup_x + popup_width - 45, popup_y + 18, 32, 32)
        pygame.draw.rect(screen, (200, 60, 60), close_rect, border_radius=6)
        close_text = font.render("X", True, (255, 255, 255))
        screen.blit(close_text, (close_rect.centerx - close_text.get_width() // 2,
                                close_rect.centery - close_text.get_height() // 2))
        
        return close_rect
    
    def check_win(self, row, col, player):
        """Check if the player has won"""
        for dr, dc in DIRECTIONS:
            count = 1
            for i in range(1, 5):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False
    
    def ai_move(self):
        """AI makes a move"""
        if self.game_over:
            return
        
        self.ai_thinking = True
        start_time = time.time()
        
        best_move = self.ai_player.get_move(self, self.board, 'O')
        
        self.ai_thinking_time = time.time() - start_time
        self.ai_thinking = False
        
        if best_move:
            row, col = best_move
            self.board[row][col] = 'O'
            self.history.append((row, col))
            self.move_history.append(('O', row, col))
            self.last_move = (row, col, 'O')
            self.move_count += 1
            
            # Add particle effect
            pos_x = BOARD_PADDING + col * CELL_SIZE
            pos_y = BOARD_PADDING + row * CELL_SIZE
            self.add_particle_effect(pos_x, pos_y, WHITE)
            
            # Add move indicator
            self.move_indicators.append({'row': row, 'col': col, 'timer': 30})
            
            comments = [
                f"AI plays ({row+1}, {col+1})",
                f"🤖 AI chooses ({row+1}, {col+1})",
                f"AI moved to ({row+1}, {col+1}) in {self.ai_thinking_time:.2f}s"
            ]
            self.message = random.choice(comments)
            
            if self.check_win(row, col, 'O'):
                self.game_over = True
                self.winner = 'O'
                self.message = "🤖 AI Wins! Want to play again? 🤖"
                self.game_record['metadata']['result'] = 'Computer Wins'
                self.win_tracker.add_game_result('O')
                self.win_tracker.save_stats()
                self.flash_effect = True
                self.flash_timer = 10
            else:
                self.current_player = 'X'
        else:
            if len(self.get_valid_moves()) == 0:
                self.game_over = True
                self.message = "🤝 Draw! 🤝"
                self.win_tracker.add_game_result('draw')
                self.win_tracker.save_stats()
        
        self.update_win_probability()
    
    def get_valid_moves(self):
        """Get all valid moves on the board"""
        moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == '.':
                    moves.append((i, j))
        return moves
    
    def player_move(self, pos):
        """Player makes a move"""
        if self.game_over:
            self.message = "Game is over, please restart"
            return False
        
        if self.current_player != 'X':
            self.message = "Please wait for AI to think"
            return False
        
        row, col = pos
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            self.message = "Invalid position"
            return False
        
        if self.board[row][col] != '.':
            self.message = "Position already occupied"
            return False
        
        self.board[row][col] = 'X'
        self.history.append((row, col))
        self.move_history.append(('X', row, col))
        self.last_move = (row, col, 'X')
        self.move_count += 1
        
        # Add particle effect
        pos_x = BOARD_PADDING + col * CELL_SIZE
        pos_y = BOARD_PADDING + row * CELL_SIZE
        self.add_particle_effect(pos_x, pos_y, BLACK)
        
        # Add move indicator
        self.move_indicators.append({'row': row, 'col': col, 'timer': 30})
        
        self.message = f"Player moves to ({row+1}, {col+1})"
        
        self.update_win_probability()
        
        if self.check_win(row, col, 'X'):
            self.game_over = True
            self.winner = 'X'
            self.message = "🎉 Congratulations! You won! 🎉"
            self.game_record['metadata']['result'] = 'Player Wins'
            self.win_tracker.add_game_result('X')
            self.win_tracker.save_stats()
            self.flash_effect = True
            self.flash_timer = 10
        else:
            self.current_player = 'O'
            self.ai_move()
        
        return True
    
    def undo(self):
        """Undo last two moves"""
        if self.game_over:
            self.message = "Cannot undo after game over"
            return
        
        if len(self.history) < 2:
            self.message = "Not enough moves to undo"
            return
        
        # Undo two moves
        last_o = self.history.pop()
        self.board[last_o[0]][last_o[1]] = '.'
        last_x = self.history.pop()
        self.board[last_x[0]][last_x[1]] = '.'
        
        if self.move_history:
            self.move_history.pop()
        if self.move_history:
            self.move_history.pop()
        
        self.current_player = 'X'
        self.last_move = None if not self.history else (self.history[-1][0], self.history[-1][1], 'X')
        self.message = "Undo successful"
        self.game_over = False
        self.winner = None
        self.move_count -= 2
        
        self.update_win_probability()
    
    def save_game_record(self):
        """Save game record to file"""
        if not self.move_history:
            self.message = "No moves to save"
            return
        
        self.game_record['metadata']['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.game_record['metadata']['difficulty'] = self.difficulty
        self.game_record['moves'] = [{'player': p, 'row': r, 'col': c, 'move_num': i+1} 
                                     for i, (p, r, c) in enumerate(self.move_history)]
        self.game_record['winrate_history'] = self.win_tracker.current_game_moves
        
        if not os.path.exists("game_records"):
            os.makedirs("game_records")
        
        filename = f"game_records/Gomoku-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.game_record, f, ensure_ascii=False, indent=2)
        
        self.message = f"Game saved: {filename}"
    
    def reset_game(self):
        """Reset the game"""
        self.board = self.reset_board()
        self.current_player = 'X'
        self.history.clear()
        self.move_history.clear()
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.message = "Game restarted! Good luck!"
        self.win_probability = {'X': 50.0, 'O': 50.0}
        self.ai_thinking = False
        self.move_count = 0
        self.particles.clear()
        self.move_indicators.clear()
        self.win_tracker.current_game_moves.clear()
    
    def change_difficulty(self, new_difficulty):
        """Change AI difficulty"""
        if new_difficulty in self.difficulty_options:
            self.difficulty = new_difficulty
            self.ai_player.difficulty = new_difficulty
            self.message = f"Difficulty changed to {new_difficulty.upper()}"
            self.show_difficulty_menu = False
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        x, y = pos
        
        # Handle difficulty menu
        if self.show_difficulty_menu and hasattr(self, 'diff_rects'):
            for rect, diff in self.diff_rects:
                if rect.collidepoint(pos):
                    self.change_difficulty(diff)
                    return
        
        # Handle button clicks
        for name, button in self.buttons.items():
            # 创建鼠标事件
            mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos)
            if button.handle_event(mouse_event):
                if name == 'undo':
                    self.undo()
                elif name == 'save':
                    self.save_game_record()
                elif name == 'replay':
                    self.reset_game()
                elif name == 'stats':
                    self.show_stats = not self.show_stats
                elif name == 'difficulty':
                    self.show_difficulty_menu = not self.show_difficulty_menu
                elif name == 'exit':
                    self.win_tracker.save_stats()
                    pygame.quit()
                    sys.exit()
                return
        
        # Handle statistics popup close
        if self.show_stats:
            popup_width = 580
            popup_height = 480
            popup_x = (WINDOW_SIZE - popup_width) // 2
            popup_y = (WINDOW_SIZE - popup_height) // 2
            close_rect = pygame.Rect(popup_x + popup_width - 45, popup_y + 18, 32, 32)
            if close_rect.collidepoint(pos):
                self.show_stats = False
                return
        
        # Player move
        if self.game_over or self.current_player != 'X' or self.ai_thinking:
            return
        
        # Calculate board coordinates
        col = round((x - BOARD_PADDING) / CELL_SIZE)
        row = round((y - BOARD_PADDING) / CELL_SIZE)
        
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.player_move((row, col))
    
    def update_hover(self, pos):
        """Update hover position"""
        x, y = pos
        col = round((x - BOARD_PADDING) / CELL_SIZE)
        row = round((y - BOARD_PADDING) / CELL_SIZE)
        
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.hover_pos = (row, col)
        else:
            self.hover_pos = None

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    game.update_win_probability()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.win_tracker.save_stats()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                game.update_hover(event.pos)
                # 更新按钮悬停状态
                for button in game.buttons.values():
                    button.handle_event(event)
        
        game.draw_board()
        game.draw_info_panel()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()