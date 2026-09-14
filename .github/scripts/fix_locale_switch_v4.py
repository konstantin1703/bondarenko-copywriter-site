from pathlib import Path

loc = Path('v4-locale-v1.js')
s = loc.read_text(encoding='utf-8')

old_set = """  const setLanguage=(lang,{persist=true,url=true}={})=>{\n    activeLang=lang==='en'?'en':'ru';document.documentElement.lang=activeLang;\n    if(persist)try{localStorage.setItem('vanta-lang',activeLang)}catch{}\n    if(url){const u=new URL(location.href);u.searchParams.set('lang',activeLang);history.replaceState(null,'',u);}\n    translateTree(document);localizeCountryRows();setMeta();updateSwitches();\n    window.dispatchEvent(new CustomEvent('vanta:languagechange',{detail:{lang:activeLang}}));\n  };\n  const makeSwitch=cls=>{const wrap=document.createElement('div');wrap.className=`lang-switch ${cls}`;wrap.setAttribute('aria-label','Language / Язык');wrap.innerHTML='<button type=\"button\" data-lang=\"ru\" aria-pressed=\"true\">RU</button><button type=\"button\" data-lang=\"en\" aria-pressed=\"false\">EN</button>';wrap.addEventListener('click',e=>{const b=e.target.closest('button[data-lang]');if(b)setLanguage(b.dataset.lang);});return wrap;};\n  document.getElementById('header')?.appendChild(makeSwitch('header-lang'));\n  document.getElementById('mobileMenu')?.appendChild(makeSwitch('mobile-lang'));\n"""

new_set = """  const setLanguage=(lang,{persist=true,url=true}={})=>{\n    activeLang=lang==='en'?'en':'ru';\n    document.documentElement.lang=activeLang;\n    if(persist)try{localStorage.setItem('vanta-lang',activeLang)}catch{}\n    /* Translate first. A History API quirk must never block the visible language change. */\n    translateTree(document);localizeCountryRows();setMeta();updateSwitches();\n    if(url)try{const u=new URL(location.href);u.searchParams.set('lang',activeLang);history.replaceState(history.state,'',u.pathname+u.search+u.hash)}catch{}\n    window.dispatchEvent(new CustomEvent('vanta:languagechange',{detail:{lang:activeLang}}));\n  };\n  const makeSwitch=cls=>{const wrap=document.createElement('div');wrap.className=`lang-switch ${cls}`;wrap.setAttribute('aria-label','Language / Язык');wrap.innerHTML='<button type=\"button\" data-lang=\"ru\" aria-pressed=\"true\">RU</button><button type=\"button\" data-lang=\"en\" aria-pressed=\"false\">EN</button>';return wrap;};\n  document.getElementById('header')?.appendChild(makeSwitch('header-lang'));\n  document.getElementById('mobileMenu')?.appendChild(makeSwitch('mobile-lang'));\n\n  const switchLanguage=target=>{\n    setLanguage(target);\n    requestAnimationFrame(()=>{\n      const hero=(document.querySelector('.hero-white')?.textContent||'').trim();\n      const ok=target==='en'?hero==='Silence':hero==='Тишина';\n      if(!ok){\n        const u=new URL(location.href);\n        u.searchParams.set('lang',target);\n        location.replace(u.href);\n      }\n    });\n  };\n  document.addEventListener('click',e=>{\n    const b=e.target.closest?.('.lang-switch button[data-lang]');\n    if(!b)return;\n    e.preventDefault();\n    e.stopImmediatePropagation();\n    switchLanguage(b.dataset.lang);\n  },true);\n"""

if old_set not in s:
    raise SystemExit('locale switch anchor not found')
s = s.replace(old_set, new_set, 1)
loc.write_text(s, encoding='utf-8')

css = Path('v4-request-modal-v1.css')
c = css.read_text(encoding='utf-8')
needle = '.mobile-lang{display:none!important}'
replacement = '#header .header-lang{z-index:5!important;pointer-events:auto!important}#header .header-lang button{pointer-events:auto!important;touch-action:manipulation!important}\n.mobile-lang{display:none!important}'
if needle not in c:
    raise SystemExit('locale css anchor not found')
c = c.replace(needle, replacement, 1)
css.write_text(c, encoding='utf-8')

idx = Path('index.html')
i = idx.read_text(encoding='utf-8')
i = i.replace('v4-locale-v1.js?v=3', 'v4-locale-v1.js?v=4', 1)
i = i.replace('v4-request-modal-v1.css?v=3', 'v4-request-modal-v1.css?v=4', 1)
idx.write_text(i, encoding='utf-8')
print('locale switch v4 patch ready')
