import random
import time
import os

def clear_console():
    """Clear the console output."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_sequence(length):
    """Generate a random sequence of numbers."""
    return [random.randint(0, 9) for _ in range(length)]

def display_sequence(sequence):
    """Display the sequence to the player."""
    print("Remember this sequence:")
    for number in sequence:
        print(number, end=' ', flush=True)
        time.sleep(1)  # Pause for 1 second between numbers
    
    time.sleep(1)  # Delay before clearing
    clear_console()

def get_player_input(length):
    """Get the player's input and return it as a list of integers."""
    player_input = input(f"Enter the sequence of {length} numbers (space-separated): ")
    try:
        # Splitting and converting to integers
        input_numbers = list(map(int, player_input.split()))
        
        # Check if the length matches
        if len(input_numbers) != length:
            print(f"Please enter exactly {length} numbers.")
            return get_player_input(length)  # Prompt again
        
        return input_numbers
    except ValueError:
        print("Invalid input! Please enter only numbers.")
        return get_player_input(length)  # Prompt again

def play_game():
    """Main function to run the memory game."""
    level = 1
    while True:
        print(f"\nLevel {level}")
        sequence = generate_sequence(level)
        print(f"Expected Sequence: {sequence}")  # Debugging line
        display_sequence(sequence)

        player_guess = get_player_input(level)
        print(f"Player Guess: {player_guess}")  # Debugging line

        if player_guess == sequence:
            print("Correct! Moving to the next level...")
            level += 1  # Increase the difficulty
        else:
            print("Incorrect! Game over.")
            print(f"The correct sequence was: {sequence}")
            break

if __name__ == "__main__":
    play_game()
