(function(){
  const KEY='hanine_article_views_v1';
  const normalize=p=>p.replace(/\/index\.html$/,'/').replace(/\/+$/,'')||'/';
  let views={};
  try{views=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(e){views={};}
  const current=normalize(location.pathname);
  if(current.startsWith('/articles/')){
    views[current]=(Number(views[current])||0)+1;
    try{localStorage.setItem(KEY,JSON.stringify(views));}catch(e){}
  }
  const boxes=document.querySelectorAll('[data-popular-posts]');
  if(!boxes.length)return;
  fetch('/popular-posts.json?v=1',{cache:'no-store'})
    .then(r=>r.ok?r.json():[])
    .then(items=>{
      if(!Array.isArray(items))return;
      const ranked=items.map((x,i)=>{
        const path=normalize(x.url||'');
        return {...x,_path:path,_score:(Number(views[path])||0)*100000+(Number(x.seed)||0)-i};
      }).filter(x=>x._path!==current).sort((a,b)=>b._score-a._score).slice(0,5);
      boxes.forEach(box=>{
        box.innerHTML=ranked.map((x,i)=>`<a class="popular-post-item" href="${x.url}">
          <span class="popular-rank">${i+1}</span>
          <span class="popular-post-copy"><strong>${esc(x.title||'생활정보')}</strong><small>${esc(x.category||'생활정보')}</small></span>
          <span class="popular-arrow" aria-hidden="true">→</span>
        </a>`).join('');
      });
    }).catch(()=>{});
  function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
})();