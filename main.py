import pygame
from rpg_chess.Controller import chess_engine
from rpg_chess.Data.constants import WIDTH, HEIGHT, SQUARE_SIZE, DIMENSION
# from rpg_chess.Data.board import Board

FPS = 20
IMAGES = {}


def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wK", "wQ", "bP", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

# main driver
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Chess")
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = chess_engine.GameState()
    load_images()
    running = True
    square_selected = () #no selected square -> tuple (row, col)
    player_clicks = [] #keep track of player clicks with 2 tuples for ex.  [(6, 4), (4, 4)] -> select and unselect a piece

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() # (x, y) location of mouse
                col = location[0] // SQUARE_SIZE
                row= location[1] // SQUARE_SIZE
                if square_selected == (row, col): #same square clicked twice = illegal move
                    square_selected = () #unselect
                    player_clicks = [] #reset player clicks
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)

                if len(player_clicks) == 2: # we have 2 legal clicks
                    move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_move(move)
                    square_selected = () # move made unselect clicks
                    player_clicks = []

        draw_game_state(screen, gs)
        clock.tick(FPS)
        pygame.display.flip()


def draw_game_state(screen, gs):
    draw_board(screen)  # draw squares
    draw_pieces(screen, gs.board)


def draw_board(screen):
    # remainder 0 for white (brown), 1 for black (gray)
    colors = [pygame.Color("brown"), pygame.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(
                col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                

if __name__ == "__main__":
    main()