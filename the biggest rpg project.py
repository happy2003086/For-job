import random

# Define the Weapon class
class Weapon:
    def __init__(self, name, bonus, description):
        self.name = name
        self.bonus = bonus
        self.description = description

# Define the Character class
class Character:
    def __init__(self, name, weapon=None):
        self.name = name
        self.weapon = weapon
        self.hp = 100  # Starting HP
        self.experience = 0
        self.potions = 3  # Player starts with 3 healing potions

    def is_alive(self):
        return self.hp > 0

    def attack(self):
        if self.weapon:
            return self.weapon.bonus
        return 10  # Default attack damage if no weapon equipped

    def gain_experience(self, amount):
        self.experience += amount
        print(f"{self.name} gained {amount} experience!")

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"{self.name} equipped the {weapon.name}!")

    def use_potion(self):
        if self.potions > 0:
            self.hp += 30  # Heal 30 HP
            self.potions -= 1
            print(f"{self.name} used a potion! HP is now {self.hp}.")
        else:
            print(f"{self.name} has no potions left!")

# Define the Monster class
class Monster:
    def __init__(self, name, hp, attack_bonus):
        self.name = name
        self.hp = hp
        self.attack_bonus = attack_bonus

    def is_alive(self):
        return self.hp > 0

    def attack(self):
        return self.attack_bonus

# Define some weapons
sword = Weapon("Sword", 10, "A basic sword with sharp edges.")
axe = Weapon("Axe", 15, "A heavy axe that deals more damage but is slower.")
gun = Weapon("Gun", 20, "A powerful ranged weapon with high damage but lower defense.")

# Define some monsters
def random_monster_encounter():
    monsters = [
        Monster("Goblin", 30, 5),
        Monster("Dragon", 100, 15),
        Monster("Phoenix", 80, 12)
    ]
    return random.choice(monsters)

# Battle function
def battle(player, monster):
    while player.is_alive() and monster.is_alive():
        print(f"\n{player.name}'s HP: {player.hp} | {monster.name}'s HP: {monster.hp}")
        
        # Player's turn
        action = input("Do you want to (a)ttack or (u)se potion? ").lower()
        
        if action == "a":
            player_attack = player.attack()
            monster.hp -= player_attack
            print(f"{player.name} attacks {monster.name} for {player_attack} damage!")
        elif action == "u":
            player.use_potion()
        else:
            print("Invalid action. Please choose 'a' to attack or 'u' to use a potion.")
            continue

        # Check if monster is defeated
        if not monster.is_alive():
            print(f"{monster.name} has been defeated!")
            player.gain_experience(50)  # Example experience for defeating a monster
            break

        # Monster attacks
        monster_attack = monster.attack()
        player.hp -= monster_attack
        print(f"{monster.name} attacks {player.name} for {monster_attack} damage!")

        # Check if player is defeated
        if not player.is_alive():
            print(f"{player.name} has been defeated!")
            break

# Explore function
def explore(player):
    print("\nExploring the world...")

    # Random encounter with a monster
    monster = random_monster_encounter()

    # Offer the player the option to fight or flee
    while player.is_alive():
        print(f"\nYou have encountered a {monster.name}!")
        choice = input("Do you want to (f)ight or (f)lee? ").lower()
        if choice == "f":
            battle(player, monster)
            if not player.is_alive():
                print(f"{player.name} has been defeated!")
                break
            break  # If the player defeats the monster or survives, break out of the loop
        elif choice == "flee":
            print(f"{player.name} fled the battle!")
            break  # Exit encounter loop when player flees
        else:
            print("Invalid choice. Please choose 'f' to fight or 'flee' to escape.")

# Game logic
def start_game():
    print("Welcome to RPG Adventure!")
    print("1. New Game")
    print("2. Load Game")
    print("3. Continue")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        character_name = input("Enter your character's name: ")
        player = Character(character_name)

        print("\nAvailable weapons:")
        print("Weapon: Sword | Bonus: 10 | Description: A basic sword with sharp edges.")
        print("Weapon: Axe | Bonus: 15 | Description: A heavy axe that deals more damage but is slower.")
        print("Weapon: Gun | Bonus: 20 | Description: A powerful ranged weapon with high damage but lower defense.")
        
        equip_choice = input("Choose a weapon to equip (Sword/Axe/Gun): ").lower()
        if equip_choice == "sword":
            player.equip_weapon(sword)
        elif equip_choice == "axe":
            player.equip_weapon(axe)
        elif equip_choice == "gun":
            player.equip_weapon(gun)
        else:
            print("Invalid choice, equipping Sword by default.")
            player.equip_weapon(sword)

        # Game loop
        while player.is_alive():
            explore(player)

        if not player.is_alive():
            print(f"{player.name} has been defeated. Game over.")
    
    elif choice == "4":
        print("Exiting game.")
        exit()
    else:
        print("Invalid choice, please choose again.")
        start_game()

# Main game loop
if __name__ == "__main__":
    start_game()
