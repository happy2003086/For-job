import random
import time

def print_slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.03)
    print()

class Character:
    def __init__(self, name, job):
        self.name = name
        self.job = job
        self.health = 100
        self.attack = 10
        self.defense = 5
        self.skills = []
        self.setup_job()

    def setup_job(self):
        if self.job == "Warrior":
            self.health += 20
            self.attack += 5
            self.skills.append("Power Attack")
        elif self.job == "Mage":
            self.attack += 10
            self.skills.append("Fireball")
        elif self.job == "Rogue":
            self.defense += 5
            self.skills.append("Backstab")

    def take_damage(self, damage):
        self.health -= max(0, damage - self.defense)
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def use_skill(self):
        if self.skills:
            print(f"Available skills: {', '.join(self.skills)}")
            skill = input("Choose a skill (type the skill name): ")
            if skill in self.skills:
                return skill
        return None

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

def battle(player, enemy):
    print(f"\nA battle begins! Your opponent is {enemy.name}!")
    while player.is_alive() and enemy.is_alive():
        print(f"\n{player.name} (Health: {player.health}) vs {enemy.name} (Health: {enemy.health})")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Skill")
        choice = input("Choose your action (1/2/3): ")

        if choice == "1":
            damage = random.randint(player.attack - 2, player.attack + 2)
            enemy.take_damage(damage)
            print(f"You dealt {damage} damage to {enemy.name}!")
        elif choice == "2":
            print(f"{player.name} chooses to defend, reducing incoming damage!")
            player.defense += 2
        elif choice == "3":
            skill = player.use_skill()
            if skill == "Power Attack":
                damage = random.randint(player.attack + 5, player.attack + 10)
                enemy.take_damage(damage)
                print(f"You used Power Attack, dealing {damage} damage to {enemy.name}!")
            elif skill == "Fireball":
                damage = random.randint(player.attack + 10, player.attack + 15)
                enemy.take_damage(damage)
                print(f"You used Fireball, dealing {damage} damage to {enemy.name}!")
            elif skill == "Backstab":
                damage = random.randint(player.attack + 3, player.attack + 8)
                enemy.take_damage(damage)
                print(f"You used Backstab, dealing {damage} damage to {enemy.name}!")
            else:
                print("Invalid skill!")
                continue
        else:
            print("Invalid choice!")
            continue

        if enemy.is_alive():
            enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 2)
            player.take_damage(enemy_damage)
            print(f"{enemy.name} dealt {enemy_damage} damage to you!")

    if player.is_alive():
        print(f"\nYou defeated {enemy.name}!")
        return True
    else:
        print(f"\nYou were defeated by {enemy.name}...")
        return False

def start_game():
    print_slow("Welcome to the Fantasy Adventure RPG!")
    name = input("Please enter your name: ")
    print("Please choose your class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    job_choice = input("Choose your class (1/2/3): ")
    jobs = {"1": "Warrior", "2": "Mage", "3": "Rogue"}
    job = jobs.get(job_choice, "Warrior")

    player = Character(name, job)
    print(f"\n{player.name}, you are a {player.job}. Are you ready to begin your adventure?")

    # Main story
    print("\nYou wake up in a mysterious forest, surrounded by unknown dangers and opportunities...")
    time.sleep(1)
    print("Suddenly, a wild wolf jumps out of the bushes!")
    wild_wolf = Enemy("Wild Wolf", 30, 8)
    if not battle(player, wild_wolf):
        print("Game over...")
        return

    print("\nYou defeated the wolf and continue onward...")
    time.sleep(1)
    print("You arrive at a fork in the road, with a dark cave to the left and a shimmering lake to the right.")
    print("1. Left: Dark Cave")
    print("2. Right: Shimmering Lake")
    choice = input("Choose a direction (1/2): ")

    if choice == "1":
        print("\nYou enter the Dark Cave...")
        time.sleep(1)
        print("Deep inside the cave, you encounter a giant spider!")
        giant_spider = Enemy("Giant Spider", 50, 12)
        if not battle(player, giant_spider):
            print("Game over...")
            return
        print("\nYou defeated the giant spider and found treasure in the cave!")
    elif choice == "2":
        print("\nYou arrive at the Shimmering Lake...")
        time.sleep(1)
        print("A water monster emerges from the lake!")
        water_monster = Enemy("Water Monster", 40, 10)
        if not battle(player, water_monster):
            print("Game over...")
            return
        print("\nYou defeated the water monster, and the gems in the lake sparkle brightly!")
    else:
        print("Invalid choice!")
        return

    print("\nCongratulations, you have completed your adventure!")
    print("Victory!")

if __name__ == "__main__":
    start_game()  # Ensure this line is correctly indented
