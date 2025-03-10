import random

def print_board(board):
    """顯示棋盤"""
    print("  " + " ".join(str(i + 1) for i in range(len(board[0]))))
    for i, row in enumerate(board):
        print(str(i + 1) + " " + " ".join(row))

def create_board(rows, cols, num_mines):
    """建立地雷棋盤"""
    board = [["-" for _ in range(cols)] for _ in range(rows)]
    mines = random.sample(range(rows * cols), num_mines)
    mine_positions = set()

    for mine in mines:
        row, col = divmod(mine, cols)
        board[row][col] = "X"
        mine_positions.add((row, col))

    return board, mine_positions

def count_adjacent_mines(board, row, col):
    """計算某格周圍的地雷數"""
    count = 0
    for i in range(max(0, row - 1), min(len(board), row + 2)):
        for j in range(max(0, col - 1), min(len(board[0]), col + 2)):
            if board[i][j] == "X":
                count += 1
    return count

def reveal_cell(board, visible_board, row, col, mine_positions):
    """揭示某格，並展開空白區域"""
    if (row, col) in mine_positions:
        return False  # 踩到地雷，遊戲結束
    
    if visible_board[row][col] != "-":  
        return True  # 這格已經被揭示

    count = count_adjacent_mines(board, row, col)
    visible_board[row][col] = str(count) if count > 0 else " "

    # 當 count 為 0，則遞歸展開相鄰格
    if count == 0:
        for i in range(max(0, row - 1), min(len(board), row + 2)):
            for j in range(max(0, col - 1), min(len(board[0]), col + 2)):
                if (i, j) != (row, col):
                    reveal_cell(board, visible_board, i, j, mine_positions)

    return True

def is_win(visible_board, mine_positions):
    """檢查是否已經勝利（所有非地雷格都已經揭示）"""
    for r in range(len(visible_board)):
        for c in range(len(visible_board[0])):
            if visible_board[r][c] == "-" and (r, c) not in mine_positions:
                return False
    return True

def main():
    rows, cols, num_mines = 8, 8, 10
    board, mine_positions = create_board(rows, cols, num_mines)
    visible_board = [["-" for _ in range(cols)] for _ in range(rows)]

    print("💣 掃雷遊戲開始！")
    
    while True:
        print_board(visible_board)
        move = input("輸入行 列 (或輸入 'F 行 列' 來標記地雷): ").split()
        
        if len(move) == 3 and move[0].upper() == "F":
            try:
                row, col = int(move[1]) - 1, int(move[2]) - 1
                if visible_board[row][col] == "-":
                    visible_board[row][col] = "F"
                elif visible_board[row][col] == "F":
                    visible_board[row][col] = "-"  # 取消標記
            except (ValueError, IndexError):
                print("輸入錯誤，請輸入有效的行列數字。")
            continue
        
        try:
            row, col = int(move[0]) - 1, int(move[1]) - 1
            if not (0 <= row < rows and 0 <= col < cols):
                print("輸入超出範圍，請重新輸入！")
                continue

            if not reveal_cell(board, visible_board, row, col, mine_positions):
                print_board(board)
                print("💥 你踩到地雷了，遊戲結束！")
                break

            if is_win(visible_board, mine_positions):
                print_board(visible_board)
                print("🎉 恭喜，你贏了！")
                break

        except (ValueError, IndexError):
            print("輸入錯誤，請輸入有效的行列數字。")

if __name__ == "__main__":
    main()
