import random

# 定義棋盤大小
BOARD_SIZE = 15

# 定義棋盤
board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 記錄步數
player_moves = 0
computer_moves = 0

# 打印棋盤
def print_board():
    global player_moves, computer_moves

    # 計算列標題所需的空格數
    max_column_width = len(str(BOARD_SIZE))

    # 打印列標題，右對齊
    print(" " * (max_column_width + 1), end="")  # 留出適當的空間
    for i in range(BOARD_SIZE):
        print(f"{i+1:>{max_column_width}}", end=" ")  # 列標題右對齊
    print()

    # 打印棋盤的每一行
    for i in range(BOARD_SIZE):
        # 每行的數字右對齊
        print(f"{i+1:>{max_column_width}} ", end="")  # 行標題右對齊
        for j in range(BOARD_SIZE):
            print(f"{board[i][j]:>{max_column_width}}", end=" ")  # 格子右對齊
        print()

    # 顯示步數
    print(f"\n玩家已下 {player_moves} 步")
    print(f"電腦已下 {computer_moves} 步")

# 檢查是否有玩家獲勝
def check_win(row, col, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、兩條斜線
    for dr, dc in directions:
        count = 1

        # 向正方向檢查
        for i in range(1, 5):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break

        # 向反方向檢查
        for i in range(1, 5):
            r, c = row - i * dr, col - i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break

        if count >= 5:
            return True

    return False

# 評估每個步驟的分數
def evaluate_move(row, col, player):
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、兩條斜線

    for dr, dc in directions:
        count = 1

        # 向正方向檢查
        for i in range(1, 5):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break

        # 向反方向檢查
        for i in range(1, 5):
            r, c = row - i * dr, col - i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break

        score += count

    return score

# 評估對方的威脅
def evaluate_defense(row, col, player):
    opponent = 'O' if player == 'X' else 'X'
    defense_score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、兩條斜線

    for dr, dc in directions:
        count = 0
        # 向正方向檢查
        for i in range(1, 5):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
                count += 1
            else:
                break

        # 向反方向檢查
        for i in range(1, 5):
            r, c = row - i * dr, col - i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
                count += 1
            else:
                break

        if count == 4:
            defense_score += 100  # 防守高分
        elif count == 3:
            defense_score += 50   # 防守中等分

    return defense_score

# 檢查是否有空位
def get_available_moves():
    available_moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == '.':
                available_moves.append((r, c))
    return available_moves

# 玩家下棋
def player_move():
    global player_moves  # 使用全局變量來追蹤玩家的步數
    while True:
        try:
            row, col = map(int, input("請輸入你的下棋位置 (行 列): ").split())
            row, col = row - 1, col - 1  # 調整為 0 基索引
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == '.':
                board[row][col] = 'X'
                player_moves += 1  # 玩家下了一步，步數加1
                return row, col
            else:
                print("無效的棋步，請重新輸入。")
        except ValueError:
            print("輸入無效，請重新輸入。")

# 電腦下棋
def computer_move():
    global computer_moves  # 使用全局變量來追蹤電腦的步數
    best_score = -1
    best_move = None

    available_moves = get_available_moves()
    for move in available_moves:
        row, col = move
        # 防守優先：檢查對方的威脅
        defense_score = evaluate_defense(row, col, 'O')
        if defense_score > best_score:
            best_score = defense_score
            best_move = move

    if best_move:
        row, col = best_move
        board[row][col] = 'O'
        computer_moves += 1  # 電腦下了一步，步數加1
        return row, col

# 主遊戲邏輯
def main():
    print("五子棋遊戲開始！")
    print_board()

    current_player = 'X'  # 玩家 'X' 先行
    moves = 0

    while True:
        if current_player == 'X':
            print("玩家的回合：")
            row, col = player_move()
            moves += 1

            if check_win(row, col, 'X'):
                print_board()
                print("玩家獲勝！")
                break
        else:
            print("電腦的回合：")
            row, col = computer_move()
            moves += 1

            if check_win(row, col, 'O'):
                print_board()
                print("電腦獲勝！")
                break

        print_board()
        
        # 如果棋盤已滿，平局
        if moves == BOARD_SIZE * BOARD_SIZE:
            print_board()
            print("遊戲結束，平局！")
            break

        # 換玩家
        current_player = 'O' if current_player == 'X' else 'X'

# 運行遊戲
if __name__ == "__main__":
    main()
