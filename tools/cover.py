from ae_lib import *
W,H=1640,624
img=background(W,H,glows=((0.5,0.5,0.45,0.9,0.28),),seed=11,floor=None)
# logo centered-left, claim right
img2,lb=add_logo(img,width=620,top=70)
# shift: draw logo on left third manually
base=background(W,H,glows=((0.28,0.5,0.35,0.9,0.28),(0.78,0.5,0.4,0.8,0.12)),seed=11)
lg,lbm=add_logo(Image.new('RGBA',(W,H),(0,0,0,0)),width=640,top=0)
