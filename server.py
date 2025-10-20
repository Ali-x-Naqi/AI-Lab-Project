# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import math

# Initialize the Flask app
app = Flask(__name__)
# Enable CORS to allow our HTML page to send requests to this server
CORS(app)

def check_winner(board):
    """
    Checks for a winner on the board.
    Returns: (winner ('X' or 'O'), winning_line_coords) or (None, None)
    """
    lines = [
        # Rows
        [[0, 0], [0, 1], [0, 2]], [[1, 0], [1, 1], [1, 2]], [[2, 0], [2, 1], [2, 2]],
        # Columns
        [[0, 0], [1, 0], [2, 0]], [[0, 1], [1, 1], [2, 1]], [[0, 2], [1, 2], [2, 2]],
        # Diagonals
        [[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]],
    ]
    for line in lines:
        p1, p2, p3 = line
        player = board[p1[0]][p1[1]]
        if player != '' and player == board[p2[0]][p2[1]] == board[p3[0]][p3[1]]:
            return player, line
    return None, None

def is_board_full(board):
    """ Checks if the board is full. """
    for row in board:
        for cell in row:
            if cell == '':
                return False
    return True

def minimax(current_board, is_maximizing):
    """ The core Minimax algorithm. """
    winner, _ = check_winner(current_board)
    if winner == 'O': return 10
    if winner == 'X': return -10
    if is_board_full(current_board): return 0

    if is_maximizing:
        best_score = -math.inf
        for r in range(3):
            for c in range(3):
                if current_board[r][c] == '':
                    current_board[r][c] = 'O'
                    score = minimax(current_board, False)
                    current_board[r][c] = ''
                    best_score = max(score, best_score)
        return best_score
    else: # Minimizing player
        best_score = math.inf
        for r in range(3):
            for c in range(3):
                if current_board[r][c] == '':
                    current_board[r][c] = 'X'
                    score = minimax(current_board, True)
                    current_board[r][c] = ''
                    best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    """ Finds the best move for the AI ('O'). """
    best_val = -math.inf
    best_move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == '':
                board[r][c] = 'O'
                move_val = minimax(board, False) # Look for the best score after we move
                board[r][c] = '' # Undo the move
                if move_val > best_val:
                    best_move = [r, c]
                    best_val = move_val
    return best_move

@app.route('/get_ai_move', methods=['POST'])
def get_ai_move():
    """ API endpoint to get the AI's move and check game status. """
    board = request.get_json()['board']
    
    # First, check if the player's move resulted in a win or draw
    winner, line = check_winner(board)
    if winner:
        return jsonify({'status': 'player_wins', 'winning_line': line})
    if is_board_full(board):
        return jsonify({'status': 'draw'})

    # If the game continues, AI calculates its move
    ai_move = find_best_move(board)
    if ai_move:
        board[ai_move[0]][ai_move[1]] = 'O'

    # Now check if the AI's move resulted in a win or draw
    winner, line = check_winner(board)
    if winner:
        return jsonify({'ai_move': ai_move, 'status': 'ai_wins', 'winning_line': line})
    if is_board_full(board):
        return jsonify({'ai_move': ai_move, 'status': 'draw'})

    # If the game still continues, return the AI move and continue status
    return jsonify({'ai_move': ai_move, 'status': 'continue'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)

