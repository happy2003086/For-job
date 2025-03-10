import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Frogger')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game variables
frog_width = 40
frog_height = 40
frog_x = SCREEN_WIDTH // 2 - frog_width // 2
frog_y = SCREEN_HEIGHT - frog_height - 10
frog_speed = 10

car_width = 50
car_height = 40
car_speed = 5
car_frequency = 25  # The higher, the less frequent cars spawn

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Initialize clock
clock = pygame.time.Clock()

# Car class
class Car:
    def __init__(self, y, direction):
        self.x = SCREEN_WIDTH if direction == "left" else -car_width
        self.y = y
        self.direction = direction

    def move(self):
        if self.direction == "left":
            self.x -= car_speed
        else:
            self.x += car_speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, car_width, car_height))

# Function to display text on the screen
def display_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Main game loop
def game_loop():
    global frog_x, frog_y

    # List of cars
    cars = []

    # Game state variables
    score = 0
    game_over = False

    while not game_over:
        screen.fill(GREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # Touch/mouse event to move the frog
            if event.type == pygame.MOUSEMOTION:
                # Get the position where the finger touches or the mouse is
                mouse_x, mouse_y = event.pos

                # Move frog to that position
                frog_x = mouse_x - frog_width // 2
                frog_y = mouse_y - frog_height // 2

            # Optionally, detect touch presses for other events like restart or game over
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # Handle restart logic, if needed
                    pass

        # Spawn cars periodically
        if random.randint(1, car_frequency) == 1:
            car_y = random.randint(0, SCREEN_HEIGHT - car_height)
            direction = random.choice(["left", "right"])
            cars.append(Car(car_y, direction))

        # Move and draw cars
        for car in cars:
            car.move()
            car.draw()

            # Check for collision with the frog
            if frog_x < car.x + car_width and frog_x + frog_width > car.x and frog_y < car.y + car_height and frog_y + frog_height > car.y:
                game_over = True

            # Remove off-screen cars
            if car.x < -car_width or car.x > SCREEN_WIDTH:
                cars.remove(car)

        # Draw frog
        pygame.draw.rect(screen, BLACK, (frog_x, frog_y, frog_width, frog_height))

        # Display score
        display_text(f"Score: {score}", WHITE, 10, 10)

        # Check for frog reaching the top
        if frog_y <= 0:
            score += 1
            frog_y = SCREEN_HEIGHT - frog_height - 10

        # Update the screen
        pygame.display.update()

        # Frame rate
        clock.tick(60)

    # Game Over Screen
    screen.fill(BLACK)
    display_text(f"Game Over! Final Score: {score}", WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    pygame.display.update()
    pygame.time.wait(2000)

# Run the game
game_loop()

# Quit Pygame
pygame.quit()
