import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sad Anime Face Bounce")

# Colors
WHITE = (255, 255, 255)
SKIN = (255, 204, 153)  # Light peach skin color
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Blue for tears

# Character properties
char_radius = 50  # Head size
char_x = random.randint(char_radius, WIDTH - char_radius)
char_y = random.randint(char_radius, HEIGHT - char_radius)
char_speed_x = 5
char_speed_y = 5

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (mouse_x - char_x) ** 2 + (mouse_y - char_y) ** 2 <= char_radius ** 2:
                char_x = random.randint(char_radius, WIDTH - char_radius)
                char_y = random.randint(char_radius, HEIGHT - char_radius)

    # Move the character
    char_x += char_speed_x
    char_y += char_speed_y

    # Bounce the character
    if char_x <= char_radius or char_x >= WIDTH - char_radius:
        char_speed_x = -char_speed_x
    if char_y <= char_radius or char_y >= HEIGHT - char_radius:
        char_speed_y = -char_speed_y

    # Fill the background
    screen.fill(WHITE)

    # Draw anime-style face (head)
    pygame.draw.circle(screen, SKIN, (char_x, char_y), char_radius)

    # Draw sad eyes (tilted down)
    pygame.draw.ellipse(screen, BLACK, (char_x - 25, char_y - 15, 10, 15))  # Left eye
    pygame.draw.ellipse(screen, BLACK, (char_x + 15, char_y - 15, 10, 15))  # Right eye

  
    # Draw sad mouth (curved down)
    pygame.draw.arc(screen, BLACK, (char_x - 20, char_y + 10, 40, 20), 3.14, 6.28, 3)  # Sad mouth

    # Update the display
    pygame.display.flip()
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()
