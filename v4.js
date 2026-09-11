(()=>{'use strict';
const header=document.getElementById('header');
const progress=document.getElementById('progress');
const menu=document.getElementById('menu');
const mobile=document.getElementById('mobileMenu');
const updateScroll=()=>{const y=window.scrollY;const max=Math.max(document.documentElement.scrollHeight-innerHeight,1);header.classList.toggle('scrolled',y>18);progress.style.transform=`scaleX(${Math.min(y/max,1)})`};
updateScroll();addEventListener('scroll',updateScroll,{passive:true});
menu.addEventListener('click',()=>{const open=mobile.classList.toggle('open');menu.classList.toggle('open',open);menu.setAttribute('aria-expanded',open);mobile.setAttribute('aria-hidden',!open)});
mobile.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{mobile.classList.remove('open');menu.classList.remove('open');menu.setAttribute('aria-expanded','false');mobile.setAttribute('aria-hidden','true')}));
const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('show');io.unobserve(e.target)}}),{threshold:.1});document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
const rail=document.getElementById('rail');const shift=()=>Math.min(rail.clientWidth*.82,760);document.getElementById('prev').addEventListener('click',()=>rail.scrollBy({left:-shift(),behavior:'smooth'}));document.getElementById('next').addEventListener('click',()=>rail.scrollBy({left:shift(),behavior:'smooth'}));

const dash=document.getElementById('dash');
const speed=document.getElementById('speed');
const battery=document.getElementById('battery');
const range=document.getElementById('range');
const regen=document.getElementById('regen');
const power=document.getElementById('power');
const powerLabel=document.getElementById('powerLabel');
const modeName=document.getElementById('modeName');
const modeDesc=document.getElementById('modeDesc');
const states={
  road:{speed:'084',battery:'78%',range:'214 км',regen:'СРЕДНЯЯ',power:'62%',dial:'142deg',name:'ДОРОГА',desc:'Сбалансированный отклик'},
  attack:{speed:'146',battery:'61%',range:'128 км',regen:'НИЗКАЯ',power:'94%',dial:'232deg',name:'ТРЕК',desc:'Максимальная отдача привода'},
  range:{speed:'062',battery:'84%',range:'286 км',regen:'ВЫСОКАЯ',power:'42%',dial:'106deg',name:'ЭКО',desc:'Приоритет запаса хода'}
};
const applyMode=(key)=>{const s=states[key];if(!s)return;dash.dataset.mode=key;dash.classList.remove('dash-shift');void dash.offsetWidth;dash.classList.add('dash-shift');speed.textContent=s.speed;battery.textContent=s.battery;range.textContent=s.range;regen.textContent=s.regen;power.style.width=s.power;powerLabel.textContent=s.power;modeName.textContent=s.name;modeDesc.textContent=s.desc;dash.style.setProperty('--dial',s.dial)};
document.querySelectorAll('.modes button').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.modes button').forEach(x=>{const active=x===btn;x.classList.toggle('active',active);x.setAttribute('aria-pressed',active)});applyMode(btn.dataset.mode)}));
applyMode('road');

const clock=document.getElementById('clock');const tick=()=>clock.textContent=new Date().toLocaleTimeString('ru-RU',{hour:'2-digit',minute:'2-digit'});tick();setInterval(tick,15000);
const stage=document.getElementById('stage'),activateBtn=document.getElementById('activateBtn'),status=document.getElementById('bootStatus'),note=document.getElementById('activateNote');
activateBtn.addEventListener('click',()=>{const on=stage.classList.toggle('stage-live');status.textContent=on?'SYSTEM ACTIVE':'STANDBY';activateBtn.querySelector('span').textContent=on?'ОТКЛЮЧИТЬ DEMO':'АКТИВИРОВАТЬ R1';note.textContent=on?'Оптика и бортовая система активированы. Можно менять цветовой режим.':'Система ожидает запуска.'});
document.querySelectorAll('.sw').forEach(sw=>sw.addEventListener('click',()=>{document.querySelectorAll('.sw').forEach(x=>{const active=x===sw;x.classList.toggle('active',active);x.setAttribute('aria-pressed',active)});stage.classList.remove('color-green','color-stealth');if(sw.dataset.color==='green')stage.classList.add('color-green');if(sw.dataset.color==='stealth')stage.classList.add('color-stealth')}));
})();