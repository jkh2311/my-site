(function(){
  'use strict';
  function rad(v){return v*Math.PI/180}
  function deg(v){return v*180/Math.PI}
  function bearing(lat1,lng1,lat2,lng2){
    var p1=rad(lat1), p2=rad(lat2), dl=rad(lng2-lng1);
    var y=Math.sin(dl)*Math.cos(p2);
    var x=Math.cos(p1)*Math.sin(p2)-Math.sin(p1)*Math.cos(p2)*Math.cos(dl);
    return (deg(Math.atan2(y,x))+360)%360;
  }
  function initOne(el){
    if(el.dataset.rvReady==='1' || !window.kakao || !kakao.maps) return;
    var lat=parseFloat(el.dataset.lat), lng=parseFloat(el.dataset.lng);
    if(!isFinite(lat)||!isFinite(lng)) return;
    var target=new kakao.maps.LatLng(lat,lng);
    var rv=new kakao.maps.Roadview(el);
    var client=new kakao.maps.RoadviewClient();
    function load(radius, next){
      client.getNearestPanoId(target,radius,function(panoId){
        if(!panoId){ if(next) return next(); return fail(); }
        rv.setPanoId(panoId,target);
        kakao.maps.event.addListener(rv,'init',function(){
          try{
            var pos=rv.getPosition();
            var pan=bearing(pos.getLat(),pos.getLng(),lat,lng);
            rv.setViewpoint({pan:pan,tilt:0,zoom:0});
          }catch(e){}
          el.dataset.rvReady='1';
        });
      });
    }
    function fail(){
      el.classList.add('roadview-unavailable');
      el.innerHTML='<div class="roadview-fallback"><b>외관 거리뷰를 불러올 수 없습니다.</b><span>아래 네이버 위치지도를 이용해 주세요.</span></div>';
      el.dataset.rvReady='1';
    }
    load(80,function(){load(180)});
  }
  function init(){ document.querySelectorAll('.funeral-exterior-roadview[data-lat][data-lng]').forEach(initOne); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
