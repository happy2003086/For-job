import random

# 4-in-a-row (Connect Four) game with computer opponent

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 29)

def check_winner(board, player):
    for r in range(6):
        for c in range(7):
            if c + 3 < 7 and all(board[r][c + i] == player for i in range(4)):  # Horizontal
                return True
            if r + 3 < 6 and all(board[r + i][c] == player for i in range(4)):  # Vertical
                return True
            if r + 3 < 6 and c + 3 < 7 and all(board[r + i][c + i] == player for i in range(4)):  # Diagonal (down-right)
                return True
            if r - 3 >= 0 and c + 3 < 7 and all(board[r - i][c + i] == player for i in range(4)):  # Diagonal (up-right)
                return True
    return False

def drop_disc(board, col, player):
    for row in range(5, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return row, col
    return None, None  # Column is full

def is_full(board):
    return all(board[0][col] != " " for col in range(7))

def easy_ai(board):
    """Easy AI: Random move"""
    available_cols = [col for col in range(7) if board[0][col] == " "]
    return random.choice(available_cols)

def medium_ai(board):
    """Medium AI: Random move, but it tries to block immediate threats"""
    # Check for possible winning moves for both AI and player
    for col in range(7):
        if board[0][col] == " ":
            row, _ = drop_disc(board, col, "O")  # Temporarily simulate AI move
            if check_winner(board, "O"):
                board[row][col] = " "
                return col
            board[row][col] = " "
            # Try to block player's winning move
            drop_disc(board, col, "X")  # Temporarily simulate player's move
            if check_winner(board, "X"):
                board[row][col] = " "
                return col
            board[row][col] = " "
    return easy_ai(board)

def hard_ai(board):
    """Hard AI: Minimax algorithm with alpha-beta pruning"""

    def minimax(board, depth, alpha, beta, maximizing_player):
        if check_winner(board, "O"):
            return 1
        if check_winner(board, "X"):
            return -1
        if is_full(board) or depth == 3:  # Limit recursion depth to 3 for faster thinking
            return 0

        if maximizing_player:
            max_eval = -float("inf")
            for col in range(7):
                if board[0][col] == " ":
                    row, _ = drop_disc(board, col, "O")
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[row][col] = " "  # Restore the board after simulation
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:  # Beta pruning
                        break
            return max_eval
        else:
            min_eval = float("inf")
            for col in range(7):
                if board[0][col] == " ":
                    row, _ = drop_disc(board, col, "X")
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[row][col] = " "  # Restore the board after simulation
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:  # Alpha pruning
                        break
            return min_eval

    best_move = None
    best_value = -float("inf")
    for col in range(7):
        if board[0][col] == " ":
            row, _ = drop_disc(board, col, "O")
            move_value = minimax(board, 0, -float("inf"), float("inf"), False)
            board[row][col] = " "  # Restore the board after simulation
            if move_value > best_value:
                best_value = move_value
                best_move = col
    return best_move

def play_game():
    board = [[" " for _ in range(7)] for _ in range(6)]
    current_player = "X"  # Player starts first
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()

    if difficulty == "easy":
        ai_move = easy_ai
    elif difficulty == "medium":
        ai_move = medium_ai
    elif difficulty == "hard":
        ai_move = hard_ai
    else:
        print("Invalid difficulty, defaulting to easy.")
        ai_move = easy_ai

    while True:
        print_board(board)
        
        if current_player == "X":  # Player's turn
            try:
                col = int(input(f"Your turn, choose a column (0-6): "))
                if col < 0 or col > 6 or board[0][col] != " ":
                    print("Invalid move, try again.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue
        else:  # AI's turn
            print("AI is thinking...")
            col = ai_move(board)

        row, col = drop_disc(board, col, current_player)

        if row is not None:
            if check_winner(board, current_player):
                print_board(board)
                if current_player == "X":
                    print("You win!")
                else:
                    print("AI wins!")
                break
            if is_full(board):
                print_board(board)
                print("It's a tie!")
                break
            current_player = "O" if current_player == "X" else "X"  # Switch player

if __name__ == "__main__":
    play_game()
