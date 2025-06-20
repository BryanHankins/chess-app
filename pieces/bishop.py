class Bishop:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♗' if self.color == 'w' else '♝'

    def valid_moves(self, board, pos, last_move=None, has_moved=None):
        row, col = pos
        moves = []
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves
