# server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import math
import random
import heapq
from typing import List, Optional, Tuple

# Initialize the Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
# Enable CORS to allow our HTML page to send requests to this server
CORS(app)


# -----------------------------
# Tic-Tac-Toe (Minimax)
# -----------------------------

def check_winner(board: List[List[str]]):
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

def is_board_full(board: List[List[str]]):
    """ Checks if the board is full. """
    for row in board:
        for cell in row:
            if cell == '':
                return False
    return True

def minimax(current_board: List[List[str]], is_maximizing: bool) -> int:
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

def find_best_move(board: List[List[str]]):
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

@app.route('/api/tictactoe/get_ai_move', methods=['POST'])
@app.route('/get_ai_move', methods=['POST'])  # backward compatibility
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


# -----------------------------
# Maze: Generation (DFS) and Solve (A*)
# -----------------------------

def generate_maze(rows: int, cols: int) -> List[List[int]]:
    """Generate a perfect maze using randomized DFS.
    Returns a grid with 0 = passage, 1 = wall.
    The grid dimensions will be (2*rows+1) x (2*cols+1) to encode walls.
    """
    grid_rows = 2 * rows + 1
    grid_cols = 2 * cols + 1
    grid = [[1 for _ in range(grid_cols)] for _ in range(grid_rows)]

    def carve(r: int, c: int):
        grid[r][c] = 0
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < grid_rows - 1 and 1 <= nc < grid_cols - 1 and grid[nr][nc] == 1:
                grid[r + dr // 2][c + dc // 2] = 0
                carve(nr, nc)

    # Start carving from (1,1)
    carve(1, 1)

    # Ensure entrance and exit
    grid[1][0] = 0
    grid[grid_rows - 2][grid_cols - 1] = 0
    return grid


def astar(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """A* pathfinding on a 0/1 grid (0=free, 1=wall)."""
    rows, cols = len(grid), len(grid[0])

    def h(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_heap = []
    heapq.heappush(open_heap, (0 + h(start, goal), 0, start))
    came_from = {start: None}
    g_score = {start: 0}
    visited = set()

    while open_heap:
        _, g, current = heapq.heappop(open_heap)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            # Reconstruct path
            path = []
            cur = current
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
            return path

        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                neighbor = (nr, nc)
                tentative_g = g + 1
                if tentative_g < g_score.get(neighbor, math.inf):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + h(neighbor, goal)
                    heapq.heappush(open_heap, (f, tentative_g, neighbor))

    return None


@app.route('/api/maze/generate', methods=['POST'])
def api_maze_generate():
    data = request.get_json(force=True) or {}
    rows = int(data.get('rows', 10))
    cols = int(data.get('cols', 10))
    rows = max(2, min(rows, 50))
    cols = max(2, min(cols, 50))
    grid = generate_maze(rows, cols)
    start = (1, 0)
    goal = (len(grid) - 2, len(grid[0]) - 1)
    return jsonify({'grid': grid, 'start': list(start), 'goal': list(goal)})


@app.route('/api/maze/solve', methods=['POST'])
def api_maze_solve():
    data = request.get_json(force=True)
    grid = data['grid']
    start = tuple(data['start'])
    goal = tuple(data['goal'])
    path = astar(grid, start, goal)
    return jsonify({'path': path})


# -----------------------------
# Sudoku Solver (Backtracking)
# -----------------------------

def is_valid_sudoku(board: List[List[int]], r: int, c: int, val: int) -> bool:
    for i in range(9):
        if board[r][i] == val or board[i][c] == val:
            return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if board[i][j] == val:
                return False
    return True


def solve_sudoku(board: List[List[int]]) -> bool:
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for val in range(1, 10):
                    if is_valid_sudoku(board, r, c, val):
                        board[r][c] = val
                        if solve_sudoku(board):
                            return True
                        board[r][c] = 0
                return False
    return True


@app.route('/api/sudoku/solve', methods=['POST'])
def api_sudoku_solve():
    data = request.get_json(force=True)
    board = data['board']
    if len(board) != 9 or any(len(row) != 9 for row in board):
        return jsonify({'error': 'Invalid board size'}), 400
    # Normalize empty cells
    norm = [[int(x) if str(x).isdigit() else 0 for x in row] for row in board]
    if solve_sudoku(norm):
        return jsonify({'solution': norm})
    return jsonify({'error': 'No solution found'}), 422


# -----------------------------
# N-Queens (Backtracking)
# -----------------------------

def solve_n_queens(n: int) -> Optional[List[Tuple[int, int]]]:
    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c
    positions: List[Tuple[int, int]] = []

    def backtrack(r: int) -> bool:
        if r == n:
            return True
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            positions.append((r, c))
            if backtrack(r + 1):
                return True
            positions.pop()
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
        return False

    return positions if backtrack(0) else None


@app.route('/api/nqueens/solve', methods=['POST'])
def api_nqueens_solve():
    data = request.get_json(force=True)
    n = int(data.get('n', 8))
    n = max(1, min(n, 14))
    solution = solve_n_queens(n)
    return jsonify({'n': n, 'solution': solution})


# -----------------------------
# Treasure Hunt (Q-Learning demo)
# -----------------------------

def treasure_env(size: int = 5):
    size = max(3, min(size, 8))
    grid = [[0 for _ in range(size)] for _ in range(size)]
    # Place fixed obstacles for determinism
    obstacles = {(1, 2), (2, 2), (3, 1)} if size >= 4 else set()
    for r, c in obstacles:
        if r < size and c < size:
            grid[r][c] = -1  # obstacle
    start = (0, 0)
    goal = (size - 1, size - 1)
    grid[goal[0]][goal[1]] = 2  # treasure
    return grid, start, goal


def q_learning_solve(size: int = 5, episodes: int = 800):
    grid, start, goal = treasure_env(size)
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    q = {}  # dict[(r,c)][action_idx] = value
    alpha = 0.5
    gamma = 0.9
    epsilon = 0.2

    def is_valid(r: int, c: int) -> bool:
        return 0 <= r < size and 0 <= c < size and grid[r][c] != -1

    def reward(r: int, c: int) -> int:
        if (r, c) == goal:
            return 100
        if grid[r][c] == -1:
            return -100
        return -1

    for _ in range(episodes):
        state = start
        for _ in range(size * size * 4):
            r, c = state
            q.setdefault(state, [0.0] * 4)
            # epsilon-greedy
            if random.random() < epsilon:
                a_idx = random.randrange(4)
            else:
                a_idx = max(range(4), key=lambda i: q[state][i])
            dr, dc = actions[a_idx]
            nr, nc = r + dr, c + dc
            if not is_valid(nr, nc):
                nr, nc = r, c
            new_state = (nr, nc)
            q.setdefault(new_state, [0.0] * 4)
            rwd = reward(nr, nc)
            td_target = rwd + gamma * max(q[new_state])
            q[state][a_idx] += alpha * (td_target - q[state][a_idx])
            state = new_state
            if state == goal:
                break

    # Extract greedy path
    path = [start]
    state = start
    visited = set([start])
    for _ in range(size * size * 4):
        if state == goal:
            break
        q.setdefault(state, [0.0] * 4)
        a_idx = max(range(4), key=lambda i: q[state][i])
        dr, dc = actions[a_idx]
        nr, nc = state[0] + dr, state[1] + dc
        if not is_valid(nr, nc):
            break
        state = (nr, nc)
        if state in visited:
            break
        visited.add(state)
        path.append(state)

    return grid, start, goal, path


@app.route('/api/treasure/solve', methods=['GET'])
def api_treasure_solve():
    size = int(request.args.get('size', 5))
    grid, start, goal, path = q_learning_solve(size=size)
    return jsonify({'grid': grid, 'start': list(start), 'goal': list(goal), 'path': [list(p) for p in path]})


# -----------------------------
# Chess (python-chess, Minimax with Alpha-Beta)
# -----------------------------

try:
    import chess  # type: ignore
except Exception:  # pragma: no cover
    chess = None


PIECE_VALUES = {
    chess.PAWN if chess else 1: 100,
    chess.KNIGHT if chess else 2: 320,
    chess.BISHOP if chess else 3: 330,
    chess.ROOK if chess else 4: 500,
    chess.QUEEN if chess else 5: 900,
    chess.KING if chess else 6: 20000,
}


def evaluate_board(board) -> int:
    if chess is None:
        return 0
    # Material balance
    score = 0
    for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        score += len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]
    return score if board.turn == chess.WHITE else -score


def alpha_beta(board, depth: int, alpha: int, beta: int, maximizing: bool) -> Tuple[int, Optional['chess.Move']]:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None
    best_move = None
    if maximizing:
        value = -math.inf
        for move in board.legal_moves:
            board.push(move)
            eval_score, _ = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval_score > value:
                value = eval_score
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return int(value), best_move
    else:
        value = math.inf
        for move in board.legal_moves:
            board.push(move)
            eval_score, _ = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval_score < value:
                value = eval_score
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return int(value), best_move


@app.route('/api/chess/move', methods=['POST'])
def api_chess_move():
    if chess is None:
        return jsonify({'error': 'python-chess not installed on server'}), 500
    data = request.get_json(force=True)
    fen = data.get('fen')
    depth = int(data.get('depth', 2))
    if not fen:
        return jsonify({'error': 'fen is required'}), 400
    try:
        board = chess.Board(fen)
    except Exception:
        return jsonify({'error': 'invalid FEN'}), 400
    maximizing = board.turn  # True if white to move
    score, move = alpha_beta(board, max(1, min(depth, 3)), -math.inf, math.inf, maximizing)
    if move is None:
        return jsonify({'best_move': None, 'score': score})
    return jsonify({'best_move': move.uci(), 'score': score})


# -----------------------------
# Health and index route
# -----------------------------

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({'status': 'ok'})


@app.route('/')
def root_index():
    # Serve landing page
    return send_from_directory('.', 'index.html')


# Pretty routes for modular pages
@app.route('/pages/<path:filename>')
def pages(filename: str):
    return send_from_directory('pages', filename)


@app.route('/assets/<path:filename>')
def assets(filename: str):
    return send_from_directory('assets', filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

