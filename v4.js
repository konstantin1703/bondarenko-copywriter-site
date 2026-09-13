(()=>{
  'use strict';

  const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer=window.matchMedia('(hover:hover) and (pointer:fine)').matches;
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
    if(open)lastFocus=document.activeElement;
    document.body.classList.toggle('nav-open',open);
    mobile.classList.toggle('open',open);
    menu.classList.toggle('open',open);
    menu.setAttribute('aria-expanded',String(open));
    mobile.setAttribute('aria-hidden',String(!open));
    if(open)mobile.querySelector('a')?.focus();
    else if(restoreFocus)(lastFocus instanceof HTMLElement?lastFocus:menu).focus();
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

  // Progressive section reveal. No scroll locking or scroll-driven timelines.
  const revealEls=document.querySelectorAll('.reveal');
  if(reduceMotion||!('IntersectionObserver' in window)){
    revealEls.forEach(el=>el.classList.add('show'));
  }else{
    const io=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('show');io.unobserve(entry.target);}
    }),{threshold:.1,rootMargin:'0px 0px -3% 0px'});
    revealEls.forEach(el=>io.observe(el));
  }

  // Tiny pointer parallax: product media moves inside its frame, never the layout.
  if(!reduceMotion&&finePointer){
    const bindParallax=(host,img,maxX,maxY,hero=false)=>{
      if(!host||!img)return;
      let raf=0;
      const render=(x,y)=>{
        if(hero){img.style.setProperty('--hero-x',`${x.toFixed(2)}px`);img.style.setProperty('--hero-y',`${y.toFixed(2)}px`);}
        else{img.style.setProperty('--px',`${x.toFixed(2)}px`);img.style.setProperty('--py',`${y.toFixed(2)}px`);}
      };
      host.addEventListener('pointermove',e=>{
        if(raf)return;
        raf=requestAnimationFrame(()=>{
          raf=0;
          const r=host.getBoundingClientRect();
          const nx=((e.clientX-r.left)/r.width-.5)*2;
          const ny=((e.clientY-r.top)/r.height-.5)*2;
          render(nx*maxX,ny*maxY);
        });
      },{passive:true});
      host.addEventListener('pointerleave',()=>render(0,0),{passive:true});
    };
    const heroHost=document.querySelector('.hero-media');
    bindParallax(heroHost,heroHost?.querySelector('img'),8,6,true);
    const performanceHost=document.querySelector('.performance-media');
    bindParallax(performanceHost,performanceHost?.querySelector('img'),7,5);
    const materialHost=document.querySelector('.material-hero');
    bindParallax(materialHost,materialHost?.querySelector('img'),5,4);
  }

  // Engineering callouts: hover/focus previews, tap/click pins one annotation.
  const architecture=document.querySelector('.architecture-stage');
  const calls=[...(architecture?.querySelectorAll('.call')||[])];
  const svg=architecture?.querySelector('.callout-map');
  const paths=[...(svg?.querySelectorAll('.call-line')||[])];
  const halos=[...(svg?.querySelectorAll('.call-halo')||[])];
  const points=[...(svg?.querySelectorAll('.call-point')||[])];
  let pinnedCall=-1;
  const paintCall=index=>{
    const active=index>=0;
    if(active)architecture?.classList.add('has-interacted');
    architecture?.classList.toggle('has-call-focus',active);
    calls.forEach((call,i)=>{
      const on=i===index;
      call.classList.toggle('is-active',on);
      call.setAttribute('aria-pressed',String(on));
    });
    [paths,halos,points].forEach(group=>group.forEach((el,i)=>{
      el.classList.toggle('is-active',i===index);
      el.classList.toggle('is-muted',active&&i!==index);
    }));
  };
  calls.forEach((call,i)=>{
    if(finePointer){
      call.addEventListener('pointerenter',()=>{if(pinnedCall<0)paintCall(i);},{passive:true});
      call.addEventListener('pointerleave',()=>{if(pinnedCall<0)paintCall(-1);},{passive:true});
    }
    call.addEventListener('focus',()=>{if(pinnedCall<0)paintCall(i);});
    call.addEventListener('blur',()=>{if(pinnedCall<0)paintCall(-1);});
    const toggle=()=>{pinnedCall=pinnedCall===i?-1:i;paintCall(pinnedCall);};
    call.addEventListener('click',toggle);
    call.addEventListener('keydown',e=>{
      if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle();}
      if(e.key==='Escape'){pinnedCall=-1;paintCall(-1);call.blur();}
    });
  });
  architecture?.addEventListener('click',e=>{
    if(pinnedCall>=0&&!e.target.closest('.call')){pinnedCall=-1;paintCall(-1);}
  });

  // Gallery: centered frame becomes the visual anchor; keyboard arrows mirror buttons.
  const rail=document.getElementById('rail');
  const galleryFrames=[...(rail?.querySelectorAll('figure')||[])];
  let galleryRaf=0;
  const updateGalleryActive=()=>{
    galleryRaf=0;
    if(!rail||!galleryFrames.length)return;
    const center=rail.scrollLeft+rail.clientWidth/2;
    let active=0,best=Infinity;
    galleryFrames.forEach((frame,i)=>{
      const fc=frame.offsetLeft+frame.offsetWidth/2;
      const d=Math.abs(fc-center);
      if(d<best){best=d;active=i;}
    });
    galleryFrames.forEach((frame,i)=>frame.classList.toggle('is-active',i===active));
  };
  const requestGalleryUpdate=()=>{
    if(galleryRaf)return;
    galleryRaf=requestAnimationFrame(updateGalleryActive);
  };
  const shift=()=>Math.min((rail?.clientWidth||0)*.82,760);
  const scrollGallery=direction=>rail?.scrollBy({left:direction*shift(),behavior:reduceMotion?'auto':'smooth'});
  document.getElementById('prev')?.addEventListener('click',()=>scrollGallery(-1));
  document.getElementById('next')?.addEventListener('click',()=>scrollGallery(1));
  rail?.addEventListener('scroll',requestGalleryUpdate,{passive:true});
  rail?.addEventListener('keydown',e=>{
    if(e.key==='ArrowLeft'){e.preventDefault();scrollGallery(-1);}
    if(e.key==='ArrowRight'){e.preventDefault();scrollGallery(1);}
  });
  addEventListener('resize',requestGalleryUpdate,{passive:true});
  updateGalleryActive();

  // Ride System — one state model, animated speed and calibrated visual settle.
  const dash=document.getElementById('dash');
  const speed=document.getElementById('speed');
  const battery=document.getElementById('battery');
  const range=document.getElementById('range');
  const regen=document.getElementById('regen');
  const powerLabel=document.getElementById('powerLabel');
  const powerMeter=dash?.querySelector('.power');
  const speedArc=document.getElementById('speedArc');
  const powerArcSvg=document.getElementById('powerArcSvg');
  const speedTicks=document.getElementById('speedTicks');
  const modeName=document.getElementById('modeName');
  const modeDesc=document.getElementById('modeDesc');
  const states={
    road:{speed:84,battery:'78%',range:'214 км',regen:'СРЕДНЯЯ',regenValue:48,power:62,dial:142,name:'ДОРОГА',desc:'Сбалансированный отклик'},
    attack:{speed:146,battery:'61%',range:'128 км',regen:'НИЗКАЯ',regenValue:18,power:94,dial:232,name:'ТРЕК',desc:'Максимальная отдача привода'},
    range:{speed:62,battery:'84%',range:'286 км',regen:'ВЫСОКАЯ',regenValue:88,power:42,dial:106,name:'ЭКО',desc:'Приоритет запаса хода'}
  };

const svgNS='http://www.w3.org/2000/svg';
if(speedTicks&&!speedTicks.childElementCount){
  const count=31;
  for(let i=0;i<count;i+=1){
    const angle=135+(270/(count-1))*i;
    const rad=angle*Math.PI/180;
    const major=i%5===0;
    const inner=major?108:112;
    const outer=119;
    const line=document.createElementNS(svgNS,'line');
    line.setAttribute('x1',String(160+Math.cos(rad)*inner));
    line.setAttribute('y1',String(160+Math.sin(rad)*inner));
    line.setAttribute('x2',String(160+Math.cos(rad)*outer));
    line.setAttribute('y2',String(160+Math.sin(rad)*outer));
    line.classList.add(major?'is-major':'is-minor');
    speedTicks.appendChild(line);
  }
}
const setSvgArc=(arc,percent)=>{
  if(!arc)return;
  const clamped=Math.max(0,Math.min(Number(percent)||0,100));
  const visible=75*clamped/100;
  arc.style.strokeDasharray=`${visible.toFixed(2)} ${(100-visible).toFixed(2)}`;
};
setSvgArc(speedArc,42);
setSvgArc(powerArcSvg,62);

let speedAnimation=0;
  let calibrateTimer=0;
  const formatSpeed=value=>String(Math.max(0,Math.round(value))).padStart(3,'0');
  const animateSpeed=target=>{
    if(!speed)return;
    cancelAnimationFrame(speedAnimation);
    const from=Number.parseInt(speed.textContent,10)||0;
    if(reduceMotion||from===target){speed.textContent=formatSpeed(target);return;}
    const start=performance.now();
    const duration=520;
    const tickSpeed=now=>{
      const t=Math.min((now-start)/duration,1);
      const eased=1-Math.pow(1-t,3);
      speed.textContent=formatSpeed(from+(target-from)*eased);
      if(t<1)speedAnimation=requestAnimationFrame(tickSpeed);
    };
    speedAnimation=requestAnimationFrame(tickSpeed);
  };
  const calibrate=()=>{
    if(!dash||reduceMotion)return;
    clearTimeout(calibrateTimer);
    dash.classList.remove('calibrating','dash-shift');
    void dash.offsetWidth;
    dash.classList.add('calibrating','dash-shift');
    calibrateTimer=setTimeout(()=>dash.classList.remove('calibrating','dash-shift'),520);
  };
  const applyMode=(key,{animate=true}={})=>{
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
  };
  document.querySelectorAll('.modes button').forEach(btn=>btn.addEventListener('click',()=>{
    if(btn.getAttribute('aria-pressed')==='true')return;
    document.querySelectorAll('.modes button').forEach(x=>{
      const active=x===btn;
      x.classList.toggle('active',active);
      x.setAttribute('aria-pressed',String(active));
    });
    applyMode(btn.dataset.mode);
  }));
  applyMode('road',{animate:false});

  const clock=document.getElementById('clock');
  const tick=()=>{if(clock)clock.textContent=new Date().toLocaleTimeString('ru-RU',{hour:'2-digit',minute:'2-digit'});};
  tick();
  setInterval(tick,15000);

  // Activation — restrained OEM boot sequence: CHECK -> READY -> ACTIVE.
  const stage=document.getElementById('stage');
  const activateBtn=document.getElementById('activateBtn');
  const status=document.getElementById('bootStatus');
  const note=document.getElementById('activateNote');
  const activateLabel=activateBtn?.querySelector('span');
  let activationOn=false;
  let activationBusy=false;
  let bootTimers=[];
  const clearBootTimers=()=>{bootTimers.forEach(clearTimeout);bootTimers=[];};
  const setActivationUi=on=>{
    activationOn=on;
    stage?.classList.toggle('stage-live',on);
    stage?.classList.remove('stage-booting','stage-ready');
    stage?.setAttribute('aria-busy','false');
    activateBtn?.setAttribute('aria-busy','false');
    activateBtn?.setAttribute('aria-pressed',String(on));
    if(status)status.textContent=on?'SYSTEM ACTIVE':'STANDBY';
    if(activateLabel)activateLabel.textContent=on?'ОТКЛЮЧИТЬ DEMO':'АКТИВИРОВАТЬ R1';
    if(note)note.textContent=on?'Оптика и бортовая система активированы. Можно менять цветовой режим.':'Система ожидает запуска.';
    activationBusy=false;
  };
  const bootActivation=()=>{
    if(!stage||!activateBtn||activationBusy)return;
    if(activationOn){clearBootTimers();setActivationUi(false);return;}
    if(reduceMotion){setActivationUi(true);return;}
    activationBusy=true;
    stage.classList.remove('stage-live','stage-ready');
    stage.classList.add('stage-booting');
    stage.setAttribute('aria-busy','true');
    activateBtn.setAttribute('aria-busy','true');
    if(status)status.textContent='SYSTEM CHECK';
    if(activateLabel)activateLabel.textContent='ЗАПУСК...';
    if(note)note.textContent='Проверка бортовой системы.';
    bootTimers=[
      setTimeout(()=>{
        stage.classList.add('stage-ready');
        if(status)status.textContent='READY';
        if(note)note.textContent='Система готова к активации.';
      },330),
      setTimeout(()=>setActivationUi(true),820)
    ];
  };
  activateBtn?.addEventListener('click',bootActivation);
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
