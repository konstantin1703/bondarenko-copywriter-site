from pathlib import Path
import csv, io, json, re, urllib.request, zipfile

index_path=Path('index.html')
css_path=Path('v4.css')
js_path=Path('v4.js')
html=index_path.read_text(encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
js=js_path.read_text(encoding='utf-8')

# Cache versions.
html=html.replace('v4.css?v=22','v4.css?v=23').replace('v4.js?v=15','v4.js?v=16')

# Premium outline globe before a country/phone region is selected.
globe='''<svg class="region-globe" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.75"></circle><path d="M3.5 12h17"></path><path d="M12 3.25c2.55 2.35 3.85 5.28 3.85 8.75S14.55 18.4 12 20.75C9.45 18.4 8.15 15.47 8.15 12S9.45 5.6 12 3.25Z"></path></svg>'''
html=html.replace('<span class="region-symbol is-empty" id="phoneFlag" aria-hidden="true"></span>',f'<span class="region-symbol is-empty" id="phoneFlag" aria-hidden="true">{globe}</span>')
html=html.replace('<span class="region-symbol is-empty" id="countryFlag" aria-hidden="true"></span>',f'<span class="region-symbol is-empty" id="countryFlag" aria-hidden="true">{globe}</span>')

# Make location fields explicit comboboxes.
html=html.replace('class="smart-location-input" id="reqRegion" name="region" autocomplete="off" placeholder="Начни вводить регион"', 'class="smart-location-input" id="reqRegion" name="region" autocomplete="off" placeholder="Начни вводить регион" role="combobox" aria-autocomplete="list" aria-controls="regionSuggest" aria-expanded="false"')
html=html.replace('class="smart-location-input" id="reqCity" name="city" autocomplete="off" required placeholder="Начни вводить город"', 'class="smart-location-input" id="reqCity" name="city" autocomplete="off" required placeholder="Начни вводить город" role="combobox" aria-autocomplete="list" aria-controls="citySuggest" aria-expanded="false"')
html=html.replace('Можно выбрать из подсказок или оставить своё значение.','Начни вводить — подсказки будут только по выбранной стране.')
html=html.replace('Поиск учитывает выбранную страну и регион.','Города других стран не показываются.')

# Move tech close outside the clipped panel. Existing JS keeps working by id.
old='<dialog aria-labelledby="techTitle" class="tech-sheet" id="techSheet">\n<div class="tech-sheet-panel tech-profile-v3">'
new='<dialog aria-labelledby="techTitle" class="tech-sheet" id="techSheet">\n<button aria-label="Закрыть инженерный профиль" class="tech-floating-close" id="techClose" type="button"><span aria-hidden="true"></span></button>\n<div class="tech-sheet-panel tech-profile-v3">'
if old not in html:
    raise SystemExit('tech dialog opening marker not found')
html=html.replace(old,new,1)
html=html.replace('    <button aria-label="Закрыть инженерный профиль" id="techClose" type="button">×</button>\n','',1)

# Notify the location module whenever delivery country changes.
needle="deliveryCountry=c;countryButton.dataset.iso=c.iso;setFlag(countryFlag,c);"
replacement="deliveryCountry=c;countryButton.dataset.iso=c.iso;window.dispatchEvent(new CustomEvent('vanta:countrychange',{detail:c}));setFlag(countryFlag,c);"
if needle not in js:
    raise SystemExit('country selection marker not found')
js=js.replace(needle,replacement,1)

# Build world region/city data from GeoNames (CC BY 4.0), split per country for lazy loading.
data_root=Path('data')
locations_dir=data_root/'locations'
locations_dir.mkdir(parents=True,exist_ok=True)
for old_file in locations_dir.glob('*.json'):
    old_file.unlink()

def download(url):
    req=urllib.request.Request(url,headers={'User-Agent':'VANTA-R1-portfolio-build/1.0'})
    with urllib.request.urlopen(req,timeout=60) as r:
        return r.read()

admin_raw=download('https://download.geonames.org/export/dump/admin1Codes.txt').decode('utf-8','replace')
regions={}
admin_names={}
for line in admin_raw.splitlines():
    parts=line.split('\t')
    if len(parts)<2 or '.' not in parts[0]:
        continue
    key,name=parts[0],parts[1].strip()
    country,code=key.split('.',1)
    admin_names[(country,code)]=name
    if name:
        regions.setdefault(country,[]).append(name)
for country,names in regions.items():
    regions[country]=sorted(set(names),key=lambda x:x.casefold())
(data_root/'regions.json').write_text(json.dumps(regions,ensure_ascii=False,separators=(',',':')),encoding='utf-8')

city_zip=download('https://download.geonames.org/export/dump/cities5000.zip')
with zipfile.ZipFile(io.BytesIO(city_zip)) as zf:
    city_text=zf.read('cities5000.txt').decode('utf-8','replace')

cyrillic_countries={'RU','BY','KZ','KG','UA','BG','RS','MK','ME','MD'}
def pick_display(name,aliases,country):
    if country not in cyrillic_countries:
        return name
    for alias in aliases:
        if re.search(r'[А-Яа-яЁё]',alias):
            return alias
    return name

cities_by_country={}
for line in city_text.splitlines():
    p=line.split('\t')
    if len(p)<15:
        continue
    name=p[1].strip(); ascii_name=p[2].strip(); aliases=[a.strip() for a in p[3].split(',') if a.strip()]
    country=p[8].strip(); admin_code=p[10].strip(); population=int(p[14] or 0)
    if not country or not name:
        continue
    display=pick_display(name,aliases,country)
    region=admin_names.get((country,admin_code),'')
    search_aliases=[]
    for value in [name,ascii_name,*aliases]:
        if value and value.casefold()!=display.casefold() and len(value)<=80 and value not in search_aliases:
            search_aliases.append(value)
        if len(search_aliases)>=4:
            break
    cities_by_country.setdefault(country,[]).append({'n':display,'r':region,'p':population,'a':search_aliases})

for country,items in cities_by_country.items():
    # Deduplicate same place/region and keep the most populous record.
    dedup={}
    for item in items:
        key=(item['n'].casefold(),item['r'].casefold())
        if key not in dedup or item['p']>dedup[key]['p']:
            dedup[key]=item
    rows=sorted(dedup.values(),key=lambda x:(-x['p'],x['n'].casefold()))
    (locations_dir/f'{country}.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')),encoding='utf-8')

(data_root/'README.md').write_text('''# Location data\n\nRegion and city autocomplete data is generated from [GeoNames](https://www.geonames.org/) data and used only by the portfolio checkout mock. GeoNames data is licensed under Creative Commons Attribution 4.0.\n''',encoding='utf-8')

# Replace the old handcrafted location module with country-strict lazy data search.
location_v5=r'''/* VANTA R1 — Location Search V5 / country-strict autocomplete 2026-09 */
(()=>{
  'use strict';
  const countryButton=document.getElementById('countryButton');
  const regionInput=document.getElementById('reqRegion');
  const cityInput=document.getElementById('reqCity');
  const regionBox=document.getElementById('regionSuggest');
  const cityBox=document.getElementById('citySuggest');
  if(!countryButton||!regionInput||!cityInput||!regionBox||!cityBox)return;

  const cache={regions:null,cities:new Map()};
  let countryIso=countryButton.dataset.iso||'';
  let selectedRegion='';
  let cityLoadToken=0;
  const norm=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('ru').trim();
  const esc=value=>String(value??'').replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const setExpanded=(input,on)=>input.setAttribute('aria-expanded',String(on));
  const openBox=(input,box)=>{box.hidden=false;setExpanded(input,true);};
  const closeBox=(input,box)=>{box.hidden=true;setExpanded(input,false);};
  const info=(input,box,text)=>{box.innerHTML=`<div class="location-suggest-empty">${esc(text)}</div>`;openBox(input,box);};

  const loadRegions=async()=>{
    if(cache.regions)return cache.regions;
    const res=await fetch('data/regions.json',{cache:'force-cache'});
    if(!res.ok)throw new Error('regions');
    cache.regions=await res.json();
    return cache.regions;
  };
  const loadCities=async iso=>{
    if(cache.cities.has(iso))return cache.cities.get(iso);
    const res=await fetch(`data/locations/${encodeURIComponent(iso)}.json`,{cache:'force-cache'});
    if(!res.ok)throw new Error('cities');
    const data=await res.json();
    cache.cities.set(iso,data);
    return data;
  };
  const rank=(value,query)=>{const a=norm(value),q=norm(query);if(!q)return 2;if(a.startsWith(q))return 0;if(a.includes(q))return 1;return 99;};
  const manualRow=value=>value?`<button type="button" class="use-manual" data-value="${esc(value)}"><strong>Использовать «${esc(value)}»</strong><small>РУЧНОЙ ВВОД</small></button>`:'';

  const renderRegions=async()=>{
    if(!countryIso){info(regionInput,regionBox,'Сначала выбери страну.');return;}
    const query=regionInput.value.trim();
    info(regionInput,regionBox,'Загружаю регионы…');
    try{
      const all=await loadRegions();
      const pool=all[countryIso]||[];
      const rows=pool.map(name=>({name,score:rank(name,query)})).filter(x=>x.score<99).sort((a,b)=>a.score-b.score||a.name.localeCompare(b.name,'ru')).slice(0,12);
      regionBox.innerHTML=rows.map(x=>`<button type="button" data-value="${esc(x.name)}"><strong>${esc(x.name)}</strong><small>РЕГИОН · ${esc(countryIso)}</small></button>`).join('')+manualRow(query);
      if(!regionBox.innerHTML)regionBox.innerHTML='<div class="location-suggest-empty">Совпадений нет — можно оставить введённое значение.</div>';
      openBox(regionInput,regionBox);
    }catch{info(regionInput,regionBox,'Справочник недоступен — введи регион вручную.');}
  };

  const cityMatches=(rows,query)=>{
    const q=norm(query),r=norm(selectedRegion);
    return rows.map(item=>{
      const aliases=[item.n,...(item.a||[])];
      const score=Math.min(...aliases.map(x=>rank(x,q)));
      return {item,score};
    }).filter(x=>x.score<99&&(!r||norm(x.item.r)===r))
      .sort((a,b)=>a.score-b.score||(b.item.p||0)-(a.item.p||0)||a.item.n.localeCompare(b.item.n,'ru'))
      .slice(0,12).map(x=>x.item);
  };
  const renderCities=async()=>{
    if(!countryIso){info(cityInput,cityBox,'Сначала выбери страну.');return;}
    const query=cityInput.value.trim();
    if(!query){info(cityInput,cityBox,'Начни вводить название города.');return;}
    const token=++cityLoadToken;
    info(cityInput,cityBox,`Ищу города · ${countryIso}…`);
    try{
      const rows=await loadCities(countryIso);
      if(token!==cityLoadToken)return;
      const matches=cityMatches(rows,query);
      cityBox.innerHTML=matches.map(item=>`<button type="button" data-value="${esc(item.n)}" data-region="${esc(item.r||'')}"><strong>${esc(item.n)}</strong><small>${esc(item.r||countryIso)}</small></button>`).join('')+manualRow(query);
      if(!cityBox.innerHTML)cityBox.innerHTML='<div class="location-suggest-empty">В выбранной стране совпадений нет — можно оставить введённое значение.</div>';
      openBox(cityInput,cityBox);
    }catch{info(cityInput,cityBox,'Справочник недоступен — введи город вручную.');}
  };

  const keyboard=(input,box,onPick)=>{
    let active=-1;
    input.addEventListener('keydown',e=>{
      const buttons=[...box.querySelectorAll('button[data-value]')];
      if(e.key==='Escape'){closeBox(input,box);active=-1;return;}
      if(!['ArrowDown','ArrowUp','Enter'].includes(e.key))return;
      if(e.key==='Enter'&&active<0){closeBox(input,box);return;}
      e.preventDefault();
      if(e.key==='ArrowDown')active=Math.min(active+1,buttons.length-1);
      if(e.key==='ArrowUp')active=Math.max(active-1,0);
      if(e.key==='Enter'&&buttons[active]){onPick(buttons[active]);closeBox(input,box);active=-1;return;}
      buttons.forEach((b,i)=>b.classList.toggle('is-active',i===active));
      buttons[active]?.scrollIntoView({block:'nearest'});
    });
    input.addEventListener('input',()=>{active=-1;});
  };

  const pickRegion=btn=>{
    regionInput.value=btn.dataset.value||'';
    selectedRegion=btn.classList.contains('use-manual')?'':regionInput.value;
    cityInput.value='';
    closeBox(regionInput,regionBox);closeBox(cityInput,cityBox);
  };
  const pickCity=btn=>{
    cityInput.value=btn.dataset.value||'';
    if(btn.dataset.region&&!selectedRegion){regionInput.value=btn.dataset.region;selectedRegion=btn.dataset.region;}
    closeBox(cityInput,cityBox);
  };
  regionBox.addEventListener('pointerdown',e=>{const btn=e.target.closest('button[data-value]');if(!btn)return;e.preventDefault();pickRegion(btn);});
  cityBox.addEventListener('pointerdown',e=>{const btn=e.target.closest('button[data-value]');if(!btn)return;e.preventDefault();pickCity(btn);});
  keyboard(regionInput,regionBox,pickRegion);keyboard(cityInput,cityBox,pickCity);

  let regionTimer=0,cityTimer=0;
  regionInput.addEventListener('focus',renderRegions);
  regionInput.addEventListener('input',()=>{selectedRegion='';clearTimeout(regionTimer);regionTimer=setTimeout(renderRegions,55);});
  regionInput.addEventListener('change',async()=>{
    try{const all=await loadRegions();const exact=(all[countryIso]||[]).find(x=>norm(x)===norm(regionInput.value));selectedRegion=exact||'';}catch{selectedRegion='';}
    cityInput.value='';
  });
  cityInput.addEventListener('focus',renderCities);
  cityInput.addEventListener('input',()=>{clearTimeout(cityTimer);cityTimer=setTimeout(renderCities,55);});

  window.addEventListener('vanta:countrychange',e=>{
    const next=e.detail?.iso||countryButton.dataset.iso||'';
    if(next===countryIso)return;
    countryIso=next;selectedRegion='';cityLoadToken+=1;
    regionInput.value='';cityInput.value='';
    closeBox(regionInput,regionBox);closeBox(cityInput,cityBox);
    loadRegions().catch(()=>{});if(countryIso)loadCities(countryIso).catch(()=>{});
  });
  countryButton.addEventListener('click',()=>{closeBox(regionInput,regionBox);closeBox(cityInput,cityBox);});
  document.addEventListener('pointerdown',e=>{if(!e.target.closest('.smart-location-field')){closeBox(regionInput,regionBox);closeBox(cityInput,cityBox);}});
})();'''
pattern=r'/\* VANTA R1 — Location Search V4 2026-09 \*/[\s\S]*$'
if not re.search(pattern,js):
    raise SystemExit('old location module not found')
js=re.sub(pattern,location_v5+'\n',js,1)

# CSS overrides for clean globe, unclipped close and stronger autocomplete surface.
css += r'''

/* VANTA R1 — Product Flow V5 / close + location autocomplete 2026-09 */
.region-symbol.is-empty{width:22px!important;height:22px!important;min-width:22px!important;border:0!important;border-radius:0!important;display:grid!important;place-items:center!important}
.region-symbol.is-empty:before,.region-symbol.is-empty:after{display:none!important;content:none!important}
.region-globe{width:21px;height:21px;fill:none;stroke:#858d86;stroke-width:1.35;stroke-linecap:round;stroke-linejoin:round;opacity:.92}
.phone-prefix:hover .region-globe,.phone-prefix:focus-visible .region-globe,.country-button:hover .region-globe,.country-button:focus-visible .region-globe{stroke:#d6dbd6}
#techSheet[open] #techClose.tech-floating-close{position:fixed!important;z-index:10060!important;top:calc(env(safe-area-inset-top,0px) + 18px)!important;right:18px!important;width:48px!important;height:48px!important;margin:0!important;padding:0!important;border:1px solid #4b504c!important;border-radius:50%!important;background:rgba(9,10,9,.94)!important;backdrop-filter:blur(12px);overflow:visible!important;color:transparent!important;box-shadow:0 12px 38px rgba(0,0,0,.42)!important}
#techSheet[open] #techClose.tech-floating-close span:before,#techSheet[open] #techClose.tech-floating-close span:after{content:"";position:absolute;left:50%;top:50%;width:17px;height:1.5px;background:#f1f2ef;border-radius:2px;transform-origin:center}
#techSheet[open] #techClose.tech-floating-close span:before{transform:translate(-50%,-50%) rotate(45deg)}
#techSheet[open] #techClose.tech-floating-close span:after{transform:translate(-50%,-50%) rotate(-45deg)}
#techSheet[open] #techClose.tech-floating-close:before,#techSheet[open] #techClose.tech-floating-close:after{content:none!important;display:none!important}
.tech-profile-head{padding-right:0!important}
.location-suggest{z-index:140!important;background:rgba(8,9,8,.985)!important;border-color:#444a45!important;backdrop-filter:blur(18px);box-shadow:0 24px 70px rgba(0,0,0,.62)!important}
.location-suggest button{min-height:52px!important;padding:10px 14px!important;grid-template-columns:1fr!important;gap:4px!important}
.location-suggest button strong{font-size:11px!important;letter-spacing:.01em!important}
.location-suggest button small{font-size:8px!important;letter-spacing:.08em!important;color:#747c75!important}
.location-suggest button.is-active,.location-suggest button:hover{background:#121412!important;box-shadow:inset 2px 0 0 var(--accent)}
.location-suggest .use-manual{border-top:1px solid #353a36!important;background:#0b0c0b!important}
.location-suggest-empty{padding:17px 14px!important;font-size:9px!important;line-height:1.45!important;color:#777f78!important}
@media(max-width:520px){#techSheet[open] #techClose.tech-floating-close{top:calc(env(safe-area-inset-top,0px) + 14px)!important;right:14px!important;width:46px!important;height:46px!important}.region-symbol.is-empty{width:21px!important;height:21px!important;min-width:21px!important}.location-suggest{max-height:44svh!important}}
'''

index_path.write_text(html,encoding='utf-8')
css_path.write_text(css,encoding='utf-8')
js_path.write_text(js,encoding='utf-8')

# Fast build checks.
assert 'v4.css?v=23' in html and 'v4.js?v=16' in html
assert 'Location Search V5' in js
assert 'tech-floating-close' in html
assert (data_root/'regions.json').exists()
print('V5 patch ready:',len(cities_by_country),'country city files')
