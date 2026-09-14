from pathlib import Path

# Minor typography + duplicate CSS cleanup.
p=Path('v4-locale-v1.css')
s=p.read_text(encoding='utf-8')
s=s.replace('.tech-floating-close>span:before{transform:translate(-50%,-50%) rotate(45deg)}.tech-floating-close>span:after{transform:translate(-50%,-50%) rotate(-45deg)}\n','')
s=s.replace('.hero-mark small,.performance-media figcaption,.material-hero figcaption span,.detail-triptych figcaption,#dash small,', '.hero-mark small,.performance-media figcaption,.material-hero figcaption,.material-hero figcaption span,.detail-triptych figcaption,#dash small,#dash .dash-stats small,.modes small,',1)
s=s.replace('.hero-mark small,.performance-media figcaption,.material-hero figcaption span,.detail-triptych figcaption,#dash small,', '.hero-mark small,.performance-media figcaption,.material-hero figcaption,.material-hero figcaption span,.detail-triptych figcaption,#dash small,#dash .dash-stats small,.modes small,',1)
s=s.replace('.location-suggest button small{font-size:7px;max-width:18ch}', '.location-suggest button small{font-size:8px;max-width:18ch}')
p.write_text(s,encoding='utf-8')

# RU-primary Tech button + CSS cache bump.
p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'R1 / TECH SHEET' in s:
    s=s.replace('R1 / TECH SHEET','R1 / ИНЖЕНЕРНЫЙ ПРОФИЛЬ',1)
if 'v4-locale-v1.css?v=2' not in s:
    raise SystemExit('locale css v2 anchor missing')
s=s.replace('v4-locale-v1.css?v=2','v4-locale-v1.css?v=3',1)
p.write_text(s,encoding='utf-8')

# Translate the new RU-primary Tech trigger in EN.
p=Path('v4-locale-v1.js')
s=p.read_text(encoding='utf-8')
anchor="    'ВАШ R1':'YOUR R1'"
if anchor not in s: raise SystemExit('extra text anchor missing')
s=s.replace(anchor,"    'R1 / ИНЖЕНЕРНЫЙ ПРОФИЛЬ':'R1 / ENGINEERING PROFILE',\n"+anchor,1)
p.write_text(s,encoding='utf-8')

# Make QA criteria reflect the new architecture, and use a deterministic programmatic gallery click.
p=Path('.github/scripts/full_qa.mjs')
s=p.read_text(encoding='utf-8')
s=s.replace("if(!html.includes('v4-locale-v1.js?v=4')) issue('static','locale cache-bust is not v4');","if(!html.includes('v4-locale-v1.js?v=5')) issue('static','locale cache-bust is not v5');")
old_dynamic="""  const hardcodedDynamic=[
    ['Ride mode state',/name:'ТРЕК'|desc:'Максимальная отдача привода'|regen:'НИЗКАЯ'/],
    ['Configurator dynamic copy',/МОДУЛЬ|НЕ УСТАНОВЛЕНО|СБОРКА СОХРАНЕНА/],
    ['Activation dynamic copy',/ОТКЛЮЧИТЬ R1|ЗАПУСК\\.\\.\\.|Система ожидает запуска/]
  ];
  hardcodedDynamic.forEach(([name,re])=>{if(re.test(js))warn('static',`${name} is hard-coded in RU inside v4.js and depends on mutation translation`)});
  if(!locale.includes('MutationObserver')) issue('static','locale runtime has no observer for dynamic UI text');
"""
new_dynamic="""  if(!js.includes("window.addEventListener('vanta:languagechange',()=>applyMode")) issue('static','Ride System has no direct language-change renderer');
  if(!js.includes("window.addEventListener('vanta:languagechange',render)")) issue('static','Configurator has no direct language-change renderer');
  if(!js.includes("window.addEventListener('vanta:languagechange',paintActivationCopy)")) issue('static','Activation has no direct language-change renderer');
  if(locale.includes('new MutationObserver')) warn('static','locale runtime still has a global MutationObserver despite direct dynamic localization');
"""
if old_dynamic not in s: raise SystemExit('QA dynamic audit anchor missing')
s=s.replace(old_dynamic,new_dynamic,1)
old_gallery="""  if(await firstGallery.count()){
    await firstGallery.click();await page.waitForTimeout(80);
    if(lang==='en')await assertEnglishClean(page,`${scope}:gallery`,'.gallery-lightbox');
    const close=page.locator('.gallery-lightbox-close');if(await close.count())await close.click();
  }
"""
new_gallery="""  if(await firstGallery.count()){
    await firstGallery.evaluate(el=>el.click());await page.waitForTimeout(100);
    const dialog=page.locator('.gallery-lightbox');
    const opened=await dialog.evaluate(el=>el.open||el.hasAttribute('open')).catch(()=>false);
    if(!opened)issue(scope,'gallery click handler did not open fullscreen viewer');
    else{
      if(lang==='en')await assertEnglishClean(page,`${scope}:gallery`,'.gallery-lightbox');
      const close=page.locator('.gallery-lightbox-close');if(await close.count())await close.evaluate(el=>el.click());
    }
  }
"""
if old_gallery not in s: raise SystemExit('QA gallery anchor missing')
s=s.replace(old_gallery,new_gallery,1)
p.write_text(s,encoding='utf-8')

print('Final QA cleanup prepared')
