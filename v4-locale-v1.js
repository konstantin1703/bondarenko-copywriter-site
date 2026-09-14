/* VANTA R1 — RU/EN + localized location autocomplete 2026-09 */
(()=>{
  'use strict';

  const TEXT={
    'Характер':'Performance','Архитектура':'Architecture','Материалы':'Materials','Галерея':'Gallery','Система':'System','Конфигуратор':'Configurator','Заявка':'Request','Активация':'Activation',
    '02 / Характер':'02 / Performance','03 / Архитектура':'03 / Architecture','04 / Материалы':'04 / Materials','05 / Галерея':'05 / Gallery','06 / Система':'06 / System','07 / Конфигуратор':'07 / Configurator','08 / Заявка':'08 / Request','09 / Активация':'09 / Activation',
    'Тишина':'Silence','До первого':'Before the first','Импульса':'Impulse','VANTA R1 — электрический superbike, созданный вокруг мгновенной тяги, минимальной массы и абсолютного контроля.':'VANTA R1 is an electric superbike built around instant torque, minimal mass and absolute control.',
    'целевая мощность / кВт':'target power / kW','0—100 км/ч':'0—100 km/h','запас хода / км':'target range / km','целевая масса / кг':'target mass / kg',
    '02 / ХАРАКТЕР / PERFORMANCE':'02 / PERFORMANCE / CHARACTER','Мощность,':'Power,','которая не шумит.':'without the noise.','Полный момент приходит сразу. Без переключений, без задержки — только прямая связь между намерением и ускорением.':'Full torque arrives instantly. No shifts, no delay — only a direct connection between intent and acceleration.','пиковый момент':'peak torque','силовая архитектура':'power architecture',
    '03 / АРХИТЕКТУРА / FORM':'03 / ARCHITECTURE / FORM','Инженерия':'Engineering','без компромиссов.':'without compromise.','Каждая поверхность отвечает за функцию: охлаждение, поток воздуха, жёсткость и контроль массы.':'Every surface serves a function: cooling, airflow, rigidity and mass control.','карбоновый монокок':'carbon monocoque','направленный воздушный поток':'directed airflow','компактный электропривод':'compact electric drive',
    'Материалы,':'Materials,','которые имеют смысл.':'with a purpose.','Кованый карбон, матовый графит и световая линия работают как единая поверхность — без декоративного шума.':'Forged carbon, matte graphite and the light signature work as one surface — without decorative noise.','LIGHT SIGNATURE / ОПТИКА':'LIGHT SIGNATURE / OPTICS','BRAKE + FORK / ШАССИ':'BRAKE + FORK / CHASSIS','TAIL SIGNATURE / КОРМА':'TAIL SIGNATURE / REAR',
    'Форма следует за силой.':'Form follows force.','05 / ГАЛЕРЕЯ / ХАРАКТЕР':'05 / GALLERY / CHARACTER','Один R1.':'One R1.','Шесть граней характера.':'Six sides of character.','01 / МГНОВЕННЫЙ ОТКЛИК':'01 / INSTANT RESPONSE','Тяга приходит без паузы.':'Torque arrives without delay.','02 / ЧИСТАЯ АЭРОДИНАМИКА':'02 / CLEAN AERODYNAMICS','Форма направляет поток.':'Form directs the airflow.','03 / СВЕТОВОЙ СЛЕД':'03 / LIGHT TRACE','Задняя графика узнаётся мгновенно.':'The rear signature is instantly recognizable.','04 / КАРБОН БЕЗ ДЕКОРА':'04 / CARBON WITHOUT DECOR','Материал работает на форму.':'The material serves the form.','05 / ТОЧКА КОНТРОЛЯ':'05 / CONTROL POINT','Информация только по делу.':'Only essential information.','06 / СВЕТ КАК ПОДПИСЬ':'06 / LIGHT AS A SIGNATURE','Узкая LED-графика R1.':'A slim R1 LED signature.',
    '06 / RIDE SYSTEM / БОРТОВАЯ СИСТЕМА':'06 / RIDE SYSTEM / COCKPIT','Полный контроль.':'Total control.','Всегда под рукой.':'Always within reach.','Цифровая приборка R1 показывает только то, что нужно в движении: скорость, заряд, запас хода, рекуперацию и активный режим. Переключи режим — телеметрия изменится.':'The R1 display shows only what matters in motion: speed, charge, range, regeneration and the active ride mode. Switch modes and the telemetry responds.','СКОРОСТЬ':'SPEED','км/ч':'km/h','МОЩНОСТЬ':'POWER','АКТИВНЫЙ РЕЖИМ':'ACTIVE MODE','ДОРОГА':'ROAD','ТРЕК':'ATTACK','ЭКО':'RANGE','Сбалансированный отклик':'Balanced response','Максимальная отдача привода':'Maximum drive output','Приоритет запаса хода':'Range priority','ЗАРЯД':'CHARGE','ЗАПАС ХОДА':'RANGE','РЕКУПЕРАЦИЯ':'REGEN','СРЕДНЯЯ':'MEDIUM','НИЗКАЯ':'LOW','ВЫСОКАЯ':'HIGH',
    'Собери свой':'Build your','Начни с заводского характера, добавь инженерные пакеты и сразу увидишь, как каждый выбор меняет динамику, массу, дальность и итоговую стоимость.':'Start with a factory character, add engineering packages and see immediately how each choice changes performance, mass, range and final price.','СТОИМОСТЬ':'PRICE','ХАРАКТЕР СБОРКИ':'BUILD CHARACTER','Сбалансированный / дорожный / быстрая зарядка':'balanced / road / fast charge','МОМЕНТ':'TORQUE','МАССА':'MASS','ЗАПАС':'RANGE','ТЕЛЕМЕТРИЯ':'TELEMETRY','БАЗОВАЯ КОНФИГУРАЦИЯ':'BASE CONFIGURATION','УСТАНОВЛЕННЫЕ МОДУЛИ':'INSTALLED MODULES','ВЕРНУТЬ FACTORY SETUP':'RESTORE FACTORY SETUP','СБРОСИТЬ СБОРКУ':'RESET BUILD','ХАРАКТЕР':'CHARACTER','Баланс отклика, зарядки и повседневной дальности.':'Balanced response, charging and everyday range.','Максимальная отдача, меньше массы, жёстче характер.':'Maximum output, lower mass, sharper character.','Приоритет дальности, эффективности и энергетического цикла.':'Priority on range, efficiency and the energy cycle.','ИНЖЕНЕРНЫЕ ПАКЕТЫ':'ENGINEERING PACKAGES','Усиленная силовая электроника, охлаждение и более резкий профиль отдачи.':'Upgraded power electronics, cooling and a sharper output profile.','Активная аэродинамика для стабильности и снижения сопротивления на скорости.':'Active aerodynamics for stability and reduced drag at speed.','Кованый карбон и облегчённые узлы для снижения массы.':'Forged carbon and lightweight components reduce overall mass.','Увеличенный энергетический пакет для дальних маршрутов.':'Expanded energy pack for longer routes.','Расширенный термоконтроль и ускоренный зарядный профиль.':'Extended thermal control and an accelerated charging profile.','Данные поездки, состояние систем и расширенная аналитика сессии.':'Ride data, system status and extended session analytics.','ДОБАВИТЬ':'ADD','УСТАНОВЛЕНО':'INSTALLED','СВЕТОВАЯ ПОДПИСЬ':'LIGHT SIGNATURE','агрессивный акцент':'aggressive accent','энергетический акцент':'energy accent','минимальная световая графика':'minimal light graphic','СОХРАНИТЬ СБОРКУ':'SAVE BUILD','СБОРКА СОХРАНЕНА':'BUILD SAVED','ПЕРЕЙТИ К ЗАЯВКЕ':'CONTINUE TO REQUEST','BASE R1 — чистая конфигурация':'BASE R1 — clean configuration','CUSTOM BUILD — ручная конфигурация':'CUSTOM BUILD — manual configuration',
    'КОНТАКТЫ':'CONTACTS','ДОСТАВКА':'DELIVERY','ПРОВЕРКА':'REVIEW','КОНТАКТНЫЕ ДАННЫЕ':'CONTACT DETAILS','Данные владельца конфигурации':'Configuration owner details','ИМЯ':'FIRST NAME','ФАМИЛИЯ':'LAST NAME','ТЕЛЕФОН':'PHONE','Код':'Code','Номер телефона':'Phone number','Выбери страну или телефонный код.':'Choose a country or calling code.','ПРОДОЛЖИТЬ':'CONTINUE','АДРЕС':'ADDRESS','Адрес доставки R1':'R1 delivery address','СТРАНА':'COUNTRY','ВЫБЕРИ СТРАНУ':'SELECT COUNTRY','РЕГИОН / ОБЛАСТЬ / ШТАТ':'REGION / STATE / PROVINCE','Начни вводить — подсказки будут только по выбранной стране.':'Start typing — suggestions are limited to the selected country.','ГОРОД':'CITY','Города других стран не показываются.':'Cities from other countries are never shown.','ИНДЕКС':'POSTAL CODE','ДОПОЛНИТЕЛЬНО':'ADDITIONAL','Квартира / офис / комментарий':'Apartment / office / note','← НАЗАД':'← BACK','ПРОВЕРИТЬ':'REVIEW','ПРОВЕРКА ЗАЯВКИ':'REQUEST REVIEW','Проверь данные перед подтверждением':'Check the details before confirmation','КОНТАКТ':'CONTACT','КОНФИГУРАЦИЯ':'CONFIGURATION','ПОДТВЕРДИТЬ ЗАЯВКУ':'CONFIRM REQUEST','ЗАЯВКА':'REQUEST','СФОРМИРОВАНА.':'CONFIRMED.','Конфигурация R1 закреплена за заявкой. Система готова перейти к активации выбранного профиля.':'Your R1 configuration has been locked to the request. The system is ready to activate the selected profile.','АКТИВИРОВАТЬ СВОЙ R1':'ACTIVATE YOUR R1','Начни вводить регион':'Start typing a region','Начни вводить город':'Start typing a city','Улица, дом':'Street, building','Страна или код +7':'Country or code +49','Ничего не найдено':'No results found','КОД ТЕЛЕФОНА':'PHONE CODE',
    'Готов к первому':'Ready for the first','импульсу?':'impulse?','Запусти R1: оптика проснётся, световая система активируется, а выбранный характер сцены перейдёт в рабочий режим.':'Start R1: the optics wake up, the light system activates and the selected visual character enters its live state.','Фирменная красная световая подпись.':'Signature red light graphic.','АКТИВИРОВАТЬ R1':'ACTIVATE R1','Система ожидает запуска.':'System ready for activation.','Холодный электрический зелёный акцент.':'Cold electric green accent.','Минимальная световая графика.':'Minimal light graphic.',
    'ИНЖЕНЕРНЫЙ':'ENGINEERING','ПРОФИЛЬ R1':'PROFILE R1','Шесть параметров, которые формируют отклик, тягу, энергетический цикл, массу и практическую дальность R1.':'Six parameters define R1 response, torque, energy cycle, mass and practical range.','ПРИВОД':'DRIVE','Пиковая мощность':'Peak power','Максимальная целевая отдача электрического привода.':'Maximum target output of the electric drive.','Крутящий момент':'Torque','Тяга доступна практически сразу после открытия газа.':'Torque is available almost immediately after throttle input.','ВЛИЯНИЕ НА R1':'IMPACT ON R1','Мгновенный отклик и высокий темп разгона без паузы на переключения.':'Instant response and rapid acceleration without shift interruptions.','ЭНЕРГОСИСТЕМА':'ENERGY SYSTEM','Высоковольтная архитектура':'High-voltage architecture','Основа для высокой мощности и эффективной быстрой зарядки.':'The foundation for high output and efficient fast charging.','Зарядка 10→80%':'Charging 10→80%','Целевой энергетический цикл на совместимой DC-станции.':'Target charge cycle on a compatible DC station.','Высокую скорость восстановления заряда и устойчивую отдачу силовой системы.':'Fast energy recovery and consistent power-system output.','ХОДОВОЙ ПРОФИЛЬ':'VEHICLE PROFILE','Целевая масса':'Target mass','Расчётная масса базовой инженерной конфигурации R1.':'Calculated mass of the base R1 engineering configuration.','Запас хода':'Range','Расчётная дальность базовой конфигурации на одном заряде.':'Calculated range of the base configuration on one charge.','Баланс между управляемостью, плотностью компоновки и практической дальностью.':'A balance of handling, packaging density and practical range.','ИНЖЕНЕРНЫЙ ИТОГ':'ENGINEERING SUMMARY','Характер R1 складывается не из одной большой цифры.':'R1 character is not defined by a single headline number.','формируют отклик и тягу.':'define response and torque.','определяют энергетический темп.':'set the energy-cycle pace.','задают баланс динамики, массы и реальной дальности.':'balance dynamics, mass and real-world range.',
    'VANTA R1 — авторский электрический superbike-концепт. Все изображения мотоцикла созданы специально для этого проекта.':'VANTA R1 is an original electric superbike concept. All motorcycle imagery was created specifically for this project.'
  };
  const ATTR={
    'VANTA — наверх':'VANTA — back to top','Основная навигация':'Main navigation','Открыть меню':'Open menu','Мобильная навигация':'Mobile navigation','Ключевые характеристики концепта':'Key concept specifications','Предыдущий кадр':'Previous frame','Следующий кадр':'Next frame','Галерея VANTA R1':'VANTA R1 gallery','Интерактивная приборная панель VANTA R1':'Interactive VANTA R1 instrument panel','Режим движения':'Ride mode','Профиль R1':'R1 profile','Световая подпись конфигуратора':'Configurator light signature','Цветовой режим':'Light color mode','Красная подсветка':'Red lighting','Зелёная подсветка':'Green lighting','Закрыть инженерный профиль':'Close engineering profile','Закрыть выбор страны':'Close country picker'
  };
  const reverse=Object.fromEntries(Object.entries(TEXT).map(([ru,en])=>[en,ru]));
  const reverseAttr=Object.fromEntries(Object.entries(ATTR).map(([ru,en])=>[en,ru]));
  let activeLang='ru';
  let applying=false;

  const preserveSpace=(raw,next)=>{const a=raw.match(/^\s*/)?.[0]||'',b=raw.match(/\s*$/)?.[0]||'';return a+next+b;};
  const dynamic=(value,lang)=>{
    let s=value;
    if(lang==='en'){
      s=s.replace(/(\d+)\s+МОДУЛ(?:Ь|Я|ЕЙ)/g,(_,n)=>`${n} MODULE${n==='1'?'':'S'}`)
        .replace(/(\d+(?:[.,]\d+)?)\s*кВт/g,'$1 kW').replace(/(\d+(?:[.,]\d+)?)\s*Н·м/g,'$1 N·m').replace(/(\d+(?:[.,]\d+)?)\s*кг/g,'$1 kg').replace(/(\d+(?:[.,]\d+)?)\s*км/g,'$1 km').replace(/(\d+(?:[.,]\d+)?)\s*мин(?:ут[аы]?)?/g,'$1 min');
    }else{
      s=s.replace(/(\d+)\s+MODULES?/g,(_,n)=>`${n} ${Number(n)%10===1&&Number(n)%100!==11?'МОДУЛЬ':([2,3,4].includes(Number(n)%10)&&![12,13,14].includes(Number(n)%100)?'МОДУЛЯ':'МОДУЛЕЙ')}`)
        .replace(/(\d+(?:[.,]\d+)?)\s*kW/g,'$1 кВт').replace(/(\d+(?:[.,]\d+)?)\s*N·m/g,'$1 Н·м').replace(/(\d+(?:[.,]\d+)?)\s*kg/g,'$1 кг').replace(/(\d+(?:[.,]\d+)?)\s*km(?!\/h)/g,'$1 км').replace(/(\d+(?:[.,]\d+)?)\s*min/g,'$1 мин');
    }
    return s;
  };
  const translateNode=node=>{
    if(node.nodeType!==Node.TEXT_NODE)return;
    const raw=node.nodeValue||'',key=raw.trim();if(!key)return;
    const dict=activeLang==='en'?TEXT:reverse;
    let next=dict[key]||key;
    next=dynamic(next,activeLang);
    if(next!==key)node.nodeValue=preserveSpace(raw,next);
  };
  const translateAttrs=root=>{
    const dict=activeLang==='en'?ATTR:reverseAttr;
    root.querySelectorAll?.('[aria-label],[placeholder],[title]').forEach(el=>{
      ['aria-label','placeholder','title'].forEach(attr=>{const v=el.getAttribute(attr);if(!v)return;const mapped=dict[v]||TEXT[v]||reverse[v];if(mapped)el.setAttribute(attr,mapped);});
    });
  };
  const translateTree=root=>{
    if(applying)return;applying=true;
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:n=>/^(SCRIPT|STYLE|NOSCRIPT)$/.test(n.parentElement?.tagName||'')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
    let node;while((node=walker.nextNode()))translateNode(node);
    translateAttrs(root.nodeType===Node.DOCUMENT_NODE?document:root);
    applying=false;
  };

  const displayName=iso=>{try{return new Intl.DisplayNames([activeLang],{type:'region'}).of(iso)||iso}catch{return iso}};
  const localizeCountryRows=()=>{
    document.querySelectorAll('.region-option[data-iso]').forEach(btn=>{const strong=btn.querySelector('strong');if(strong)strong.textContent=displayName(btn.dataset.iso).toLocaleUpperCase(activeLang);});
    const country=document.getElementById('countryButton'),name=document.getElementById('countryName');if(country?.dataset.iso&&name)name.textContent=displayName(country.dataset.iso).toLocaleUpperCase(activeLang);
  };
  const setMeta=()=>{
    document.title='VANTA R1 — Electric Superbike Concept';
    const d=document.querySelector('meta[name="description"]');if(d)d.content=activeLang==='en'?'VANTA R1 — an original electric superbike concept and interactive digital product experience.':'VANTA R1 — авторский концепт электрического superbike и интерактивная digital-презентация.';
  };
  const updateSwitches=()=>document.querySelectorAll('.lang-switch button').forEach(b=>{const on=b.dataset.lang===activeLang;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));});
  const setLanguage=(lang,{persist=true,url=true}={})=>{
    activeLang=lang==='en'?'en':'ru';document.documentElement.lang=activeLang;
    if(persist)try{localStorage.setItem('vanta-lang',activeLang)}catch{}
    if(url){const u=new URL(location.href);u.searchParams.set('lang',activeLang);history.replaceState(null,'',u);}
    translateTree(document);localizeCountryRows();setMeta();updateSwitches();
    window.dispatchEvent(new CustomEvent('vanta:languagechange',{detail:{lang:activeLang}}));
  };
  const makeSwitch=cls=>{const wrap=document.createElement('div');wrap.className=`lang-switch ${cls}`;wrap.setAttribute('aria-label','Language / Язык');wrap.innerHTML='<button type="button" data-lang="ru" aria-pressed="true">RU</button><button type="button" data-lang="en" aria-pressed="false">EN</button>';wrap.addEventListener('click',e=>{const b=e.target.closest('button[data-lang]');if(b)setLanguage(b.dataset.lang);});return wrap;};
  document.getElementById('header')?.appendChild(makeSwitch('header-lang'));
  document.getElementById('mobileMenu')?.appendChild(makeSwitch('mobile-lang'));

  const params=new URLSearchParams(location.search);let initial=params.get('lang');if(!['ru','en'].includes(initial)){try{initial=localStorage.getItem('vanta-lang')}catch{}}if(!['ru','en'].includes(initial))initial='ru';
  setLanguage(initial,{persist:false,url:false});
  window.vantaLocale={get:()=>activeLang,set:setLanguage};

  const observer=new MutationObserver(muts=>{if(applying)return;let touched=false;for(const m of muts){if(m.type==='characterData'){translateNode(m.target);touched=true;}else m.addedNodes.forEach(n=>{if(n.nodeType===1||n.nodeType===3){translateTree(n.nodeType===1?n:n.parentNode);touched=true;}});}if(touched)localizeCountryRows();});
  observer.observe(document.body,{subtree:true,childList:true,characterData:true});

  /* Replace legacy autocomplete nodes to remove pointerdown selection listeners. */
  const cloneClean=id=>{const old=document.getElementById(id);if(!old)return null;const fresh=old.cloneNode(true);old.replaceWith(fresh);return fresh;};
  const countryButton=document.getElementById('countryButton');
  let regionInput=document.getElementById('reqRegion'),cityInput=document.getElementById('reqCity'),regionBox=cloneClean('regionSuggest'),cityBox=cloneClean('citySuggest');
  if(!countryButton||!regionInput||!cityInput||!regionBox||!cityBox)return;

  const cache={regions:null,cities:new Map()};let countryIso=countryButton.dataset.iso||'',selectedRegionCode='',cityToken=0;
  const norm=v=>String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase(activeLang).trim();
  const esc=v=>String(v??'').replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const locName=obj=>activeLang==='en'?(obj.en||obj.ru):(obj.ru||obj.en);
  const open=(input,box)=>{box.hidden=false;input.setAttribute('aria-expanded','true')};const close=(input,box)=>{box.hidden=true;input.setAttribute('aria-expanded','false')};
  const info=(input,box,ru,en)=>{box.innerHTML=`<div class="location-suggest-empty">${esc(activeLang==='en'?en:ru)}</div>`;open(input,box)};
  const loadRegions=async()=>{if(cache.regions)return cache.regions;let r=await fetch('data/regions-i18n.json',{cache:'force-cache'});if(!r.ok)throw new Error('regions');cache.regions=await r.json();return cache.regions};
  const loadCities=async iso=>{if(cache.cities.has(iso))return cache.cities.get(iso);const r=await fetch(`data/locations-i18n/${encodeURIComponent(iso)}.json`,{cache:'force-cache'});if(!r.ok)throw new Error('cities');const rows=await r.json();cache.cities.set(iso,rows);return rows};
  const rank=(name,q)=>{const a=norm(name),b=norm(q);if(!b)return 2;if(a.startsWith(b))return 0;if(a.includes(b))return 1;return 99};
  const manual=q=>q?`<button type="button" class="use-manual" data-value="${esc(q)}"><strong>${activeLang==='en'?'Use':'Использовать'} «${esc(q)}»</strong><small>${activeLang==='en'?'MANUAL ENTRY':'РУЧНОЙ ВВОД'}</small></button>`:'';
  const regionsForCountry=async()=>{const all=await loadRegions();return all[countryIso]||[]};
  const renderRegions=async()=>{
    if(!countryIso){info(regionInput,regionBox,'Сначала выбери страну.','Select a country first.');return}
    const q=regionInput.value.trim();info(regionInput,regionBox,'Загружаю регионы…','Loading regions…');
    try{const pool=await regionsForCountry();const rows=pool.map(x=>({x,score:Math.min(rank(x.ru,q),rank(x.en,q))})).filter(x=>x.score<99).sort((a,b)=>a.score-b.score||locName(a.x).localeCompare(locName(b.x),activeLang)).slice(0,16);regionBox.innerHTML=rows.map(({x})=>`<button type="button" data-value="${esc(locName(x))}" data-code="${esc(x.code)}"><strong>${esc(locName(x))}</strong><small>${esc(displayName(countryIso))}</small></button>`).join('')+manual(q);if(!regionBox.innerHTML)info(regionInput,regionBox,'Совпадений нет — можно оставить введённое значение.','No matches — you can keep the entered value.');else open(regionInput,regionBox)}catch{info(regionInput,regionBox,'Справочник недоступен — введи регион вручную.','Region database unavailable — enter it manually.')}};
  const renderCities=async()=>{
    if(!countryIso){info(cityInput,cityBox,'Сначала выбери страну.','Select a country first.');return}
    const q=cityInput.value.trim();if(!q){info(cityInput,cityBox,'Начни вводить название города.','Start typing a city name.');return}
    const token=++cityToken;info(cityInput,cityBox,'Ищу города…','Searching cities…');
    try{const rows=await loadCities(countryIso);if(token!==cityToken)return;const matches=rows.map(x=>({x,score:Math.min(rank(x.ru,q),rank(x.en,q),...(x.a_ru||[]).map(a=>rank(a,q)),...(x.a_en||[]).map(a=>rank(a,q)))})).filter(({x,score})=>score<99&&(!selectedRegionCode||x.r===selectedRegionCode)).sort((a,b)=>a.score-b.score||(b.x.p||0)-(a.x.p||0)||locName(a.x).localeCompare(locName(b.x),activeLang)).slice(0,18);const regions=await regionsForCountry();const rmap=new Map(regions.map(x=>[x.code,locName(x)]));cityBox.innerHTML=matches.map(({x})=>`<button type="button" data-value="${esc(locName(x))}" data-region-code="${esc(x.r||'')}"><strong>${esc(locName(x))}</strong><small>${esc(rmap.get(x.r)||displayName(countryIso))}</small></button>`).join('')+manual(q);if(!cityBox.innerHTML)info(cityInput,cityBox,'В выбранной стране совпадений нет — можно оставить введённое значение.','No matches in the selected country — you can keep the entered value.');else open(cityInput,cityBox)}catch{info(cityInput,cityBox,'Справочник недоступен — введи город вручную.','City database unavailable — enter it manually.')}};

  const pickRegion=async btn=>{regionInput.value=btn.dataset.value||'';selectedRegionCode=btn.classList.contains('use-manual')?'':(btn.dataset.code||'');regionInput.dataset.regionCode=selectedRegionCode;cityInput.value='';cityInput.dataset.cityId='';close(regionInput,regionBox);close(cityInput,cityBox);regionInput.dispatchEvent(new Event('change',{bubbles:true}))};
  const pickCity=async btn=>{cityInput.value=btn.dataset.value||'';const code=btn.dataset.regionCode||'';if(code&&!selectedRegionCode){selectedRegionCode=code;regionInput.dataset.regionCode=code;try{const regions=await regionsForCountry();const item=regions.find(x=>x.code===code);if(item)regionInput.value=locName(item)}catch{}}close(cityInput,cityBox);cityInput.dispatchEvent(new Event('change',{bubbles:true}))};
  const touchSafe=(box,pick)=>{let startY=0,moved=false,blockUntil=0;box.addEventListener('touchstart',e=>{startY=e.touches[0]?.clientY||0;moved=false},{passive:true});box.addEventListener('touchmove',e=>{if(Math.abs((e.touches[0]?.clientY||startY)-startY)>7)moved=true},{passive:true});box.addEventListener('touchend',()=>{if(moved)blockUntil=Date.now()+350},{passive:true});box.addEventListener('click',e=>{const btn=e.target.closest('button[data-value]');if(!btn)return;if(Date.now()<blockUntil){e.preventDefault();return}pick(btn)});};
  touchSafe(regionBox,pickRegion);touchSafe(cityBox,pickCity);
  let rt=0,ct=0;regionInput.addEventListener('focus',renderRegions);regionInput.addEventListener('input',()=>{selectedRegionCode='';regionInput.dataset.regionCode='';clearTimeout(rt);rt=setTimeout(renderRegions,45)});cityInput.addEventListener('focus',renderCities);cityInput.addEventListener('input',()=>{clearTimeout(ct);ct=setTimeout(renderCities,45)});
  window.addEventListener('vanta:countrychange',e=>{countryIso=e.detail?.iso||countryButton.dataset.iso||'';selectedRegionCode='';cityToken+=1;regionInput.value='';cityInput.value='';regionInput.dataset.regionCode='';close(regionInput,regionBox);close(cityInput,cityBox);if(countryIso){loadRegions().catch(()=>{});loadCities(countryIso).catch(()=>{})}});
  window.addEventListener('vanta:languagechange',async()=>{try{if(selectedRegionCode){const regions=await regionsForCountry();const item=regions.find(x=>x.code===selectedRegionCode);if(item)regionInput.value=locName(item)}}catch{}if(!regionBox.hidden)renderRegions();if(!cityBox.hidden)renderCities();localizeCountryRows()});
  document.addEventListener('pointerdown',e=>{if(!e.target.closest('.smart-location-field')){close(regionInput,regionBox);close(cityInput,cityBox)}});
})();
