/* HANINE ARTICLE SIDEBAR AUTO V1
   article-index.json만 갱신하면 모든 게시글의 카테고리/최근 글이 자동 갱신됩니다. */
(function(){
  'use strict';
  const CATEGORY_MAP = [
    ['life','생활정보'],['support','지원금/정책'],['finance','금융정보'],['health','건강정보'],['property','부동산정보'],['auto','자동차정보'],['travel','여행/맛집'],['it','IT/생활꿀팁']
  ];
  const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function categoryMatches(value,label){ return String(value||'')===label;
  }
  function sortRecent(a,b){
    const da=String(a.publishedAt||'');
    const db=String(b.publishedAt||'');
    if(db!==da) return db.localeCompare(da);
    return 0;
  }
  async function render(){
    const layout=document.querySelector('.article-layout');
    if(!layout) return;
    let sidebar=layout.querySelector('.article-sidebar');
    if(!sidebar){
      sidebar=document.createElement('aside');
      sidebar.className='article-sidebar';
      sidebar.setAttribute('aria-label','게시글 사이드바');
      layout.appendChild(sidebar);
    }
    try{
      const res=await fetch('/article-index.json?v='+Date.now(),{cache:'no-store'});
      if(!res.ok) throw new Error('index');
      const posts=await res.json();
      if(!Array.isArray(posts)) throw new Error('format');
      const current=location.pathname;
      const categories=CATEGORY_MAP.map(([key,label])=>{
        const count=posts.filter(p=>categoryMatches(p.category,label)).length;
        return '<a href="/articles.html?category='+key+'"><span>'+esc(label)+'</span><b>'+count+'</b></a>';
      }).join('');
      const recent=posts.slice().sort(sortRecent).filter(p=>p.url!==current).slice(0,5).map(p=>
        '<a class="recent-post-item" href="'+esc(p.url)+'"><span><strong>'+esc(p.title)+'</strong><small>'+esc(p.category||'생활정보')+'</small></span></a>'
      ).join('');
      sidebar.innerHTML=
        '<section class="sidebar-card"><h2>카테고리</h2><div class="sidebar-categories">'+
          '<a href="/articles.html"><span>전체보기</span><b>'+posts.length+'</b></a>'+categories+
        '</div></section>'+
        '<section class="sidebar-card"><h2>최근 글</h2><div class="recent-post-list">'+recent+'</div></section>';
    }catch(e){
      /* 기존 정적 사이드바가 있으면 그대로 둡니다. */
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',render);
  else render();
})();
