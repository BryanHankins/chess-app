from flask import Flask, render_template, jsonify, request
from pieces.king import King
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn
import copy
from opponent.ai_opponent import AIOpponent


app = Flask(__name__)

board = []
turn = 'w'
last_move = None

has_moved = {
    'w_king': False,
    'b_king': False,
    'w_rook_0': False,
    'w_rook_7': False,
    'b_rook_0': False,
    'b_rook_7': False,
}
ai = AIOpponent('b', difficulty='medium')  # You can change to 'easy' or 'hard'

def create_board():
    b = [[None for _ in range(8)] for _ in range(8)]
    b[0] = [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')]
    b[1] = [Pawn('w') for _ in range(8)]
    b[6] = [Pawn('b') for _ in range(8)]
    b[7] = [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')]
    return b

board = create_board()

def find_king(board, color):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and isinstance(piece, King) and piece.color == color:
                return (r, c)
    return None

def is_in_check(color, board):
    king_pos = find_king(board, color)
    if king_pos is None:
        return False
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece.color != color:
                try:
                    if king_pos in piece.valid_moves(board, (r, c), last_move, has_moved):
                        return True
                except Exception:
                    continue
    return False

def has_legal_moves(color, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece.color == color:
                for move in piece.valid_moves(board, (r, c), last_move, has_moved):
                    test_board = copy.deepcopy(board)
                    test_board[move[0]][move[1]] = test_board[r][c]
                    test_board[r][c] = None
                    if not is_in_check(color, test_board):
                        return True
    return False

def game_status():
    if is_in_check(turn, board):
        if not has_legal_moves(turn, board):
            return 'checkmate'
        return 'check'
    elif not has_legal_moves(turn, board):
        return 'stalemate'
    return 'ok'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/board')
def get_board():
    display_board = [[cell.symbol() if cell else '.' for cell in row] for row in board]
    return jsonify({'board': display_board, 'turn': turn})

@app.route('/reset', methods=['POST'])
def reset():
    global board, turn, last_move, has_moved
    board = create_board()
    turn = 'w'
    last_move = None
    has_moved = {
        'w_king': False,
        'b_king': False,
        'w_rook_0': False,
        'w_rook_7': False,
        'b_rook_0': False,
        'b_rook_7': False,
    }
    return jsonify({'status': 'reset'})

@app.route('/moves', methods=['POST'])
def get_moves():
    data = request.json
    row, col = data['position']
    piece = board[row][col]
    if not piece or piece.color != turn:
        return jsonify({'moves': []})
    return jsonify({'moves': piece.valid_moves(board, (row, col), last_move, has_moved)})

@app.route('/move', methods=['POST'])
def move():
    global turn, last_move
    data = request.json
    from_row, from_col = data['from']
    to_row, to_col = data['to']

    piece = board[from_row][from_col]
    if not piece or piece.color != turn:
        return jsonify({'status': 'invalid', 'reason': 'wrong piece or empty square'})

    valid = piece.valid_moves(board, (from_row, from_col), last_move, has_moved)
    if (to_row, to_col) not in valid:
        return jsonify({'status': 'invalid', 'reason': 'illegal move'})

    # Self-check test
    test_board = copy.deepcopy(board)
    test_board[to_row][to_col] = test_board[from_row][from_col]
    test_board[from_row][from_col] = None
    if is_in_check(turn, test_board):
        return jsonify({'status': 'invalid', 'reason': 'move results in check'})

    # Castling move
    if isinstance(piece, King) and abs(from_col - to_col) == 2:
        if to_col == 6:  # Kingside
            board[to_row][5] = board[to_row][7]
            board[to_row][7] = None
        elif to_col == 2:  # Queenside
            board[to_row][3] = board[to_row][0]
            board[to_row][0] = None

    # En passant
    if isinstance(piece, Pawn) and abs(from_col - to_col) == 1 and board[to_row][to_col] is None:
        ep_row = to_row - (1 if piece.color == 'w' else -1)
        board[ep_row][to_col] = None

    # Apply move
    board[to_row][to_col] = piece
    board[from_row][from_col] = None

    # Promotion
    if isinstance(piece, Pawn):
        if (piece.color == 'w' and to_row == 7) or (piece.color == 'b' and to_row == 0):
            board[to_row][to_col] = Queen(piece.color)

    # Update movement state
    if isinstance(piece, King):
        has_moved[f'{piece.color}_king'] = True
    elif isinstance(piece, Rook):
        if from_col == 0:
            has_moved[f'{piece.color}_rook_0'] = True
        elif from_col == 7:
            has_moved[f'{piece.color}_rook_7'] = True

    last_move = ((from_row, from_col), (to_row, to_col))

    status = game_status()
    if status == 'checkmate':
        return jsonify({'status': 'checkmate', 'winner': 'White' if turn == 'b' else 'Black'})
    elif status == 'stalemate':
        return jsonify({'status': 'stalemate'})
    elif status == 'check':
        turn = 'b' if turn == 'w' else 'w'
        return jsonify({'status': 'check'})

    turn = 'b' if turn == 'w' else 'w'
    return jsonify({'status': 'ok'})
@app.route('/ai-move', methods=['POST'])
def ai_move():
    global board, turn, last_move

    if turn != ai.color:
        return jsonify({'status': 'not_ai_turn'})

    move = ai.choose_move(board, last_move, has_moved)
    if not move:
        return jsonify({'status': 'no_moves'})

    (from_r, from_c), (to_r, to_c) = move
    piece = board[from_r][from_c]

    # Apply special moves
    if isinstance(piece, King) and abs(from_c - to_c) == 2:
        if to_c == 6:
            board[to_r][5] = board[to_r][7]
            board[to_r][7] = None
        elif to_c == 2:
            board[to_r][3] = board[to_r][0]
            board[to_r][0] = None

    if isinstance(piece, Pawn) and abs(from_c - to_c) == 1 and board[to_r][to_c] is None:
        ep_row = to_r - (1 if piece.color == 'w' else -1)
        board[ep_row][to_c] = None

    # Move piece
    board[to_r][to_c] = piece
    board[from_r][from_c] = None

    # Promotion
    if isinstance(piece, Pawn):
        if (piece.color == 'w' and to_r == 7) or (piece.color == 'b' and to_r == 0):
            board[to_r][to_c] = Queen(piece.color)

    # Update movement state
    if isinstance(piece, King):
        has_moved[f'{piece.color}_king'] = True
    elif isinstance(piece, Rook):
        if from_c == 0:
            has_moved[f'{piece.color}_rook_0'] = True
        elif from_c == 7:
            has_moved[f'{piece.color}_rook_7'] = True

    last_move = ((from_r, from_c), (to_r, to_c))

    # Check game status
    status = game_status()
    if status == 'checkmate':
        return jsonify({'status': 'checkmate', 'winner': 'White' if turn == 'b' else 'Black'})
    elif status == 'stalemate':
        return jsonify({'status': 'stalemate'})
    elif status == 'check':
        turn = 'w' if turn == 'b' else 'b'
        return jsonify({'status': 'check'})

    turn = 'w' if turn == 'b' else 'b'
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)