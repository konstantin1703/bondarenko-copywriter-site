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
