"""Storie 'pubblicitarie' (1080x1920): titolo grande a sinistra, parola chiave in ciano, flacone grande inclinato, pannello vetro in basso."""
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from photo_lib import *
from PIL import ImageFilter

def glass(img,box,r=36,alpha=120):
    W,H=img.size; x0,y0,x1,y1=box
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.rounded_rectangle(box,r,fill=(8,22,40,alpha),outline=CY+(110,),width=2)
    return Image.alpha_composite(img,lay)

def story_pro(key,kick,head,accent,body,chips=(),mark=None,tilt=-7,W=1080,H=1920,hsize=104):
    img,y=base(W,H,logo_w=500,glows=((0.62,0.52,0.7,0.5,0.30),))
    d=ImageDraw.Draw(img)
    # scritta gigante di sfondo, ruotata
    if mark:
        sz=520
        while d.textlength(mark,font=font('Bold',sz))>W*1.05: sz-=10
        wm=Image.new('RGBA',(W*2,sz*2),(0,0,0,0)); ImageDraw.Draw(wm).text((W//2,sz//2),mark,font=font('Bold',sz),fill=(255,255,255,40))
        wm=wm.rotate(90,expand=True) if False else wm
        lay=Image.new('RGBA',(W,H),(0,0,0,0)); lay.paste(wm,(-W//2+int(W*0.0),int(H*0.40)),wm); img=Image.alpha_composite(img,lay)
    # kicker con barra
    x=80; y=int(H*0.205)
    d=ImageDraw.Draw(img); d.rounded_rectangle([x,y+14,x+70,y+22],4,fill=CY+(255,))
    d.text((x+96,y-6),kick.upper(),font=font('Medium',40),fill=CY+(255,))
    y+=78
    # titolo a sinistra
    fh=font('Bold',hsize)
    for ln in head:
        img=glow_text_left(img,ln,x,y,fh,WHITE); y+=int(hsize*1.08)
    fa=font('Bold',int(hsize*1.12))
    img=glow_text_left(img,accent,x,y,fa,CY+(255,)); y+=int(hsize*1.30)
    # flacone grande
    bottom=H-560; bh=min(820,bottom-y-20)
    img=place(img,key,int(W*0.60),bottom,bh,tilt=tilt)
    # pannello vetro con testo
    top=H-520; img=glass(img,(60,top,W-60,H-150))
    yy=paragraph(img,body,top+34,font('Regular',44),(236,243,250,255),maxw=W-200,align='l',x=100) if False else None
    yy=paragraph_left(img,body,100,top+36,font('Regular',42),(236,243,250,255),W-200)
    if chips: img=chips_row(img,chips,H-262,size=30,h=62)
    return foot(img,y=H-108)

def glow_text_left(img,txt,x,y,f,fill):
    W,H=img.size; g=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(g).text((x,y),txt,font=f,fill=CY+(120,))
    img=Image.alpha_composite(img,g.filter(ImageFilter.GaussianBlur(20)))
    ImageDraw.Draw(img).text((x,y),txt,font=f,fill=fill); return img

def paragraph_left(img,txt,x,y,f,fill,maxw,gap=1.38):
    d=ImageDraw.Draw(img); words=txt.split(); line=''; 
    for w in words:
        t=(line+' '+w).strip()
        if d.textlength(t,font=f)>maxw and line:
            d.text((x,y),line,font=f,fill=fill); y+=int(f.size*gap); line=w
        else: line=t
    if line: d.text((x,y),line,font=f,fill=fill); y+=int(f.size*gap)
    return y

if __name__=='__main__':
    im=story_pro('opel_gm_dexos2_1l','Lo sapevi?',['Dexos è una'],'specifica GM.',
        'Se il libretto richiede dexos2 o dexos D, la stessa dicitura deve comparire in etichetta.',
        chips=('Opel GM Dexos2','5W-30'),mark='DEXOS',tilt=-4)
    p=save(im,'test/st_prova_dexos.jpg'); print(p)
