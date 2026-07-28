
const r=document.documentElement;const s=localStorage.getItem('sd-theme');if(s)r.dataset.theme=s;
document.querySelector('[data-theme]')?.addEventListener('click',()=>{r.dataset.theme=r.dataset.theme==='light'?'dark':'light';localStorage.setItem('sd-theme',r.dataset.theme)});
document.querySelectorAll('pre').forEach(p=>{const b=document.createElement('button');b.textContent='Copy';b.style.float='right';b.onclick=async()=>{await navigator.clipboard.writeText(p.innerText.replace(/^Copy/,'').trim());b.textContent='Copied';setTimeout(()=>b.textContent='Copy',1000)};p.prepend(b)});
