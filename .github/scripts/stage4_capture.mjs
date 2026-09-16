import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const BASE='http://127.0.0.1:4173';
const OUT='artifacts/stage4';
fs.mkdirSync(OUT,{recursive:true});

const cases=[
  {name:'desktop',width:1440,height:1000,isMobile:false,lang:'ru'},
  {name:'mobile',width:390,height:844,isMobile:true,lang:'ru'}
];

const sections=[
  ['hero','.hero'],
  ['performance','#performance'],
  ['architecture','#architecture'],
  ['materials','#materials'],
  ['gallery','#gallery'],
  ['system','#system'],
  ['configurator','#configurator'],
  ['activate','#activate']
];

async function settle(page,c){
  await page.goto(`${BASE}/?qa=stage4&lang=${c.lang}`,{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>window.vantaLocale&&document.documentElement.classList.contains('request-modal-ready'),null,{timeout:15000});
  await page.addStyleTag({content:`
    html{scroll-behavior:auto!important}
    *,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}
    .reveal{opacity:1!important;transform:none!important}
  `});
  await page.evaluate(async()=>{
    const sleep=ms=>new Promise(r=>setTimeout(r,ms));
    await Promise.race([document.fonts?.ready||Promise.resolve(),sleep(3000)]);
    const h=Math.max(document.body.scrollHeight,document.documentElement.scrollHeight);
    for(let y=0;y<h;y+=Math.max(500,innerHeight*.75)){
      scrollTo(0,y);
      await sleep(25);
    }
    scrollTo(0,0);
    await sleep(150);
  });
}

const browser=await chromium.launch({headless:true});
try{
  for(const c of cases){
    const context=await browser.newContext({viewport:{width:c.width,height:c.height},isMobile:c.isMobile,hasTouch:c.isMobile,deviceScaleFactor:1});
    const page=await context.newPage();
    await settle(page,c);

    await page.screenshot({path:path.join(OUT,`${c.name}-full.png`),fullPage:true,animations:'disabled'});

    for(const [name,selector] of sections){
      const loc=page.locator(selector).first();
      if(await loc.count()){
        await loc.scrollIntoViewIfNeeded();
        await page.waitForTimeout(50);
        await loc.screenshot({path:path.join(OUT,`${c.name}-${name}.png`),animations:'disabled'});
      }
    }

    const trigger=page.locator('#configRequest');
    if(await trigger.count()){
      await trigger.scrollIntoViewIfNeeded();
      await trigger.click();
      await page.waitForFunction(()=>document.getElementById('request')?.classList.contains('request-modal-open'));
      await page.waitForTimeout(80);
      await page.screenshot({path:path.join(OUT,`${c.name}-request-modal.png`),animations:'disabled'});
    }

    await context.close();
  }
}finally{
  await browser.close();
}

console.log('Stage 4 screenshots captured.');
