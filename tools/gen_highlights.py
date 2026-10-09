import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from photo_lib import *
from ae_slides import icon_ring
def cover(label,kind=None,key=None,keys=None):
    W,H=1080,1920
    img=background(W,H,glows=((0.5,0.5,0.55,0.3,0.28),),seed=11)
    cy=H//2-40
    if kind: img=icon_ring(img,kind,W//2,cy,330)
    if key:
        r=360; ring=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ring)
        d.ellipse([W//2-r,cy-r,W//2+r,cy+r],fill=(0,200,230,22),outline=CY+(210,),width=5); img=Image.alpha_composite(img,ring)
        img=place(img,key,W//2,cy+300,560,glow=False,reflect=False)
    if keys:
        r=380; ring=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ring)
        d.ellipse([W//2-r,cy-r,W//2+r,cy+r],fill=(0,200,230,22),outline=CY+(210,),width=5); img=Image.alpha_composite(img,ring)
        for i,k in enumerate(keys): img=place(img,k,W//2+(i-1)*190,cy+(250 if i==1 else 215),(430 if i==1 else 380),glow=False,reflect=False)
    img=glow_text(img,label,cy+r+110 if (key or keys) else cy+480,font('Bold',92),fill=WHITE)
    return img
os.makedirs(OUT+'/highlights',exist_ok=True)
C=[('PRODOTTI',dict(key='castrol_edge_ll3_5w30')),('MARCHI',dict(keys=['mobil1_esp_5w30','total_ineo_mc3','petronas_prime_av'])),
('SPECIFICHE',dict(kind='check')),('CONSIGLI',dict(kind='book')),('SPEDIZIONE',dict(kind='truck')),('RESO',dict(kind='return')),('ASSISTENZA',dict(kind='chat'))]
for lab,kw in C:
    img=cover(lab,**kw); img.convert('RGB').save(f'{OUT}/highlights/{lab.lower()}.jpg',quality=93)
from PIL import Image
S=Image.new('RGB',(7*270,480))
for i,(lab,_) in enumerate(C): S.paste(Image.open(f'{OUT}/highlights/{lab.lower()}.jpg').resize((270,480)),(i*270,0))
S.save('/tmp/sheet.jpg')
