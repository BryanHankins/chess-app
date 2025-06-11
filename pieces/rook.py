class Rook:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♖' if self.color == 'w' else '♜'

    def valid_moves(self, board, pos):
        row, col = pos
        moves = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
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
