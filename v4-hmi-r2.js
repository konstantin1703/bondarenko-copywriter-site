(()=>{'use strict';
const dash=document.getElementById('dash');
if(!dash)return;

const energyStates={
  road:{power:62,regen:48},
  attack:{power:94,regen:18},
  range:{power:42,regen:88}
};

const powerMeter=dash.querySelector('.power');

const syncEnergy=(mode)=>{
  const state=energyStates[mode];
  if(!state)return;

  dash.style.setProperty('--power-angle',`${state.power*2.7}deg`);
  dash.style.setProperty('--power-half',`${state.power*.5}%`);
  dash.style.setProperty('--regen-half',`${state.regen*.5}%`);

  if(powerMeter){
    powerMeter.setAttribute('aria-label',`Рекуперация ${state.regen} процентов, мощность ${state.power} процентов`);
  }
};

const observer=new MutationObserver((mutations)=>{
  if(mutations.some(m=>m.type==='attributes'&&m.attributeName==='data-mode')){
    syncEnergy(dash.dataset.mode||'road');
  }
});
observer.observe(dash,{attributes:true,attributeFilter:['data-mode']});

syncEnergy(dash.dataset.mode||'road');
})();