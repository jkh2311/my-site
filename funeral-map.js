(function(){
  'use strict';
  function initFuneralMaps(){
    if(!window.naver || !naver.maps) return;
    document.querySelectorAll('.naver-dynamic-map[data-lat][data-lng]').forEach(function(el){
      if(el.dataset.mapReady==='1') return;
      var lat=parseFloat(el.dataset.lat), lng=parseFloat(el.dataset.lng);
      if(!isFinite(lat)||!isFinite(lng)) return;
      var center=new naver.maps.LatLng(lat,lng);
      var map=new naver.maps.Map(el,{
        center:center,
        zoom:17,
        minZoom:7,
        zoomControl:true,
        zoomControlOptions:{position:naver.maps.Position.TOP_RIGHT},
        mapDataControl:false,
        scaleControl:true,
        logoControl:true
      });
      new naver.maps.Marker({position:center,map:map,title:el.dataset.name||'장례식장'});
      el.dataset.mapReady='1';
    });
  }
  window.hanineInitNaverMaps=initFuneralMaps;
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',initFuneralMaps);
  else initFuneralMaps();
})();
