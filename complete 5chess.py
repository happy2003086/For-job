import random

BOARD_SIZE = 15
board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board():
    """打印棋盤"""
    max_width = len(str(BOARD_SIZE))
    
    print(" " * (max_width + 1), end="")
    for i in range(BOARD_SIZE):
        print(f"{i+1:>{max_width}}", end=" ")
    print()

    for i in range(BOARD_SIZE):
        print(f"{i+1:>{max_width}}", end=" ")
        for j in range(BOARD_SIZE):
            print(f"{board[i][j]:>{max_width}}", end=" ")
        print()

def check_win(row, col, player):
    """檢查是否有五顆連續的子"""
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

def evaluate_position(row, col, player):
    """評估某個落點的分數"""
    if board[row][col] != '.':
        return -1  # 不能下在已經有子的地方
    
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  
        open_ends = 0  # 活三、活四的關鍵

        # 計算正方向
        for i in range(1, 5):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if board[r][c] == player:
                    count += 1
                elif board[r][c] == '.':
                    open_ends += 1
                    break
                else:
                    break
        
        # 計算反方向
        for i in range(1, 5):
            r, c = row - i * dr, col - i * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if board[r][c] == player:
                    count += 1
                elif board[r][c] == '.':
                    open_ends += 1
                    break
                else:
                    break

        if count >= 5:
            return 100000  # 立即獲勝
        elif count == 4:
            if open_ends == 2:
                score += 10000  # 活四（兩端開放）
            elif open_ends == 1:
                score += 5000   # 死四（單端開放）
        elif count == 3:
            if open_ends == 2:
                score += 1000   # 活三（兩端開放）
            elif open_ends == 1:
                score += 500    # 死三
        elif count == 2:
            if open_ends == 2:
                score += 100    # 活二

    return score

def get_best_move():
    """選擇最佳的落子位置"""
    best_score = -1
    best_move = None

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] != '.':
                continue  # 跳過已經有子的地方

            # **進攻：優先嘗試獲勝**
            attack_score = evaluate_position(row, col, 'O')
            if attack_score >= 100000:
                return (row, col)  # 直接獲勝

            # **防守：如果對手快贏，強制防守**
            defense_score = evaluate_position(row, col, 'X')
            if defense_score >= 100000:
                return (row, col)  # 立即封鎖

            # **總分 = 進攻 + 防守**
            total_score = attack_score + defense_score
            if total_score > best_score:
                best_score = total_score
                best_move = (row, col)

    return best_move

def player_move():
    """玩家落子"""
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

def computer_move():
    """電腦落子"""
    if all(board[row][col] == '.' for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)):
        row, col = BOARD_SIZE // 2, BOARD_SIZE // 2  # 第一手棋下在正中間
    else:
        row, col = get_best_move()

    board[row][col] = 'O'
    return row, col

def main():
    print("五子棋遊戲開始！")
    print_board()

    current_player = 'X'  # 玩家先行

    while True:
        if current_player == 'X':
            print("玩家的回合：")
            row, col = player_move()
        else:
            print("電腦的回合：")
            row, col = computer_move()

        print_board()

        if check_win(row, col, current_player):
            print(f"{'玩家' if current_player == 'X' else '電腦'} 獲勝！")
            break

        if all(board[r][c] != '.' for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
            print("遊戲結束，平局！")
            break

        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()
