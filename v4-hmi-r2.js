(()=>{'use strict';
const dash=document.getElementById('dash');
if(!dash)return;

const energyStates={
  road:{power:62,regen:56},
  attack:{power:94,regen:24},
  range:{power:42,regen:82}
};

const syncEnergy=(mode)=>{
  const state=energyStates[mode];
  if(!state)return;
  dash.style.setProperty('--power-angle',`${state.power*2.7}deg`);
  dash.style.setProperty('--power-half',`${state.power/2}%`);
  dash.style.setProperty('--regen-half',`${state.regen/2}%`);
};

document.querySelectorAll('.modes button').forEach(btn=>{
  btn.addEventListener('click',()=>syncEnergy(btn.dataset.mode));
});

syncEnergy(dash.dataset.mode||'road');
})();