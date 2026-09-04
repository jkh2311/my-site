(function(){
  'use strict';
  var KEY='hanine-eye-comfort';
  function isOn(){try{return localStorage.getItem(KEY)==='on';}catch(e){return false;}}
  function save(on){try{localStorage.setItem(KEY,on?'on':'off');}catch(e){}}
  function apply(on){
    document.documentElement.classList.toggle('eye-comfort-mode',!!on);
    var buttons=document.querySelectorAll('.eye-comfort-toggle');
    for(var i=0;i<buttons.length;i++){
      var btn=buttons[i];
      btn.setAttribute('aria-pressed',on?'true':'false');
      btn.setAttribute('aria-label',on?'눈편한 모드 끄기':'눈편한 모드 켜기');
      btn.setAttribute('title',on?'눈편한 모드 끄기':'눈편한 모드 켜기');
      var icon=btn.querySelector('.eye-comfort-icon');
      var label=btn.querySelector('.eye-comfort-label');
      if(icon) icon.textContent=on?'☀️':'🌙';
      if(label) label.textContent=on?'원래 화면':'눈편한 모드';
    }
  }
  function toggleMode(ev){
    if(ev){ev.preventDefault();ev.stopPropagation();}
    var next=!document.documentElement.classList.contains('eye-comfort-mode');
    save(next);apply(next);
  }
  function bind(){
    apply(isOn());
    var buttons=document.querySelectorAll('.eye-comfort-toggle');
    for(var i=0;i<buttons.length;i++){
      if(buttons[i].getAttribute('data-eye-bound')==='1') continue;
      buttons[i].setAttribute('data-eye-bound','1');
      buttons[i].addEventListener('click',toggleMode,false);
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',bind,false);
  else bind();
  window.addEventListener('pageshow',function(){apply(isOn());},false);
})();
