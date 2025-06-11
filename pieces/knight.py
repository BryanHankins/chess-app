class Knight:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♘' if self.color == 'w' else '♞'

    def valid_moves(self, board, pos):
        row, col = pos
        moves = []
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    moves.append((r, c))
        return moves
