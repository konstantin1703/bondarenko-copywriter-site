import fs from 'node:fs';
import { chromium } from 'playwright';

const BASE=process.env.BASE||'http://127.0.0.1:4173';
const failures=[];
const notes=[];
const fail=(scope,message)=>failures.push(`[${scope}] ${message}`);
const note=(scope,message)=>notes.push(`[${scope}] ${message}`);

function expectStatic(condition,message){
  if(!condition)fail('static',message);
}

function staticAudit(){
  const html=fs.readFileSync('index.html','utf8');
  const js=fs.readFileSync('v4.js','utf8');
  const locale=fs.readFileSync('v4-locale-v1.js','utf8');
  const modal=fs.readFileSync('v4-request-modal-v1.js','utf8');
  const bundle=fs.readFileSync('v4-bundle-v1.css','utf8');
  const cssSources=['v4.css','v4-locale-v1.css','v4-request-modal-v1.css','v4-typography-v1.css','v4-visual-v1.css','v4-impact-v1.css','v4-artdirection-v1.css'];

  expectStatic(html.includes('v4.js?v=18'),'v4.js cache-bust must be v18');
  expectStatic(html.includes('v4-locale-v1.js?v=6'),'locale cache-bust must be v6');
  expectStatic(html.includes('v4-request-modal-v1.js?v=5'),'request modal JS cache-bust must be v5');
  expectStatic(html.includes('v4-bundle-v1.css?v=3'),'consolidated CSS bundle link missing');
  expectStatic(!html.includes('v4.css?v=23'),'legacy core CSS must not be linked directly');
  expectStatic(!html.includes('v4-locale-v1.css?v=3'),'locale CSS must not be linked directly');
  expectStatic(!html.includes('v4-request-modal-v1.css?v=6'),'request modal CSS must not be linked directly');
  expectStatic(!html.includes('v4-typography-v1.css?v=1'),'typography CSS must not be linked directly');
  expectStatic(!html.includes('v4-visual-v1.css'),'stage 4 CSS must be delivered through the consolidated bundle only');
  expectStatic(bundle.includes('VANTA R1 — generated CSS bundle v1'),'generated bundle header missing');
  expectStatic(bundle.includes('Stage 2 / selective functional typography pass'),'stage 2 typography layer missing from bundle');
  expectStatic(bundle.includes('Stage 4 / visual + interaction polish'),'stage 4 visual UX layer missing from bundle');
  expectStatic(bundle.includes('iOS / WebKit tech-sheet close glyph'),'WebKit-safe tech close glyph missing from bundle');
  expectStatic(bundle.includes('Stage 6 / premium composition pass'),'stage 6 art-direction layer missing from bundle');
  for(const source of cssSources){
    const sourceCss=fs.readFileSync(source,'utf8').trim();
    expectStatic(bundle.includes(sourceCss),`consolidated bundle is stale or missing ${source}`);
  }

  expectStatic(!js.includes('"dial":"+381 p"'),'Serbia calling code typo regressed');
  expectStatic(js.includes('"dial":"+381"'),'Serbia calling code +381 missing');
  expectStatic(!locale.includes("cache:'no-store'"),'versioned location JSON must remain cacheable');

  expectStatic(html.includes('id="reqPhoneLabel"'),'phone label id missing');
  expectStatic(html.includes('aria-labelledby="reqPhoneLabel"'),'phone accessible label relationship missing');
  expectStatic(html.includes('aria-describedby="phoneHint"'),'phone hint relationship missing');

  expectStatic(modal.includes('setBackgroundInert'),'request modal background inert handling missing');
  expectStatic(modal.includes("if(e.key!=='Tab')return"),'request modal Tab focus trap missing');
  expectStatic(modal.includes("request-modal-close')?.focus"),'request modal initial focus handling missing');
  expectStatic(bundle.includes('font-size:16px!important'),'mobile request input 16px safeguard missing from bundle');
}

async function runCase(browser,{name,width,height,isMobile,lang,testSwitch=false}){
  const scope=`${name}-${lang}`;
  const context=await browser.newContext({viewport:{width,height},isMobile,hasTouch:isMobile,deviceScaleFactor:1});
  const page=await context.newPage();
  const consoleErrors=[];
  const pageErrors=[];

  page.on('console',msg=>{if(msg.type()==='error')consoleErrors.push(msg.text())});
  page.on('pageerror',err=>pageErrors.push(err.message));

  try{
    await page.goto(`${BASE}/?qa=smoke&lang=${lang}`,{waitUntil:'domcontentloaded',timeout:60000});
    await page.waitForFunction(()=>window.vantaLocale&&document.documentElement.classList.contains('request-modal-ready'),null,{timeout:15000});

    const identity=await page.evaluate(()=>({title:document.title,lang:document.documentElement.lang,body:document.body.innerText.trim().slice(0,120)}));
    if(identity.title!=='VANTA R1 — Electric Superbike Concept')fail(scope,`unexpected title: ${identity.title}`);
    if(identity.lang!==lang)fail(scope,`html lang=${identity.lang}, expected ${lang}`);
    if(identity.body.length<20)fail(scope,'page rendered as blank/near-blank');

    const dupIds=await page.evaluate(()=>{
      const counts=new Map();
      document.querySelectorAll('[id]').forEach(el=>counts.set(el.id,(counts.get(el.id)||0)+1));
      return [...counts].filter(([,count])=>count>1).map(([id,count])=>`${id}×${count}`);
    });
    if(dupIds.length)fail(scope,`duplicate IDs: ${dupIds.join(', ')}`);

    const overflow=await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth}));
    if(overflow.scrollWidth>overflow.clientWidth+3)fail(scope,`horizontal overflow ${overflow.scrollWidth}px > ${overflow.clientWidth}px`);

    const functionalType=await page.evaluate(()=>{
      const selectors=[
        ['config summary label','.config-stats small',8.5],
        ['config module description','.config-module-copy small',10],
        ['config module effect','.config-effect',8.5],
        ['config action','.config-actions button',9]
      ];
      return selectors.map(([name,selector,min])=>{
        const el=document.querySelector(selector);
        return {name,selector,min,size:el?parseFloat(getComputedStyle(el).fontSize):null};
      });
    });
    const tooSmallFunctional=functionalType.filter(row=>row.size===null||row.size+0.01<row.min);
    if(tooSmallFunctional.length)fail(scope,`functional typography below stage-2 floor: ${tooSmallFunctional.map(x=>`${x.name}:${x.size}px<${x.min}px`).join(', ')}`);

    const stage4UX=await page.evaluate(()=>{
      const nav=document.querySelector('.desktop-nav a');
      const sw=document.querySelector('.sw');
      const materialCaption=document.querySelector('.detail-triptych figcaption');
      return {
        navSize:nav?parseFloat(getComputedStyle(nav).fontSize):null,
        swWidth:sw?sw.getBoundingClientRect().width:null,
        swHeight:sw?sw.getBoundingClientRect().height:null,
        materialCaptionSize:materialCaption?parseFloat(getComputedStyle(materialCaption).fontSize):null
      };
    });
    if(!isMobile&&width>=1180&&(stage4UX.navSize===null||stage4UX.navSize<10))fail(scope,`desktop navigation below stage-4 floor: ${stage4UX.navSize}px`);
    if(isMobile&&((stage4UX.swWidth??0)<44||(stage4UX.swHeight??0)<44))fail(scope,`activation swatch touch target below 44px: ${stage4UX.swWidth}x${stage4UX.swHeight}`);
    if(stage4UX.materialCaptionSize===null||stage4UX.materialCaptionSize+0.01<8.5)fail(scope,`material caption below stage-4 floor: ${stage4UX.materialCaptionSize}px`);

    const phoneSemantics=await page.evaluate(()=>{
      const input=document.getElementById('reqPhone');
      return input?{
        labelledby:input.getAttribute('aria-labelledby'),
        describedby:input.getAttribute('aria-describedby'),
        labelExists:!!document.getElementById('reqPhoneLabel'),
        hintExists:!!document.getElementById('phoneHint')
      }:null;
    });
    if(!phoneSemantics||phoneSemantics.labelledby!=='reqPhoneLabel'||phoneSemantics.describedby!=='phoneHint'||!phoneSemantics.labelExists||!phoneSemantics.hintExists){
      fail(scope,'phone accessibility relationships are incomplete at runtime');
    }

    const trigger=page.locator('#configRequest');
    await trigger.scrollIntoViewIfNeeded();
    await trigger.click();
    await page.waitForFunction(()=>document.getElementById('request')?.classList.contains('request-modal-open'));
    await page.waitForTimeout(50);

    const modalState=await page.evaluate(()=>({
      activeClose:document.activeElement?.classList.contains('request-modal-close')||false,
      role:document.getElementById('request')?.getAttribute('role'),
      ariaModal:document.getElementById('request')?.getAttribute('aria-modal'),
      headerInert:document.getElementById('header')?.inert||false,
      heroInert:document.querySelector('.hero')?.inert||false,
      title:document.querySelector('.request-modal-title strong')?.textContent?.trim()
    }));
    if(!modalState.activeClose)fail(scope,'modal did not move focus to close button');
    if(modalState.role!=='dialog'||modalState.ariaModal!=='true')fail(scope,'modal ARIA state missing');
    if(!modalState.headerInert||!modalState.heroInert)fail(scope,'background is not inert while request modal is open');
    const requestType=await page.evaluate(()=>{
      const selectors=[
        ['request progress','.request-progress span',9],
        ['request field label','.request-field>span',9],
        ['request hint','.field-hint',innerWidth<=600?10:9.5],
        ['request action','.request-controls button',innerWidth<=600?9.5:9],
        ['request summary label','.request-summary-head small',8.5]
      ];
      return selectors.map(([name,selector,min])=>{
        const el=document.querySelector(selector);
        return {name,selector,min,size:el?parseFloat(getComputedStyle(el).fontSize):null};
      });
    });
    const requestTooSmall=requestType.filter(row=>row.size===null||row.size+0.01<row.min);
    if(requestTooSmall.length)fail(scope,`request functional typography below stage-2 floor: ${requestTooSmall.map(x=>`${x.name}:${x.size}px<${x.min}px`).join(', ')}`);
    const modalOverflow=await page.evaluate(()=>({sw:document.getElementById('request')?.scrollWidth||0,cw:document.getElementById('request')?.clientWidth||0}));
    if(modalOverflow.sw>modalOverflow.cw+3)fail(scope,`request modal horizontal overflow ${modalOverflow.sw}px > ${modalOverflow.cw}px`);
    const expectedModalTitle=lang==='en'?'R1 REQUEST':'ОФОРМЛЕНИЕ R1';
    if(modalState.title!==expectedModalTitle)fail(scope,`request modal localization mismatch: ${modalState.title}`);

    await page.locator('.request-modal-close').focus();
    await page.keyboard.press('Shift+Tab');
    const trappedBackward=await page.evaluate(()=>document.getElementById('request')?.contains(document.activeElement)||false);
    if(!trappedBackward)fail(scope,'Shift+Tab escaped request modal');
    await page.keyboard.press('Tab');
    const wrappedToStart=await page.evaluate(()=>document.activeElement?.classList.contains('request-modal-close')||false);
    if(!wrappedToStart)fail(scope,'Tab did not wrap from last focusable back to modal start');

    if(isMobile){
      const inputSizes=await page.evaluate(()=>[...document.querySelectorAll('#request.request-modal-open input')]
        .filter(el=>el.getClientRects().length>0)
        .map(el=>({id:el.id,size:parseFloat(getComputedStyle(el).fontSize)})));
      const tooSmall=inputSizes.filter(row=>row.size<16);
      if(tooSmall.length)fail(scope,`visible mobile request inputs below 16px: ${tooSmall.map(x=>`${x.id}:${x.size}`).join(', ')}`);

      await page.locator('#phoneRegionButton').click();
      await page.waitForFunction(()=>document.getElementById('regionPicker')?.open===true);
      const regionSearchSize=await page.locator('#regionSearch').evaluate(el=>parseFloat(getComputedStyle(el).fontSize));
      if(regionSearchSize<16)fail(scope,`mobile region search is ${regionSearchSize}px`);
      await page.locator('#regionPickerClose').click();
    }

    await page.locator('.request-modal-close').focus();
    await page.keyboard.press('Escape');
    await page.waitForFunction(()=>!document.getElementById('request')?.classList.contains('request-modal-open'));
    await page.waitForTimeout(30);

    const closedState=await page.evaluate(()=>({
      returned:document.activeElement?.id==='configRequest',
      headerInert:document.getElementById('header')?.inert||false,
      heroInert:document.querySelector('.hero')?.inert||false,
      role:document.getElementById('request')?.getAttribute('role')
    }));
    if(!closedState.returned)fail(scope,'focus did not return to request trigger after Escape');
    if(closedState.headerInert||closedState.heroInert)fail(scope,'background inert state was not restored after modal close');
    if(closedState.role!==null)fail(scope,'dialog role remained after modal close');

    if(testSwitch){
      const target=lang==='en'?'ru':'en';
      await page.locator(`.header-lang button[data-lang="${target}"]`).evaluate(el=>el.click());
      await page.waitForFunction(expected=>document.documentElement.lang===expected,target);
      const switched=await page.evaluate(()=>({lang:document.documentElement.lang,url:new URL(location.href).searchParams.get('lang')}));
      if(switched.lang!==target||switched.url!==target)fail(scope,`language switch failed: lang=${switched.lang}, url=${switched.url}`);
    }

    note(scope,'render, bundle integrity, stage-4 UX floors, modal accessibility, responsive input sizing and locale checks passed');
  }catch(error){
    fail(scope,`exception: ${error?.stack||error}`);
  }

  if(pageErrors.length)fail(scope,`page errors: ${pageErrors.join(' | ')}`);
  if(consoleErrors.length)fail(scope,`console errors: ${consoleErrors.join(' | ')}`);
  await context.close();
}

staticAudit();

const browser=await chromium.launch({headless:true});
try{
  await runCase(browser,{name:'desktop',width:1440,height:1000,isMobile:false,lang:'ru',testSwitch:true});
  await runCase(browser,{name:'desktop',width:1440,height:1000,isMobile:false,lang:'en'});
  await runCase(browser,{name:'mobile',width:390,height:844,isMobile:true,lang:'ru'});
  await runCase(browser,{name:'mobile',width:390,height:844,isMobile:true,lang:'en'});
}finally{
  await browser.close();
}

console.log('\nVANTA R1 permanent smoke QA');
for(const line of notes)console.log(`PASS ${line}`);
if(failures.length){
  console.error(`\nFAILURES (${failures.length})`);
  for(const line of failures)console.error(`FAIL ${line}`);
  process.exitCode=1;
}else{
  console.log('\nAll smoke checks passed.');
}
