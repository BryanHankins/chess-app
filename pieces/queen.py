from pieces.rook import Rook
from pieces.bishop import Bishop

class Queen:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♕' if self.color == 'w' else '♛'

    def valid_moves(self, board, pos, last_move=None, has_moved=None):
        rook = Rook(self.color)
        bishop = Bishop(self.color)
        rook_moves = rook.valid_moves(board, pos, last_move, has_moved)
        bishop_moves = bishop.valid_moves(board, pos, last_move, has_moved)
        return rook_moves + bishop_moves
