/* Public article view counter */
(function(){
 'use strict';
 var article=document.querySelector('main article.article');
 if(!article || !location.pathname.startsWith('/articles/') || !location.pathname.endsWith('.html'))return;
 var target=article.querySelector('.article-published-detail') || article.querySelector('.article-main-title');
 if(!target)return;
 var el=document.createElement('span');el.className='hani-article-views';el.setAttribute('aria-live','polite');el.textContent=' · 👁 조회수 확인 중';target.appendChild(el);
 var slug=location.pathname.split('/').pop().slice(0,-5);
 var key='haninelife-com-article-views-'+slug;
 var storageKey='hani-view-once-'+slug;
 var last=0;try{last=Number(localStorage.getItem(storageKey))||0;}catch(e){}
 var countIt=Date.now()-last>86400000;
 var endpoint='https://countapi.mileshilliard.com/api/v1/'+(countIt?'hit/':'get/')+encodeURIComponent(key);
 fetch(endpoint,{cache:'no-store'}).then(function(response){if(!response.ok)throw Error('counter unavailable');return response.json();}).then(function(data){
 var value=Number(data.value);if(!Number.isFinite(value)||value<0)throw Error('invalid count');
 el.textContent=' · 👁 조회수 '+Math.floor(value).toLocaleString('ko-KR');
 if(countIt){try{localStorage.setItem(storageKey,String(Date.now()));}catch(e){}}
 }).catch(function(){el.textContent=' · 👁 조회수 집계 중';});
})();
