"""Controllo qualità sui post programmati (output di getScheduledPosts salvato in JSON).
Uso: python3 tools/qc.py <file.json>   -> elenca violazioni delle regole fisse."""
import json, re, sys
RULES=[
 (r'€|\beuro\b|\bprezz|\bsconto|\boffert|\bpromo', 'prezzo/offerta nel testo'),
 (r'sostituzion[ea] gratuit', '"sostituzione gratuita" vietata'),
 (r'0W-?20', None),  # gestita sotto (solo Selenia vietato)
 (r'\bIvan\b', 'nome personale'),
]
def check(p):
    t=p.get('text') or ''; out=[]
    for pat,msg in RULES:
        if msg and re.search(pat,t,re.I): out.append(msg)
    if re.search(r'selenia[^\n]{0,40}0W-?20',t,re.I): out.append('Selenia 0W-20 archiviato')
    ig=(p.get('instagramData') or {}).get('type','POST')
    if ig!='STORY':
        if 'autoevostore.it (link in bio)' not in t: out.append('manca chiusura "autoevostore.it (link in bio)"')
        if 'DM' not in t and 'libretto' not in t: out.append('manca invito DM/libretto')
    media=p.get('media') or []; alts=p.get('mediaAltText') or []
    if media and len(alts)<len(media) and not any(m.endswith('.mp4') for m in media): out.append('alt text mancante')
    if p.get('draft'): out.append('BOZZA')
    nets={x['network'] for x in p.get('providers',[])}
    if nets!={'facebook','instagram'}: out.append('provider diversi da FB+IG: %s'%sorted(nets))
    return out
if __name__=='__main__':
    d=json.load(open(sys.argv[1])); d=d['data'] if isinstance(d,dict) else d
    bad=0
    for p in sorted(d,key=lambda p:p['publicationDate']['dateTime']):
        v=check(p)
        if v: bad+=1; print(p['publicationDate']['dateTime'][:16],p['id'],'; '.join(v))
    print(f'{len(d)} post controllati, {bad} con problemi')
