(function(){
  'use strict';
  var KEY='hanine-dark-mode';
  function isOn(){try{return localStorage.getItem(KEY)==='on';}catch(e){return false;}}
  function save(on){try{localStorage.setItem(KEY,on?'on':'off');}catch(e){}}
  function apply(on){
    document.documentElement.classList.toggle('dark-mode',!!on);
    var buttons=document.querySelectorAll('.dark-mode-toggle');
    for(var i=0;i<buttons.length;i++){
      var btn=buttons[i];
      btn.setAttribute('aria-pressed',on?'true':'false');
      btn.setAttribute('aria-label',on?'다크모드 끄기':'다크모드 켜기');
      btn.setAttribute('title',on?'다크모드 끄기':'다크모드 켜기');
      var icon=btn.querySelector('.dark-mode-icon');
      var label=btn.querySelector('.dark-mode-label');
      if(icon) icon.textContent=on?'☀️':'🌙';
      if(label) label.textContent=on?'라이트모드':'다크모드';
    }
  }
  function toggleMode(ev){
    if(ev){ev.preventDefault();ev.stopPropagation();}
    var next=!document.documentElement.classList.contains('dark-mode');
    save(next);apply(next);
  }
  function bind(){
    apply(isOn());
    var buttons=document.querySelectorAll('.dark-mode-toggle');
    for(var i=0;i<buttons.length;i++){
      if(buttons[i].getAttribute('data-dark-bound')==='1') continue;
      buttons[i].setAttribute('data-dark-bound','1');
      buttons[i].addEventListener('click',toggleMode,false);
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',bind,false);
  else bind();
  window.addEventListener('pageshow',function(){apply(isOn());},false);
})();


/* CONTENT_CATEGORY_DRAWER_V1 */
(function(){
  function initCategoryMenus(){
    document.querySelectorAll('.content-category-area').forEach(function(area){
      var btn=area.querySelector('.content-category-toggle');
      var menu=area.querySelector('.content-category-menu');
      if(!btn||!menu||btn.dataset.ready==='1') return;
      btn.dataset.ready='1';
      btn.addEventListener('click',function(){
        var open=area.classList.toggle('is-open');
        btn.setAttribute('aria-expanded',open?'true':'false');
      });
      menu.querySelectorAll('a').forEach(function(a){
        a.addEventListener('click',function(){area.classList.remove('is-open');btn.setAttribute('aria-expanded','false');});
      });
      document.addEventListener('click',function(e){
        if(window.innerWidth<=700&&!area.contains(e.target)){area.classList.remove('is-open');btn.setAttribute('aria-expanded','false');}
      });
      var q=new URLSearchParams(location.search).get('category');
      if(q){var active=menu.querySelector('[data-cat="'+CSS.escape(q)+'"]');if(active)active.classList.add('active');}
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initCategoryMenus);else initCategoryMenus();
})();
