from cal_lib import *
items=[
 ('thu15_mobil','MOBIL 1 ESP','5W-30',['ACEA C3','BMW LL-04','MB 229.52','VW 504.00 / 507.00'],111),
 ('thu22_castrol','CASTROL EDGE','0W-20 C5',['ACEA C5 / C6','API SQ','dexos1 Gen 3','MB 229.71'],112),
 ('thu29_total','TOTAL QUARTZ','INEO MC3 5W-30',['ACEA C3','API SN PLUS','Low SAPS'],113),
 ('thu05_bmw','BMW TWINPOWER TURBO','0W-30 LL-04',['ACEA C3','API SN','BMW Longlife-04'],114)]
for key,l1,l2,chips,seed in items:
    save(slide(icon=('drop' if len(chips)<4 else None),lines=[(l1,WHITE,68 if len(l1)>14 else 80),(l2,CYc,76)],body='Olio motore sintetico.',chips=chips,foot='Spedizione gratuita in Italia  ·  autoevostore.it',seed=seed),key)
