import random
import sys
import time

# Define the possible characters for the code
characters = ['0', '1', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.', '-', '+', '#']

# Function to generate random green code text
def generate_green_code():
    while True:
        # Randomly select the length of the line (from 20 to 80 characters)
        line_length = random.randint(20, 80)
        
        # Create a random line of code
        line = ''.join(random.choice(characters) for _ in range(line_length))
        
        # Print the line in green text
        sys.stdout.write(f"\033[32m{line}\033[0m\n")
        
        # Wait a bit before generating the next line
        time.sleep(0.05)

# Start the code generation
if __name__ == "__main__":
    generate_green_code()
