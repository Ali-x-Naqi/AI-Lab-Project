const API_GEN = '/api/maze/generate';
const API_SOLVE = '/api/maze/solve';

const gridWrap = document.getElementById('maze-grid');
const genBtn = document.getElementById('maze-generate');
const solveBtn = document.getElementById('maze-solve');
const rowsEl = document.getElementById('maze-rows');
const colsEl = document.getElementById('maze-cols');

let grid = null, start = null, goal = null;

function renderGrid(){
  if (!grid) return;
  const r = grid.length, c = grid[0].length;
  gridWrap.style.gridTemplateColumns = `repeat(${c}, 20px)`;
  gridWrap.innerHTML = '';
  for (let i=0;i<r;i++){
    for (let j=0;j<c;j++){
      const div = document.createElement('div');
      div.className = 'maze-cell ' + (grid[i][j] === 1 ? 'maze-wall' : 'maze-free');
      if (start && i===start[0] && j===start[1]) div.classList.add('maze-start');
      if (goal && i===goal[0] && j===goal[1]) div.classList.add('maze-goal');
      gridWrap.appendChild(div);
    }
  }
}

genBtn.addEventListener('click', async ()=>{
  const rows = +rowsEl.value || 10; const cols = +colsEl.value || 10;
  const res = await fetch(API_GEN, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({rows, cols})});
  const data = await res.json();
  grid = data.grid; start = data.start; goal = data.goal; renderGrid();
});

solveBtn.addEventListener('click', async ()=>{
  if (!grid) return;
  const res = await fetch(API_SOLVE, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({grid, start, goal})});
  const data = await res.json();
  const path = data.path || [];
  const r = grid.length, c = grid[0].length;
  for (let k=0;k<path.length;k++){
    const [i,j] = path[k];
    const idx = i * c + j;
    const cell = gridWrap.children[idx];
    if (cell) cell.classList.add('maze-path');
  }
});
