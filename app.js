(() => {
  'use strict';

  const root = document.documentElement;
  const body = document.body;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  window.addEventListener('load', () => {
    window.setTimeout(() => $('#boot')?.classList.add('is-done'), reduceMotion ? 0 : 900);
  });

  const header = $('#siteHeader');
  const progress = $('#scrollProgress');
  let ticking = false;

  const updateScroll = () => {
    const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    const p = Math.min(1, window.scrollY / max);
    if (progress) progress.style.transform = `scaleX(${p})`;
    header?.classList.toggle('is-scrolled', window.scrollY > 16);

    const bike = $('#bikeSvg');
    if (bike && !reduceMotion) {
      const y = Math.min(22, window.scrollY * .025);
      bike.style.setProperty('--bike-y', `${y}px`);
      $$('.wheel').forEach((wheel) => {
        wheel.style.transform = `rotate(${window.scrollY * .12}deg)`;
      });
    }
    ticking = false;
  };

  window.addEventListener('scroll', () => {
    if (!ticking) { requestAnimationFrame(updateScroll); ticking = true; }
  }, { passive: true });
  updateScroll();

  const reveals = $$('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .12, rootMargin: '0px 0px -5% 0px' });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-visible'));
  }

  const menuToggle = $('#menuToggle');
  const mobileNav = $('#mobileNav');
  const setMenu = (open) => {
    menuToggle?.setAttribute('aria-expanded', String(open));
    mobileNav?.setAttribute('aria-hidden', String(!open));
    mobileNav?.classList.toggle('is-open', open);
    body.classList.toggle('menu-open', open);
  };
  menuToggle?.addEventListener('click', () => setMenu(menuToggle.getAttribute('aria-expanded') !== 'true'));
  $$('#mobileNav a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
  window.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

  const cursor = $('#cursor');
  const cursorDot = $('#cursorDot');
  if (window.matchMedia('(hover:hover)').matches && cursor && cursorDot) {
    let cx = innerWidth / 2, cy = innerHeight / 2, tx = cx, ty = cy;
    body.classList.add('cursor-ready');
    window.addEventListener('pointermove', (e) => { tx = e.clientX; ty = e.clientY; cursorDot.style.transform = `translate(${tx}px, ${ty}px) translate(-50%,-50%)`; });
    const loop = () => {
      cx += (tx - cx) * .16; cy += (ty - cy) * .16;
      cursor.style.transform = `translate(${cx}px, ${cy}px) translate(-50%,-50%)`;
      requestAnimationFrame(loop);
    };
    loop();
    $$('a, button').forEach((el) => {
      el.addEventListener('pointerenter', () => body.classList.add('cursor-link'));
      el.addEventListener('pointerleave', () => body.classList.remove('cursor-link'));
    });
  }

  const bikeStage = $('#bikeStage');
  if (bikeStage && !reduceMotion && window.matchMedia('(hover:hover)').matches) {
    bikeStage.addEventListener('pointermove', (e) => {
      const r = bikeStage.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5;
      const y = (e.clientY - r.top) / r.height - .5;
      root.style.setProperty('--bike-ry', `${x * 4.5}deg`);
      root.style.setProperty('--bike-rx', `${-y * 3}deg`);
    });
    bikeStage.addEventListener('pointerleave', () => {
      root.style.setProperty('--bike-ry', '0deg'); root.style.setProperty('--bike-rx', '0deg');
    });
  }

  const powerValue = $('#powerValue');
  const powerSection = $('.power');
  if (powerValue && powerSection) {
    let ran = false;
    const powerObserver = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !ran) {
        ran = true;
        if (reduceMotion) { powerValue.textContent = '210'; return; }
        const start = performance.now();
        const dur = 1400;
        const animate = (now) => {
          const t = Math.min(1, (now - start) / dur);
          const eased = 1 - Math.pow(1 - t, 4);
          powerValue.textContent = String(Math.round(210 * eased));
          if (t < 1) requestAnimationFrame(animate);
        };
        requestAnimationFrame(animate);
      }
    }, { threshold: .35 });
    powerObserver.observe(powerSection);
  }

  const modes = {
    road: { speed: 118, battery: '78%', regen: 'MED', range: '241 KM' },
    attack: { speed: 184, battery: '62%', regen: 'LOW', range: '168 KM' },
    range: { speed: 92, battery: '84%', regen: 'HIGH', range: '302 KM' }
  };
  $$('.mode').forEach((btn) => {
    btn.addEventListener('click', () => {
      $$('.mode').forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      const key = btn.dataset.mode;
      const d = modes[key];
      $('#dashMode').textContent = key.toUpperCase();
      $('#dashSpeed').textContent = d.speed;
      $('#dashBattery').textContent = d.battery;
      $('#dashRegen').textContent = d.regen;
      $('#dashRange').textContent = d.range;
    });
  });

  const finishes = {
    obsidian: { color: '#151515', accent: '#ff4a2f', name: 'OBSIDIAN / 01' },
    silver: { color: '#9a9b98', accent: '#cfd0cc', name: 'LIQUID SILVER / 02' },
    signal: { color: '#b82014', accent: '#ff3c25', name: 'SIGNAL RED / 03' }
  };
  $$('.swatch').forEach((btn) => {
    btn.addEventListener('click', () => {
      const f = finishes[btn.dataset.finish];
      $$('.swatch').forEach((b) => { b.classList.remove('is-active'); b.setAttribute('aria-pressed', 'false'); });
      btn.classList.add('is-active'); btn.setAttribute('aria-pressed', 'true');
      root.style.setProperty('--bike-color', f.color);
      root.style.setProperty('--accent', f.accent);
      $('#finishName').textContent = f.name;
    });
  });

  const ignite = $('#ignite');
  const ignitionLayer = $('#ignitionLayer');
  const stopIgnition = () => {
    ignitionLayer?.classList.remove('is-on');
    body.classList.remove('ignited');
    ignite?.focus({ preventScroll: true });
  };
  ignite?.addEventListener('click', () => {
    ignitionLayer?.classList.add('is-on'); body.classList.add('ignited');
    window.setTimeout(stopIgnition, reduceMotion ? 400 : 2400);
  });
  ignitionLayer?.addEventListener('click', stopIgnition);

  const canvas = $('#signalCanvas');
  if (canvas && !reduceMotion) {
    const ctx = canvas.getContext('2d', { alpha: true });
    let dpr = Math.min(2, devicePixelRatio || 1);
    let w = 0, h = 0;
    const points = [];
    let mouse = { x: .52, y: .45 };

    const resize = () => {
      const r = canvas.getBoundingClientRect(); w = r.width; h = r.height;
      canvas.width = Math.max(1, Math.floor(w * dpr)); canvas.height = Math.max(1, Math.floor(h * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      points.length = 0;
      const count = Math.max(22, Math.floor(w / 48));
      for (let i = 0; i < count; i++) points.push({ x: Math.random()*w, y: Math.random()*h, vx:(Math.random()-.5)*.18, vy:(Math.random()-.5)*.12, a:.08+Math.random()*.18 });
    };
    resize();
    window.addEventListener('resize', resize, { passive:true });
    $('.hero')?.addEventListener('pointermove', (e) => { const r = canvas.getBoundingClientRect(); mouse = { x:(e.clientX-r.left)/r.width, y:(e.clientY-r.top)/r.height }; });

    const draw = () => {
      ctx.clearRect(0,0,w,h);
      const mx = mouse.x*w, my = mouse.y*h;
      for (let i=0;i<points.length;i++) {
        const p = points[i]; p.x += p.vx; p.y += p.vy;
        if (p.x<0) p.x=w; if (p.x>w) p.x=0; if (p.y<0) p.y=h; if (p.y>h) p.y=0;
        ctx.fillStyle = `rgba(255,255,255,${p.a})`; ctx.fillRect(p.x,p.y,1,1);
        const dm = Math.hypot(p.x-mx,p.y-my);
        if (dm<170) { ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(mx,my); ctx.strokeStyle=`rgba(255,74,47,${(1-dm/170)*.09})`; ctx.stroke(); }
        for (let j=i+1;j<points.length;j++) {
          const q=points[j], d=Math.hypot(p.x-q.x,p.y-q.y);
          if (d<120) { ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(q.x,q.y); ctx.strokeStyle=`rgba(255,255,255,${(1-d/120)*.035})`; ctx.stroke(); }
        }
      }
      requestAnimationFrame(draw);
    };
    requestAnimationFrame(draw);
  }
})();
