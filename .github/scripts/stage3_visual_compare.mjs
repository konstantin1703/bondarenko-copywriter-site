import pixelmatch from 'pixelmatch';
import { PNG } from 'pngjs';
import { chromium } from 'playwright';

const BASELINE=process.env.BASELINE_URL||'http://127.0.0.1:4173';
const CANDIDATE=process.env.CANDIDATE_URL||'http://127.0.0.1:4174';
const MAX_RATIO=0.0005;
const failures=[];

const cases=[
  {name:'desktop-ru',width:1440,height:1000,isMobile:false,lang:'ru'},
  {name:'desktop-en',width:1440,height:1000,isMobile:false,lang:'en'},
  {name:'mobile-ru',width:390,height:844,isMobile:true,lang:'ru'},
  {name:'mobile-en',width:390,height:844,isMobile:true,lang:'en'}
];

async function settle(page,base,c){
  await page.goto(`${base}/?qa=stage3&lang=${c.lang}`,{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>window.vantaLocale&&document.documentElement.classList.contains('request-modal-ready'),null,{timeout:15000});
  await page.addStyleTag({content:`
    html{scroll-behavior:auto!important}
    *,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}
    .reveal{opacity:1!important;transform:none!important}
  `});
  await page.evaluate(async()=>{
    if(document.fonts?.ready)await document.fonts.ready;
    const h=Math.max(document.body.scrollHeight,document.documentElement.scrollHeight);
    for(let y=0;y<h;y+=Math.max(500,innerHeight*.8)){
      scrollTo(0,y);
      await new Promise(r=>setTimeout(r,20));
    }
    scrollTo(0,0);
    await Promise.all([...document.images].map(img=>img.complete?Promise.resolve():new Promise(r=>{img.addEventListener('load',r,{once:true});img.addEventListener('error',r,{once:true})})));
    await Promise.all([...document.images].map(img=>img.decode?.().catch(()=>{})||Promise.resolve()));
  });
  await page.waitForTimeout(80);
}

function comparePng(scope,aBuffer,bBuffer){
  const a=PNG.sync.read(aBuffer);
  const b=PNG.sync.read(bBuffer);
  if(a.width!==b.width||a.height!==b.height){
    failures.push(`${scope}: dimensions differ ${a.width}x${a.height} vs ${b.width}x${b.height}`);
    return;
  }
  const diff=new PNG({width:a.width,height:a.height});
  const pixels=pixelmatch(a.data,b.data,diff.data,a.width,a.height,{threshold:0.1,includeAA:false});
  const ratio=pixels/(a.width*a.height);
  console.log(`COMPARE ${scope}: ${(ratio*100).toFixed(4)}% mismatch`);
  if(ratio>MAX_RATIO)failures.push(`${scope}: ${(ratio*100).toFixed(4)}% pixel mismatch > ${(MAX_RATIO*100).toFixed(4)}%`);
}

async function fingerprint(page){
  return page.evaluate(()=>{
    const selectors=['body','.header','.hero','.performance','#configurator','.config-summary','.config-module','.request-field input','footer'];
    const props=['display','position','fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','color','backgroundColor','borderTopColor','paddingTop','paddingRight','paddingBottom','paddingLeft','marginTop','marginRight','marginBottom','marginLeft','gridTemplateColumns','gap'];
    return selectors.map(selector=>{
      const el=document.querySelector(selector);
      if(!el)return {selector,missing:true};
      const cs=getComputedStyle(el);
      const r=el.getBoundingClientRect();
      const styles=Object.fromEntries(props.map(p=>[p,cs[p]]));
      return {selector,rect:[r.x,r.y,r.width,r.height].map(v=>Math.round(v*100)/100),styles};
    });
  });
}

const browser=await chromium.launch({headless:true});
try{
  for(const c of cases){
    const context=await browser.newContext({viewport:{width:c.width,height:c.height},isMobile:c.isMobile,hasTouch:c.isMobile,deviceScaleFactor:1});
    const baseline=await context.newPage();
    const candidate=await context.newPage();
    await settle(baseline,BASELINE,c);
    await settle(candidate,CANDIDATE,c);

    const [fpA,fpB]=await Promise.all([fingerprint(baseline),fingerprint(candidate)]);
    if(JSON.stringify(fpA)!==JSON.stringify(fpB))failures.push(`${c.name}: computed-style/layout fingerprint differs`);

    const [fullA,fullB]=await Promise.all([
      baseline.screenshot({fullPage:true,animations:'disabled'}),
      candidate.screenshot({fullPage:true,animations:'disabled'})
    ]);
    comparePng(`${c.name}/full-page`,fullA,fullB);

    for(const page of [baseline,candidate]){
      const trigger=page.locator('#configRequest');
      await trigger.scrollIntoViewIfNeeded();
      await trigger.click();
      await page.waitForFunction(()=>document.getElementById('request')?.classList.contains('request-modal-open'));
      await page.waitForTimeout(40);
    }
    const [modalA,modalB]=await Promise.all([
      baseline.screenshot({animations:'disabled'}),
      candidate.screenshot({animations:'disabled'})
    ]);
    comparePng(`${c.name}/request-modal`,modalA,modalB);

    await context.close();
  }
}finally{
  await browser.close();
}

if(failures.length){
  console.error(`\nStage 3 visual regression failures (${failures.length})`);
  failures.forEach(x=>console.error(`FAIL ${x}`));
  process.exitCode=1;
}else{
  console.log('\nStage 3 visual regression guard passed: baseline and consolidated bundle are visually equivalent.');
}
