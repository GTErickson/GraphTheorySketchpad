import pygame

# Initialize Pygame
pygame.init()

# Screen settings
LAUNCHER_WIDTH, LAUNCHER_HEIGHT = 400, 300
SKETCHPAD_WIDTH, SKETCHPAD_HEIGHT = 1200, 600
BACKGROUND_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 102, 204)
TEXT_COLOR = (255, 255, 255)
NODE_COLOR = (0, 102, 204)  # Default node color (blue)
EDGE_COLOR = (0, 0, 0)
FONT_COLOR = (0, 0, 0)
NODE_RADIUS = 10

# Font for labels
font = pygame.font.Font(None, 24)

# Color options
COLOR_OPTIONS = {
    "Blue": (0, 102, 204),
    "Orange": (255, 102, 0),
    "Green": (0, 204, 0),
    "Purple": (128, 0, 128)
}