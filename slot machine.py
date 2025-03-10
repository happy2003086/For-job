import random

# Define the symbols for the slot machine
symbols = ['🍒', '🍋', '🍊', '⭐', '🍉', '🔔', '🍀', '💰']
payouts = {
    '🍒': 2,
    '🍋': 3,
    '🍊': 4,
    '⭐': 5,
    '🍉': 6,
    '🔔': 7,
    '🍀': 8,
    '💰': 10
}

def spin_reels():
    """Spin the reels and return the result."""
    return [random.choice(symbols) for _ in range(3)]

def check_winning_condition(reels):
    """Check if the player has won and calculate the payout."""
    if len(set(reels)) == 1:  # All symbols must be the same to win
        return payouts[reels[0]]  # Return payout for the winning symbol
    return 0  # No win

def main():
    print("Welcome to the Slot Machine!")
    
    balance = 100  # Starting balance
    while True:
        print(f"\nYour balance: ${balance}")
        bet = input("Enter your bet amount (or type 'exit' to quit): ")
        
        if bet.lower() == 'exit':
            break
        
        try:
            bet = int(bet)
            if bet <= 0 or bet > balance:
                print("Invalid bet amount. Please try again.")
                continue
            
            print("Spinning... 🎰")
            reels = spin_reels()
            print(" | ".join(reels))

            payout = check_winning_condition(reels)
            if payout > 0:
                print(f"Congratulations! You win ${bet * payout}!")
                balance += bet * payout
            else:
                print("Sorry, you lose.")
                balance -= bet

            if balance <= 0:
                print("You have run out of money! Game over.")
                break
                
        except ValueError:
            print("Please enter a valid amount.")

    print("Thanks for playing!")

if __name__ == "__main__":
    main()
