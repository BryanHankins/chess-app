# rook.py
class Rook:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return '♖' if self.color == 'w' else '♜'

    def valid_moves(self, board, pos, last_move=None, has_moved=None):
        moves = []
        r, c = pos

        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target is None:
                    moves.append((nr, nc))
                elif target.color != self.color:
                    moves.append((nr, nc))
                    break
                else:
                    break
                nr += dr
                nc += dc

        return moves
