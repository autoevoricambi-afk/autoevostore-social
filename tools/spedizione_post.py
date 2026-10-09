from ae_lib import *
W,H=1080,1350
img=background(W,H,glows=((0.5,0.55,0.55,0.35,0.22),),seed=21,floor=1180)
img,lb=add_logo(img,width=440,top=30)
img=icon_ring(img,'truck',W//2,lb+175,125)
y0=lb+340
big=font('Bold',84)
ctext(img,"DALL'ORDINE",y0,big,(255,255,255,255));ctext(img,'ALLA CONSEGNA.',y0+104,big,CY+(255,))
y=y0+235
ctext(img,'Spedizione gratuita in Italia in 24/48h.',y,font('Medium',40),(230,238,248,255))
f=font('Medium',34)
cy=y+70
for k,t in enumerate(['1  Ordini sul sito','2  Prepariamo il tuo pacco','3  Consegna in 24/48h']):
    img=chip(img,W/2,cy+k*84,t,f)
ctext(img,'Europa in 3-7 giorni lavorativi  ·  Reso entro 14 giorni',1228,font('Regular',28),(185,200,220,255))
ctext(img,'autoevostore.it',1290,font('Regular',26),(150,170,195,255))
img.convert('RGB').save('spedizione_post.png')
