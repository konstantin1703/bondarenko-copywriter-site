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
  const navAnchors=[...document.querySelectorAll('.desktop-nav a,.activate-link,.mobile-menu a')];
  const navSections=[...document.querySelectorAll('main section[id]')];

  const updateScroll=()=>{
    scrollTick=false;
    const y=window.scrollY;
    const max=Math.max(document.documentElement.scrollHeight-window.innerHeight,1);
    header?.classList.toggle('scrolled',y>18);
    if(progress) progress.style.transform=`scaleX(${Math.min(y/max,1)})`;
    if(navSections.length){
      const probe=y+innerHeight*.34;
      let current='';
      navSections.forEach(section=>{if(section.offsetTop<=probe)current=section.id;});
      navAnchors.forEach(link=>link.classList.toggle('is-current',link.getAttribute('href')===`#${current}`));
    }
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

  const revealEls=document.querySelectorAll('.reveal');
  if(reduceMotion||!('IntersectionObserver' in window)){
    revealEls.forEach(el=>el.classList.add('show'));
  }else{
    const io=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('show');io.unobserve(entry.target);}
    }),{threshold:.1,rootMargin:'0px 0px -3% 0px'});
    revealEls.forEach(el=>io.observe(el));
  }

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
    const hotspots=[['45.5%','24.6%'],['80.5%','30%'],['33%','52%']];
    if(architecture&&active){architecture.style.setProperty('--call-x',hotspots[index][0]);architecture.style.setProperty('--call-y',hotspots[index][1]);}
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

  const rail=document.getElementById('rail');
  const galleryFrames=[...(rail?.querySelectorAll('figure')||[])];
  const galleryCounter=document.getElementById('galleryCounter');
  const galleryProgress=document.getElementById('galleryProgress');
  const prevButton=document.getElementById('prev');
  const nextButton=document.getElementById('next');
  let galleryRaf=0;
  let galleryIndex=0;
  const setGalleryActive=index=>{
    if(!galleryFrames.length)return;
    galleryIndex=Math.max(0,Math.min(index,galleryFrames.length-1));
    galleryFrames.forEach((frame,i)=>{const active=i===galleryIndex;frame.classList.toggle('is-active',active);frame.setAttribute('aria-current',active?'true':'false');});
    if(galleryCounter)galleryCounter.textContent=`${String(galleryIndex+1).padStart(2,'0')} / ${String(galleryFrames.length).padStart(2,'0')}`;
    if(galleryProgress)galleryProgress.style.width=`${((galleryIndex+1)/galleryFrames.length)*100}%`;
    if(prevButton)prevButton.disabled=galleryIndex===0;
    if(nextButton)nextButton.disabled=galleryIndex===galleryFrames.length-1;
  };
  const closestGalleryIndex=()=>{
    if(!rail||!galleryFrames.length)return 0;
    const rr=rail.getBoundingClientRect();const center=rr.left+rr.width/2;let active=0,best=Infinity;
    galleryFrames.forEach((frame,i)=>{const r=frame.getBoundingClientRect();const d=Math.abs((r.left+r.width/2)-center);if(d<best){best=d;active=i;}});
    return active;
  };
  const updateGalleryActive=()=>{galleryRaf=0;setGalleryActive(closestGalleryIndex());};
  const requestGalleryUpdate=()=>{if(!galleryRaf)galleryRaf=requestAnimationFrame(updateGalleryActive);};
  const scrollGalleryTo=index=>{
    if(!rail||!galleryFrames.length)return;const target=Math.max(0,Math.min(index,galleryFrames.length-1));const frame=galleryFrames[target];
    const left=frame.offsetLeft-(rail.clientWidth-frame.offsetWidth)/2;rail.scrollTo({left,behavior:reduceMotion?'auto':'smooth'});setGalleryActive(target);
  };
  prevButton?.addEventListener('click',()=>scrollGalleryTo(galleryIndex-1));
  nextButton?.addEventListener('click',()=>scrollGalleryTo(galleryIndex+1));
  rail?.addEventListener('scroll',requestGalleryUpdate,{passive:true});
  rail?.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();scrollGalleryTo(galleryIndex-1);}if(e.key==='ArrowRight'){e.preventDefault();scrollGalleryTo(galleryIndex+1);}if(e.key==='Home'){e.preventDefault();scrollGalleryTo(0);}if(e.key==='End'){e.preventDefault();scrollGalleryTo(galleryFrames.length-1);}});
  addEventListener('resize',requestGalleryUpdate,{passive:true});
  if(rail&&finePointer){
    let dragging=false,startX=0,startScroll=0,moved=false;
    rail.addEventListener('pointerdown',e=>{if(e.button!==0)return;dragging=true;moved=false;startX=e.clientX;startScroll=rail.scrollLeft;rail.classList.add('is-dragging');rail.setPointerCapture?.(e.pointerId);});
    rail.addEventListener('pointermove',e=>{if(!dragging)return;const dx=e.clientX-startX;if(Math.abs(dx)>3)moved=true;rail.scrollLeft=startScroll-dx;});
    const endDrag=e=>{if(!dragging)return;dragging=false;rail.classList.remove('is-dragging');rail.releasePointerCapture?.(e.pointerId);if(moved)scrollGalleryTo(closestGalleryIndex());};
    rail.addEventListener('pointerup',endDrag);rail.addEventListener('pointercancel',endDrag);
  }
  setGalleryActive(0);

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

  const stage=document.getElementById('stage');
  const activateBtn=document.getElementById('activateBtn');
  const status=document.getElementById('bootStatus');
  const note=document.getElementById('activateNote');
  const activateLabel=activateBtn?.querySelector('span');
  const finishName=document.getElementById('finishName');
  const finishDesc=document.getElementById('finishDesc');
  const finishes={red:{name:'SIGNAL RED',desc:'Фирменная красная световая подпись.'},green:{name:'VOLT GREEN',desc:'Холодный электрический зелёный акцент.'},stealth:{name:'STEALTH BLACK',desc:'Монохромный режим без лишнего блеска.'}};
  let currentFinish='red';
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
    if(note)note.textContent=on?`${finishes[currentFinish].name}: оптика и бортовая система активированы.`:'Система ожидает запуска.';
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
  const applyFinish=(key,{announce=true}={})=>{
    const finish=finishes[key]||finishes.red;currentFinish=finishes[key]?key:'red';
    document.querySelectorAll('.sw').forEach(x=>{const active=x.dataset.color===currentFinish;x.classList.toggle('active',active);x.setAttribute('aria-pressed',String(active));});
    stage?.classList.remove('color-green','color-stealth','color-shifting');
    if(currentFinish==='green')stage?.classList.add('color-green');
    if(currentFinish==='stealth')stage?.classList.add('color-stealth');
    if(stage&&!reduceMotion){void stage.offsetWidth;stage.classList.add('color-shifting');setTimeout(()=>stage.classList.remove('color-shifting'),420);}
    if(finishName)finishName.textContent=finish.name;
    if(finishDesc)finishDesc.textContent=finish.desc;
    if(announce&&note)note.textContent=activationOn?`${finish.name}: световой характер обновлён.`:'Выбран световой характер. Система ожидает запуска.';
  };
  document.querySelectorAll('.sw').forEach(sw=>sw.addEventListener('click',()=>applyFinish(sw.dataset.color)));
  applyFinish('red',{announce:false});

  const techTrigger=document.getElementById('techTrigger');
  const techSheet=document.getElementById('techSheet');
  const techClose=document.getElementById('techClose');
  techTrigger?.addEventListener('click',()=>{if(techSheet?.showModal)techSheet.showModal();else techSheet?.setAttribute('open','');});
  techClose?.addEventListener('click',()=>techSheet?.close?.());
  techSheet?.addEventListener('click',e=>{if(e.target===techSheet)techSheet.close?.();});
})();

/* VANTA R1 — Final Product QA Pass 2026-09 */
(()=>{
  'use strict';
  const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const facts=document.querySelector('.facts');
  const factNumbers=[...(facts?.querySelectorAll('b')||[])];
  let factsDone=false;
  const runFacts=()=>{
    if(factsDone||!facts||!factNumbers.length)return;
    factsDone=true;
    facts.classList.add('is-counting');
    factNumbers.forEach((node,index)=>{
      const raw=node.textContent.trim();
      const match=raw.match(/^(\d+(?:[.,]\d+)?)(.*)$/);
      if(!match)return;
      const target=Number(match[1].replace(',','.'));
      const suffix=match[2];
      if(reduce){node.textContent=`${match[1]}${suffix}`;return;}
      const start=performance.now()+index*70;
      const duration=540;
      const tick=now=>{
        const t=Math.max(0,Math.min((now-start)/duration,1));
        const eased=1-Math.pow(1-t,3);
        const value=target*eased;
        node.textContent=`${Number.isInteger(target)?Math.round(value):value.toFixed(1)}${suffix}`;
        if(t<1)requestAnimationFrame(tick);
        else node.textContent=`${match[1]}${suffix}`;
      };
      requestAnimationFrame(tick);
    });
    setTimeout(()=>facts.classList.remove('is-counting'),850);
  };
  if(facts){
    if(reduce||!('IntersectionObserver' in window))runFacts();
    else{
      const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
        if(entry.isIntersecting){runFacts();observer.disconnect();}
      }),{threshold:.42});
      observer.observe(facts);
    }
  }

  const rail=document.getElementById('rail');
  const frames=[...(rail?.querySelectorAll('figure')||[])];
  if(rail&&frames.length){
    const dialog=document.createElement('dialog');
    dialog.className='gallery-lightbox';
    dialog.setAttribute('aria-label','Полноэкранная галерея VANTA R1');
    dialog.innerHTML=`<div class="gallery-lightbox-head"><span class="gallery-lightbox-count">01 / ${String(frames.length).padStart(2,'0')}</span><button class="gallery-lightbox-close" type="button" aria-label="Закрыть галерею">×</button></div><div class="gallery-lightbox-stage"><button class="gallery-lightbox-nav gallery-lightbox-prev" type="button" aria-label="Предыдущий кадр">←</button><img alt=""><button class="gallery-lightbox-nav gallery-lightbox-next" type="button" aria-label="Следующий кадр">→</button></div><div class="gallery-lightbox-caption"><strong></strong><span></span></div>`;
    document.body.appendChild(dialog);
    const image=dialog.querySelector('.gallery-lightbox-stage img');
    const count=dialog.querySelector('.gallery-lightbox-count');
    const title=dialog.querySelector('.gallery-lightbox-caption strong');
    const desc=dialog.querySelector('.gallery-lightbox-caption span');
    const prev=dialog.querySelector('.gallery-lightbox-prev');
    const next=dialog.querySelector('.gallery-lightbox-next');
    const close=dialog.querySelector('.gallery-lightbox-close');
    let index=0;
    let touchX=0;
    const render=()=>{
      const frame=frames[index];
      const source=frame.querySelector('img');
      const strong=frame.querySelector('figcaption strong');
      const span=frame.querySelector('figcaption span');
      if(image&&source){image.src=source.currentSrc||source.src;image.alt=source.alt||'VANTA R1';}
      if(count)count.textContent=`${String(index+1).padStart(2,'0')} / ${String(frames.length).padStart(2,'0')}`;
      if(title)title.textContent=strong?.textContent||'';
      if(desc)desc.textContent=span?.textContent||'';
      if(prev)prev.disabled=index===0;
      if(next)next.disabled=index===frames.length-1;
    };
    const openAt=i=>{
      index=Math.max(0,Math.min(i,frames.length-1));
      render();
      document.body.classList.add('gallery-open');
      if(dialog.showModal)dialog.showModal();else dialog.setAttribute('open','');
    };
    const closeViewer=()=>{
      document.body.classList.remove('gallery-open');
      if(dialog.open&&dialog.close)dialog.close();else dialog.removeAttribute('open');
    };
    frames.forEach((frame,i)=>frame.querySelector('img')?.addEventListener('click',()=>openAt(i)));
    prev?.addEventListener('click',()=>{if(index>0){index-=1;render();}});
    next?.addEventListener('click',()=>{if(index<frames.length-1){index+=1;render();}});
    close?.addEventListener('click',closeViewer);
    dialog.addEventListener('close',()=>document.body.classList.remove('gallery-open'));
    dialog.addEventListener('click',e=>{if(e.target===dialog)closeViewer();});
    dialog.addEventListener('keydown',e=>{
      if(e.key==='ArrowLeft'&&index>0){e.preventDefault();index-=1;render();}
      if(e.key==='ArrowRight'&&index<frames.length-1){e.preventDefault();index+=1;render();}
    });
    dialog.addEventListener('touchstart',e=>{touchX=e.changedTouches[0]?.clientX||0;},{passive:true});
    dialog.addEventListener('touchend',e=>{
      const end=e.changedTouches[0]?.clientX||touchX;
      const dx=end-touchX;
      if(Math.abs(dx)<44)return;
      if(dx<0&&index<frames.length-1){index+=1;render();}
      if(dx>0&&index>0){index-=1;render();}
    },{passive:true});
  }
})();


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

/* VANTA R1 — Configurator V2 + Request Flow 2026-09 */
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
