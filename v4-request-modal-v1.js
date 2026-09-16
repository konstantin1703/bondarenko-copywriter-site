/* VANTA R1 — Request Interface controller / RU cleanup */
(()=>{
  'use strict';

  const request=document.getElementById('request');
  const requestBtn=document.getElementById('configRequest');
  const form=document.getElementById('requestForm');
  if(!request||!requestBtn||!form)return;

  const q=id=>document.getElementById(id);
  const lang=()=>window.vantaLocale?.get?.()||document.documentElement.lang||'ru';
  const focusableSelector='a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';
  let opened=false;
  let lockedScroll=0;
  let inerted=[];
  let returnFocus=null;

  /* Modal chrome is independent of the page section, but reuses the existing form DOM. */
  const bar=document.createElement('div');
  bar.className='request-modal-bar';
  bar.innerHTML=`
    <div class="request-modal-title"><small></small><strong></strong></div>
    <button class="request-modal-close" type="button" aria-label="Закрыть оформление заявки"></button>`;
  request.prepend(bar);

  const configbar=document.createElement('div');
  configbar.className='request-modal-configbar';
  configbar.setAttribute('aria-live','polite');
  configbar.innerHTML=`
    <span class="rm-build"><small></small><b>R1</b></span>
    <span class="rm-price"><small></small><b>—</b></span>
    <span class="rm-code"><small></small><b>—</b></span>`;
  bar.after(configbar);

  const setLead=(el,value)=>{
    if(!el)return;
    let node=[...el.childNodes].find(n=>n.nodeType===Node.TEXT_NODE);
    if(!node){node=document.createTextNode('');el.prepend(node)}
    node.nodeValue=value;
  };
  const text=(sel,value)=>{const el=request.querySelector(sel);if(el)el.textContent=value};
  const attr=(id,name,value)=>{const el=q(id);if(el)el.setAttribute(name,value)};

  const syncCompactSummary=()=>{
    const profile=q('requestProfile')?.textContent?.trim()||'R1';
    const price=q('requestPrice')?.textContent?.trim()||'—';
    const code=q('requestConfigCode')?.textContent?.trim()||'—';
    configbar.querySelector('.rm-build b').textContent=profile;
    configbar.querySelector('.rm-price b').textContent=price;
    configbar.querySelector('.rm-code b').textContent=code;
  };

  const paintRequestLanguage=()=>{
    const en=lang()==='en';
    bar.querySelector('.request-modal-title small').textContent=en?'R1 / REQUEST INTERFACE':'R1 / СИСТЕМА ЗАЯВКИ';
    bar.querySelector('.request-modal-title strong').textContent=en?'R1 REQUEST':'ОФОРМЛЕНИЕ R1';
    bar.querySelector('.request-modal-close').setAttribute('aria-label',en?'Close request':'Закрыть оформление заявки');

    const progress=[...request.querySelectorAll('.request-progress button')];
    const main=en?['CONTACTS','DELIVERY','REVIEW']:['КОНТАКТЫ','ДОСТАВКА','ПРОВЕРКА'];
    const sub=en?['IDENTITY','DELIVERY','CONFIRM']:['ДАННЫЕ','АДРЕС','ПРОВЕРКА'];
    progress.forEach((button,i)=>{
      const span=button.querySelector('span');
      setLead(span,main[i]||'');
      const small=span?.querySelector('small');if(small)small.textContent=sub[i]||'';
    });

    setLead(request.querySelector('.request-summary-kicker'),en?'YOUR CONFIGURATION':'ВАША КОНФИГУРАЦИЯ');
    const summaryHeads=request.querySelectorAll('.request-summary-head span>small');
    if(summaryHeads[0])summaryHeads[0].textContent=en?'YOUR R1':'ВАШ R1';
    if(summaryHeads[1])summaryHeads[1].textContent=en?'PRICE':'СТОИМОСТЬ';
    const stats=request.querySelectorAll('.request-summary-stats span>small');
    const statNames=en?['POWER','MASS','RANGE']:['МОЩНОСТЬ','МАССА','ЗАПАС'];
    stats.forEach((el,i)=>el.textContent=statNames[i]||el.textContent);
    text('.request-summary-modules>small',en?'ACTIVE BUILD':'УСТАНОВЛЕНО');
    text('.request-summary-code>span',en?'BUILD CODE':'КОД СБОРКИ');

    const pickerSmall=request.querySelector('.region-picker-panel header small');
    if(pickerSmall)pickerSmall.textContent=en?'COUNTRY DATABASE':'СПРАВОЧНИК СТРАН';
    const lock=request.querySelector('.request-lock-mark span');if(lock)lock.textContent=en?'R1 / REQUEST SYSTEM':'R1 / СИСТЕМА ЗАЯВКИ';
    const locked=request.querySelector('.request-complete>small');if(locked)locked.textContent=en?'CONFIGURATION LOCKED':'КОНФИГУРАЦИЯ ЗАФИКСИРОВАНА';
    const requestId=request.querySelector('.request-code span');if(requestId)requestId.textContent=en?'REQUEST ID':'НОМЕР ЗАЯВКИ';

    /* Attribute localization is enforced here because the older locale layer translated RU placeholders both ways. */
    attr('reqFirst','placeholder',en?'First name':'Иван');
    attr('reqLast','placeholder',en?'Last name':'Иванов');
    attr('reqPhone','placeholder',en?'Phone number':'Номер телефона');
    attr('reqRegion','placeholder',en?'Start typing a region':'Начни вводить регион');
    attr('reqCity','placeholder',en?'Start typing a city':'Начни вводить город');
    attr('reqPostal','placeholder',en?'Postal code':'000000');
    attr('reqAddress','placeholder',en?'Street, building':'Улица, дом');
    attr('reqAddress2','placeholder',en?'Apartment / office / note':'Квартира / офис / комментарий');
    attr('regionSearch','placeholder',en?'Country or calling code':'Страна или код +7');

    const phoneHint=q('phoneHint');if(phoneHint)phoneHint.textContent=en?'Choose a country or calling code.':'Выбери страну или телефонный код.';
    const regionHint=q('reqRegion')?.parentElement?.querySelector('.field-hint');if(regionHint)regionHint.textContent=en?'Start typing — suggestions are limited to the selected country.':'Начни вводить — подсказки будут только по выбранной стране.';
    const cityHint=q('reqCity')?.parentElement?.querySelector('.field-hint');if(cityHint)cityHint.textContent=en?'Cities from other countries are never shown.':'Показываются только города выбранной страны.';

    const countryName=q('countryName');
    if(countryName&&['ВЫБЕРИ СТРАНУ','SELECT COUNTRY','CHOOSE COUNTRY'].includes(countryName.textContent.trim()))countryName.textContent=en?'SELECT COUNTRY':'ВЫБЕРИ СТРАНУ';
    const dial=q('phoneDial');
    if(dial&&['Код','Code','CODE'].includes(dial.textContent.trim()))dial.textContent=en?'Code':'Код';

    configbar.querySelector('.rm-build small').textContent=en?'YOUR R1':'ВАШ R1';
    configbar.querySelector('.rm-price small').textContent=en?'PRICE':'СТОИМОСТЬ';
    configbar.querySelector('.rm-code small').textContent=en?'BUILD CODE':'КОД СБОРКИ';
    syncCompactSummary();
  };

  const closeMobileMenu=()=>{
    q('mobileMenu')?.classList.remove('open');
    q('menu')?.classList.remove('open');
    q('menu')?.setAttribute('aria-expanded','false');
    q('mobileMenu')?.setAttribute('aria-hidden','true');
  };

  const lockPage=()=>{
    lockedScroll=window.scrollY||document.documentElement.scrollTop||0;
    document.body.style.setProperty('--request-scroll-lock',`${-lockedScroll}px`);
    document.body.classList.add('request-open');
  };
  const unlockPage=()=>{
    document.body.classList.remove('request-open');
    document.body.style.removeProperty('--request-scroll-lock');
    window.scrollTo(0,lockedScroll);
  };

  const setBackgroundInert=()=>{
    const parent=request.parentElement;
    const candidates=[
      ...[...document.body.children].filter(el=>el!==parent),
      ...(parent?[...parent.children].filter(el=>el!==request):[])
    ];
    inerted=[...new Set(candidates)].map(el=>({el,wasInert:el.inert}));
    inerted.forEach(({el})=>{el.inert=true});
  };
  const restoreBackground=()=>{
    inerted.forEach(({el,wasInert})=>{el.inert=wasInert});
    inerted=[];
  };
  const visibleFocusables=()=>[...request.querySelectorAll(focusableSelector)].filter(el=>!el.disabled&&el.getClientRects().length>0);

  const openModal=({push=true}={})=>{
    if(opened)return;
    opened=true;
    returnFocus=document.activeElement instanceof HTMLElement?document.activeElement:requestBtn;
    closeMobileMenu();
    paintRequestLanguage();
    syncCompactSummary();
    request.classList.add('request-modal-open');
    request.setAttribute('aria-modal','true');
    request.setAttribute('role','dialog');
    lockPage();
    setBackgroundInert();
    request.scrollTop=0;
    queueMicrotask(()=>bar.querySelector('.request-modal-close')?.focus({preventScroll:true}));
    if(push&&location.hash!=='#request')history.pushState({...(history.state||{}),vantaRequestModal:true},'','#request');
  };

  const closeInternal=({cleanHash=false}={})=>{
    if(!opened)return;
    opened=false;
    request.classList.remove('request-modal-open');
    request.removeAttribute('aria-modal');
    request.removeAttribute('role');
    restoreBackground();
    unlockPage();
    if(cleanHash&&location.hash==='#request')history.replaceState({...history.state,vantaRequestModal:false},'',location.pathname+location.search);
    const target=returnFocus?.isConnected?returnFocus:requestBtn;
    returnFocus=null;
    target?.focus?.({preventScroll:true});
  };

  const closeByUser=()=>{
    if(history.state?.vantaRequestModal){history.back();return}
    closeInternal({cleanHash:true});
  };

  bar.querySelector('.request-modal-close').addEventListener('click',closeByUser);
  request.addEventListener('keydown',e=>{
    if(e.key==='Escape'){
      e.preventDefault();
      closeByUser();
      return;
    }
    if(e.key!=='Tab')return;
    const focusables=visibleFocusables();
    if(!focusables.length){e.preventDefault();return}
    const first=focusables[0];
    const last=focusables[focusables.length-1];
    const active=document.activeElement;
    if(e.shiftKey&&(active===first||!request.contains(active))){e.preventDefault();last.focus()}
    else if(!e.shiftKey&&(active===last||!request.contains(active))){e.preventDefault();first.focus()}
  });

  /* Capture phase prevents the old scrollIntoView handler from running. */
  requestBtn.addEventListener('click',e=>{
    e.preventDefault();
    e.stopImmediatePropagation();
    openModal({push:true});
  },true);

  document.addEventListener('click',e=>{
    const link=e.target.closest('a[href="#request"]');
    if(!link)return;
    e.preventDefault();
    e.stopImmediatePropagation();
    openModal({push:true});
  },true);

  q('requestToActivation')?.addEventListener('click',()=>{
    /* Let the existing activation handler continue after the modal has disappeared. */
    closeInternal({cleanHash:true});
  },true);

  window.addEventListener('popstate',()=>{
    if(opened)closeInternal({cleanHash:false});
    else if(location.hash==='#request')openModal({push:false});
  });

  const repaint=()=>queueMicrotask(paintRequestLanguage);
  window.addEventListener('vanta:languagechange',repaint);
  new MutationObserver(repaint).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});

  const summaryObserver=new MutationObserver(syncCompactSummary);
  [q('requestProfile'),q('requestPrice'),q('requestConfigCode')].filter(Boolean).forEach(el=>summaryObserver.observe(el,{subtree:true,childList:true,characterData:true}));

  document.documentElement.classList.add('request-modal-ready');
  paintRequestLanguage();
  syncCompactSummary();

  if(location.hash==='#request')queueMicrotask(()=>openModal({push:false}));
})();
