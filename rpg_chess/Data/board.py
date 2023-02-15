import pygame
from .constants import ROWS, COLS, WHITE, BLACK, SQUARE_SIZE

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None