class King:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♔' if self.color == 'w' else '♚'

    def valid_moves(self, board, pos, last_move=None, has_moved=None):
        moves = []
        r, c = pos
        deltas = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),          ( 0, 1),
                  ( 1, -1), ( 1, 0), ( 1, 1)]

        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target is None or target.color != self.color:
                    moves.append((nr, nc))

        # Castling
        if has_moved and not has_moved[f'{self.color}_king']:
            row = 0 if self.color == 'w' else 7
            if not has_moved[f'{self.color}_rook_7'] and all(board[row][i] is None for i in range(5, 7)):
                moves.append((row, 6))
            if not has_moved[f'{self.color}_rook_0'] and all(board[row][i] is None for i in range(1, 4)):
                moves.append((row, 2))

        return moves
