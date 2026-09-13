from pathlib import Path
import re

index_path=Path('index.html')
css_path=Path('v4.css')
index=index_path.read_text()
css=css_path.read_text()

new_dialog='''<dialog aria-labelledby="techTitle" class="tech-sheet" id="techSheet">
<div class="tech-sheet-panel tech-sheet-v2">
<div class="tech-sheet-head">
  <div class="tech-sheet-titleblock">
    <small>R1 / TECH SHEET / ENGINEERING DATA</small>
    <h2 id="techTitle">ТЕХПАСПОРТ R1</h2>
    <p>Ключевые целевые параметры концепта — что означает каждая цифра и на что она влияет.</p>
  </div>
  <button aria-label="Закрыть технические характеристики" id="techClose" type="button">×</button>
</div>
<div class="tech-grid tech-grid-v2">
  <section class="tech-group" aria-label="Привод">
    <header class="tech-group-head"><b>01</b><div><h3>ПРИВОД</h3><small>DRIVE SYSTEM</small></div></header>
    <div class="tech-metric"><div class="tech-value"><strong>210</strong><em>кВт</em></div><span class="tech-label">Пиковая мощность</span><p>Максимальная целевая отдача электрического привода.</p></div>
    <div class="tech-metric"><div class="tech-value"><strong>390</strong><em>Н·м</em></div><span class="tech-label">Крутящий момент</span><p>Тяга доступна практически сразу после открытия газа.</p></div>
  </section>
  <section class="tech-group" aria-label="Энергосистема">
    <header class="tech-group-head"><b>02</b><div><h3>ЭНЕРГОСИСТЕМА</h3><small>ENERGY SYSTEM</small></div></header>
    <div class="tech-metric"><div class="tech-value"><strong>800</strong><em>V</em></div><span class="tech-label">Высоковольтная архитектура</span><p>Основа для высокой мощности и эффективной быстрой зарядки.</p></div>
    <div class="tech-metric"><div class="tech-value"><strong>18</strong><em>мин</em></div><span class="tech-label">Зарядка 10→80%</span><p>Целевое время на совместимой станции быстрой зарядки.</p></div>
  </section>
  <section class="tech-group" aria-label="Параметры мотоцикла">
    <header class="tech-group-head"><b>03</b><div><h3>ПАРАМЕТРЫ</h3><small>VEHICLE TARGETS</small></div></header>
    <div class="tech-metric"><div class="tech-value"><strong>189</strong><em>кг</em></div><span class="tech-label">Целевая масса</span><p>Расчётная масса R1 в концептуальной инженерной конфигурации.</p></div>
    <div class="tech-metric"><div class="tech-value"><strong>320</strong><em>км</em></div><span class="tech-label">Запас хода</span><p>Расчётный целевой диапазон движения на одном заряде.</p></div>
  </section>
</div>
<div class="tech-meaning">
  <div><small>КАК ЧИТАТЬ ЭТИ ДАННЫЕ</small><strong>Цифры описывают характер R1.</strong></div>
  <p><b>210 кВт + 390 Н·м</b> отвечают за ускорение и тягу. <b>800 V + 18 мин</b> — за энергетическую архитектуру и скорость зарядки. <b>189 кг + 320 км</b> показывают баланс массы и практического запаса хода.</p>
  <span>Все значения — целевые параметры демонстрационного concept-проекта, а не сертифицированные характеристики серийной модели.</span>
</div>
</div>
</dialog>'''

index_new,count=re.subn(r'<dialog aria-labelledby="techTitle" class="tech-sheet" id="techSheet">.*?</dialog>',new_dialog,index,flags=re.S)
if count!=1:
    raise SystemExit(f'tech dialog replacements: {count}')
index_new=index_new.replace('v4.css?v=16','v4.css?v=17')
if index_new==index:
    raise SystemExit('index unchanged')

css_append=r'''

/* VANTA R1 — Tech Sheet V2: Russian-first engineering explainer 2026-09 */
.tech-sheet-v2{
  width:min(980px,calc(100vw - 34px))!important;
  max-height:min(90svh,920px)!important;
  overflow:auto!important;
  padding:30px!important;
  border:1px solid #393c39!important;
  background:
    radial-gradient(circle at 8% 0%,rgba(255,46,27,.055),transparent 28%),
    linear-gradient(180deg,#0a0b0a 0%,#070807 100%)!important;
  box-shadow:0 32px 90px rgba(0,0,0,.62),inset 0 1px 0 rgba(255,255,255,.025)!important;
}
.tech-sheet-v2 .tech-sheet-head{
  display:flex!important;
  align-items:flex-start!important;
  justify-content:space-between!important;
  gap:28px!important;
  padding:0 0 26px!important;
  margin:0 0 16px!important;
  border-bottom:1px solid #303330!important;
}
.tech-sheet-titleblock{max-width:700px}
.tech-sheet-titleblock>small{
  display:block;
  margin-bottom:12px;
  color:#8d938e;
  font-size:9px;
  letter-spacing:.19em;
}
.tech-sheet-titleblock h2{
  margin:0!important;
  font-size:clamp(42px,6vw,76px)!important;
  line-height:.88!important;
  letter-spacing:-.055em!important;
  color:#f4f5f1!important;
}
.tech-sheet-titleblock>p{
  max-width:620px;
  margin:16px 0 0!important;
  color:#a7aaa6!important;
  font-size:13px!important;
  line-height:1.5!important;
}
.tech-grid-v2{
  display:grid!important;
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:10px!important;
  border:0!important;
  margin-top:0!important;
}
.tech-grid-v2 .tech-group{
  display:grid!important;
  grid-template-rows:auto 1fr 1fr!important;
  min-width:0!important;
  border:1px solid #2d302e!important;
  background:linear-gradient(180deg,rgba(255,255,255,.016),rgba(255,255,255,.003))!important;
  overflow:hidden!important;
  position:relative!important;
}
.tech-grid-v2 .tech-group:before{
  content:"";
  position:absolute;
  inset:0 auto auto 0;
  width:48px;
  height:2px;
  background:var(--accent);
  opacity:.85;
}
.tech-group-head{
  display:flex!important;
  align-items:center!important;
  gap:13px!important;
  min-height:76px!important;
  padding:18px 18px 16px!important;
  border-bottom:1px solid #292c2a!important;
  background:rgba(255,255,255,.009)!important;
}
.tech-group-head>b{
  color:var(--accent)!important;
  font-size:11px!important;
  font-weight:700!important;
  letter-spacing:.14em!important;
}
.tech-group-head h3{
  margin:0!important;
  color:#e9ebe7!important;
  font-size:13px!important;
  line-height:1.05!important;
  letter-spacing:.055em!important;
}
.tech-group-head small{
  display:block!important;
  margin-top:5px!important;
  color:#747a75!important;
  font-size:7.5px!important;
  letter-spacing:.17em!important;
}
.tech-grid-v2 .tech-metric{
  display:flex!important;
  flex-direction:column!important;
  justify-content:center!important;
  min-width:0!important;
  min-height:176px!important;
  padding:19px 18px 18px!important;
  border:0!important;
  border-bottom:1px solid #292c2a!important;
  background:transparent!important;
  text-align:left!important;
}
.tech-grid-v2 .tech-metric:last-child{border-bottom:0!important}
.tech-value{
  display:flex!important;
  align-items:baseline!important;
  gap:8px!important;
  margin-bottom:9px!important;
  white-space:nowrap!important;
}
.tech-value strong{
  margin:0!important;
  color:#f7f8f4!important;
  font-size:clamp(46px,5vw,66px)!important;
  font-weight:500!important;
  line-height:.82!important;
  letter-spacing:-.065em!important;
  font-variant-numeric:tabular-nums!important;
}
.tech-value em{
  color:#b8bcb8!important;
  font-style:normal!important;
  font-size:11px!important;
  font-weight:600!important;
  letter-spacing:.08em!important;
}
.tech-label{
  display:block!important;
  margin:0 0 7px!important;
  color:#d9dcd8!important;
  font-size:10px!important;
  font-weight:600!important;
  line-height:1.25!important;
  letter-spacing:.045em!important;
  text-transform:uppercase!important;
}
.tech-grid-v2 .tech-metric p{
  margin:0!important;
  color:#818682!important;
  font-size:9.5px!important;
  line-height:1.48!important;
}
.tech-meaning{
  display:grid!important;
  grid-template-columns:.72fr 1.28fr!important;
  gap:12px 30px!important;
  margin-top:14px!important;
  padding:20px!important;
  border:1px solid #303330!important;
  background:linear-gradient(90deg,rgba(255,46,27,.035),rgba(255,255,255,.008) 42%,transparent)!important;
}
.tech-meaning>div small{
  display:block!important;
  color:var(--accent)!important;
  font-size:8px!important;
  letter-spacing:.18em!important;
}
.tech-meaning>div strong{
  display:block!important;
  margin-top:8px!important;
  color:#eceeeb!important;
  font-size:15px!important;
  line-height:1.25!important;
}
.tech-meaning>p{
  margin:0!important;
  color:#aaaeaa!important;
  font-size:10.5px!important;
  line-height:1.58!important;
}
.tech-meaning>p b{color:#e7e9e6!important;font-weight:600!important}
.tech-meaning>span{
  grid-column:1/-1!important;
  padding-top:13px!important;
  border-top:1px solid #292c2a!important;
  color:#696e6a!important;
  font-size:8.5px!important;
  line-height:1.5!important;
}
@media(max-width:720px){
  .tech-sheet-v2{
    width:calc(100vw - 20px)!important;
    max-height:92svh!important;
    padding:20px!important;
  }
  .tech-sheet-v2 .tech-sheet-head{gap:14px!important;padding-bottom:20px!important}
  .tech-sheet-titleblock h2{font-size:clamp(35px,10.7vw,48px)!important;letter-spacing:-.05em!important}
  .tech-sheet-titleblock>p{font-size:11px!important;max-width:30ch!important}
  .tech-grid-v2{grid-template-columns:1fr!important;gap:9px!important}
  .tech-grid-v2 .tech-group{
    grid-template-columns:minmax(105px,.58fr) 1fr 1fr!important;
    grid-template-rows:auto!important;
  }
  .tech-group-head{
    min-height:150px!important;
    padding:15px 13px!important;
    border-bottom:0!important;
    border-right:1px solid #292c2a!important;
    align-items:flex-start!important;
    flex-direction:column!important;
    justify-content:center!important;
    gap:7px!important;
  }
  .tech-group-head h3{font-size:10px!important;word-break:normal!important}
  .tech-group-head small{font-size:6.5px!important;line-height:1.3!important}
  .tech-grid-v2 .tech-metric{
    min-height:150px!important;
    padding:15px 13px!important;
    border-bottom:0!important;
    border-right:1px solid #292c2a!important;
  }
  .tech-grid-v2 .tech-metric:last-child{border-right:0!important}
  .tech-value{gap:5px!important;margin-bottom:8px!important}
  .tech-value strong{font-size:clamp(36px,10.5vw,48px)!important}
  .tech-value em{font-size:8px!important}
  .tech-label{font-size:8px!important;line-height:1.25!important;margin-bottom:6px!important}
  .tech-grid-v2 .tech-metric p{font-size:7.8px!important;line-height:1.42!important}
  .tech-meaning{grid-template-columns:1fr!important;gap:10px!important;padding:16px!important}
  .tech-meaning>p{font-size:9px!important}
  .tech-meaning>span{grid-column:1!important;font-size:7.7px!important}
}
@media(max-width:390px){
  .tech-sheet-v2{padding:16px!important}
  .tech-grid-v2 .tech-group{grid-template-columns:94px 1fr 1fr!important}
  .tech-group-head,.tech-grid-v2 .tech-metric{min-height:144px!important;padding:13px 10px!important}
  .tech-value strong{font-size:36px!important}
  .tech-label{font-size:7.4px!important}
  .tech-grid-v2 .tech-metric p{font-size:7.3px!important}
}
'''

if 'Tech Sheet V2: Russian-first engineering explainer' not in css:
    css_new=css.rstrip()+css_append+'\n'
else:
    raise SystemExit('techsheet v2 css already exists')

index_path.write_text(index_new)
css_path.write_text(css_new)
print('patched index.html and v4.css')
