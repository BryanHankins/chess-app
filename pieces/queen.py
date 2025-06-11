class Queen:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♕' if self.color == 'w' else '♛'

    def valid_moves(self, board, pos):
        # Queen = Rook + Bishop
        from pieces.rook import Rook
        from pieces.bishop import Bishop
        return Rook(self.color).valid_moves(board, pos) + Bishop(self.color).valid_moves(board, pos)
