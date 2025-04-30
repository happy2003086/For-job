import random

def is_valid(board, row, col, num):
    # 檢查行是否有相同數字
    for i in range(9):
        if board[row][i] == num:
            return False
    # 檢查列是否有相同數字
    for i in range(9):
        if board[i][col] == num:
            return False
    # 檢查3x3區域是否有相同數字
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def print_board(board, trial_board, cursor_row, cursor_col):
    # 格式化打印，確保每個格子寬度一致
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:  # 已確認的數字
                print(f" {board[row][col]} ", end=" ")
            elif trial_board[row][col] != 0:  # 試錯模式的數字
                print(f"({trial_board[row][col]})", end=" ")
            else:  # 空格
                if row == cursor_row and col == cursor_col:
                    print(f"[ ]", end=" ")  # 用方框標示當前光標
                else:
                    print(f" . ", end=" ")
            
            if (col + 1) % 3 == 0 and col != 8:  # 每隔3格插入一個分隔線
                print("|", end=" ")
        print()

        if (row + 1) % 3 == 0 and row != 8:  # 每隔3行插入一個分隔線
            print("-------+-------+-------")
    print()

def solve_sudoku(board):
    """回溯法求解數獨"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_sudoku():
    """生成一個完整的、唯一解的數獨棋盤"""
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    return board

def remove_numbers(board, difficulty=0.5):
    """隨機移除數字以設置難度"""
    board_copy = [row[:] for row in board]
    squares_to_remove = int(difficulty * 81)  # 根據難度決定移除的數字數量
    count = 0
    while count < squares_to_remove:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board_copy[row][col] != 0:
            board_copy[row][col] = 0
            count += 1
    return board_copy

def play_sudoku():
    print("Welcome to Sudoku!")
    print("Use '0' to represent empty spaces.")
    print("You can input numbers from 1 to 9.")
    print("Once you fill in a correct number, it cannot be changed.")
    print("Press 'T' to try a number and 'C' to confirm it.")
    print("Use 'WASD' to move the cursor around the board.")

    full_board = generate_full_sudoku()  # 生成一個完整的數獨棋盤
    board = remove_numbers(full_board, difficulty=0.5)  # 隨機移除部分數字來設置難度
    trial_board = [row[:] for row in board]  # 試錯模式的棋盤（鉛筆模式）
    cursor_row, cursor_col = 0, 0  # 初始光標位置

    while True:
        print_board(board, trial_board, cursor_row, cursor_col)
        
        action = input("Press 'T' to try, 'C' to confirm, or 'exit' to quit: ").strip().lower()

        if action == "t":
            try:
                num = int(input("Enter the number (1-9): "))
                if num < 1 or num > 9:
                    print("Number must be between 1 and 9. Please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter valid integers.")
                continue

            if board[cursor_row][cursor_col] != 0:
                print("This spot is already filled! Try a different one.")
                continue

            trial_board[cursor_row][cursor_col] = num
            print(f"Number {num} is tentatively placed at ({cursor_row}, {cursor_col}).")
        
        elif action == "c":
            try:
                num = int(input("Enter the number (1-9): "))
                if num < 1 or num > 9:
                    print("Number must be between 1 and 9. Please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter valid integers.")
                continue
            
            if board[cursor_row][cursor_col] != 0:
                print("This spot is already filled! Try a different one.")
                continue
            
            if is_valid(board, cursor_row, cursor_col, num):
                board[cursor_row][cursor_col] = num
                trial_board[cursor_row][cursor_col] = 0
                print("Correct choice!")
            else:
                print("Invalid number for this position!")
        
        elif action == "exit":
            print("Exiting the game.")
            break

        elif action == "w":
            cursor_row = max(0, cursor_row - 1)
        elif action == "s":
            cursor_row = min(8, cursor_row + 1)
        elif action == "a":
            cursor_col = max(0, cursor_col - 1)
        elif action == "d":
            cursor_col = min(8, cursor_col + 1)
        else:
            print("Invalid action. Please enter 'T', 'C', 'exit', or use 'WASD' to move.")
            continue
        
        # 檢查是否完成
        if all(board[row][col] != 0 for row in range(9) for col in range(9)):
            print("Congratulations! You've solved the Sudoku!")
            print_board(board, trial_board, cursor_row, cursor_col)
            break

if __name__ == "__main__":
    play_sudoku()