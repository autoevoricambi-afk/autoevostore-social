import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ae_slides import *
from PIL import Image, ImageDraw
W,H=1080,1350
CYc=CY+(255,)
OUT=ROOT+'/media/2026-10'
os.makedirs(OUT,exist_ok=True)
def story(**k): return slide(W=1080,H=1920,logo_w=560,logo_top=130,sc=1.25,**k)
def add_brt(img, cy, scale=1.0):
    """White card with the BRT logo centered at y=cy."""
    b=Image.open(ROOT+'/assets/brt_logo.png').convert('RGBA')
    bg=Image.new('RGBA',b.size,(255,255,255,255)); bg.alpha_composite(b); b=bg.convert('RGB')
    import numpy as np
    a=np.array(b).astype(int); nz=np.argwhere((255*3-a.sum(axis=2))>40); y0,x0=nz.min(0); y1,x1=nz.max(0)
    b=b.crop((x0,y0,x1+1,y1+1)).convert('RGBA')
    bw=int(360*scale); bh=int(b.height*bw/b.width)
    b=b.resize((bw,bh),Image.LANCZOS)
    cw,ch=bw+90,bh+60
    card=Image.new('RGBA',(cw,ch),(255,255,255,255))
    m=Image.new('L',(cw,ch),0); ImageDraw.Draw(m).rounded_rectangle([0,0,cw-1,ch-1],radius=36,fill=255)
    card.paste(b,(45,30),b)
    base=img.convert('RGBA'); base.paste(card,((img.width-cw)//2,int(cy-ch/2)),m)
    return base.convert('RGB')
def save(img,key): img.save(f'{OUT}/{key}.png',optimize=True)
