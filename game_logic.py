# game_logic.py
import copy
from pieces.king import King

def find_king(board, color):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and isinstance(piece, King) and piece.color == color:
                return (r, c)
    return None

def is_in_check(color, board, last_move, has_moved):
    king_pos = find_king(board, color)
    if not king_pos:
        return False
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece.color != color:
                if king_pos in piece.valid_moves(board, (r, c), last_move, has_moved):
                    return True
    return False

def has_legal_moves(color, board, last_move, has_moved):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece.color == color:
                for move in piece.valid_moves(board, (r, c), last_move, has_moved):
                    test_board = copy.deepcopy(board)
                    test_board[move[0]][move[1]] = test_board[r][c]
                    test_board[r][c] = None
                    if not is_in_check(color, test_board, last_move, has_moved):
                        return True
    return False
