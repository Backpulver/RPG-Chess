import pygame
from rpg_chess.Controller import chess_engine
from rpg_chess.Data.constants import *
from rpg_chess.View.draw import *

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
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # mouse handler
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
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

                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True
                                square_selected = () # move made unselect clicks
                                player_clicks = []
                        if not move_made: # fix for clicks if invalid move (we used to click 2 times)
                            player_clicks = [square_selected]

            # key handler
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: # undo a move when z is pressed
                    gs.undo_move()
                    move_made = True
                if event.key == pygame.K_r: # reset the board when r is pressed
                    gs = chess_engine.GameState()
                    valid_moves = gs.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False

            if move_made:
                valid_moves = gs.get_valid_moves()
                move_made = False

        draw_game_state(screen, gs, valid_moves, square_selected)

        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                draw_text(screen, "Black wins by checkmate!")
            else:
                draw_text(screen, "White wins by checkmate!")
        elif gs.stalemate:
            game_over = True
            draw_text(screen, "Draw")

        clock.tick(FPS)
        pygame.display.flip()
        

if __name__ == "__main__":
    main()