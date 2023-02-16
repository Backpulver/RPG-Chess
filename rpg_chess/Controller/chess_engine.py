class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bP", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.white_to_move = True
        self.move_log = []
        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves, 
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

    # takes a move and does it, not working for en passant, castling or pawn promotion
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) # keep log so we can undo
        self.white_to_move = not self.white_to_move # swap players

    # undo last move
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
    
    # All valid moves
    def get_valid_moves(self):
        return self.get_all_possible_moves() # for now we wont worry about king being in danger of capture in the next move

    # All moves, but the king can be in check the next turn
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
            if col + 1 <= 7: # capture to the right
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else: # black to move
            
            if self.board[row + 1][col] == "--": # move 1 square forward
                moves.append(Move((row, col), (row + 1, col), self.board))

                if row == 1 and self.board[row + 2][col] == "--": # move 2 squares if possible
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0: # capture to the left
                if self.board[row + 1][col - 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7: # capture to the right
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
        #add pawn promotions later

    def get_rook_moves(self, row, col, moves):
        pass

    def get_knight_moves(self, row, col, moves):
        pass

    def get_bishop_moves(self, row, col, moves):
        pass

    def get_queen_moves(self, row, col, moves):
        pass

    def get_king_moves(self, row, col, moves):
        pass


class Move():
    # key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        print(self.move_id)

    # override the = 
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]