from ae_lib import *
W,H=1080,1350
slides=[
 dict(h1=('OLIO GIUSTO.',(255,255,255,255)),h2=('SERVIZIO VERO.',CY+(255,)),sub='Chi siamo: AUTO EVO STORE',sub2='Scorri per conoscerci',cover=True),
 dict(h1=('DA ANDRIA',(255,255,255,255)),h2=('PER TUTTA ITALIA.',CY+(255,)),icon='pin',sub='AUTO EVO RICAMBI S.R.L.',sub2='Andria (BT), Puglia'),
 dict(h1=('SOLO OLI',(255,255,255,255)),h2=('E LUBRIFICANTI.',CY+(255,)),icon='drop',sub='Olio motore, cambio e fluidi tecnici.',sub2='Niente altro: solo quello che sappiamo scegliere bene.'),
 dict(h1=('SPEDIZIONE',(255,255,255,255)),h2=('GRATUITA IN ITALIA.',CY+(255,)),icon='truck',sub='Consegna in 24/48h.',chips=['Italia 24/48h','Europa 3-7 giorni','Reso entro 14 giorni']),
 dict(h1=('NON SEI SICURO',(255,255,255,255)),h2=("DELL'OLIO?",CY+(255,)),icon='chat',sub='Scrivici targa e modello in DM:',sub2='controlliamo noi la specifica giusta.',cta=True),
]
for i,s in enumerate(slides):
    img=background(W,H,glows=((0.5,0.55,0.55,0.35,0.22),),seed=3+i,floor=1180)
    img,lb=add_logo(img,width=720 if s.get('cover') else 440,top=30 if not s.get('cover') else 120)
    if s.get('icon'): img=icon_ring(img,s['icon'],W//2,lb+175,125)
    y0=(lb+340) if s.get('icon') else lb+150
    big=font('Bold',96 if len(s['h2'][0])<16 else 86)
    ctext(img,s['h1'][0],y0,big,s['h1'][1]);ctext(img,s['h2'][0],y0+112,big,s['h2'][1])
    y=y0+250
    ctext(img,s['sub'],y,font('Medium',44),(230,238,248,255))
    if s.get('sub2'): ctext(img,s['sub2'],y+68,font('Regular',36),(185,200,220,255))
    if s.get('chips'):
        cy=y+80;f=font('Medium',32)
        img=chip(img,W/2,cy,s['chips'][0],f);img=chip(img,W/2,cy+84,s['chips'][1],f);img=chip(img,W/2,cy+168,s['chips'][2],f)
    if s.get('cta'): ctext(img,'autoevostore.it  (link in bio)',y+170,font('Bold',46),CY+(255,))
    img=dots(img,len(slides),i,1250)
    ctext(img,'autoevostore.it' if not s.get('cta') else 'AUTO EVO STORE',1290,font('Regular',26),(150,170,195,255))
    img.convert('RGB').save(f'chisiamo_{i+1}.png')
# contact sheet
sheet=Image.new('RGB',(5*360,450),(0,0,0))
for i in range(5): sheet.paste(Image.open(f'chisiamo_{i+1}.png').resize((360,450)),(i*360,0))
sheet.save('chisiamo_sheet.png')
