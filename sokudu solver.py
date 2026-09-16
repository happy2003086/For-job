import tkinter as tk
from tkinter import messagebox

# ==================== 核心演算法 (你的邏輯) ====================
def is_valid(board, row, col, num):
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

# ==================== UI 介面類別 ====================
class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku AI Solver")
        self.entries = []
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        # 容器背景深色，做出黑線效果
        container = tk.Frame(self.root, bg="#333333", padx=2, pady=2)
        container.pack(pady=20)
        
        for r in range(9):
            row_entries = []
            for c in range(9):
                # 3x3 區塊背景切換，方便對位
                bg_color = "#f0f0f0" if (r // 3 + c // 3) % 2 == 0 else "#ffffff"
                
                # width=2 配合 ipady=8 係手機版嘅黃金比例
                e = tk.Entry(container, width=2, font=('Arial', 16, 'bold'),
                             justify='center', bg=bg_color, fg="black", 
                             borderwidth=1, relief="flat")
                e.grid(row=r, column=c, padx=1, pady=1, ipady=8) 
                row_entries.append(e)
            self.entries.append(row_entries)

    def create_buttons(self):
        # 按鈕區
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)

        # 統一按鈕樣式
        btn_style = {"font": ("Arial", 12, "bold"), "fg": "white", "height": 2}

        solve_btn = tk.Button(btn_frame, text="SOLVE", bg="#2e7d32", 
                              command=self.solve, **btn_style)
        solve_btn.pack(side="left", expand=True, fill="x", padx=2)

        clear_btn = tk.Button(btn_frame, text="CLEAR", bg="#c62828", 
                               command=self.clear, **btn_style)
        clear_btn.pack(side="left", expand=True, fill="x", padx=2)

        test_btn = tk.Button(btn_frame, text="TEST", bg="#1565c0", 
                              command=self.load_test_case, **btn_style)
        test_btn.pack(side="left", expand=True, fill="x", padx=2)

    def get_board(self):
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.entries[r][c].get().strip()
                row.append(int(val) if val.isdigit() else 0)
            board.append(row)
        return board

    def set_board(self, board):
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)
                if board[r][c] != 0:
                    self.entries[r][c].insert(0, str(board[r][c]))

    def solve(self):
        try:
            board = self.get_board()
            if solve_sudoku(board):
                self.set_board(board)
            else:
                messagebox.showerror("Error", "No solution!")
        except Exception:
            messagebox.showerror("Error", "Invalid Input!")

    def clear(self):
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)

    def load_test_case(self):
        test_data = [
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
        self.clear()
        self.set_board(test_data)

# ==================== 啟動程式 ====================
if __name__ == "__main__":
    root = tk.Tk()
    # Pydroid 3 環境下自動調整視窗
    app = SudokuApp(root)
    root.mainloop()