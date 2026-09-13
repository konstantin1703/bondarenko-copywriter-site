from pathlib import Path

ROOT = Path('.')
index = (ROOT / 'index.html').read_text(encoding='utf-8')
css = (ROOT / 'v4.css').read_text(encoding='utf-8')
js = (ROOT / 'v4.js').read_text(encoding='utf-8')

# Asset versions
index = index.replace('v4.css?v=20', 'v4.css?v=21').replace('v4.js?v=12', 'v4.js?v=13')

config_html = r'''<section class="configurator chapter" id="configurator">
  <div class="config-head reveal">
    <div>
      <div class="eyebrow">07 / R1 CONFIGURATOR / BUILD SYSTEM</div>
      <h2>Собери свой<br/><em>R1.</em></h2>
    </div>
    <p>Начни с заводского характера, добавь инженерные пакеты и сразу увидишь, как каждый выбор меняет динамику, массу, дальность и итоговую стоимость.</p>
  </div>

  <div class="config-layout">
    <div class="config-preview reveal">
      <div class="config-preview-media" data-tone="red" id="configPreview">
        <img alt="VANTA R1 — конфигуратор" decoding="async" loading="lazy" src="https://res.cloudinary.com/dg9shucn/image/upload/f_auto,q_auto:good,c_limit,w_1400/v1789100635/vanta-r1-hq-side.jpg"/>
        <div class="config-preview-glow" aria-hidden="true"></div>
        <div class="config-preview-id"><small>YOUR R1</small><strong id="configProfileLabel">ROAD</strong><span id="configModuleCount">2 МОДУЛЯ</span></div>
      </div>

      <div class="config-summary" aria-live="polite">
        <div class="config-summary-top">
          <span><small>BUILD CODE</small><strong id="configCode">R1-RD-SR-FC-TL</strong></span>
          <span class="config-price"><small>CONCEPT PRICE</small><strong id="configPrice">€36 000</strong></span>
        </div>
        <div class="config-character"><small>ХАРАКТЕР СБОРКИ</small><strong id="configCharacter">Сбалансированный / дорожный / быстрая зарядка</strong></div>
        <div class="config-compare-label"><span>BASE R1</span><span>YOUR R1</span></div>
        <div class="config-stats">
          <span><small>МОЩНОСТЬ</small><b id="cfgPower">210 кВт</b><em id="cfgPowerDelta">BASE</em></span>
          <span><small>МОМЕНТ</small><b id="cfgTorque">390 Н·м</b><em id="cfgTorqueDelta">BASE</em></span>
          <span><small>МАССА</small><b id="cfgMass">189 кг</b><em id="cfgMassDelta">BASE</em></span>
          <span><small>ЗАПАС</small><b id="cfgRange">320 км</b><em id="cfgRangeDelta">BASE</em></span>
          <span><small>10→80%</small><b id="cfgCharge">14 мин</b><em id="cfgChargeDelta">−4 мин</em></span>
        </div>
        <div class="config-balance"><span>БАЗОВАЯ КОНФИГУРАЦИЯ</span><b>210 кВт · 390 Н·м · 189 кг · 320 км · 18 мин</b></div>
        <div class="config-active-build"><div><small>ACTIVE BUILD</small><strong>УСТАНОВЛЕННЫЕ МОДУЛИ</strong></div><div id="configActiveModules"></div></div>
      </div>
    </div>

    <div class="config-panel reveal">
      <section class="config-step config-step-profile">
        <div class="config-step-head"><b>01</b><div><strong>ХАРАКТЕР</strong><small>FACTORY PROFILE</small></div></div>
        <div class="config-presets" aria-label="Профиль R1">
          <button class="active" data-preset="road" aria-pressed="true"><span>ДОРОГА</span><small>ROAD</small><p>Баланс отклика, зарядки и повседневной дальности.</p><i>FACTORY</i></button>
          <button data-preset="attack" aria-pressed="false"><span>ТРЕК</span><small>ATTACK</small><p>Максимальная отдача, меньше массы, жёстче характер.</p><i>FACTORY</i></button>
          <button data-preset="range" aria-pressed="false"><span>ЭКО</span><small>RANGE</small><p>Приоритет дальности, эффективности и энергетического цикла.</p><i>FACTORY</i></button>
        </div>
        <div class="factory-setup"><small>FACTORY SETUP</small><strong id="configFactoryCopy">FAST CHARGE 800V + RIDER TELEMETRY</strong></div>
      </section>

      <section class="config-step">
        <div class="config-step-head"><b>02</b><div><strong>ИНЖЕНЕРНЫЕ ПАКЕТЫ</strong><small>ENGINEERING OPTIONS</small></div></div>
        <div class="config-modules">
          <button class="config-module" data-module="performance" aria-pressed="false"><span class="module-index">P01</span><span class="config-module-copy"><strong>PERFORMANCE PACK</strong><small>Усиленная силовая электроника, охлаждение и более резкий профиль отдачи.</small></span><span class="config-effect">+18 кВт · +30 Н·м · +3 кг · −16 км</span><span class="config-module-price">+€3 900</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="aero" aria-pressed="false"><span class="module-index">A02</span><span class="config-module-copy"><strong>ACTIVE AERO</strong><small>Активная аэродинамика для стабильности и снижения сопротивления на скорости.</small></span><span class="config-effect">+2 кг · +6 км</span><span class="config-module-price">+€2 600</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="carbon" aria-pressed="false"><span class="module-index">C03</span><span class="config-module-copy"><strong>CARBON STRUCTURE</strong><small>Кованый карбон и облегчённые узлы для снижения массы.</small></span><span class="config-effect">−9 кг</span><span class="config-module-price">+€4 800</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="range" aria-pressed="false"><span class="module-index">R04</span><span class="config-module-copy"><strong>RANGE SYSTEM</strong><small>Увеличенный энергетический пакет для дальних маршрутов.</small></span><span class="config-effect">+52 км · +12 кг · +2 мин</span><span class="config-module-price">+€4 200</span><i>ДОБАВИТЬ</i></button>
          <button class="config-module" data-module="fast" aria-pressed="true"><span class="module-index">F05</span><span class="config-module-copy"><strong>FAST CHARGE 800V</strong><small>Расширенный термоконтроль и ускоренный зарядный профиль.</small></span><span class="config-effect">18 → 14 мин</span><span class="config-module-price">+€1 900</span><i>УСТАНОВЛЕНО</i></button>
          <button class="config-module" data-module="telemetry" aria-pressed="true"><span class="module-index">T06</span><span class="config-module-copy"><strong>RIDER TELEMETRY</strong><small>Данные поездки, состояние систем и расширенная аналитика сессии.</small></span><span class="config-effect">DATA+</span><span class="config-module-price">+€1 200</span><i>УСТАНОВЛЕНО</i></button>
        </div>
      </section>

      <section class="config-step">
        <div class="config-step-head"><b>03</b><div><strong>СВЕТОВАЯ ПОДПИСЬ</strong><small>LIGHT SIGNATURE</small></div></div>
        <div class="config-finishes" aria-label="Световая подпись конфигуратора">
          <button class="active" data-config-tone="red" aria-pressed="true"><i></i><span><b>SIGNAL RED</b><small>агрессивный акцент</small></span></button>
          <button data-config-tone="green" aria-pressed="false"><i></i><span><b>VOLT GREEN</b><small>энергетический акцент</small></span></button>
          <button data-config-tone="stealth" aria-pressed="false"><i></i><span><b>STEALTH</b><small>минимальная световая графика</small></span></button>
        </div>
      </section>

      <div class="config-actions">
        <button class="config-save" id="configSave" type="button"><span>СОХРАНИТЬ CONFIG</span><i>+</i></button>
        <button class="config-request" id="configRequest" type="button"><span>ПЕРЕЙТИ К ЗАЯВКЕ</span><i>→</i></button>
      </div>
      <p class="config-note">VANTA R1 / CONFIGURATION SYSTEM · параметры и стоимость относятся к концептуальной конфигурации проекта.</p>
    </div>
  </div>
</section>
'''

request_html = r'''<section class="request chapter" id="request">
  <div class="request-head reveal">
    <div>
      <div class="eyebrow">08 / REQUEST / APPLICATION</div>
      <h2>Зафиксируй<br/><em>свой R1.</em></h2>
    </div>
    <p>Контактные данные и адрес — последний шаг перед фиксацией выбранной конфигурации R1.</p>
  </div>

  <div class="request-layout">
    <form class="request-form reveal" id="requestForm" novalidate>
      <div class="request-progress" aria-label="Этапы заявки">
        <button class="active" type="button" data-request-nav="1" aria-current="step"><b>01</b><span>КОНТАКТЫ<small>IDENTITY</small></span></button>
        <button type="button" data-request-nav="2"><b>02</b><span>ДОСТАВКА<small>DELIVERY</small></span></button>
        <button type="button" data-request-nav="3"><b>03</b><span>ПРОВЕРКА<small>CONFIRM</small></span></button>
      </div>

      <section class="request-step active" data-request-step="1">
        <div class="request-step-title"><b>01</b><div><strong>КОНТАКТНЫЕ ДАННЫЕ</strong><small>Данные владельца конфигурации</small></div></div>
        <div class="request-fields two-col">
          <label class="request-field"><span>ИМЯ</span><input id="reqFirst" name="firstName" autocomplete="given-name" required placeholder="Иван"/></label>
          <label class="request-field"><span>ФАМИЛИЯ</span><input id="reqLast" name="lastName" autocomplete="family-name" required placeholder="Иванов"/></label>
          <label class="request-field full"><span>EMAIL</span><input id="reqEmail" name="email" autocomplete="email" inputmode="email" type="email" required placeholder="name@example.com"/></label>
          <div class="request-field full"><span>ТЕЛЕФОН</span><div class="phone-combo"><button class="phone-prefix" id="phoneRegionButton" type="button" aria-haspopup="dialog"><span class="region-symbol is-empty" id="phoneFlag" aria-hidden="true"></span><b id="phoneDial">Код</b><i>⌄</i></button><input id="reqPhone" name="phone" autocomplete="tel-national" inputmode="tel" required placeholder="Номер телефона"/></div><small class="field-hint" id="phoneHint">Выбери страну или телефонный код.</small></div>
        </div>
        <div class="request-controls"><span></span><button class="request-next" type="button" data-request-next="2">ПРОДОЛЖИТЬ <i>→</i></button></div>
      </section>

      <section class="request-step" data-request-step="2" hidden>
        <div class="request-step-title"><b>02</b><div><strong>АДРЕС</strong><small>Адрес доставки R1</small></div></div>
        <div class="request-fields two-col">
          <div class="request-field full"><span>СТРАНА</span><button class="country-button" id="countryButton" type="button" aria-haspopup="dialog"><span class="region-symbol is-empty" id="countryFlag" aria-hidden="true"></span><b id="countryName">ВЫБЕРИ СТРАНУ</b><i>⌄</i></button><small class="field-error" id="countryError"></small></div>
          <label class="request-field"><span>РЕГИОН / ОБЛАСТЬ / ШТАТ</span><input id="reqRegion" name="region" autocomplete="address-level1" placeholder="Регион"/></label>
          <label class="request-field"><span>ГОРОД</span><input id="reqCity" name="city" autocomplete="address-level2" required placeholder="Город"/></label>
          <label class="request-field"><span>ИНДЕКС</span><input id="reqPostal" name="postal" autocomplete="postal-code" required placeholder="000000"/></label>
          <label class="request-field full"><span>АДРЕС</span><input id="reqAddress" name="address" autocomplete="street-address" required placeholder="Улица, дом"/></label>
          <label class="request-field full"><span>ДОПОЛНИТЕЛЬНО</span><input id="reqAddress2" name="address2" autocomplete="address-line2" placeholder="Квартира / офис / комментарий"/></label>
        </div>
        <div class="request-controls"><button class="request-back" type="button" data-request-back="1">← НАЗАД</button><button class="request-next" type="button" data-request-next="3">ПРОВЕРИТЬ <i>→</i></button></div>
      </section>

      <section class="request-step" data-request-step="3" hidden>
        <div class="request-step-title"><b>03</b><div><strong>ПРОВЕРКА ЗАЯВКИ</strong><small>Проверь данные перед подтверждением</small></div></div>
        <div class="request-review">
          <article><small>КОНТАКТ</small><strong id="reviewName">—</strong><span id="reviewContact">—</span></article>
          <article><small>ДОСТАВКА</small><strong id="reviewCountry">—</strong><span id="reviewAddress">—</span></article>
          <article class="request-review-config"><small>КОНФИГУРАЦИЯ</small><strong id="reviewConfig">—</strong><span id="reviewModules">—</span></article>
        </div>
        <div class="request-controls"><button class="request-back" type="button" data-request-back="2">← НАЗАД</button><button class="request-submit" type="submit">ПОДТВЕРДИТЬ ЗАЯВКУ <i>→</i></button></div>
      </section>

      <section class="request-complete" id="requestComplete" hidden>
        <div class="request-lock-mark"><i></i><span>R1 / REQUEST SYSTEM</span></div>
        <small>CONFIGURATION LOCKED</small>
        <h3>ЗАЯВКА<br/>СФОРМИРОВАНА.</h3>
        <p>Конфигурация R1 закреплена за заявкой. Система готова перейти к активации выбранного профиля.</p>
        <div class="request-code"><span>REQUEST ID</span><b id="requestCode">—</b></div>
        <button class="request-to-activation" id="requestToActivation" type="button"><span>АКТИВИРОВАТЬ СВОЙ R1</span><i>→</i></button>
      </section>
    </form>

    <aside class="request-summary reveal" aria-live="polite">
      <div class="request-summary-kicker"><span></span>YOUR CONFIGURATION</div>
      <div class="request-bike" data-tone="red" id="requestBike"><img alt="VANTA R1 — выбранная конфигурация" loading="lazy" decoding="async" src="https://res.cloudinary.com/dg9shucn/image/upload/f_auto,q_auto:good,c_limit,w_900/v1789100635/vanta-r1-hq-side.jpg"/><div></div></div>
      <div class="request-summary-head"><span><small>YOUR R1</small><strong id="requestProfile">ROAD</strong></span><span><small>CONCEPT PRICE</small><strong id="requestPrice">€36 000</strong></span></div>
      <div class="request-summary-stats"><span><small>POWER</small><b id="requestPower">210 кВт</b></span><span><small>MASS</small><b id="requestMass">189 кг</b></span><span><small>RANGE</small><b id="requestRange">320 км</b></span></div>
      <div class="request-summary-modules"><small>ACTIVE BUILD</small><div id="requestModules"></div></div>
      <div class="request-summary-code"><span>BUILD CODE</span><b id="requestConfigCode">R1-RD-SR-FC-TL</b></div>
    </aside>
  </div>

  <dialog class="region-picker" id="regionPicker" aria-labelledby="regionPickerTitle">
    <div class="region-picker-panel">
      <header><div><small>REGION DATABASE</small><strong id="regionPickerTitle">ВЫБЕРИ СТРАНУ</strong></div><button id="regionPickerClose" type="button" aria-label="Закрыть выбор страны">×</button></header>
      <label class="region-search"><span aria-hidden="true"></span><input id="regionSearch" type="search" autocomplete="off" placeholder="Страна или код +7"/></label>
      <div class="region-list" id="regionList" role="listbox"></div>
    </div>
  </dialog>
</section>
'''

tech_html = r'''<dialog aria-labelledby="techTitle" class="tech-sheet" id="techSheet">
<div class="tech-sheet-panel tech-profile-v3">
  <div class="tech-sheet-head tech-profile-head">
    <div class="tech-sheet-titleblock">
      <small>R1 / ENGINEERING PROFILE / CORE DATA</small>
      <h2 id="techTitle">ИНЖЕНЕРНЫЙ<br/>ПРОФИЛЬ R1</h2>
      <p>Шесть параметров, которые формируют отклик, тягу, энергетический цикл, массу и практическую дальность R1.</p>
    </div>
    <button aria-label="Закрыть инженерный профиль" id="techClose" type="button">×</button>
  </div>

  <div class="tech-profile-groups">
    <section class="tech-profile-group">
      <header><b>01</b><div><h3>ПРИВОД</h3><small>DRIVE SYSTEM</small></div></header>
      <div class="tech-profile-metrics">
        <article><div class="tech-profile-value"><strong>210</strong><em>кВт</em></div><h4>Пиковая мощность</h4><p>Максимальная целевая отдача электрического привода.</p></article>
        <article><div class="tech-profile-value"><strong>390</strong><em>Н·м</em></div><h4>Крутящий момент</h4><p>Тяга доступна практически сразу после открытия газа.</p></article>
      </div>
      <div class="tech-profile-impact"><small>ЧТО ЭТО ДАЁТ</small><p>Мгновенный отклик и высокий темп разгона без паузы на переключения.</p></div>
    </section>

    <section class="tech-profile-group">
      <header><b>02</b><div><h3>ЭНЕРГОСИСТЕМА</h3><small>ENERGY SYSTEM</small></div></header>
      <div class="tech-profile-metrics">
        <article><div class="tech-profile-value"><strong>800</strong><em>В</em></div><h4>Высоковольтная архитектура</h4><p>Основа для высокой мощности и эффективной быстрой зарядки.</p></article>
        <article><div class="tech-profile-value"><strong>18</strong><em>мин</em></div><h4>Зарядка 10→80%</h4><p>Целевой энергетический цикл на совместимой DC-станции.</p></article>
      </div>
      <div class="tech-profile-impact"><small>ЧТО ЭТО ДАЁТ</small><p>Высокую скорость восстановления заряда и устойчивую отдачу силовой системы.</p></div>
    </section>

    <section class="tech-profile-group">
      <header><b>03</b><div><h3>ХОДОВОЙ ПРОФИЛЬ</h3><small>VEHICLE PROFILE</small></div></header>
      <div class="tech-profile-metrics">
        <article><div class="tech-profile-value"><strong>189</strong><em>кг</em></div><h4>Целевая масса</h4><p>Расчётная масса базовой инженерной конфигурации R1.</p></article>
        <article><div class="tech-profile-value"><strong>320</strong><em>км</em></div><h4>Запас хода</h4><p>Расчётная дальность базовой конфигурации на одном заряде.</p></article>
      </div>
      <div class="tech-profile-impact"><small>ЧТО ЭТО ДАЁТ</small><p>Баланс между управляемостью, плотностью компоновки и практической дальностью.</p></div>
    </section>
  </div>

  <div class="tech-conclusion">
    <div><small>ИНЖЕНЕРНЫЙ ИТОГ</small><strong>Характер R1 складывается не из одной большой цифры.</strong></div>
    <p><b>210 кВт и 390 Н·м</b> формируют отклик и тягу. <b>800 В и 18 минут</b> определяют энергетический темп. <b>189 кг и 320 км</b> задают баланс динамики, массы и реальной дальности.</p>
  </div>
</div>
</dialog>
'''

# Replace major HTML regions by stable section boundaries.
config_start = index.index('<section class="configurator chapter" id="configurator">')
request_start = index.index('<section class="request chapter" id="request">')
activate_start = index.index('<section class="activate chapter" id="activate">')
index = index[:config_start] + config_html + '\n' + request_html + '\n' + index[activate_start:]

tech_start = index.index('<dialog aria-labelledby="techTitle" class="tech-sheet" id="techSheet">')
footer_start = index.index('<footer>')
index = index[:tech_start] + tech_html + '\n' + index[footer_start:]

# Remove demo wording from activation surface as part of the product illusion.
index = index.replace('<div class="eyebrow">09 / ACTIVATION / DEMO</div>', '<div class="eyebrow">09 / ACTIVATION / SYSTEM</div>')
index = index.replace('Запусти демонстрационный режим: оптика проснётся, световая система активируется, а цветовой характер сцены изменится.', 'Запусти R1: оптика проснётся, световая система активируется, а выбранный характер сцены перейдёт в рабочий режим.')

# Consolidate the final product-flow CSS tail instead of stacking another override layer.
css_marker = '/* VANTA R1 — Tech Sheet Reinforcement + Configurator V2 + Request Flow 2026-09 */'
if css_marker in css:
    css = css[:css.index(css_marker)].rstrip() + '\n\n'

css += r'''/* VANTA R1 — Product Flow V3 / Engineering Profile / Configurator / Request 2026-09 */

/* Engineering Profile */
.tech-profile-v3{width:min(1040px,calc(100vw - 34px))!important;max-height:min(92svh,940px)!important;overflow:auto!important;padding:30px!important;border:1px solid #383c39!important;background:radial-gradient(circle at 8% 0%,rgba(255,48,32,.085),transparent 24%),linear-gradient(180deg,#0a0b0a,#060706)!important;box-shadow:0 34px 100px rgba(0,0,0,.68),inset 0 1px 0 rgba(255,255,255,.025)!important;isolation:isolate}
.tech-profile-v3:before{content:"";position:absolute;z-index:-1;inset:0;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.012) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.01) 1px,transparent 1px);background-size:54px 54px;mask-image:linear-gradient(180deg,#000,transparent 68%)}
.tech-profile-head{display:flex!important;justify-content:space-between!important;align-items:flex-start!important;gap:30px!important;padding:0 0 26px!important;margin:0 0 18px!important;border-bottom:1px solid #303330!important}
.tech-profile-head .tech-sheet-titleblock{max-width:760px}.tech-profile-head .tech-sheet-titleblock>small{display:block;margin-bottom:12px;color:#979d98;font-size:9px;letter-spacing:.19em}.tech-profile-head .tech-sheet-titleblock h2{margin:0!important;font-size:clamp(44px,6.1vw,78px)!important;line-height:.86!important;letter-spacing:-.055em!important;color:#f5f6f2!important}.tech-profile-head .tech-sheet-titleblock h2:after{content:"";display:block;width:88px;height:2px;margin-top:16px;background:var(--accent);box-shadow:0 0 18px rgba(255,46,27,.22)}.tech-profile-head .tech-sheet-titleblock>p{max-width:660px;margin:17px 0 0!important;color:#a4a9a4!important;font-size:13px!important;line-height:1.55!important}
.tech-profile-head #techClose{flex:0 0 54px;width:54px!important;height:54px!important;border-radius:50%!important;border:1px solid #3d423e!important;background:#0a0b0a!important;color:transparent!important;position:relative!important}.tech-profile-head #techClose:before,.tech-profile-head #techClose:after{content:"";position:absolute;left:50%;top:50%;width:19px;height:1.5px;background:#eef0ec;transform-origin:center}.tech-profile-head #techClose:before{transform:translate(-50%,-50%) rotate(45deg)}.tech-profile-head #techClose:after{transform:translate(-50%,-50%) rotate(-45deg)}
.tech-profile-groups{display:grid;gap:10px}.tech-profile-group{display:grid;grid-template-columns:180px minmax(0,1fr) 260px;border:1px solid #2e322f;background:linear-gradient(90deg,rgba(255,48,32,.024),rgba(255,255,255,.007) 24%,transparent);position:relative;overflow:hidden}.tech-profile-group:before{content:"";position:absolute;left:0;top:0;width:64px;height:2px;background:var(--accent)}
.tech-profile-group>header{padding:24px 22px;border-right:1px solid #292d2a;display:grid;align-content:start;gap:34px}.tech-profile-group>header>b{font-size:21px;line-height:1;color:var(--accent);letter-spacing:.08em}.tech-profile-group>header h3{margin:0;color:#f2f3ef;font-size:13px;line-height:1.08;letter-spacing:.06em}.tech-profile-group>header small{display:block;margin-top:6px;color:#727973;font-size:7px;letter-spacing:.17em}
.tech-profile-metrics{display:grid;grid-template-columns:1fr 1fr}.tech-profile-metrics article{padding:23px 22px;min-width:0;border-right:1px solid #292d2a}.tech-profile-metrics article:last-child{border-right:0}.tech-profile-value{display:flex;align-items:baseline;gap:8px;margin-bottom:14px;white-space:nowrap}.tech-profile-value strong{font-family:"Inter Tight","Inter",sans-serif;font-size:clamp(52px,5.2vw,72px);font-weight:500;line-height:.82;letter-spacing:-.065em;color:#f8f9f5;font-variant-numeric:tabular-nums}.tech-profile-value em{font-style:normal;color:#b7bcb7;font-size:10px;font-weight:600;letter-spacing:.08em}.tech-profile-metrics h4{margin:0 0 8px;color:#e6e9e5;font-size:9.5px;letter-spacing:.055em;text-transform:uppercase}.tech-profile-metrics p{margin:0;color:#858b86;font-size:9px;line-height:1.48}
.tech-profile-impact{padding:23px 21px;border-left:1px solid #292d2a;display:flex;flex-direction:column;justify-content:center;background:rgba(255,255,255,.008)}.tech-profile-impact small{color:#ff6255;font-size:7px;letter-spacing:.17em}.tech-profile-impact p{margin:11px 0 0;color:#b3b8b3;font-size:10px;line-height:1.55}
.tech-conclusion{display:grid;grid-template-columns:.82fr 1.18fr;gap:28px;margin-top:13px;padding:22px;border:1px solid #303431;border-left:2px solid var(--accent);background:linear-gradient(90deg,rgba(255,48,32,.045),rgba(255,255,255,.006) 40%,transparent)}.tech-conclusion small{display:block;color:#ff6255;font-size:8px;letter-spacing:.18em}.tech-conclusion strong{display:block;margin-top:9px;color:#f0f2ee;font-size:17px;line-height:1.26}.tech-conclusion p{margin:0;color:#a7aca7;font-size:10.5px;line-height:1.6}.tech-conclusion b{color:#eceeeb;font-weight:600}

/* Configurator V3 */
.configurator{padding:116px var(--pad);background:#050605;position:relative;overflow:clip}.configurator:before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 20% 27%,rgba(255,46,27,.07),transparent 28%),linear-gradient(180deg,transparent 0 72%,rgba(255,255,255,.012));opacity:.95}.config-head,.config-layout{position:relative;z-index:1}.config-head{display:grid;grid-template-columns:1.15fr .72fr;gap:58px;align-items:end;margin-bottom:46px}.config-head h2{font-size:clamp(54px,5.8vw,96px);margin-top:22px}.config-head p{margin:0;max-width:520px;font-size:14px;line-height:1.55}
.config-layout{display:grid;grid-template-columns:minmax(0,1.02fr) minmax(430px,.98fr);gap:30px;align-items:start}.config-preview{position:sticky;top:calc(var(--header) + 18px)}.config-preview-media{--config-accent:#ff3728;position:relative;overflow:hidden;border:1px solid #333734;background:#060706;aspect-ratio:1.18}.config-preview-media img{width:100%;height:100%;object-fit:cover;filter:brightness(.82) saturate(.92);transform:scale(1.02);transition:filter .5s ease,transform .65s var(--motion-ease)}.config-preview-media:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,transparent 44%,rgba(2,3,2,.82)),radial-gradient(circle at 58% 55%,color-mix(in srgb,var(--config-accent) 17%,transparent),transparent 43%)}.config-preview-media[data-tone="green"]{--config-accent:#47df86}.config-preview-media[data-tone="stealth"]{--config-accent:#aeb3b0}.config-preview-media[data-tone="green"] img{filter:hue-rotate(104deg) saturate(.78) brightness(.84)}.config-preview-media[data-tone="stealth"] img{filter:grayscale(.9) brightness(.7) contrast(1.06)}.config-preview-glow{position:absolute;z-index:2;inset:auto 8% 0;height:39%;background:radial-gradient(ellipse at 50% 100%,color-mix(in srgb,var(--config-accent) 30%,transparent),transparent 68%);mix-blend-mode:screen;opacity:.58}.config-preview-id{position:absolute;z-index:3;left:22px;right:22px;bottom:20px;display:grid;grid-template-columns:auto 1fr auto;align-items:end;gap:12px}.config-preview-id small,.config-preview-id span{font-size:8px;letter-spacing:.17em;color:#909691}.config-preview-id strong{font-family:"Inter Tight","Inter",sans-serif;font-size:36px;letter-spacing:-.045em;font-weight:600;color:#fff}.config-preview-id span{text-align:right}
.config-summary{border:1px solid #333734;border-top:0;background:rgba(7,8,7,.96);backdrop-filter:blur(15px)}.config-summary-top{display:grid;grid-template-columns:1fr auto;gap:24px;padding:17px 20px;border-bottom:1px solid #2a2e2b}.config-summary-top span{display:grid;gap:5px}.config-summary-top small,.config-stats small{font-size:7px;letter-spacing:.16em;color:#777e79}.config-summary-top strong{font-size:12px;letter-spacing:.07em}.config-price{text-align:right}.config-price strong{font-family:"Inter Tight","Inter",sans-serif;font-size:27px!important;letter-spacing:-.04em!important;color:#fff}.config-character{padding:15px 20px;border-bottom:1px solid #292d2a;display:grid;gap:7px;background:linear-gradient(90deg,rgba(255,46,27,.035),transparent)}.config-character small{font-size:7px;letter-spacing:.16em;color:#777e79}.config-character strong{font-size:11px;color:#dedfdb;font-weight:500}.config-compare-label{display:flex;justify-content:space-between;padding:9px 13px 0;color:#5f6660;font-size:6px;letter-spacing:.15em}.config-stats{display:grid;grid-template-columns:repeat(5,1fr)}.config-stats>span{min-width:0;padding:13px 10px 15px;border-right:1px solid #282c29;display:grid;gap:5px}.config-stats>span:last-child{border-right:0}.config-stats b{font-size:12px;font-weight:600;white-space:nowrap}.config-stats em{font-style:normal;font-size:6.5px;letter-spacing:.07em;color:#727873}.config-stats em.is-positive{color:#74db9f}.config-stats em.is-negative{color:#ff776c}.config-balance{display:flex;justify-content:space-between;gap:16px;padding:10px 14px;border-top:1px solid #272b28;color:#666d67}.config-balance span{font-size:6px;letter-spacing:.15em}.config-balance b{font-size:7px;letter-spacing:.04em;font-weight:500;text-align:right}.config-active-build{display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 16px;border-top:1px solid #292d2a;align-items:center}.config-active-build>div:first-child{display:grid;gap:4px}.config-active-build small{font-size:6.5px;letter-spacing:.17em;color:#6c736d}.config-active-build strong{font-size:8px;letter-spacing:.08em;color:#c9cdc9}.config-active-build>#configActiveModules{display:flex;gap:6px;justify-content:flex-end;flex-wrap:wrap}.config-active-build>#configActiveModules span{padding:5px 7px;border:1px solid #303531;color:#aeb4ae;font-size:6.5px;letter-spacing:.07em}
.config-panel{border:1px solid #333734;background:linear-gradient(180deg,#0a0b0a,#070807);box-shadow:0 28px 80px rgba(0,0,0,.22)}.config-step+.config-step{border-top:1px solid #2c302d}.config-step-head{display:flex;align-items:center;gap:12px;padding:16px 18px;border-bottom:1px solid #272b28;background:rgba(255,255,255,.008)}.config-step-head b{color:var(--accent);font-size:11px;letter-spacing:.1em}.config-step-head div{display:grid;gap:3px}.config-step-head strong{font-size:10px;letter-spacing:.12em}.config-step-head small{font-size:7px;letter-spacing:.17em;color:#737a74}
.config-presets{display:grid;grid-template-columns:repeat(3,1fr)}.config-presets button{position:relative;min-height:136px;padding:18px 13px;border:0;border-right:1px solid #292d2a;background:transparent;color:#878e88;cursor:pointer;display:grid;align-content:start;justify-items:start;gap:5px;text-align:left}.config-presets button:last-child{border-right:0}.config-presets button:after{content:"";position:absolute;left:15px;right:15px;bottom:0;height:2px;border-radius:2px;background:var(--accent);transform:scaleX(0);transform-origin:left;transition:.25s}.config-presets button.active{color:#f5f5f1;background:linear-gradient(180deg,rgba(255,46,27,.045),transparent)}.config-presets button.active:after{transform:scaleX(1)}.config-presets span{font-size:12px;letter-spacing:.07em}.config-presets small{font-size:7px;letter-spacing:.16em;color:inherit}.config-presets p{margin:9px 0 0;color:#727872;font-size:8px;line-height:1.45}.config-presets i{margin-top:auto;font-style:normal;font-size:6.5px;letter-spacing:.13em;color:#646b65}.factory-setup{display:flex;justify-content:space-between;gap:18px;padding:12px 16px;border-top:1px solid #272b28;background:#080908}.factory-setup small{font-size:6.5px;letter-spacing:.16em;color:#6e756f}.factory-setup strong{font-size:7.5px;letter-spacing:.06em;font-weight:500;color:#afb4af;text-align:right}
.config-modules{display:grid}.config-module{display:grid;grid-template-columns:34px minmax(0,1fr) auto auto 88px;gap:12px;align-items:center;min-height:88px;padding:15px 16px;border:0;border-bottom:1px solid #252925;background:transparent;text-align:left;cursor:pointer;transition:background .25s}.config-module:last-child{border-bottom:0}.module-index{align-self:start;padding-top:1px;color:#5f665f;font-size:7px;letter-spacing:.12em}.config-module-copy{display:grid;gap:5px;min-width:0}.config-module-copy strong{font-size:10px;letter-spacing:.085em}.config-module-copy small{font-size:8px;line-height:1.43;color:#7d837e}.config-effect{font-size:7.3px;letter-spacing:.055em;color:#a7ada8;white-space:nowrap}.config-module-price{font-family:"Inter Tight","Inter",sans-serif;font-size:11px;color:#dcdeda;white-space:nowrap}.config-module>i{font-style:normal;text-align:right;font-size:7px;letter-spacing:.11em;color:#6e746f}.config-module[aria-pressed="true"]{background:linear-gradient(90deg,rgba(255,46,27,.06),transparent 57%);box-shadow:inset 2px 0 0 var(--accent)}.config-module[aria-pressed="true"] .module-index,.config-module[aria-pressed="true"]>i{color:#ff6659}.config-module[aria-pressed="true"] .config-effect{color:#e1e4e0}
.config-finishes{display:grid;grid-template-columns:repeat(3,1fr)}.config-finishes button{min-height:76px;padding:12px;border:0;border-right:1px solid #292d2a;background:transparent;color:#7f8580;display:flex;align-items:center;justify-content:flex-start;gap:10px;cursor:pointer;text-align:left}.config-finishes button:last-child{border-right:0}.config-finishes button>i{width:12px;height:12px;border-radius:50%;background:#db2f22;box-shadow:0 0 0 1px rgba(255,255,255,.1)}.config-finishes button:nth-child(2)>i{background:#39ce79}.config-finishes button:nth-child(3)>i{background:#111;border:1px solid #4a4e4b}.config-finishes button span{display:grid;gap:3px}.config-finishes button b{font-size:8px;letter-spacing:.09em}.config-finishes button small{font-size:6.5px;color:#666d67;line-height:1.3}.config-finishes button.active{color:#f4f4f0;background:rgba(255,255,255,.018)}
.config-actions{display:grid;grid-template-columns:.78fr 1.22fr;border-top:1px solid #2c302d}.config-actions button{min-height:62px;padding:0 17px;border:0;background:transparent;color:#ddd;display:flex;align-items:center;justify-content:space-between;font-size:8px;letter-spacing:.12em;cursor:pointer}.config-save{border-right:1px solid #2c302d!important}.config-request{background:var(--accent)!important;color:#fff!important}.config-actions button i{font-style:normal;font-size:15px}.config-note{margin:0;padding:12px 16px;border-top:1px solid #272b28;color:#666d67;font-size:7.5px;line-height:1.5}.activation-build{margin-top:22px;font-size:8px;letter-spacing:.16em;color:#7e847f;text-transform:uppercase}

/* Request V2 */
.request{padding:116px var(--pad);background:#050605;position:relative;overflow:clip}.request:before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 78% 18%,rgba(255,46,27,.065),transparent 25%),linear-gradient(180deg,rgba(255,255,255,.008),transparent 32%)}.request-head,.request-layout{position:relative;z-index:1}.request-head{display:grid;grid-template-columns:1.1fr .72fr;gap:54px;align-items:end;margin-bottom:44px}.request-head h2{font-size:clamp(54px,5.8vw,94px);margin-top:22px}.request-head p{margin:0;max-width:480px;font-size:14px;line-height:1.55}.request-layout{display:grid;grid-template-columns:minmax(0,1.06fr) minmax(360px,.78fr);gap:30px;align-items:start}
.request-form{border:1px solid #333734;background:linear-gradient(180deg,#0a0b0a,#070807);min-width:0;box-shadow:0 28px 80px rgba(0,0,0,.18)}.request-progress{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid #2c302d}.request-progress button{position:relative;display:flex;align-items:center;gap:11px;min-height:68px;padding:13px 16px;border:0;border-right:1px solid #292d2a;background:transparent;color:#6f7670;text-align:left;cursor:pointer}.request-progress button:last-child{border-right:0}.request-progress button:after{content:"";position:absolute;left:16px;right:16px;bottom:-1px;height:2px;background:var(--accent);transform:scaleX(0);transform-origin:left;transition:.25s}.request-progress button.active{color:#f2f2ee;background:linear-gradient(180deg,rgba(255,46,27,.035),transparent)}.request-progress button.active:after{transform:scaleX(1)}.request-progress button.complete{color:#aeb4ae}.request-progress b{font-size:10px;color:var(--accent)}.request-progress span{display:grid;gap:3px;font-size:8px;letter-spacing:.1em}.request-progress small{font-size:6px;letter-spacing:.15em;color:#676e68}
.request-step{padding:28px}.request-step-title{display:flex;gap:14px;align-items:flex-start;padding-bottom:21px;border-bottom:1px solid #2b2f2c}.request-step-title>b{color:var(--accent);font-size:13px}.request-step-title div{display:grid;gap:5px}.request-step-title strong{font-size:13px;letter-spacing:.075em}.request-step-title small{font-size:8px;color:#747b75}.request-fields{display:grid;gap:17px;margin-top:24px}.request-fields.two-col{grid-template-columns:1fr 1fr}.request-field{display:grid;gap:8px;min-width:0;position:relative}.request-field.full{grid-column:1/-1}.request-field>span{font-size:7px;letter-spacing:.17em;color:#8b928c}.request-field input,.phone-prefix,.country-button{height:58px;border:1px solid #333834;background:linear-gradient(180deg,#090a09,#070807);color:#f0f2ee;outline:0;border-radius:0;transition:border-color .2s,background .2s,box-shadow .2s}.request-field input{width:100%;padding:0 16px;font:500 14px/1 "Inter",sans-serif}.request-field input::placeholder{color:#515751}.request-field:focus-within>span{color:#c2c7c2}.request-field input:focus,.phone-combo:focus-within .phone-prefix,.phone-combo:focus-within input,.country-button:focus{border-color:#626a63;background:#0b0c0b;box-shadow:inset 0 -2px 0 rgba(255,55,40,.72)}.request-field input.is-invalid,.country-button.is-invalid{border-color:#a94137!important;box-shadow:inset 0 -2px 0 #a94137!important}.field-hint,.field-error{font-size:7px;line-height:1.45;color:#6d746e}.field-error{color:#dc6c62;min-height:10px}
.phone-combo{display:grid;grid-template-columns:auto 1fr}.phone-prefix{min-width:122px;padding:0 13px;display:flex;align-items:center;gap:9px;border-right:0;cursor:pointer}.phone-prefix b{font-size:10px;letter-spacing:.07em}.phone-prefix>i,.country-button>i{margin-left:auto;font-style:normal;color:#767d77}.region-symbol{width:20px;height:20px;display:grid;place-items:center;font-size:17px;line-height:1}.region-symbol.is-empty{position:relative;border:1px solid #727a73;border-radius:50%}.region-symbol.is-empty:before,.region-symbol.is-empty:after{content:"";position:absolute;inset:4px 8px;border-left:1px solid #727a73;border-right:1px solid #727a73;border-radius:50%}.region-symbol.is-empty:after{inset:9px 3px;border:0;border-top:1px solid #727a73}.phone-combo input{border-left:1px solid #2b302c!important}.country-button{width:100%;padding:0 14px;display:flex;align-items:center;gap:11px;text-align:left;cursor:pointer}.country-button b{font-size:10px;letter-spacing:.075em}.field-error{display:block}
.request-controls{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:26px;padding-top:22px;border-top:1px solid #2b2f2c}.request-controls button{min-height:52px;padding:0 17px;border:1px solid #343935;background:#090a09;color:#d9ddd9;font-size:8px;letter-spacing:.11em;display:flex;align-items:center;gap:18px;cursor:pointer}.request-controls .request-next,.request-controls .request-submit{margin-left:auto;min-width:210px;justify-content:space-between;border-color:var(--accent);background:var(--accent);color:#fff}.request-controls button i{font-style:normal;font-size:14px}
.request-review{display:grid;gap:10px;margin-top:22px}.request-review article{padding:16px;border:1px solid #303531;background:#080908;display:grid;gap:7px}.request-review small{font-size:6.5px;letter-spacing:.16em;color:#707771}.request-review strong{font-size:13px;color:#eef0ec}.request-review span{font-size:8px;line-height:1.5;color:#858c86}.request-review-config{border-left:2px solid var(--accent)!important}
.request-complete[hidden],.request-progress[hidden]{display:none!important}.request-complete{min-height:620px;padding:44px 34px;display:grid;align-content:center;background:radial-gradient(circle at 12% 22%,rgba(64,221,126,.07),transparent 27%),linear-gradient(180deg,#090a09,#060706)}.request-lock-mark{display:flex;align-items:center;gap:12px;color:#8d948e;font-size:7px;letter-spacing:.17em}.request-lock-mark i{width:8px;height:8px;border-radius:50%;background:#4bdf85;box-shadow:0 0 15px rgba(75,223,133,.34)}.request-complete>small{margin-top:54px;color:#58df8c;font-size:8px;letter-spacing:.18em}.request-complete h3{margin:16px 0 22px;font-size:clamp(44px,5.6vw,72px);line-height:.88;letter-spacing:-.05em}.request-complete>p{max-width:620px;margin:0;color:#9ea49f;font-size:13px;line-height:1.55}.request-code{width:max-content;min-width:220px;margin-top:30px;padding:16px 18px;border:1px solid #353a36;display:grid;gap:7px}.request-code span{font-size:6.5px;letter-spacing:.17em;color:#747b75}.request-code b{font-size:18px;letter-spacing:.11em}.request-to-activation{margin-top:34px;min-height:60px;padding:0 20px;border:0;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:space-between;gap:28px;font-size:8px;letter-spacing:.12em;cursor:pointer}
.request-summary{position:sticky;top:calc(var(--header) + 18px);border:1px solid #343835;background:#080908;box-shadow:0 28px 80px rgba(0,0,0,.2)}.request-summary-kicker{height:42px;padding:0 15px;display:flex;align-items:center;gap:9px;border-bottom:1px solid #2a2e2b;color:#777e78;font-size:6.5px;letter-spacing:.17em}.request-summary-kicker span{width:6px;height:6px;border-radius:50%;background:#51df89}.request-bike{--request-accent:#ff3728;position:relative;aspect-ratio:1.45;overflow:hidden;border-bottom:1px solid #2b2f2c}.request-bike img{width:100%;height:100%;object-fit:cover;filter:brightness(.72) saturate(.9)}.request-bike:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 38%,rgba(3,3,3,.74)),radial-gradient(circle at 58% 64%,color-mix(in srgb,var(--request-accent) 16%,transparent),transparent 42%)}.request-bike[data-tone="green"]{--request-accent:#43df84}.request-bike[data-tone="green"] img{filter:hue-rotate(104deg) saturate(.76) brightness(.74)}.request-bike[data-tone="stealth"]{--request-accent:#aeb3b0}.request-bike[data-tone="stealth"] img{filter:grayscale(.9) brightness(.62)}.request-summary-head{display:grid;grid-template-columns:1fr auto;gap:18px;padding:18px;border-bottom:1px solid #2b2f2c}.request-summary-head>span{display:grid;gap:6px}.request-summary-head small,.request-summary-stats small{font-size:6.5px;letter-spacing:.16em;color:#737a74}.request-summary-head strong{font-family:"Inter Tight","Inter",sans-serif;font-size:25px;letter-spacing:-.035em}.request-summary-head span:last-child{text-align:right}.request-summary-stats{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid #2b2f2c}.request-summary-stats span{padding:14px 12px;border-right:1px solid #2b2f2c;display:grid;gap:6px}.request-summary-stats span:last-child{border-right:0}.request-summary-stats b{font-size:11px}.request-summary-modules{padding:14px 16px;border-bottom:1px solid #2b2f2c;display:grid;gap:9px}.request-summary-modules>small{font-size:6.5px;letter-spacing:.16em;color:#727973}.request-summary-modules>div{display:flex;flex-wrap:wrap;gap:6px}.request-summary-modules span{padding:5px 7px;border:1px solid #313632;color:#aeb4ae;font-size:6.5px;letter-spacing:.06em}.request-summary-code{padding:13px 16px;display:flex;justify-content:space-between;gap:14px;align-items:center}.request-summary-code span{font-size:6.5px;letter-spacing:.16em;color:#737a74}.request-summary-code b{font-size:9px;letter-spacing:.08em;text-align:right}
.region-picker{padding:0;border:0;background:transparent;color:#eee;max-width:none;max-height:none}.region-picker::backdrop{background:rgba(0,0,0,.78);backdrop-filter:blur(8px)}.region-picker-panel{width:min(480px,calc(100vw - 28px));max-height:min(78svh,700px);overflow:hidden;border:1px solid #383d39;background:#090a09;box-shadow:0 30px 100px rgba(0,0,0,.68)}.region-picker-panel header{height:72px;padding:0 18px;border-bottom:1px solid #2d312e;display:flex;justify-content:space-between;align-items:center}.region-picker-panel header>div{display:grid;gap:5px}.region-picker-panel header small{font-size:6.5px;letter-spacing:.17em;color:#6f766f}.region-picker-panel header strong{font-size:12px;letter-spacing:.08em}.region-picker-panel header button{width:42px;height:42px;border:1px solid #373c38;border-radius:50%;background:#0b0c0b;color:transparent;position:relative}.region-picker-panel header button:before,.region-picker-panel header button:after{content:"";position:absolute;left:50%;top:50%;width:15px;height:1px;background:#eee}.region-picker-panel header button:before{transform:translate(-50%,-50%) rotate(45deg)}.region-picker-panel header button:after{transform:translate(-50%,-50%) rotate(-45deg)}.region-search{height:56px;margin:14px;border:1px solid #323733;background:#070807;display:flex;align-items:center;gap:10px;padding:0 13px}.region-search>span{width:14px;height:14px;border:1px solid #727973;border-radius:50%;position:relative}.region-search>span:after{content:"";position:absolute;width:6px;height:1px;background:#727973;right:-4px;bottom:-2px;transform:rotate(45deg)}.region-search input{flex:1;background:transparent;border:0;outline:0;color:#eee;font:500 12px "Inter",sans-serif}.region-search input::placeholder{color:#555c56}.region-list{max-height:calc(min(78svh,700px) - 158px);overflow:auto;border-top:1px solid #292d2a}.region-option{width:100%;min-height:52px;padding:0 16px;border:0;border-bottom:1px solid #262a27;background:transparent;color:#eee;display:grid;grid-template-columns:34px 1fr auto;gap:10px;align-items:center;text-align:left;cursor:pointer}.region-option .flag{font-size:20px}.region-option strong{font-size:10px;font-weight:500}.region-option small{font-size:9px;color:#929992}.region-empty{padding:24px;color:#777e78;font-size:10px}

@media(hover:hover) and (pointer:fine){.config-presets button:hover,.config-finishes button:hover{background:rgba(255,255,255,.022);color:#fff}.config-module:hover{background:rgba(255,255,255,.018)}.config-preview-media:hover img{transform:scale(1.03)}.request-controls button:hover,.country-button:hover,.phone-prefix:hover{border-color:#596159}.region-option:hover{background:rgba(255,255,255,.025)}}

@media(max-width:980px){
  .tech-profile-v3{width:calc(100vw - 18px)!important;padding:20px!important}.tech-profile-head{gap:15px!important}.tech-profile-head .tech-sheet-titleblock h2{font-size:clamp(38px,10.5vw,52px)!important}.tech-profile-groups{gap:9px}.tech-profile-group{grid-template-columns:1fr!important}.tech-profile-group>header{padding:17px 16px!important;border-right:0!important;border-bottom:1px solid #292d2a;display:flex;align-items:center;gap:16px}.tech-profile-group>header>b{font-size:17px}.tech-profile-metrics{grid-template-columns:1fr 1fr}.tech-profile-metrics article{padding:18px 16px}.tech-profile-value strong{font-size:clamp(43px,12vw,58px)}.tech-profile-impact{border-left:0;border-top:1px solid #292d2a;padding:15px 16px}.tech-profile-impact p{margin-top:7px}.tech-conclusion{grid-template-columns:1fr;gap:12px;padding:17px}
  .configurator,.request{padding:78px var(--pad)}.config-head,.request-head{grid-template-columns:1fr;gap:18px;margin-bottom:30px}.config-head h2,.request-head h2{font-size:50px}.config-head p,.request-head p{max-width:40ch}.config-layout,.request-layout{grid-template-columns:1fr;gap:20px}.config-preview,.request-summary{position:static}.config-preview-media,.config-summary{margin-left:calc(-1*var(--pad));margin-right:calc(-1*var(--pad));border-left:0;border-right:0}.request-summary{order:-1}.request-bike{aspect-ratio:1.8}.config-panel{margin-top:4px}.config-module{grid-template-columns:30px minmax(0,1fr) auto}.config-effect{grid-column:2}.config-module-price{grid-column:3;grid-row:1}.config-module>i{grid-column:3;grid-row:2}.request-form{margin-top:0}
}
@media(max-width:520px){
  .tech-profile-v3{padding:16px!important}.tech-profile-head .tech-sheet-titleblock h2{font-size:40px!important}.tech-profile-head .tech-sheet-titleblock>p{font-size:10.5px!important;max-width:30ch!important}.tech-profile-head #techClose{width:46px!important;height:46px!important;flex-basis:46px}.tech-profile-metrics{grid-template-columns:1fr!important}.tech-profile-metrics article{border-right:0;border-bottom:1px solid #292d2a;padding:17px 15px}.tech-profile-metrics article:last-child{border-bottom:0}.tech-profile-value{margin-bottom:9px}.tech-profile-value strong{font-size:50px}.tech-profile-impact{padding:14px 15px}.tech-profile-group>header{padding:15px}.tech-conclusion strong{font-size:15px}.tech-conclusion p{font-size:9.5px}
  .configurator,.request{padding-left:20px;padding-right:20px}.config-head h2,.request-head h2{font-size:44px}.config-preview-media,.config-summary{margin-left:-20px;margin-right:-20px}.config-preview-media{aspect-ratio:1.15}.config-preview-id{left:16px;right:16px;bottom:14px}.config-preview-id strong{font-size:29px}.config-summary-top{padding:14px 16px}.config-price strong{font-size:23px!important}.config-character{padding:13px 16px}.config-compare-label{display:none}.config-stats{grid-template-columns:repeat(3,1fr)}.config-stats>span{padding:11px 9px}.config-stats>span:nth-child(3){border-right:0}.config-stats>span:nth-child(n+4){border-top:1px solid #282c29}.config-stats>span:nth-child(5){border-right:0}.config-active-build{grid-template-columns:1fr;gap:9px}.config-active-build>#configActiveModules{justify-content:flex-start}.config-presets{grid-template-columns:1fr}.config-presets button{min-height:94px;border-right:0;border-bottom:1px solid #292d2a;padding:15px 16px}.config-presets button p{max-width:34ch}.factory-setup{display:grid;gap:6px}.factory-setup strong{text-align:left}.config-module{grid-template-columns:26px minmax(0,1fr) auto;padding:14px 13px;gap:9px}.config-module-copy small{font-size:7.5px}.config-effect{font-size:7px;white-space:normal}.config-module-price{font-size:10px}.config-finishes{grid-template-columns:1fr}.config-finishes button{border-right:0;border-bottom:1px solid #292d2a;min-height:60px}.config-finishes button:last-child{border-bottom:0}.config-actions{grid-template-columns:1fr}.config-save{border-right:0!important;border-bottom:1px solid #2c302d!important}.config-actions button{min-height:58px}.config-note{font-size:7px}
  .request-head p{font-size:12px}.request-summary{margin-left:-20px;margin-right:-20px;border-left:0;border-right:0}.request-bike{aspect-ratio:1.72}.request-summary-head{padding:16px 18px}.request-summary-head strong{font-size:28px}.request-summary-stats span{padding:13px 11px}.request-form{margin-left:-20px;margin-right:-20px;border-left:0;border-right:0}.request-progress button{min-height:60px;padding:10px 9px;gap:7px}.request-progress b{display:none}.request-progress span{font-size:7px}.request-step{padding:22px 20px}.request-fields.two-col{grid-template-columns:1fr}.request-field.full{grid-column:auto}.request-field input,.phone-prefix,.country-button{height:56px}.phone-prefix{min-width:116px}.request-controls{align-items:stretch}.request-controls button{min-height:52px}.request-controls .request-next,.request-controls .request-submit{min-width:0;flex:1}.request-complete{min-height:610px;padding:36px 20px}.request-complete>small{margin-top:42px}.request-complete h3{font-size:44px}.request-code{min-width:190px}.region-picker-panel{width:calc(100vw - 18px)}
}
@media(prefers-reduced-motion:reduce){.config-preview-media img,.request-field input,.config-presets button:after,.request-progress button:after{transition:none!important}}
'''

# Replace old configurator/request JS tail with V3 logic.
js_marker = '/* VANTA R1 — Configurator V2 + Request Flow 2026-09 */'
if js_marker not in js:
    raise SystemExit('Configurator JS marker not found')
js = js[:js.index(js_marker)].rstrip() + '\n\n'

js += r'''/* VANTA R1 — Configurator V3 + Request V2 2026-09 */
(()=>{
  'use strict';
  const root=document.getElementById('configurator');
  if(!root)return;
  const base={power:210,torque:390,mass:189,range:320,charge:18,price:32900};
  const effects={
    performance:{power:18,torque:30,mass:3,range:-16,price:3900,label:'PERFORMANCE PACK',code:'PF'},
    aero:{mass:2,range:6,price:2600,label:'ACTIVE AERO',code:'AA'},
    carbon:{mass:-9,price:4800,label:'CARBON STRUCTURE',code:'CF'},
    range:{mass:12,range:52,charge:2,price:4200,label:'RANGE SYSTEM',code:'RG'},
    fast:{charge:-4,price:1900,label:'FAST CHARGE 800V',code:'FC'},
    telemetry:{price:1200,label:'RIDER TELEMETRY',code:'TL'}
  };
  const presets={
    road:{label:'ROAD',short:'RD',modules:['fast','telemetry'],tone:'red',factory:'FAST CHARGE 800V + RIDER TELEMETRY'},
    attack:{label:'ATTACK',short:'AT',modules:['performance','aero','carbon','telemetry'],tone:'red',factory:'PERFORMANCE + ACTIVE AERO + CARBON + TELEMETRY'},
    range:{label:'RANGE',short:'RG',modules:['range','fast','carbon','telemetry'],tone:'green',factory:'RANGE SYSTEM + FAST CHARGE + CARBON + TELEMETRY'}
  };
  const toneCodes={red:'SR',green:'VG',stealth:'ST'};
  let state={preset:'road',modules:new Set(presets.road.modules),tone:'red'};
  const q=id=>document.getElementById(id);
  const profileLabel=q('configProfileLabel'),moduleCount=q('configModuleCount'),code=q('configCode'),price=q('configPrice');
  const stats={power:q('cfgPower'),torque:q('cfgTorque'),mass:q('cfgMass'),range:q('cfgRange'),charge:q('cfgCharge')};
  const deltas={power:q('cfgPowerDelta'),torque:q('cfgTorqueDelta'),mass:q('cfgMassDelta'),range:q('cfgRangeDelta'),charge:q('cfgChargeDelta')};
  const preview=q('configPreview'),save=q('configSave'),request=q('configRequest'),activationBuild=q('activationBuild');
  const activeModules=q('configActiveModules'),characterNode=q('configCharacter'),factoryCopy=q('configFactoryCopy');
  const presetButtons=[...root.querySelectorAll('[data-preset]')],moduleButtons=[...root.querySelectorAll('[data-module]')],toneButtons=[...root.querySelectorAll('[data-config-tone]')];
  const money=n=>new Intl.NumberFormat('ru-RU',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(n).replace(/ /g,' ');
  const sameSet=(a,b)=>a.size===b.length&&b.every(x=>a.has(x));
  const detectPreset=()=>Object.entries(presets).find(([,p])=>sameSet(state.modules,p.modules)&&state.tone===p.tone)?.[0]||'custom';
  const calculate=()=>{const out={...base};state.modules.forEach(key=>{const e=effects[key]||{};['power','torque','mass','range','charge','price'].forEach(k=>{if(typeof e[k]==='number')out[k]+=e[k];});});return out;};
  const signed=(value,unit,{inverse=false}={})=>{if(!value)return 'BASE';const good=inverse?value<0:value>0;return {text:`${value>0?'+':'−'}${Math.abs(value)} ${unit}`,good};};
  const buildCharacter=(profile,modules)=>{
    const parts=[];
    if(profile==='ATTACK'||modules.includes('performance'))parts.push('агрессивный');
    else if(profile==='RANGE'||modules.includes('range'))parts.push('дальний');
    else parts.push('сбалансированный');
    if(modules.includes('carbon'))parts.push('облегчённый');
    if(modules.includes('fast'))parts.push('быстрая зарядка');
    if(modules.includes('aero'))parts.push('активная аэродинамика');
    if(modules.includes('telemetry'))parts.push('телеметрия');
    return parts.slice(0,3).join(' / ');
  };
  const snapshot=()=>{
    const values=calculate(),preset=detectPreset(),profile=preset==='custom'?'CUSTOM':presets[preset].label,modules=[...state.modules];
    const profileCode=preset==='custom'?'CU':presets[preset].short;
    const moduleCode=modules.map(k=>effects[k]?.code).filter(Boolean).join('-')||'BASE';
    return {profile,preset,modules,tone:state.tone,values,code:`R1-${profileCode}-${toneCodes[state.tone]}-${moduleCode}`,price:money(values.price),moduleLabels:modules.map(k=>effects[k]?.label||k),character:buildCharacter(profile,modules)};
  };
  const paintDelta=(node,value,unit,options)=>{if(!node)return;const d=signed(value,unit,options);node.textContent=typeof d==='string'?d:d.text;node.classList.remove('is-positive','is-negative');if(typeof d!=='string')node.classList.add(d.good?'is-positive':'is-negative');};
  const render=()=>{
    state.preset=detectPreset();const snap=snapshot(),v=snap.values,count=snap.modules.length;
    profileLabel.textContent=snap.profile;moduleCount.textContent=`${count} ${count===1?'МОДУЛЬ':count<5?'МОДУЛЯ':'МОДУЛЕЙ'}`;code.textContent=snap.code;price.textContent=snap.price;
    stats.power.textContent=`${v.power} кВт`;stats.torque.textContent=`${v.torque} Н·м`;stats.mass.textContent=`${v.mass} кг`;stats.range.textContent=`${v.range} км`;stats.charge.textContent=`${v.charge} мин`;
    paintDelta(deltas.power,v.power-base.power,'кВт');paintDelta(deltas.torque,v.torque-base.torque,'Н·м');paintDelta(deltas.mass,v.mass-base.mass,'кг',{inverse:true});paintDelta(deltas.range,v.range-base.range,'км');paintDelta(deltas.charge,v.charge-base.charge,'мин',{inverse:true});
    preview.dataset.tone=state.tone;if(characterNode)characterNode.textContent=snap.character;
    if(activeModules)activeModules.innerHTML=snap.moduleLabels.length?snap.moduleLabels.map(x=>`<span>${x}</span>`).join(''):'<span>BASE R1</span>';
    if(factoryCopy)factoryCopy.textContent=state.preset==='custom'?'CUSTOM BUILD — ручная конфигурация':presets[state.preset].factory;
    presetButtons.forEach(btn=>{const on=btn.dataset.preset===state.preset;btn.classList.toggle('active',on);btn.setAttribute('aria-pressed',String(on));});
    moduleButtons.forEach(btn=>{const on=state.modules.has(btn.dataset.module);btn.setAttribute('aria-pressed',String(on));const status=btn.querySelector(':scope > i');if(status)status.textContent=on?'УСТАНОВЛЕНО':'ДОБАВИТЬ';});
    toneButtons.forEach(btn=>{const on=btn.dataset.configTone===state.tone;btn.classList.toggle('active',on);btn.setAttribute('aria-pressed',String(on));});
    if(activationBuild)activationBuild.textContent=`YOUR R1 / ${snap.profile} / ${count} MODULES`;
    window.dispatchEvent(new CustomEvent('vanta:configchange',{detail:snap}));return snap;
  };
  const usePreset=key=>{const p=presets[key];if(!p)return;state={preset:key,modules:new Set(p.modules),tone:p.tone};render();};
  presetButtons.forEach(btn=>btn.addEventListener('click',()=>usePreset(btn.dataset.preset)));
  moduleButtons.forEach(btn=>btn.addEventListener('click',()=>{const key=btn.dataset.module;if(state.modules.has(key))state.modules.delete(key);else state.modules.add(key);render();}));
  toneButtons.forEach(btn=>btn.addEventListener('click',()=>{state.tone=btn.dataset.configTone;render();}));
  save?.addEventListener('click',()=>{try{localStorage.setItem('vanta-r1-config',JSON.stringify({modules:[...state.modules],tone:state.tone}));}catch{}const span=save.querySelector('span');if(span){const original='СОХРАНИТЬ CONFIG';span.textContent='CONFIG СОХРАНЁН';setTimeout(()=>span.textContent=original,1400);}});
  request?.addEventListener('click',()=>document.getElementById('request')?.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}));
  try{const saved=JSON.parse(localStorage.getItem('vanta-r1-config')||'null');if(saved&&Array.isArray(saved.modules)){state.modules=new Set(saved.modules.filter(k=>effects[k]));state.tone=['red','green','stealth'].includes(saved.tone)?saved.tone:'red';}}catch{}
  window.vantaConfig={getSnapshot:snapshot,setTone:t=>{if(['red','green','stealth'].includes(t)){state.tone=t;render();}},render};render();
})();

(()=>{
  'use strict';
  const section=document.getElementById('request'),form=document.getElementById('requestForm');if(!section||!form)return;
  const q=id=>document.getElementById(id);
  const countries=[['RU','Россия','+7'],['KZ','Казахстан','+7'],['BY','Беларусь','+375'],['DE','Германия','+49'],['FR','Франция','+33'],['IT','Италия','+39'],['ES','Испания','+34'],['PT','Португалия','+351'],['GB','Великобритания','+44'],['IE','Ирландия','+353'],['NL','Нидерланды','+31'],['BE','Бельгия','+32'],['LU','Люксембург','+352'],['CH','Швейцария','+41'],['AT','Австрия','+43'],['PL','Польша','+48'],['CZ','Чехия','+420'],['SK','Словакия','+421'],['HU','Венгрия','+36'],['RO','Румыния','+40'],['BG','Болгария','+359'],['GR','Греция','+30'],['CY','Кипр','+357'],['MT','Мальта','+356'],['HR','Хорватия','+385'],['SI','Словения','+386'],['RS','Сербия','+381'],['ME','Черногория','+382'],['BA','Босния и Герцеговина','+387'],['MK','Северная Македония','+389'],['AL','Албания','+355'],['EE','Эстония','+372'],['LV','Латвия','+371'],['LT','Литва','+370'],['FI','Финляндия','+358'],['SE','Швеция','+46'],['NO','Норвегия','+47'],['DK','Дания','+45'],['IS','Исландия','+354'],['MD','Молдова','+373'],['GE','Грузия','+995'],['AM','Армения','+374'],['AZ','Азербайджан','+994'],['UZ','Узбекистан','+998'],['TR','Турция','+90'],['IL','Израиль','+972'],['AE','ОАЭ','+971'],['SA','Саудовская Аравия','+966'],['QA','Катар','+974'],['IN','Индия','+91'],['CN','Китай','+86'],['JP','Япония','+81'],['KR','Южная Корея','+82'],['SG','Сингапур','+65'],['TH','Таиланд','+66'],['VN','Вьетнам','+84'],['ID','Индонезия','+62'],['MY','Малайзия','+60'],['AU','Австралия','+61'],['NZ','Новая Зеландия','+64'],['US','США','+1'],['CA','Канада','+1'],['MX','Мексика','+52'],['BR','Бразилия','+55'],['AR','Аргентина','+54'],['CL','Чили','+56'],['CO','Колумбия','+57'],['ZA','ЮАР','+27'],['EG','Египет','+20'],['MA','Марокко','+212']].map(([iso,name,dial])=>({iso,name,dial}));
  const flag=iso=>String.fromCodePoint(...iso.toUpperCase().split('').map(c=>127397+c.charCodeAt()));
  const countryButton=q('countryButton'),countryFlag=q('countryFlag'),countryName=q('countryName'),countryError=q('countryError'),phoneButton=q('phoneRegionButton'),phoneFlag=q('phoneFlag'),phoneDial=q('phoneDial'),phone=q('reqPhone'),phoneHint=q('phoneHint');
  const picker=q('regionPicker'),pickerTitle=q('regionPickerTitle'),pickerClose=q('regionPickerClose'),search=q('regionSearch'),list=q('regionList'),complete=q('requestComplete'),progress=form.querySelector('.request-progress');
  let pickerMode='country',deliveryCountry=null,phoneCountry=null,phoneManual=false,currentStep=1,currentConfig=window.vantaConfig?.getSnapshot?.()||null;
  const fields={first:q('reqFirst'),last:q('reqLast'),email:q('reqEmail'),region:q('reqRegion'),city:q('reqCity'),postal:q('reqPostal'),address:q('reqAddress'),address2:q('reqAddress2')};
  const steps=[...form.querySelectorAll('[data-request-step]')],nav=[...form.querySelectorAll('[data-request-nav]')];
  const moduleNames={performance:'Performance Pack',aero:'Active Aero',carbon:'Carbon Structure',range:'Range System',fast:'Fast Charge 800V',telemetry:'Rider Telemetry'};
  const formatNational=(raw,iso)=>{const d=raw.replace(/\D/g,'').slice(0,14);if(!d)return '';if(iso==='RU'||iso==='KZ')return [d.slice(0,3),d.slice(3,6),d.slice(6,8),d.slice(8,10)].filter(Boolean).join(d.length>6?'-':' ');if(iso==='US'||iso==='CA'){const a=d.slice(0,3),b=d.slice(3,6),c=d.slice(6,10);return `${a?`(${a}${a.length===3?') ':''}`:''}${b}${c?`-${c}`:''}`.trim()}return d.replace(/(\d{3})(?=\d)/g,'$1 ').trim();};
  phone?.addEventListener('input',()=>{phone.value=formatNational(phone.value,phoneCountry?.iso||'');try{phone.setSelectionRange(phone.value.length,phone.value.length)}catch{}});
  const renderPicker=(query='')=>{const needle=query.trim().toLocaleLowerCase('ru');const rows=countries.filter(c=>!needle||c.name.toLocaleLowerCase('ru').includes(needle)||c.dial.includes(needle)||c.iso.toLowerCase()===needle);list.innerHTML=rows.length?rows.map(c=>`<button class="region-option" type="button" role="option" data-iso="${c.iso}"><span class="flag">${flag(c.iso)}</span><strong>${c.name}</strong><small>${c.dial}</small></button>`).join(''):'<div class="region-empty">Ничего не найдено</div>';};
  const openPicker=mode=>{pickerMode=mode;pickerTitle.textContent=mode==='country'?'ВЫБЕРИ СТРАНУ':'КОД ТЕЛЕФОНА';search.value='';renderPicker();if(picker.showModal)picker.showModal();else picker.setAttribute('open','');setTimeout(()=>search.focus(),50);};
  const closePicker=()=>picker.close?.();countryButton?.addEventListener('click',()=>openPicker('country'));phoneButton?.addEventListener('click',()=>openPicker('phone'));pickerClose?.addEventListener('click',closePicker);search?.addEventListener('input',()=>renderPicker(search.value));
  const setFlag=(node,c)=>{node.classList.remove('is-empty');node.textContent=flag(c.iso);};
  picker?.addEventListener('click',e=>{if(e.target===picker){closePicker();return;}const btn=e.target.closest('.region-option');if(!btn)return;const c=countries.find(x=>x.iso===btn.dataset.iso);if(!c)return;if(pickerMode==='country'){deliveryCountry=c;setFlag(countryFlag,c);countryName.textContent=c.name.toUpperCase();countryButton.classList.remove('is-invalid');countryError.textContent='';if(!phoneManual){phoneCountry=c;setFlag(phoneFlag,c);phoneDial.textContent=c.dial;phoneHint.textContent=`${c.name} ${c.dial}`;phone.value=formatNational(phone.value,c.iso);}}else{phoneCountry=c;phoneManual=true;setFlag(phoneFlag,c);phoneDial.textContent=c.dial;phoneHint.textContent=`${c.name} ${c.dial}`;phone.value=formatNational(phone.value,c.iso);}closePicker();});
  const setStep=n=>{currentStep=n;if(complete)complete.hidden=true;if(progress)progress.hidden=false;steps.forEach(s=>{const on=Number(s.dataset.requestStep)===n;s.hidden=!on;s.classList.toggle('active',on);});nav.forEach(b=>{const x=Number(b.dataset.requestNav),on=x===n;b.classList.toggle('active',on);b.classList.toggle('complete',x<n);b.toggleAttribute('aria-current',on);});if(n===3)fillReview();};
  const validInput=input=>{if(!input)return true;const ok=input.checkValidity();input.classList.toggle('is-invalid',!ok);return ok;};
  const validateStep=n=>{if(n===1){const ok=[fields.first,fields.last,fields.email].every(validInput);const digits=phone.value.replace(/\D/g,'');const phoneOk=!!phoneCountry&&digits.length>=6;phone.classList.toggle('is-invalid',!phoneOk);if(!phoneCountry)phoneHint.textContent='Выбери страну или телефонный код.';else if(!phoneOk)phoneHint.textContent='Проверь номер: нужно минимум 6 цифр.';return ok&&phoneOk;}if(n===2){let ok=[fields.city,fields.postal,fields.address].every(validInput);if(!deliveryCountry){countryButton.classList.add('is-invalid');countryError.textContent='Выбери страну.';ok=false;}return ok;}return true;};
  form.querySelectorAll('[data-request-next]').forEach(btn=>btn.addEventListener('click',()=>{if(validateStep(currentStep))setStep(Number(btn.dataset.requestNext));}));form.querySelectorAll('[data-request-back]').forEach(btn=>btn.addEventListener('click',()=>setStep(Number(btn.dataset.requestBack))));nav.forEach(btn=>btn.addEventListener('click',()=>{const n=Number(btn.dataset.requestNav);if(n<currentStep)setStep(n);else if(n===currentStep+1&&validateStep(currentStep))setStep(n);}));form.querySelectorAll('input').forEach(input=>input.addEventListener('input',()=>input.classList.remove('is-invalid')));
  const fullPhone=()=>phoneCountry?`${phoneCountry.dial} ${phone.value}`.trim():phone.value;
  const fillReview=()=>{q('reviewName').textContent=`${fields.first.value} ${fields.last.value}`.trim()||'—';q('reviewContact').textContent=[fields.email.value,fullPhone()].filter(Boolean).join(' · ')||'—';q('reviewCountry').textContent=deliveryCountry?`${flag(deliveryCountry.iso)} ${deliveryCountry.name}`:'—';q('reviewAddress').textContent=[fields.postal.value,fields.region.value,fields.city.value,fields.address.value,fields.address2.value].filter(Boolean).join(', ')||'—';if(currentConfig){q('reviewConfig').textContent=currentConfig.code;q('reviewModules').textContent=currentConfig.moduleLabels.join(' · ')||'BASE R1';}};
  const paintConfig=snap=>{currentConfig=snap;if(!snap)return;q('requestProfile').textContent=snap.profile;q('requestPrice').textContent=snap.price;q('requestPower').textContent=`${snap.values.power} кВт`;q('requestMass').textContent=`${snap.values.mass} кг`;q('requestRange').textContent=`${snap.values.range} км`;q('requestConfigCode').textContent=snap.code;q('requestBike').dataset.tone=snap.tone;q('requestModules').innerHTML=snap.modules.length?snap.modules.map(k=>`<span>${moduleNames[k]||k}</span>`).join(''):'<span>BASE R1</span>';if(currentStep===3)fillReview();};
  addEventListener('vanta:configchange',e=>paintConfig(e.detail));paintConfig(currentConfig);
  if(complete)complete.hidden=true;if(progress)progress.hidden=false;
  form.addEventListener('submit',e=>{e.preventDefault();const step1ok=validateStep(1),step2ok=validateStep(2);if(!step1ok||!step2ok){setStep(!step1ok?1:2);return;}fillReview();steps.forEach(s=>s.hidden=true);if(progress)progress.hidden=true;if(complete)complete.hidden=false;const rnd=new Uint32Array(1);try{crypto.getRandomValues(rnd)}catch{rnd[0]=Math.floor(Math.random()*9999)}q('requestCode').textContent=`VR1-${currentConfig?.preset==='custom'?'CU':(currentConfig?.preset||'CU').slice(0,2).toUpperCase()}-${String(rnd[0]%10000).padStart(4,'0')}`;});
  q('requestToActivation')?.addEventListener('click',()=>{const tone=currentConfig?.tone||'red';document.querySelector(`.sw[data-color="${tone}"]`)?.click();document.getElementById('activate')?.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});});setStep(1);
})();
'''

(ROOT / 'index.html').write_text(index, encoding='utf-8')
(ROOT / 'v4.css').write_text(css, encoding='utf-8')
(ROOT / 'v4.js').write_text(js, encoding='utf-8')

print('Product Flow V3 patched')
