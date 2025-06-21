import random
import copy
from game_logic import is_in_check, has_legal_moves

class AIOpponent:
    def __init__(self, color, difficulty='easy'):
        self.color = color
        self.difficulty = difficulty

    def get_all_valid_moves(self, board, last_move, has_moved):
        from pieces.king import King
        from pieces.queen import Queen
        from pieces.rook import Rook
        from pieces.bishop import Bishop
        from pieces.knight import Knight
        from pieces.pawn import Pawn

        moves = []
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece.color == self.color:
                    for move in piece.valid_moves(board, (r, c), last_move, has_moved):
                        moves.append(((r, c), move))
        return moves

    def evaluate_board(self, board):
        value_map = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}
        center_bonus = {(3, 3), (3, 4), (4, 3), (4, 4)}
        score = 0
        for r, row in enumerate(board):
            for c, piece in enumerate(row):
                if piece:
                    symbol = piece.symbol().lower()
                    value = value_map.get(symbol, 0)
                    value += 0.5 if (r, c) in center_bonus else 0
                    score += value if piece.color == self.color else -value

        if is_in_check(self.color, board, None, {}):
            score -= 3

        return score

    def is_checkmate(self, board, last_move, has_moved):
        return is_in_check(self.color, board, last_move, has_moved) and not has_legal_moves(self.color, board, last_move, has_moved)

    def minimax(self, board, depth, alpha, beta, maximizing, last_move, has_moved):
        if depth == 0 or self.is_checkmate(board, last_move, has_moved):
            return self.evaluate_board(board), None

        best_move = None
        moves = self.get_all_valid_moves(board, last_move, has_moved)

        if maximizing:
            max_eval = float('-inf')
            for move in moves:
                temp_board = copy.deepcopy(board)
                fr, to = move
                temp_board[to[0]][to[1]] = temp_board[fr[0]][fr[1]]
                temp_board[fr[0]][fr[1]] = None
                eval, _ = self.minimax(temp_board, depth-1, alpha, beta, False, last_move, has_moved)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                temp_board = copy.deepcopy(board)
                fr, to = move
                temp_board[to[0]][to[1]] = temp_board[fr[0]][fr[1]]
                temp_board[fr[0]][fr[1]] = None
                eval, _ = self.minimax(temp_board, depth-1, alpha, beta, True, last_move, has_moved)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def choose_move(self, board, last_move, has_moved):
        all_moves = self.get_all_valid_moves(board, last_move, has_moved)
        if not all_moves:
            return None

        if self.difficulty == 'easy':
            return random.choice(all_moves)

        elif self.difficulty == 'medium':
            scored = []
            for move in all_moves:
                fr, to = move
                temp_board = copy.deepcopy(board)
                temp_board[to[0]][to[1]] = temp_board[fr[0]][fr[1]]
                temp_board[fr[0]][fr[1]] = None
                score = self.evaluate_board(temp_board)
                scored.append((score, move))
            return max(scored, key=lambda x: x[0])[1]

        elif self.difficulty == 'hard':
            _, best = self.minimax(board, 4, float('-inf'), float('inf'), True, last_move, has_moved)
            return best

        return random.choice(all_moves)
