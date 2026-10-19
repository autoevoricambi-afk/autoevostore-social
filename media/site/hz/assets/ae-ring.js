(function(){
  function init(root){
    if(!root||root.dataset.aeInit)return;root.dataset.aeInit='1';
    var stage=root.querySelector('.ae-ring__stage'),rot=root.querySelector('.ae-ring__rot'),items=[].slice.call(root.querySelectorAll('.ae-ring__it'));
    var n=items.length;if(n<2)return;
    var capN=root.querySelector('[data-cap-n]'),capS=root.querySelector('[data-cap-s]'),go=root.querySelector('[data-go]'),glow=root.querySelector('.ae-ring__glow');
    var rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
    var step=360/n,ang=0,vel=0,target=null,dragging=false,moved=0,lastX=0,lastT=0,vis=true,raf=0,front=-1,auto=!rm,idle=0;
    function R(){var w=stage.clientWidth;return Math.max(150,Math.min(w*(w<640?.46:.34),430))}
    function layout(){
      var r=R();
      items.forEach(function(it,i){it.style.transform='rotateY('+(i*step)+'deg) translateZ('+r+'px)'});
    }
    function norm(a){a=a%360;if(a>180)a-=360;if(a<-180)a+=360;return a}
    function paint(){
      rot.style.transform='translateZ('+(-R())+'px) rotateY('+ang+'deg)';
      var best=0,bd=999;
      items.forEach(function(it,i){var d=Math.abs(norm(i*step+ang));if(d<bd){bd=d;best=i}it.dataset.front=d<step/2?'1':'0'});
      if(best!==front){front=best;var it=items[best];
        if(capN)capN.textContent=it.dataset.name;if(capS)capS.textContent=it.dataset.sub;
        if(go){go.href=it.getAttribute('href');go.setAttribute('aria-label','Vedi '+it.dataset.name)}
        if(glow)glow.style.setProperty('--ae-c',it.dataset.c||'#1fbf75');
        items.forEach(function(x,j){x.setAttribute('aria-current',j===best?'true':'false');x.tabIndex=j===best?0:-1});
      }
    }
    function snapTo(i){ // porta l'elemento i davanti per la via piu' breve
      var d=norm(i*step+ang);target=ang-d;vel=0;auto=false;idle=0
    }
    function tick(){
      raf=0;if(!vis)return;
      if(dragging){}
      else if(target!==null){var d=target-ang;ang+=d*.12;if(Math.abs(d)<.05){ang=target;target=null}}
      else if(Math.abs(vel)>.01){ang+=vel;vel*=.94}
      else if(Math.abs(vel)<=.01&&!rm&&auto){ang-=.12}
      else if(!rm&&!auto){idle++;if(idle>420)auto=true}
      paint();
      if(!rm||target!==null||Math.abs(vel)>.01||dragging)raf=requestAnimationFrame(tick);
    }
    function wake(){if(!raf)raf=requestAnimationFrame(tick)}
    stage.addEventListener('pointerdown',function(e){if(e.button>0)return;dragging=true;moved=0;lastX=e.clientX;lastT=performance.now();vel=0;target=null;auto=false;stage.classList.add('is-drag');try{stage.setPointerCapture(e.pointerId)}catch(_){}wake()});
    stage.addEventListener('pointermove',function(e){if(!dragging)return;var dx=e.clientX-lastX,now=performance.now(),dt=Math.max(1,now-lastT);moved+=Math.abs(dx);ang+=dx*.32;vel=dx*.32*(16/dt);lastX=e.clientX;lastT=now;wake()});
    function up(){if(!dragging)return;dragging=false;stage.classList.remove('is-drag');if(Math.abs(vel)<.4)vel=0;wake();setTimeout(function(){moved=0},0)}
    stage.addEventListener('pointerup',up);stage.addEventListener('pointercancel',up);
    items.forEach(function(it,i){it.addEventListener('click',function(e){if(moved>6){e.preventDefault();return}if(i!==front){e.preventDefault();snapTo(i);wake()}})});
    function move(dir){var i=(front+dir+n)%n;snapTo(i);wake()}
    var pv=root.querySelector('[data-prev]'),nx=root.querySelector('[data-next]');
    if(pv)pv.addEventListener('click',function(){move(-1)});if(nx)nx.addEventListener('click',function(){move(1)});
    root.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();move(1)}else if(e.key==='ArrowLeft'){e.preventDefault();move(-1)}});
    window.addEventListener('resize',function(){layout();paint()});
    if('IntersectionObserver' in window)new IntersectionObserver(function(es){vis=es[0].isIntersecting;if(vis)wake()},{threshold:0}).observe(root);
    layout();paint();wake();
  }
  function boot(){document.querySelectorAll('.ae-ring').forEach(init)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
  document.addEventListener('shopify:section:load',boot);
})();
