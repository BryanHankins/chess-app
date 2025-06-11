class Pawn:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♙' if self.color == 'w' else '♟'

    def valid_moves(self, board, pos, last_move=None):
        row, col = pos
        direction = 1 if self.color == 'w' else -1
        start_row = 1 if self.color == 'w' else 6
        moves = []

        # Forward move
        next_row = row + direction
        if 0 <= next_row < 8 and board[next_row][col] is None:
            moves.append((next_row, col))

            # Two-step from starting row
            if row == start_row and board[next_row + direction][col] is None:
                moves.append((next_row + direction, col))

        # Diagonal captures and en passant
        for dc in [-1, 1]:
            nr, nc = row + direction, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target and target.color != self.color:
                    moves.append((nr, nc))

                # En passant
                if last_move:
                    (fr, fc), (tr, tc) = last_move
                    if abs(fc - col) == 1 and fr == (6 if self.color == 'b' else 1) and tr == row and tc == col + dc:
                        adjacent = board[row][col + dc]
                        if adjacent and isinstance(adjacent, Pawn) and adjacent.color != self.color:
                            moves.append((nr, nc))

        return moves
