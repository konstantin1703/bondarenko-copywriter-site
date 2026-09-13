from pathlib import Path
import re

repo=Path('.')
html_p=repo/'index.html'
css_p=repo/'v4.css'
js_p=repo/'v4.js'
html=html_p.read_text(encoding='utf-8')
css=css_p.read_text(encoding='utf-8')
js=js_p.read_text(encoding='utf-8')

# --- HTML: replace configurator and insert request flow before activation ---
start=html.index('<section class="configurator chapter" id="configurator">')
act=html.index('<section class="activate chapter" id="activate">', start)
config_request=r'''<section class="configurator chapter" id="configurator">
  <div class="config-head reveal">
    <div>
      <div class="eyebrow">07 / R1 CONFIGURATOR / YOUR R1</div>
      <h2>Собери свой<br/><em>характер R1.</em></h2>
    </div>
    <p>Выбери характер, установи нужные модули и сразу увидишь честный инженерный баланс: мощность, момент, масса, запас хода, зарядка и стоимость меняются вместе с конфигурацией.</p>
  </div>
  <div class="config-layout">
    <div class="config-preview reveal">
      <div class="config-preview-media" data-tone="red" id="configPreview">
        <img alt="VANTA R1 — конфигуратор" decoding="async" loading="lazy" src="https://res.cloudinary.com/dg9shucn/image/upload/f_auto,q_auto:good,c_limit,w_1400/v1789100635/vanta-r1-hq-side.jpg"/>
        <div class="config-preview-glow" aria-hidden="true"></div>
        <div class="config-preview-id"><small>YOUR R1</small><strong id="configProfileLabel">ROAD</strong><span id="configModuleCount">2 МОДУЛЯ</span></div>
      </div>
      <div class="config-summary" aria-live="polite">
        <div class="config-summary-top"><span><small>CONFIGURATION</small><strong id="configCode">R1-ROAD-02</strong></span><span class="config-price"><small>CONCEPT PRICE</small><strong id="configPrice">€36 000</strong></span></div>
        <div class="config-stats">
          <span><small>МОЩНОСТЬ</small><b id="cfgPower">210 кВт</b><em id="cfgPowerDelta">BASE</em></span>
          <span><small>МОМЕНТ</small><b id="cfgTorque">390 Н·м</b><em id="cfgTorqueDelta">BASE</em></span>
          <span><small>МАССА</small><b id="cfgMass">189 кг</b><em id="cfgMassDelta">BASE</em></span>
          <span><small>ЗАПАС</small><b id="cfgRange">320 км</b><em id="cfgRangeDelta">BASE</em></span>
          <span><small>10→80%</small><b id="cfgCharge">15 мин</b><em id="cfgChargeDelta">−3 мин</em></span>
        </div>
        <div class="config-balance"><span>BASELINE</span><b>210 кВт / 390 Н·м / 189 кг / 320 км / 18 мин</b></div>
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
        <div class="config-step-head"><b>02</b><div><strong>МОДУЛИ</strong><small>ENGINEERING OPTIONS</small></div></div>
        <div class="config-modules">
          <button class="config-module" data-module="performance" aria-pressed="false"><span class="config-module-copy"><strong>PERFORMANCE PACK</strong><small>Усиленная силовая электроника и охлаждение.</small></span><span class="config-effect">+18 кВт · +30 Н·м · +3 кг · −16 км</span><span class="config-module-price">+€3 900</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="aero" aria-pressed="false"><span class="config-module-copy"><strong>ACTIVE AERO</strong><small>Активная аэродинамика: стабильность и низкое сопротивление.</small></span><span class="config-effect">+2 кг · +6 км</span><span class="config-module-price">+€2 600</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="carbon" aria-pressed="false"><span class="config-module-copy"><strong>CARBON STRUCTURE</strong><small>Расширенный пакет кованого карбона и облегчённых узлов.</small></span><span class="config-effect">−9 кг</span><span class="config-module-price">+€4 800</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="range" aria-pressed="false"><span class="config-module-copy"><strong>RANGE SYSTEM</strong><small>Увеличенный энергетический пакет для дальних маршрутов.</small></span><span class="config-effect">+52 км · +12 кг · +2 мин</span><span class="config-module-price">+€4 200</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="fast" aria-pressed="true"><span class="config-module-copy"><strong>FAST CHARGE 800V</strong><small>Расширенный профиль термоконтроля и быстрой зарядки.</small></span><span class="config-effect">18 → 14 мин</span><span class="config-module-price">+€1 900</span><i>УСТАНОВЛЕНО</i></button>
          <button class="config-module" data-module="telemetry" aria-pressed="true"><span class="config-module-copy"><strong>RIDER TELEMETRY</strong><small>Расширенные данные поездки, состояния систем и экспорт сессии.</small></span><span class="config-effect">DATA+</span><span class="config-module-price">+€1 200</span><i>УСТАНОВЛЕНО</i></button>
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
        <button class="config-request" id="configRequest" type="button"><span>ПЕРЕЙТИ К ЗАЯВКЕ</span><i>→</i></button>
      </div>
      <p class="config-note">Демонстрационный конфигуратор: стоимость и параметры относятся к fictional product-concept VANTA R1 и не являются коммерческим предложением.</p>
    </div>
  </div>
</section>

<section class="request chapter" id="request">
  <div class="request-head reveal">
    <div>
      <div class="eyebrow">08 / REQUEST / APPLICATION</div>
      <h2>Зафиксируй<br/><em>свой R1.</em></h2>
    </div>
    <p>Финальный демонстрационный шаг: контактные данные, страна и адрес. Ничего не отправляется — форма существует только внутри portfolio-сценария.</p>
  </div>

  <div class="request-layout">
    <form class="request-form reveal" id="requestForm" novalidate>
      <div class="request-progress" aria-label="Этапы заявки">
        <button class="active" type="button" data-request-nav="1" aria-current="step"><b>01</b><span>КОНТАКТЫ<small>IDENTITY</small></span></button>
        <button type="button" data-request-nav="2"><b>02</b><span>ДОСТАВКА<small>DELIVERY</small></span></button>
        <button type="button" data-request-nav="3"><b>03</b><span>ПРОВЕРКА<small>CONFIRM</small></span></button>
      </div>

      <section class="request-step active" data-request-step="1">
        <div class="request-step-title"><b>01</b><div><strong>КОНТАКТНЫЕ ДАННЫЕ</strong><small>Кому принадлежит конфигурация</small></div></div>
        <div class="request-fields two-col">
          <label class="request-field"><span>ИМЯ</span><input id="reqFirst" name="firstName" autocomplete="given-name" required placeholder="Иван"/></label>
          <label class="request-field"><span>ФАМИЛИЯ</span><input id="reqLast" name="lastName" autocomplete="family-name" required placeholder="Иванов"/></label>
          <label class="request-field full"><span>EMAIL</span><input id="reqEmail" name="email" autocomplete="email" inputmode="email" type="email" required placeholder="name@example.com"/></label>
          <div class="request-field full"><span>ТЕЛЕФОН</span><div class="phone-combo"><button class="phone-prefix" id="phoneRegionButton" type="button" aria-haspopup="dialog"><span id="phoneFlag">🌐</span><b id="phoneDial">КОД</b><i>⌄</i></button><input id="reqPhone" name="phone" autocomplete="tel-national" inputmode="tel" required placeholder="Номер телефона"/></div><small class="field-hint" id="phoneHint">Выбери регион номера — например 🇷🇺 Россия +7.</small></div>
        </div>
        <div class="request-controls"><span></span><button class="request-next" type="button" data-request-next="2">ПРОДОЛЖИТЬ <i>→</i></button></div>
      </section>

      <section class="request-step" data-request-step="2" hidden>
        <div class="request-step-title"><b>02</b><div><strong>АДРЕС</strong><small>Демонстрационные данные доставки</small></div></div>
        <div class="request-fields two-col">
          <div class="request-field full"><span>СТРАНА</span><button class="country-button" id="countryButton" type="button" aria-haspopup="dialog"><span id="countryFlag">🌐</span><b id="countryName">ВЫБЕРИ СТРАНУ</b><i>⌄</i></button><small class="field-error" id="countryError"></small></div>
          <label class="request-field"><span>РЕГИОН / ОБЛАСТЬ / ШТАТ</span><input id="reqRegion" name="region" autocomplete="address-level1" placeholder="Регион"/></label>
          <label class="request-field"><span>ГОРОД</span><input id="reqCity" name="city" autocomplete="address-level2" required placeholder="Город"/></label>
          <label class="request-field"><span>ИНДЕКС</span><input id="reqPostal" name="postal" autocomplete="postal-code" required placeholder="000000"/></label>
          <label class="request-field full"><span>АДРЕС</span><input id="reqAddress" name="address" autocomplete="street-address" required placeholder="Улица, дом"/></label>
          <label class="request-field full"><span>ДОПОЛНИТЕЛЬНО</span><input id="reqAddress2" name="address2" autocomplete="address-line2" placeholder="Квартира / офис / комментарий"/></label>
        </div>
        <div class="request-controls"><button class="request-back" type="button" data-request-back="1">← НАЗАД</button><button class="request-next" type="button" data-request-next="3">ПРОВЕРИТЬ <i>→</i></button></div>
      </section>

      <section class="request-step" data-request-step="3" hidden>
        <div class="request-step-title"><b>03</b><div><strong>ПРОВЕРКА ЗАЯВКИ</strong><small>Ничего не отправится в сеть</small></div></div>
        <div class="request-review">
          <article><small>КОНТАКТ</small><strong id="reviewName">—</strong><span id="reviewContact">—</span></article>
          <article><small>ДОСТАВКА</small><strong id="reviewCountry">—</strong><span id="reviewAddress">—</span></article>
          <article class="request-review-config"><small>КОНФИГУРАЦИЯ</small><strong id="reviewConfig">R1-ROAD-02</strong><span id="reviewModules">—</span></article>
        </div>
        <div class="request-privacy"><i></i><p><b>DEMO ONLY.</b> Поля используются только для интерактивной презентации. Данные не сохраняются и не отправляются.</p></div>
        <div class="request-controls"><button class="request-back" type="button" data-request-back="2">← НАЗАД</button><button class="request-submit" type="submit">ПОДТВЕРДИТЬ ЗАЯВКУ <i>→</i></button></div>
      </section>

      <section class="request-complete" id="requestComplete" hidden>
        <div class="request-lock-mark"><i></i><span>R1 / REQUEST SYSTEM</span></div>
        <small>CONFIGURATION LOCKED</small>
        <h3>ЗАЯВКА<br/>СФОРМИРОВАНА.</h3>
        <p>Это демонстрационное подтверждение portfolio-сценария. Конфигурация зафиксирована локально только на экране — никакие персональные данные не передавались.</p>
        <div class="request-code"><span>REQUEST ID</span><b id="requestCode">VR1-0000</b></div>
        <button class="request-to-activation" id="requestToActivation" type="button"><span>АКТИВИРОВАТЬ СВОЙ R1</span><i>→</i></button>
      </section>
    </form>

    <aside class="request-summary reveal" aria-live="polite">
      <div class="request-bike" data-tone="red" id="requestBike"><img alt="VANTA R1 — выбранная конфигурация" loading="lazy" decoding="async" src="https://res.cloudinary.com/dg9shucn/image/upload/f_auto,q_auto:good,c_limit,w_900/v1789100635/vanta-r1-hq-side.jpg"/><div></div></div>
      <div class="request-summary-head"><span><small>YOUR R1</small><strong id="requestProfile">ROAD</strong></span><span><small>CONCEPT PRICE</small><strong id="requestPrice">€36 000</strong></span></div>
      <div class="request-summary-stats"><span><small>POWER</small><b id="requestPower">210 кВт</b></span><span><small>MASS</small><b id="requestMass">189 кг</b></span><span><small>RANGE</small><b id="requestRange">320 км</b></span></div>
      <div class="request-summary-modules"><small>УСТАНОВЛЕНО</small><div id="requestModules"></div></div>
      <div class="request-summary-code"><span>CONFIG</span><b id="requestConfigCode">R1-ROAD-02</b></div>
    </aside>
  </div>

  <dialog class="region-picker" id="regionPicker" aria-labelledby="regionPickerTitle">
    <div class="region-picker-panel">
      <header><div><small>REGION DATABASE</small><strong id="regionPickerTitle">ВЫБЕРИ СТРАНУ</strong></div><button id="regionPickerClose" type="button" aria-label="Закрыть выбор страны">×</button></header>
      <label class="region-search"><span>⌕</span><input id="regionSearch" type="search" autocomplete="off" placeholder="Поиск страны или кода +7"/></label>
      <div class="region-list" id="regionList" role="listbox"></div>
    </div>
  </dialog>
</section>

'''
html=html[:start]+config_request+html[act:]
html=html.replace('<div class="eyebrow">08 / ACTIVATION / DEMO</div>','<div class="eyebrow">09 / ACTIVATION / DEMO</div>')
html=html.replace('<a href="#configurator">07 / Конфигуратор</a><a href="#activate">08 / Активация</a>','<a href="#configurator">07 / Конфигуратор</a><a href="#request">08 / Заявка</a><a href="#activate">09 / Активация</a>')
html=html.replace('v4.css?v=19','v4.css?v=20').replace('v4.js?v=11','v4.js?v=12')

# --- CSS: replace current configurator/reinforcement tail with clean V2 + request system ---
marker='/* VANTA R1 — Configurator + Tech Sheet Visual Reinforcement 2026-09 */'
if marker not in css:
    raise SystemExit('CSS configurator marker not found')
css=css[:css.index(marker)]
css+=r'''/* VANTA R1 — Tech Sheet Reinforcement + Configurator V2 + Request Flow 2026-09 */
.tech-sheet-v2{position:relative;isolation:isolate;background:radial-gradient(circle at 8% 0%,rgba(255,46,27,.085),transparent 28%),linear-gradient(180deg,#0a0b0a,#070807)!important}
.tech-sheet-v2:before{content:"";position:absolute;z-index:-1;inset:0;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.014) 1px,transparent 1px);background-size:38px 38px;mask-image:linear-gradient(180deg,#000 0%,transparent 72%)}
.tech-sheet-titleblock small{color:#a4aaa4!important}.tech-sheet-titleblock h2{position:relative;padding-bottom:5px}.tech-sheet-titleblock h2:after{content:"";display:block;width:74px;height:2px;margin-top:15px;background:var(--accent);box-shadow:0 0 18px rgba(255,46,27,.22)}
.tech-grid-v2 .tech-group{position:relative;overflow:hidden;box-shadow:inset 0 1px 0 rgba(255,255,255,.018)}
.tech-group-head{position:relative;background:linear-gradient(135deg,rgba(255,46,27,.045),transparent 62%)!important}.tech-group-head b{font-size:17px!important;text-shadow:0 0 18px rgba(255,46,27,.16)}
.tech-value strong{color:#fafaf6!important;text-shadow:0 0 26px rgba(255,255,255,.035)}.tech-value em{color:#b4bab4!important}.tech-label{color:#f0f0eb!important}.tech-grid-v2 .tech-metric p{color:#868c86!important}
.tech-meaning{position:relative;overflow:hidden;background:linear-gradient(90deg,rgba(255,46,27,.045),rgba(255,255,255,.008) 38%,transparent)!important}.tech-meaning:before{content:"";position:absolute;inset:0 auto 0 0;width:2px;background:var(--accent);opacity:.7}.tech-meaning>div small{color:#ff6255!important}

/* Configurator V2 */
.configurator{padding:110px var(--pad);background:#060706;position:relative;overflow:clip}.configurator:before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 22% 34%,rgba(255,46,27,.06),transparent 29%),linear-gradient(180deg,transparent 0 70%,rgba(255,255,255,.012));opacity:.9}
.config-head,.config-layout{position:relative;z-index:1}.config-head{display:grid;grid-template-columns:1.2fr .72fr;gap:54px;align-items:end;margin-bottom:44px}.config-head h2{font-size:clamp(52px,5.5vw,92px);margin-top:22px}.config-head p{margin:0;max-width:500px;font-size:14px}
.config-layout{display:grid;grid-template-columns:minmax(0,1.04fr) minmax(410px,.96fr);gap:30px;align-items:start}.config-preview{position:sticky;top:calc(var(--header) + 18px)}
.config-preview-media{--config-accent:#ff3728;position:relative;overflow:hidden;border:1px solid #303330;background:#060706;aspect-ratio:1.22}.config-preview-media img{width:100%;height:100%;object-fit:cover;filter:brightness(.8) saturate(.92);transition:filter .5s ease,transform .7s var(--motion-ease);transform:scale(1.015)}.config-preview-media:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(3,3,3,.8)),radial-gradient(circle at 62% 54%,color-mix(in srgb,var(--config-accent) 16%,transparent),transparent 42%);pointer-events:none;transition:.45s ease}.config-preview-media[data-tone="green"]{--config-accent:#43df84}.config-preview-media[data-tone="stealth"]{--config-accent:#aeb3b0}.config-preview-media[data-tone="green"] img{filter:hue-rotate(104deg) saturate(.78) brightness(.82)}.config-preview-media[data-tone="stealth"] img{filter:grayscale(.9) brightness(.7) contrast(1.06)}.config-preview-glow{position:absolute;z-index:2;inset:auto 8% 0;height:38%;background:radial-gradient(ellipse at 50% 100%,color-mix(in srgb,var(--config-accent) 30%,transparent),transparent 68%);mix-blend-mode:screen;opacity:.55;transition:.4s}.config-preview-id{position:absolute;z-index:3;left:22px;right:22px;bottom:20px;display:grid;grid-template-columns:auto 1fr auto;align-items:end;gap:12px}.config-preview-id small,.config-preview-id span{font-size:8px;letter-spacing:.17em;color:#8c928d}.config-preview-id strong{font-family:"Inter Tight","Inter",sans-serif;font-size:34px;letter-spacing:-.04em;font-weight:600;color:#fff}.config-preview-id span{text-align:right}
.config-summary{border:1px solid #303330;border-top:0;background:rgba(8,9,8,.94);backdrop-filter:blur(14px)}.config-summary-top{display:grid;grid-template-columns:1fr auto;gap:24px;padding:17px 20px;border-bottom:1px solid #292c2a}.config-summary-top span{display:grid;gap:5px}.config-summary-top small,.config-stats small{font-size:7px;letter-spacing:.16em;color:#777e79}.config-summary-top strong{font-size:13px;letter-spacing:.08em}.config-price{text-align:right}.config-price strong{font-family:"Inter Tight","Inter",sans-serif;font-size:25px!important;letter-spacing:-.035em!important;color:#fff}.config-stats{display:grid;grid-template-columns:repeat(5,1fr)}.config-stats>span{min-width:0;padding:14px 11px;border-right:1px solid #272a28;display:grid;gap:5px}.config-stats>span:last-child{border-right:0}.config-stats b{font-size:12px;font-weight:600;white-space:nowrap}.config-stats em{font-style:normal;font-size:6.5px;letter-spacing:.08em;color:#707771}.config-stats em.is-positive{color:#71d89b}.config-stats em.is-negative{color:#ff756a}.config-balance{display:flex;justify-content:space-between;gap:16px;padding:10px 14px;border-top:1px solid #252825;color:#666d67}.config-balance span{font-size:6.5px;letter-spacing:.16em}.config-balance b{font-size:7px;letter-spacing:.05em;font-weight:500;text-align:right}
.config-panel{border:1px solid #303330;background:linear-gradient(180deg,#0a0b0a,#070807);box-shadow:0 24px 70px rgba(0,0,0,.18)}.config-step+.config-step{border-top:1px solid #2b2e2b}.config-step-head{display:flex;align-items:center;gap:12px;padding:16px 18px;border-bottom:1px solid #252825;background:rgba(255,255,255,.008)}.config-step-head b{color:var(--accent);font-size:11px;letter-spacing:.1em}.config-step-head div{display:grid;gap:3px}.config-step-head strong{font-size:10px;letter-spacing:.12em}.config-step-head small{font-size:7px;letter-spacing:.17em;color:#737a74}
.config-presets{display:grid;grid-template-columns:repeat(3,1fr)}.config-presets button{position:relative;min-height:88px;padding:15px 10px;border:0;border-right:1px solid #272a28;background:transparent;color:#858b86;cursor:pointer;display:grid;align-content:center;justify-items:center;gap:5px}.config-presets button:last-child{border-right:0}.config-presets button:after{content:"";position:absolute;left:22%;right:22%;bottom:0;height:2px;border-radius:2px;background:var(--accent);transform:scaleX(0);transform-origin:center;transition:.25s}.config-presets button.active{color:#f5f5f1;background:linear-gradient(180deg,rgba(255,46,27,.045),transparent)}.config-presets button.active:after{transform:scaleX(1)}.config-presets span{font-size:11px;letter-spacing:.08em}.config-presets small{font-size:7px;letter-spacing:.16em;color:inherit}.config-presets i{font-style:normal;font-size:7px;color:#656b66}
.config-modules{display:grid}.config-module{display:grid;grid-template-columns:minmax(0,1fr) auto auto 88px;gap:12px;align-items:center;min-height:82px;padding:14px 16px;border:0;border-bottom:1px solid #242724;background:transparent;text-align:left;cursor:pointer;transition:background .25s,border-color .25s}.config-module:last-child{border-bottom:0}.config-module-copy{display:grid;gap:5px;min-width:0}.config-module-copy strong{font-size:10px;letter-spacing:.09em}.config-module-copy small{font-size:8px;line-height:1.42;color:#7c827d}.config-effect{font-size:7.5px;letter-spacing:.06em;color:#a4aaa5;white-space:nowrap}.config-module-price{font-family:"Inter Tight","Inter",sans-serif;font-size:11px;color:#d9ddd9;white-space:nowrap}.config-module>i{font-style:normal;text-align:right;font-size:7px;letter-spacing:.12em;color:#6e746f}.config-module[aria-pressed="true"]{background:linear-gradient(90deg,rgba(255,46,27,.055),transparent 54%);box-shadow:inset 2px 0 0 var(--accent)}.config-module[aria-pressed="true"]>i{color:#ff6255}.config-module[aria-pressed="true"] .config-effect{color:#e2e4e1}
.config-finishes{display:grid;grid-template-columns:repeat(3,1fr)}.config-finishes button{min-height:58px;border:0;border-right:1px solid #272a28;background:transparent;color:#7e847f;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer}.config-finishes button:last-child{border-right:0}.config-finishes button i{width:12px;height:12px;border-radius:50%;background:#db2f22;box-shadow:0 0 0 1px rgba(255,255,255,.1)}.config-finishes button:nth-child(2) i{background:#37ca76}.config-finishes button:nth-child(3) i{background:#111;border:1px solid #4a4e4b}.config-finishes button span{font-size:8px;letter-spacing:.1em}.config-finishes button.active{color:#f4f4f0;background:rgba(255,255,255,.018)}
.config-actions{display:grid;grid-template-columns:.8fr 1.2fr;border-top:1px solid #2b2e2b}.config-actions button{min-height:60px;padding:0 16px;border:0;background:transparent;color:#ddd;display:flex;align-items:center;justify-content:space-between;font-size:8px;letter-spacing:.12em;cursor:pointer}.config-save{border-right:1px solid #2b2e2b!important}.config-request{background:var(--accent)!important;color:#fff!important}.config-actions button i{font-style:normal;font-size:15px}.config-note{margin:0;padding:13px 16px;border-top:1px solid #252825;font-size:8px;line-height:1.5;color:#666c67}.activation-build{margin-top:22px;font-size:8px;letter-spacing:.16em;color:#7e847f;text-transform:uppercase}

/* Request / faux checkout */
.request{padding:110px var(--pad);background:#050605;position:relative;overflow:clip}.request:before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 80% 22%,rgba(255,46,27,.05),transparent 26%),linear-gradient(180deg,rgba(255,255,255,.008),transparent 28%)}.request-head,.request-layout{position:relative;z-index:1}.request-head{display:grid;grid-template-columns:1.1fr .72fr;gap:54px;align-items:end;margin-bottom:44px}.request-head h2{font-size:clamp(52px,5.5vw,92px);margin-top:22px}.request-head p{margin:0;max-width:500px;font-size:14px}
.request-layout{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(300px,.55fr);gap:28px;align-items:start}.request-form{border:1px solid #303330;background:linear-gradient(180deg,#0a0b0a,#070807);min-width:0}.request-progress{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid #2b2e2b}.request-progress button{position:relative;display:flex;align-items:center;gap:10px;min-height:62px;padding:12px 15px;border:0;border-right:1px solid #282b29;background:transparent;color:#6f7670;text-align:left;cursor:pointer}.request-progress button:last-child{border-right:0}.request-progress button:after{content:"";position:absolute;left:18%;right:18%;bottom:-1px;height:2px;background:var(--accent);transform:scaleX(0);transition:.25s}.request-progress button.active{color:#f2f2ee}.request-progress button.active:after{transform:scaleX(1)}.request-progress button.complete{color:#aeb4ae}.request-progress b{font-size:9px;color:var(--accent)}.request-progress span{display:grid;gap:3px;font-size:8px;letter-spacing:.11em}.request-progress small{font-size:6px;letter-spacing:.15em;color:#676e68}
.request-step{padding:24px}.request-step-title{display:flex;gap:13px;align-items:flex-start;padding-bottom:20px;border-bottom:1px solid #292c2a}.request-step-title>b{color:var(--accent);font-size:12px}.request-step-title div{display:grid;gap:5px}.request-step-title strong{font-size:12px;letter-spacing:.08em}.request-step-title small{font-size:8px;color:#747b75}.request-fields{display:grid;gap:15px;margin-top:22px}.request-fields.two-col{grid-template-columns:1fr 1fr}.request-field{display:grid;gap:7px;min-width:0}.request-field.full{grid-column:1/-1}.request-field>span{font-size:7px;letter-spacing:.16em;color:#7f8680}.request-field input{width:100%;height:52px;padding:0 14px;border:1px solid #303430;background:#080908;color:#f2f3ef;border-radius:0;outline:0;font:500 14px/1 "Inter",sans-serif;transition:border-color .2s,background .2s}.request-field input::placeholder{color:#555b56}.request-field input:focus{border-color:#6c726c;background:#0a0b0a}.request-field input.is-invalid{border-color:#a63b31}.field-hint,.field-error{font-size:7px;line-height:1.4;color:#666d67}.field-error{color:#d9665d;min-height:10px}
.phone-combo{display:grid;grid-template-columns:auto 1fr}.phone-prefix,.country-button{height:52px;border:1px solid #303430;background:#080908;color:#eceeea;cursor:pointer}.phone-prefix{min-width:112px;padding:0 12px;display:flex;align-items:center;gap:8px;border-right:0}.phone-prefix span{font-size:18px}.phone-prefix b{font-size:11px;font-weight:600;letter-spacing:.04em}.phone-prefix i,.country-button i{font-style:normal;color:#747b75;margin-left:auto}.country-button{width:100%;padding:0 14px;display:flex;align-items:center;gap:10px;text-align:left}.country-button>span{font-size:20px}.country-button b{font-size:11px;letter-spacing:.05em}.country-button.is-invalid{border-color:#a63b31}
.request-controls{display:grid;grid-template-columns:1fr auto;align-items:center;gap:12px;margin-top:24px;padding-top:18px;border-top:1px solid #292c2a}.request-controls button{min-height:48px;padding:0 15px;border:1px solid #343834;background:transparent;color:#cfd3cf;font-size:8px;letter-spacing:.12em;cursor:pointer}.request-controls .request-next,.request-controls .request-submit{min-width:184px;background:var(--accent);border-color:var(--accent);color:#fff;display:flex;align-items:center;justify-content:space-between;gap:20px}.request-controls button i{font-style:normal;font-size:14px}.request-back{justify-self:start}
.request-review{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:22px}.request-review article{min-height:116px;padding:16px;border:1px solid #2e322e;background:rgba(255,255,255,.008);display:grid;align-content:start;gap:7px}.request-review article.request-review-config{grid-column:1/-1}.request-review small{font-size:7px;letter-spacing:.16em;color:#737a74}.request-review strong{font-size:13px;color:#f0f1ed}.request-review span{font-size:9px;line-height:1.45;color:#888f89}.request-privacy{display:flex;gap:12px;margin-top:15px;padding:13px 14px;border-left:2px solid var(--accent);background:rgba(255,46,27,.035)}.request-privacy i{width:7px;height:7px;margin-top:5px;border-radius:50%;background:var(--accent);box-shadow:0 0 12px rgba(255,46,27,.3)}.request-privacy p{margin:0;font-size:8px;line-height:1.5;color:#7d847e}.request-privacy b{color:#c7cbc7}
.request-summary{position:sticky;top:calc(var(--header) + 18px);border:1px solid #303330;background:#080908}.request-bike{--request-accent:#ff3728;position:relative;overflow:hidden;aspect-ratio:1.25;border-bottom:1px solid #292c2a}.request-bike img{width:100%;height:100%;object-fit:cover;filter:brightness(.65) saturate(.82);transition:.4s}.request-bike:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 42%,rgba(3,3,3,.82)),radial-gradient(circle at 50% 80%,color-mix(in srgb,var(--request-accent) 22%,transparent),transparent 55%)}.request-bike[data-tone="green"]{--request-accent:#43df84}.request-bike[data-tone="green"] img{filter:hue-rotate(104deg) saturate(.75) brightness(.7)}.request-bike[data-tone="stealth"]{--request-accent:#aeb3b0}.request-bike[data-tone="stealth"] img{filter:grayscale(.92) brightness(.62)}.request-summary-head{display:grid;grid-template-columns:1fr auto;gap:14px;padding:16px;border-bottom:1px solid #292c2a}.request-summary-head span{display:grid;gap:5px}.request-summary-head span:last-child{text-align:right}.request-summary-head small,.request-summary-stats small,.request-summary-modules>small{font-size:6.5px;letter-spacing:.16em;color:#737a74}.request-summary-head strong{font-family:"Inter Tight","Inter",sans-serif;font-size:20px;letter-spacing:-.03em}.request-summary-stats{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid #292c2a}.request-summary-stats span{padding:12px;border-right:1px solid #292c2a;display:grid;gap:5px}.request-summary-stats span:last-child{border-right:0}.request-summary-stats b{font-size:10px;white-space:nowrap}.request-summary-modules{padding:14px 16px;border-bottom:1px solid #292c2a}.request-summary-modules>div{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.request-summary-modules span{padding:6px 7px;border:1px solid #303430;color:#8d948e;font-size:6.5px;letter-spacing:.07em}.request-summary-code{display:flex;justify-content:space-between;gap:12px;padding:12px 16px}.request-summary-code span{font-size:6.5px;letter-spacing:.16em;color:#737a74}.request-summary-code b{font-size:8px;letter-spacing:.08em}
.request-complete{padding:42px 26px 30px;min-height:520px;display:grid;align-content:center;justify-items:start;background:radial-gradient(circle at 20% 20%,rgba(255,46,27,.07),transparent 34%)}.request-lock-mark{display:flex;align-items:center;gap:9px;margin-bottom:34px}.request-lock-mark i{width:8px;height:8px;border-radius:50%;background:#52df88;box-shadow:0 0 18px rgba(82,223,136,.45)}.request-lock-mark span{font-size:7px;letter-spacing:.18em;color:#7c837d}.request-complete>small{font-size:8px;letter-spacing:.18em;color:#53d989}.request-complete h3{margin:12px 0 18px;font-family:"Inter Tight","Inter",sans-serif;font-size:clamp(42px,6vw,68px);line-height:.88;letter-spacing:-.055em}.request-complete p{max-width:560px;margin:0;color:#8a908b;font-size:11px;line-height:1.55}.request-code{display:grid;gap:6px;margin-top:28px;padding:13px 16px;border:1px solid #303430}.request-code span{font-size:6.5px;letter-spacing:.16em;color:#727973}.request-code b{font-size:14px;letter-spacing:.1em}.request-to-activation{width:min(360px,100%);height:54px;margin-top:28px;padding:0 16px;border:0;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:space-between;font-size:8px;letter-spacing:.12em;cursor:pointer}.request-to-activation i{font-style:normal;font-size:16px}

/* Searchable country / calling code picker */
.region-picker{width:min(560px,calc(100vw - 28px));max-height:min(78svh,720px);padding:0;border:1px solid #373b37;background:#080908;color:#f1f2ee}.region-picker::backdrop{background:rgba(0,0,0,.78);backdrop-filter:blur(8px)}.region-picker-panel{display:grid;grid-template-rows:auto auto minmax(0,1fr);max-height:min(78svh,720px)}.region-picker header{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:18px;border-bottom:1px solid #292c2a}.region-picker header div{display:grid;gap:5px}.region-picker header small{font-size:6.5px;letter-spacing:.17em;color:#727973}.region-picker header strong{font-size:13px;letter-spacing:.07em}.region-picker header button{width:42px;height:42px;border:1px solid #3b403b;border-radius:50%;background:#0b0c0b;color:#eee;font-size:22px;cursor:pointer}.region-search{display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:center;margin:14px 16px;padding:0 13px;height:48px;border:1px solid #303430;background:#060706}.region-search span{color:#7c837d}.region-search input{width:100%;border:0;outline:0;background:transparent;color:#f1f2ee;font-size:12px}.region-list{overflow:auto;padding:0 8px 10px}.region-option{width:100%;min-height:52px;padding:8px 10px;border:0;border-bottom:1px solid #222522;background:transparent;color:#dfe1dd;display:grid;grid-template-columns:32px minmax(0,1fr) auto;gap:10px;align-items:center;text-align:left;cursor:pointer}.region-option:hover{background:rgba(255,255,255,.025)}.region-option .flag{font-size:20px}.region-option strong{font-size:10px;font-weight:500}.region-option small{font-size:8px;color:#7c837d}.region-empty{padding:24px;text-align:center;color:#777e78;font-size:10px}

@media(hover:hover) and (pointer:fine){.config-presets button:hover,.config-finishes button:hover{background:rgba(255,255,255,.025);color:#fff}.config-module:hover{background:rgba(255,255,255,.018)}.config-preview-media:hover img{transform:scale(1.025)}.request-progress button:hover,.request-controls button:hover,.country-button:hover,.phone-prefix:hover{border-color:#555b55;color:#fff}}
@media(max-width:1100px){.config-layout{grid-template-columns:minmax(0,1fr) minmax(380px,.95fr)}.config-module{grid-template-columns:minmax(0,1fr) auto 82px}.config-module-price{display:none}}
@media(max-width:980px){.configurator,.request{padding:74px var(--pad)}.config-head,.request-head{grid-template-columns:1fr;gap:18px;margin-bottom:30px}.config-head h2,.request-head h2{font-size:49px}.config-head p,.request-head p{max-width:40ch}.config-layout,.request-layout{grid-template-columns:1fr;gap:18px}.config-preview,.request-summary{position:static}.config-preview-media{margin:0 calc(-1*var(--pad));border-left:0;border-right:0;aspect-ratio:1.2}.config-summary{margin:0 calc(-1*var(--pad));border-left:0;border-right:0}.config-panel{margin-top:4px}.config-module{grid-template-columns:minmax(0,1fr) auto;gap:8px}.config-module>i{grid-column:2;grid-row:1/4}.config-effect{grid-column:1}.config-module-price{display:block;grid-column:1;font-size:9px}.request-layout{display:flex;flex-direction:column}.request-summary{order:-1}.request-bike{display:none}.request-summary-modules{display:none}.request-summary-head{padding:13px 15px}.request-summary-stats span{padding:10px}.tech-sheet-v2 .tech-group{box-shadow:none!important}}
@media(max-width:620px){.request{padding-left:20px;padding-right:20px}.request-form,.request-summary{margin-left:-20px;margin-right:-20px;border-left:0;border-right:0}.request-progress button{min-height:58px;padding:10px}.request-progress b{display:none}.request-progress span{font-size:7px}.request-step{padding:20px}.request-fields.two-col{grid-template-columns:1fr}.request-field.full{grid-column:auto}.request-review{grid-template-columns:1fr}.request-review article.request-review-config{grid-column:auto}.request-controls{grid-template-columns:auto 1fr}.request-controls .request-next,.request-controls .request-submit{min-width:0}.request-summary-stats b{font-size:9px}.region-picker{width:100vw;max-width:none;height:min(78svh,700px);max-height:none;margin:auto 0 0;border-left:0;border-right:0;border-bottom:0}.region-picker-panel{max-height:none;height:100%}}
@media(max-width:520px){.configurator{padding-left:20px;padding-right:20px}.config-head h2,.request-head h2{font-size:43px}.config-preview-id{left:16px;right:16px;bottom:14px}.config-preview-id strong{font-size:28px}.config-summary-top{padding:14px 16px}.config-stats{grid-template-columns:repeat(3,1fr)}.config-stats>span{padding:12px 10px}.config-stats>span:nth-child(3){border-right:0}.config-stats>span:nth-child(n+4){border-top:1px solid #272a28}.config-stats>span:nth-child(5){border-right:0}.config-balance{display:grid;gap:5px}.config-balance b{text-align:left}.config-presets button{min-height:82px}.config-module{padding:13px 14px}.config-finishes button{min-height:54px}.config-actions{grid-template-columns:1fr}.config-save{border-right:0!important;border-bottom:1px solid #2b2e2b!important}.request-summary-head strong{font-size:18px}.request-step-title{padding-bottom:16px}.phone-prefix{min-width:100px}.request-complete{padding:34px 20px}.request-complete h3{font-size:42px}}
@media(prefers-reduced-motion:reduce){.config-preview-media img,.request-bike img{transition:none!important}}
'''

# --- JS: replace configurator tail with audited Configurator V2 + request flow ---
js_marker='/* VANTA R1 — Configurator 2026-09 */'
if js_marker not in js:
    raise SystemExit('JS configurator marker not found')
js=js[:js.index(js_marker)]
js+=r'''/* VANTA R1 — Configurator V2 + Request Flow 2026-09 */
(()=>{
  'use strict';
  const root=document.getElementById('configurator');
  if(!root)return;
  const base={power:210,torque:390,mass:189,range:320,charge:18,price:32900};
  const effects={
    performance:{power:18,torque:30,mass:3,range:-16,price:3900,label:'PERFORMANCE PACK'},
    aero:{mass:2,range:6,price:2600,label:'ACTIVE AERO'},
    carbon:{mass:-9,price:4800,label:'CARBON STRUCTURE'},
    range:{mass:12,range:52,charge:2,price:4200,label:'RANGE SYSTEM'},
    fast:{charge:-4,price:1900,label:'FAST CHARGE 800V'},
    telemetry:{price:1200,label:'RIDER TELEMETRY'}
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
  const deltas={power:q('cfgPowerDelta'),torque:q('cfgTorqueDelta'),mass:q('cfgMassDelta'),range:q('cfgRangeDelta'),charge:q('cfgChargeDelta')};
  const preview=q('configPreview'),save=q('configSave'),request=q('configRequest'),activationBuild=q('activationBuild');
  const presetButtons=[...root.querySelectorAll('[data-preset]')];
  const moduleButtons=[...root.querySelectorAll('[data-module]')];
  const toneButtons=[...root.querySelectorAll('[data-config-tone]')];
  const money=n=>new Intl.NumberFormat('ru-RU',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(n).replace(/ /g,' ');
  const sameSet=(a,b)=>a.size===b.length&&b.every(x=>a.has(x));
  const detectPreset=()=>Object.entries(presets).find(([,p])=>sameSet(state.modules,p.modules)&&state.tone===p.tone)?.[0]||'custom';
  const calculate=()=>{
    const out={...base};
    state.modules.forEach(key=>{const e=effects[key]||{};['power','torque','mass','range','charge','price'].forEach(k=>{if(typeof e[k]==='number')out[k]+=e[k];});});
    return out;
  };
  const signed=(value,unit,{inverse=false}={})=>{
    if(!value)return 'BASE';
    const good=inverse?value<0:value>0;
    return {text:`${value>0?'+':'−'}${Math.abs(value)} ${unit}`,good};
  };
  const snapshot=()=>{
    const values=calculate();
    const preset=detectPreset();
    const profile=preset==='custom'?'CUSTOM':presets[preset].label;
    const modules=[...state.modules];
    return {profile,preset,modules,tone:state.tone,values,code:`R1-${profile}-${String(modules.length).padStart(2,'0')}`,price:money(values.price),moduleLabels:modules.map(k=>effects[k]?.label||k)};
  };
  const paintDelta=(node,value,unit,options)=>{
    if(!node)return;
    const d=signed(value,unit,options);
    node.textContent=typeof d==='string'?d:d.text;
    node.classList.remove('is-positive','is-negative');
    if(typeof d!=='string')node.classList.add(d.good?'is-positive':'is-negative');
  };
  const render=()=>{
    state.preset=detectPreset();
    const snap=snapshot(),v=snap.values;
    profileLabel.textContent=snap.profile;
    const count=snap.modules.length;
    moduleCount.textContent=`${count} ${count===1?'МОДУЛЬ':count<5?'МОДУЛЯ':'МОДУЛЕЙ'}`;
    code.textContent=snap.code;price.textContent=snap.price;
    stats.power.textContent=`${v.power} кВт`;stats.torque.textContent=`${v.torque} Н·м`;stats.mass.textContent=`${v.mass} кг`;stats.range.textContent=`${v.range} км`;stats.charge.textContent=`${v.charge} мин`;
    paintDelta(deltas.power,v.power-base.power,'кВт');paintDelta(deltas.torque,v.torque-base.torque,'Н·м');paintDelta(deltas.mass,v.mass-base.mass,'кг',{inverse:true});paintDelta(deltas.range,v.range-base.range,'км');paintDelta(deltas.charge,v.charge-base.charge,'мин',{inverse:true});
    preview.dataset.tone=state.tone;
    presetButtons.forEach(btn=>{const on=btn.dataset.preset===state.preset;btn.classList.toggle('active',on);btn.setAttribute('aria-pressed',String(on));});
    moduleButtons.forEach(btn=>{const on=state.modules.has(btn.dataset.module);btn.setAttribute('aria-pressed',String(on));const status=btn.querySelector(':scope > i');if(status)status.textContent=on?'УСТАНОВЛЕНО':'ДОБАВИТЬ';});
    toneButtons.forEach(btn=>{const on=btn.dataset.configTone===state.tone;btn.classList.toggle('active',on);btn.setAttribute('aria-pressed',String(on));});
    if(activationBuild)activationBuild.textContent=`YOUR R1 / ${snap.profile} / ${count} MODULES`;
    window.dispatchEvent(new CustomEvent('vanta:configchange',{detail:snap}));
    return snap;
  };
  const usePreset=key=>{const p=presets[key];if(!p)return;state={preset:key,modules:new Set(p.modules),tone:p.tone};render();};
  presetButtons.forEach(btn=>btn.addEventListener('click',()=>usePreset(btn.dataset.preset)));
  moduleButtons.forEach(btn=>btn.addEventListener('click',()=>{const key=btn.dataset.module;if(state.modules.has(key))state.modules.delete(key);else state.modules.add(key);render();}));
  toneButtons.forEach(btn=>btn.addEventListener('click',()=>{state.tone=btn.dataset.configTone;render();}));
  save?.addEventListener('click',()=>{
    try{localStorage.setItem('vanta-r1-config',JSON.stringify({modules:[...state.modules],tone:state.tone}));}catch{}
    const span=save.querySelector('span');if(span){const original='СОХРАНИТЬ CONFIG';span.textContent='CONFIG СОХРАНЁН';setTimeout(()=>span.textContent=original,1400);}
  });
  request?.addEventListener('click',()=>document.getElementById('request')?.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}));
  try{const saved=JSON.parse(localStorage.getItem('vanta-r1-config')||'null');if(saved&&Array.isArray(saved.modules)){state.modules=new Set(saved.modules.filter(k=>effects[k]));state.tone=['red','green','stealth'].includes(saved.tone)?saved.tone:'red';}}catch{}
  window.vantaConfig={getSnapshot:snapshot,setTone:t=>{if(['red','green','stealth'].includes(t)){state.tone=t;render();}},render};
  render();
})();

(()=>{
  'use strict';
  const section=document.getElementById('request');
  const form=document.getElementById('requestForm');
  if(!section||!form)return;
  const q=id=>document.getElementById(id);
  const countries=[
    ['RU','Россия','+7'],['KZ','Казахстан','+7'],['BY','Беларусь','+375'],['DE','Германия','+49'],['FR','Франция','+33'],['IT','Италия','+39'],['ES','Испания','+34'],['PT','Португалия','+351'],['GB','Великобритания','+44'],['IE','Ирландия','+353'],['NL','Нидерланды','+31'],['BE','Бельгия','+32'],['LU','Люксембург','+352'],['CH','Швейцария','+41'],['AT','Австрия','+43'],['PL','Польша','+48'],['CZ','Чехия','+420'],['SK','Словакия','+421'],['HU','Венгрия','+36'],['RO','Румыния','+40'],['BG','Болгария','+359'],['GR','Греция','+30'],['CY','Кипр','+357'],['MT','Мальта','+356'],['HR','Хорватия','+385'],['SI','Словения','+386'],['RS','Сербия','+381'],['ME','Черногория','+382'],['BA','Босния и Герцеговина','+387'],['MK','Северная Македония','+389'],['AL','Албания','+355'],['EE','Эстония','+372'],['LV','Латвия','+371'],['LT','Литва','+370'],['FI','Финляндия','+358'],['SE','Швеция','+46'],['NO','Норвегия','+47'],['DK','Дания','+45'],['IS','Исландия','+354'],['MD','Молдова','+373'],['GE','Грузия','+995'],['AM','Армения','+374'],['AZ','Азербайджан','+994'],['UZ','Узбекистан','+998'],['TR','Турция','+90'],['IL','Израиль','+972'],['AE','ОАЭ','+971'],['SA','Саудовская Аравия','+966'],['QA','Катар','+974'],['IN','Индия','+91'],['CN','Китай','+86'],['JP','Япония','+81'],['KR','Южная Корея','+82'],['SG','Сингапур','+65'],['TH','Таиланд','+66'],['VN','Вьетнам','+84'],['ID','Индонезия','+62'],['MY','Малайзия','+60'],['AU','Австралия','+61'],['NZ','Новая Зеландия','+64'],['US','США','+1'],['CA','Канада','+1'],['MX','Мексика','+52'],['BR','Бразилия','+55'],['AR','Аргентина','+54'],['CL','Чили','+56'],['CO','Колумбия','+57'],['ZA','ЮАР','+27'],['EG','Египет','+20'],['MA','Марокко','+212']
  ].map(([iso,name,dial])=>({iso,name,dial}));
  const flag=iso=>String.fromCodePoint(...iso.toUpperCase().split('').map(c=>127397+c.charCodeAt()));
  const countryButton=q('countryButton'),countryFlag=q('countryFlag'),countryName=q('countryName'),countryError=q('countryError');
  const phoneButton=q('phoneRegionButton'),phoneFlag=q('phoneFlag'),phoneDial=q('phoneDial'),phone=q('reqPhone'),phoneHint=q('phoneHint');
  const picker=q('regionPicker'),pickerTitle=q('regionPickerTitle'),pickerClose=q('regionPickerClose'),search=q('regionSearch'),list=q('regionList');
  let pickerMode='country',deliveryCountry=null,phoneCountry=null,phoneManual=false,currentStep=1,currentConfig=window.vantaConfig?.getSnapshot?.()||null;
  const fields={first:q('reqFirst'),last:q('reqLast'),email:q('reqEmail'),region:q('reqRegion'),city:q('reqCity'),postal:q('reqPostal'),address:q('reqAddress'),address2:q('reqAddress2')};
  const steps=[...form.querySelectorAll('[data-request-step]')],nav=[...form.querySelectorAll('[data-request-nav]')];
  const moduleNames={performance:'Performance Pack',aero:'Active Aero',carbon:'Carbon Structure',range:'Range System',fast:'Fast Charge 800V',telemetry:'Rider Telemetry'};
  const formatNational=(raw,iso)=>{
    const d=raw.replace(/\D/g,'').slice(0,14);
    if(!d)return '';
    if(iso==='RU'||iso==='KZ'){return [d.slice(0,3),d.slice(3,6),d.slice(6,8),d.slice(8,10)].filter(Boolean).join(d.length>6?'-':' ')}
    if(iso==='US'||iso==='CA'){const a=d.slice(0,3),b=d.slice(3,6),c=d.slice(6,10);return `${a?`(${a}${a.length===3?') ':''}`:''}${b}${c?`-${c}`:''}`.trim()}
    return d.replace(/(\d{3})(?=\d)/g,'$1 ').trim();
  };
  phone?.addEventListener('input',()=>{const pos=phone.selectionStart||0;phone.value=formatNational(phone.value,phoneCountry?.iso||'');try{phone.setSelectionRange(phone.value.length,phone.value.length)}catch{}});
  const renderPicker=(query='')=>{
    const needle=query.trim().toLocaleLowerCase('ru');
    const rows=countries.filter(c=>!needle||c.name.toLocaleLowerCase('ru').includes(needle)||c.dial.includes(needle)||c.iso.toLowerCase()===needle);
    list.innerHTML=rows.length?rows.map(c=>`<button class="region-option" type="button" role="option" data-iso="${c.iso}"><span class="flag">${flag(c.iso)}</span><strong>${c.name}</strong><small>${c.dial}</small></button>`).join(''):'<div class="region-empty">Ничего не найдено</div>';
  };
  const openPicker=mode=>{
    pickerMode=mode;pickerTitle.textContent=mode==='country'?'ВЫБЕРИ СТРАНУ':'КОД ТЕЛЕФОНА';search.value='';renderPicker();
    if(picker.showModal)picker.showModal();else picker.setAttribute('open','');setTimeout(()=>search.focus(),50);
  };
  const closePicker=()=>picker.close?.();
  countryButton?.addEventListener('click',()=>openPicker('country'));phoneButton?.addEventListener('click',()=>openPicker('phone'));pickerClose?.addEventListener('click',closePicker);search?.addEventListener('input',()=>renderPicker(search.value));
  picker?.addEventListener('click',e=>{if(e.target===picker){closePicker();return;}const btn=e.target.closest('.region-option');if(!btn)return;const c=countries.find(x=>x.iso===btn.dataset.iso);if(!c)return;if(pickerMode==='country'){deliveryCountry=c;countryFlag.textContent=flag(c.iso);countryName.textContent=c.name.toUpperCase();countryButton.classList.remove('is-invalid');countryError.textContent='';if(!phoneManual){phoneCountry=c;phoneFlag.textContent=flag(c.iso);phoneDial.textContent=c.dial;phoneHint.textContent=`${c.name} ${c.dial} · код выбран по стране доставки.`;phone.value=formatNational(phone.value,c.iso);}}else{phoneCountry=c;phoneManual=true;phoneFlag.textContent=flag(c.iso);phoneDial.textContent=c.dial;phoneHint.textContent=`${c.name} ${c.dial} · регион номера выбран вручную.`;phone.value=formatNational(phone.value,c.iso);}closePicker();});
  const setStep=n=>{currentStep=n;steps.forEach(s=>{const on=Number(s.dataset.requestStep)===n;s.hidden=!on;s.classList.toggle('active',on);});nav.forEach(b=>{const x=Number(b.dataset.requestNav),on=x===n;b.classList.toggle('active',on);b.classList.toggle('complete',x<n);b.toggleAttribute('aria-current',on);});if(n===3)fillReview();};
  const validInput=input=>{if(!input)return true;const ok=input.checkValidity();input.classList.toggle('is-invalid',!ok);return ok;};
  const validateStep=n=>{
    if(n===1){const ok=[fields.first,fields.last,fields.email].every(validInput);const digits=phone.value.replace(/\D/g,'');const phoneOk=!!phoneCountry&&digits.length>=6;phone.classList.toggle('is-invalid',!phoneOk);if(!phoneCountry)phoneHint.textContent='Сначала выбери регион номера.';else if(!phoneOk)phoneHint.textContent='Проверь номер: нужно минимум 6 цифр.';return ok&&phoneOk;}
    if(n===2){let ok=[fields.city,fields.postal,fields.address].every(validInput);if(!deliveryCountry){countryButton.classList.add('is-invalid');countryError.textContent='Выбери страну.';ok=false;}return ok;}
    return true;
  };
  form.querySelectorAll('[data-request-next]').forEach(btn=>btn.addEventListener('click',()=>{if(validateStep(currentStep))setStep(Number(btn.dataset.requestNext));}));
  form.querySelectorAll('[data-request-back]').forEach(btn=>btn.addEventListener('click',()=>setStep(Number(btn.dataset.requestBack))));
  nav.forEach(btn=>btn.addEventListener('click',()=>{const n=Number(btn.dataset.requestNav);if(n<currentStep)setStep(n);else if(n===currentStep+1&&validateStep(currentStep))setStep(n);}));
  form.querySelectorAll('input').forEach(input=>input.addEventListener('input',()=>input.classList.remove('is-invalid')));
  const fullPhone=()=>phoneCountry?`${phoneCountry.dial} ${phone.value}`.trim():phone.value;
  const fillReview=()=>{q('reviewName').textContent=`${fields.first.value} ${fields.last.value}`.trim()||'—';q('reviewContact').textContent=[fields.email.value,fullPhone()].filter(Boolean).join(' · ')||'—';q('reviewCountry').textContent=deliveryCountry?`${flag(deliveryCountry.iso)} ${deliveryCountry.name}`:'—';q('reviewAddress').textContent=[fields.postal.value,fields.region.value,fields.city.value,fields.address.value,fields.address2.value].filter(Boolean).join(', ')||'—';if(currentConfig){q('reviewConfig').textContent=currentConfig.code;q('reviewModules').textContent=currentConfig.moduleLabels.join(' · ')||'BASE CONFIGURATION';}};
  const paintConfig=snap=>{currentConfig=snap;if(!snap)return;q('requestProfile').textContent=snap.profile;q('requestPrice').textContent=snap.price;q('requestPower').textContent=`${snap.values.power} кВт`;q('requestMass').textContent=`${snap.values.mass} кг`;q('requestRange').textContent=`${snap.values.range} км`;q('requestConfigCode').textContent=snap.code;q('requestBike').dataset.tone=snap.tone;q('requestModules').innerHTML=snap.modules.length?snap.modules.map(k=>`<span>${moduleNames[k]||k}</span>`).join(''):'<span>BASE CONFIGURATION</span>';if(currentStep===3)fillReview();};
  addEventListener('vanta:configchange',e=>paintConfig(e.detail));paintConfig(currentConfig);
  form.addEventListener('submit',e=>{e.preventDefault();if(!validateStep(1)||!validateStep(2)){setStep(!validateStep(1)?1:2);return;}fillReview();steps.forEach(s=>s.hidden=true);q('requestComplete').hidden=false;form.querySelector('.request-progress').hidden=true;const rnd=new Uint32Array(1);try{crypto.getRandomValues(rnd)}catch{rnd[0]=Math.floor(Math.random()*9999)}const suffix=String(rnd[0]%10000).padStart(4,'0');q('requestCode').textContent=`VR1-${currentConfig?.profile||'CUSTOM'}-${suffix}`;});
  q('requestToActivation')?.addEventListener('click',()=>{const tone=currentConfig?.tone||'red';document.querySelector(`.sw[data-color="${tone}"]`)?.click();document.getElementById('activate')?.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});});
  setStep(1);
})();
'''

html_p.write_text(html,encoding='utf-8')
css_p.write_text(css,encoding='utf-8')
js_p.write_text(js,encoding='utf-8')

# basic production validation
if html.count('id="request"')!=1: raise SystemExit('request section id count invalid')
ids=re.findall(r'id="([^"]+)"',html)
dups=sorted({x for x in ids if ids.count(x)>1})
if dups: raise SystemExit(f'duplicate ids: {dups}')
if css.count('{')!=css.count('}'): raise SystemExit('CSS brace mismatch')

# remove temporary runner payloads from final tree
Path('.qa/request-config-v2.py').unlink(missing_ok=True)
Path('.github/workflows/request-config-v2.yml').unlink(missing_ok=True)
