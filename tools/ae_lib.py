import numpy as np, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F=ROOT+'/assets/fonts/Poppins-%s.ttf'
LOGO=ROOT+'/assets/logo.png'
CY=(0,200,230)
def font(w,s): return ImageFont.truetype(F%w,s)
def background(W,H,glows=((0.5,0.5,0.5,0.4,0.22),),seed=7,floor=None):
    y=np.linspace(0,1,H)[:,None,None]
    top=np.array([4,9,22]);mid=np.array([6,28,44]);bot=np.array([3,8,18])
    g=np.where(y<0.62, top+(mid-top)*(y/0.62), mid+(bot-mid)*((y-0.62)/0.38))
    bg=np.repeat(g,W,axis=1).astype(np.float32)
    yy,xx=np.mgrid[0:H,0:W]
    for cx,cy,rx,ry,amp in glows:
        d=((xx-cx*W)/(rx*W))**2+((yy-cy*H)/(ry*H))**2
        bg+=(np.exp(-d*2.2)*amp)[...,None]*np.array(CY,np.float32)
    img=Image.fromarray(np.clip(bg,0,255).astype(np.uint8)).convert('RGBA')
    random.seed(seed)
    sp=Image.new('RGBA',(W,H),(0,0,0,0));sd=ImageDraw.Draw(sp)
    for _ in range(60):
        x=random.randint(20,W-20);yv=random.randint(int(H*0.2),int(H*0.8));r=random.choice([1,1,2,2,3])
        c=random.choice([(255,220,120),(120,230,255),(255,255,255)])
        sd.ellipse([x-r,yv-r,x+r,yv+r],fill=c+(random.randint(90,200),))
    img=Image.alpha_composite(img,sp.filter(ImageFilter.GaussianBlur(0.8)))
    if floor:
        fl=Image.new('RGBA',(W,H),(0,0,0,0));ImageDraw.Draw(fl).rectangle([0,floor,W,floor+2],fill=CY+(170,))
        img=Image.alpha_composite(img,fl.filter(ImageFilter.GaussianBlur(10)));img=Image.alpha_composite(img,fl)
    return img
def add_logo(img,width=600,top=36):
    W,H=img.size
    logo=Image.open(LOGO).convert('RGBA').crop((130,240,1450,880))
    lh=int(width*640/1320);logo=logo.resize((width,lh),Image.LANCZOS)
    cx=W//2;cy=top+lh//2
    haze=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(haze).ellipse([cx-width*0.57,cy-lh//2-30,cx+width*0.57,cy+lh//2+30],fill=(150,175,210,95))
    img=Image.alpha_composite(img,haze.filter(ImageFilter.GaussianBlur(38)))
    lg=Image.new('RGBA',(W,H),(0,0,0,0));lg.paste(logo,(cx-width//2,top),logo)
    return Image.alpha_composite(img,lg),top+lh
def ctext(img,txt,y,f,fill):
    d=ImageDraw.Draw(img);w=d.textlength(txt,font=f);d.text(((img.width-w)/2,y),txt,font=f,fill=fill)
def glow_text(img,txt,y,f,fill=(255,255,255,255),glow=CY,blur=26):
    W,H=img.size;d=ImageDraw.Draw(img);w=d.textlength(txt,font=f)
    gl=Image.new('RGBA',(W,H),(0,0,0,0));ImageDraw.Draw(gl).text(((W-w)/2,y),txt,font=f,fill=glow+(255,))
    img=Image.alpha_composite(img,gl.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).text(((W-w)/2,y),txt,font=f,fill=fill);return img
def chip(img,cx,y,txt,f,pad=28,h=64):
    d=ImageDraw.Draw(img);w=d.textlength(txt,font=f)+2*pad
    layer=Image.new('RGBA',img.size,(0,0,0,0))
    ImageDraw.Draw(layer).rounded_rectangle([cx-w/2,y,cx+w/2,y+h],h//2,fill=(255,255,255,18),outline=CY+(190,),width=3)
    img=Image.alpha_composite(img,layer);d=ImageDraw.Draw(img)
    d.text((cx-w/2+pad,y+(h-f.size)/2-4),txt,font=f,fill=(235,242,250,255));return img
def dots(img,n,i,y):
    W=img.size[0];d=ImageDraw.Draw(img);gap=34;x0=W/2-(n-1)*gap/2
    for k in range(n):
        r=9 if k==i else 6
        d.ellipse([x0+k*gap-r,y-r,x0+k*gap+r,y+r],fill=CY+(255,) if k==i else (90,110,135,255))
    return img

import math
def _icon(kind,S=1200):
    im=Image.new('RGBA',(S,S),(0,0,0,0));d=ImageDraw.Draw(im);w=int(S*0.045);c=CY+(255,)
    if kind=='pin':
        cx,cy,r=S/2,S*0.40,S*0.24
        d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=c,width=w)
        d.line([(cx-r*0.93,cy+r*0.37),(cx,S*0.86),(cx+r*0.93,cy+r*0.37)],fill=c,width=w,joint='curve')
        d.ellipse([cx-r*0.42,cy-r*0.42,cx+r*0.42,cy+r*0.42],outline=c,width=w)
    elif kind=='drop':
        cx=S/2;pts=[]
        for t in np.linspace(0,1,80):
            a=t*2*math.pi
            x=cx+S*0.30*math.sin(a)*(1-math.cos(a))/1.2*1.0
            y=S*0.50-S*0.34*math.cos(a)*1.0+S*0.0
            pts.append((x,y))
        # teardrop: circle bottom + point on top
        pts=[(cx,S*0.12)]
        for ang in np.linspace(-0.55,math.pi+0.55,60):
            pts.append((cx+S*0.27*math.cos(ang+math.pi/2*0)*(-1 if False else 1)*1,S*0.60+S*0.27*math.sin(ang)))
        pts=[(cx,S*0.10)]+[(cx+S*0.27*math.sin(a),S*0.62-S*0.27*math.cos(a)) for a in np.linspace(math.pi*0.62,math.pi*2-math.pi*0.62,70)[::-1]]+[(cx,S*0.10)]
        d.line(pts,fill=c,width=w,joint='curve')
        d.arc([cx-S*0.12,S*0.50,cx+S*0.12,S*0.74],20,100,fill=c,width=int(w*0.7))
    elif kind=='truck':
        d.rounded_rectangle([S*0.10,S*0.28,S*0.60,S*0.64],int(S*0.03),outline=c,width=w)
        d.line([(S*0.60,S*0.40),(S*0.80,S*0.40),(S*0.90,S*0.53),(S*0.90,S*0.64),(S*0.60,S*0.64)],fill=c,width=w,joint='curve')
        for x in (S*0.28,S*0.74):
            d.ellipse([x-S*0.075,S*0.62,x+S*0.075,S*0.77],fill=(5,15,28,255),outline=c,width=w)
        for k,ln in enumerate((0.34,0.50)): d.line([(S*0.02,S*(0.35+k*0.12)),(S*0.08,S*(0.35+k*0.12))],fill=c,width=int(w*0.8))
    elif kind=='chat':
        d.rounded_rectangle([S*0.12,S*0.20,S*0.88,S*0.66],int(S*0.10),outline=c,width=w)
        d.line([(S*0.30,S*0.66),(S*0.26,S*0.84),(S*0.46,S*0.66)],fill=c,width=w,joint='curve')
        for x in (0.34,0.50,0.66): d.ellipse([S*x-S*0.035,S*0.43-S*0.035,S*x+S*0.035,S*0.43+S*0.035],fill=c)
    return im
def icon_ring(img,kind,cx,cy,R=170):
    W,H=img.size;S=1200
    ic=_icon(kind,S).resize((int(R*1.55),int(R*1.55)),Image.LANCZOS)
    lay=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(lay)
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=(0,200,230,22),outline=CY+(210,),width=4)
    d.ellipse([cx-R-24,cy-R-24,cx+R+24,cy+R+24],outline=CY+(70,),width=2)
    lay.paste(ic,(int(cx-ic.width/2),int(cy-ic.height/2)),ic)
    g=lay.filter(ImageFilter.GaussianBlur(22))
    img=Image.alpha_composite(img,g);img=Image.alpha_composite(img,g);return Image.alpha_composite(img,lay)
