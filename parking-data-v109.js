(function(){
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function copyButton(value){return '<button type="button" class="parking-copy" data-copy="'+esc(value)+'">주소 복사</button>'}
function row(k,v){if(!v)return '';return '<div class="parking-data-row"><b>'+esc(k)+'</b><span>'+esc(v)+'</span></div>'}
function render(list){var el=document.getElementById('parking-data-list');if(!el)return; if(!list||!list.length){el.innerHTML='';return}
 el.innerHTML=list.map(function(p){
   var naver='https://map.naver.com/p/search/'+encodeURIComponent(p.name+' '+p.address);
   return '<article class="parking-blog-card"><div class="parking-blog-head"><div><span class="parking-type-badge">'+esc(p.type||'공영주차장')+'</span><h2>'+esc(p.name)+'</h2></div></div>'+
   '<p class="parking-address">📍 '+esc(p.address)+' '+copyButton(p.address)+'</p>'+
   '<div class="parking-data-grid">'+row('주차장 형태',p.type)+row('주차면',p.spaces? p.spaces+'면':'')+row('운영시간',p.hours)+row('요금',p.fee)+row('정기권',p.monthly)+row('전화',p.phone)+'</div>'+
   (p.note?'<p class="parking-note">'+esc(p.note)+'</p>':'')+
   '<p class="parking-map-links"><a class="parking-naver-primary-v110" href="'+naver+'" target="_blank" rel="noopener">네이버지도에서 상세정보·길찾기</a></p></article>'
 }).join('');
 document.querySelectorAll('.parking-copy').forEach(function(b){b.addEventListener('click',function(){var v=b.getAttribute('data-copy')||'';function done(){var old=b.textContent;b.textContent='복사됨';setTimeout(function(){b.textContent=old},1200)}if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(v).then(done)}else{var t=document.createElement('textarea');t.value=v;document.body.appendChild(t);t.select();document.execCommand('copy');t.remove();done()}})})
}
document.addEventListener('DOMContentLoaded',function(){var el=document.getElementById('parking-data-list');if(!el)return;var d=el.getAttribute('data-district');fetch('/parking-seoul-v109.json?v=109').then(function(r){return r.json()}).then(function(all){render(all[d]||[])}).catch(function(){})})
})();