from ae_lib import *
import ae_lib, math
from PIL import ImageDraw, Image
WHITE=(255,255,255,255); SOFT=(230,238,248,255); MUTE=(185,200,220,255); DIM=(150,170,195,255)
_old=ae_lib._icon
def _icon2(kind,S=1200):
    if kind in ('pin','drop','truck','chat'): return _old(kind,S)
    im=Image.new('RGBA',(S,S),(0,0,0,0));d=ImageDraw.Draw(im);w=int(S*0.045);c=CY+(255,)
    if kind=='book':
        d.rounded_rectangle([S*0.14,S*0.22,S*0.86,S*0.78],int(S*0.03),outline=c,width=w)
        d.line([(S*0.5,S*0.22),(S*0.5,S*0.78)],fill=c,width=w)
        for k in range(3):
            y=S*(0.38+k*0.12); d.line([(S*0.22,y),(S*0.42,y)],fill=c,width=int(w*0.7)); d.line([(S*0.58,y),(S*0.78,y)],fill=c,width=int(w*0.7))
    elif kind=='globe':
        d.ellipse([S*0.14,S*0.14,S*0.86,S*0.86],outline=c,width=w)
        d.ellipse([S*0.34,S*0.14,S*0.66,S*0.86],outline=c,width=int(w*0.8))
        d.line([(S*0.14,S*0.5),(S*0.86,S*0.5)],fill=c,width=int(w*0.8))
        d.arc([S*0.18,S*0.26,S*0.82,S*0.74],200,340,fill=c,width=int(w*0.7)); d.arc([S*0.18,S*0.26,S*0.82,S*0.74],20,160,fill=c,width=int(w*0.7))
    elif kind=='return':
        d.arc([S*0.18,S*0.22,S*0.82,S*0.78],40,340,fill=c,width=w)
        d.polygon([(S*0.70,S*0.12),(S*0.88,S*0.30),(S*0.60,S*0.34)],fill=c)
    elif kind=='check':
        d.ellipse([S*0.12,S*0.12,S*0.88,S*0.88],outline=c,width=w)
        d.line([(S*0.30,S*0.52),(S*0.45,S*0.67),(S*0.72,S*0.36)],fill=c,width=int(w*1.3),joint='curve')
    elif kind=='clock':
        d.ellipse([S*0.12,S*0.12,S*0.88,S*0.88],outline=c,width=w)
        d.line([(S*0.5,S*0.5),(S*0.5,S*0.26)],fill=c,width=w); d.line([(S*0.5,S*0.5),(S*0.68,S*0.60)],fill=c,width=w)
    return im
ae_lib._icon=_icon2
def wrap(txt,f,maxw):
    d=ImageDraw.Draw(Image.new('RGBA',(10,10)));words=txt.split();lines=[];cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur);cur=w
    if cur: lines.append(cur)
    return lines
def paragraph(img,txt,y,f,fill,maxw=860,lh=1.45):
    for ln in wrap(txt,f,maxw):
        ctext(img,ln,y,f,fill);y+=int(f.size*lh)
    return y
def _slide(_off=0,sc=1.0,W=1080,H=1350,top=30,logo_w=440,icon=None,lines=(),big=None,body=None,body2=None,chips=(),cta=None,foot=None,n=None,i=None,seed=3,logo_top=None,cover=False):
    floor=1180 if H==1350 else 1700
    img=background(W,H,glows=((0.5,0.55,0.55,0.35,0.22),),seed=seed,floor=floor)
    lt=logo_top if logo_top is not None else (120 if cover else top)
    img,lb=add_logo(img,width=720 if cover else logo_w,top=lt)
    y=lb+60+_off
    if icon:
        img=icon_ring(img,icon,W//2,lb+190+_off,125);y=lb+370+_off
    for txt,col,size in lines:
        size=int(size*sc);f=font('Bold',size);ctext(img,txt,y,f,col);y+=int(size*1.18)
    if big:
        txt,size=big;size=int(size*sc);img=glow_text(img,txt,y+6,font('Bold',size),fill=CY+(255,),glow=CY,blur=22);y+=int(size*1.3)
    y+=14
    if body: y=paragraph(img,body,y,font('Medium',int(42*sc)),SOFT,maxw=int(860))+8
    if body2:
        for part in body2.split('\n'): y=paragraph(img,part,y,font('Regular',int(36*sc)),MUTE)
        y+=8
    if chips:
        f=font('Medium',int(32*sc))
        for c in chips:
            img=chip(img,W/2,y,c,f);y+=int(84*sc)
    if cta: ctext(img,cta,y+10,font('Bold',46),CY+(255,))
    if n: img=dots(img,n,i,floor+70)
    ctext(img,foot or 'autoevostore.it',floor+110,font('Regular',26),DIM)
    return img.convert('RGB'),y,lb,floor

def slide(**k):
    _,y,lb,floor=_slide(0,**k)
    avail=floor-60-(lb+60); used=y-(lb+60)
    off=max(0,int((avail-used)*0.5))
    img,_,_,_=_slide(off,**k)
    return img
