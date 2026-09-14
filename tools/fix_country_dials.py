from pathlib import Path
import re,json,csv,io,urllib.request

p=Path('v4.js')
js=p.read_text(encoding='utf-8')
m=re.search(r"  const countries=(\[\{.*?\}\]);\n  const flag=",js,re.S)
if not m:
    raise SystemExit('countries array not found')
rows=json.loads(m.group(1))
url='https://raw.githubusercontent.com/datasets/country-codes/main/data/country-codes.csv'
with urllib.request.urlopen(url,timeout=25) as r:
    text=r.read().decode('utf-8-sig')
reader=csv.DictReader(io.StringIO(text))
dials={}
for row in reader:
    iso=(row.get('ISO3166-1-Alpha-2') or '').strip()
    dial=(row.get('Dial') or '').strip()
    if not iso or not dial: continue
    # The dataset stores country calling codes without the leading plus.
    # Keep the first canonical code when multiple entries are present.
    dial=dial.split(',')[0].strip().split(' and ')[0].strip()
    dials[iso]='+'+dial.lstrip('+')
name_overrides={'US':'США','AE':'ОАЭ','GB':'Великобритания','KR':'Южная Корея','KP':'Северная Корея','CZ':'Чехия','MD':'Молдова','TW':'Тайвань','VA':'Ватикан'}
for c in rows:
    if c['iso'] in dials:
        c['dial']=dials[c['iso']]
    if c['iso'] in name_overrides:
        c['name']=name_overrides[c['iso']]
new='  const countries='+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\n  const flag='
js=js[:m.start()]+new+js[m.end():]
p.write_text(js,encoding='utf-8')
check={c['iso']:c['dial'] for c in rows}
expected={'RU':'+7','KZ':'+7','US':'+1','CA':'+1','DE':'+49','AE':'+971'}
for iso,dial in expected.items():
    if check.get(iso)!=dial:
        raise SystemExit(f'{iso}: expected {dial}, got {check.get(iso)}')
if len(rows)<180:
    raise SystemExit(f'country count too small: {len(rows)}')
print('corrected',len(rows),'countries')
