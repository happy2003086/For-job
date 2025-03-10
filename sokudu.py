import numpy as np
import random

# 打印數獨板
def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("---------------------")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=' ')
            print(board[i, j] if board[i, j] != 0 else ".", end=' ')
        print()

# 找到空格
def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                return i, j, True
    return -1, -1, False

# 檢查數字是否有效
def check_validity(board, row, col, num):
    # 檢查行和列
    if num in board[:, col] or num in board[row, :]:
        return False
    # 檢查3x3宮格
    row_start, col_start = (row // 3) * 3, (col // 3) * 3
    if num in board[row_start:row_start+3, col_start:col_start+3]:
        return False
    return True

# 生成未解數獨板
def generate_unsolved_puzzle(board, difficulty):
    count, upper_limit = 0, 0
    if difficulty == "Easy":
        print("生成簡單難度的數獨...\n")
        upper_limit = 35
    elif difficulty == "Medium":
        print("生成中等難度的數獨...\n")
        upper_limit = 41
    else:
        print("生成困難難度的數獨...\n")
        upper_limit = 47

    while count <= upper_limit:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if board[i, j] != 0:
            temp = board[i, j]
            board[i, j] = 0
            board_copy = board.copy()
            if not solve_sudoku(board_copy, temp):
                board[i, j] = temp
                continue
            count += 1

# 解決數獨
def solve_sudoku(board, not_check=-1):
    row, col, is_empty = find_empty_cell(board)
    if not is_empty:
        return True
    for num in np.random.permutation(range(1, 10)):
        if num != not_check and check_validity(board, row, col, num):
            board[row, col] = num
            if solve_sudoku(board, not_check):
                return True
            board[row, col] = 0
    return False

# 玩數獨
def play_sudoku(solved_board, unsolved_board):
    while True:
        print_board(unsolved_board)
        try:
            row = int(input("輸入要填寫的行號 (1-9): ")) - 1
            col = int(input("輸入要填寫的列號 (1-9): ")) - 1
            num = int(input("輸入要填寫的數字 (1-9, 輸入0撤銷): "))
        except ValueError:
            print("輸入無效，請輸入數字！")
            continue

        if row < 0 or row > 8 or col < 0 or col > 8 or num < 0 or num > 9:
            print("輸入超出範圍，請重新輸入！")
            continue

        if num == 0:
            if unsolved_board[row, col] != 0:
                unsolved_board[row, col] = 0
                print("已撤銷該位置的數字！")
            else:
                print("該位置為空，無法撤銷！")
            continue

        if unsolved_board[row, col] != 0:
            print("該位置已填寫，無法修改！")
            continue

        if solved_board[row, col] == num:
            unsolved_board[row, col] = num
            print("填寫正確！")
        else:
            print("填寫錯誤，請重新嘗試！")

        if np.array_equal(solved_board, unsolved_board):
            print("恭喜你，數獨完成！")
            break

# 主程式
def main():
    print("歡迎來到數獨遊戲！")
    while True:
        try:
            ch = int(input("請選擇難度：\n1. 簡單\n2. 中等\n3. 困難\n你的選擇："))
            if ch not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            print("輸入無效，請輸入1、2或3！")

    difficulty = ["Easy", "Medium", "Hard"][ch - 1]
    board = np.zeros((9, 9), dtype="int8")

    if solve_sudoku(board):
        solved_board = board.copy()
        generate_unsolved_puzzle(board, difficulty)
        unsolved_board = board.copy()
        print("\n生成的數獨題目：\n")
        print_board(unsolved_board)
        play_sudoku(solved_board, unsolved_board)
    else:
        print("生成數獨失敗，請重試！")

if __name__ == "__main__":
    main()