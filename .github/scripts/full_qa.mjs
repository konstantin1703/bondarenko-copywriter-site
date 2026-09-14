import fs from 'node:fs';
import { chromium } from 'playwright';

const BASE='http://127.0.0.1:4173';
const issues=[];
const warnings=[];
const notes=[];
const issue=(scope,msg)=>issues.push(`[${scope}] ${msg}`);
const warn=(scope,msg)=>warnings.push(`[${scope}] ${msg}`);
const note=(scope,msg)=>notes.push(`[${scope}] ${msg}`);
const cyr=/[А-Яа-яЁё]/;

function staticAudit(){
  const html=fs.readFileSync('index.html','utf8');
  const js=fs.readFileSync('v4.js','utf8');
  const locale=fs.readFileSync('v4-locale-v1.js','utf8');
  const modal=fs.readFileSync('v4-request-modal-v1.js','utf8');
  const css=fs.readFileSync('v4.css','utf8');
  const localeCss=fs.readFileSync('v4-locale-v1.css','utf8');
  const modalCss=fs.readFileSync('v4-request-modal-v1.css','utf8');

  if(!html.includes('v4-locale-v1.js?v=4')) issue('static','locale cache-bust is not v4');
  if(!html.includes('v4-request-modal-v1.js?v=4')) issue('static','request modal cache-bust is not v4');
  if(js.includes("fetch('data/regions.json'")||js.includes('data/locations/${encodeURIComponent(iso)}.json')) issue('static','legacy location autocomplete is still active in v4.js alongside i18n autocomplete');
  if(js.includes("request?.addEventListener('click',()=>document.getElementById('request')?.scrollIntoView")) warn('static','legacy config→request scroll handler still exists under modal controller');
  if(fs.existsSync('.github/workflows/locale-hotfix.yml')) warn('static','obsolete locale-hotfix workflow remains in repository');
  if(fs.existsSync('.github/workflows/apply-locale-v1.yml')) warn('static','one-shot apply-locale-v1 workflow remains in repository');
  if(locale.length>26000) warn('static',`locale runtime is large (${locale.length} bytes); review duplicated translation/runtime responsibilities`);
  if(js.length>50000) warn('static',`main runtime is large (${js.length} bytes); legacy blocks should be removed where superseded`);

  const cssAll=css+'\n'+localeCss+'\n'+modalCss;
  const importantCount=(cssAll.match(/!important/g)||[]).length;
  if(importantCount>90) warn('static',`CSS override stack contains ${importantCount} !important declarations`);

  const hardcodedDynamic=[
    ['Ride mode state',/name:'ТРЕК'|desc:'Максимальная отдача привода'|regen:'НИЗКАЯ'/],
    ['Configurator dynamic copy',/МОДУЛЬ|НЕ УСТАНОВЛЕНО|СБОРКА СОХРАНЕНА/],
    ['Activation dynamic copy',/ОТКЛЮЧИТЬ R1|ЗАПУСК\.\.\.|Система ожидает запуска/]
  ];
  hardcodedDynamic.forEach(([name,re])=>{if(re.test(js))warn('static',`${name} is hard-coded in RU inside v4.js and depends on mutation translation`)});
  if(!locale.includes('MutationObserver')) issue('static','locale runtime has no observer for dynamic UI text');
  if(!modal.includes('request-modal-open')) issue('static','request modal controller missing');
}

async function textNodesWithCyr(page,root='body',visibleOnly=false){
  return page.locator(root).evaluate((host,visibleOnly)=>{
    const out=[]; const seen=new Set();
    const walker=document.createTreeWalker(host,NodeFilter.SHOW_TEXT);
    const isVisible=el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)!==0&&r.width>0&&r.height>0;};
    let n;
    while((n=walker.nextNode())){
      const t=(n.nodeValue||'').replace(/\s+/g,' ').trim();
      if(!t||!/[А-Яа-яЁё]/.test(t))continue;
      const el=n.parentElement;
      if(!el||/^(SCRIPT|STYLE|NOSCRIPT)$/.test(el.tagName))continue;
      if(visibleOnly&&!isVisible(el))continue;
      const key=t;
      if(!seen.has(key)){seen.add(key);out.push(t);}
    }
    return out;
  },visibleOnly);
}

async function latinTextNodes(page,root='body',visibleOnly=true){
  return page.locator(root).evaluate((host,visibleOnly)=>{
    const out=[]; const seen=new Set();
    const walker=document.createTreeWalker(host,NodeFilter.SHOW_TEXT);
    const isVisible=el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)!==0&&r.width>0&&r.height>0;};
    let n;
    while((n=walker.nextNode())){
      const t=(n.nodeValue||'').replace(/\s+/g,' ').trim();
      if(!t||!/[A-Za-z]{3}/.test(t))continue;
      const el=n.parentElement;
      if(!el||/^(SCRIPT|STYLE|NOSCRIPT)$/.test(el.tagName))continue;
      if(visibleOnly&&!isVisible(el))continue;
      if(!seen.has(t)){seen.add(t);out.push(t);}
    }
    return out.slice(0,120);
  },visibleOnly);
}

async function attrCyr(page){
  return page.evaluate(()=>{
    const attrs=['aria-label','placeholder','title','alt'];
    const out=[];
    document.querySelectorAll('*').forEach(el=>attrs.forEach(a=>{const v=el.getAttribute(a);if(v&&/[А-Яа-яЁё]/.test(v))out.push(`${a}: ${v}`)}));
    return [...new Set(out)];
  });
}

async function basicDomAudit(page,scope,mobile){
  const dupIds=await page.evaluate(()=>{const m={};document.querySelectorAll('[id]').forEach(el=>(m[el.id]??=[]).push(el));return Object.entries(m).filter(([,v])=>v.length>1).map(([k,v])=>`${k}×${v.length}`)});
  if(dupIds.length)issue(scope,`duplicate IDs: ${dupIds.join(', ')}`);

  const overflow=await page.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}));
  if(overflow.sw>overflow.cw+3)issue(scope,`document horizontal overflow ${overflow.sw}px > ${overflow.cw}px`);

  const unnamed=await page.evaluate(()=>[...document.querySelectorAll('button')].filter(el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();if(s.display==='none'||s.visibility==='hidden'||r.width===0||r.height===0)return false;return !(el.getAttribute('aria-label')||el.textContent.trim()||el.getAttribute('title'));}).map(el=>el.id||el.className||'<button>'));
  if(unnamed.length)issue(scope,`visible buttons without accessible name: ${unnamed.join(', ')}`);

  const broken=await page.evaluate(()=>[...document.images].map(i=>({i,src:i.currentSrc||i.getAttribute('src')||''})).filter(x=>x.src&&x.i.complete&&x.i.naturalWidth===0).map(x=>x.src));
  if(broken.length)issue(scope,`broken images: ${broken.slice(0,5).join(', ')}`);

  if(mobile){
    const inputZoom=await page.evaluate(()=>[...document.querySelectorAll('input,textarea,select')].filter(el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&r.width>0&&parseFloat(s.fontSize)<16}).map(el=>`${el.id||el.name||el.tagName}:${getComputedStyle(el).fontSize}`));
    if(inputZoom.length)warn(scope,`mobile inputs below 16px (iOS zoom risk): ${inputZoom.join(', ')}`);
    const targetSel=['#menu','.header-lang button','#techClose','.request-modal-close','.gallery-lightbox-close'];
    for(const sel of targetSel){
      const loc=page.locator(sel).first();
      if(await loc.count()&&await loc.isVisible().catch(()=>false)){
        const b=await loc.boundingBox();
        if(b&&(b.width<40||b.height<40))warn(scope,`${sel} touch target ${Math.round(b.width)}×${Math.round(b.height)}px`);
      }
    }
  }
}

async function typographyAudit(page,scope){
  const report=await page.evaluate(()=>{
    const isVisible=el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0;};
    const tiny=[];document.querySelectorAll('p,button,input,small,figcaption,.eyebrow,label>span').forEach(el=>{if(!isVisible(el))return;const fs=parseFloat(getComputedStyle(el).fontSize);if(fs<7.5)tiny.push(`${el.tagName.toLowerCase()}.${String(el.className||'').split(' ').filter(Boolean).slice(0,2).join('.')}:${fs}px:${el.textContent.trim().slice(0,40)}`)});
    const clipped=[];document.querySelectorAll('h1,h2,h3,.mode-name,.request-step-title strong').forEach(el=>{if(!isVisible(el))return;const r=el.getBoundingClientRect();if(r.right>innerWidth+2||r.left<-2)clipped.push(`${el.tagName}.${el.className||''}:${Math.round(r.left)}..${Math.round(r.right)}`)});
    return {tiny:[...new Set(tiny)].slice(0,30),clipped};
  });
  if(report.tiny.length)warn(scope,`microtype <7.5px: ${report.tiny.join(' | ')}`);
  if(report.clipped.length)issue(scope,`heading/text viewport clipping: ${report.clipped.join(', ')}`);
}

async function assertEnglishClean(page,scope,root='body'){
  const bad=await textNodesWithCyr(page,root,false);
  if(bad.length)issue(scope,`Cyrillic remains in EN: ${bad.slice(0,30).join(' || ')}`);
}

async function exercise(page,lang,scope){
  // Ride System — all dynamic states.
  const modes=page.locator('.modes button');
  for(let i=0;i<await modes.count();i++){
    await modes.nth(i).click();
    await page.waitForTimeout(80);
    if(lang==='en')await assertEnglishClean(page,`${scope}:ride-${i}`,'#dash');
  }

  // Configurator dynamic content.
  const presets=page.locator('[data-preset]');
  for(let i=0;i<Math.min(await presets.count(),3);i++){
    await presets.nth(i).click();await page.waitForTimeout(50);
    if(lang==='en')await assertEnglishClean(page,`${scope}:config-${i}`,'#configurator');
  }
  const module=page.locator('[data-module]').first();
  if(await module.count()){await module.click();await page.waitForTimeout(50);if(lang==='en')await assertEnglishClean(page,`${scope}:config-module`,'#configurator');}

  // Tech profile.
  if(await page.locator('#techTrigger').count()){
    await page.locator('#techTrigger').click();await page.waitForTimeout(80);
    if(lang==='en')await assertEnglishClean(page,`${scope}:tech`,'#techSheet');
    await page.locator('#techClose').click();
  }

  // Gallery fullscreen.
  const firstGallery=page.locator('#rail figure img').first();
  if(await firstGallery.count()){
    await firstGallery.click();await page.waitForTimeout(80);
    if(lang==='en')await assertEnglishClean(page,`${scope}:gallery`,'.gallery-lightbox');
    const close=page.locator('.gallery-lightbox-close');if(await close.count())await close.click();
  }

  // Activation dynamic states.
  if(await page.locator('#activateBtn').count()){
    await page.locator('#activateBtn').click();await page.waitForTimeout(900);
    if(lang==='en')await assertEnglishClean(page,`${scope}:activation-live`,'#activate');
    const sw=page.locator('.sw');
    for(let i=0;i<await sw.count();i++){await sw.nth(i).click();await page.waitForTimeout(80);if(lang==='en')await assertEnglishClean(page,`${scope}:activation-swatch-${i}`,'#activate');}
  }

  // Request modal + hidden steps + location autocomplete runtime.
  if(await page.locator('#configRequest').count()){
    await page.locator('#configRequest').click();await page.waitForTimeout(120);
    if(lang==='en')await assertEnglishClean(page,`${scope}:request`,'#request');
    const requestVisible=await page.locator('#request').evaluate(el=>el.classList.contains('request-modal-open'));
    if(!requestVisible)issue(scope,'configRequest did not open request modal');

    await page.evaluate(()=>{
      const s=document.querySelector('[data-request-step="2"]');if(s)s.hidden=false;
      const country=document.getElementById('countryButton');if(country)country.dataset.iso='RU';
      window.dispatchEvent(new CustomEvent('vanta:countrychange',{detail:{iso:'RU'}}));
    });
    const oldRequests=[];
    const listener=req=>{const u=req.url();if(u.includes('/data/regions.json')||u.includes('/data/locations/'))oldRequests.push(u)};
    page.on('request',listener);
    const reg=page.locator('#reqRegion');
    if(await reg.count()){
      await reg.fill(lang==='en'?'A':'А');await page.waitForTimeout(350);
      const box=page.locator('#regionSuggest');
      const count=await box.locator('button[data-value]').count().catch(()=>0);
      if(!count)warn(scope,'region autocomplete produced no buttons in RU country test');
      if(count){
        const before=await reg.inputValue();
        await box.locator('button[data-value]').first().dispatchEvent('pointerdown');
        await page.waitForTimeout(30);
        const after=await reg.inputValue();
        if(before!==after)issue(scope,'region pointerdown still selects an item; touch-scroll regression risk');
        const scroll=await box.evaluate(el=>({h:el.scrollHeight,c:el.clientHeight,overflow:getComputedStyle(el).overflowY,touch:getComputedStyle(el).touchAction}));
        if(scroll.h>scroll.c&&scroll.overflow!=='auto'&&scroll.overflow!=='scroll')issue(scope,`suggestion list not scrollable: overflow-y=${scroll.overflow}`);
        if(!/pan-y|auto/.test(scroll.touch))warn(scope,`suggestion list touch-action=${scroll.touch}`);
      }
    }
    page.off('request',listener);
    if(oldRequests.length)issue(scope,`legacy location network requests fired: ${[...new Set(oldRequests)].join(', ')}`);

    const close=page.locator('.request-modal-close');if(await close.count())await close.click();
  }
}

async function runCase(browser,{name,width,height,isMobile,hasTouch,lang}){
  const scope=`${name}-${lang}`;
  const context=await browser.newContext({viewport:{width,height},isMobile,hasTouch,deviceScaleFactor:1});
  const page=await context.newPage();
  const consoleErrors=[];const pageErrors=[];
  page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text())});
  page.on('pageerror',e=>pageErrors.push(e.message));
  await page.goto(`${BASE}/?qa=full&lang=${lang}`,{waitUntil:'networkidle',timeout:60000});
  await page.waitForFunction(()=>window.vantaLocale&&document.documentElement.classList.contains('request-modal-ready'),null,{timeout:10000});
  const actual=await page.getAttribute('html','lang');if(actual!==lang)issue(scope,`html lang=${actual}`);
  await basicDomAudit(page,scope,isMobile);
  await typographyAudit(page,scope);

  if(lang==='en'){
    await assertEnglishClean(page,`${scope}:initial`);
    const badAttrs=await attrCyr(page);if(badAttrs.length)warn(scope,`Cyrillic remains in EN accessibility/media attrs: ${badAttrs.slice(0,25).join(' || ')}`);
  }else{
    const latin=await latinTextNodes(page,'body',true);note(scope,`visible Latin-bearing RU strings (${latin.length} sampled): ${latin.slice(0,50).join(' || ')}`);
  }

  await exercise(page,lang,scope);

  // Explicit switch QA.
  const target=lang==='ru'?'en':'ru';
  const button=page.locator(`.header-lang button[data-lang="${target}"]`);
  if(await button.count()){
    await button.click();await page.waitForTimeout(180);
    const afterLang=await page.getAttribute('html','lang');
    const hero=(await page.locator('.hero-white').textContent()||'').trim();
    if(afterLang!==target)issue(scope,`language switch failed: expected ${target}, got ${afterLang}`);
    if(target==='en'&&hero!=='Silence')issue(scope,`RU→EN hero is "${hero}"`);
    if(target==='ru'&&hero!=='Тишина')issue(scope,`EN→RU hero is "${hero}"`);
  }else issue(scope,'header language switch missing');

  if(consoleErrors.length)issue(scope,`console errors: ${consoleErrors.join(' || ')}`);
  if(pageErrors.length)issue(scope,`page errors: ${pageErrors.join(' || ')}`);
  await context.close();
}

staticAudit();
const browser=await chromium.launch({headless:true});
try{
  const cases=[
    {name:'mobile',width:390,height:844,isMobile:true,hasTouch:true,lang:'ru'},
    {name:'mobile',width:390,height:844,isMobile:true,hasTouch:true,lang:'en'},
    {name:'desktop',width:1440,height:1000,isMobile:false,hasTouch:false,lang:'ru'},
    {name:'desktop',width:1440,height:1000,isMobile:false,hasTouch:false,lang:'en'}
  ];
  for(const c of cases){console.log(`\n=== QA ${c.name} ${c.lang.toUpperCase()} ===`);await runCase(browser,c);}
}finally{await browser.close();}

console.log('\n=== FULL QA REPORT ===');
console.log(`ISSUES ${issues.length}`);issues.forEach(x=>console.log('ISSUE',x));
console.log(`WARNINGS ${warnings.length}`);warnings.forEach(x=>console.log('WARN',x));
console.log(`NOTES ${notes.length}`);notes.forEach(x=>console.log('NOTE',x));
if(issues.length)process.exitCode=2;
