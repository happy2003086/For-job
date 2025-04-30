import random
from itertools import combinations

# Define the deck of cards
RANKS = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']

def create_deck():
    """Create a full deck of cards (without suits)"""
    return RANKS * 4  # 4 cards for each rank

def deal_cards(deck, num_players=2, cards_per_player=13):
    """Deal cards to players"""
    random.shuffle(deck)
    hands = [[] for _ in range(num_players)]
    for _ in range(cards_per_player):
        for i in range(num_players):
            if deck:
                hands[i].append(deck.pop())
    return hands

def is_single(hand):
    """Check if the hand is a single card"""
    return len(hand) == 1

def is_pair(hand):
    """Check if the hand is a pair"""
    return len(hand) == 2 and hand[0] == hand[1]

def is_triplet(hand):
    """Check if the hand is a triplet"""
    return len(hand) == 3 and hand[0] == hand[1] == hand[2]

def is_four_of_a_kind(hand):
    """Check if the hand is four of a kind"""
    return len(hand) == 4 and hand[0] == hand[1] == hand[2] == hand[3]

def is_straight(hand):
    """Check if the hand is a straight (5 consecutive cards)"""
    if len(hand) != 5:
        return False
    
    # Get the rank indices and sort them
    indices = sorted([RANKS.index(card) for card in hand])
    
    # Check if the cards are consecutive
    for i in range(1, 5):
        if indices[i] != indices[i-1] + 1:
            return False
    return True

def compare_plays(play1, play2):
    """Compare two plays"""
    if not play1 or not play2:
        return False
    
    # Compare the hand sizes
    if len(play1) != len(play2):
        return False
    
    # Compare the highest card
    max1 = max(play1, key=lambda x: RANKS.index(x))
    max2 = max(play2, key=lambda x: RANKS.index(x))
    return RANKS.index(max1) > RANKS.index(max2)

def validate_play(hand, selected_cards):
    """Validate if the player's selected cards are valid"""
    if not selected_cards:
        return False
    
    # Check if the selected cards are all in the hand
    temp_hand = hand.copy()
    for card in selected_cards:
        if card in temp_hand:
            temp_hand.remove(card)
        else:
            return False
    
    if len(selected_cards) == 1:
        return is_single(selected_cards)
    elif len(selected_cards) == 2:
        return is_pair(selected_cards)
    elif len(selected_cards) == 3:
        return is_triplet(selected_cards)
    elif len(selected_cards) == 4:
        return is_four_of_a_kind(selected_cards)
    elif len(selected_cards) == 5:
        return is_straight(selected_cards)
    return False

def computer_play(hand, last_play=None):
    """Improved computer play logic, follows the rules"""
    possible_plays = []
    
    # Generate all valid plays
    for n in range(1, 6):
        if n > len(hand):
            continue
        
        for combo in combinations(hand, n):
            combo = list(combo)
            valid = False
            
            if n == 1:
                valid = is_single(combo)
            elif n == 2:
                valid = is_pair(combo)
            elif n == 3:
                valid = is_triplet(combo)
            elif n == 4:
                valid = is_four_of_a_kind(combo)
            elif n == 5:
                valid = is_straight(combo)
            
            if valid:
                # If no last play, or can beat the last play
                if not last_play or (len(combo) == len(last_play) and compare_plays(combo, last_play)):
                    possible_plays.append(combo)
    
    if not possible_plays:
        return []  # No valid moves
    
    # Prioritize plays that reduce the most cards
    possible_plays.sort(key=lambda x: -len(x))
    
    # Among the same size plays, choose the one with the highest card
    possible_plays.sort(key=lambda x: (-len(x), -max(RANKS.index(c) for c in x)))
    
    return possible_plays[0]

def print_hand(hand):
    """Print the hand"""
    print(" ".join(sorted(hand, key=lambda x: RANKS.index(x))))

def print_game_state(player_hand, computer_hand, player_name="Player", computer_name="Computer"):
    """Print the game state"""
    print(f"\n{player_name}'s hand ({len(player_hand)} cards): ", end="")
    print_hand(player_hand)
    print(f"{computer_name}'s hand ({len(computer_hand)} cards): ", end="")
    print_hand(computer_hand)

def get_player_move(hand, last_play=None):
    """Get the player's move, ensuring they follow the rule of playing a higher card"""
    while True:
        print("\nYour hand: ", end="")
        print_hand(sorted(hand, key=lambda x: RANKS.index(x)))
        choice = input("Select cards to play (space-separated, e.g. '3 3'), or type 'pass' to skip: ")
        
        if choice.lower() == 'pass':
            return []
        
        selected = choice.split()
        
        # Validate the selected cards
        if not validate_play(hand, selected):
            print("Invalid input or the selected cards don't follow the rules, please try again!")
            continue
        
        # If there's a previous play, check if the player is playing a higher card
        if last_play:
            # Check if the hand is the same type
            if len(selected) != len(last_play):
                print("You must play the same type of hand as the last play, please try again!")
                continue
            
            # Check if the cards are higher than the last play
            if not compare_plays(selected, last_play):
                print("Your play is not higher than the last play, please try again!")
                continue
        
        return selected

def play_game():
    """Main game flow"""
    print("Welcome to the Poker Game!")
    print("Game rules: Each player has 13 cards. You can play a single card, pair, triplet, four of a kind, or a straight")
    print("You must play the same type of hand as the last play, and it must be higher. Or you can skip your turn.")
    print("If the opponent passes, you don't need to follow the type of hand, and can play any valid hand.")
    
    # Create and deal cards
    deck = create_deck()
    player_hand, computer_hand = deal_cards(deck)
    
    # Sort the hands for easier viewing
    player_hand.sort(key=lambda x: RANKS.index(x))
    computer_hand.sort(key=lambda x: RANKS.index(x))
    
    current_player = random.randint(0, 1)  # Randomly decide who starts first
    last_play = None
    consecutive_passes = 0  # Track consecutive passes
    
    while player_hand and computer_hand:
        print_game_state(player_hand, computer_hand)
        
        if current_player == 0:
            # Player's turn
            print("\n=== Your Turn ===")
            selected = get_player_move(player_hand, last_play)
            
            if selected:
                # Remove the played cards from the hand
                for card in selected:
                    player_hand.remove(card)
                last_play = selected
                print(f"\nYou played: {' '.join(selected)}")
                consecutive_passes = 0
            else:
                print("\nYou chose to pass")
                consecutive_passes += 1
        else:
            # Computer's turn
            print("\n=== Computer's Turn ===")
            selected = computer_play(computer_hand, last_play)
            
            if selected:
                # Remove the played cards from the hand
                for card in selected:
                    computer_hand.remove(card)
                last_play = selected
                print(f"Computer played: {' '.join(selected)}")
                consecutive_passes = 0
            else:
                print("Computer chose to pass")
                consecutive_passes += 1
        
        # If both players consecutively pass, clear the last play
        if consecutive_passes >= 2:
            last_play = None
            consecutive_passes = 0
            print("\nBoth players passed, restarting the play!")
        
        # Switch players
        current_player = 1 - current_player
        
        # If the opponent passes, allow the player to play any valid hand
        if last_play is None or consecutive_passes > 0:
            last_play = None  # Allow any valid play
        
        # Check if the game is over
        if not player_hand:
            print("\nCongratulations! You have played all your cards, you win!")
            break
        if not computer_hand:
            print("\nThe computer has played all its cards, you lose!")
            break

if __name__ == "__main__":
    play_game()
