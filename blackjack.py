import os
import random

# Initialize a standard deck of cards
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4

def clear():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def deal(deck):
    """Deal two cards from the deck."""
    hand = []
    for _ in range(2):
        card = deck.pop(random.randint(0, len(deck) - 1))  # Randomly pop a card
        hand.append(convert_card(card))  # Convert number cards to face cards
    return hand

def convert_card(card):
    """Convert card numbers to face card representations."""
    if card == 11:
        return "J"
    elif card == 12:
        return "Q"
    elif card == 13:
        return "K"
    elif card == 14:
        return "A"
    return card

def total(hand):
    """Calculate the total value of the hand, adjusting Aces as needed."""
    total = 0
    aces = 0  # Count the number of Aces in the hand

    for card in hand:
        if card in ("J", "Q", "K"):
            total += 10
        elif card == "A":
            total += 11  # Initially count Aces as 11
            aces += 1
        else:
            total += card

    # Adjust for Aces if total exceeds 21
    while total > 21 and aces:
        total -= 10  # Count an Ace as 1 instead of 11
        aces -= 1

    return total

def hit(hand):
    """Draw a card and add it to the hand."""
    card = deck.pop(random.randint(0, len(deck) - 1))
    hand.append(convert_card(card))

def print_results(dealer_hand, player_hand):
    """Display the results of the game."""
    clear()
    print("The dealer has:", dealer_hand, "for a total of", total(dealer_hand))
    print("You have:", player_hand, "for a total of", total(player_hand))

def play_again():
    """Prompt the user to play again."""
    again = input("Do you want to play again? (Y/N): ").lower()
    if again == "y":
        main()
    else:
        print("Bye!")
        exit()

def score(dealer_hand, player_hand):
    """Determine and print the game results."""
    print_results(dealer_hand, player_hand)
    player_total = total(player_hand)
    dealer_total = total(dealer_hand)

    if player_total > 21:
        print("Sorry. You busted. You lose!\n")
    elif dealer_total > 21:
        print("Dealer busts. You win!\n")
    elif player_total == dealer_total:
        print("It's a tie!\n")
    elif player_total > dealer_total:
        print("Congratulations. You win!\n")
    else:
        print("Sorry. You lose.\n")

def main():
    """Main game loop."""
    global deck  # Allow access to the global deck variable
    clear()
    print("WELCOME TO BLACKJACK!\n")
    
    # Reset and shuffle the deck at the start of the game
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
    random.shuffle(deck)

    dealer_hand = deal(deck)
    player_hand = deal(deck)

    while True:
        print("The dealer is showing:", dealer_hand[0])
        print("You have:", player_hand, "for a total of", total(player_hand))

        # Check for Blackjack
        if total(player_hand) == 21:
            print("Congratulations! You got a Blackjack!\n")
            play_again()

        choice = input("Do you want to [H]it, [S]tand, or [Q]uit: ").lower()
        clear()

        if choice == "h":
            hit(player_hand)  # Draw a card for the player
            # Check if the player busts
            if total(player_hand) > 21:
                print("Sorry. You busted with a total of", total(player_hand), ". You lose!\n")
                play_again()
        elif choice == "s":
            while total(dealer_hand) < 17:
                hit(dealer_hand)  # Dealer draws cards
            score(dealer_hand, player_hand)
            play_again()
        elif choice == "q":
            print("Bye!")
            exit()

if __name__ == "__main__":
    main()
