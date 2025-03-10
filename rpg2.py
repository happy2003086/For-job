import random

class Character:
    def __init__(self, name, health, attack, weapon=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.weapon = weapon

    def attack_target(self, target):
        damage = random.randint(1, self.attack)
        if self.weapon:
            damage += self.weapon.attack
            print(f"{self.name} attacks {target.name} with {self.weapon.name}, dealing {damage} damage!")
        else:
            print(f"{self.name} attacks {target.name}, dealing {damage} damage!")
        target.health -= damage

class Monster:
    def __init__(self, name, health, attack, dropped_weapon=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.dropped_weapon = dropped_weapon

    def attack_target(self, target):
        damage = random.randint(1, self.attack)
        target.health -= damage
        print(f"{self.name} attacks {target.name}, dealing {damage} damage!")

class Weapon:
    def __init__(self, name, attack):
        self.name = name
        self.attack = attack

# Game start
print("Welcome to the text adventure game!")

# Create character
character_name = input("Please enter your character name: ")
player = Character(character_name, 100, 10)

# Weapon list
weapon_list = [
    Weapon("Rusty Sword", 5),
    Weapon("Common Sword", 10),
    Weapon("Sharp Sword", 15)
]

# Healing potion
healing_potion = {"name": "Healing Potion", "heal_amount": 50, "quantity": 3}

# Game main loop
while player.health > 0:
    # Randomly generate monsters
    monster_name = random.choice(["Goblin", "Slime", "Demon"])
    monster = Monster(monster_name, random.randint(50, 150), random.randint(5, 15))

    print(f"\nYou encountered a {monster.name}!")

    # Battle loop
    while player.health > 0 and monster.health > 0:
        print(f"\nYour health: {player.health}")
        print(f"{monster.name}'s health: {monster.health}")

        # Player action
        print(f"You have {healing_potion['quantity']} {healing_potion['name']}(s).")
        action = input("Do you want to attack, run, or use a healing potion? (attack/run/heal): ")

        if action == "attack":
            player.attack_target(monster)
            if monster.health <= 0:
                print(f"You defeated the {monster.name}!")
                if monster.dropped_weapon:
                    print(f"You got a {monster.dropped_weapon.name}!")
                    player.weapon = monster.dropped_weapon
                    print(f"You equipped the {player.weapon.name}!")
                break
            monster.attack_target(player)
            if player.health <= 0:
                print("You were defeated...")
                break
        elif action == "run":
            print("You chose to run away...")
            break
        elif action == "heal":
            if healing_potion["quantity"] > 0:
                heal_amount = healing_potion["heal_amount"]
                player.health += heal_amount
                if player.health > 100:
                    player.health = 100
                healing_potion["quantity"] -= 1
                print(f"You used a {healing_potion['name']} and recovered {heal_amount} health!")
            else:
                print("You don't have any healing potions left!")
        else:
            print("Invalid action, please choose again.")

    if player.health <= 0:
        break

    # End of battle
    
if player.health > 0:
        print("\nYou won the battle!")

# Game over
print("\nGame over.")