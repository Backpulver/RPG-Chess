import pygame
from rpg_chess.Controller import chess_engine
from rpg_chess.Data.constants import *

IMAGES = {}
def load_images():
    for piece in PIECE_NAMES:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))

# main driver
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Chess")
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = chess_engine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False # so we know when to stop checking for next move is a check
    load_images()
    running = True
    square_selected = () #no selected square -> tuple (row, col)
    player_clicks = [] #keep track of player clicks with 2 tuples for ex.  [(6, 4), (4, 4)] -> select and unselect a piece

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # mouse handler
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

                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        square_selected = () # move made unselect clicks
                        player_clicks = []
                    else: # fix for clicks if invalid move (we used to click 2 times)
                        player_clicks = [square_selected]

            # key handler
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: # undo a move when z is pressed
                    gs.undo_move()
                    move_made = True

            if move_made:
                valid_moves = gs.get_valid_moves()
                move_made = False

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