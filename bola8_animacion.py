# Corrected Code for bola8_animacion.py

# Import necessary libraries
import pygame
import sys

# Initialize Pygame
pygame.init()

# Setup canvas
WIDTH, HEIGHT = 800, 600
canvas = pygame.display.set_mode((WIDTH, HEIGHT))

# Function to draw text
def draw_text(surface, text, position, font_size=36, color=(255, 255, 255), origin='topleft'):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(
        **{origin: position}
    )
    surface.blit(text_surface, rect)

# Function to handle transformations
def apply_transformation(position, origin='center'):
    if origin == 'center':
        return (position[0] - WIDTH // 2, position[1] - HEIGHT // 2)
    return position

# Function to validate size
def validate_size(size):
    if size <= 0:
        raise ValueError("Size must be a positive integer")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear canvas
    canvas.fill((0, 0, 0))

    # Call draw_text with the new implementation
    draw_text(canvas, 'Hello, World!', (10, 10), origin='topleft')

    # Update the display (reduced redundant updates)
    pygame.display.update()