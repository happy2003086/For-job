import random

class Zombie:
    def __init__(self, hp):
        self.hp = hp

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        print(f"The zombie took {damage} damage, remaining HP: {self.hp}")

class Player:
    def __init__(self):
        self.health = 100
        self.tools = {
            "Knife": 10,
            "Gun": 25,
            "Axe": 15,
            "Baseball Bat": 5
        }

    def choose_tool(self):
        print("\nAvailable tools:")
        for tool in self.tools:
            print(f"- {tool} (Damage: {self.tools[tool]})")
        choice = input("Please choose your tool: ")
        return choice if choice in self.tools else None

    def receive_damage(self, damage):
        self.health -= damage
        print(f"You took {damage} damage, remaining health: {self.health}")
        if self.health <= 0:
            print("You died, game over!")

class Maze:
    def __init__(self, size):
        self.size = size
        self.zombies = self.generate_zombies()
        self.player_position = (0, 0)

    def generate_zombies(self):
        zombies = []
        for _ in range(random.randint(3, 6)):  # Generate 3 to 6 random zombies
            hp = random.randint(20, 50)
            zombies.append(Zombie(hp))
        return zombies

    def move_player(self, direction):
        x, y = self.player_position
        if direction == "up":
            if x > 0:
                self.player_position = (x - 1, y)
        elif direction == "down":
            if x < self.size - 1:
                self.player_position = (x + 1, y)
        elif direction == "left":
            if y > 0:
                self.player_position = (x, y - 1)
        elif direction == "right":
            if y < self.size - 1:
                self.player_position = (x, y + 1)

class Game:
    def __init__(self):
        self.player = Player()
        self.maze = Maze(5)  # 5x5 maze

    def start(self):
        print("Welcome to Zombie Escape!")
        while self.player.health > 0 and self.maze.zombies:
            print(f"\nYour position: {self.maze.player_position}")
            self.show_zombies()
            self.player_turn()
            self.zombie_turn()

        if self.player.health > 0:
            print("You have defeated all the zombies, congratulations!")

    def show_zombies(self):
        print(f"Zombies remaining: {len(self.maze.zombies)}")
        for i, zombie in enumerate(self.maze.zombies):
            print(f"Zombie {i + 1} HP: {zombie.hp}")

    def player_turn(self):
        tool = self.player.choose_tool()
        if tool:
            zombie = self.maze.zombies[0]  # Attack the first zombie
            zombie.take_damage(self.player.tools[tool])
            if not zombie.is_alive():
                print("You successfully killed a zombie!")
                self.maze.zombies.remove(zombie)
        else:
            print("Invalid choice, please choose again.")

        direction = input("Choose a direction to move (up, down, left, right): ")
        self.maze.move_player(direction)

    def zombie_turn(self):
        for zombie in self.maze.zombies:
            if zombie.is_alive():
                damage = random.randint(5, 15)
                self.player.receive_damage(damage)

# Start the game
if __name__ == "__main__":
    game = Game()
    game.start()
