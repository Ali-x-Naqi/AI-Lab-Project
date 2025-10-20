export const API = {
  ttt: '/api/tictactoe/get_ai_move',
  mazeGen: '/api/maze/generate',
  mazeSolve: '/api/maze/solve',
  sudokuSolve: '/api/sudoku/solve',
  nqueensSolve: '/api/nqueens/solve',
  treasureSolve: '/api/treasure/solve',
  chessMove: '/api/chess/move',
};

export function headerNav(current) {
  return `
  <header>
    <div class="brand">AI <span class="accent">Games</span> Hub</div>
    <nav>
      <a href="/" class="${current==='home'?'active':''}">Home</a>
      <a href="/pages/tictactoe.html" class="${current==='ttt'?'active':''}">Tic-Tac-Toe</a>
      <a href="/pages/maze.html" class="${current==='maze'?'active':''}">Maze</a>
      <a href="/pages/sudoku.html" class="${current==='sudoku'?'active':''}">Sudoku</a>
      <a href="/pages/nqueens.html" class="${current==='nqueens'?'active':''}">N-Queens</a>
      <a href="/pages/treasure.html" class="${current==='treasure'?'active':''}">Treasure</a>
      <a href="/pages/chess.html" class="${current==='chess'?'active':''}">Chess</a>
    </nav>
  </header>`;
}
