const API_SOLVE = '/api/sudoku/solve';

const gridEl = document.getElementById('sudoku-grid');
const solveBtn = document.getElementById('sudoku-solve');
const clearBtn = document.getElementById('sudoku-clear');

// Build 9x9 inputs
for (let r=0;r<9;r++){
  for (let c=0;c<9;c++){
    const inp = document.createElement('input');
    inp.className = 'sudoku-cell'; inp.type='number'; inp.min='1'; inp.max='9';
    inp.placeholder='';
    if (r%3===0 && c===0) {
      const sep = document.createElement('div'); sep.className='sudoku-subgrid'; sep.style.gridColumn=`1 / span 9`; sep.style.height='2px'; sep.style.margin='6px 0'; if (r>0) gridEl.appendChild(sep);
    }
    gridEl.appendChild(inp);
    if ((c+1)%3===0 && c!==8) { const spacer = document.createElement('div'); spacer.style.width='6px'; spacer.style.height='0'; gridEl.appendChild(spacer); }
  }
}

function readBoard(){
  const cells = Array.from(gridEl.querySelectorAll('input.sudoku-cell'));
  const board = [];
  for (let r=0;r<9;r++){
    const row = [];
    for (let c=0;c<9;c++){
      const v = cells[r*9 + c].value.trim();
      row.push(v ? parseInt(v,10) : 0);
    }
    board.push(row);
  }
  return board;
}

function writeBoard(board){
  const cells = Array.from(gridEl.querySelectorAll('input.sudoku-cell'));
  for (let r=0;r<9;r++){
    for (let c=0;c<9;c++){
      cells[r*9 + c].value = board[r][c] ? String(board[r][c]) : '';
    }
  }
}

solveBtn.addEventListener('click', async ()=>{
  const board = readBoard();
  const res = await fetch(API_SOLVE, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({board})});
  if (res.ok){ const data = await res.json(); writeBoard(data.solution); }
  else { alert('No solution or invalid board'); }
});

clearBtn.addEventListener('click', ()=>{ writeBoard(Array.from({length:9},()=>Array(9).fill(0))); });
