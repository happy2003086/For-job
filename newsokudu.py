import random

def generate_full_grid():
    """Generates a fully filled valid Sudoku grid."""
    base = 3
    side = base * base
    # Randomly shuffle numbers 1-9
    nums = random.sample(range(1, base * base + 1), base * base)

    # Create an empty grid
    grid = [[0] * side for _ in range(side)]

    # Fill the diagonal boxes
    for i in range(base):
        fill_box(grid, i * base, i * base, nums)

    # Fill remaining cells
    fill_remaining(grid)
    return grid

def fill_box(grid, row_start, col_start, nums):
    """Fill a 3x3 box with numbers."""
    for i in range(3):
        for j in range(3):
            grid[row_start + i][col_start + j] = nums[i * 3 + j]

def fill_remaining(grid):
    """Fill the remaining cells of the grid."""
    # Simple backtracking algorithm to fill the remaining cells
    # This function is quite complex due to Sudoku's rules
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for num in range(1, 10):
                    if is_safe(grid, i, j, num):
                        grid[i][j] = num
                        if fill_remaining(grid):
                            return True
                        grid[i][j] = 0
                return False
    return True

def is_safe(grid, row, col, num):
    """Check if it's safe to place a number in the grid."""
    # Check if the number is not in the current row
    for x in range(9):
        if grid[row][x] == num:
            return False

    # Check if the number is not in the current column
    for x in range(9):
        if grid[x][col] == num:
            return False

    # Check if the number is not in the current 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False

    return True

def remove_cells(grid, level):
    """Remove cells from the grid to create a puzzle."""
    for _ in range(level):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = 0
    return grid

def display_grid(grid):
    """Display the Sudoku grid."""
    for row in grid:
        print(" | ".join(str(num) if num != 0 else '_' for num in row))
        print("-" * 47)

def main():
    # Generate a full Sudoku grid
    full_grid = generate_full_grid()
    
    # Remove some cells to create a puzzle
    puzzle_grid = remove_cells(full_grid, level=40)  # Adjust the level for difficulty

    print("Welcome to the Sudoku game!")
    print("Fill the Sudoku grid (9x9). Input numbers 1-9.")
    print("Type '0' to leave a cell empty.")

    while True:
        display_grid(puzzle_grid)

        row = int(input("Enter row (1-9) or -1 to exit: ")) - 1
        if row == -2:  # Check for exit condition
            break
        col = int(input("Enter column (1-9): ")) - 1
        
        if 0 <= row < 9 and 0 <= col < 9:
            user_input = int(input(f"Enter number for position ({row+1}, {col+1}): "))
            
            if user_input < 0 or user_input > 9:
                print("Please enter a number between 0 and 9.")
                continue
            
            if puzzle_grid[row][col] != 0:
                print("You cannot overwrite a filled cell. Try another one!")
                continue
            
            puzzle_grid[row][col] = user_input
            
            if user_input == 0:
                continue

            if is_safe(full_grid, row, col, user_input):
                print("✓ Correct!")
            else:
                print("✗ Wrong! Try again.")
        else:
            print("Invalid row or column. Please enter values between 1 and 9.")

    print("\nFinal grid:")
    display_grid(puzzle_grid)
    print("\nThe correct solution was:")
    display_grid(full_grid)

if __name__ == "__main__":
    main()
