(function(){
  var KEY='hanine-eye-comfort';
  function isOn(){try{return localStorage.getItem(KEY)==='on';}catch(e){return false;}}
  function save(on){try{localStorage.setItem(KEY,on?'on':'off');}catch(e){}}
  function apply(on){
    document.documentElement.classList.toggle('eye-comfort-mode',on);
    document.querySelectorAll('.eye-comfort-toggle').forEach(function(btn){
      btn.setAttribute('aria-pressed',on?'true':'false');
      btn.setAttribute('aria-label',on?'눈편한 모드 끄기':'눈편한 모드 켜기');
      btn.setAttribute('title',on?'눈편한 모드 끄기':'눈편한 모드 켜기');
      var icon=btn.querySelector('.eye-comfort-icon');
      var label=btn.querySelector('.eye-comfort-label');
      if(icon) icon.textContent=on?'☀️':'🌙';
      if(label) label.textContent=on?'원래 화면':'눈편한 모드';
    });
  }
  apply(isOn());
  document.addEventListener('click',function(e){
    var btn=e.target.closest && e.target.closest('.eye-comfort-toggle');
    if(!btn) return;
    var next=!document.documentElement.classList.contains('eye-comfort-mode');
    save(next);apply(next);
  });
  document.addEventListener('DOMContentLoaded',function(){apply(isOn());});
})();
