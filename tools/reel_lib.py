"""Reel verticali 1080x1920 con foto reali: frame PIL + ffmpeg.
Uso: python3 tools/reel_lib.py  (genera media/reels/*.mp4 e la copertina .jpg)"""
import os, subprocess, shutil, math, sys
sys.path.insert(0,os.path.dirname(__file__))
from photo_lib import *

W,H,FPS=1080,1920,30
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def seg(t,a,b): return (t-a)/(b-a)

def sprite(key,h):
    """Flacone con ombra e riflesso su canvas trasparente. Ritorna (img, cx_off, bottom_off)."""
    ph=photo(key,h); sw,sh=ph.width+500,h+420
    cv=Image.new('RGBA',(sw,sh),(0,0,0,0))
    cv=place(cv,key,sw//2,h+170,h,glow=True,reflect=True)
    return cv,sw//2,h+170

def text_layer(txt,size,weight='Bold',fill=WHITE,w=W):
    f=font(weight,size); d=ImageDraw.Draw(Image.new('RGBA',(5,5)))
    lines=txt.split('\n'); lh=int(size*1.25)
    im=Image.new('RGBA',(w,lh*len(lines)+20),(0,0,0,0)); dd=ImageDraw.Draw(im)
    for i,l in enumerate(lines):
        tw=dd.textlength(l,font=f); dd.text(((w-tw)/2,i*lh),l,font=f,fill=fill)
    return im

def chip_layer(txt,size=36):
    f=font('Medium',size); d=ImageDraw.Draw(Image.new('RGBA',(5,5))); tw=int(d.textlength(txt,font=f))+64
    im=Image.new('RGBA',(tw+20,90),(0,0,0,0))
    ImageDraw.Draw(im).rounded_rectangle([8,8,tw+8,80],36,fill=(255,255,255,22),outline=CY+(200,),width=3)
    ImageDraw.Draw(im).text((8+32,8+(72-size)/2-6),txt,font=f,fill=(235,242,250,255))
    return im

def with_alpha(im,a):
    if a>=1: return im
    im=im.copy(); al=im.split()[3].point(lambda v:int(v*max(0,a))); im.putalpha(al); return im

def paste(bg,im,x,y,a=1.0):
    im=with_alpha(im,a); bg.alpha_composite(im,(int(x),int(y))) if 0<=x and 0<=y and x+im.width<=bg.width and y+im.height<=bg.height else bg.paste(im,(int(x),int(y)),im)

def render(name,dur,frame_fn,bg):
    d=f'/tmp/reel_{name}'; shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    n=int(dur*FPS)
    for i in range(n):
        fr=bg.copy(); frame_fn(fr,i/FPS)
        fr.convert('RGB').save(f'{d}/f{i:04d}.jpg',quality=93)
    out=f'{OUT}/reels/{name}.mp4'; os.makedirs(os.path.dirname(out),exist_ok=True)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{d}/f%04d.jpg','-f','lavfi','-t',str(dur),'-i','anullsrc=r=44100:cl=stereo',
        '-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',out],check=True)
    fr=Image.open(f'{d}/f{int(1.3*FPS):04d}.jpg'); fr.save(f'{OUT}/reels/{name}.jpg',quality=90)
    shutil.rmtree(d); return out

def stage():
    img,bot=base(W,H,logo_w=560)
    return img,bot

# ---------------------------------------------------------------- Reel A: due 5W-40
def reel_a():
    bg,lb=stage(); bg=bg.convert('RGBA')
    f=font('Medium',32)
    foot(bg)
    sA,cxA,boA=sprite('petronas_prime_av',720); sB,cxB,boB=sprite('selenia_k_pure_energy_5w40',720)
    t1=text_layer('Non tutti i 5W-40\nsono uguali.',92); t2=text_layer('Cambia l’omologazione,\nnon il grado.',64,'Medium',SOFT)
    nA=text_layer('Petronas Syntium Prime AV',48); nB=text_layer('Selenia K Pure Energy',48)
    cA=[chip_layer(x) for x in ('ACEA C3','MB 229.51','VW 505.01')]; cB=[chip_layer(x) for x in ('ACEA C3','FIAT 9.55535-S2')]
    e1=text_layer('Controlla quella\ndel tuo libretto.',84); e2=text_layer('Targa, modello e anno in DM:\nverifichiamo noi la specifica giusta.',46,'Medium',SOFT)
    e3=text_layer('autoevostore.it  ·  link in bio',40,'Medium',CY+(255,))
    ybot=1370
    def fn(fr,t):
        if t<2.8:
            a=ease(seg(t,0.1,0.8))*(1-ease(seg(t,2.3,2.8)))
            paste(fr,t1,0,640+int(30*(1-ease(seg(t,0.1,0.8)))),a);
            paste(fr,t2,0,980,ease(seg(t,0.9,1.5))*(1-ease(seg(t,2.3,2.8))))
        if 2.6<=t<6.4:
            u=ease(seg(t,2.6,3.4)); a=1-ease(seg(t,6.0,6.4))
            paste(fr,sA,540-cxA+int(-500*(1-u)),ybot-boA,a*u)
            paste(fr,nA,0,ybot+60,ease(seg(t,3.2,3.8))*a)
            for i,c in enumerate(cA): paste(fr,c,540-c.width//2,ybot+130+i*92,ease(seg(t,3.8+i*0.5,4.2+i*0.5))*a)
        if 6.2<=t<10.0:
            u=ease(seg(t,6.2,7.0)); a=1-ease(seg(t,9.6,10.0))
            paste(fr,sB,540-cxB+int(500*(1-u)),ybot-boB,a*u)
            paste(fr,nB,0,ybot+60,ease(seg(t,6.8,7.4))*a)
            for i,c in enumerate(cB): paste(fr,c,540-c.width//2,ybot+130+i*92,ease(seg(t,7.4+i*0.5,7.8+i*0.5))*a)
        if t>=9.8:
            a=ease(seg(t,9.8,10.5))
            paste(fr,e1,0,700,a); paste(fr,e2,0,1010,ease(seg(t,10.4,11.0))); paste(fr,e3,0,1250,ease(seg(t,11.0,11.6)))
    return render('reel_5w40',13.0,fn,bg)

# ---------------------------------------------------------------- Reel C: leggere l'etichetta
def reel_c():
    bg,lb=stage(); bg=bg.convert('RGBA'); foot(bg)
    s,cx,bo=sprite('mobil1_esp_5w30',500)
    t1=text_layer('Come leggere\nun’etichetta.',96)
    items=[('5W-30','Viscosità: come scorre l’olio'),('ACEA C3','Categoria: per motori con DPF/FAP'),('BMW LL-04 · MB 229.52','Omologazioni del costruttore')]
    cards=[]
    for big,small in items:
        im=Image.new('RGBA',(W,200),(0,0,0,0)); d=ImageDraw.Draw(im)
        d.rounded_rectangle([90,10,W-90,190],40,fill=(255,255,255,22),outline=CY+(200,),width=3)
        fb=font('Bold',56 if len(big)<12 else 46); d.text((140,28),big,font=fb,fill=WHITE)
        d.text((140,112),small,font=font('Regular',34),fill=SOFT); cards.append(im)
    e1=text_layer('Dubbi? Scrivici\ntarga e modello.',84); e3=text_layer('autoevostore.it  ·  link in bio',40,'Medium',CY+(255,))
    e2=text_layer('Verifichiamo noi la specifica giusta.',44,'Medium',SOFT)
    def fn(fr,t):
        if t<2.4:
            a=ease(seg(t,0.1,0.8))*(1-ease(seg(t,2.0,2.4))); paste(fr,t1,0,700,a)
        if 2.2<=t<11.0:
            u=ease(seg(t,2.2,3.0)); a=1-ease(seg(t,10.6,11.0))
            paste(fr,s,540-cx,1670-bo+int(260*(1-u)),a*u)
            for i,c in enumerate(cards):
                st=3.4+i*2.3; paste(fr,c,int(90*(1-ease(seg(t,st,st+0.6)))),415+i*215,ease(seg(t,st,st+0.6))*a)
        if t>=10.8:
            paste(fr,e1,0,700,ease(seg(t,10.8,11.5))); paste(fr,e2,0,1010,ease(seg(t,11.4,12.0))); paste(fr,e3,0,1200,ease(seg(t,12.0,12.6)))
    return render('reel_etichetta',14.0,fn,bg)

# ---------------------------------------------------------------- Reel B: marchi
def reel_b():
    bg,lb=stage(); bg=bg.convert('RGBA'); foot(bg)
    seq=[('castrol_edge_0w20_c5','Castrol EDGE 0W-20 C5'),('mobil1_esp_5w30','Mobil 1 ESP 5W-30'),('total_ineo_mc3','TotalEnergies Quartz Ineo MC3'),
         ('petronas_prime_av','Petronas Syntium Prime AV'),('selenia_wr_forward_0w30','Selenia WR Forward 0W-30'),('mannol_longlife_504_507','MANNOL Longlife 504/507'),('castrol_transmax_axle_80w90','Castrol Transmax Axle EPX')]
    sp=[sprite(k,760) for k,_ in seq]; nm=[text_layer(n,50) for _,n in seq]
    t1=text_layer('Marchi originali.\nUn solo ordine.',92)
    e1=text_layer('Scegli per specifica,\nnon per nome.',84); e2=text_layer('Targa e modello in DM: verifichiamo noi.',44,'Medium',SOFT)
    e3=text_layer('autoevostore.it  ·  link in bio',40,'Medium',CY+(255,))
    D=1.6; T0=2.6
    def fn(fr,t):
        if t<2.4: paste(fr,t1,0,700,ease(seg(t,0.1,0.8))*(1-ease(seg(t,2.0,2.4))))
        for i,(s,cx,bo) in enumerate(sp):
            a0=T0+i*D
            if a0-0.1<=t<a0+D+0.3:
                u=ease(seg(t,a0,a0+0.5)); o=1-ease(seg(t,a0+D-0.2,a0+D+0.25))
                paste(fr,s,540-cx+int(420*(1-u))-int(420*(1-o)),1500-bo,u*o)
                paste(fr,nm[i],0,1560,ease(seg(t,a0+0.3,a0+0.7))*o)
        te=T0+len(sp)*D
        if t>=te:
            paste(fr,e1,0,700,ease(seg(t,te,te+0.7))); paste(fr,e2,0,1010,ease(seg(t,te+0.6,te+1.2))); paste(fr,e3,0,1200,ease(seg(t,te+1.2,te+1.8)))
    return render('reel_marchi',T0+len(sp)*D+3.2,fn,bg)

if __name__=='__main__':
    which=sys.argv[1:] or ['a','c','b']
    for w in which: print(dict(a=reel_a,b=reel_b,c=reel_c)[w]())
