import random
import time
from collections import defaultdict

BOARD_SIZE = 15
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

def print_board(board):
    max_width = len(str(BOARD_SIZE))
    col_labels = [chr(ord('A') + i) if i < 8 else chr(ord('A') + i + 1) for i in range(BOARD_SIZE)]
    print(" " * (max_width + 1), end="")
    for label in col_labels:
        print(f"{label:>{max_width}}", end=" ")
    print()
    for i in range(BOARD_SIZE):
        print(f"{i+1:>{max_width}}", end=" ")
        for j in range(BOARD_SIZE):
            print(f"{board[i][j]:>{max_width}}", end=" ")
        print(f"{i+1:>{max_width}}")
    print(" " * (max_width + 1), end="")
    for label in col_labels:
        print(f"{label:>{max_width}}", end=" ")
    print()

def check_win(row, col, player, board):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 5):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - i * dr, col - i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

def evaluate_pattern(count, open_ends):
    if count >= 5:
        return 'FIVE'
    if count == 4:
        if open_ends == 2:
            return 'LIVE_FOUR'
        elif open_ends == 1:
            return 'FOUR'
    if count == 3:
        if open_ends == 2:
            return 'LIVE_THREE'
        elif open_ends == 1:
            return 'THREE'
    if count == 2:
        if open_ends == 2:
            return 'LIVE_TWO'
        elif open_ends == 1:
            return 'TWO'
    if count == 1 and open_ends == 2:
        return 'ONE'
    return None

def evaluate_position(row, col, player, board):
    if board[row][col] != '.':
        return -1
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    pattern_counts = defaultdict(int)
    for dr, dc in directions:
        count = 1
        open_ends = 0
        for i in range(1, 6):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if board[r][c] == player:
                    count += 1
                elif board[r][c] == '.':
                    open_ends += 1
                    break
                else:
                    break
            else:
                break
        for i in range(1, 6):
            r, c = row - i * dr, col - i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if board[r][c] == player:
                    count += 1
                elif board[r][c] == '.':
                    open_ends += 1
                    break
                else:
                    break
            else:
                break
        pattern = evaluate_pattern(count, open_ends)
        if pattern:
            pattern_counts[pattern] += 1
    if pattern_counts.get('FIVE', 0) > 0:
        return PATTERN_SCORES['FIVE']
    if pattern_counts.get('LIVE_FOUR', 0) > 0 or pattern_counts.get('FOUR', 0) >= 2:
        return PATTERN_SCORES['LIVE_FOUR']
    for pattern, cnt in pattern_counts.items():
        score += PATTERN_SCORES[pattern] * cnt
    if pattern_counts.get('LIVE_THREE', 0) >= 2:
        score += PATTERN_SCORES['LIVE_THREE'] * 2
    return score

def get_valid_moves(board):
    moves = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != '.':
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE and board[ni][nj] == '.':
                            moves.add((ni, nj))
    if not moves:
        moves.add((BOARD_SIZE//2, BOARD_SIZE//2))
    return list(moves)

def get_best_move(board):
    valid_moves = get_valid_moves(board)
    if not valid_moves:
        return (BOARD_SIZE//2, BOARD_SIZE//2)
    best_score = -1
    best_move = random.choice(valid_moves)
    for (row, col) in valid_moves:
        attack_score = evaluate_position(row, col, 'O', board)
        if attack_score >= PATTERN_SCORES['FIVE']:
            return (row, col)
        defense_score = evaluate_position(row, col, 'X', board)
        if defense_score >= PATTERN_SCORES['FIVE']:
            return (row, col)
        total_score = attack_score * 1.2 + defense_score
        if total_score > best_score:
            best_score = total_score
            best_move = (row, col)
    return best_move

def player_move(board):
    while True:
        try:
            input_str = input("請輸入你的下棋位置 (如 A1 或 1A): ").strip().upper()
            if len(input_str) >= 2:
                if input_str[0].isalpha() and input_str[1:].isdigit():
                    col = ord(input_str[0]) - ord('A')
                    if col > 7:
                        col -= 1
                    row = int(input_str[1:]) - 1
                elif input_str[-1].isalpha() and input_str[:-1].isdigit():
                    col = ord(input_str[-1]) - ord('A')
                    if col > 7:
                        col -= 1
                    row = int(input_str[:-1]) - 1
                else:
                    raise ValueError
            else:
                raise ValueError
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == '.':
                board[row][col] = 'X'
                return row, col
            else:
                print("無效的棋步，請重新輸入。")
        except (ValueError, IndexError):
            print("輸入無效，請使用格式如 A1 或 1A。")

def computer_move(board):
    print("電腦思考中", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()
    row, col = get_best_move(board)
    board[row][col] = 'O'
    print(f"電腦下在 {chr(ord('A') + col if col < 8 else ord('A') + col + 1)}{row + 1}")
    return row, col

def reset_board():
    return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def play_again():
    while True:
        replay = input("是否再玩一局？(y/n): ").strip().lower()
        if replay in ['y', 'n']:
            return replay == 'y'
        else:
            print("請輸入 'y' 或 'n'。")

def main():
    print("歡迎玩五子棋！")
    while True:
        board = reset_board()
        print_board(board)
        while True:
            print("Player's turn")
            row, col = player_move(board)  # Player move
            print_board(board)
            if check_win(row, col, 'X', board):
                print("你贏了！")
                break
            print("Computer's turn")
            row, col = computer_move(board)  # Computer move
            print_board(board)
            if check_win(row, col, 'O', board):
                print("電腦贏了！")
                break
        if not play_again():
            print("感謝遊玩，再見！")
            break
if __name__ == "__main__":
    main()