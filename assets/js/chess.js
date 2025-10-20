const API_MOVE = '/api/chess/move';

const fenEl = document.getElementById('ch-fen');
const depthEl = document.getElementById('ch-depth');
const moveBtn = document.getElementById('ch-move');
const outEl = document.getElementById('ch-output');

moveBtn.addEventListener('click', async ()=>{
  const fen = fenEl.value.trim(); if (!fen) { alert('Enter FEN'); return; }
  outEl.textContent = 'Analyzing...';
  const res = await fetch(API_MOVE, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({fen, depth: parseInt(depthEl.value||'2',10)}) });
  const data = await res.json();
  if (data.error){ outEl.textContent = 'Server error: ' + data.error; }
  else { outEl.textContent = `Best move: ${data.best_move || 'None'} (score ${data.score})`; }
});
