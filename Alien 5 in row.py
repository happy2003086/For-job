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
BUTTON_HEIGHT = 45
INFO_HEIGHT = 160
TOTAL_HEIGHT = WINDOW_SIZE + BUTTON_HEIGHT + INFO_HEIGHT

# ========== 外星科技風格配色 ==========
BACKGROUND_TOP = (8, 4, 32)
BACKGROUND_BOTTOM = (2, 12, 45)
BOARD_COLOR = (6, 18, 38)
LINE_COLOR = (0, 255, 200)
PLAYER_COLOR = (100, 200, 255)
AI_COLOR = (255, 80, 120)
HOVER_COLOR = (0, 255, 200)
BUTTON_COLOR = (20, 40, 80)
BUTTON_HOVER = (0, 200, 200)
BUTTON_CLICK = (0, 255, 150)
INFO_BG = (4, 12, 28)
ACCENT_GLOW = (0, 255, 200)
WARNING_GLOW = (255, 50, 100)
SUCCESS_GLOW = (0, 255, 150)

font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 20)

# ========== 進階評分系統 ==========
# 棋型分數（極大提高攻擊性同防守性）
PATTERN_SCORES = {
    'FIVE': 10000000,           # 成五
    'LIVE_FOUR': 500000,        # 活四
    'RUSH_FOUR': 200000,        # 衝四（一面被封）
    'LIVE_THREE': 100000,       # 活三
    'SLEEP_THREE': 10000,       # 眠三
    'LIVE_TWO': 5000,           # 活二
    'SLEEP_TWO': 500,           # 眠二
    'LIVE_ONE': 100,            # 活一
}

DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

# 快取評分結果
score_cache = {}

class Particle:
    def __init__(self, x, y, color, particle_type="glow"):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 1.0
        self.color = color
        self.size = random.randint(2, 6)
        self.particle_type = particle_type
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08
        self.life -= 0.025
        return self.life > 0
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * self.life)
            if self.particle_type == "glow":
                for i in range(2):
                    glow_size = self.size + i * 2
                    glow_color = (*self.color[:3], alpha // (i + 2))
                    s = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, glow_color, (glow_size, glow_size), glow_size)
                    screen.blit(s, (int(self.x - glow_size), int(self.y - glow_size)))
            else:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class GlowEffect:
    def __init__(self, x, y, color, radius=30, duration=20):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.duration = duration
        self.current = duration
        
    def update(self):
        self.current -= 1
        return self.current > 0
        
    def draw(self, screen):
        if self.current > 0:
            alpha = int(80 * (self.current / self.duration))
            for i in range(3):
                r = self.radius - i * 8
                if r > 0:
                    glow_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                    glow_color = (*self.color[:3], alpha // (i + 1))
                    pygame.draw.circle(glow_surf, glow_color, (r, r), r)
                    screen.blit(glow_surf, (int(self.x - r), int(self.y - r)))

class Button:
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR, hover_color=BUTTON_HOVER):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        self.is_clicked = False
        self.click_animation = 0
        self.glow_intensity = 0
        
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
        if self.is_hovered:
            self.glow_intensity = min(1.0, self.glow_intensity + 0.1)
        else:
            self.glow_intensity = max(0, self.glow_intensity - 0.05)
            
    def draw(self, screen):
        if self.glow_intensity > 0:
            glow_rect = self.rect.inflate(6, 6)
            for i in range(3):
                r = glow_rect.inflate(-i*2, -i*2)
                pygame.draw.rect(screen, (*BUTTON_HOVER, 30 - i*10), r, border_radius=12)
        
        color = BUTTON_CLICK if self.click_animation > 0 else self.current_color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, ACCENT_GLOW, self.rect, 2, border_radius=10)
        
        if self.is_hovered:
            scan_y = (pygame.time.get_ticks() // 5) % (self.rect.height + 20) - 10
            if self.rect.y <= scan_y <= self.rect.y + self.rect.height:
                pygame.draw.line(screen, (255, 255, 255, 100), 
                               (self.rect.x, scan_y), (self.rect.x + self.rect.width, scan_y), 2)
        
        text_surf = button_font.render(self.text, True, (200, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class EnhancedAIPlayer:
    def __init__(self, difficulty='hard'):
        self.difficulty = difficulty
        self.nodes_evaluated = 0
        self.killer_moves = {}  # 殺手啟發式
        self.history_table = {}  # 歷史啟發式
        
    def get_move(self, game, board, player):
        """主入口：根據難度選擇不同搜尋深度"""
        depth_map = {
            'easy': 1,
            'medium': 2,
            'hard': 4,
            'expert': 6
        }
        depth = depth_map.get(self.difficulty, 4)
        
        # 如果棋盤全空，下天元（中心）
        occupied = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] != '.']
        if not occupied:
            return (BOARD_SIZE // 2, BOARD_SIZE // 2)
        
        self.nodes_evaluated = 0
        opponent = 'X' if player == 'O' else 'O'
        
        # 即時勝利檢查
        immediate = self.find_immediate_win(board, player)
        if immediate:
            return immediate
        
        # 即時防守檢查
        immediate_block = self.find_immediate_win(board, opponent)
        if immediate_block:
            return immediate_block
        
        # Alpha-Beta 搜索
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        moves = self.get_ordered_moves(board, player)
        
        for move in moves[:20]:  # 只考慮前20個最佳候選
            row, col = move
            board[row][col] = player
            score = -self.alpha_beta(board, depth - 1, -beta, -alpha, opponent)
            board[row][col] = '.'
            
            if score > best_score:
                best_score = score
                best_move = move
                alpha = max(alpha, score)
        
        return best_move
    
    def find_immediate_win(self, board, player):
        """檢查能否一步成五"""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == '.':
                    board[i][j] = player
                    if self.check_five(board, i, j, player):
                        board[i][j] = '.'
                        return (i, j)
                    board[i][j] = '.'
        return None
    
    def check_five(self, board, row, col, player):
        """檢查某位置是否形成五連"""
        for dr, dc in DIRECTIONS:
            count = 1
            for step in range(1, 5):
                r, c = row + step * dr, col + step * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                    count += 1
                else:
                    break
            for step in range(1, 5):
                r, c = row - step * dr, col - step * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False
    
    def alpha_beta(self, board, depth, alpha, beta, player):
        """Alpha-Beta剪枝搜索"""
        self.nodes_evaluated += 1
        
        # 檢查勝利狀態
        opponent = 'X' if player == 'O' else 'O'
        
        # 終止條件
        if depth == 0:
            return self.evaluate_board(board, player)
        
        # 檢查是否有五連
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == player:
                    if self.check_five(board, i, j, player):
                        return 10000000 + depth
                elif board[i][j] == opponent:
                    if self.check_five(board, i, j, opponent):
                        return -10000000 - depth
        
        moves = self.get_ordered_moves(board, player)
        if not moves:
            return 0
        
        best_score = float('-inf')
        
        for move in moves[:15]:  # 限制分支因子
            row, col = move
            board[row][col] = player
            score = -self.alpha_beta(board, depth - 1, -beta, -alpha, opponent)
            board[row][col] = '.'
            
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            
            if alpha >= beta:
                # 記錄殺手移動
                self.killer_moves[depth] = move
                break
        
        return best_score
    
    def get_ordered_moves(self, board, player):
        """獲取排序後的候選移動（啟發式排序）"""
        candidates = []
        occupied = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] != '.']
        
        # 生成候選位置（距離現有棋子2格內）
        move_set = set()
        for i, j in occupied:
            for di in range(-2, 3):
                for dj in range(-2, 3):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE and board[ni][nj] == '.':
                        move_set.add((ni, nj))
        
        if not move_set:
            return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
        
        # 為每個候選位置評分
        opponent = 'X' if player == 'O' else 'O'
        for move in move_set:
            row, col = move
            board[row][col] = player
            attack_score = self.evaluate_position(board, row, col, player)
            board[row][col] = '.'
            
            board[row][col] = opponent
            defense_score = self.evaluate_position(board, row, col, opponent)
            board[row][col] = '.'
            
            # 組合攻擊分和防守分
            total_score = attack_score * 1.1 + defense_score
            
            # 中心加成
            center = BOARD_SIZE // 2
            center_dist = abs(row - center) + abs(col - center)
            total_score += (BOARD_SIZE - center_dist) * 100
            
            candidates.append((total_score, move))
        
        candidates.sort(key=lambda x: x[0], reverse=True)
        return [move for _, move in candidates]
    
    def evaluate_board(self, board, player):
        """評估整個棋盤局勢"""
        opponent = 'X' if player == 'O' else 'O'
        score = 0
        
        # 評估所有方向的所有可能
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == player:
                    score += self.evaluate_position(board, i, j, player)
                elif board[i][j] == opponent:
                    score -= self.evaluate_position(board, i, j, opponent) * 1.05  # 稍加重視防守
        
        return score
    
    def evaluate_position(self, board, row, col, player):
        """精確評估某位置在各方向的棋型"""
        total_score = 0
        
        for dr, dc in DIRECTIONS:
            line = self.extract_line(board, row, col, dr, dc, player)
            total_score += self.score_line(line)
        
        return total_score
    
    def extract_line(self, board, row, col, dr, dc, player):
        """提取一條線上的棋型"""
        line = []
        # 向正方向
        for step in range(5):
            r, c = row + step * dr, col + step * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                line.append(board[r][c])
            else:
                line.append('#')  # 邊界視為阻擋
        
        # 向反方向（不重複當前位置）
        reverse = []
        for step in range(1, 5):
            r, c = row - step * dr, col - step * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                reverse.insert(0, board[r][c])
            else:
                reverse.insert(0, '#')
        
        full_line = reverse + [player] + line[1:]
        
        # 計算連續和開放度
        count = 1
        open_left = 0
        open_right = 0
        
        # 向右計算
        for i in range(5, len(full_line)):
            if full_line[i] == player:
                count += 1
            elif full_line[i] == '.':
                open_right += 1
                break
            else:
                break
        
        # 向左計算
        for i in range(3, -1, -1):
            if full_line[i] == player:
                count += 1
            elif full_line[i] == '.':
                open_left += 1
                break
            else:
                break
        
        return (count, open_left + open_right)
    
    def score_line(self, line_info):
        """根據連子數和開放度計算分數"""
        count, open_ends = line_info
        
        if count >= 5:
            return PATTERN_SCORES['FIVE']
        
        if count == 4:
            if open_ends >= 2:
                return PATTERN_SCORES['LIVE_FOUR']
            elif open_ends == 1:
                return PATTERN_SCORES['RUSH_FOUR']
            return 0
        
        if count == 3:
            if open_ends >= 2:
                return PATTERN_SCORES['LIVE_THREE']
            elif open_ends == 1:
                return PATTERN_SCORES['SLEEP_THREE']
            return 0
        
        if count == 2:
            if open_ends >= 2:
                return PATTERN_SCORES['LIVE_TWO']
            elif open_ends == 1:
                return PATTERN_SCORES['SLEEP_TWO']
            return 0
        
        if count == 1:
            return PATTERN_SCORES['LIVE_ONE'] if open_ends >= 2 else 50
        
        return 0

class WinRateTracker:
    def __init__(self):
        self.total_games = self.player_wins = self.computer_wins = self.draws = 0
        self.current_game_moves = []
        self.winrate_history = []
        self.move_times = []
        
    def reset_stats(self):
        """重置所有統計數據"""
        self.total_games = 0
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0
        self.current_game_moves.clear()
        self.winrate_history.clear()
        self.move_times.clear()
        self.save_stats()
        
    def add_game_result(self, winner):
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
                'avg_thinking_time': sum(self.move_times) / len(self.move_times) if self.move_times else 0
            })
            self.current_game_moves.clear()
            self.move_times.clear()
    
    def add_move_winrate(self, winrate, thinking_time=0):
        self.current_game_moves.append({'X': winrate['X'], 'O': winrate['O']})
        if thinking_time > 0:
            self.move_times.append(thinking_time)
    
    def get_player_win_rate(self):
        return round((self.player_wins / self.total_games) * 100, 1) if self.total_games > 0 else 0
    
    def get_computer_win_rate(self):
        return round((self.computer_wins / self.total_games) * 100, 1) if self.total_games > 0 else 0
    
    def calculate_current_winrate(self, board, current_player):
        """計算當前局面嘅估計勝率"""
        if not board:
            return {'X': 50.0, 'O': 50.0}
        
        p_score = 1
        c_score = 1
        ai = EnhancedAIPlayer()
        
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 'X':
                    p_score += ai.evaluate_position(board, i, j, 'X')
                elif board[i][j] == 'O':
                    c_score += ai.evaluate_position(board, i, j, 'O')
        
        total = p_score + c_score
        if total == 0:
            return {'X': 50.0, 'O': 50.0}
        
        p_rate = (p_score / total) * 100
        p_rate = max(5, min(95, p_rate))
        
        if current_player == 'O':
            p_rate = max(5, p_rate - 10)
        
        return {'X': round(p_rate, 1), 'O': round(100 - p_rate, 1)}
    
    def save_stats(self, filename="winrate_stats.json"):
        stats = {
            'total_games': self.total_games,
            'player_wins': self.player_wins,
            'computer_wins': self.computer_wins,
            'draws': self.draws
        }
        with open(filename, 'w') as f:
            json.dump(stats, f)
    
    def load_stats(self, filename="winrate_stats.json"):
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.total_games = data.get('total_games', 0)
                    self.player_wins = data.get('player_wins', 0)
                    self.computer_wins = data.get('computer_wins', 0)
                    self.draws = data.get('draws', 0)
            except:
                pass

class Game:
    def __init__(self):
        self.board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.history = []
        self.move_history = []
        self.win_probability = {'X': 50.0, 'O': 50.0}
        self.game_over = False
        self.winner = None
        self.message = "🛸 Alien System Online. Initiate Connection."
        self.hover_pos = None
        self.ai_thinking = False
        self.ai_thinking_time = 0
        self.last_move = None
        self.difficulty = 'hard'
        self.difficulty_options = ['easy', 'medium', 'hard', 'expert']
        
        button_width = 140
        button_height = BUTTON_HEIGHT
        button_gap = 20
        total_width = button_width * 2 + button_gap
        start_x = (WINDOW_SIZE - total_width) // 2
        button_y = WINDOW_SIZE + 10

        self.buttons = {
            'restart': Button(start_x, button_y, button_width, button_height, '⟳ RESTART'),
            'reset_stats': Button(start_x + button_width + button_gap, button_y, button_width, button_height, '📊 RESET STATS')
        }

        self.ai_player = EnhancedAIPlayer(self.difficulty)
        self.win_tracker = WinRateTracker()
        self.win_tracker.load_stats()
        self.particles = []
        self.move_indicators = []
        self.flash_timer = 0
        self.glow_effects = []
        self.starfield = [(random.randint(0, WINDOW_SIZE), random.randint(0, TOTAL_HEIGHT), random.randint(1, 3)) for _ in range(100)]
        self.scan_line_offset = 0

    def restart_game(self):
        self.board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.cu
