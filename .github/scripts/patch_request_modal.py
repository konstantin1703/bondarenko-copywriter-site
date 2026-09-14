from pathlib import Path

# Bump asset versions in the page.
index = Path('index.html')
s = index.read_text(encoding='utf-8')
s = s.replace('v4-locale-v1.js?v=2', 'v4-locale-v1.js?v=3')
s = s.replace('v4-request-modal-v1.css?v=2', 'v4-request-modal-v1.css?v=3')
s = s.replace('v4-request-modal-v1.js?v=2', 'v4-request-modal-v1.js?v=3')
index.write_text(s, encoding='utf-8')

# Fix directional attribute translation and force fresh localized location data.
loc = Path('v4-locale-v1.js')
j = loc.read_text(encoding='utf-8')

old_attrs = "['aria-label','placeholder','title'].forEach(attr=>{const v=el.getAttribute(attr);if(!v)return;const mapped=dict[v]||TEXT[v]||reverse[v];if(mapped)el.setAttribute(attr,mapped);});"
new_attrs = "['aria-label','placeholder','title'].forEach(attr=>{const v=el.getAttribute(attr);if(!v)return;const mapped=activeLang==='en'?(dict[v]||TEXT[v]):(dict[v]||reverse[v]);if(mapped)el.setAttribute(attr,mapped);});"
if old_attrs not in j:
    raise SystemExit('translateAttrs anchor not found')
j = j.replace(old_attrs, new_attrs, 1)

old_regions = "fetch('data/regions-i18n.json',{cache:'force-cache'})"
new_regions = "fetch('data/regions-i18n.json?v=3',{cache:'no-store'})"
old_cities = "fetch(`data/locations-i18n/${encodeURIComponent(iso)}.json`,{cache:'force-cache'})"
new_cities = "fetch(`data/locations-i18n/${encodeURIComponent(iso)}.json?v=3`,{cache:'no-store'})"
if old_regions not in j or old_cities not in j:
    raise SystemExit('location fetch anchors not found')
j = j.replace(old_regions, new_regions, 1).replace(old_cities, new_cities, 1)

# Persist a selected city id so RU/EN switching can relocalize an already selected city.
old_city_button = "<button type=\"button\" data-value=\"${esc(locName(x))}\" data-region-code=\"${esc(x.r||'')}\">"
new_city_button = "<button type=\"button\" data-id=\"${esc(x.id||'')}\" data-value=\"${esc(locName(x))}\" data-region-code=\"${esc(x.r||'')}\">"
if old_city_button not in j:
    raise SystemExit('city result anchor not found')
j = j.replace(old_city_button, new_city_button, 1)

old_pick_city = "const pickCity=async btn=>{cityInput.value=btn.dataset.value||'';const code=btn.dataset.regionCode||'';if(code&&!selectedRegionCode){selectedRegionCode=code;regionInput.dataset.regionCode=code;try{const regions=await regionsForCountry();const item=regions.find(x=>x.code===code);if(item)regionInput.value=locName(item)}catch{}}close(cityInput,cityBox);cityInput.dispatchEvent(new Event('change',{bubbles:true}))};"
new_pick_city = "const pickCity=async btn=>{cityInput.value=btn.dataset.value||'';cityInput.dataset.cityId=btn.classList.contains('use-manual')?'':(btn.dataset.id||'');const code=btn.dataset.regionCode||'';if(code&&!selectedRegionCode){selectedRegionCode=code;regionInput.dataset.regionCode=code;try{const regions=await regionsForCountry();const item=regions.find(x=>x.code===code);if(item)regionInput.value=locName(item)}catch{}}close(cityInput,cityBox);cityInput.dispatchEvent(new Event('change',{bubbles:true}))};"
if old_pick_city not in j:
    raise SystemExit('pickCity anchor not found')
j = j.replace(old_pick_city, new_pick_city, 1)

old_lang = "window.addEventListener('vanta:languagechange',async()=>{try{if(selectedRegionCode){const regions=await regionsForCountry();const item=regions.find(x=>x.code===selectedRegionCode);if(item)regionInput.value=locName(item)}}catch{}if(!regionBox.hidden)renderRegions();if(!cityBox.hidden)renderCities();localizeCountryRows()});"
new_lang = "window.addEventListener('vanta:languagechange',async()=>{try{if(selectedRegionCode){const regions=await regionsForCountry();const item=regions.find(x=>x.code===selectedRegionCode);if(item)regionInput.value=locName(item)}const cityId=cityInput.dataset.cityId||'';if(cityId&&countryIso){const rows=await loadCities(countryIso);const city=rows.find(x=>String(x.id)===String(cityId));if(city)cityInput.value=locName(city)}}catch{}if(!regionBox.hidden)renderRegions();if(!cityBox.hidden)renderCities();localizeCountryRows()});"
if old_lang not in j:
    raise SystemExit('language-change anchor not found')
j = j.replace(old_lang, new_lang, 1)

loc.write_text(j, encoding='utf-8')
print('locale v3 + request modal v3 ready')
