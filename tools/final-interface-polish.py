from pathlib import Path

index_path=Path('index.html')
css_path=Path('v4.css')
js_path=Path('v4.js')
html=index_path.read_text()
css=css_path.read_text()
js=js_path.read_text()

# --- TECH SHEET semantic grouping ---
old_grid='''<div class="tech-grid">
<div><strong>210</strong><span>кВт / TARGET POWER</span></div>
<div><strong>390</strong><span>Н·м / PEAK TORQUE</span></div>
<div><strong>800</strong><span>V / ARCHITECTURE</span></div>
<div><strong>189</strong><span>кг / TARGET MASS</span></div>
<div><strong>320</strong><span>км / TARGET RANGE</span></div>
<div><strong>18</strong><span>мин / 10—80% TARGET</span></div>
</div>'''
new_grid='''<div class="tech-grid">
<section class="tech-group" aria-label="Drive"><small>01 / DRIVE</small><div class="tech-metric"><strong>210</strong><span>кВт / TARGET POWER</span></div><div class="tech-metric"><strong>390</strong><span>Н·м / PEAK TORQUE</span></div></section>
<section class="tech-group" aria-label="Energy"><small>02 / ENERGY</small><div class="tech-metric"><strong>800</strong><span>V / ARCHITECTURE</span></div><div class="tech-metric"><strong>18</strong><span>мин / 10—80% TARGET</span></div></section>
<section class="tech-group" aria-label="Vehicle"><small>03 / VEHICLE</small><div class="tech-metric"><strong>189</strong><span>кг / TARGET MASS</span></div><div class="tech-metric"><strong>320</strong><span>км / TARGET RANGE</span></div></section>
</div>'''
if old_grid not in html:
    raise SystemExit('TECH SHEET grid signature not found')
html=html.replace(old_grid,new_grid,1)
if 'v4.css?v=15' not in html or 'v4.js?v=9' not in html:
    raise SystemExit('Unexpected asset versions')
html=html.replace('v4.css?v=15','v4.css?v=16',1).replace('v4.js?v=9','v4.js?v=10',1)

# --- Collapse the two most recent tail override layers into one production block ---
cut_marker='/* VANTA R1 — gallery close + single OEM mode indicator 2026-09 */'
if cut_marker not in css:
    raise SystemExit('Expected tail override marker not found')
css=css.split(cut_marker,1)[0].rstrip()+"\n\n"

final_css=r'''/* VANTA R1 — Final Interface Polish 2026-09 */
:root{
  --control-line:#454944;
  --control-line-hover:#747a74;
  --control-bg:#090a09;
  --control-bg-hover:#101110;
}

/* One clean OEM mode indicator — no inset duplicate lines. */
.modes button.active{box-shadow:none!important}
.modes button.active:after{
  content:""!important;
  position:absolute!important;
  left:20%!important;
  right:20%!important;
  bottom:7px!important;
  height:2px!important;
  border-radius:999px!important;
  background:var(--dash-accent)!important;
  box-shadow:0 0 6px color-mix(in srgb,var(--dash-accent) 22%,transparent)!important;
}

/* Unified tactile language for interactive controls. */
.gallery-controls button,.gallery-lightbox-nav,.gallery-lightbox-close,#techClose,.tech-trigger,.sw,.menu{
  -webkit-tap-highlight-color:transparent;
}
.gallery-controls button,.gallery-lightbox-nav{
  border-color:var(--control-line)!important;
  background:rgba(8,9,8,.86)!important;
  color:#e9ebe8!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.035),0 8px 22px rgba(0,0,0,.2);
  transition:transform .18s ease,border-color .2s ease,background .2s ease,opacity .2s ease!important;
}
.gallery-controls button:active,.gallery-lightbox-nav:active{transform:scale(.94)}
@media(hover:hover) and (pointer:fine){
  .gallery-controls button:hover,.gallery-lightbox-nav:hover{border-color:var(--control-line-hover)!important;background:var(--control-bg-hover)!important;color:#fff!important}
}
.tech-trigger{
  border-color:#393d39!important;
  background:linear-gradient(180deg,rgba(255,255,255,.014),rgba(255,255,255,.003))!important;
  transition:transform .18s ease,border-color .22s ease,color .22s ease,background .22s ease!important;
}
.tech-trigger:active{transform:translateY(1px)}
.activate-btn{transition:transform .18s ease,filter .25s ease,background .25s ease!important}
.activate-btn:active{transform:translateY(1px) scale(.995)!important}

/* Gallery + TECH SHEET share the same VANTA close control. */
.gallery-lightbox-close,#techClose{
  position:relative!important;
  display:grid!important;
  place-items:center!important;
  width:46px!important;
  height:46px!important;
  min-width:46px!important;
  min-height:46px!important;
  padding:0!important;
  border-radius:50%!important;
  border:1px solid var(--control-line)!important;
  background:radial-gradient(circle at 35% 28%,rgba(255,255,255,.055),transparent 34%),var(--control-bg)!important;
  color:transparent!important;
  font-size:0!important;
  line-height:0!important;
  appearance:none!important;
  -webkit-appearance:none!important;
  outline:none!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.045),0 8px 22px rgba(0,0,0,.28)!important;
  transition:transform .18s ease,border-color .2s ease,background .2s ease,box-shadow .2s ease!important;
  cursor:pointer;
}
.gallery-lightbox-close:before,.gallery-lightbox-close:after,#techClose:before,#techClose:after{
  content:""!important;
  position:absolute!important;
  width:17px!important;
  height:1.5px!important;
  border-radius:99px!important;
  background:#e8eae7!important;
  box-shadow:0 0 5px rgba(255,255,255,.08)!important;
}
.gallery-lightbox-close:before,#techClose:before{transform:rotate(45deg)!important}
.gallery-lightbox-close:after,#techClose:after{transform:rotate(-45deg)!important}
.gallery-lightbox-close:focus,#techClose:focus{outline:none!important}
.gallery-lightbox-close:active,#techClose:active{
  transform:scale(.94)!important;
  border-color:color-mix(in srgb,var(--accent) 68%,#575957)!important;
  background:#0d0908!important;
  box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 20%,transparent),0 0 15px color-mix(in srgb,var(--accent) 11%,transparent)!important;
}
@media(hover:hover) and (pointer:fine){
  .gallery-lightbox-close:hover,#techClose:hover{border-color:var(--control-line-hover)!important;background:var(--control-bg-hover)!important;transform:translateY(-1px)}
  .gallery-lightbox-close:focus-visible,#techClose:focus-visible{outline:none!important;box-shadow:0 0 0 1px #c9ccc9,0 0 0 4px rgba(255,46,27,.11),0 8px 22px rgba(0,0,0,.28)!important}
}

/* TECH SHEET: grouped engineering data with staged reveal. */
.tech-sheet-panel{padding:30px}
.tech-sheet-head{padding-bottom:24px}
.tech-grid{
  display:grid!important;
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:12px!important;
  margin-top:24px!important;
  border:0!important;
  background:none!important;
}
.tech-group{
  min-width:0;
  border:1px solid #292d29;
  background:linear-gradient(180deg,rgba(255,255,255,.012),rgba(255,255,255,.002));
}
.tech-group>small{
  display:block;
  padding:12px 14px;
  border-bottom:1px solid #292d29;
  font-size:7px;
  letter-spacing:.18em;
  color:#777e78;
}
.tech-metric{
  min-height:132px;
  padding:18px 14px 16px;
  display:flex;
  flex-direction:column;
  justify-content:flex-end;
  border-bottom:1px solid #242824;
  opacity:0;
  transform:translateY(10px);
  transition:opacity .42s var(--motion-ease),transform .48s var(--motion-ease);
}
.tech-metric:last-child{border-bottom:0}
.tech-metric strong{font-family:"Inter Tight","Inter",sans-serif;font-size:48px;font-weight:500;line-height:.9;letter-spacing:-.055em;font-variant-numeric:tabular-nums lining-nums}
.tech-metric span{margin-top:11px;font-size:7.5px;line-height:1.35;letter-spacing:.12em;color:#858b85}
.tech-sheet[open] .tech-metric{opacity:1;transform:none}
.tech-sheet[open] .tech-group:nth-child(1) .tech-metric:nth-of-type(1){transition-delay:.06s}
.tech-sheet[open] .tech-group:nth-child(1) .tech-metric:nth-of-type(2){transition-delay:.11s}
.tech-sheet[open] .tech-group:nth-child(2) .tech-metric:nth-of-type(1){transition-delay:.14s}
.tech-sheet[open] .tech-group:nth-child(2) .tech-metric:nth-of-type(2){transition-delay:.19s}
.tech-sheet[open] .tech-group:nth-child(3) .tech-metric:nth-of-type(1){transition-delay:.22s}
.tech-sheet[open] .tech-group:nth-child(3) .tech-metric:nth-of-type(2){transition-delay:.27s}

/* Premium lightbox: calmer entry, tighter caption, tactile swipe feedback. */
.gallery-lightbox[open]{animation:vantaLightboxFade .22s ease}
.gallery-lightbox-stage img{
  transform:translate3d(var(--lightbox-drag,0px),0,0)!important;
  transition:transform .24s var(--motion-ease),opacity .2s ease!important;
  will-change:transform;
}
.gallery-lightbox[open] .gallery-lightbox-stage img{animation:vantaLightboxMediaIn .34s var(--motion-ease)}
.gallery-lightbox.is-swiping .gallery-lightbox-stage img{transition:none!important}
.gallery-lightbox-caption{min-height:64px!important;padding-top:11px!important;padding-bottom:11px!important;background:#050605!important}
.gallery-lightbox-caption strong{font-size:9.5px!important}
.gallery-lightbox-caption span{font-size:8.5px!important}
@keyframes vantaLightboxFade{from{opacity:.72}to{opacity:1}}
@keyframes vantaLightboxMediaIn{from{opacity:.35;transform:translate3d(0,7px,0) scale(.985)}to{opacity:1;transform:translate3d(0,0,0) scale(1)}}

/* Activation: short lock confirmation after a live light-signature change. */
.activation-stage.signature-locking .boot-hud strong{color:var(--accent)!important;text-shadow:0 0 11px color-mix(in srgb,var(--accent) 34%,transparent)}
.activation-stage.signature-locked .boot-hud strong{color:#f0f3f0!important;text-shadow:0 0 8px color-mix(in srgb,var(--accent) 18%,transparent)}
.activation-stage.signature-locked .boot-hud:after{
  content:"";
  width:28px;
  height:1px;
  justify-self:end;
  margin-top:2px;
  background:var(--accent);
  box-shadow:0 0 8px color-mix(in srgb,var(--accent) 24%,transparent);
  animation:vantaLockLine .28s var(--motion-ease);
}
@keyframes vantaLockLine{from{width:0;opacity:.2}to{width:28px;opacity:1}}

/* Mobile speed readout calibration: all 062 / 084 / 146 stay centered inside the inner dial. */
@media(max-width:520px){
  .modes button.active:after{left:18%!important;right:18%!important;bottom:7px!important;height:2px!important}
  .gallery-lightbox-close,#techClose{width:44px!important;height:44px!important;min-width:44px!important;min-height:44px!important}
  .speed-readout{transform:translateY(-27px)!important}
  .speed-readout strong{font-size:clamp(62px,16vw,68px)!important;line-height:.8!important;letter-spacing:-.065em!important;transform:scaleX(.9)!important;transform-origin:center!important}
  .speed-readout small{letter-spacing:.17em!important}
  .speed-readout i{margin-top:8px!important;letter-spacing:.12em!important}
  .tech-sheet-panel{padding:18px}
  .tech-grid{grid-template-columns:1fr!important;gap:9px!important;margin-top:18px!important}
  .tech-group{display:grid;grid-template-columns:78px repeat(2,minmax(0,1fr));align-items:stretch}
  .tech-group>small{display:flex;align-items:center;padding:10px;border:0;border-right:1px solid #292d29;font-size:6.5px;line-height:1.45}
  .tech-metric{min-height:96px;padding:13px 10px;border-bottom:0;border-right:1px solid #242824}
  .tech-metric:last-child{border-right:0}
  .tech-metric strong{font-size:34px}
  .tech-metric span{font-size:6.5px;letter-spacing:.09em}
  .gallery-lightbox-caption{min-height:74px!important;padding:9px 64px calc(9px + env(safe-area-inset-bottom))!important}
}
@media(max-width:390px){
  .speed-readout{transform:translateY(-25px)!important}
  .speed-readout strong{font-size:clamp(60px,16vw,64px)!important;transform:scaleX(.9)!important}
  .tech-group{grid-template-columns:66px repeat(2,minmax(0,1fr))}
  .tech-metric strong{font-size:31px}
}
@media(prefers-reduced-motion:reduce){
  .tech-metric,.gallery-lightbox[open],.gallery-lightbox[open] .gallery-lightbox-stage img,.activation-stage.signature-locked .boot-hud:after{animation:none!important;transition:none!important}
}
'''
css+=final_css.strip()+"\n"

# --- JS polish: live signature lock + tactile lightbox drag ---
js_marker='/* VANTA R1 — Final Interface Polish 2026-09 */'
if js_marker not in js:
    js += r'''

/* VANTA R1 — Final Interface Polish 2026-09 */
(()=>{
  'use strict';
  const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* A live color switch is a recalibration, not a reboot. */
  const stage=document.getElementById('stage');
  const bootStatus=document.getElementById('bootStatus');
  let lockTimerA=0,lockTimerB=0;
  document.querySelectorAll('.sw').forEach(sw=>sw.addEventListener('click',()=>{
    if(!stage?.classList.contains('stage-live')||!bootStatus)return;
    clearTimeout(lockTimerA);clearTimeout(lockTimerB);
    stage.classList.remove('signature-locking','signature-locked');
    void stage.offsetWidth;
    stage.classList.add('signature-locking');
    bootStatus.textContent='CALIBRATING';
    if(reduceMotion){bootStatus.textContent='SYSTEM ACTIVE';stage.classList.remove('signature-locking');return;}
    lockTimerA=setTimeout(()=>{
      stage.classList.remove('signature-locking');
      stage.classList.add('signature-locked');
      bootStatus.textContent='SIGNATURE LOCKED';
    },330);
    lockTimerB=setTimeout(()=>{
      stage.classList.remove('signature-locked');
      bootStatus.textContent='SYSTEM ACTIVE';
    },760);
  }));

  /* Give the fullscreen image a small physical response while the existing swipe logic changes frames. */
  const dialog=document.querySelector('.gallery-lightbox');
  const lightboxStage=dialog?.querySelector('.gallery-lightbox-stage');
  const lightboxImage=lightboxStage?.querySelector('img');
  if(dialog&&lightboxStage&&lightboxImage&&!reduceMotion){
    let startX=0;
    let dragging=false;
    lightboxStage.addEventListener('touchstart',e=>{
      startX=e.touches[0]?.clientX||0;
      dragging=true;
      dialog.classList.add('is-swiping');
    },{passive:true});
    lightboxStage.addEventListener('touchmove',e=>{
      if(!dragging)return;
      const x=e.touches[0]?.clientX||startX;
      const dx=Math.max(-54,Math.min(54,(x-startX)*.22));
      lightboxImage.style.setProperty('--lightbox-drag',`${dx}px`);
    },{passive:true});
    const settle=()=>{
      if(!dragging)return;
      dragging=false;
      dialog.classList.remove('is-swiping');
      requestAnimationFrame(()=>lightboxImage.style.setProperty('--lightbox-drag','0px'));
    };
    lightboxStage.addEventListener('touchend',settle,{passive:true});
    lightboxStage.addEventListener('touchcancel',settle,{passive:true});
  }
})();
'''

index_path.write_text(html)
css_path.write_text(css)
js_path.write_text(js)

# --- static validation ---
assert html.count('id="techSheet"')==1
assert html.count('class="tech-group"')==3
assert 'v4.css?v=16' in html and 'v4.js?v=10' in html
assert css.count('{')==css.count('}')
assert css.count('Final Interface Polish 2026-09')==1
assert 'shared close control + mobile speed alignment' not in css
assert 'gallery close + single OEM mode indicator' not in css
assert js.count('Final Interface Polish 2026-09')==1
print('final interface polish prepared')
