import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const BASE='http://127.0.0.1:4173';
const OUT='artifacts/stage5';
fs.mkdirSync(OUT,{recursive:true});

const cases=[
  {name:'desktop',width:1440,height:1000,isMobile:false},
  {name:'mobile',width:390,height:844,isMobile:true}
];
const sections=[
  ['performance','#performance'],
  ['architecture','#architecture'],
  ['materials','#materials'],
  ['gallery','#gallery'],
  ['system','#system'],
  ['configurator','#configurator'],
  ['activate','#activate']
];

const browser=await chromium.launch({headless:true});
try{
  for(const c of cases){
    const context=await browser.newContext({viewport:{width:c.width,height:c.height},isMobile:c.isMobile,hasTouch:c.isMobile,deviceScaleFactor:1});
    const page=await context.newPage();
    await page.goto(`${BASE}/?qa=stage5&lang=ru`,{waitUntil:'domcontentloaded',timeout:60000});
    await page.waitForFunction(()=>window.vantaLocale&&document.documentElement.classList.contains('request-modal-ready'),null,{timeout:15000});
    await Promise.race([page.evaluate(()=>document.fonts?.ready),page.waitForTimeout(3000)]);

    await page.waitForTimeout(850);
    await page.screenshot({path:path.join(OUT,`${c.name}-hero-motion.png`)});

    await page.addStyleTag({content:`
      html{scroll-behavior:auto!important}
      *,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}
      .reveal{opacity:1!important;transform:none!important}
      .hero-copy .eyebrow,.hero-copy .hero-title>span,.hero-copy>p,.hero-mark,.spec-strip>div{opacity:1!important;transform:none!important;filter:none!important}
    `});
    await page.evaluate(async()=>{
      const sleep=ms=>new Promise(r=>setTimeout(r,ms));
      const h=Math.max(document.body.scrollHeight,document.documentElement.scrollHeight);
      for(let y=0;y<h;y+=Math.max(500,innerHeight*.75)){
        scrollTo(0,y);
        await sleep(28);
      }
      scrollTo(0,0);
      await sleep(120);
    });

    await page.screenshot({path:path.join(OUT,`${c.name}-full.png`),fullPage:true,animations:'disabled'});

    for(const [name,selector] of sections){
      const loc=page.locator(selector).first();
      if(!await loc.count())continue;
      await loc.scrollIntoViewIfNeeded();
      await page.waitForTimeout(50);
      await loc.screenshot({path:path.join(OUT,`${c.name}-${name}.png`),animations:'disabled'});
    }

    await context.close();
  }
}finally{
  await browser.close();
}

console.log('Stage 5 screenshots captured.');
