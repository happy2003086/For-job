import pygame
import math

pygame.init()
clock = pygame.time.Clock()  # Fixed: Needed parentheses to create Clock object

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('3D Time Tunnel Effect')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
colors = [(255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255)]  # Tunnel colors

# Parameters
tunnel_radius = 200
num_rings = 30
speed = 0.5  # Reduced speed for better visual effect

# Main game loop
running = True
t = 0
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the tunnel rings
    for i in range(num_rings):
        # Calculate z-position (depth) of the ring
        z = 1 - (i / num_rings)  # z goes from 1 (closest) to 0 (farthest)
        
        # Calculate size and position based on perspective
        size = (tunnel_radius * z) / 2
        x_pos = 400 + math.cos(math.radians(t + i * 5)) * size * 0.5  # Added some rotation
        y_pos = 300 + math.sin(math.radians(t + i * 5)) * size * 0.5
        
        # Calculate radius based on perspective
        radius = size / (z + 0.5)  # Adjust divisor for different tunnel shapes
        
        # Calculate color intensity based on depth
        color_idx = i % len(colors)
        color = tuple(int(c * z) for c in colors[color_idx])  # Darken with distance
        
        pygame.draw.circle(screen, color, (int(x_pos), int(y_pos)), int(radius))

    t += speed

    pygame.display.flip()
    clock.tick(60)  # Fixed: Now properly calling tick() method

pygame.quit()