(function(){
  function init(root){
    if(!root||root.dataset.aeInit)return;root.dataset.aeInit='1';
    var cv=root.querySelector('canvas'),ctx=cv.getContext('2d');if(!ctx)return;
    var rng=root.querySelector('input[type=range]'),out=root.querySelector('[data-temp]'),pre=[].slice.call(root.querySelectorAll('[data-pre]'));
    var rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
    var lanes=[].slice.call(root.querySelectorAll('[data-grade]')).map(function(el){
      var g=el.getAttribute('data-grade'),m=/^(\d+)W-?(\d+)$/i.exec(g.replace(/\s/g,''));
      return m?{g:g,w:+m[1],h:+m[2],drops:[],acc:Math.random()}:null}).filter(Boolean);
    if(!lanes.length)return;
    var W=0,H=0,dpr=1,temp=parseFloat(rng.value),vis=true,raf=0,last=0;
    function cold(w){return Math.max(.18,1-w*.045)}      /* 0W scorre meglio a freddo di 15W (illustrativo) */
    function hot(h){return h<=20?1.15:h<=30?1:h<=40?.86:.74} /* a caldo piu' denso = scorre un po' meno */
    function flow(l){var t=Math.min(1,Math.max(0,(temp+20)/120));var c=cold(l.w),k=hot(l.h);return k*(c+(1-c)*Math.pow(t,.7))}
    function resize(){var r=cv.getBoundingClientRect();dpr=Math.min(2,window.devicePixelRatio||1);W=r.width;H=r.height;cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);draw()}
    function colorFor(t){/* ambra a freddo piu' scuro e denso, piu' chiaro a caldo */var a=.62+.38*Math.min(1,Math.max(0,(t+20)/120));return 'rgba('+Math.round(214*a)+','+Math.round(148*a)+','+Math.round(34*a)+',1)'}
    function draw(){
      ctx.clearRect(0,0,W,H);
      var n=lanes.length,pad=Math.max(16,W*.04),lw=(W-pad*2)/n,top=54,bot=H-30;
      ctx.font='600 '+Math.round(Math.min(18,W/30))+'px Inter,system-ui,sans-serif';ctx.textAlign='center';
      lanes.forEach(function(l,i){
        var cx=pad+lw*i+lw/2,tw=Math.min(62,lw*.5);
        /* tubo */
        var g=ctx.createLinearGradient(cx-tw/2,0,cx+tw/2,0);g.addColorStop(0,'rgba(244,241,234,.04)');g.addColorStop(.5,'rgba(244,241,234,.1)');g.addColorStop(1,'rgba(244,241,234,.03)');
        ctx.fillStyle=g;ctx.strokeStyle='rgba(244,241,234,.16)';ctx.lineWidth=1;
        rr(cx-tw/2,top,tw,bot-top,tw/2);ctx.fill();ctx.stroke();
        /* gocce */
        var col=colorFor(temp);
        l.drops.forEach(function(d){
          var y=top+d.y*(bot-top),r=d.r*Math.min(1,tw/34);
          var rg=ctx.createRadialGradient(cx-r*.35,y-r*.4,r*.1,cx,y,r*1.15);rg.addColorStop(0,'rgba(255,236,170,.95)');rg.addColorStop(.35,col);rg.addColorStop(1,'rgba(90,50,8,.95)');
          var tl=Math.min(r*(1+flow(l)*5),y-top);var tg=ctx.createLinearGradient(0,y-tl,0,y);tg.addColorStop(0,'rgba(214,148,34,0)');tg.addColorStop(1,'rgba(214,148,34,.45)');ctx.fillStyle=tg;ctx.fillRect(cx-r*.55,y-tl,r*1.1,tl);
          ctx.fillStyle=rg;ctx.beginPath();ctx.ellipse(cx,y,r,r*1.28,0,0,6.2832);ctx.fill();
          ctx.fillStyle='rgba(255,255,255,.55)';ctx.beginPath();ctx.ellipse(cx-r*.34,y-r*.5,r*.22,r*.34,-.4,0,6.2832);ctx.fill();
        });
        /* etichetta + barra di scorrimento */
        var f=flow(l);
        ctx.fillStyle='#f4f1ea';ctx.fillText(l.g,cx,30);
        var bw=Math.min(70,lw*.6);ctx.fillStyle='rgba(244,241,234,.12)';rr(cx-bw/2,H-16,bw,5,3);ctx.fill();
        ctx.fillStyle='#1fbf75';rr(cx-bw/2,H-16,Math.max(4,bw*Math.min(1,f/1.15)),5,3);ctx.fill();
      });
    }
    function rr(x,y,w,h,r){r=Math.min(r,w/2,h/2);ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath()}
    function step(ts){
      raf=0;if(!vis)return;var dt=Math.min(.05,(ts-(last||ts))/1000);last=ts;
      lanes.forEach(function(l){
        var f=flow(l);
        var lastD=l.drops[l.drops.length-1];
        if(!lastD||lastD.y>.19){l.drops.push({y:0,r:6+((l.drops.length*7)%4)})}   /* distanza fissa: la differenza si vede nella velocita' */
        l.drops.forEach(function(d){d.y+=dt*f*.62});
        l.drops=l.drops.filter(function(d){return d.y<1.04});
      });
      draw();raf=requestAnimationFrame(step);
    }
    function wake(){if(rm){draw();return}if(!raf){last=0;raf=requestAnimationFrame(step)}}
    function setTemp(v){temp=v;rng.value=v;out.firstChild.nodeValue=Math.round(v)+' °C';rng.setAttribute('aria-valuetext',Math.round(v)+' gradi');pre.forEach(function(b){b.setAttribute('aria-pressed',String(+b.dataset.pre===Math.round(v)))});if(rm)draw()}
    rng.addEventListener('input',function(){setTemp(parseFloat(rng.value))});
    pre.forEach(function(b){b.addEventListener('click',function(){setTemp(+b.dataset.pre)})});
    window.addEventListener('resize',resize);
    if('IntersectionObserver' in window)new IntersectionObserver(function(es){vis=es[0].isIntersecting;if(vis)wake()},{threshold:0}).observe(root);
    setTemp(-10);resize();wake();
  }
  function boot(){document.querySelectorAll('.ae-visco').forEach(init)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
  document.addEventListener('shopify:section:load',boot);
})();
