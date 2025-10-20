const API_TTT = '/api/tictactoe/get_ai_move';

const boardEl = document.getElementById('ttt-board');
const statusEl = document.getElementById('ttt-status');
const modal = document.getElementById('ttt-modal');
const modalMsg = document.getElementById('ttt-modal-msg');
const restartBtn = document.getElementById('ttt-restart');
const restartBtn2 = document.getElementById('ttt-restart-2');

let boardState = [['', '', ''], ['', '', ''], ['', '', '']];
let isPlayerTurn = true;
let gameActive = true;

function renderBoard() {
  boardEl.innerHTML = '';
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 3; c++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.dataset.row = r;
      cell.dataset.col = c;
      const v = boardState[r][c];
      if (v === 'X') { cell.classList.add('x'); cell.textContent = 'X'; }
      if (v === 'O') { cell.classList.add('o'); cell.textContent = 'O'; }
      cell.addEventListener('click', onClickCell);
      boardEl.appendChild(cell);
    }
  }
}

async function onClickCell(e) {
  if (!isPlayerTurn || !gameActive) return;
  const r = +e.currentTarget.dataset.row;
  const c = +e.currentTarget.dataset.col;
  if (boardState[r][c] !== '') return;
  boardState[r][c] = 'X';
  renderBoard();
  isPlayerTurn = false;
  statusEl.textContent = 'AI is thinking...';
  boardEl.classList.add('disabled');
  try {
    const res = await fetch(API_TTT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ board: boardState }) });
    const data = await res.json();
    if (data.ai_move) { const [rr, cc] = data.ai_move; boardState[rr][cc] = 'O'; }
    renderBoard();
    if (data.status !== 'continue') endGame(data.status, data.winning_line);
    else { isPlayerTurn = true; statusEl.textContent = 'Your Turn (X)'; }
  } catch (err) {
    statusEl.textContent = 'Error contacting server'; console.error(err);
  } finally {
    if (gameActive) boardEl.classList.remove('disabled');
  }
}

function endGame(status, winningLine) {
  gameActive = false; boardEl.classList.add('disabled');
  let msg = '';
  if (status === 'ai_wins') { msg = 'AI Wins!'; modalMsg && (modalMsg.style.color = 'var(--player-o-color)'); }
  else if (status === 'player_wins') { msg = 'You Win!'; modalMsg && (modalMsg.style.color = 'var(--player-x-color)'); }
  else { msg = "It's a Draw!"; modalMsg && (modalMsg.style.color = 'var(--text)'); }
  if (winningLine) {
    winningLine.forEach(([rr, cc]) => {
      const cell = boardEl.children[rr * 3 + cc];
      if (cell) cell.classList.add('win');
    });
  }
  if (modalMsg) modalMsg.textContent = msg;
  setTimeout(() => modal.classList.add('visible'), 300);
}

function restart() {
  boardState = [['', '', ''], ['', '', ''], ['', '', '']]; isPlayerTurn = true; gameActive = true; statusEl.textContent = 'Your Turn (X)'; modal.classList.remove('visible'); boardEl.classList.remove('disabled'); renderBoard();
}

restartBtn && restartBtn.addEventListener('click', restart);
restartBtn2 && restartBtn2.addEventListener('click', () => restartBtn.click());

renderBoard();
