from pathlib import Path
import re

ROOT=Path('.')

def sub_once(text, pattern, repl, name, flags=re.S):
    out,n=re.subn(pattern,repl,text,count=1,flags=flags)
    if n!=1:
        raise SystemExit(f'{name}: expected one match, got {n}')
    return out

# ---------------- v4.js: localize dynamic systems directly, remove legacy location runtime ----------------
p=ROOT/'v4.js'
s=p.read_text(encoding='utf-8')

ride_states="""  const rideLang=()=>document.documentElement.lang==='en'?'en':'ru';
  const rideCopy={
    ru:{km:'км',regen:{medium:'СРЕДНЯЯ',low:'НИЗКАЯ',high:'ВЫСОКАЯ'},modes:{road:{name:'ДОРОГА',desc:'Сбалансированный отклик'},attack:{name:'ТРЕК',desc:'Максимальная отдача привода'},range:{name:'ЭКО',desc:'Приоритет запаса хода'}},meter:(r,p)=>`Рекуперация ${r} процентов, мощность ${p} процентов`},
    en:{km:'km',regen:{medium:'MEDIUM',low:'LOW',high:'HIGH'},modes:{road:{name:'ROAD',desc:'Balanced response'},attack:{name:'ATTACK',desc:'Maximum drive output'},range:{name:'RANGE',desc:'Range priority'}},meter:(r,p)=>`Regeneration ${r} percent, power ${p} percent`}
  };
  const states={
    road:{speed:84,battery:'78%',range:214,regen:'medium',regenValue:48,power:62,dial:142},
    attack:{speed:146,battery:'61%',range:128,regen:'low',regenValue:18,power:94,dial:232},
    range:{speed:62,battery:'84%',range:286,regen:'high',regenValue:88,power:42,dial:106}
  };

  const svgNS="""
s=sub_once(s,r"  const states=\{.*?\n  \};\n\n  const svgNS=",ride_states,'ride states')

old_apply="""  const applyMode=(key,{animate=true}={})=>{
    const s=states[key];
    if(!dash||!s)return;
    dash.dataset.mode=key;
    if(animate)calibrate();
    animateSpeed(s.speed);
    if(battery)battery.textContent=s.battery;
    if(range)range.textContent=s.range;
    if(regen)regen.textContent=s.regen;
    if(powerLabel)powerLabel.textContent=`${s.power}%`;
    if(modeName)modeName.textContent=s.name;
    if(modeDesc)modeDesc.textContent=s.desc;
    setSvgArc(speedArc,s.speed/2);
    setSvgArc(powerArcSvg,s.power);
    dash.style.setProperty('--dial',`${s.dial}deg`);
    dash.style.setProperty('--power-angle',`${s.power*2.7}deg`);
    dash.style.setProperty('--power-half',`${s.power*.5}%`);
    dash.style.setProperty('--regen-half',`${s.regenValue*.5}%`);
    powerMeter?.setAttribute('aria-label',`Рекуперация ${s.regenValue} процентов, мощность ${s.power} процентов`);
  };"""
new_apply="""  const applyMode=(key,{animate=true}={})=>{
    const s=states[key];
    if(!dash||!s)return;
    const copy=rideCopy[rideLang()];
    const mode=copy.modes[key];
    dash.dataset.mode=key;
    if(animate)calibrate();
    animateSpeed(s.speed);
    if(battery)battery.textContent=s.battery;
    if(range)range.textContent=`${s.range} ${copy.km}`;
    if(regen)regen.textContent=copy.regen[s.regen];
    if(powerLabel)powerLabel.textContent=`${s.power}%`;
    if(modeName)modeName.textContent=mode.name;
    if(modeDesc)modeDesc.textContent=mode.desc;
    setSvgArc(speedArc,s.speed/2);
    setSvgArc(powerArcSvg,s.power);
    dash.style.setProperty('--dial',`${s.dial}deg`);
    dash.style.setProperty('--power-angle',`${s.power*2.7}deg`);
    dash.style.setProperty('--power-half',`${s.power*.5}%`);
    dash.style.setProperty('--regen-half',`${s.regenValue*.5}%`);
    powerMeter?.setAttribute('aria-label',copy.meter(s.regenValue,s.power));
  };"""
if old_apply not in s: raise SystemExit('ride applyMode anchor not found')
s=s.replace(old_apply,new_apply,1)
s=s.replace("  applyMode('road',{animate:false});\n\n  const clock=document.getElementById('clock');\n  const tick=()=>{if(clock)clock.textContent=new Date().toLocaleTimeString('ru-RU',{hour:'2-digit',minute:'2-digit'});};",
"  applyMode('road',{animate:false});\n  window.addEventListener('vanta:languagechange',()=>applyMode(dash?.dataset.mode||'road',{animate:false}));\n\n  const clock=document.getElementById('clock');\n  const tick=()=>{if(clock)clock.textContent=new Date().toLocaleTimeString(rideLang()==='en'?'en-GB':'ru-RU',{hour:'2-digit',minute:'2-digit'});};",1)

activation_block="""  const activationLang=()=>document.documentElement.lang==='en'?'en':'ru';
  const activationCopy={
    ru:{activate:'АКТИВИРОВАТЬ R1',deactivate:'ОТКЛЮЧИТЬ R1',starting:'ЗАПУСК...',standby:'Система ожидает запуска.',checking:'Проверка бортовой системы.',ready:'Система готова к активации.',active:name=>`${name}: оптика и бортовая система активированы.`,updated:name=>`${name}: световой характер обновлён.`,selected:'Выбран световой характер. Система ожидает запуска.',desc:{red:'Фирменная красная световая подпись.',green:'Холодный электрический зелёный акцент.',stealth:'Монохромный режим без лишнего блеска.'}},
    en:{activate:'ACTIVATE R1',deactivate:'DEACTIVATE R1',starting:'STARTING...',standby:'System ready for activation.',checking:'Running onboard system check.',ready:'System ready to activate.',active:name=>`${name}: optics and onboard systems are active.`,updated:name=>`${name}: light signature updated.`,selected:'Light signature selected. System ready for activation.',desc:{red:'Signature red light graphic.',green:'Cold electric green accent.',stealth:'Monochrome mode with no unnecessary glare.'}}
  };
  const finishes={red:{name:'SIGNAL RED'},green:{name:'VOLT GREEN'},stealth:{name:'STEALTH BLACK'}};
  let currentFinish='red';
  let activationOn=false;
  let activationBusy=false;
  let bootTimers=[];
  const activationText=()=>activationCopy[activationLang()];
  const clearBootTimers=()=>{bootTimers.forEach(clearTimeout);bootTimers=[];};
  const paintActivationCopy=()=>{
    const copy=activationText(),finish=finishes[currentFinish]||finishes.red;
    if(activateLabel)activateLabel.textContent=activationBusy?copy.starting:(activationOn?copy.deactivate:copy.activate);
    if(finishDesc)finishDesc.textContent=copy.desc[currentFinish]||copy.desc.red;
    if(note)note.textContent=activationOn?copy.active(finish.name):copy.standby;
  };
  const setActivationUi=on=>{
    activationOn=on;
    stage?.classList.toggle('stage-live',on);
    stage?.classList.remove('stage-booting','stage-ready');
    stage?.setAttribute('aria-busy','false');
    activateBtn?.setAttribute('aria-busy','false');
    activateBtn?.setAttribute('aria-pressed',String(on));
    if(status)status.textContent=on?'SYSTEM ACTIVE':'STANDBY';
    activationBusy=false;
    paintActivationCopy();
  };
  const bootActivation=()=>{
    if(!stage||!activateBtn||activationBusy)return;
    if(activationOn){clearBootTimers();setActivationUi(false);return;}
    if(reduceMotion){setActivationUi(true);return;}
    activationBusy=true;
    const copy=activationText();
    stage.classList.remove('stage-live','stage-ready');
    stage.classList.add('stage-booting');
    stage.setAttribute('aria-busy','true');
    activateBtn.setAttribute('aria-busy','true');
    if(status)status.textContent='SYSTEM CHECK';
    if(activateLabel)activateLabel.textContent=copy.starting;
    if(note)note.textContent=copy.checking;
    bootTimers=[
      setTimeout(()=>{
        stage.classList.add('stage-ready');
        if(status)status.textContent='READY';
        if(note)note.textContent=activationText().ready;
      },330),
      setTimeout(()=>setActivationUi(true),820)
    ];
  };
  activateBtn?.addEventListener('click',bootActivation);
  const applyFinish=(key,{announce=true}={})=>{
    const finish=finishes[key]||finishes.red;currentFinish=finishes[key]?key:'red';
    document.querySelectorAll('.sw').forEach(x=>{const active=x.dataset.color===currentFinish;x.classList.toggle('active',active);x.setAttribute('aria-pressed',String(active));});
    stage?.classList.remove('color-green','color-stealth','color-shifting');
    if(currentFinish==='green')stage?.classList.add('color-green');
    if(currentFinish==='stealth')stage?.classList.add('color-stealth');
    if(stage&&!reduceMotion){void stage.offsetWidth;stage.classList.add('color-shifting');setTimeout(()=>stage.classList.remove('color-shifting'),420);}
    if(finishName)finishName.textContent=finish.name;
    if(finishDesc)finishDesc.textContent=activationText().desc[currentFinish];
    if(announce&&note)note.textContent=activationOn?activationText().updated(finish.name):activationText().selected;
  };
  document.querySelectorAll('.sw').forEach(sw=>sw.addEventListener('click',()=>applyFinish(sw.dataset.color)));
  applyFinish('red',{announce:false});
  window.addEventListener('vanta:languagechange',paintActivationCopy);
"""
s=sub_once(s,r"  const finishes=\{.*?  applyFinish\('red',\{announce:false\}\);\n",activation_block,'activation block')

# Work only in Configurator + Request section for safer replacements.
marker='/* VANTA R1 — Configurator V3 + Request V2 2026-09 */'
if marker not in s: raise SystemExit('config marker missing')
head,tail=s.split(marker,1)
segment=marker+tail

segment=segment.replace("  const toneCodes={red:'SR',green:'VG',stealth:'ST'};",
"""  const toneCodes={red:'SR',green:'VG',stealth:'ST'};
  const configLang=()=>document.documentElement.lang==='en'?'en':'ru';
  const configCopy={
    ru:{units:{power:'кВт',torque:'Н·м',mass:'кг',range:'км',charge:'мин'},add:'ДОБАВИТЬ',installed:'УСТАНОВЛЕНО',notInstalled:'НЕ УСТАНОВЛЕНО',saved:'СБОРКА СОХРАНЕНА',save:'СОХРАНИТЬ СБОРКУ',baseFactory:'BASE R1 — чистая конфигурация',customFactory:'CUSTOM BUILD — ручная конфигурация',your:'ВАШ R1',character:{balanced:'сбалансированный',aggressive:'агрессивный',long:'дальний',light:'облегчённый',fast:'быстрая зарядка',aero:'активная аэродинамика',telemetry:'телеметрия'}},
    en:{units:{power:'kW',torque:'N·m',mass:'kg',range:'km',charge:'min'},add:'ADD',installed:'INSTALLED',notInstalled:'NOT INSTALLED',saved:'BUILD SAVED',save:'SAVE BUILD',baseFactory:'BASE R1 — clean configuration',customFactory:'CUSTOM BUILD — manual configuration',your:'YOUR R1',character:{balanced:'balanced',aggressive:'aggressive',long:'long-range',light:'lightweight',fast:'fast charging',aero:'active aero',telemetry:'telemetry'}}
  };
  const moduleCountLabel=(count,lang=configLang())=>lang==='en'?`${count} MODULE${count===1?'':'S'}`:`${count} ${count%10===1&&count%100!==11?'МОДУЛЬ':([2,3,4].includes(count%10)&&![12,13,14].includes(count%100)?'МОДУЛЯ':'МОДУЛЕЙ')}`;""",1)

segment=segment.replace("  const money=n=>new Intl.NumberFormat('ru-RU',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(n).replace(/ /g,' ');",
"  const money=n=>new Intl.NumberFormat(configLang()==='en'?'en-IE':'ru-RU',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(n).replace(/ /g,' ');",1)

segment=sub_once(segment,r"  const buildCharacter=\(profile,modules\)=>\{.*?\n  \};\n  const snapshot=", """  const buildCharacter=(profile,modules)=>{
    const c=configCopy[configLang()].character;
    const parts=[];
    if(profile==='ATTACK'||modules.includes('performance'))parts.push(c.aggressive);
    else if(profile==='RANGE'||modules.includes('range'))parts.push(c.long);
    else parts.push(c.balanced);
    if(modules.includes('carbon'))parts.push(c.light);
    if(modules.includes('fast'))parts.push(c.fast);
    if(modules.includes('aero'))parts.push(c.aero);
    if(modules.includes('telemetry'))parts.push(c.telemetry);
    return parts.slice(0,3).join(' / ');
  };
  const snapshot=""",'config character')

new_render="""  const render=()=>{
    const lang=configLang(),copy=configCopy[lang],u=copy.units;
    state.preset=detectPreset();const snap=snapshot(),v=snap.values,count=snap.modules.length;
    profileLabel.textContent=snap.profile;moduleCount.textContent=moduleCountLabel(count,lang);code.textContent=snap.code;price.textContent=snap.price;
    stats.power.textContent=`${v.power} ${u.power}`;stats.torque.textContent=`${v.torque} ${u.torque}`;stats.mass.textContent=`${v.mass} ${u.mass}`;stats.range.textContent=`${v.range} ${u.range}`;stats.charge.textContent=`${v.charge} ${u.charge}`;if(stats.telemetry)stats.telemetry.textContent=state.modules.has('telemetry')?'LIVE':'OFF';if(deltas.telemetry)deltas.telemetry.textContent=state.modules.has('telemetry')?'R1 LINK':copy.notInstalled;stats.telemetry?.parentElement?.classList.toggle('is-off',!state.modules.has('telemetry'));
    paintDelta(deltas.power,v.power-base.power,u.power);paintDelta(deltas.torque,v.torque-base.torque,u.torque);paintDelta(deltas.mass,v.mass-base.mass,u.mass,{inverse:true});paintDelta(deltas.range,v.range-base.range,u.range);paintDelta(deltas.charge,v.charge-base.charge,u.charge,{inverse:true});
    preview.dataset.tone=state.tone;if(characterNode)characterNode.textContent=snap.character;
    if(activeModules)activeModules.innerHTML=snap.moduleLabels.length?snap.moduleLabels.map(x=>`<span>${x}</span>`).join(''):'<span>BASE R1</span>';
    if(factoryCopy)factoryCopy.textContent=state.preset==='base'?copy.baseFactory:state.preset==='custom'?copy.customFactory:presets[state.preset].factory;if(factoryResetBtn){factoryResetBtn.hidden=state.preset!=='custom';factoryResetBtn.disabled=state.preset!=='custom';}if(resetBuildBtn){resetBuildBtn.hidden=state.modules.size===0;resetBuildBtn.disabled=state.modules.size===0;}
    presetButtons.forEach(btn=>{const on=btn.dataset.preset===state.preset;btn.classList.toggle('active',on);btn.setAttribute('aria-pressed',String(on));});
    moduleButtons.forEach(btn=>{const on=state.modules.has(btn.dataset.module);btn.setAttribute('aria-pressed',String(on));const status=btn.querySelector(':scope > i');if(status)status.textContent=on?copy.installed:copy.add;});
    toneButtons.forEach(btn=>{const on=btn.dataset.configTone===state.tone;btn.classList.toggle('active',on);btn.setAttribute('aria-pressed',String(on));});
    if(activationBuild)activationBuild.textContent=`${copy.your} / ${snap.profile} / ${moduleCountLabel(count,lang)}`;
    window.dispatchEvent(new CustomEvent('vanta:configchange',{detail:snap}));return snap;
  };"""
segment=sub_once(segment,r"  const render=\(\)=>\{.*?window\.dispatchEvent\(new CustomEvent\('vanta:configchange',\{detail:snap\}\)\);return snap;\n  \};",new_render,'config render')

segment=sub_once(segment,r"  save\?\.addEventListener\('click',\(\)=>\{.*?\}\);\n  request\?\.addEventListener\('click',\(\)=>document\.getElementById\('request'\)\?\.scrollIntoView\(.*?\)\);",
"""  save?.addEventListener('click',()=>{try{localStorage.setItem('vanta-r1-config',JSON.stringify({modules:[...state.modules],tone:state.tone}));}catch{}const span=save.querySelector('span');if(span){span.textContent=configCopy[configLang()].saved;setTimeout(()=>span.textContent=configCopy[configLang()].save,1400);}});""",'config save legacy request')

segment=segment.replace("  window.vantaConfig={getSnapshot:snapshot,setTone:t=>{if(['red','green','stealth'].includes(t)){state.tone=t;render();}},setPreset:usePreset,reset:resetBuild,restoreFactory,render};render();",
"  window.addEventListener('vanta:languagechange',render);\n  window.vantaConfig={getSnapshot:snapshot,setTone:t=>{if(['red','green','stealth'].includes(t)){state.tone=t;render();}},setPreset:usePreset,reset:resetBuild,restoreFactory,render};render();",1)

# Fix one malformed phone code while touching the country source.
segment=segment.replace('"dial":"+290 n"','"dial":"+290"')

segment=segment.replace("  const moduleNames={performance:'Performance Pack',aero:'Active Aero',carbon:'Carbon Structure',range:'Range System',fast:'Fast Charge 800V',telemetry:'Rider Telemetry'};",
"""  const moduleNames={performance:'Performance Pack',aero:'Active Aero',carbon:'Carbon Structure',range:'Range System',fast:'Fast Charge 800V',telemetry:'Rider Telemetry'};
  const requestLang=()=>document.documentElement.lang==='en'?'en':'ru';
  const requestCopy={ru:{chooseCountry:'ВЫБЕРИ СТРАНУ',phoneCode:'КОД ТЕЛЕФОНА',none:'Ничего не найдено',choosePhone:'Выбери страну или телефонный код.',badPhone:'Проверь номер: нужно минимум 6 цифр.',chooseDelivery:'Выбери страну.',units:{power:'кВт',mass:'кг',range:'км'}},en:{chooseCountry:'SELECT COUNTRY',phoneCode:'PHONE CODE',none:'No results found',choosePhone:'Choose a country or calling code.',badPhone:'Check the number: enter at least 6 digits.',chooseDelivery:'Select a country.',units:{power:'kW',mass:'kg',range:'km'}}};
  const countryLabel=c=>{if(!c)return '';if(requestLang()==='ru')return c.name;try{return new Intl.DisplayNames(['en'],{type:'region'}).of(c.iso)||c.name}catch{return c.name}};""",1)

segment=sub_once(segment,r"  const renderPicker=\(query=''\)=>\{.*?\};\n  const openPicker=mode=>\{.*?\};",
"""  const renderPicker=(query='')=>{const lang=requestLang(),copy=requestCopy[lang],needle=query.trim().toLocaleLowerCase(lang);const rows=countries.filter(c=>{const label=countryLabel(c);return !needle||c.name.toLocaleLowerCase('ru').includes(needle)||label.toLocaleLowerCase(lang).includes(needle)||c.dial.includes(needle)||c.iso.toLowerCase()===needle;});list.innerHTML=rows.length?rows.map(c=>`<button class=\"region-option\" type=\"button\" role=\"option\" data-iso=\"${c.iso}\"><span class=\"flag\">${flag(c.iso)}</span><strong>${countryLabel(c)}</strong><small>${c.dial}</small></button>`).join(''):`<div class=\"region-empty\">${copy.none}</div>`;};
  const openPicker=mode=>{pickerMode=mode;pickerTitle.textContent=mode==='country'?requestCopy[requestLang()].chooseCountry:requestCopy[requestLang()].phoneCode;search.value='';renderPicker();if(picker.showModal)picker.showModal();else picker.setAttribute('open','');setTimeout(()=>search.focus(),50);};""",'request picker')

old_picker="""  picker?.addEventListener('click',e=>{if(e.target===picker){closePicker();return;}const btn=e.target.closest('.region-option');if(!btn)return;const c=countries.find(x=>x.iso===btn.dataset.iso);if(!c)return;if(pickerMode==='country'){deliveryCountry=c;countryButton.dataset.iso=c.iso;window.dispatchEvent(new CustomEvent('vanta:countrychange',{detail:c}));setFlag(countryFlag,c);countryName.textContent=c.name.toUpperCase();countryButton.classList.remove('is-invalid');countryError.textContent='';if(!phoneManual){phoneCountry=c;setFlag(phoneFlag,c);phoneDial.textContent=c.dial;phoneHint.textContent=`${c.name} ${c.dial}`;phone.value=formatNational(phone.value,c.iso);}}else{phoneCountry=c;phoneManual=true;setFlag(phoneFlag,c);phoneDial.textContent=c.dial;phoneHint.textContent=`${c.name} ${c.dial}`;phone.value=formatNational(phone.value,c.iso);}closePicker();});"""
new_picker="""  picker?.addEventListener('click',e=>{if(e.target===picker){closePicker();return;}const btn=e.target.closest('.region-option');if(!btn)return;const c=countries.find(x=>x.iso===btn.dataset.iso);if(!c)return;const label=countryLabel(c);if(pickerMode==='country'){deliveryCountry=c;countryButton.dataset.iso=c.iso;window.dispatchEvent(new CustomEvent('vanta:countrychange',{detail:c}));setFlag(countryFlag,c);countryName.textContent=label.toLocaleUpperCase(requestLang());countryButton.classList.remove('is-invalid');countryError.textContent='';if(!phoneManual){phoneCountry=c;setFlag(phoneFlag,c);phoneDial.textContent=c.dial;phoneHint.textContent=`${label} ${c.dial}`;phone.value=formatNational(phone.value,c.iso);}}else{phoneCountry=c;phoneManual=true;setFlag(phoneFlag,c);phoneDial.textContent=c.dial;phoneHint.textContent=`${label} ${c.dial}`;phone.value=formatNational(phone.value,c.iso);}closePicker();});"""
if old_picker not in segment: raise SystemExit('request picker click anchor missing')
segment=segment.replace(old_picker,new_picker,1)

segment=sub_once(segment,r"  const validateStep=n=>\{.*?return true;\};",
"""  const validateStep=n=>{const copy=requestCopy[requestLang()];if(n===1){const ok=[fields.first,fields.last,fields.email].every(validInput);const digits=phone.value.replace(/\D/g,'');const phoneOk=!!phoneCountry&&digits.length>=6;phone.classList.toggle('is-invalid',!phoneOk);if(!phoneCountry)phoneHint.textContent=copy.choosePhone;else if(!phoneOk)phoneHint.textContent=copy.badPhone;return ok&&phoneOk;}if(n===2){let ok=[fields.city,fields.postal,fields.address].every(validInput);if(!deliveryCountry){countryButton.classList.add('is-invalid');countryError.textContent=copy.chooseDelivery;ok=false;}return ok;}return true;};""",'request validation')

segment=sub_once(segment,r"  const fillReview=\(\)=>\{.*?\};\n  const paintConfig=snap=>\{.*?\};",
"""  const fillReview=()=>{q('reviewName').textContent=`${fields.first.value} ${fields.last.value}`.trim()||'—';q('reviewContact').textContent=[fields.email.value,fullPhone()].filter(Boolean).join(' · ')||'—';q('reviewCountry').textContent=deliveryCountry?`${flag(deliveryCountry.iso)} ${countryLabel(deliveryCountry)}`:'—';q('reviewAddress').textContent=[fields.postal.value,fields.region.value,fields.city.value,fields.address.value,fields.address2.value].filter(Boolean).join(', ')||'—';if(currentConfig){q('reviewConfig').textContent=currentConfig.code;q('reviewModules').textContent=currentConfig.moduleLabels.join(' · ')||'BASE R1';}};
  const paintConfig=snap=>{currentConfig=snap;if(!snap)return;const u=requestCopy[requestLang()].units;q('requestProfile').textContent=snap.profile;q('requestPrice').textContent=snap.price;q('requestPower').textContent=`${snap.values.power} ${u.power}`;q('requestMass').textContent=`${snap.values.mass} ${u.mass}`;q('requestRange').textContent=`${snap.values.range} ${u.range}`;q('requestConfigCode').textContent=snap.code;q('requestBike').dataset.tone=snap.tone;q('requestModules').innerHTML=snap.modules.length?snap.modules.map(k=>`<span>${moduleNames[k]||k}</span>`).join(''):'<span>BASE R1</span>';if(currentStep===3)fillReview();};""",'request review/config')

segment=segment.replace("  addEventListener('vanta:configchange',e=>paintConfig(e.detail));paintConfig(currentConfig);",
"""  addEventListener('vanta:configchange',e=>paintConfig(e.detail));
  addEventListener('vanta:languagechange',()=>{const lang=requestLang();if(deliveryCountry)countryName.textContent=countryLabel(deliveryCountry).toLocaleUpperCase(lang);if(phoneCountry)phoneHint.textContent=`${countryLabel(phoneCountry)} ${phoneCountry.dial}`;if(picker?.open){pickerTitle.textContent=pickerMode==='country'?requestCopy[lang].chooseCountry:requestCopy[lang].phoneCode;renderPicker(search?.value||'');}paintConfig(currentConfig);if(currentStep===3)fillReview();});
  paintConfig(currentConfig);""",1)

# Remove the superseded Location Search V5 module entirely.
legacy='\n\n/* VANTA R1 — Location Search V5 / country-strict autocomplete 2026-09 */'
if legacy not in segment: raise SystemExit('legacy location block marker missing')
segment=segment.split(legacy,1)[0].rstrip()+"\n"
s=head+segment
p.write_text(s,encoding='utf-8')

# ---------------- locale runtime: static translations + safe tree traversal + alt localization ----------------
p=ROOT/'v4-locale-v1.js'
s=p.read_text(encoding='utf-8')
extra_text="""  Object.assign(TEXT,{
    'Зафиксируй':'Lock in','свой R1.':'your R1.','Контактные данные и адрес — последний шаг перед фиксацией выбранной конфигурации R1.':'Contact details and delivery address are the final step before locking in your R1 configuration.',
    'кВт':'kW','Н·м':'N·m','В':'V','мин':'min','кг':'kg','км':'km',
    '210 кВт и 390 Н·м':'210 kW and 390 N·m','800 В и 18 минут':'800 V and 18 min','189 кг и 320 км':'189 kg and 320 km',
    'Монохромный режим без лишнего блеска.':'Monochrome mode with no unnecessary glare.',
    'ВАШ R1':'YOUR R1','КОД СБОРКИ':'BUILD CODE','АКТИВНАЯ СБОРКА':'ACTIVE BUILD','ЗАВОДСКОЙ ПРОФИЛЬ':'FACTORY PROFILE','ЗАВОДСКАЯ СБОРКА':'FACTORY SETUP','ВЕРНУТЬ ЗАВОДСКУЮ СБОРКУ':'RESTORE FACTORY SETUP','ИНЖЕНЕРНЫЕ ОПЦИИ':'ENGINEERING OPTIONS','КОНФИГУРАЦИЯ / СВЕТОВАЯ ПОДПИСЬ':'CONFIG / LIGHT SIGNATURE','10—80% / целевое':'10—80% / target'
  });
"""
anchor="  };\n  const ATTR={"
if anchor not in s: raise SystemExit('locale TEXT/ATTR anchor missing')
s=s.replace(anchor,"  };\n"+extra_text+"  const ATTR={",1)

extra_attr="""  Object.assign(ATTR,{
    'VANTA R1 — фронтальный ракурс три четверти':'VANTA R1 — front three-quarter view','VANTA R1 в динамической световой сцене':'VANTA R1 in a dynamic lighting scene','VANTA R1 в архитектурной студии':'VANTA R1 in the architecture studio',
    'Подсветить CARBON MONOCOQUE':'Highlight CARBON MONOCOQUE','Подсветить ACTIVE AERO':'Highlight ACTIVE AERO','Подсветить AXIAL DRIVE':'Highlight AXIAL DRIVE',
    'Макро-деталь карбонового корпуса VANTA R1':'Macro detail of the VANTA R1 carbon body','Фара VANTA R1':'VANTA R1 headlight','Переднее колесо и тормоз VANTA R1':'VANTA R1 front wheel and brake','Задняя оптика VANTA R1':'VANTA R1 rear light','Световая подпись и карбоновая поверхность VANTA R1':'VANTA R1 light signature and carbon surface',
    'VANTA R1 — фронт три четверти':'VANTA R1 — front three-quarter view','VANTA R1 — боковой профиль':'VANTA R1 — side profile','VANTA R1 — задний ракурс':'VANTA R1 — rear view','VANTA R1 — студийный портрет':'VANTA R1 — studio portrait','Кокпит VANTA R1':'VANTA R1 cockpit','Оптика VANTA R1':'VANTA R1 lighting','Кокпит VANTA R1 с цифровой приборной панелью':'VANTA R1 cockpit with digital instrument display',
    'VANTA R1 — конфигуратор':'VANTA R1 — configurator','Этапы заявки':'Request steps','VANTA R1 — выбранная конфигурация':'VANTA R1 — selected configuration','VANTA R1 — финальный активационный ракурс':'VANTA R1 — final activation view','Полноэкранная галерея VANTA R1':'Fullscreen VANTA R1 gallery','Закрыть галерею':'Close gallery'
  });
"""
anchor="  };\n  const reverse=Object.fromEntries(Object.entries(TEXT)"
if anchor not in s: raise SystemExit('locale ATTR/reverse anchor missing')
s=s.replace(anchor,"  };\n"+extra_attr+"  const reverse=Object.fromEntries(Object.entries(TEXT)",1)

s=sub_once(s,r"  const translateAttrs=root=>\{.*?\n  \};\n  const translateTree=root=>\{.*?\n  \};",
"""  const translateAttrs=root=>{
    const dict=activeLang==='en'?ATTR:reverseAttr;
    const scope=root?.nodeType===Node.DOCUMENT_NODE?document:root;
    scope?.querySelectorAll?.('[aria-label],[placeholder],[title],[alt]').forEach(el=>{
      ['aria-label','placeholder','title','alt'].forEach(attr=>{const v=el.getAttribute(attr);if(!v)return;const mapped=activeLang==='en'?(dict[v]||TEXT[v]):(dict[v]||reverse[v]);if(mapped)el.setAttribute(attr,mapped);});
    });
  };
  const translateTree=root=>{
    if(applying||!root||typeof root.nodeType!=='number')return;
    applying=true;
    try{
      const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:n=>/^(SCRIPT|STYLE|NOSCRIPT)$/.test(n.parentElement?.tagName||'')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
      let node;while((node=walker.nextNode()))translateNode(node);
      translateAttrs(root);
    }finally{applying=false;}
  };""",'safe locale traversal')

s=s.replace("  const updateSwitches=()=>document.querySelectorAll('.lang-switch button').forEach(b=>{const on=b.dataset.lang===activeLang;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));});",
"  const updateSwitches=()=>{document.querySelectorAll('.lang-switch').forEach(w=>w.setAttribute('aria-label',activeLang==='en'?'Language':'Язык'));document.querySelectorAll('.lang-switch button').forEach(b=>{const on=b.dataset.lang===activeLang;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));});};",1)

# Remove MutationObserver translation; dynamic systems now render their locale directly.
s=sub_once(s,r"\n  const observer=new MutationObserver\(.*?observer\.observe\(document\.body,\{subtree:true,childList:true,characterData:true\}\);\n","\n",'locale mutation observer')
p.write_text(s,encoding='utf-8')

# ---------------- locale CSS: consolidate language control + tech close; typography QA ----------------
p=ROOT/'v4-locale-v1.css'
s=p.read_text(encoding='utf-8')
lang_css=""":root{--lang-pill-bg:#0a0a0a;--lang-pill-line:#3a3d3a}
.lang-switch{display:inline-flex;align-items:center;border:1px solid var(--lang-pill-line);background:rgba(7,8,7,.86);border-radius:999px;height:44px;padding:2px;gap:0;box-shadow:inset 0 0 0 1px rgba(255,255,255,.015);overflow:hidden;z-index:112;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
.lang-switch button{appearance:none;position:relative;min-width:40px;height:40px;padding:0 8px;border:0;border-radius:999px;background:transparent;color:#737a74;font:600 8.5px/1 Inter,sans-serif;letter-spacing:.1em;cursor:pointer;transition:color .2s,background .2s,box-shadow .2s;touch-action:manipulation}
.lang-switch button.active{background:#eeefeb;color:#090a09;box-shadow:0 1px 8px rgba(255,255,255,.08)}
.lang-switch button[data-lang="ru"]:after{content:"";position:absolute;left:11px;right:11px;bottom:5px;height:1px;background:linear-gradient(90deg,#fff 0 33%,#486dcc 33% 66%,#dd4038 66%);opacity:.55}.lang-switch button[data-lang="en"]:after{content:"";position:absolute;left:11px;right:11px;bottom:5px;height:1px;background:linear-gradient(90deg,#476cab 0 45%,#eee 45% 55%,#d74a42 55%);opacity:.45}
.header-lang{position:absolute;right:calc(var(--pad) + 112px);top:50%;transform:translateY(-50%)}.mobile-lang{display:none}
@media(max-width:980px){#header.header{grid-template-columns:1fr auto auto;column-gap:5px}.header-lang{display:inline-flex;position:static;right:auto;top:auto;transform:none;grid-column:2;grid-row:1;justify-self:end;margin-right:1px}.header .menu{grid-column:3;grid-row:1;margin:0}.mobile-lang{display:none}}
"""
s=sub_once(s,r":root\{--lang-pill-bg:.*?@media\(max-width:980px\)\{.*?\}\n",lang_css,'locale language css')

# Use one centered cross implementation in this file.
s=sub_once(s,r"\.tech-floating-close:after\{.*?\.tech-floating-close>span:after\{.*?\}\n",
""".tech-floating-close>span{display:none!important}.tech-floating-close::before,.tech-floating-close::after{content:""!important;display:block!important;position:absolute!important;left:50%!important;top:50%!important;width:20px!important;height:1.6px!important;margin:0!important;background:#f4f4f0!important;border:0!important;border-radius:99px!important;transform-origin:50% 50%!important;opacity:1!important}.tech-floating-close::before{transform:translate(-50%,-50%) rotate(45deg)!important}.tech-floating-close::after{transform:translate(-50%,-50%) rotate(-45deg)!important}
""",'tech cross consolidation')

typography_css="""
/* Full typography QA: micro labels stay technical but remain readable on mobile. */
.hero-mark small,.performance-media figcaption,.material-hero figcaption span,.detail-triptych figcaption,#dash small,#configurator .config-preview-id small,#configurator .config-summary small,#configurator .config-step-head small,#configurator .factory-setup small,#activate .activation-config small{font-size:8px!important;line-height:1.35}
html[lang="ru"] #dash small,html[lang="ru"] #configurator small,html[lang="ru"] #activate small{letter-spacing:.1em}
@media(max-width:600px){html[lang="en"] .hero-title{font-size:clamp(42px,11vw,54px)!important;max-width:9.4ch!important;letter-spacing:-.06em!important}.hero-mark small,.performance-media figcaption,.material-hero figcaption span,.detail-triptych figcaption,#dash small,#configurator .config-preview-id small,#configurator .config-summary small,#configurator .config-step-head small,#configurator .factory-setup small,#activate .activation-config small{font-size:8px!important}}
"""
s=s.rstrip()+"\n"+typography_css
p.write_text(s,encoding='utf-8')

# ---------------- request modal CSS: remove duplicate lang/tech rules; improve modal microcopy ----------------
p=ROOT/'v4-request-modal-v1.css'
s=p.read_text(encoding='utf-8')
s=sub_once(s,r"/\* Header language control:.*?/\* Request is removed from the document flow only after JS has initialized the modal controller\. \*/",
"/* Request is removed from the document flow only after JS has initialized the modal controller. */",'request css duplicate header/tech')
s=s.replace('.request-modal-title small{font-size:7px;','.request-modal-title small{font-size:8px;',1)
s=s.replace('.request-modal-title small{font-size:6.5px;','.request-modal-title small{font-size:8px;',1)
s=s.replace('.request-modal-configbar small{font-size:6.5px;','.request-modal-configbar small{font-size:8px;',1)
p.write_text(s,encoding='utf-8')

# ---------------- index: RU-first labels + cache-bust ----------------
p=ROOT/'index.html'
s=p.read_text(encoding='utf-8')
replacements={
  '10—80% / target':'10—80% / целевое',
  '<small>YOUR R1</small><strong id="configProfileLabel">':'<small>ВАШ R1</small><strong id="configProfileLabel">',
  '<small>BUILD CODE</small><strong id="configCode">':'<small>КОД СБОРКИ</small><strong id="configCode">',
  '<div class="config-compare-label"><span>BASE R1</span><span>YOUR R1</span></div>':'<div class="config-compare-label"><span>BASE R1</span><span>ВАШ R1</span></div>',
  '<div class="config-active-build"><div><small>ACTIVE BUILD</small>':'<div class="config-active-build"><div><small>АКТИВНАЯ СБОРКА</small>',
  '<span>ВЕРНУТЬ FACTORY SETUP</span>':'<span>ВЕРНУТЬ ЗАВОДСКУЮ СБОРКУ</span>',
  '<small>FACTORY PROFILE</small>':'<small>ЗАВОДСКОЙ ПРОФИЛЬ</small>',
  '<div class="factory-setup"><small>FACTORY SETUP</small>':'<div class="factory-setup"><small>ЗАВОДСКАЯ СБОРКА</small>',
  '<strong>ИНЖЕНЕРНЫЕ ПАКЕТЫ</strong><small>ENGINEERING OPTIONS</small>':'<strong>ИНЖЕНЕРНЫЕ ПАКЕТЫ</strong><small>ИНЖЕНЕРНЫЕ ОПЦИИ</small>',
  '<small>CONFIG / LIGHT SIGNATURE</small>':'<small>КОНФИГУРАЦИЯ / СВЕТОВАЯ ПОДПИСЬ</small>',
  '<div class="activation-build" id="activationBuild">YOUR R1 / ROAD / 2 MODULES</div>':'<div class="activation-build" id="activationBuild">ВАШ R1 / ROAD / 2 МОДУЛЯ</div>',
  'v4-locale-v1.css?v=1':'v4-locale-v1.css?v=2',
  'v4-request-modal-v1.css?v=4':'v4-request-modal-v1.css?v=5',
  'v4.js?v=16':'v4.js?v=17',
  'v4-locale-v1.js?v=4':'v4-locale-v1.js?v=5'
}
for old,new in replacements.items():
    if old not in s: raise SystemExit(f'index anchor missing: {old[:70]}')
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# ---------------- location README ----------------
p=ROOT/'data/README.md'
p.write_text('# Location data\n\nLocalized region and city autocomplete data is generated from [GeoNames](https://www.geonames.org/) and used by the VANTA R1 request interface. GeoNames data is licensed under Creative Commons Attribution 4.0. Runtime data lives in `regions-i18n.json` and `locations-i18n/`.\n',encoding='utf-8')

# ---------------- QA harness false-positive cleanup ----------------
p=ROOT/'.github/scripts/full_qa.mjs'
s=p.read_text(encoding='utf-8')
s=s.replace("const broken=await page.evaluate(()=>[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src));",
"const broken=await page.evaluate(()=>[...document.images].map(i=>({i,src:i.currentSrc||i.getAttribute('src')||''})).filter(x=>x.src&&x.i.complete&&x.i.naturalWidth===0).map(x=>x.src));",1)
p.write_text(s,encoding='utf-8')

print('Full QA production fix pass prepared successfully')
