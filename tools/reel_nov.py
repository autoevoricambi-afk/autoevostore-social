"""Reel novembre: errori, tre 0W-30, non solo auto. Uso: python3 tools/reel_nov.py [err|030|uso]"""
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from reel_lib import *

def seq_reel(name,intro,items,end1,end2,D=3.4,T0=2.7):
    bg,lb=stage(); bg=bg.convert('RGBA'); foot(bg)
    sp=[sprite(k,700) for k,_,_ in items]; nm=[text_layer(n,50) for _,n,_ in items]
    ch=[[chip_layer(c) for c in cs] for _,_,cs in items]
    t1=text_layer(intro,90); e1=text_layer(end1,84); e2=text_layer(end2,44,'Medium',SOFT)
    e3=text_layer('autoevostore.it  ·  link in bio',40,'Medium',CY+(255,))
    ybot=1330
    def fn(fr,t):
        if t<T0-0.2: paste(fr,t1,0,640+int(30*(1-ease(seg(t,0.1,0.8)))),ease(seg(t,0.1,0.8))*(1-ease(seg(t,T0-0.6,T0-0.2))))
        for i,(s,cx,bo) in enumerate(sp):
            a0=T0+i*D
            if a0-0.1<=t<a0+D+0.3:
                u=ease(seg(t,a0,a0+0.6)); o=1-ease(seg(t,a0+D-0.3,a0+D+0.2))
                paste(fr,s,540-cx+int((-1)**i*480*(1-u))+int((-1)**i*-480*(1-o)),ybot-bo,u*o)
                paste(fr,nm[i],0,ybot+60,ease(seg(t,a0+0.5,a0+1.0))*o)
                for j,c in enumerate(ch[i]): paste(fr,c,540-c.width//2,ybot+135+j*92,ease(seg(t,a0+0.9+j*0.4,a0+1.3+j*0.4))*o)
        te=T0+len(sp)*D
        if t>=te:
            paste(fr,e1,0,700,ease(seg(t,te,te+0.7))); paste(fr,e2,0,1010,ease(seg(t,te+0.6,te+1.2))); paste(fr,e3,0,1200,ease(seg(t,te+1.2,te+1.8)))
    return render(name,T0+len(sp)*D+3.4,fn,bg)

def reel_err():
    bg,lb=stage(); bg=bg.convert('RGBA'); foot(bg)
    s,cx,bo=sprite('petronas_prime_av',500)
    t1=text_layer('Tre errori che\nfanno comprare\nl’olio sbagliato.',92)
    items=[('1','Guardare solo la viscosità','Due 5W-40, omologazioni diverse'),
           ('2','Scegliere per marchio','Conta la specifica richiesta dal costruttore'),
           ('3','Non aprire il libretto','La risposta è lì, nero su bianco')]
    cards=[]
    for n,big,small in items:
        im=Image.new('RGBA',(W,200),(0,0,0,0)); d=ImageDraw.Draw(im)
        d.rounded_rectangle([90,10,W-90,190],40,fill=(255,255,255,22),outline=CY+(200,),width=3)
        d.text((135,24),n,font=font('Bold',110),fill=CY+(255,))
        d.text((230,34),big,font=font('Bold',46),fill=WHITE); d.text((230,112),small,font=font('Regular',31),fill=SOFT); cards.append(im)
    e1=text_layer('Dubbi? Scrivici\ntarga e modello.',84); e2=text_layer('Verifichiamo noi la specifica giusta.',44,'Medium',SOFT)
    e3=text_layer('autoevostore.it  ·  link in bio',40,'Medium',CY+(255,))
    def fn(fr,t):
        if t<2.6: paste(fr,t1,0,640,ease(seg(t,0.1,0.8))*(1-ease(seg(t,2.2,2.6))))
        if 2.4<=t<11.2:
            u=ease(seg(t,2.4,3.2)); a=1-ease(seg(t,10.8,11.2))
            paste(fr,s,540-cx,1670-bo+int(260*(1-u)),a*u)
            for i,c in enumerate(cards):
                st=3.6+i*2.3; paste(fr,c,int(90*(1-ease(seg(t,st,st+0.6)))),415+i*215,ease(seg(t,st,st+0.6))*a)
        if t>=11.0:
            paste(fr,e1,0,700,ease(seg(t,11.0,11.7))); paste(fr,e2,0,1010,ease(seg(t,11.6,12.2))); paste(fr,e3,0,1200,ease(seg(t,12.2,12.8)))
    return render('reel_errori',14.2,fn,bg)

def reel_030():
    return seq_reel('reel_030','Stesso grado:\n0W-30.',[
        ('castrol_edge_ll_0w30','Castrol EDGE 0W-30 LL',('ACEA C3','VW 504.00 / 507.00')),
        ('castrol_magnatec_0w30_d','Castrol MAGNATEC 0W-30 D',('ACEA C2','Ford WSS-M2C950-A')),
        ('selenia_wr_forward_0w30','Selenia WR Forward 0W-30',('ACEA C2','FIAT 955535-DS1/DH1'))],
        'Tre specifiche.\nControlla il libretto.','Targa, modello e anno in DM: verifichiamo noi.')

def reel_uso():
    return seq_reel('reel_uso','Non solo olio\nmotore auto.',[
        ('castrol_power1_2t','Castrol Power 1 Ultimate 2T',('Moto','JASO FD')),
        ('mannol_outboard_7207','MANNOL 7207 Outboard Marine 2T',('Motori marini','NMMA TC-W3')),
        ('castrol_transmax_axle_80w90','Castrol Transmax Axle EPX',('Differenziale','API GL-5')),
        ('mannol_atf_dexron3','MANNOL ATF Dexron III',('Cambio automatico','Servosterzo'))],
        'Scegli per uso\ne per specifica.','Targa e modello in DM: verifichiamo noi.')

if __name__=='__main__':
    for w in (sys.argv[1:] or ['err','030','uso']): print(dict(err=reel_err,**{'030':reel_030},uso=reel_uso)[w]())
