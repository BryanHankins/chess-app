class Pawn:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♙' if self.color == 'w' else '♟'

    def valid_moves(self, board, pos, last_move=None, has_moved=None):
        moves = []
        r, c = pos
        direction = 1 if self.color == 'w' else -1
        start_row = 1 if self.color == 'w' else 6
        enemy_color = 'b' if self.color == 'w' else 'w'

        # Move forward
        if 0 <= r + direction < 8 and board[r + direction][c] is None:
            moves.append((r + direction, c))
            if r == start_row and board[r + 2 * direction][c] is None:
                moves.append((r + 2 * direction, c))

        # Captures
        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target and target.color == enemy_color:
                    moves.append((nr, nc))

        # En passant
        if last_move:
            (fr, fc), (tr, tc) = last_move
            if isinstance(board[tr][tc], Pawn) and abs(tr - fr) == 2 and tr == r and abs(tc - c) == 1:
                moves.append((r + direction, tc))

        return moves