import random

def roll_dice():
    return random.randint(1, 6)

def play_turn(player_name, is_ai=False):
    turn_score = 0
    while True:
        roll = roll_dice()
        print(f"{player_name} rolled a {roll}")

        if roll == 1:
            print(f"{player_name} loses the turn score!")
            return 0  # Lose all turn points
        else:
            turn_score += roll
            print(f"{player_name}'s turn score: {turn_score}")

            if is_ai:
                # Simple AI logic: hold if turn score is 20 or more
                if turn_score >= 20:
                    print(f"{player_name} decides to hold.")
                    return turn_score
                else:
                    print(f"{player_name} chooses to roll again.")
            else:
                choice = input("Do you want to roll again or hold? (r/h): ").strip().lower()
                if choice == 'h':
                    return turn_score  # Return turn score to add to total

def main():
    scores = {'You': 0, 'Computer AI': 0}
    winning_score = 100

    while True:
        for player, is_ai in zip(scores.keys(), [False, True]):
            print(f"\n{player}'s turn:")
            turn_score = play_turn(player, is_ai)
            scores[player] += turn_score
            print(f"{player}'s total score: {scores[player]}")

            if scores[player] >= winning_score:
                print(f"{player} wins with a score of {scores[player]}!")
                return

if __name__ == "__main__":
    main()
