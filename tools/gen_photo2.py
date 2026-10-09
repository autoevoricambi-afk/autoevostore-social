"""Storie serali 'prodotto del giorno' (10-23 ott) con foto reali. Specifiche solo da titolo/tag Shopify."""
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from photo_lib import *
H=1920
L=[ # key, layout, kicker, lines, spec/bullets
('10','selenia_wr_forward_0w30','hero','Selenia',['WR Forward 0W-30'],('ACEA C2','FIAT 955535-DS1/DH1')),
('11','castrol_edge_td_5w40','big','Castrol EDGE',['Turbo Diesel'],('ACEA C3','FIAT 9.55535-S2','VW 505.00/505.01'),'5W-40'),
('12','mannol_longlife_504_507','split','MANNOL',['Longlife','504/507'],['5W-30','ACEA C3','VW 504.00 / 507.00','Porsche C30']),
('13','selenia_multipower_gas','hero','Selenia',['Multipower Gas 5W-40'],('GPL/Metano','ACEA C3')),
('14','selenia_wr_5w40_diesel','big','Selenia WR',['Diesel'],('ACEA A3/B4','API SN/CF','FIAT 9.55535-N2/N3'),'5W-40'),
('15','castrol_magnatec_0w30_d','split','Castrol MAGNATEC',['0W-30 D'],['Olio sintetico','ACEA C2','Ford WSS-M2C950-A']),
('16','opel_gm_dexos2_1l','hero','Opel GM',['5W-30 dexos2'],('ACEA C3','MB 229.51/229.52','DPF compatibile')),
('17','selenia_20k_10w40','big','Selenia 20K',['Semisintetico'],('ACEA A3/B4','FCA 9.55535-G2/D2'),'10W-40'),
('18','castrol_edge_ll_0w30','split','Castrol EDGE',['0W-30 LL'],['Olio sintetico','ACEA C3','VW 504.00 / 507.00','LongLife III']),
('19','selenia_wr_pure_energy_5w30','hero','Petronas Selenia',['WR Pure Energy 5W-30'],('ACEA C2','FIAT / Mopar')),
('20','castrol_magnatec_5w30_a5','big','Castrol MAGNATEC',['5W-30 A5'],('ACEA A5/B5','Ford WSS-M2C913'),'5W-30'),
('21','castrol_transmax_axle_80w90','split','Castrol',['Transmax','Axle EPX'],['Olio per differenziale','80W-90','API GL-5','ZF TE-ML 05A/12E/16B/17B/19B/21A']),
('22','castrol_power1_2t','hero','Castrol Power 1 Ultimate',['2T moto'],('100% sintetico','API TC+','JASO FD')),
('23','mannol_outboard_7207','hero','MANNOL 7207',['Outboard Marine 2T'],('API TC','NMMA TC-W3','JASO FC')),
]
for it in L:
    d,key,lay,kick,lines,sp=it[:6]
    if lay=='hero': img=hero(key,kick,lines,chips=sp,H=H,fonts=64)
    elif lay=='big': img=bigspec(key,it[6],kick,lines,chips=sp,H=H,fonts=72)
    else: img=split(key,kick,lines,sp,H=H,fonts=64)
    ctext(img,'Dubbi? Scrivici targa e modello in DM.',H-175,font('Regular',34),SOFT)
    save(img,f'2026-10/ev{d}.jpg')
print('ok')
