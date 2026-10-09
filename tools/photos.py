"""Ingest product screenshots (captured from Shopify CDN) -> cutout PNGs in products/."""
import os, numpy as np
from PIL import Image, ImageFilter
from collections import deque
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC='/tmp/claude-chrome-screenshots-EBKO3u'
MAP={1:'petronas_xs_5w30',8:'selenia_wr_forward_0w30',9:'selenia_digitek_0w30',10:'selenia_wr_5w40_diesel',
11:'castrol_edge_td_5w40',12:'mobil1_esp_5w30',13:'mannol_longlife_504_507',14:'selenia_multipower_gas',15:'selenia_20k_10w40',
16:'castrol_edge_ll3_5w30',17:'total_ineo_mc3',18:'castrol_magnatec_0w30_d',20:'opel_gm_dexos2_1l',21:'selenia_wr_pure_energy_5w30',
22:'selenia_k_pure_energy_5w40',24:'castrol_magnatec_5w30_a5',25:'castrol_magnatec_prof_d_0w30',26:'castrol_edge_ll_0w30',
27:'castrol_transmax_axle_80w90',28:'castrol_power1_2t',29:'mannol_outboard_7207',32:'castrol_edge_0w20_c5',33:'mannol_8118',
34:'petronas_prime_av',35:'mannol_atf_dexron3'}
GRAPHIC={30:'wrc_ultraplus_5w30',31:'wrc_ultraplus_5w40_gas'}

def find(idx):
    for f in os.listdir(SRC):
        if f.endswith('-%d.jpg'%idx): return os.path.join(SRC,f)

def crop_bars(im):
    a=np.asarray(im.convert('L')).astype(int)
    ok=np.where(a.mean(0)>30)[0]
    return im.crop((ok[0],0,ok[-1]+1,im.height))

def cutout(im):
    rgb=np.asarray(im.convert('RGB')).astype(int); h,w,_=rgb.shape
    white=(rgb.min(2)>236)
    seen=np.zeros((h,w),bool); dq=deque()
    for x in range(w):
        for y in (0,h-1):
            if white[y,x] and not seen[y,x]: seen[y,x]=True; dq.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if white[y,x] and not seen[y,x]: seen[y,x]=True; dq.append((y,x))
    while dq:
        y,x=dq.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<h and 0<=nx<w and white[ny,nx] and not seen[ny,nx]:
                seen[ny,nx]=True; dq.append((ny,nx))
    alpha=Image.fromarray(((~seen)*255).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.1))
    from scipy import ndimage
    m=np.asarray(alpha)>128
    lab,n=ndimage.label(m)
    if n>1:
        sizes=ndimage.sum(m,lab,range(1,n+1)); keep=lab==(1+int(np.argmax(sizes)))
        keep=ndimage.binary_dilation(keep,iterations=3)
        alpha=Image.fromarray((np.asarray(alpha)*keep).astype('uint8'))
    out=im.convert('RGBA'); out.putalpha(alpha)
    return out.crop(alpha.point(lambda v:255 if v>128 else 0).getbbox())

if __name__=='__main__':
    os.makedirs(os.path.join(ROOT,'products'),exist_ok=True)
    for idx,key in MAP.items():
        c=cutout(crop_bars(Image.open(find(idx))))
        c.save(os.path.join(ROOT,'products',key+'.png'),optimize=True); print(key,c.size)
    for idx,key in GRAPHIC.items():
        im=Image.open(find(idx)).convert('RGB').crop((43,0,1105,1063))
        im.save(os.path.join(ROOT,'products',key+'_graphic.jpg'),quality=92); print(key,im.size)
