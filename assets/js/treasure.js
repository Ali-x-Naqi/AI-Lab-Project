const API_SOLVE = '/api/treasure/solve';

const sizeEl = document.getElementById('tr-size');
const runBtn = document.getElementById('tr-run');
const gridEl = document.getElementById('tr-grid');

function render(grid, path, start, goal){
  const r = grid.length, c = grid[0].length;
  gridEl.style.gridTemplateColumns = `repeat(${c}, 20px)`;
  gridEl.innerHTML = '';
  const pathSet = new Set((path||[]).map(([i,j])=>`${i},${j}`));
  for (let i=0;i<r;i++){
    for (let j=0;j<c;j++){
      const cell = document.createElement('div');
      cell.className = 'maze-cell ' + (grid[i][j]===1? 'maze-wall' : 'maze-free');
      if (start && i===start[0] && j===start[1]) cell.classList.add('maze-start');
      if (goal && i===goal[0] && j===goal[1]) cell.classList.add('maze-goal');
      if (pathSet.has(`${i},${j}`)) cell.classList.add('maze-path');
      gridEl.appendChild(cell);
    }
  }
}

runBtn.addEventListener('click', async ()=>{
  const size = parseInt(sizeEl.value||'5',10);
  const res = await fetch(`${API_SOLVE}?size=${encodeURIComponent(size)}`);
  const data = await res.json();
  render(data.grid, data.path, data.start, data.goal);
});
