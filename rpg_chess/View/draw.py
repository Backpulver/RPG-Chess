import pygame
from rpg_chess.Data.constants import *

def draw_game_state(screen, gs, valid_moves, square_selected):
    draw_board(screen)  # draw squares
    highlight_squares(screen, gs, valid_moves, square_selected)
    draw_pieces(screen, gs.board)

def draw_board(screen):
    # remainder 0 for white (brown), 1 for black (gray)
    colors = [pygame.Color("brown"), pygame.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(
                col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

IMAGES = {}
def load_images():
    for piece in PIECE_NAMES:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_text(screen, text):
    font = pygame.font.SysFont("Arial", 32, True, False)
    text_obj = font.render(text, 0, pygame.Color(BLACK))
    text_location = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 4.2 - text_obj.get_width() / 4.2, HEIGHT / 2 - text_obj.get_height() / 2)
    screen.blit(text_obj, text_location)

def highlight_squares(screen, gs, valid_moves, square_selected):
    if square_selected != ():
        row, col = square_selected
        if gs.board[row][col][0] == ("w" if gs.white_to_move else "b"):
            # highlight selected square
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(250) # transperancy value 0 for transperant to 255 
            surface.fill(pygame.Color(BLUE))
            screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            #highlight moves from figure in square
            surface.fill(pygame.Color(GREEN))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(surface, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))