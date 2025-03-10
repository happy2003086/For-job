def is_valid(board, row, col, num):
    """檢查數字 num 是否可以放在 board[row][col]"""
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    
    box_x, box_y = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_x + i][box_y + j] == num:
                return False
    return True

def solve_sudoku(board):
    """回溯演算法解數獨"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False  # 無法填入數字，回溯
    return True  # 解決數獨

def print_board(board):
    """格式化輸出數獨盤面"""
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))

# 測試數獨盤面 (0 代表空格)
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# 如果這個文件作為主程序運行
if __name__ == "__main__":
    print("原始數獨:")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("\n解出的數獨:")
        print_board(sudoku_board)
    else:
        print("\n無解")
