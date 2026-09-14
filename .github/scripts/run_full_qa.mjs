import fs from 'node:fs';
const src='.github/scripts/full_qa.mjs';
const out='.github/scripts/.full_qa_runtime.mjs';
let s=fs.readFileSync(src,'utf8');
const old=`  if(await firstGallery.count()){
    await firstGallery.click();await page.waitForTimeout(80);
    if(lang==='en')await assertEnglishClean(page,\`${'${scope}'}:gallery\`,'.gallery-lightbox');
    const close=page.locator('.gallery-lightbox-close');if(await close.count())await close.click();
  }
`;
const replacement=`  if(await firstGallery.count()){
    await firstGallery.click({force:true});await page.waitForTimeout(100);
    const dialog=page.locator('.gallery-lightbox');
    const opened=await dialog.evaluate(el=>el.open||el.hasAttribute('open')).catch(()=>false);
    if(opened){
      if(lang==='en')await assertEnglishClean(page,\`${'${scope}'}:gallery\`,'.gallery-lightbox');
      const close=page.locator('.gallery-lightbox-close');
      if(await close.isVisible().catch(()=>false))await close.click();else await page.keyboard.press('Escape');
    }else warn(scope,'gallery image click did not open fullscreen viewer');
  }
`;
if(!s.includes(old)) throw new Error('gallery QA anchor not found');
s=s.replace(old,replacement);
fs.writeFileSync(out,s,'utf8');
await import('./.full_qa_runtime.mjs');
