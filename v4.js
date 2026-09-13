(()=>{
  'use strict';

  const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const header=document.getElementById('header');
  const progress=document.getElementById('progress');
  const menu=document.getElementById('menu');
  const mobile=document.getElementById('mobileMenu');
  let lastFocus=null;
  let scrollTick=false;

  const updateScroll=()=>{
    scrollTick=false;
    const y=window.scrollY;
    const max=Math.max(document.documentElement.scrollHeight-window.innerHeight,1);
    header?.classList.toggle('scrolled',y>18);
    if(progress) progress.style.transform=`scaleX(${Math.min(y/max,1)})`;
  };
  const requestScrollUpdate=()=>{
    if(scrollTick)return;
    scrollTick=true;
    requestAnimationFrame(updateScroll);
  };
  updateScroll();
  addEventListener('scroll',requestScrollUpdate,{passive:true});

  const navFocusable=()=>[menu,...(mobile?.querySelectorAll('a')||[])].filter(Boolean);
  const setNav=(open,{restoreFocus=true}={})=>{
    if(!menu||!mobile)return;
    if(open){lastFocus=document.activeElement;}
    document.body.classList.toggle('nav-open',open);
    mobile.classList.toggle('open',open);
    menu.classList.toggle('open',open);
    menu.setAttribute('aria-expanded',String(open));
    mobile.setAttribute('aria-hidden',String(!open));
    if(open){mobile.querySelector('a')?.focus();}
    else if(restoreFocus){(lastFocus instanceof HTMLElement?lastFocus:menu).focus();}
  };
  menu?.addEventListener('click',()=>setNav(!mobile?.classList.contains('open')));
  mobile?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setNav(false,{restoreFocus:false})));
  document.addEventListener('keydown',e=>{
    if(!mobile?.classList.contains('open'))return;
    if(e.key==='Escape'){e.preventDefault();setNav(false);return;}
    if(e.key==='Tab'){
      const focusable=navFocusable();
      if(!focusable.length)return;
      const first=focusable[0],last=focusable[focusable.length-1];
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    }
  });
  addEventListener('resize',()=>{if(innerWidth>980&&mobile?.classList.contains('open'))setNav(false,{restoreFocus:false})},{passive:true});

  const revealEls=document.querySelectorAll('.reveal');
  if(reduceMotion||!('IntersectionObserver' in window)){
    revealEls.forEach(el=>el.classList.add('show'));
  }else{
    const io=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('show');io.unobserve(entry.target);}
    }),{threshold:.1});
    revealEls.forEach(el=>io.observe(el));
  }

  const rail=document.getElementById('rail');
  const shift=()=>Math.min((rail?.clientWidth||0)*.82,760);
  document.getElementById('prev')?.addEventListener('click',()=>rail?.scrollBy({left:-shift(),behavior:reduceMotion?'auto':'smooth'}));
  document.getElementById('next')?.addEventListener('click',()=>rail?.scrollBy({left:shift(),behavior:reduceMotion?'auto':'smooth'}));

  const dash=document.getElementById('dash');
  const speed=document.getElementById('speed');
  const battery=document.getElementById('battery');
  const range=document.getElementById('range');
  const regen=document.getElementById('regen');
  const powerLabel=document.getElementById('powerLabel');
  const powerMeter=dash?.querySelector('.power');
  const modeName=document.getElementById('modeName');
  const modeDesc=document.getElementById('modeDesc');
  const states={
    road:{speed:'084',battery:'78%',range:'214 км',regen:'СРЕДНЯЯ',regenValue:48,power:62,dial:142,name:'ДОРОГА',desc:'Сбалансированный отклик'},
    attack:{speed:'146',battery:'61%',range:'128 км',regen:'НИЗКАЯ',regenValue:18,power:94,dial:232,name:'ТРЕК',desc:'Максимальная отдача привода'},
    range:{speed:'062',battery:'84%',range:'286 км',regen:'ВЫСОКАЯ',regenValue:88,power:42,dial:106,name:'ЭКО',desc:'Приоритет запаса хода'}
  };
  const applyMode=key=>{
    const s=states[key];
    if(!dash||!s)return;
    dash.dataset.mode=key;
    dash.classList.remove('dash-shift');
    if(!reduceMotion){void dash.offsetWidth;dash.classList.add('dash-shift');}
    if(speed)speed.textContent=s.speed;
    if(battery)battery.textContent=s.battery;
    if(range)range.textContent=s.range;
    if(regen)regen.textContent=s.regen;
    if(powerLabel)powerLabel.textContent=`${s.power}%`;
    if(modeName)modeName.textContent=s.name;
    if(modeDesc)modeDesc.textContent=s.desc;
    dash.style.setProperty('--dial',`${s.dial}deg`);
    dash.style.setProperty('--power-angle',`${s.power*2.7}deg`);
    dash.style.setProperty('--power-half',`${s.power*.5}%`);
    dash.style.setProperty('--regen-half',`${s.regenValue*.5}%`);
    powerMeter?.setAttribute('aria-label',`Рекуперация ${s.regenValue} процентов, мощность ${s.power} процентов`);
  };
  document.querySelectorAll('.modes button').forEach(btn=>btn.addEventListener('click',()=>{
    document.querySelectorAll('.modes button').forEach(x=>{
      const active=x===btn;
      x.classList.toggle('active',active);
      x.setAttribute('aria-pressed',String(active));
    });
    applyMode(btn.dataset.mode);
  }));
  applyMode('road');

  const clock=document.getElementById('clock');
  const tick=()=>{if(clock)clock.textContent=new Date().toLocaleTimeString('ru-RU',{hour:'2-digit',minute:'2-digit'});};
  tick();
  setInterval(tick,15000);

  const stage=document.getElementById('stage');
  const activateBtn=document.getElementById('activateBtn');
  const status=document.getElementById('bootStatus');
  const note=document.getElementById('activateNote');
  activateBtn?.addEventListener('click',()=>{
    const on=stage?.classList.toggle('stage-live')||false;
    if(status)status.textContent=on?'SYSTEM ACTIVE':'STANDBY';
    activateBtn.setAttribute('aria-pressed',String(on));
    const label=activateBtn.querySelector('span');
    if(label)label.textContent=on?'ОТКЛЮЧИТЬ DEMO':'АКТИВИРОВАТЬ R1';
    if(note)note.textContent=on?'Оптика и бортовая система активированы. Можно менять цветовой режим.':'Система ожидает запуска.';
  });
  document.querySelectorAll('.sw').forEach(sw=>sw.addEventListener('click',()=>{
    document.querySelectorAll('.sw').forEach(x=>{
      const active=x===sw;
      x.classList.toggle('active',active);
      x.setAttribute('aria-pressed',String(active));
    });
    stage?.classList.remove('color-green','color-stealth');
    if(sw.dataset.color==='green')stage?.classList.add('color-green');
    if(sw.dataset.color==='stealth')stage?.classList.add('color-stealth');
  }));
})();
