"""Layout con foto reali dei flaconi (products/*.png, ritagli RGBA).
Formati: feed 1080x1350 (W,H), storia 1080x1920. Solo logo, font e foto del repo."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from ae_lib import ROOT, CY, font, background, add_logo, ctext, glow_text, chip, dots
from ae_slides import wrap, paragraph

PR=ROOT+'/products'
OUT=ROOT+'/media'
WHITE=(245,248,252,255); SOFT=(170,190,210,255); GOLD=(255,208,110,255)

def photo(key,h):
    im=Image.open(f'{PR}/{key}.png').convert('RGBA')
    return im.resize((max(1,int(im.width*h/im.height)),h),Image.LANCZOS)

def place(img,key,cx,bottom,h,glow=True,reflect=True,tilt=0):
    """Mette il flacone centrato in cx con base a `bottom`, alto h."""
    W,H=img.size; ph=photo(key,h)
    if tilt: ph=ph.rotate(tilt,resample=Image.BICUBIC,expand=True)
    x=int(cx-ph.width/2); y=int(bottom-ph.height)
    if glow:
        g=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(g)
        rx,ry=ph.width*0.95,ph.height*0.62
        d.ellipse([cx-rx,y+ph.height*0.5-ry,cx+rx,y+ph.height*0.5+ry],fill=CY+(70,))
        img=Image.alpha_composite(img,g.filter(ImageFilter.GaussianBlur(70)))
    # ombra a terra
    sh=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(sh).ellipse([cx-ph.width*0.55,bottom-18,cx+ph.width*0.55,bottom+26],fill=(0,0,0,170))
    img=Image.alpha_composite(img,sh.filter(ImageFilter.GaussianBlur(16)))
    if reflect:
        rf=ph.transpose(Image.FLIP_TOP_BOTTOM); rh=int(ph.height*0.22); rf=rf.crop((0,0,rf.width,rh))
        a=np.asarray(rf.split()[3]).astype(np.float32)*np.linspace(0.32,0,rh)[:,None]
        rf.putalpha(Image.fromarray(a.astype('uint8')))
        rl=Image.new('RGBA',(W,H),(0,0,0,0)); rl.paste(rf,(x,int(bottom)+4),rf)
        img=Image.alpha_composite(img,rl)
    pl=Image.new('RGBA',(W,H),(0,0,0,0)); pl.paste(ph,(x,y),ph)
    return Image.alpha_composite(img,pl)

def base(W,H,logo_w=460,glows=None,seed=5):
    glows=glows or ((0.5,0.55,0.55,0.4,0.20),)
    img=background(W,H,glows=glows,seed=seed)
    img,bot=add_logo(img,logo_w,top=int(H*0.03) if H<1500 else 110)
    return img,bot

def title(img,lines,y,size=74,fill=WHITE,gap=1.12,align='c',x=None,glow=True):
    f=font('Bold',size)
    for ln in lines:
        if align=='c':
            img=glow_text(img,ln,y,f,fill=fill,blur=22) if glow else (ctext(img,ln,y,f,fill) or img)
        else:
            ImageDraw.Draw(img).text((x,y),ln,font=f,fill=fill)
        y+=int(size*gap*1.15)
    return img,y

def kicker(img,txt,y,size=34):
    f=font('Medium',size); W=img.width
    d=ImageDraw.Draw(img); t=txt.upper(); w=d.textlength(t,font=f)+len(t)*5
    x=(W-w)/2
    for ch in t:
        d.text((x,y),ch,font=f,fill=CY+(255,)); x+=d.textlength(ch,font=f)+5
    return img

def foot(img,txt='autoevostore.it  ·  link in bio',y=None,size=32):
    H=img.height; y=y if y is not None else H-92
    ctext(img,txt,y,font('Medium',size),SOFT); return img

def chips_row(img,items,y,size=30,h=62):
    f=font('Medium',size); d=ImageDraw.Draw(img); W=img.width
    ws=[d.textlength(t,font=f)+56 for t in items]; gap=18
    tot=sum(ws)+gap*(len(items)-1); x=(W-tot)/2
    for t,w in zip(items,ws):
        img=chip(img,x+w/2,y,t,f,pad=28,h=h); x+=w+gap
    return img

def save(img,path):
    os.makedirs(os.path.dirname(f'{OUT}/{path}'),exist_ok=True)
    img.convert('RGB').save(f'{OUT}/{path}',optimize=True)
    return f'media/{path}'

# ---------------------------------------------------------------- layout
def hero(key,kick,lines,chips=(),W=1080,H=1350,bottle_h=None,fonts=74,sub=None):
    """Flacone grande al centro, titolo sopra, chip sotto."""
    story=H>1500
    img,y=base(W,H,logo_w=520 if story else 440)
    y=y+34
    img=kicker(img,kick,y); y+=64
    img,y=title(img,lines,y,size=fonts)
    if sub:
        y+=4; paragraph(img,sub,y,font('Regular',34),SOFT,maxw=860);
    bh=bottle_h or int(H*0.50)
    bottom=H-(200 if not chips else 270) if not story else H-340
    bh=min(bh,bottom-y-50)
    img=place(img,key,W//2,bottom,bh)
    if chips: img=chips_row(img,chips,bottom+(44 if not story else 56))
    return foot(img)

def split(key,kick,lines,bullets,W=1080,H=1350,fonts=64):
    """Flacone a sinistra, testo a destra."""
    story=H>1500
    img,y=base(W,H,logo_w=480 if not story else 540,glows=((0.28,0.55,0.4,0.4,0.24),))
    bottom=H-(200 if not story else 340); bh=int(H*0.62) if not story else int(H*0.56)
    pw=photo(key,100); bh=min(bh,int(W*0.40*100/pw.width))
    img=place(img,key,int(W*0.26),bottom,bh)
    x=int(W*0.50); ty=y+50
    d=ImageDraw.Draw(img)
    f=font('Medium',30); d.text((x,ty),kick.upper(),font=f,fill=CY+(255,)); ty+=62
    for ln in lines:
        d.text((x,ty),ln,font=font('Bold',fonts),fill=WHITE); ty+=int(fonts*1.25)
    ty+=26
    fb=font('Regular',34)
    for b in bullets:
        for i,l in enumerate(wrap(b,fb,W-x-60)):
            if i==0: d.ellipse([x,ty+14,x+14,ty+28],fill=CY+(255,))
            d.text((x+34,ty),l,font=fb,fill=(225,235,245,255)); ty+=int(34*1.4)
        ty+=14
    return foot(img)

def duo(keyA,keyB,kick,lines,capA,capB,W=1080,H=1350,fonts=70):
    """Due flaconi affiancati con didascalie (confronto)."""
    story=H>1500
    img,y=base(W,H,logo_w=460 if not story else 540,glows=((0.28,0.6,0.35,0.35,0.2),(0.72,0.6,0.35,0.35,0.2)))
    y=y+34
    img=kicker(img,kick,y); y+=64
    img,y=title(img,lines,y,size=fonts)
    bottom=H-(250 if not story else 380); bh=min(int(H*0.46),bottom-y-40)
    img=place(img,keyA,int(W*0.28),bottom,bh); img=place(img,keyB,int(W*0.72),bottom,bh)
    f=font('Medium',30)
    for cx,cap in ((int(W*0.28),capA),(int(W*0.72),capB)):
        for j,l in enumerate(cap):
            ctext_at(img,l,cx,bottom+46+j*44,f if j else font('Bold',34),WHITE if j==0 else SOFT)
    return foot(img)

def ctext_at(img,txt,cx,y,f,fill):
    d=ImageDraw.Draw(img); w=d.textlength(txt,font=f); d.text((cx-w/2,y),txt,font=f,fill=fill)

def lineup(keys,kick,lines,cap=None,W=1080,H=1350,fonts=70):
    """Fila di 3-4 flaconi della stessa altezza."""
    story=H>1500
    img,y=base(W,H,logo_w=460 if not story else 540)
    y=y+34
    img=kicker(img,kick,y); y+=64
    img,y=title(img,lines,y,size=fonts)
    n=len(keys); bottom=H-(240 if not story else 340); bh=min(int(H*0.40),bottom-y-40,int(W/n*0.9/0.52))
    for i,k in enumerate(keys):
        img=place(img,k,int(W*(i+0.5)/n),bottom,bh,glow=False,reflect=True)
    if cap: ctext(img,cap,bottom+52,font('Medium',34),SOFT)
    return foot(img)

def text_slide(kick,lines,body=None,key=None,W=1080,H=1350,fonts=72,bullets=(),chips=()):
    """Slide di testo con piccolo flacone ancorato in basso (opzionale)."""
    story=H>1500
    img,y=base(W,H,logo_w=460 if not story else 540,glows=((0.5,0.78,0.6,0.35,0.22),))
    y=y+40
    img=kicker(img,kick,y); y+=70
    img,y=title(img,lines,y,size=fonts); y+=18
    if body:
        y=paragraph(img,body,y,font('Regular',38),(220,232,244,255),maxw=900) or y
    fb=font('Regular',38); d=ImageDraw.Draw(img)
    for b in bullets:
        for i,l in enumerate(wrap(b,fb,860)):
            if i==0: d.ellipse([110,y+17,126,y+33],fill=CY+(255,))
            d.text((150,y),l,font=fb,fill=(225,235,245,255)); y+=54
        y+=18
    if chips: img=chips_row(img,chips,(H-300) if not story else (H-420))
    if key: img=place(img,key,W//2,H-170 if not story else H-330,min(int(H*0.38),(H-170 if not story else H-330)-y-30))
    return foot(img)

def bigspec(key,spec,kick,lines,chips=(),W=1080,H=1350,tilt=-6,fonts=60):
    """Scritta gigante della viscosità dietro al flacone leggermente inclinato."""
    story=H>1500
    img,y=base(W,H,logo_w=460 if not story else 540,glows=((0.5,0.6,0.6,0.4,0.22),))
    # watermark
    sz=330
    while ImageDraw.Draw(Image.new('RGBA',(5,5))).textlength(spec,font=font('Bold',sz))>W*0.94: sz-=10
    fw=font('Bold',sz)
    wm=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(wm)
    tw=d.textlength(spec,font=fw); cy=int(H*0.50 if not story else H*0.46)
    d.text(((W-tw)/2,cy-190),spec,font=fw,fill=(255,255,255,30))
    img=Image.alpha_composite(img,wm)
    y=y+34; img=kicker(img,kick,y); y+=64
    img,y=title(img,lines,y,size=fonts)
    bottom=H-(270 if chips else 200) if not story else H-340
    bh=min(int(H*0.56),bottom-y-30)
    img=place(img,key,W//2,bottom,bh,tilt=tilt)
    if chips: img=chips_row(img,chips,bottom+(40 if not story else 52))
    return foot(img)
