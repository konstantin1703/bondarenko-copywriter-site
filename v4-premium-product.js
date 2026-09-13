(()=>{
  'use strict';

  const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer=window.matchMedia('(hover:hover) and (pointer:fine)').matches;

  // Current-section navigation state.
  const navAnchors=[...document.querySelectorAll('.desktop-nav a,.activate-link,.mobile-menu a')];
  const navSections=[...document.querySelectorAll('main section[id]')];
  let navRaf=0;
  const updateCurrentSection=()=>{
    navRaf=0;
    if(!navSections.length)return;
    const probe=window.scrollY+window.innerHeight*.34;
    let current='';
    navSections.forEach(section=>{if(section.offsetTop<=probe)current=section.id;});
    navAnchors.forEach(link=>link.classList.toggle('is-current',link.getAttribute('href')===`#${current}`));
  };
  const requestNavUpdate=()=>{if(!navRaf)navRaf=requestAnimationFrame(updateCurrentSection);};
  addEventListener('scroll',requestNavUpdate,{passive:true});
  addEventListener('resize',requestNavUpdate,{passive:true});
  updateCurrentSection();

  // Gallery: add product counter/progress without changing source markup.
  const rail=document.getElementById('rail');
  const frames=[...(rail?.querySelectorAll('figure')||[])];
  const controls=document.querySelector('.gallery-controls');
  const head=document.querySelector('.gallery-head');
  let toolbar=document.querySelector('.gallery-toolbar');
  let counter=document.getElementById('galleryCounter');
  let progress=document.getElementById('galleryProgress');
  if(head&&controls&&!toolbar){
    toolbar=document.createElement('div');
    toolbar.className='gallery-toolbar';
    const meta=document.createElement('div');
    meta.className='gallery-meta';
    meta.setAttribute('aria-live','polite');
    counter=document.createElement('span');
    counter.id='galleryCounter';
    counter.textContent=`01 / ${String(frames.length).padStart(2,'0')}`;
    const track=document.createElement('i');
    track.setAttribute('aria-hidden','true');
    progress=document.createElement('b');
    progress.id='galleryProgress';
    track.append(progress);
    meta.append(counter,track);
    controls.before(toolbar);
    toolbar.append(meta,controls);
  }

  const prev=document.getElementById('prev');
  const next=document.getElementById('next');
  let galleryIndex=0;
  let galleryRaf=0;
  const setGalleryActive=index=>{
    if(!frames.length)return;
    galleryIndex=Math.max(0,Math.min(index,frames.length-1));
    frames.forEach((frame,i)=>{
      const active=i===galleryIndex;
      frame.classList.toggle('is-active',active);
      frame.setAttribute('aria-current',active?'true':'false');
    });
    if(counter)counter.textContent=`${String(galleryIndex+1).padStart(2,'0')} / ${String(frames.length).padStart(2,'0')}`;
    if(progress)progress.style.width=`${((galleryIndex+1)/frames.length)*100}%`;
    if(prev)prev.disabled=galleryIndex===0;
    if(next)next.disabled=galleryIndex===frames.length-1;
  };
  const closestIndex=()=>{
    if(!rail||!frames.length)return 0;
    const rr=rail.getBoundingClientRect();
    const center=rr.left+rr.width/2;
    let index=0,best=Infinity;
    frames.forEach((frame,i)=>{
      const r=frame.getBoundingClientRect();
      const d=Math.abs((r.left+r.width/2)-center);
      if(d<best){best=d;index=i;}
    });
    return index;
  };
  const updateGallery=()=>{galleryRaf=0;setGalleryActive(closestIndex());};
  const requestGalleryUpdate=()=>{if(!galleryRaf)galleryRaf=requestAnimationFrame(updateGallery);};
  const scrollToFrame=index=>{
    if(!rail||!frames.length)return;
    const target=Math.max(0,Math.min(index,frames.length-1));
    const frame=frames[target];
    const left=frame.offsetLeft-(rail.clientWidth-frame.offsetWidth)/2;
    rail.scrollTo({left,behavior:reduceMotion?'auto':'smooth'});
    setGalleryActive(target);
  };
  prev?.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();scrollToFrame(galleryIndex-1);},true);
  next?.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();scrollToFrame(galleryIndex+1);},true);
  rail?.addEventListener('keydown',e=>{
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;
    e.preventDefault();e.stopImmediatePropagation();
    if(e.key==='ArrowLeft')scrollToFrame(galleryIndex-1);
    if(e.key==='ArrowRight')scrollToFrame(galleryIndex+1);
    if(e.key==='Home')scrollToFrame(0);
    if(e.key==='End')scrollToFrame(frames.length-1);
  },true);
  rail?.addEventListener('scroll',requestGalleryUpdate,{passive:true});
  addEventListener('resize',requestGalleryUpdate,{passive:true});
  if(rail&&finePointer){
    let dragging=false,startX=0,startScroll=0,moved=false;
    rail.addEventListener('pointerdown',e=>{
      if(e.button!==0)return;
      dragging=true;moved=false;startX=e.clientX;startScroll=rail.scrollLeft;
      rail.classList.add('is-dragging');rail.setPointerCapture?.(e.pointerId);
    });
    rail.addEventListener('pointermove',e=>{
      if(!dragging)return;
      const dx=e.clientX-startX;
      if(Math.abs(dx)>3)moved=true;
      rail.scrollLeft=startScroll-dx;
    });
    const finish=e=>{
      if(!dragging)return;
      dragging=false;rail.classList.remove('is-dragging');rail.releasePointerCapture?.(e.pointerId);
      if(moved)scrollToFrame(closestIndex());
    };
    rail.addEventListener('pointerup',finish);
    rail.addEventListener('pointercancel',finish);
  }
  setGalleryActive(0);

  // Activation configurator: names and micro-transition layered over existing boot logic.
  const swatches=document.querySelector('.swatches');
  const stage=document.getElementById('stage');
  const note=document.getElementById('activateNote');
  let config=document.querySelector('.activation-config');
  let finishName=document.getElementById('finishName');
  let finishDesc=document.getElementById('finishDesc');
  const finishes={
    red:{name:'SIGNAL RED',desc:'Фирменная красная световая подпись.'},
    green:{name:'VOLT GREEN',desc:'Холодный электрический зелёный акцент.'},
    stealth:{name:'STEALTH BLACK',desc:'Монохромный режим без лишнего блеска.'}
  };
  if(swatches&&!config){
    config=document.createElement('div');
    config.className='activation-config';
    config.setAttribute('aria-live','polite');
    const label=document.createElement('small');
    label.textContent='CONFIG / LIGHT SIGNATURE';
    finishName=document.createElement('strong');
    finishName.id='finishName';
    finishDesc=document.createElement('span');
    finishDesc.id='finishDesc';
    config.append(label,finishName,finishDesc);
    swatches.after(config);
  }
  const applyFinish=(key,{announce=true}={})=>{
    const finish=finishes[key]||finishes.red;
    if(finishName)finishName.textContent=finish.name;
    if(finishDesc)finishDesc.textContent=finish.desc;
    if(stage&&!reduceMotion){
      stage.classList.remove('color-shifting');
      void stage.offsetWidth;
      stage.classList.add('color-shifting');
      setTimeout(()=>stage.classList.remove('color-shifting'),420);
    }
    if(announce&&note){
      note.textContent=stage?.classList.contains('stage-live')?`${finish.name}: световой характер обновлён.`:'Выбран световой характер. Система ожидает запуска.';
    }
  };
  document.querySelectorAll('.sw').forEach(sw=>sw.addEventListener('click',()=>applyFinish(sw.dataset.color)));
  applyFinish(document.querySelector('.sw.active')?.dataset.color||'red',{announce:false});
})();
