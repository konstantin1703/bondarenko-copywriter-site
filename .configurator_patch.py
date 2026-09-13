from pathlib import Path
import re

root=Path('.')
index_path=root/'index.html'
css_path=root/'v4.css'
js_path=root/'v4.js'
index=index_path.read_text(encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
js=js_path.read_text(encoding='utf-8')

SECTION='''
<section class="configurator chapter" id="configurator">
  <div class="config-head reveal">
    <div>
      <div class="eyebrow">07 / R1 CONFIGURATOR / YOUR R1</div>
      <h2>Собери свой<br/><em>характер R1.</em></h2>
    </div>
    <p>Выбери базовый профиль, добавь нужные модули и сразу увидишь, как меняются характер, масса, запас хода и итоговая конфигурация.</p>
  </div>
  <div class="config-layout">
    <div class="config-preview reveal">
      <div class="config-preview-media" data-tone="red" id="configPreview">
        <img alt="VANTA R1 — конфигуратор" decoding="async" loading="lazy" src="https://res.cloudinary.com/dg9shucn/image/upload/f_auto,q_auto:good,c_limit,w_1400/v1789100635/vanta-r1-hq-side.jpg"/>
        <div class="config-preview-glow" aria-hidden="true"></div>
        <div class="config-preview-id"><small>YOUR R1</small><strong id="configProfileLabel">ROAD</strong><span id="configModuleCount">2 МОДУЛЯ</span></div>
      </div>
      <div class="config-summary" aria-live="polite">
        <div class="config-summary-top"><span><small>CONFIG</small><strong id="configCode">R1-ROAD-02</strong></span><span class="config-price"><small>CONCEPT PRICE</small><strong id="configPrice">€36 000</strong></span></div>
        <div class="config-stats">
          <span><small>МОЩНОСТЬ</small><b id="cfgPower">210 кВт</b></span>
          <span><small>МОМЕНТ</small><b id="cfgTorque">390 Н·м</b></span>
          <span><small>МАССА</small><b id="cfgMass">189 кг</b></span>
          <span><small>ЗАПАС</small><b id="cfgRange">320 км</b></span>
          <span><small>10→80%</small><b id="cfgCharge">15 мин</b></span>
        </div>
      </div>
    </div>

    <div class="config-panel reveal">
      <section class="config-step">
        <div class="config-step-head"><b>01</b><div><strong>ХАРАКТЕР</strong><small>RIDE PROFILE</small></div></div>
        <div class="config-presets" aria-label="Профиль R1">
          <button class="active" data-preset="road" aria-pressed="true"><span>ДОРОГА</span><small>ROAD</small><i>баланс</i></button>
          <button data-preset="attack" aria-pressed="false"><span>ТРЕК</span><small>ATTACK</small><i>максимум</i></button>
          <button data-preset="range" aria-pressed="false"><span>ЭКО</span><small>RANGE</small><i>дальность</i></button>
        </div>
      </section>

      <section class="config-step">
        <div class="config-step-head"><b>02</b><div><strong>МОДУЛИ</strong><small>OPTION MODULES</small></div></div>
        <div class="config-modules">
          <button class="config-module" data-module="performance" aria-pressed="false"><span class="config-module-copy"><strong>PERFORMANCE PACK</strong><small>Повышенная отдача силовой установки.</small></span><span class="config-effect">+15 кВт · +20 Н·м</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="aero" aria-pressed="false"><span class="config-module-copy"><strong>ACTIVE AERO</strong><small>Активная аэродинамика для скоростного режима.</small></span><span class="config-effect">+2 кг · −4 км</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="carbon" aria-pressed="false"><span class="config-module-copy"><strong>CARBON STRUCTURE</strong><small>Расширенный пакет кованого карбона.</small></span><span class="config-effect">−8 кг</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="range" aria-pressed="false"><span class="config-module-copy"><strong>RANGE SYSTEM</strong><small>Увеличенный энергетический пакет.</small></span><span class="config-effect">+45 км · +7 кг</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="fast" aria-pressed="true"><span class="config-module-copy"><strong>FAST CHARGE 800V</strong><small>Максимальный профиль быстрой зарядки.</small></span><span class="config-effect">18 → 15 мин</span><i>УСТАНОВЛЕНО</i></button>
          <button class="config-module" data-module="telemetry" aria-pressed="true"><span class="config-module-copy"><strong>RIDER TELEMETRY</strong><small>Расширенные данные поездки и состояния систем.</small></span><span class="config-effect">DATA+</span><i>УСТАНОВЛЕНО</i></button>
        </div>
      </section>

      <section class="config-step">
        <div class="config-step-head"><b>03</b><div><strong>СВЕТОВАЯ ПОДПИСЬ</strong><small>LIGHT SIGNATURE</small></div></div>
        <div class="config-finishes" aria-label="Световая подпись конфигуратора">
          <button class="active" data-config-tone="red" aria-pressed="true"><i></i><span>SIGNAL RED</span></button>
          <button data-config-tone="green" aria-pressed="false"><i></i><span>VOLT GREEN</span></button>
          <button data-config-tone="stealth" aria-pressed="false"><i></i><span>STEALTH</span></button>
        </div>
      </section>

      <div class="config-actions">
        <button class="config-save" id="configSave" type="button"><span>СОХРАНИТЬ CONFIG</span><i>+</i></button>
        <button class="config-activate" id="configActivate" type="button"><span>ПЕРЕЙТИ К АКТИВАЦИИ</span><i>→</i></button>
      </div>
      <p class="config-note">Демонстрационный конфигуратор: стоимость и параметры используются для product-concept VANTA R1 и не являются коммерческим предложением.</p>
    </div>
  </div>
</section>
'''

if 'id="configurator"' not in index:
    marker='<section class="activate chapter" id="activate">'
    if marker not in index:
        raise SystemExit('activation marker not found')
    index=index.replace(marker,SECTION+'\n'+marker,1)

index=index.replace('<a href="#system">Система</a>','<a href="#system">Система</a><a href="#configurator">Конфигуратор</a>',1)
index=index.replace('<a href="#system">06 / Система</a><a href="#activate">07 / Активация</a>','<a href="#system">06 / Система</a><a href="#configurator">07 / Конфигуратор</a><a href="#activate">08 / Активация</a>',1)
index=index.replace('<div class="eyebrow">07 / ACTIVATION / DEMO</div>','<div class="eyebrow">08 / ACTIVATION / DEMO</div>',1)
if 'id="activationBuild"' not in index:
    index=index.replace('<div aria-label="Цветовой режим" class="swatches">','<div class="activation-build" id="activationBuild">YOUR R1 / ROAD / 2 MODULES</div>\n<div aria-label="Цветовой режим" class="swatches">',1)
index=re.sub(r'v4\.css\?v=\d+', 'v4.css?v=19', index)
index=re.sub(r'v4\.js\?v=\d+', 'v4.js?v=11', index)

CSS='''

/* VANTA R1 — Configurator + Tech Sheet Visual Reinforcement 2026-09 */
.tech-sheet-v2{position:relative;isolation:isolate;background:radial-gradient(circle at 8% 0%,rgba(255,46,27,.085),transparent 28%),linear-gradient(180deg,#0a0b0a,#070807)!important}
.tech-sheet-v2:before{content:"";position:absolute;z-index:-1;inset:0;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.014) 1px,transparent 1px);background-size:38px 38px;mask-image:linear-gradient(180deg,#000 0%,transparent 72%)}
.tech-sheet-titleblock small{color:#a4aaa4!important}.tech-sheet-titleblock h2{position:relative;padding-bottom:5px}.tech-sheet-titleblock h2:after{content:"";display:block;width:74px;height:2px;margin-top:15px;background:var(--accent);box-shadow:0 0 18px rgba(255,46,27,.22)}
.tech-grid-v2 .tech-group{position:relative;overflow:hidden;box-shadow:inset 0 1px 0 rgba(255,255,255,.018)}
.tech-group-head{position:relative;background:linear-gradient(135deg,rgba(255,46,27,.045),transparent 62%)!important}.tech-group-head b{font-size:17px!important;text-shadow:0 0 18px rgba(255,46,27,.16)}
.tech-value strong{color:#fafaf6!important;text-shadow:0 0 26px rgba(255,255,255,.035)}.tech-value em{color:#b4bab4!important}.tech-label{color:#f0f0eb!important}.tech-grid-v2 .tech-metric p{color:#868c86!important}
.tech-meaning{position:relative;overflow:hidden;background:linear-gradient(90deg,rgba(255,46,27,.045),rgba(255,255,255,.008) 38%,transparent)!important}.tech-meaning:before{content:"";position:absolute;inset:0 auto 0 0;width:2px;background:var(--accent);opacity:.7}.tech-meaning>div small{color:#ff6255!important}

.configurator{padding:110px var(--pad);background:#060706;position:relative;overflow:clip}
.configurator:before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 22% 34%,rgba(255,46,27,.055),transparent 29%),linear-gradient(180deg,transparent 0 70%,rgba(255,255,255,.012));opacity:.9}
.config-head,.config-layout{position:relative;z-index:1}.config-head{display:grid;grid-template-columns:1.2fr .72fr;gap:54px;align-items:end;margin-bottom:44px}.config-head h2{font-size:clamp(52px,5.5vw,92px);margin-top:22px}.config-head p{margin:0;max-width:470px;font-size:14px}
.config-layout{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(390px,.95fr);gap:30px;align-items:start}.config-preview{position:sticky;top:calc(var(--header) + 18px)}
.config-preview-media{--config-accent:#ff3728;position:relative;overflow:hidden;border:1px solid #2b2e2b;background:#060706;aspect-ratio:1.22}.config-preview-media img{width:100%;height:100%;object-fit:cover;filter:brightness(.78) saturate(.9);transition:filter .5s ease,transform .7s var(--motion-ease);transform:scale(1.015)}.config-preview-media:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 52%,rgba(3,3,3,.76)),radial-gradient(circle at 62% 54%,color-mix(in srgb,var(--config-accent) 15%,transparent),transparent 42%);pointer-events:none;transition:.45s ease}.config-preview-media[data-tone="green"]{--config-accent:#43df84}.config-preview-media[data-tone="stealth"]{--config-accent:#aeb3b0}.config-preview-media[data-tone="green"] img{filter:hue-rotate(104deg) saturate(.76) brightness(.8)}.config-preview-media[data-tone="stealth"] img{filter:grayscale(.9) brightness(.68) contrast(1.06)}.config-preview-glow{position:absolute;z-index:2;inset:auto 8% 0;height:38%;background:radial-gradient(ellipse at 50% 100%,color-mix(in srgb,var(--config-accent) 28%,transparent),transparent 68%);mix-blend-mode:screen;opacity:.54;transition:.4s}.config-preview-id{position:absolute;z-index:3;left:22px;right:22px;bottom:20px;display:grid;grid-template-columns:auto 1fr auto;align-items:end;gap:12px}.config-preview-id small,.config-preview-id span{font-size:8px;letter-spacing:.17em;color:#888e89}.config-preview-id strong{font-family:"Inter Tight","Inter",sans-serif;font-size:34px;letter-spacing:-.04em;font-weight:600;color:#fff}.config-preview-id span{text-align:right}
.config-summary{border:1px solid #2b2e2b;border-top:0;background:rgba(8,9,8,.92);backdrop-filter:blur(14px)}.config-summary-top{display:grid;grid-template-columns:1fr auto;gap:24px;padding:17px 20px;border-bottom:1px solid #292c2a}.config-summary-top span{display:grid;gap:5px}.config-summary-top small,.config-stats small{font-size:7px;letter-spacing:.16em;color:#777e79}.config-summary-top strong{font-size:13px;letter-spacing:.08em}.config-price{text-align:right}.config-price strong{font-family:"Inter Tight","Inter",sans-serif;font-size:25px!important;letter-spacing:-.035em!important;color:#fff}.config-stats{display:grid;grid-template-columns:repeat(5,1fr)}.config-stats span{min-width:0;padding:15px 12px;border-right:1px solid #272a28;display:grid;gap:6px}.config-stats span:last-child{border-right:0}.config-stats b{font-size:12px;font-weight:600;white-space:nowrap}
.config-panel{border:1px solid #2d302e;background:linear-gradient(180deg,#0a0b0a,#070807)}.config-step+.config-step{border-top:1px solid #2b2e2b}.config-step-head{display:flex;align-items:center;gap:12px;padding:16px 18px;border-bottom:1px solid #252825;background:rgba(255,255,255,.008)}.config-step-head b{color:var(--accent);font-size:11px;letter-spacing:.1em}.config-step-head div{display:grid;gap:3px}.config-step-head strong{font-size:10px;letter-spacing:.12em}.config-step-head small{font-size:7px;letter-spacing:.17em;color:#737a74}
.config-presets{display:grid;grid-template-columns:repeat(3,1fr)}.config-presets button{position:relative;min-height:88px;padding:15px 10px;border:0;border-right:1px solid #272a28;background:transparent;color:#858b86;cursor:pointer;display:grid;align-content:center;justify-items:center;gap:5px}.config-presets button:last-child{border-right:0}.config-presets button:after{content:"";position:absolute;left:18%;right:18%;bottom:0;height:2px;background:var(--accent);transform:scaleX(0);transform-origin:center;transition:.25s}.config-presets button.active{color:#f5f5f1;background:linear-gradient(180deg,rgba(255,46,27,.045),transparent)}.config-presets button.active:after{transform:scaleX(1)}.config-presets span{font-size:11px;letter-spacing:.08em}.config-presets small{font-size:7px;letter-spacing:.16em;color:inherit}.config-presets i{font-style:normal;font-size:7px;color:#656b66}
.config-modules{display:grid}.config-module{display:grid;grid-template-columns:minmax(0,1fr) auto 86px;gap:14px;align-items:center;min-height:76px;padding:14px 16px;border:0;border-bottom:1px solid #242724;background:transparent;text-align:left;cursor:pointer;transition:background .25s,border-color .25s}.config-module:last-child{border-bottom:0}.config-module-copy{display:grid;gap:5px;min-width:0}.config-module-copy strong{font-size:10px;letter-spacing:.09em}.config-module-copy small{font-size:8px;line-height:1.4;color:#7c827d}.config-effect{font-size:8px;letter-spacing:.08em;color:#a2a8a3;white-space:nowrap}.config-module>i{font-style:normal;text-align:right;font-size:7px;letter-spacing:.12em;color:#6e746f}.config-module[aria-pressed="true"]{background:linear-gradient(90deg,rgba(255,46,27,.055),transparent 54%);box-shadow:inset 2px 0 0 var(--accent)}.config-module[aria-pressed="true"]>i{color:#ff6255}.config-module[aria-pressed="true"] .config-effect{color:#dddeda}
.config-finishes{display:grid;grid-template-columns:repeat(3,1fr)}.config-finishes button{min-height:58px;border:0;border-right:1px solid #272a28;background:transparent;color:#7e847f;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer}.config-finishes button:last-child{border-right:0}.config-finishes button i{width:12px;height:12px;border-radius:50%;background:#db2f22;box-shadow:0 0 0 1px rgba(255,255,255,.1)}.config-finishes button:nth-child(2) i{background:#37ca76}.config-finishes button:nth-child(3) i{background:#111;border:1px solid #4a4e4b}.config-finishes button span{font-size:8px;letter-spacing:.1em}.config-finishes button.active{color:#f4f4f0;background:rgba(255,255,255,.018)}
.config-actions{display:grid;grid-template-columns:1fr 1.15fr;border-top:1px solid #2b2e2b}.config-actions button{min-height:58px;padding:0 16px;border:0;background:transparent;color:#ddd;display:flex;align-items:center;justify-content:space-between;font-size:8px;letter-spacing:.12em;cursor:pointer}.config-save{border-right:1px solid #2b2e2b!important}.config-activate{background:var(--accent)!important;color:#fff!important}.config-actions button i{font-style:normal;font-size:15px}.config-note{margin:0;padding:13px 16px;border-top:1px solid #252825;font-size:8px;line-height:1.5;color:#666c67}.activation-build{margin-top:22px;font-size:8px;letter-spacing:.16em;color:#7e847f;text-transform:uppercase}
@media(hover:hover) and (pointer:fine){.config-presets button:hover,.config-finishes button:hover{background:rgba(255,255,255,.025);color:#fff}.config-module:hover{background:rgba(255,255,255,.018)}.config-preview-media:hover img{transform:scale(1.025)}}
@media(max-width:980px){.configurator{padding:74px var(--pad)}.config-head{grid-template-columns:1fr;gap:18px;margin-bottom:30px}.config-head h2{font-size:49px}.config-head p{max-width:38ch}.config-layout{grid-template-columns:1fr;gap:18px}.config-preview{position:static}.config-preview-media{margin:0 calc(-1*var(--pad));border-left:0;border-right:0;aspect-ratio:1.2}.config-summary{margin:0 calc(-1*var(--pad));border-left:0;border-right:0}.config-panel{margin-top:4px}.config-module{grid-template-columns:minmax(0,1fr) auto;gap:10px}.config-module>i{grid-column:2;grid-row:1/3}.config-effect{grid-column:1}.tech-sheet-v2 .tech-group{box-shadow:none!important}}
@media(max-width:520px){.configurator{padding-left:20px;padding-right:20px}.config-head h2{font-size:43px}.config-preview-id{left:16px;right:16px;bottom:14px}.config-preview-id strong{font-size:28px}.config-summary-top{padding:14px 16px}.config-stats{grid-template-columns:repeat(3,1fr)}.config-stats span{padding:12px 10px}.config-stats span:nth-child(3){border-right:0}.config-stats span:nth-child(n+4){border-top:1px solid #272a28}.config-stats span:nth-child(4){grid-column:1/2}.config-stats span:nth-child(5){grid-column:2/4;border-right:0}.config-presets button{min-height:80px}.config-module{min-height:82px;padding:13px}.config-module-copy small{font-size:7.5px}.config-effect{font-size:7.5px}.config-module>i{font-size:6.6px}.config-finishes button{min-height:54px;gap:6px}.config-finishes button span{font-size:7px}.config-actions{grid-template-columns:1fr}.config-save{border-right:0!important;border-bottom:1px solid #2b2e2b!important}.config-note{font-size:7.5px}}
@media(max-width:390px){.config-head h2{font-size:37px}.config-preview-media{aspect-ratio:1.05}.config-stats b{font-size:11px}.config-presets span{font-size:10px}.config-module-copy strong{font-size:9px}}
'''
if 'VANTA R1 — Configurator + Tech Sheet Visual Reinforcement 2026-09' not in css:
    css=css.rstrip()+CSS+'\n'

JS='''

/* VANTA R1 — Configurator 2026-09 */
(()=>{
  'use strict';
  const root=document.getElementById('configurator');
  if(!root)return;
  const base={power:210,torque:390,mass:189,range:320,charge:18,price:32900};
  const effects={
    performance:{power:15,torque:20,range:-18,price:3900},
    aero:{mass:2,range:-4,price:2600},
    carbon:{mass:-8,price:4800},
    range:{mass:7,range:45,price:4200},
    fast:{charge:-3,price:1900},
    telemetry:{price:1200}
  };
  const presets={
    road:{label:'ROAD',modules:['fast','telemetry'],tone:'red'},
    attack:{label:'ATTACK',modules:['performance','aero','carbon','telemetry'],tone:'red'},
    range:{label:'RANGE',modules:['range','fast','carbon','telemetry'],tone:'green'}
  };
  let state={preset:'road',modules:new Set(presets.road.modules),tone:'red'};
  const q=id=>document.getElementById(id);
  const profileLabel=q('configProfileLabel'),moduleCount=q('configModuleCount'),code=q('configCode'),price=q('configPrice');
  const stats={power:q('cfgPower'),torque:q('cfgTorque'),mass:q('cfgMass'),range:q('cfgRange'),charge:q('cfgCharge')};
  const preview=q('configPreview'),save=q('configSave'),activate=q('configActivate'),activationBuild=q('activationBuild');
  const presetButtons=[...root.querySelectorAll('[data-preset]')];
  const moduleButtons=[...root.querySelectorAll('[data-module]')];
  const toneButtons=[...root.querySelectorAll('[data-config-tone]')];
  const money=n=>new Intl.NumberFormat('ru-RU',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(n).replace(/\u00a0/g,' ');
  const sameSet=(a,b)=>a.size===b.length&&b.every(x=>a.has(x));
  const detectPreset=()=>Object.entries(presets).find(([,p])=>sameSet(state.modules,p.modules)&&state.tone===p.tone)?.[0]||'custom';
  const calculate=()=>{
    const out={...base};
    state.modules.forEach(key=>{const e=effects[key]||{};Object.keys(e).forEach(k=>out[k]=(out[k]||0)+e[k]);});
    return out;
  };
  const render=()=>{
    state.preset=detectPreset();
    const values=calculate();
    const profile=state.preset==='custom'?'CUSTOM':presets[state.preset].label;
    profileLabel.textContent=profile;
    const count=state.modules.size;
    moduleCount.textContent=`${count} ${count===1?'МОДУЛЬ':count<5?'МОДУЛЯ':'МОДУЛЕЙ'}`;
    code.textContent=`R1-${profile}-${String(count).padStart(2,'0')}`;
    price.textContent=money(values.price);
    stats.power.textContent=`${values.power} кВт`;
    stats.torque.textContent=`${values.torque} Н·м`;
    stats.mass.textContent=`${values.mass} кг`;
    stats.range.textContent=`${values.range} км`;
    stats.charge.textContent=`${values.charge} мин`;
    preview.dataset.tone=state.tone;
    presetButtons.forEach(btn=>{const on=btn.dataset.preset===state.preset;btn.classList.toggle('active',on);btn.setAttribute('aria-pressed',String(on));});
    moduleButtons.forEach(btn=>{const on=state.modules.has(btn.dataset.module);btn.setAttribute('aria-pressed',String(on));const status=btn.querySelector(':scope > i');if(status)status.textContent=on?'УСТАНОВЛЕНО':'ДОБАВИТЬ';});
    toneButtons.forEach(btn=>{const on=btn.dataset.configTone===state.tone;btn.classList.toggle('active',on);btn.setAttribute('aria-pressed',String(on));});
    if(activationBuild)activationBuild.textContent=`YOUR R1 / ${profile} / ${count} MODULES`;
  };
  const usePreset=key=>{const p=presets[key];if(!p)return;state={preset:key,modules:new Set(p.modules),tone:p.tone};render();};
  presetButtons.forEach(btn=>btn.addEventListener('click',()=>usePreset(btn.dataset.preset)));
  moduleButtons.forEach(btn=>btn.addEventListener('click',()=>{const key=btn.dataset.module;if(state.modules.has(key))state.modules.delete(key);else state.modules.add(key);render();}));
  toneButtons.forEach(btn=>btn.addEventListener('click',()=>{state.tone=btn.dataset.configTone;render();}));
  save?.addEventListener('click',()=>{
    try{localStorage.setItem('vanta-r1-config',JSON.stringify({modules:[...state.modules],tone:state.tone}));}catch{}
    const span=save.querySelector('span');if(span){const original='СОХРАНИТЬ CONFIG';span.textContent='CONFIG СОХРАНЁН';setTimeout(()=>span.textContent=original,1400);}
  });
  activate?.addEventListener('click',()=>{
    const swatch=document.querySelector(`.sw[data-color="${state.tone}"]`);swatch?.click();
    document.getElementById('activate')?.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
  });
  try{
    const saved=JSON.parse(localStorage.getItem('vanta-r1-config')||'null');
    if(saved&&Array.isArray(saved.modules)){state.modules=new Set(saved.modules.filter(k=>effects[k]));state.tone=['red','green','stealth'].includes(saved.tone)?saved.tone:'red';}
  }catch{}
  render();
})();
'''
if 'VANTA R1 — Configurator 2026-09' not in js:
    js=js.rstrip()+JS+'\n'

# Basic validation before writing.
ids=re.findall(r'id="([^"]+)"',index)
dupes=sorted({x for x in ids if ids.count(x)>1})
if dupes:
    raise SystemExit(f'duplicate ids: {dupes}')
if index.count('id="configurator"')!=1:
    raise SystemExit('configurator insertion failed')
if css.count('{')!=css.count('}'):
    raise SystemExit('css brace mismatch')
if js.count('VANTA R1 — Configurator 2026-09')!=1:
    raise SystemExit('js marker mismatch')

index_path.write_text(index,encoding='utf-8')
css_path.write_text(css,encoding='utf-8')
js_path.write_text(js,encoding='utf-8')
