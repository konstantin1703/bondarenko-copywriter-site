from __future__ import annotations
from pathlib import Path
import io, json, urllib.request, zipfile

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUT=DATA/'locations-i18n'
OUT.mkdir(parents=True,exist_ok=True)

UA='VANTA-R1-portfolio-build/2.0'
def download(url:str)->bytes:
    req=urllib.request.Request(url,headers={'User-Agent':UA})
    with urllib.request.urlopen(req,timeout=120) as r:
        return r.read()

def norm_name(value:str)->str:
    return ' '.join((value or '').replace('\u00a0',' ').split()).strip()

def choose(current, candidate, preferred=False):
    candidate=norm_name(candidate)
    if not candidate:
        return current
    if current is None or preferred:
        return (candidate, preferred)
    return current

print('Downloading admin1 codes…')
admin_text=download('https://download.geonames.org/export/dump/admin1CodesASCII.txt').decode('utf-8','replace')
regions_meta={}
ids=set()
for line in admin_text.splitlines():
    p=line.split('\t')
    if len(p)<4 or '.' not in p[0]:
        continue
    full,name,ascii_name,gid=p[0],norm_name(p[1]),norm_name(p[2]),p[3].strip()
    country,code=full.split('.',1)
    try: geoid=int(gid)
    except: continue
    regions_meta[(country,code)]={'id':geoid,'name':name,'ascii':ascii_name}
    ids.add(geoid)

print('Downloading cities5000…')
raw=download('https://download.geonames.org/export/dump/cities5000.zip')
with zipfile.ZipFile(io.BytesIO(raw)) as zf:
    city_text=zf.read('cities5000.txt').decode('utf-8','replace')

cities=[]
for line in city_text.splitlines():
    p=line.split('\t')
    if len(p)<15: continue
    try: geoid=int(p[0]); population=int(p[14] or 0)
    except: continue
    country=p[8].strip(); admin1=p[10].strip()
    if not country or not p[1].strip(): continue
    row={'id':geoid,'name':norm_name(p[1]),'ascii':norm_name(p[2]),'aliases':[norm_name(x) for x in p[3].split(',') if norm_name(x)],'country':country,'r':admin1,'p':population}
    cities.append(row);ids.add(geoid)

print(f'Downloading localized names for {len(ids):,} geonames…')
alt_raw=download('https://download.geonames.org/export/dump/alternateNamesV2.zip')
localized={}
with zipfile.ZipFile(io.BytesIO(alt_raw)) as zf:
    # Current dump uses alternateNamesV2.txt.
    member=next((n for n in zf.namelist() if n.endswith('.txt')),zf.namelist()[0])
    with zf.open(member) as fh:
        for bline in fh:
            try: line=bline.decode('utf-8','replace').rstrip('\n');p=line.split('\t')
            except: continue
            if len(p)<4: continue
            try: geoid=int(p[1])
            except: continue
            if geoid not in ids: continue
            lang=p[2].strip().lower()
            if lang not in ('ru','en'): continue
            name=norm_name(p[3])
            if not name: continue
            preferred=len(p)>4 and p[4]=='1'
            historic=len(p)>7 and p[7]=='1'
            colloquial=len(p)>6 and p[6]=='1'
            if historic or colloquial: continue
            entry=localized.setdefault(geoid,{})
            cur=entry.get(lang)
            if cur is None or (preferred and not cur[1]):
                entry[lang]=(name,preferred)

def lname(geoid:int,lang:str,fallback:str)->str:
    val=localized.get(geoid,{}).get(lang)
    return val[0] if val else norm_name(fallback)

print('Writing localized regions…')
regions={}
for (country,code),m in regions_meta.items():
    en=lname(m['id'],'en',m['name'] or m['ascii'])
    ru=lname(m['id'],'ru',en)
    regions.setdefault(country,[]).append({'code':code,'ru':ru,'en':en})
for country,items in regions.items():
    items.sort(key=lambda x:(x['ru'].casefold(),x['en'].casefold()))
(DATA/'regions-i18n.json').write_text(json.dumps(regions,ensure_ascii=False,separators=(',',':')),encoding='utf-8')

print('Writing localized cities…')
by_country={}
for c in cities:
    en=lname(c['id'],'en',c['ascii'] or c['name'])
    ru=lname(c['id'],'ru',en)
    aliases_en=[];aliases_ru=[]
    for a in [c['name'],c['ascii'],*c['aliases']]:
        a=norm_name(a)
        if not a: continue
        if a.casefold()!=en.casefold() and a not in aliases_en and len(a)<=80: aliases_en.append(a)
        if any('А'<=ch<='я' or ch in 'Ёё' for ch in a) and a.casefold()!=ru.casefold() and a not in aliases_ru and len(a)<=80: aliases_ru.append(a)
        if len(aliases_en)>=4 and len(aliases_ru)>=4: break
    row={'id':c['id'],'ru':ru,'en':en,'r':c['r'],'p':c['p']}
    if aliases_ru: row['a_ru']=aliases_ru[:4]
    if aliases_en: row['a_en']=aliases_en[:4]
    by_country.setdefault(c['country'],[]).append(row)

for old in OUT.glob('*.json'): old.unlink()
for country,items in by_country.items():
    dedup={}
    for x in items:
        key=(x['ru'].casefold(),x['en'].casefold(),x['r'])
        if key not in dedup or x['p']>dedup[key]['p']: dedup[key]=x
    rows=sorted(dedup.values(),key=lambda x:(-x['p'],x['ru'].casefold(),x['en'].casefold()))
    (OUT/f'{country}.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')),encoding='utf-8')

print(f'Wrote {len(regions)} country region sets and {len(by_country)} country city files.')
