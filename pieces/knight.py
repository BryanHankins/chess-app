class Knight:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♘' if self.color == 'w' else '♞'

    def valid_moves(self, board, pos, last_move=None, has_moved=None):
        moves = []
        r, c = pos
        deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target is None or target.color != self.color:
                    moves.append((nr, nc))

        return moves
