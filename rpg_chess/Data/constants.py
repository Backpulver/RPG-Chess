import pygame
#Game Constants
FPS = 20
PIECE_NAMES = ("wP", "wR", "wN", "wB", "wK", "wQ", "bP", "bR", "bN", "bB", "bK", "bQ")

# Board Constants
DIMENSION = 8
WIDTH, HEIGHT = 1150, 700
SQUARE_SIZE = 88 # Magic number !DO NOT CHANGE!, a lot of bugs using border, width and hight // dimention led me to this deredje

# Color Constants
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
BROWN = pygame.Color("#8B4513")
GRAY = pygame.Color("#D3D3D3")