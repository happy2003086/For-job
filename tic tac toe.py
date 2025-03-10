import random

def draw_board(board):
    """Draw the Tic-Tac-Toe board."""
    print("Current board:")
    print("-------------")
    for i in range(3):
        print("|", board[i * 3], "|", board[i * 3 + 1], "|", board[i * 3 + 2], "|")
        print("-------------")

def check_win(board, player):
    """Check if the given player has won the game."""
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
        (0, 4, 8), (2, 4, 6)              # Diagonal
    ]
    for a, b, c in win_conditions:
        if board[a] == player and board[b] == player and board[c] == player:
            return True
    return False

def is_board_full(board):
    """Check if the board is full."""
    return ' ' not in board

def get_computer_move(board):
    """Determine the computer's move."""
    # Check corners first
    for corner in [0, 2, 6, 8]:
        if board[corner] == ' ':
            return corner

    # Check center
    if board[4] == ' ':
        return 4

    # Block opponent
    for i in range(3):
        # Check rows
        if board[i * 3] == board[i * 3 + 1] == 'O' and board[i * 3 + 2] == ' ':
            return i * 3 + 2
        # Check columns
        if board[i] == board[i + 3] == 'O' and board[i + 6] == ' ':
            return i + 6
    # Check diagonals
    if board[0] == board[4] == 'O' and board[8] == ' ':
        return 8
    if board[2] == board[4] == 'O' and board[6] == ' ':
        return 6

    # Try to win
    for i in range(3):
        # Check rows
        if board[i * 3] == board[i * 3 + 1] == 'X' and board[i * 3 + 2] == ' ':
            return i * 3 + 2
        # Check columns
        if board[i] == board[i + 3] == 'X' and board[i + 6] == ' ':
            return i + 6
    # Check diagonals
    if board[0] == board[4] == 'X' and board[8] == ' ':
        return 8
    if board[2] == board[4] == 'X' and board[6] == ' ':
        return 6

    # If no moves found, choose randomly
    possible_moves = [i for i, x in enumerate(board) if x == ' ']
    return random.choice(possible_moves)

def main():
    """Main game loop."""
    board = [' ' for _ in range(9)]  # Initialize the board
    current_player = 'X'  # X always starts
    game_over = False

    while not game_over:
        draw_board(board)

        if current_player == 'X':
            move = int(input("Player X, choose your move (1-9): ")) - 1  # Convert 1-9 to 0-8
        else:
            move = get_computer_move(board)
            print(f"Computer O chooses position {move + 1}")  # Display computer move in 1-9

        if board[move] == ' ':
            board[move] = current_player
            if check_win(board, current_player):
                draw_board(board)
                print(f"Player {current_player} wins!")
                game_over = True
            elif is_board_full(board):
                draw_board(board)
                print("It's a tie!")
                game_over = True
            else:
                current_player = 'O' if current_player == 'X' else 'X'
        else:
            print("Invalid move! Try again.")

if __name__ == "__main__":
    main()
