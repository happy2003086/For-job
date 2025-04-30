import random
from typing import List, Tuple, Dict

class Noun:
    def __init__(self, name: str, characteristics: Dict[str, bool]):
        self.name = name
        self.characteristics = characteristics
    
    def matches(self, characteristic: str, answer: str) -> bool:
        """Check if the noun matches the given characteristic and answer."""
        if answer == "maybe":
            return True  # Maybe doesn't filter anything
        expected_value = (answer == "yes")
        return self.characteristics.get(characteristic, False) == expected_value

class TwentyQuestionsGame:
    def __init__(self):
        self.nouns = self.initialize_nouns()
        self.questions = [
            ("Is it an animal?", "is_animal"),
            ("Can you eat it?", "can_eat"),
            ("Is it something you can usually find at home?", "find_at_home"),
            ("Is it a mode of transportation?", "mode_of_transportation"),
            ("Does it have life?", "has_life"),
            ("Is it bigger than a cat?", "bigger_than_cat"),
            ("Does it have fur?", "has_fur"),
            ("Does it move?", "moves"),
            ("Can you play with it?", "play_with"),
            ("Is it a common household item?", "common_household_item")
        ]
        self.possible_nouns = self.nouns.copy()
        self.target_noun = None
    
    @staticmethod
    def initialize_nouns() -> List[Noun]:
        """Initialize the database of nouns with their characteristics."""
        nouns_data = [
            ("apple", {"is_animal": False, "can_eat": True, "find_at_home": True, "mode_of_transportation": False, 
                      "has_life": False, "bigger_than_cat": False, "has_fur": False, "moves": False, 
                      "play_with": False, "common_household_item": True}),
            ("banana", {"is_animal": False, "can_eat": True, "find_at_home": True, "mode_of_transportation": False, 
                       "has_life": False, "bigger_than_cat": False, "has_fur": False, "moves": False, 
                       "play_with": False, "common_household_item": True}),
            ("car", {"is_animal": False, "can_eat": False, "find_at_home": False, "mode_of_transportation": True, 
                    "has_life": False, "bigger_than_cat": True, "has_fur": False, "moves": True, 
                    "play_with": False, "common_household_item": False}),
            ("dog", {"is_animal": True, "can_eat": False, "find_at_home": True, "mode_of_transportation": False, 
                     "has_life": True, "bigger_than_cat": True, "has_fur": True, "moves": True, 
                     "play_with": True, "common_household_item": True}),
            ("elephant", {"is_animal": True, "can_eat": False, "find_at_home": False, "mode_of_transportation": False, 
                         "has_life": True, "bigger_than_cat": True, "has_fur": False, "moves": True, 
                         "play_with": False, "common_household_item": False}),
            ("flower", {"is_animal": False, "can_eat": False, "find_at_home": True, "mode_of_transportation": False, 
                       "has_life": True, "bigger_than_cat": False, "has_fur": False, "moves": False, 
                       "play_with": False, "common_household_item": True}),
            ("guitar", {"is_animal": False, "can_eat": False, "find_at_home": True, "mode_of_transportation": False, 
                       "has_life": False, "bigger_than_cat": True, "has_fur": False, "moves": False, 
                       "play_with": True, "common_household_item": True}),
            ("house", {"is_animal": False, "can_eat": False, "find_at_home": True, "mode_of_transportation": False, 
                      "has_life": False, "bigger_than_cat": True, "has_fur": False, "moves": False, 
                      "play_with": False, "common_household_item": True}),
            ("island", {"is_animal": False, "can_eat": False, "find_at_home": False, "mode_of_transportation": False, 
                        "has_life": False, "bigger_than_cat": True, "has_fur": False, "moves": False, 
                        "play_with": False, "common_household_item": False}),
            ("jacket", {"is_animal": False, "can_eat": False, "find_at_home": True, "mode_of_transportation": False, 
                       "has_life": False, "bigger_than_cat": False, "has_fur": True, "moves": False, 
                       "play_with": False, "common_household_item": True}),
        ]
        return [Noun(name, chars) for name, chars in nouns_data]
    
    def select_target(self):
        """Let the user select a target noun (or think of one)."""
        print("\nThink of any noun (it doesn't have to be from this list).")
        print("Here are some examples to help you think:")
        
        sample = random.sample([n.name for n in self.nouns], min(10, len(self.nouns)))
        for i, noun in enumerate(sample):
            print(f"{i + 1}. {noun}")
        
        input("\nPress Enter when you've thought of your noun...")
        self.possible_nouns = self.nouns.copy()
    
    def get_best_question(self) -> Tuple[str, str]:
        """Select the question that best divides the remaining possibilities."""
        if not self.possible_nouns or len(self.possible_nouns) == 1:
            return None, None
        
        best_question = None
        best_char = None
        best_score = float('inf')
        
        for question, char in self.questions:
            yes_count = sum(1 for noun in self.possible_nouns if noun.characteristics.get(char, False))
            no_count = len(self.possible_nouns) - yes_count
            score = abs(yes_count - no_count)  # We want the question that most evenly splits the possibilities
            
            if score < best_score:
                best_score = score
                best_question = question
                best_char = char
        
        return best_question, best_char
    
    def play_round(self):
        """Play one round of 20 Questions."""
        for i in range(20):
            question, char = self.get_best_question()
            
            if not question or len(self.possible_nouns) == 1:
                break
            
            print(f"\nQuestion {i + 1}: {question}")
            while True:
                ans = input("Answer (yes/no/maybe): ").strip().lower()
                if ans in ("yes", "no", "maybe"):
                    break
                print("Please answer with 'yes', 'no', or 'maybe'")
            
            # Filter possible nouns based on answer
            self.possible_nouns = [n for n in self.possible_nouns if n.matches(char, ans)]
            
            # Try to guess if we've narrowed it down enough
            if len(self.possible_nouns) <= 3 or (i + 1) % 5 == 0:
                if self.make_guess():
                    return
        
        # Final guess if we haven't guessed yet
        if len(self.possible_nouns) > 0:
            self.make_guess()
        else:
            print("\nI'm stumped! I couldn't figure out what you were thinking of.")
    
    def make_guess(self) -> bool:
        """Make a guess and return whether it was correct."""
        if not self.possible_nouns:
            return False
            
        guess = random.choice(self.possible_nouns)
        print(f"\nI guess... is it '{guess.name}'?")
        
        while True:
            response = input("Was I correct? (yes/no): ").strip().lower()
            if response in ("yes", "no"):
                break
            print("Please answer with 'yes' or 'no'")
        
        if response == "yes":
            print("\nHooray! I guessed it correctly!")
            return True
        else:
            print("Okay, I'll try again with more questions...")
            self.possible_nouns.remove(guess)
            return False
    
    def play(self):
        """Main game loop."""
        print("Welcome to 20 Questions!")
        print("Think of any noun, and I'll try to guess it by asking up to 20 questions.")
        
        while True:
            self.select_target()
            self.play_round()
            
            while True:
                play_again = input("\nWould you like to play again? (yes/no): ").strip().lower()
                if play_again in ("yes", "no"):
                    break
                print("Please answer with 'yes' or 'no'")
            
            if play_again == "no":
                print("\nThanks for playing 20 Questions! Goodbye!")
                break

# Start the game
if __name__ == "__main__":
    game = TwentyQuestionsGame()
    game.play()