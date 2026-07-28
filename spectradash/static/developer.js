const out=document.getElementById('testResult');
async function call(url){out.textContent='Running…';try{const r=await fetch(url,{method:'POST'});const d=await r.json();out.textContent=JSON.stringify(d,null,2);}catch(e){out.textContent='Request failed: '+e;}}
document.querySelectorAll('[data-action]').forEach(b=>b.addEventListener('click',()=>{const m={weather:'/api/developer/test-weather',preview:'/api/refresh',display:'/api/hardware-test',scheduler:'/api/restart-scheduler'};call(m[b.dataset.action]);}));
async function logs(){try{const r=await fetch('/api/developer/logs');const d=await r.json();const el=document.getElementById('liveLogs');el.textContent=(d.lines||[]).join('\n')||'No application log entries yet.';el.scrollTop=el.scrollHeight;}catch(e){}}
document.getElementById('clearLogs')?.addEventListener('click',async()=>{await fetch('/api/developer/clear-logs',{method:'POST'});logs();});
logs();setInterval(logs,3000);
