from ae_lib import *
from PIL import ImageDraw
W,H=1080,1920
img=background(W,H,glows=((0.5,0.5,0.6,0.3,0.2),),seed=33,floor=1700)
img,lb=add_logo(img,width=620,top=130)
y0=lb+120
big=font('Bold',104)
ctext(img,'5W-30',y0,big,(255,255,255,255))
ctext(img,'O',y0+120,font('Medium',58),(185,200,220,255))
img=glow_text(img,'5W-40?',y0+190,big,fill=CY+(255,),glow=CY,blur=22)
ctext(img,'Che viscosità usa la tua auto?',y0+400,font('Medium',44),(230,238,248,255))
# two cards
d=ImageDraw.Draw(img)
layer=Image.new('RGBA',img.size,(0,0,0,0));ld=ImageDraw.Draw(layer)
for i,(cx,t) in enumerate([(300,'5W-30'),(780,'5W-40')]):
    ld.rounded_rectangle([cx-190,y0+500,cx+190,y0+640],40,fill=(255,255,255,18),outline=CY+(200,),width=4)
img=Image.alpha_composite(img,layer)
for cx,t in [(300,'5W-30'),(780,'5W-40')]:
    f=font('Bold',62);w=ImageDraw.Draw(img).textlength(t,font=f);ImageDraw.Draw(img).text((cx-w/2,y0+530),t,font=f,fill=(255,255,255,255))
ctext(img,'Non lo ricordi? Guarda nel libretto',y0+720,font('Regular',38),(185,200,220,255))
ctext(img,'oppure scrivici targa e modello in DM.',y0+776,font('Regular',38),(185,200,220,255))
ctext(img,'autoevostore.it',1790,font('Regular',30),(150,170,195,255))
img.convert('RGB').save('storia_5w.png')
