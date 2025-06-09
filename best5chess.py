import random
import time
import shutil
from collections import defaultdict
from datetime import datetime
import os
import pygame
import sys

# 初始化pygame，嘩，終於開始啦～
pygame.init()

# 游戏常量，唔好搞錯啊～
BOARD_SIZE = 15
CELL_SIZE = 40
BOARD_PADDING = 50
WINDOW_SIZE = BOARD_PADDING * 2 + CELL_SIZE * (BOARD_SIZE - 1)
BUTTON_HEIGHT = 40
INFO_HEIGHT = 80
TOTAL_HEIGHT = WINDOW_SIZE + BUTTON_HEIGHT + INFO_HEIGHT

# 颜色定义，睇得舒服啲～
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

# 创建窗口，開工啦～
screen = pygame.display.set_mode((WINDOW_SIZE, TOTAL_HEIGHT))
pygame.display.set_caption("五子棋游戏")

# 字体，文字清晰最重要～
font = pygame.font.SysFont(None, 24)
title_font = pygame.font.SysFont(None, 36)

# 棋子评分规则，呢啲超重要嘅～
PATTERN_SCORES = {
    'FIVE': 1000000,
    'LIVE_FOUR': 100000,
    'FOUR': 10000,
    'LIVE_THREE': 1000,
    'THREE': 100,
    'LIVE_TWO': 10,
    'TWO': 5,
    'ONE': 1
}

class Game:
    def __init__(self):
        self.board = self.reset_board()
        self.current_player = 'X'  # 玩家先手，咁先公平啲～
        self.history = []  # 记录棋步历史，唔好忘記啊～
        self.win_probability = {'X': 0, 'O': 0}  # 双方胜率，睇下邊個勝算大～
        self.move_history = []  # 棋谱记录
        self.start_time = None  # 游戏开始时间
        self.game_record = {
            'metadata': {
                'date': '',
                'players': {'X': '玩家', 'O': '电脑'},
                'result': '未完成'
            },
            'moves': []
        }
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.message = "欢迎来玩五子棋！"
        self.hover_pos = None
        self.buttons = {
            'undo': {'rect': pygame.Rect(20, WINDOW_SIZE + 10, 80, BUTTON_HEIGHT), 'text': '悔棋'},
            'save': {'rect': pygame.Rect(120, WINDOW_SIZE + 10, 80, BUTTON_HEIGHT), 'text': '保存棋谱'},
            'replay': {'rect': pygame.Rect(220, WINDOW_SIZE + 10, 80, BUTTON_HEIGHT), 'text': '重新开始'},
            'exit': {'rect': pygame.Rect(320, WINDOW_SIZE + 10, 80, BUTTON_HEIGHT), 'text': '退出游戏'}
        }

    def reset_board(self):
        # 重置棋盤，重新開始咯～
        return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def draw_board(self):
        # 绘制棋盘背景，漂亮喇～
        screen.fill(BACKGROUND)
        
        # 绘制棋盘网格，唔好走雞～
        for i in range(BOARD_SIZE):
            # 横线
            pygame.draw.line(screen, LINE_COLOR, 
                            (BOARD_PADDING, BOARD_PADDING + i * CELL_SIZE), 
                            (BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE), 
                            2)
            # 竖线
            pygame.draw.line(screen, LINE_COLOR, 
                            (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING), 
                            (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE), 
                            2)
        
        # 绘制棋盘上的五个点，定海神针咁重要嘅～
        points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        for point in points:
            x, y = point
            pygame.draw.circle(screen, BLACK, 
                             (BOARD_PADDING + x * CELL_SIZE, BOARD_PADDING + y * CELL_SIZE), 
                             5)
        
        # 绘制棋子，落子啦～
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
        
        # 绘制最后一步标记，好似聚光燈咁閃～
        if self.last_move:
            row, col, player = self.last_move
            pygame.draw.circle(screen, RED if player == 'X' else BLUE, 
                             (BOARD_PADDING + col * CELL_SIZE, BOARD_PADDING + row * CELL_SIZE), 
                             5)
        
        # 绘制鼠标悬停位置，提示下一步喺邊～
        if self.hover_pos and not self.game_over:
            row, col = self.hover_pos
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == '.':
                pygame.draw.circle(screen, GREEN, 
                                 (BOARD_PADDING + col * CELL_SIZE, BOARD_PADDING + row * CELL_SIZE), 
                                 5)
    
    def draw_info_panel(self):
        # 绘制信息面板背景，睇得舒服啲～
        pygame.draw.rect(screen, INFO_BG, (0, WINDOW_SIZE, WINDOW_SIZE, BUTTON_HEIGHT + INFO_HEIGHT))
        
        # 绘制按钮，方便操作～
        for name, button in self.buttons.items():
            color = BUTTON_HOVER if button['rect'].collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
            pygame.draw.rect(screen, color, button['rect'], border_radius=5)
            text = font.render(button['text'], True, WHITE)
            screen.blit(text, (button['rect'].centerx - text.get_width() // 2, 
                             button['rect'].centery - text.get_height() // 2))
        
        # 绘制游戏信息，實時更新～
        status_text = f"当前玩家: {'玩家(X)' if self.current_player == 'X' else '电脑(O)'}"
        if self.game_over:
            if self.winner == 'X':
                status_text = "玩家获胜!"
            elif self.winner == 'O':
                status_text = "电脑获胜!"
            else:
                status_text = "游戏结束!"
        
        status_surf = font.render(status_text, True, WHITE)
        screen.blit(status_surf, (420, WINDOW_SIZE + 15))
        
        # 绘制胜率信息，咁你就知勝算几多啦～
        prob_text = f"胜率评估: 玩家 {self.win_probability['X']}% - 电脑 {self.win_probability['O']}%"
        prob_surf = font.render(prob_text, True, WHITE)
        screen.blit(prob_surf, (420, WINDOW_SIZE + 45))
        
        # 绘制消息，保持互動～
        msg_surf = font.render(self.message, True, GREEN)
        screen.blit(msg_surf, (20, WINDOW_SIZE + BUTTON_HEIGHT + 20))
    
    def check_win(self, row, col, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
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

    def evaluate_pattern(self, count, open_ends):
        # 評分簡化版，簡單啲咁計～
        if count >= 5:
            return PATTERN_SCORES['FIVE']
        if count == 4:
            if open_ends == 2:
                return PATTERN_SCORES['LIVE_FOUR']
            elif open_ends == 1:
                return PATTERN_SCORES['FOUR']
        if count == 3:
            if open_ends == 2:
                return PATTERN_SCORES['LIVE_THREE']
            elif open_ends == 1:
                return PATTERN_SCORES['THREE']
        if count == 2:
            if open_ends == 2:
                return PATTERN_SCORES['LIVE_TWO']
            elif open_ends == 1:
                return PATTERN_SCORES['TWO']
        if count == 1:
            return PATTERN_SCORES['ONE']
        return 0

    def evaluate_position(self, row, col, player):
        # 評分方法，根據棋形計分啦～
        total_score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            open_ends = 0
            
            # 前面連珠數
            i = 1
            while True:
                r, c = row + i * dr, col + i * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if self.board[r][c] == player:
                        count += 1
                        i += 1
                    elif self.board[r][c] == '.':
                        open_ends += 1
                        break
                    else:
                        break
                else:
                    break
            
            # 後面連珠數
            i = 1
            while True:
                r, c = row - i * dr, col - i * dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if self.board[r][c] == player:
                        count += 1
                        i += 1
                    elif self.board[r][c] == '.':
                        open_ends += 1
                        break
                    else:
                        break
                else:
                    break

            total_score += self.evaluate_pattern(count + 1, open_ends)  # +1 因為包含該點本身
        return total_score

    def get_valid_moves(self):
        # 搵空格，落子位揾到喇～
        valid_moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == '.':
                    valid_moves.append((i, j))
        return valid_moves

    def get_best_move(self):
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            # 冇得落先，中心落子啦～
            return (BOARD_SIZE // 2, BOARD_SIZE // 2)

        best_score = -float('inf')
        best_move = random.choice(valid_moves)

        for (row, col) in valid_moves:
            attack_score = self.evaluate_position(row, col, 'O')
            defense_score = self.evaluate_position(row, col, 'X')

            # 必须先拦截或者先赢嘅地方直接落子
            if attack_score >= PATTERN_SCORES['FIVE']:
                return (row, col)
            if defense_score >= PATTERN_SCORES['FIVE']:
                return (row, col)

            # 计算总分数：进攻权重高啲，防守次之
            total_score = attack_score * 1.3 + defense_score * 1.0
            if total_score > best_score:
                best_score = total_score
                best_move = (row, col)

        return best_move

    def make_move(self, row, col, player):
        if self.board[row][col] == '.' and not self.game_over:
            self.board[row][col] = player
            self.history.append((row, col, player))
            self.last_move = (row, col, player)
            self.move_history.append({'player': player, 'row': row, 'col': col})
            self.game_record['moves'].append({'player': player, 'row': row, 'col': col})
            self.message = f"{'玩家' if player == 'X' else '电脑'} 落子於 ({row}, {col}) 嘞～"

            if self.check_win(row, col, player):
                self.game_over = True
                self.winner = player
                self.message = f"{'玩家' if player == 'X' else '电脑'} 贏咗喇，恭喜！"
                self.game_record['metadata']['result'] = f"{player}获胜"
            else:
                # 双方胜率简易估算，哈哈～
                total_moves = len(self.history)
                win_rate_x = max(0, 50 - total_moves)
                win_rate_o = max(0, 50 - win_rate_x)
                self.win_probability = {'X': win_rate_x, 'O': win_rate_o}

                self.current_player = 'O' if player == 'X' else 'X'
                if self.current_player == 'O':
                    self.message = "轮到电脑行动喇，等住佢啦～"

    def undo_move(self):
        if self.history and not self.game_over:
            last_move = self.history.pop()
            row, col, player = last_move
            self.board[row][col] = '.'
            self.move_history.pop()
            self.game_record['moves'].pop()
            self.current_player = player
            self.message = f"悔棋成功，轮到 {'玩家' if player == 'X' else '电脑'} 咯！"
            self.last_move = self.history[-1] if self.history else None

    def save_game_record(self):
        if not os.path.exists('records'):
            os.mkdir('records')
        now = datetime.now()
        filename = now.strftime("records/gomoku_%Y%m%d_%H%M%S.json")
        import json
        self.game_record['metadata']['date'] = now.strftime("%Y-%m-%d %H:%M:%S")
        self.game_record['metadata']['players']['X'] = '玩家'
        self.game_record['metadata']['players']['O'] = '电脑'
        if self.winner:
            self.game_record['metadata']['result'] = f"{self.winner}获胜"
        else:
            self.game_record['metadata']['result'] = "未完成"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.game_record, f, ensure_ascii=False, indent=2)
        self.message = f"棋谱已保存到 {filename} 嘞！"

    def replay_game(self):
        self.board = self.reset_board()
        self.current_player = 'X'
        self.history = []
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.message = "重新开始游戏，准备好喇～"

    def handle_click(self, pos):
        if self.game_over:
            self.message = "游戏已结束，按重新开始继续～"
            return

        x, y = pos
        # 点中按钮先，先睇吓～
        for name, button in self.buttons.items():
            if button['rect'].collidepoint(pos):
                if name == 'undo':
                    self.undo_move()
                elif name == 'save':
                    self.save_game_record()
                elif name == 'replay':
                    self.replay_game()
                elif name == 'exit':
                    pygame.quit()
                    sys.exit()
                return

        # 落子操作，換算位置先～
        col = round((x - BOARD_PADDING) / CELL_SIZE)
        row = round((y - BOARD_PADDING) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if self.board[row][col] == '.' and self.current_player == 'X':
                self.make_move(row, col, 'X')

    def ai_move(self):
        if self.game_over or self.current_player != 'O':
            return
        time.sleep(0.5)  # 假裝思考中～
        row, col = self.get_best_move()
        self.make_move(row, col, 'O')

    def update_hover(self):
        if self.game_over or self.current_player != 'X':
            self.hover_pos = None
            return
        x, y = pygame.mouse.get_pos()
        col = round((x - BOARD_PADDING) / CELL_SIZE)
        row = round((y - BOARD_PADDING) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if self.board[row][col] == '.':
                self.hover_pos = (row, col)
            else:
                self.hover_pos = None
        else:
            self.hover_pos = None

def main():
    game = Game()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
        
        game.update_hover()
        game.ai_move()
        game.draw_board()
        game.draw_info_panel()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()