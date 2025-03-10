import math
from functools import lru_cache

# 常量定义
BOARD_SIZE = 15
WIN_COUNT = 5
AI_DEPTH = 2
CENTER = (BOARD_SIZE // 2, BOARD_SIZE // 2)

# 棋盤初始化
board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 打印棋盤
# 打印棋盤（改進對齊）
def print_board():
    # 列標題（對齊）
    print("   " + " ".join(f"{i+1:2}" for i in range(BOARD_SIZE)))  # 列標題從1開始，寬度為2

    # 棋盤內容
    for i in range(BOARD_SIZE):
        # 行標題（對齊）
        print(f"{i+1:2} ", end="")  # 行標題從1開始，寬度為2
        # 棋盤格子內容
        print(" ".join(f"{board[i][j]:2}" for j in range(BOARD_SIZE)))  # 每個格子寬度為2

    print()  # 空行分隔

# 獲取所有可用的落子點 (只考慮已有棋子附近)
def get_available_moves():
    moves = set()
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != '.':
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == '.':
                            moves.add((nr, nc))
    return list(moves) if moves else [CENTER]  # 若無棋，先下中心

# 檢查是否有玩家獲勝
def check_win(player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == player:
                for dr, dc in directions:
                    count = 1
                    for i in range(1, WIN_COUNT):
                        nr, nc = r + i * dr, c + i * dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                            count += 1
                        else:
                            break
                    if count >= WIN_COUNT:
                        return True
    return False

# 局勢評估函數（加強「活三」「活四」判斷）
@lru_cache(maxsize=None)
def evaluate_board(player):
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == '.':
                for dr, dc in directions:
                    my_count, opp_count, open_ends = 0, 0, 0
                    for i in range(1, WIN_COUNT):
                        nr, nc = r + i * dr, c + i * dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                            if board[nr][nc] == player:
                                my_count += 1
                            elif board[nr][nc] == opponent:
                                opp_count += 1
                        else:
                            open_ends -= 1
                    
                    # 強化防守和進攻的評估
                    if my_count == 3 and open_ends >= 0:  # 活三，增加得分
                        score += 500
                    elif my_count == 4 and open_ends >= 0:  # 活四，增加得分
                        score += 10000
                    
                    if opp_count == 3 and open_ends >= 0:  # 對手活三，減少得分
                        score -= 500
                    elif opp_count == 4 and open_ends >= 0:  # 對手活四，減少得分
                        score -= 10000

    return score

# Minimax + Alpha-Beta 剪枝
def minimax(depth, alpha, beta, maximizing):
    if check_win('O'):
        return 100000  # AI 獲勝
    if check_win('X'):
        return -100000  # 玩家獲勝
    if depth == 0 or not get_available_moves():
        return evaluate_board('O')

    if maximizing:
        max_eval = -math.inf
        for move in get_available_moves():
            r, c = move
            board[r][c] = 'O'
            eval = minimax(depth - 1, alpha, beta, False)
            board[r][c] = '.'  # 還原
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in get_available_moves():
            r, c = move
            board[r][c] = 'X'
            eval = minimax(depth - 1, alpha, beta, True)
            board[r][c] = '.'  # 還原
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# AI 下棋
def computer_move():
    best_score = -math.inf
    best_move = None

    for move in get_available_moves():
        r, c = move
        board[r][c] = 'O'
        score = minimax(AI_DEPTH, -math.inf, math.inf, False)
        board[r][c] = '.'  # 還原棋盤

        if score > best_score:
            best_score = score
            best_move = move

    if best_move:
        r, c = best_move
        board[r][c] = 'O'
        return r, c
    return None, None

# 玩家下棋
def player_move():
    while True:
        try:
            row, col = map(int, input("請輸入你的下棋位置 (行 列): ").split())
            row, col = row - 1, col - 1
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == '.':
                board[row][col] = 'X'
                return row, col
            else:
                print("無效的棋步，請重新輸入。")
        except ValueError:
            print("輸入無效，請重新輸入。")

# 遊戲主函數
def main():
    print("五子棋遊戲開始！")
    print_board()

    current_player = 'X'
    moves = 0

    while True:
        if current_player == 'X':
            print("玩家的回合：")
            row, col = player_move()
            moves += 1
            if check_win('X'):
                print_board()
                print("玩家獲勝！")
                break
        else:
            print("電腦的回合：")
            row, col = computer_move()
            moves += 1
            if check_win('O'):
                print_board()
                print("電腦獲勝！")
                break

        print_board()

        if moves == BOARD_SIZE * BOARD_SIZE:
            print("遊戲結束，平局！")
            break

        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()