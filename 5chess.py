import random

class Board:
    def __init__(self):
        self.grid = [['.' for _ in range(5)] for _ in range(5)]
        self.current_player = 1  # 1 for player 1, 2 for computer

    def print_board(self):
        print("   0 1 2 3 4")
        for i, row in enumerate(self.grid):
            print(i, " ".join(row))

    def is_valid_move(self, row, col):
        """Checks if a move is valid."""
        return 0 <= row < 5 and 0 <= col < 5 and self.grid[row][col] == '.'

    def make_move(self, row, col):
        """Places a piece on the board."""
        if self.is_valid_move(row, col):
            self.grid[row][col] = 'X' if self.current_player == 1 else 'O'
            self.current_player = 3 - self.current_player  # Switch players

    def check_win(self):
        """Checks for winning conditions."""
        # Check rows
        for row in self.grid:
            if row == ['X', 'X', 'X', 'X', 'X'] or row == ['O', 'O', 'O', 'O', 'O']:
                return True

        # Check columns
        for col in range(5):
            if all(self.grid[row][col] == 'X' for row in range(5)) or all(self.grid[row][col] == 'O' for row in range(5)):
                return True

        # Check diagonals
        if all(self.grid[i][i] == 'X' for i in range(5)) or all(self.grid[i][i] == 'O' for i in range(5)):
            return True
        if all(self.grid[i][4 - i] == 'X' for i in range(5)) or all(self.grid[i][4 - i] == 'O' for i in range(5)):
            return True

        return False

    def is_full(self):
        """Checks if the board is full."""
        for row in self.grid:
            if '.' in row:
                return False
        return True

    def get_valid_moves(self):
        """Returns a list of valid moves."""
        valid_moves = []
        for row in range(5):
            for col in range(5):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves

def computer_move(board):
    """Simple computer AI: Makes a random move."""
    valid_moves = board.get_valid_moves()
    return random.choice(valid_moves)

def play_game():
    board = Board()
    print("Welcome to 5-in-a-Row (vs Computer)!")
    board.print_board()

    while True:
        if board.current_player == 1:  # Player's turn
            print(f"Your turn:")
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))
                board.make_move(row, col)
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid row and column (0-4).")
                continue
        else:  # Computer's turn
            print("Computer's turn:")
            row, col = computer_move(board)
            print(f"Computer played: row {row}, col {col}")
            board.make_move(row, col)

        board.print_board()

        if board.check_win():
            if board.current_player == 1:
                print("computer win!")
            else:
                print("you wins!")
            break

        if board.is_full():
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()