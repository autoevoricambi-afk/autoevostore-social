(function(){var AE=window.AE3D;if(!AE)return;var host=document.getElementById('ae3d-host');if(!host||host.shadowRoot)return;
var root=host.attachShadow({mode:'open'});var $$=root,$H=host;AE.meta=[{"name": "Castrol EDGE", "sub": "5W-30 LongLife", "c": "#22a559", "ar": 0.39714285714285713}, {"name": "TotalEnergies Quartz", "sub": "5W-30 INEO MC3", "c": "#e8a317", "ar": 0.4657142857142857}, {"name": "Mobil 1 ESP", "sub": "5W-30", "c": "#2f6fe0", "ar": 0.47714285714285715}, {"name": "Castrol Magnatec", "sub": "5W-30 A5", "c": "#d93a3a", "ar": 0.39571428571428574}, {"name": "Petronas Syntium", "sub": "5W-30", "c": "#13b5a3", "ar": 0.5171428571428571}, {"name": "Castrol EDGE", "sub": "0W-20 C5", "c": "#22a559", "ar": 0.3871428571428571}];
try{if(sessionStorage.getItem('aeSeen'))host.classList.add('seen');sessionStorage.setItem('aeSeen','1')}catch(e){}
var l=document.createElement('link');l.rel='stylesheet';l.href=AE.css;root.appendChild(l);
root.appendChild(document.getElementById('ae3d-tpl').content.cloneNode(true));
root.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a)return;var id=a.getAttribute('href').slice(1),t=id&&(root.getElementById(id)||document.querySelector('[id$="__'+id+'"]'));if(t){e.preventDefault();window.scrollTo({top:t.getBoundingClientRect().top+scrollY-20,behavior:'smooth'})}});
function GLR(cv){/* ---------- WebGL 3D ---------- */
const gl=cv.getContext('webgl2',{antialias:true,alpha:true,premultipliedAlpha:true});
const M={mul(a,b){const o=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++){let s=0;for(let k=0;k<4;k++)s+=a[k*4+r]*b[c*4+k];o[c*4+r]=s}return o},
 persp(f,a,n,fa){const t=1/Math.tan(f/2),nf=1/(n-fa);return new Float32Array([t/a,0,0,0,0,t,0,0,0,0,(fa+n)*nf,-1,0,0,2*fa*n*nf,0])},
 T:(x,y,z)=>new Float32Array([1,0,0,0,0,1,0,0,0,0,1,0,x,y,z,1]),S:(x,y,z)=>new Float32Array([x,0,0,0,0,y,0,0,0,0,z,0,0,0,0,1]),
 Ry(a){const c=Math.cos(a),s=Math.sin(a);return new Float32Array([c,0,-s,0,0,1,0,0,s,0,c,0,0,0,0,1])},
 Rx(a){const c=Math.cos(a),s=Math.sin(a);return new Float32Array([1,0,0,0,0,c,s,0,0,-s,c,0,0,0,0,1])}};
const VS=`#version 300 es
in vec3 aP;in vec3 aN;in vec2 aUV;uniform mat4 uVP,uM;uniform mat3 uNM;out vec3 vW;out vec3 vN;out vec2 vUV;
void main(){vec4 w=uM*vec4(aP,1.);vW=w.xyz;vN=uNM*aN;vUV=aUV;gl_Position=uVP*w;}`;
const FS=`#version 300 es
precision highp float;in vec3 vW;in vec3 vN;in vec2 vUV;uniform sampler2D uMap;uniform vec3 uCam,uAcc,uL;uniform float uBright,uAlpha,uFloor,uBack,uRefl;out vec4 o;
float box(float x,float c,float w,float s){return smoothstep(c-w-s,c-w,x)-smoothstep(c+w,c+w+s,x);}
void main(){vec4 t=texture(uMap,vUV);if(t.a<.55)discard;
 vec3 N=normalize(vN);vec3 V=normalize(uCam-vW);if(dot(N,V)<0.)N=-N;
 vec3 L=normalize(uL);vec3 H=normalize(L+V);
 float dif=max(dot(N,L),0.);float sp=pow(max(dot(N,H),0.),90.);vec3 R=reflect(-V,N);float fr=pow(1.-max(dot(N,V),0.),3.);
 float sbx=box(R.x,.55,.12,.25)*smoothstep(-.4,.5,R.y);float sbl=box(R.x,-.6,.07,.2)*smoothstep(-.5,.4,R.y);float top=smoothstep(.55,.95,R.y);
 float env=sbx*1.1+sbl*.7+top*.8;
 vec3 col=t.rgb*(.36+.8*dif)+vec3(1.)*(sp*.5+env*(.12+.5*fr))+uAcc*fr*.9;
 if(uBack>0.)col*=.5;col*=uBright;float a=uAlpha;
 if(uRefl>0.){a*=clamp(1.-(uFloor-vW.y)/1.7,0.,1.);a*=a*.55;}
 o=vec4(col*a,a);}`;
function sh(t,s){const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))console.error(gl.getShaderInfoLog(x));return x}
const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,VS));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,FS));gl.linkProgram(pr);gl.useProgram(pr);
const U={};['uVP','uM','uNM','uMap','uCam','uAcc','uBright','uAlpha','uFloor','uBack','uRefl','uL'].forEach(n=>U[n]=gl.getUniformLocation(pr,n));
const LOC={aP:gl.getAttribLocation(pr,'aP'),aN:gl.getAttribLocation(pr,'aN'),aUV:gl.getAttribLocation(pr,'aUV')};
const HB=3.0,FLOOR=-1.5;let items=[];
/* mappa di profondita: distanza dal bordo trasparente (rigonfiamento) */
function inflate(img){const ar=img.width/img.height,nx=150,ny=Math.round(nx/ar);const c=document.createElement('canvas');c.width=nx;c.height=ny;const x=c.getContext('2d');x.drawImage(img,0,0,nx,ny);const d=x.getImageData(0,0,nx,ny).data;
 const INF=1e9,D=new Float32Array(nx*ny);for(let i=0;i<nx*ny;i++)D[i]=d[i*4+3]>128?INF:0;
 for(let y=0;y<ny;y++)for(let xx=0;xx<nx;xx++){const i=y*nx+xx;if(!D[i])continue;let v=D[i];if(xx>0)v=Math.min(v,D[i-1]+1);if(y>0)v=Math.min(v,D[i-nx]+1);if(xx>0&&y>0)v=Math.min(v,D[i-nx-1]+1.414);if(xx<nx-1&&y>0)v=Math.min(v,D[i-nx+1]+1.414);D[i]=v}
 for(let y=ny-1;y>=0;y--)for(let xx=nx-1;xx>=0;xx--){const i=y*nx+xx;if(!D[i])continue;let v=D[i];if(xx<nx-1)v=Math.min(v,D[i+1]+1);if(y<ny-1)v=Math.min(v,D[i+nx]+1);if(xx<nx-1&&y<ny-1)v=Math.min(v,D[i+nx+1]+1.414);if(xx>0&&y<ny-1)v=Math.min(v,D[i+nx-1]+1.414);D[i]=v}
 const Wd=HB*ar,Dw=Wd*.3,R=nx*.17,H=new Float32Array(nx*ny);
 for(let i=0;i<nx*ny;i++){const dd=Math.min(D[i],R);H[i]=D[i]>0?Math.sqrt(Math.max(0,R*R-(R-dd)*(R-dd)))/R*Dw:0}
 for(let p=0;p<7;p++){const B=new Float32Array(H);for(let y=1;y<ny-1;y++)for(let xx=1;xx<nx-1;xx++){const i=y*nx+xx;if(D[i]>0)B[i]=(H[i]*4+H[i-1]+H[i+1]+H[i-nx]+H[i+nx])/8}H.set(B)}
 return{nx,ny,H,ar,Wd}}
function mesh(f,back){const{nx,ny,H,Wd}=f,cw=Wd/(nx-1),ch=HB/(ny-1),sg=back?-1:1,k=back?.8:1;const V=new Float32Array(nx*ny*8);
 for(let y=0;y<ny;y++)for(let x=0;x<nx;x++){const i=y*nx+x,o=i*8;const hl=H[y*nx+Math.max(0,x-1)],hr=H[y*nx+Math.min(nx-1,x+1)],hu=H[Math.max(0,y-1)*nx+x],hd=H[Math.min(ny-1,y+1)*nx+x];
  const dx=(hr-hl)/(2*cw),dy=(hu-hd)/(2*ch);let nX=-dx*sg*k,nY=-dy*sg*k,nZ=sg;const l=Math.hypot(nX,nY,nZ);
  V[o]=(x/(nx-1)-.5)*Wd;V[o+1]=(.5-y/(ny-1))*HB;V[o+2]=H[i]*sg*k;V[o+3]=nX/l;V[o+4]=nY/l;V[o+5]=nZ/l;V[o+6]=x/(nx-1);V[o+7]=y/(ny-1)}
 const I=new Uint32Array((nx-1)*(ny-1)*6);let q=0;for(let y=0;y<ny-1;y++)for(let x=0;x<nx-1;x++){const a=y*nx+x,b=a+1,c=a+nx,d=c+1;I[q++]=a;I[q++]=c;I[q++]=b;I[q++]=b;I[q++]=c;I[q++]=d}
 const vao=gl.createVertexArray();gl.bindVertexArray(vao);const vb=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,vb);gl.bufferData(gl.ARRAY_BUFFER,V,gl.STATIC_DRAW);
 [['aP',3,0],['aN',3,12],['aUV',2,24]].forEach(([n,s,off])=>{gl.enableVertexAttribArray(LOC[n]);gl.vertexAttribPointer(LOC[n],s,gl.FLOAT,false,32,off)});
 const ib=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ib);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,I,gl.STATIC_DRAW);return{vao,n:I.length}}
const SVS=`#version 300 es
in vec2 aQ;uniform mat4 uVP;uniform vec3 uC;uniform vec2 uS;out vec2 vQ;void main(){vQ=aQ;gl_Position=uVP*vec4(uC.x+aQ.x*uS.x,uC.y,uC.z+aQ.y*uS.y,1.);}`;
const SFS=`#version 300 es
precision mediump float;in vec2 vQ;uniform float uA;out vec4 o;void main(){float a=smoothstep(1.,0.,length(vQ));a=a*a*uA;o=vec4(0.,0.,0.,a);}`;
const sp=gl.createProgram();gl.attachShader(sp,sh(gl.VERTEX_SHADER,SVS));gl.attachShader(sp,sh(gl.FRAGMENT_SHADER,SFS));gl.linkProgram(sp);
const SU={uVP:gl.getUniformLocation(sp,'uVP'),uC:gl.getUniformLocation(sp,'uC'),uS:gl.getUniformLocation(sp,'uS'),uA:gl.getUniformLocation(sp,'uA')};
const sq=gl.createVertexArray();gl.bindVertexArray(sq);const sbf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,sbf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
const sl=gl.getAttribLocation(sp,'aQ');gl.enableVertexAttribArray(sl);gl.vertexAttribPointer(sl,2,gl.FLOAT,false,0,0);gl.useProgram(pr);
function shadow(VP,x,y,z,sx,sz,a){gl.useProgram(sp);gl.uniformMatrix4fv(SU.uVP,false,VP);gl.uniform3f(SU.uC,x,y,z);gl.uniform2f(SU.uS,sx,sz);gl.uniform1f(SU.uA,a);gl.bindVertexArray(sq);gl.drawArrays(gl.TRIANGLE_STRIP,0,4);gl.useProgram(pr)}
function hex(c){return[parseInt(c.slice(1,3),16)/255,parseInt(c.slice(3,5),16)/255,parseInt(c.slice(5,7),16)/255]}

return{gl,M,U,LOC,inflate,mesh,hex,HB,FLOOR,pr,shadow}}


const P=AE.meta.map((m,i)=>Object.assign({},m,{src:AE.imgs[i]})),T=5200,RM_=matchMedia('(prefers-reduced-motion:reduce)').matches;
/* ---------- titolo, apertura, nastro ---------- */
(function(){const t=$$.getElementById('t');let k=0;t.querySelectorAll('span,b').forEach(el=>{const txt=el.textContent;el.textContent='';[...txt].forEach(c=>{const x=document.createElement('span');x.className='ch';x.textContent=c===' '?' ':c;x.style.animationDelay=(1.9+k*0.035)+'s';k++;el.appendChild(x)})})})();
setTimeout(()=>$$.getElementById('cine').classList.add('go'),350);
setTimeout(()=>$$.getElementById('cine').style.display='none',3200);
(function(){const m=['Castrol','TotalEnergies','Mobil 1','Petronas','Mannol','Selenia','ENI','Ford Motorcraft'];const h=m.map(x=>'<b>'+x+'</b><em>&bull;</em>').join('');$$.getElementById('mq').innerHTML=h+h+h+h})();
const hero=$$.getElementById('hero'),stage=$$.getElementById('stage'),cv=$$.getElementById('gl');
/* ---------- UI ---------- */
const W_=['CASTROL','TOTAL','MOBIL 1','CASTROL','PETRONAS','CASTROL'],wd=$$.getElementById('word');let wcur='',cur=0;
function setWord(t){if(t===wcur&&wd.textContent)return;wcur=t;wd.classList.add('out');setTimeout(()=>{wd.textContent=t;wd.classList.remove('out');wd.classList.add('in');requestAnimationFrame(()=>requestAnimationFrame(()=>wd.classList.remove('in')))},wd.textContent?550:0)}
const bar=$$.getElementById('bar');P.forEach(()=>bar.appendChild(document.createElement('span')));
function ui(){const p=P[cur];$H.style.setProperty('--accent',p.c);setWord(W_[cur]);
 $$.getElementById('cn').textContent=p.name;{const cl=$$.getElementById('capl');if(cl)cl.href='/products/'+["castrol-edge-longlife-iii-5w-30-olio-motore-originale-vw-audi-seat-skoda-porsche-c30-mb-229-52-acea-c3", "total-quartz-ineo-mc3-5w-30-olio-motore-sintetico-low-saps-acea-c3-api-sn-plus", "mobil-1-esp-5w-30-acea-c3-bmw-ll-04-mb-229-52-vw-504-507-psa-rn0710-c30", "castrol-ford-magnatec-a5-5w-30-a5", "petronas-syntium-prime-xs-5w-30-acea-c3-dexos2-dexos-d", "castrol-edge-0w-20-c5-olio-motore-acea-c5-c6-dexos1-gen-3-mb-229-71"][cur];const lv=$$.getElementById('live');if(lv)lv.textContent=p.name+' '+p.sub}$$.getElementById('cs').textContent=p.sub;$$.getElementById('no').textContent=String(cur+1).padStart(2,'0');
 [...bar.children].forEach((s,i)=>{s.className=i==cur?'on':'';s.style.setProperty('--d',T+'ms')});
 const fl=$$.getElementById('flare');fl.classList.remove('go');void fl.offsetWidth;fl.classList.add('go');targets()}
let heroVis=true;
let R=null;try{R=GLR(cv)}catch(e){}
const gl=R?R.gl:null,M=R?R.M:null,U=R?R.U:null,inflate=R?R.inflate:null,mesh=R?R.mesh:null,hex=R?R.hex:null,FLOOR=R?R.FLOOR:-1.5;let items=[];
if(!R){const im=new Image();im.crossOrigin='anonymous';im.src=P[0].src;im.style.cssText='position:absolute;left:50%;top:50%;height:70%;transform:translate(-50%,-50%);z-index:2';stage.appendChild(im)}
let loaded=0;
if(R)P.forEach((p,i)=>{const img=new Image();img.crossOrigin='anonymous';img.onload=()=>{const f=inflate(img);const tex=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,tex);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,img);gl.generateMipmap(gl.TEXTURE_2D);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  items[i]={tex,front:mesh(f,false),back:mesh(f,true),acc:hex(p.c),s:{x:0,y:0,z:-6,ry:0,s:.5,b:0,v:0},t:{x:0,z:0,ry:0,s:1,b:1,v:1},w:f.Wd};
  if(++loaded===P.length){targets();cv.classList.add('ready')}};img.src=p.src});
function targets(){const n=P.length,sp=(cv.clientWidth/cv.clientHeight)<1?1.9:2.5;items.forEach((it,i)=>{if(!it)return;let o=((i-cur)%n+n)%n;if(o>n/2)o-=n;const a=Math.abs(o);it.o=o;it.t={x:o*sp*(a>1?1.04:1),z:-a*2.3,ry:-o*.6,s:a==0?1:.8,b:a==0?1:(a==1?.5:.2),v:a<=2?1:0}})}
/* interazione */
let mx=0,my=0,drag=0,dragV=0,down=false,moved=0,lx=0;
hero.addEventListener('mousemove',e=>{const r=hero.getBoundingClientRect();mx=(e.clientX-r.left)/r.width-.5;my=(e.clientY-r.top)/r.height-.5;hero.style.setProperty('--mx',(e.clientX-r.left)+'px');hero.style.setProperty('--my',(e.clientY-r.top)+'px')});
cv.addEventListener('pointerdown',e=>{down=true;moved=0;lx=e.clientX;cv.classList.add('drag');cv.setPointerCapture(e.pointerId)});
cv.addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-lx;lx=e.clientX;moved+=Math.abs(dx);drag+=dx*.012;dragV=dx*.012});
cv.addEventListener('pointerup',e=>{down=false;cv.classList.remove('drag');if(moved<6){const r=cv.getBoundingClientRect(),px=(e.clientX-r.left)/r.width*2-1;let best=-1,bd=.3;items.forEach((it,i)=>{if(!it||it.px===undefined)return;const d=Math.abs(it.px-px);if(d<bd&&it.o!==0){bd=d;best=i}});if(best>=0){cur=best;ui();restart()}}});
addEventListener('keydown',e=>{if(/INPUT|TEXTAREA/.test(e.target.tagName))return;if(!heroVis||false)return;if(e.key==='ArrowRight'){cur=(cur+1)%P.length;ui();restart()}if(e.key==='ArrowLeft'){cur=(cur+P.length-1)%P.length;ui();restart()}});
let timer;function restart(){clearInterval(timer);timer=setInterval(()=>{if(!down&&!document.hidden&&!window.__aeManualPause&&!matchMedia('(prefers-reduced-motion: reduce)').matches){cur=(cur+1)%P.length;ui()}},T)}restart();
const bt=$$.querySelector('.btn');bt.addEventListener('mousemove',e=>{const r=bt.getBoundingClientRect();bt.style.transform='translate('+((e.clientX-r.left-r.width/2)*.25)+'px,'+((e.clientY-r.top-r.height/2)*.35)+'px)'});bt.addEventListener('mouseleave',()=>bt.style.transform='');
/* render */
let last=performance.now(),VP,camZ=10.2,camY=-.25;
function size(){const dpr=Math.min(devicePixelRatio||1,window.__aeQ||2),w=cv.clientWidth,h=cv.clientHeight;if(cv.width!==Math.round(w*dpr)||cv.height!==Math.round(h*dpr)){cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr)}
 const asp=w/h;camZ=asp<1?11.5:10.2;VP=M.mul(M.persp(26*Math.PI/180,asp,.5,60),M.T(-mx*.7,-camY,-camZ));gl.viewport(0,0,cv.width,cv.height)}
function draw(it,model,refl,back){const nm=new Float32Array([model[0],model[1],model[2],model[4],model[5],model[6],model[8],model[9],model[10]]);
 gl.uniformMatrix4fv(U.uM,false,model);gl.uniformMatrix3fv(U.uNM,false,nm);gl.uniform1f(U.uBack,back?1:0);gl.uniform1f(U.uRefl,refl?1:0);const m=back?it.back:it.front;gl.bindVertexArray(m.vao);gl.drawElements(gl.TRIANGLES,m.n,gl.UNSIGNED_INT,0)}
function frame(now){if(!heroVis){last=now;requestAnimationFrame(frame);return}const dt=Math.min((now-last)/1000,.05);last=now;size();const k=1-Math.exp(-dt*3.4);
 gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.disable(gl.CULL_FACE);gl.enable(gl.BLEND);gl.blendFunc(gl.ONE,gl.ONE_MINUS_SRC_ALPHA);
 if(!down){drag+=dragV;dragV*=Math.pow(.02,dt);drag*=Math.exp(-dt*1.1)}
 gl.uniformMatrix4fv(U.uVP,false,VP);gl.uniform3f(U.uCam,mx*.7,camY,camZ);gl.uniform1f(U.uFloor,FLOOR);gl.uniform1i(U.uMap,0);gl.uniform3f(U.uL,.55+mx*1.5,.8-my*1.2,.7);
 const t=RM_?0:now/1000,list=items.filter(Boolean).sort((a,b)=>a.s.z-b.s.z);
 list.forEach(it=>{const s=it.s,g=it.t;['x','z','ry','s','b','v'].forEach(q=>s[q]+=(g[q]-s[q])*k)});
 const pass=(refl)=>list.forEach(it=>{const s=it.s;if(s.v<.02)return;const act=it.o===0;
  const ry=s.ry+(act?Math.sin(t*.55)*.4+mx*.5+drag:Math.sin(t*.4+it.o)*.08),rx=act?my*.12:0;
  const rot=M.mul(M.Ry(ry),M.mul(M.Rx(rx),M.S(s.s,s.s,s.s)));
  const m=refl?M.mul(M.T(s.x,2*FLOOR,s.z),M.mul(M.S(1,-1,1),rot)):M.mul(M.T(s.x,(1-s.s)*-1.5,s.z),rot);
  gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,it.tex);gl.uniform3f(U.uAcc,it.acc[0]*.55,it.acc[1]*.55,it.acc[2]*.55);gl.uniform1f(U.uBright,s.b);gl.uniform1f(U.uAlpha,s.v);
  draw(it,m,refl,true);draw(it,m,refl,false)});
 gl.depthMask(false);list.forEach(it=>{const s=it.s;if(s.v<.02)return;R.shadow(VP,s.x,FLOOR+.01,s.z,(it.w||1.2)*s.s*1.45,.95*s.s,.62*s.v*Math.min(1,s.b+.35))});pass(true);gl.depthMask(true);pass(false);
 items.forEach(it=>{if(!it)return;const w=M.mul(VP,new Float32Array([1,0,0,0,0,1,0,0,0,0,1,0,it.s.x,0,it.s.z,1]));it.px=w[12]/w[15]});
 requestAnimationFrame(frame)}
if(!gl){cv.style.display='none'}else{requestAnimationFrame(frame)}
ui();
/* nebbia + polvere */
const dc=$$.getElementById('dust'),cx=dc.getContext('2d');let Wd,Hd,dots=[];
function dsz(){Wd=dc.width=hero.clientWidth;Hd=dc.height=hero.clientHeight;dots=Array.from({length:Math.round(Wd*Hd/26000)},()=>({x:Math.random()*Wd,y:Math.random()*Hd,r:Math.random()*1.4+.3,v:Math.random()*.25+.05,a:Math.random()*.5+.15}))}
dsz();addEventListener('resize',dsz);
if(!matchMedia('(prefers-reduced-motion:reduce)').matches){const fog=Array.from({length:5},()=>({y:.45+Math.random()*.5,r:.22+Math.random()*.22,s:.00006+Math.random()*.00008,p:Math.random()*6}));
(function f(tm){cx.clearRect(0,0,Wd,Hd);const ac=getComputedStyle($H).getPropertyValue('--accent').trim()||'#22a559';cx.globalCompositeOperation='screen';
 fog.forEach(o=>{const x=(.45+.55*((Math.sin(tm*o.s+o.p)+1)/2))*Wd,y=o.y*Hd,r=o.r*Math.max(Wd,Hd);const g=cx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,ac+'14');g.addColorStop(1,ac+'00');cx.fillStyle=g;cx.fillRect(x-r,y-r,r*2,r*2)});
 cx.globalCompositeOperation='source-over';dots.forEach(d=>{d.y-=d.v;d.x+=Math.sin(d.y/60)*.12;if(d.y<-5){d.y=Hd+5;d.x=Math.random()*Wd}cx.globalAlpha=d.a;cx.fillStyle='#fff';cx.beginPath();cx.arc(d.x,d.y,d.r,0,6.3);cx.fill()});cx.globalAlpha=1;requestAnimationFrame(f)})(0)}


/* Lightweight progressive enhancements; compatible with standalone preview */
(()=>{
 const menu=$$.getElementById('menuToggle'),panel=$$.getElementById('mobileNav');
 if(menu&&panel){menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));panel.classList.toggle('open',open)});panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.setAttribute('aria-expanded','false');panel.classList.remove('open')}));document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu.setAttribute('aria-expanded','false');panel.classList.remove('open')}})}
 const prev=$$.getElementById('prevBottle'),next=$$.getElementById('nextBottle'),pause=$$.getElementById('toggleBottle');
 const key=k=>window.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true}));
 if(prev)prev.addEventListener('click',()=>key('ArrowLeft'));
 if(next)next.addEventListener('click',()=>key('ArrowRight'));
 if(pause)pause.addEventListener('click',()=>{const off=pause.getAttribute('aria-pressed')!=='true';pause.setAttribute('aria-pressed',String(off));pause.textContent=off?'▶':'Ⅱ';pause.setAttribute('aria-label',off?'Riprendi la rotazione automatica':'Metti in pausa la rotazione automatica');window.__aeManualPause=off});
 $$.querySelectorAll('.fq button').forEach((btn,i)=>{btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-controls','ae-answer-'+i);const answer=btn.nextElementSibling;answer.id='ae-answer-'+i;btn.addEventListener('click',()=>{requestAnimationFrame(()=>$$.querySelectorAll('.fq button').forEach(x=>x.setAttribute('aria-expanded',String(x.parentElement.classList.contains('on')))))})});
 document.addEventListener('visibilitychange',()=>{$H.dataset.tabHidden=String(document.hidden)});
})();

(function(){
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v)),rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
/* immagini dai dati */
$$.querySelectorAll('img[data-p]').forEach(i=>i.src=P[+i.dataset.p].src);
/* reveal */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);setTimeout(()=>e.target.classList.add('done'),1300)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
$$.querySelectorAll('.rv').forEach(el=>io.observe(el));
/* tilt 3D */
$$.querySelectorAll('.cat,.pc').forEach(el=>{
 el.addEventListener('pointermove',e=>{if(e.pointerType==='touch')return;const r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;
  el.style.transform='rotateX('+((.5-y)*12)+'deg) rotateY('+((x-.5)*14)+'deg) translateZ(0)';el.style.setProperty('--gx',x*100+'%');el.style.setProperty('--gy',y*100+'%')});
 el.addEventListener('pointerleave',()=>el.style.transform='')});
/* header, progress, cursore */
const hdr=$$.getElementById('hdr'),pbar=$$.getElementById('pbar'),cur=$$.getElementById('cur');let ly=0,cx=innerWidth/2,cy=innerHeight/2,tx=cx,ty=cy;
addEventListener('pointermove',e=>{tx=e.clientX;ty=e.clientY});
const hv=new IntersectionObserver(e=>{heroVis=e[0].isIntersecting},{threshold:0});hv.observe($$.getElementById('hero'));
/* storia 3D */
const sc=$$.getElementById('sgl'),story=$$.getElementById('storia'),chaps=[...$$.querySelectorAll('.chap')],dots=[...$$.querySelectorAll('.sprog i')],sw=$$.getElementById('sword');
let R=null;try{R=GLR(sc)}catch(e){}
let svis=false;new IntersectionObserver(e=>{svis=e[0].isIntersecting},{threshold:0}).observe(story);
let chap=-1,prog=0;
function setChap(c){if(c===chap)return;chap=c;chaps.forEach((x,i)=>x.classList.toggle('on',i===c));dots.forEach((x,i)=>x.classList.toggle('on',i===c));
 const a=P[[0,1,2,4][c]].c;story.style.setProperty('--accent',a);story.querySelector('.sglow').style.setProperty('--accent',a);
 sw.style.opacity=0;setTimeout(()=>{sw.textContent=chaps[c].dataset.w;sw.style.opacity=1},300)}
const IDX=[0,1,2,4],S=[];
if(R){const{gl,M,U,inflate,mesh,hex,FLOOR}=R;
 IDX.forEach((pi_,k)=>{const img=new Image();img.crossOrigin='anonymous';img.onload=()=>{const f=inflate(img),tex=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,tex);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,img);gl.generateMipmap(gl.TEXTURE_2D);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  S[k]={tex,front:mesh(f,false),back:mesh(f,true),acc:hex(P[pi_].c),s:{x:3,y:0,z:-5,ry:-1,v:0}};};img.src=P[pi_].src});
 let last=performance.now(),mx=0;addEventListener('pointermove',e=>mx=e.clientX/innerWidth-.5);
 function drawIt(it,model,refl,back){const nm=new Float32Array([model[0],model[1],model[2],model[4],model[5],model[6],model[8],model[9],model[10]]);
  gl.uniformMatrix4fv(U.uM,false,model);gl.uniformMatrix3fv(U.uNM,false,nm);gl.uniform1f(U.uBack,back?1:0);gl.uniform1f(U.uRefl,refl?1:0);const m=back?it.back:it.front;gl.bindVertexArray(m.vao);gl.drawElements(gl.TRIANGLES,m.n,gl.UNSIGNED_INT,0)}
 function sframe(now){requestAnimationFrame(sframe);if(!svis){last=now;return}
  const dt=Math.min((now-last)/1000,.05);last=now;const k=1-Math.exp(-dt*4);
  const dpr=Math.min(devicePixelRatio||1,window.__aeQ||2),w=sc.clientWidth,h=sc.clientHeight;if(sc.width!==Math.round(w*dpr)||sc.height!==Math.round(h*dpr)){sc.width=Math.round(w*dpr);sc.height=Math.round(h*dpr)}
  const asp=w/h,mob=asp<1,camZ=mob?12.5:10.2,camY=-.25;
  const r=story.getBoundingClientRect();prog=clamp(-r.top/(r.height-innerHeight),0,.9999);const c=Math.floor(prog*4),q=prog*4-c;setChap(c);
  const VP=M.mul(M.persp(26*Math.PI/180,asp,.5,60),M.T(-mx*.5,-camY,-camZ));gl.viewport(0,0,sc.width,sc.height);
  gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.disable(gl.CULL_FACE);gl.enable(gl.BLEND);gl.blendFunc(gl.ONE,gl.ONE_MINUS_SRC_ALPHA);
  gl.uniformMatrix4fv(U.uVP,false,VP);gl.uniform3f(U.uCam,-mx*.5,camY,camZ);gl.uniform1f(U.uFloor,FLOOR);gl.uniform1i(U.uMap,0);gl.uniform3f(U.uL,.55+mx*1.2,.8,.7);
  const baseX=mob?0:2.3,baseY=mob?1.5:0,sca=mob?.78:1.12;
  const list=S.filter(Boolean);
  list.forEach((it,i)=>{const s=it.s,a=i===c;const g={x:baseX+(a?0:(i>c?4:-4)),z:a?0:-5,ry:a?(q-.5)*2.6+Math.sin(RM_?0:now/1800)*.15:(i>c?-1.4:1.4),v:a?1:0};for(const n in g)s[n]+=(g[n]-s[n])*k});
  const pass=refl=>list.forEach(it=>{const s=it.s;if(s.v<.02)return;const rot=M.mul(M.Ry(s.ry),M.S(sca,sca,sca));
   const m=refl?M.mul(M.T(s.x,2*FLOOR-baseY*0,s.z),M.mul(M.S(1,-1,1),rot)):M.mul(M.T(s.x,baseY+(1-sca)*-1.5,s.z),rot);
   gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,it.tex);gl.uniform3f(U.uAcc,it.acc[0]*.55,it.acc[1]*.55,it.acc[2]*.55);gl.uniform1f(U.uBright,1);gl.uniform1f(U.uAlpha,s.v);drawIt(it,m,refl,true);drawIt(it,m,refl,false)});
  gl.depthMask(false);list.forEach(it=>{const s=it.s;if(s.v<.02)return;R.shadow(VP,s.x,FLOOR+.01,s.z,1.35*sca,.95*sca,.62*s.v)});if(!mob)pass(true);gl.depthMask(true);pass(false)}
 requestAnimationFrame(sframe)}
else{sc.style.display='none'}
setChap(0);
/* scroll loop */
function tick(){const y=scrollY;hdr.classList.toggle('solid',y>40);hdr.classList.toggle('hide',y>700&&y>ly+2);if(y<ly-2)hdr.classList.remove('hide');ly=y;
 pbar.style.transform='scaleX('+(y/(document.scrollingElement.scrollHeight-innerHeight||1))+')';cx+=(tx-cx)*.12;cy+=(ty-cy)*.12;cur.style.transform='translate('+cx+'px,'+cy+'px)';requestAnimationFrame(tick)}
tick();
})();


/* ===== V3 · PRO LAYER (engine originale preservato) ===== */
(()=>{
 const $=id=>$$.getElementById(id);
 const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
 /* --- governor qualita': DPR adattivo in base ai frame reali --- */
 const lowEnd=(navigator.hardwareConcurrency||8)<=4||(navigator.deviceMemory||8)<=4;
 window.__aeQ=Math.min(devicePixelRatio||1,lowEnd?1.5:2);
 (()=>{let n=0,acc=0,last=performance.now();function g(now){const dt=now-last;last=now;if(dt<250&&!document.hidden){acc+=dt;if(++n===90){if(acc/n>26&&window.__aeQ>1)window.__aeQ=Math.max(1,window.__aeQ-.25);n=0;acc=0}}requestAnimationFrame(g)}requestAnimationFrame(g)})();
 /* --- accessibilita' canvas + perdita contesto WebGL --- */
 const cv=$('gl');if(cv){cv.setAttribute('role','group');cv.setAttribute('aria-roledescription','vetrina 3D');cv.setAttribute('tabindex','0');cv.setAttribute('aria-label','Bottiglie in 3D. Usa le frecce sinistra e destra per cambiare prodotto.');
  cv.addEventListener('webglcontextlost',e=>{e.preventDefault();cv.style.display='none';const st=$('stage');if(st&&!st.querySelector('.fb')&&typeof P!=='undefined'){const im=new Image();im.crossOrigin='anonymous';im.className='fb';im.alt='';im.src=P[0].src;im.style.cssText='position:absolute;left:50%;top:50%;height:68%;transform:translate(-50%,-50%);z-index:2';st.appendChild(im)}})}
 /* --- scroll: variabile --hp (0..1) per parallax/dissolvenza hero --- */
 const hero=$('hero');let tk=false;
 function sc(){tk=false;const h=Math.min(1,Math.max(0,scrollY/Math.max(1,innerHeight*.9)));hero.style.setProperty('--hp',h.toFixed(3))}
 addEventListener('scroll',()=>{if(!tk){tk=true;requestAnimationFrame(sc)}},{passive:true});sc();
 /* --- LIQUID MOTION: shader fluido (domain warping) nello sfondo hero --- */
 const lq=$('liq');if(!lq)return;
 const gl=lq.getContext('webgl2',{antialias:false,alpha:false,powerPreference:'low-power'});
 if(!gl){lq.style.display='none';return}
 const VS='#version 300 es\nin vec2 a;void main(){gl_Position=vec4(a,0.,1.);}';
 const FS=`#version 300 es
precision mediump float;uniform vec2 uR,uM;uniform float uT;uniform vec3 uA;out vec4 o;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<4;i++){v+=a*n(p);p=p*2.03+vec2(1.7,9.2);a*=.5;}return v;}
void main(){vec2 uv=gl_FragCoord.xy/uR;float as=uR.x/uR.y;vec2 p=(uv-.5)*vec2(as,1.)*2.4;vec2 m=(uM-.5)*vec2(as,1.)*2.4;
 float d=length(p-m);vec2 dir=normalize(p-m+1e-4);p+=dir*.22*exp(-d*1.8)*sin(d*13.-uT*2.2);
 vec2 q=vec2(fbm(p+uT*.045),fbm(p+vec2(5.2,1.3)-uT*.038));
 vec2 r=vec2(fbm(p+2.6*q+vec2(1.7,9.2)+uT*.07),fbm(p+2.6*q+vec2(8.3,2.8)-uT*.055));
 float f=fbm(p+2.6*r);
 float body=smoothstep(.38,.9,f);float rim=pow(1.-abs(sin(f*10.)),22.);float spec=pow(smoothstep(.55,1.,f),4.);
 vec3 c=uA*body*.55+uA*rim*.32+vec3(1.)*spec*.12;
 c*=.55+.45*smoothstep(.0,.9,length(uv-vec2(.45,.5))*1.2);
 float lit=exp(-d*1.4)*.35;c+=uA*lit*.5;
 o=vec4(c,1.);}`;
 function sh(t,s){const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS)){console.error(gl.getShaderInfoLog(x))}return x}
 const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,VS));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,FS));gl.linkProgram(pr);gl.useProgram(pr);
 const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);const al=gl.getAttribLocation(pr,'a');gl.enableVertexAttribArray(al);gl.vertexAttribPointer(al,2,gl.FLOAT,false,0,0);
 const U={uR:gl.getUniformLocation(pr,'uR'),uM:gl.getUniformLocation(pr,'uM'),uT:gl.getUniformLocation(pr,'uT'),uA:gl.getUniformLocation(pr,'uA')};
 const hx=c=>{c=c.trim();return[parseInt(c.slice(1,3),16)/255,parseInt(c.slice(3,5),16)/255,parseInt(c.slice(5,7),16)/255]};
 let acc=[.13,.65,.35],tg=acc.slice(),mx=.7,my=.5,tx=.7,ty=.5,vis=true,fr=0;
 hero.addEventListener('pointermove',e=>{const r=hero.getBoundingClientRect();tx=(e.clientX-r.left)/r.width;ty=1-(e.clientY-r.top)/r.height});
 new IntersectionObserver(e=>vis=e[0].isIntersecting).observe(hero);
 lq.addEventListener('webglcontextlost',e=>{e.preventDefault();lq.style.display='none'});
 function draw(now){const sc=window.__aeQ>=2?.5:.38,w=Math.max(2,Math.round(lq.clientWidth*sc)),h=Math.max(2,Math.round(lq.clientHeight*sc));
  if(lq.width!==w||lq.height!==h){lq.width=w;lq.height=h;gl.viewport(0,0,w,h)}
  if(fr++%20===0){const c=getComputedStyle($H).getPropertyValue('--accent');if(c)tg=hx(c)}
  for(let i=0;i<3;i++)acc[i]+=(tg[i]-acc[i])*.04;mx+=(tx-mx)*.06;my+=(ty-my)*.06;
  gl.uniform2f(U.uR,w,h);gl.uniform2f(U.uM,mx,my);gl.uniform1f(U.uT,now/1000);gl.uniform3f(U.uA,acc[0],acc[1],acc[2]);gl.drawArrays(gl.TRIANGLE_STRIP,0,4)}
 if(rm){draw(4000)}else{(function f(now){requestAnimationFrame(f);if(!vis||document.hidden)return;draw(now)})(0)}
})();

})();