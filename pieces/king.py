class King:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♔' if self.color == 'w' else '♚'

    def valid_moves(self, board, pos, last_move=None, moved_flags=None):
        row, col = pos
        moves = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] is None or board[r][c].color != self.color:
                        moves.append((r, c))

        # Castling
        if not moved_flags:
            return moves

        k_flag = f'{self.color}_king'
        r0_flag = f'{self.color}_rook_0'
        r7_flag = f'{self.color}_rook_7'

        if not moved_flags.get(k_flag, True):
            # Kingside
            if not moved_flags.get(r7_flag, True):
                if board[row][5] is None and board[row][6] is None:
                    moves.append((row, 6))
            # Queenside
            if not moved_flags.get(r0_flag, True):
                if board[row][1] is None and board[row][2] is None and board[row][3] is None:
                    moves.append((row, 2))
        return moves
