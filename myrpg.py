import random

class Location:
    def __init__(self, name, description, is_locked=False, event=None, connected_locations=None):
        self.name = name
        self.description = description
        self.is_locked = is_locked
        self.event = event
        self.connected_locations = connected_locations if connected_locations else []

    def describe(self):
        print(f"\nYou have arrived at {self.name}.")
        print(self.description)
        if self.is_locked:
            print("This location is locked. You need something to unlock it.")
        if self.event:
            print(f"Event: {self.event}")
        if self.connected_locations:
            print("Connected locations:", ", ".join([loc.name for loc in self.connected_locations]))


class Monster:
    def __init__(self, name, health, damage, drops):
        self.name = name
        self.health = health
        self.damage = damage
        self.drops = drops

    def attack(self):
        return self.damage

    def take_damage(self, damage):
        self.health -= damage

    def drop_loot(self):
        if self.drops:
            loot = random.choice(self.drops)
            print(f"The monster drops: {loot}")
            return loot
        return None


class Character:
    def __init__(self, name, health, attack, defense, level=1):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.inventory = []

    def take_damage(self, damage):
        net_damage = max(0, damage - self.defense)
        self.health -= net_damage
        print(f"{self.name} takes {net_damage} damage. Current health: {self.health}")

    def attack_enemy(self, enemy):
        damage = random.randint(self.attack - 2, self.attack + 2)
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)
        return damage


class GameMap:
    def __init__(self):
        self.locations = {}
        self.current_location = None
        self.player = None
        self.quests = []
        self.player_health = 10
        self.max_health = 10
        self.player_level = 1
        self.player_inventory = []

    def add_location(self, location):
        self.locations[location.name] = location

    def move_to(self, location_name):
        if location_name in self.locations:
            self.current_location = self.locations[location_name]
            self.current_location.describe()
            if location_name == "Starting Village":
                self.restore_health()
        else:
            print("This location does not exist.")

    def restore_health(self):
        self.player_health = self.max_health
        print(f"Your health has been restored to {self.player_health}.")

    def start_game(self, character):
        self.player = character
        self.move_to("Starting Village")

    def explore(self):
        if self.current_location:
            print(f"You explore {self.current_location.name}.")
            event_chance = random.random()
            if event_chance < 0.3:
                self.encounter_monster()
            elif event_chance < 0.5:
                self.find_treasure()
            elif event_chance < 0.7:
                self.trigger_environment_event()
            elif event_chance < 1.0:
                self.receive_quest()

    def encounter_monster(self):
        monster = self.create_monster()
        print(f"A wild {monster.name} appears! It has {monster.health} health!")
        while self.player.health > 0 and monster.health > 0:
            action = input("What will you do? (Attack / Run): ").strip().lower()
            if action == "attack":
                damage = self.player.attack_enemy(monster)
                print(f"Monster health: {monster.health}")
            elif action == "run":
                print("You ran away!")
                break
            else:
                print("Invalid action.")
            if monster.health > 0:
                self.player.take_damage(monster.attack())
                print(f"The {monster.name} attacks you! Your health: {self.player.health}")
        
        if self.player.health <= 0:
            print("You have been defeated.")
        elif monster.health <= 0:
            print(f"You defeated the {monster.name}!")
            self.player_level += 1
            print(f"You leveled up! Your level is now {self.player_level}.")
            loot = monster.drop_loot()
            if loot:
                self.player.inventory.append(loot)

    def create_monster(self):
        monster_type = random.choice(["Goblin", "Orc", "Dragon", "Vampire", "Troll", "Undead Knight", "Demon", "Ghost", "Giant", "Zombie"])
        drops = ["Gold", "Potion", "Weapon", "Armor", "Key"]
        if monster_type == "Goblin":
            return Monster("Goblin", 5, 2, drops)
        elif monster_type == "Orc":
            return Monster("Orc", 8, 3, drops)
        elif monster_type == "Dragon":
            return Monster("Dragon", 12, 4, drops)
        elif monster_type == "Vampire":
            return Monster("Vampire", 10, 3, drops)
        elif monster_type == "Troll":
            return Monster("Troll", 15, 5, drops)
        elif monster_type == "Undead Knight":
            return Monster("Undead Knight", 20, 6, drops)
        elif monster_type == "Demon":
            return Monster("Demon", 25, 7, drops)
        elif monster_type == "Ghost":
            return Monster("Ghost", 10, 2, drops)
        elif monster_type == "Giant":
            return Monster("Giant", 30, 10, drops)
        elif monster_type == "Zombie":
            return Monster("Zombie", 8, 2, drops)

    def find_treasure(self):
        treasure = random.choice(["Gold", "Potion", "Weapon", "Armor", "Key", "Map"])
        print(f"You found a {treasure}!")
        self.player.inventory.append(treasure)
        print(f"Your inventory: {self.player.inventory}")

    def trigger_environment_event(self):
        event_type = random.choice(["Trap", "Weather Change", "Lost Path", "Hidden Cave", "Falling Rocks"])
        if event_type == "Trap":
            damage = random.randint(3, 6)
            self.player.take_damage(damage)
            print(f"You fell into a trap! You lost {damage} health.")
        elif event_type == "Weather Change":
            print("A storm is brewing! The environment is harsh. Be careful.")
        elif event_type == "Lost Path":
            print("You got lost for a while, wasting valuable time.")
        elif event_type == "Hidden Cave":
            print("You find a hidden cave! It seems to lead deeper into the world.")
            self.add_location(Location("Hidden Cave", "A dark, mysterious cave with treasures inside."))
        elif event_type == "Falling Rocks":
            damage = random.randint(4, 8)
            self.player.take_damage(damage)
            print(f"Rocks fall from the ceiling, you lose {damage} health!")

    def receive_quest(self):
        if "Find the Ancient Artifact" not in self.quests:
            print("A wise man gives you a quest: 'Find the Ancient Artifact in the Dark Forest.'")
            self.quests.append("Find the Ancient Artifact")
        else:
            print("You have already completed this quest.")

# Create the game world map
game_map = GameMap()

# Add locations
town = Location("Starting Village", "This is your hometown, a peaceful village. The villagers are friendly.")
forest = Location("Dark Forest", "A mysterious forest full of monsters and hidden treasures.", event="You encounter a monster!")
mountain = Location("High Mountain", "A tall mountain that leads to the Demon King's castle. It's locked for now.", is_locked=True)
castle = Location("Demon King's Castle", "This is the Demon King's castle, filled with powerful enemies.", event="You discover the Demon King's presence.")
village_market = Location("Village Market", "A market where you can buy and sell items.", event="Buy and sell items.")
cave = Location("Ancient Cave", "An old, mystical cave filled with untold power.", event="You sense a mysterious energy.")

# Connect locations
town.connected_locations = [forest, mountain, cave]
forest.connected_locations = [town, castle]
mountain.connected_locations = [town, castle]
castle.connected_locations = [forest, mountain]
village_market.connected_locations = [town]
cave.connected_locations = [town]

# Add to the map
game_map.add_location(town)
game_map.add_location(forest)
game_map.add_location(mountain)
game_map.add_location(castle)
game_map.add_location(village_market)
game_map.add_location(cave)

# Set the initial character
player = Character(name="Hero", health=15, attack=5, defense=2)
game_map.start_game(player)

# Game loop
while True:
    print("\nWhere would you like to move?")
    print("1. Starting Village")
    print("2. Dark Forest")
    print("3. High Mountain")
    print("4. Demon King's Castle")
    print("5. Village Market")
    print("6. Ancient Cave")
    action = input("Choose a location by number: ")
    
    if action == "1":
        game_map.move_to("Starting Village")
    elif action == "2":
        game_map.move_to("Dark Forest")
    elif action == "3":
        game_map.move_to("High Mountain")
    elif action == "4":
        game_map.move_to("Demon King's Castle")
    elif action == "5":
        game_map.move_to("Village Market")
    elif action == "6":
        game_map.move_to("Ancient Cave")
    
    game_map.explore()

