class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        
        self.white_to_move = True
        self.move_log = []
        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves, 
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False

        self.enpassant_possible = () # coordinates where an enpassant capture is possible

    # takes a move and does it, not working for en passant, castling or pawn promotion
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) # keep log so we can undo
        self.white_to_move = not self.white_to_move # swap players
        # update king position
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        # pawn promotion move
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        # enpassant move
        if move.is_enpassant:
            self.board[move.start_row][move.end_col] = "--" # remove the captured pawn from the board

        # update enpassant_possible
        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2: # a pawn has moved 2 squares
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else: # other move is made
            self.enpassant_possible = ()

    # undo last move
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            #update king position if needed
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)
            # undo enpassant
            if move.is_enpassant:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.enpassant_possible = (move.end_row, move.end_col)
            # undo 2 square pawn advance
            if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
                self.enpassant_possible = ()
    
    def is_king_in_check(self):
        if self.white_to_move:
            return self.is_square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.is_square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def is_square_under_attack(self, row, col):
        self.white_to_move = not self.white_to_move # to check we must generate opponents moves
        opponent_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move

        for move in opponent_moves:
            if move.end_row == row and move.end_col == col: # is square under attack 
                return True
        return False

    # All valid moves
    def get_valid_moves(self):
        temp_enpassant_possible = self.enpassant_possible # store info about enpassant in current position

        # all moves + considering king in check for next turn, greedy algorithm explained with numbers
        moves = self.get_all_possible_moves() # 1) generate all possible moves

        # 2) for each move we make the move
        for i in range(len(moves)- 1, -1, -1): # when removing iterate from back to avoid index bugs

            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move # after we make a move switch color so we generate opponent moves

            # 3) generate all opponent moves and check if they attack the opposing king
            if self.is_king_in_check():
                moves.remove(moves[i]) # 4) not valid move so we remove it

            self.white_to_move = not self.white_to_move # we go to other color so when we undo we keep the right player turn
            self.undo_move() # undo the move made in this scope

        if len(moves) == 0: # we cannot move => checkmate or stalemate
            if self.is_king_in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else: # if we undo a losing move
            self.checkmate = False
            self.stalemate = False
            
        self.enpassant_possible = temp_enpassant_possible # after undo reset enpassant to initial state
        return moves

    # All moves, not considering king in check for next turn, returns list of moves
    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]

                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves) # call move function so we dont write if for every piece
        return moves

    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move:

            if self.board[row - 1][col] == "--": # move 1 square forward
                moves.append(Move((row, col), (row - 1, col), self.board))

                if row == 6 and self.board[row - 2][col] == "--": # move 2 squares if possible
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0: # capture to the left
                if self.board[row - 1][col - 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
                elif (row - 1, col - 1) == self.enpassant_possible: # capture enpassant to the left
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, is_enpassant_move=True))
            if col + 1 <= 7: # capture to the right
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.enpassant_possible: # capture enpassant to the right
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, is_enpassant_move=True))

        else: # black to move
            
            if self.board[row + 1][col] == "--": # move 1 square forward
                moves.append(Move((row, col), (row + 1, col), self.board))

                if row == 1 and self.board[row + 2][col] == "--": # move 2 squares if possible
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0: # capture to the left
                if self.board[row + 1][col - 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.enpassant_possible: # capture enpassant to the left
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, is_enpassant_move=True))
            if col + 1 <= 7: # capture to the right
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.enpassant_possible: # capture enpassant to the right
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, is_enpassant_move=True))
        #add pawn promotions later

    def get_rook_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right
        enemy_color = "b" if self.white_to_move else "w"

        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row <= 7 and 0 <= end_col <= 7: #check if is on board
                    end_pos_piece = self.board[end_row][end_col]
                    if end_pos_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_pos_piece[0] == enemy_color: # can capture piece
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else: # we have a friendly piece
                        break
                else: # out of bounds
                    break

    def get_bishop_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # up and left, up and right, down and left, down and right
        enemy_color = "b" if self.white_to_move else "w"

        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row <= 7 and 0 <= end_col <= 7: #check if is on board
                    end_pos_piece = self.board[end_row][end_col]
                    if end_pos_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_pos_piece[0] == enemy_color: # can capture piece
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else: # we have a friendly piece
                        break
                else: # out of bounds
                    break
    
    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_knight_moves(self, row, col, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)) # end me if this doesnt work again
        enemy_color = "b" if self.white_to_move else "w"

        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]

            if 0 <= end_row <= 7 and 0 <= end_col <= 7: #check if is on board
                end_pos_piece = self.board[end_row][end_col]
                if end_pos_piece == "--":
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                elif end_pos_piece[0] == enemy_color: # can capture piece
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_king_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        enemy_color = "b" if self.white_to_move else "w"

        for i in range(len(directions)):
            end_row = row + directions[i][0]
            end_col = col + directions[i][1]

            if 0 <= end_row <= 7 and 0 <= end_col <= 7: #check if is on board
                end_pos_piece = self.board[end_row][end_col]
                if end_pos_piece == "--":
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                elif end_pos_piece[0] == enemy_color: # can capture piece
                    moves.append(Move((row, col), (end_row, end_col), self.board))
        #to do


class Move():
    # key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board, is_enpassant_move=False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == "wP" and self.end_row == 0) or (self.piece_moved == "bP" and self.end_row == 7)
        # enpassant
        self.is_enpassant = is_enpassant_move
        if self.is_enpassant:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        # print(self.move_id)

    # override the = 
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]