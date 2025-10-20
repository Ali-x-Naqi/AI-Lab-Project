const API_SOLVE = '/api/nqueens/solve';

const nEl = document.getElementById('nq-n');
const solveBtn = document.getElementById('nq-solve');
const boardEl = document.getElementById('nq-board');

function renderBoard(n, solution){
  boardEl.innerHTML='';
  boardEl.style.setProperty('--n', n);
  boardEl.className = 'board';
  const set = new Set((solution||[]).map(([r,c])=>`${r},${c}`));
  for (let r=0;r<n;r++){
    for (let c=0;c<n;c++){
      const sq = document.createElement('div');
      const dark = (r+c)%2===1; sq.className = 'square ' + (dark?'sq-dark':'sq-light');
      if (set.has(`${r},${c}`)) { sq.innerHTML = '<span class="queen">♛</span>'; }
      boardEl.appendChild(sq);
    }
  }
}

solveBtn.addEventListener('click', async ()=>{
  const n = Math.max(1, Math.min(14, parseInt(nEl.value||'8',10)));
  const res = await fetch(API_SOLVE, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({n})});
  const data = await res.json();
  renderBoard(data.n, data.solution||[]);
});

renderBoard(8, []);
