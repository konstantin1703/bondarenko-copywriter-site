(() => {
  'use strict';

  const boot = document.getElementById('boot');
  const header = document.getElementById('siteHeader');
  const progress = document.getElementById('scrollProgress');
  const cursor = document.getElementById('cursor');
  const menuToggle = document.getElementById('menuToggle');
  const mobileNav = document.getElementById('mobileNav');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  window.addEventListener('load', () => {
    window.setTimeout(() => boot?.classList.add('is-gone'), reduceMotion ? 0 : 650);
  });

  const onScroll = () => {
    const y = window.scrollY;
    header?.classList.toggle('is-scrolled', y > 24);
    const max = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    if (progress) progress.style.transform = `scaleX(${Math.min(y / max, 1)})`;
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  if (cursor && window.matchMedia('(pointer:fine)').matches) {
    let tx = window.innerWidth / 2, ty = window.innerHeight / 2;
    let x = tx, y = ty;
    window.addEventListener('pointermove', (e) => { tx = e.clientX; ty = e.clientY; }, { passive: true });
    const renderCursor = () => {
      x += (tx - x) * .18;
      y += (ty - y) * .18;
      cursor.style.left = `${x}px`;
      cursor.style.top = `${y}px`;
      requestAnimationFrame(renderCursor);
    };
    renderCursor();
    document.querySelectorAll('a,button').forEach((el) => {
      el.addEventListener('mouseenter', () => cursor.classList.add('is-hot'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('is-hot'));
    });
  }

  const setNav = (open) => {
    document.body.classList.toggle('nav-open', open);
    mobileNav?.classList.toggle('is-open', open);
    mobileNav?.setAttribute('aria-hidden', String(!open));
    menuToggle?.setAttribute('aria-expanded', String(open));
  };
  menuToggle?.addEventListener('click', () => setNav(!document.body.classList.contains('nav-open')));
  mobileNav?.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setNav(false)));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setNav(false); });

  const reveal = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const obs = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: .12, rootMargin: '0px 0px -6% 0px' });
    reveal.forEach((el) => obs.observe(el));
  } else {
    reveal.forEach((el) => el.classList.add('is-visible'));
  }

  const counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window) {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = Number(el.dataset.count || 0);
        const duration = reduceMotion ? 10 : 900;
        const start = performance.now();
        const tick = (now) => {
          const p = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - p, 3);
          el.textContent = String(Math.round(target * eased));
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        observer.unobserve(el);
      });
    }, { threshold: .5 });
    counters.forEach((el) => counterObserver.observe(el));
  } else {
    counters.forEach((el) => { el.textContent = el.dataset.count || '0'; });
  }

  const modes = {
    road: { speed: '084', battery: '78%', range: '214 км', regen: 'СРЕДНЯЯ', power: '62%', accent: '#ff2b17' },
    attack: { speed: '146', battery: '61%', range: '128 км', regen: 'НИЗКАЯ', power: '94%', accent: '#ff3b21' },
    range: { speed: '062', battery: '84%', range: '286 км', regen: 'ВЫСОКАЯ', power: '42%', accent: '#d8ff54' }
  };
  const dash = document.getElementById('dash');
  const speed = document.getElementById('speedValue');
  const battery = document.getElementById('batteryValue');
  const range = document.getElementById('rangeValue');
  const regen = document.getElementById('regenValue');
  const powerBar = document.getElementById('powerBar');
  document.querySelectorAll('.mode').forEach((button) => {
    button.addEventListener('click', () => {
      const state = modes[button.dataset.mode];
      if (!state) return;
      document.querySelectorAll('.mode').forEach((b) => {
        const active = b === button;
        b.classList.toggle('active', active);
        b.setAttribute('aria-pressed', String(active));
      });
      if (speed) speed.textContent = state.speed;
      if (battery) battery.textContent = state.battery;
      if (range) range.textContent = state.range;
      if (regen) regen.textContent = state.regen;
      if (powerBar) powerBar.style.width = state.power;
      dash?.style.setProperty('--dash-accent', state.accent);
    });
  });

  const clock = document.getElementById('dashClock');
  const updateClock = () => {
    const now = new Date();
    if (clock) clock.textContent = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  };
  updateClock();
  window.setInterval(updateClock, 15000);

  const ignite = document.getElementById('ignite');
  const finale = document.querySelector('.finale');
  const status = document.getElementById('igniteStatus');
  ignite?.addEventListener('click', () => {
    const live = !finale?.classList.contains('is-live');
    finale?.classList.toggle('is-live', live);
    if (status) status.textContent = live ? 'СИСТЕМА АКТИВНА / READY TO MOVE' : 'СИСТЕМА ГОТОВА / STANDBY';
    const label = ignite.querySelector('span');
    if (label) label.textContent = live ? 'СИСТЕМА АКТИВНА' : 'ЗАПУСТИТЬ / IGNITE';
  });

  if (!reduceMotion) {
    const heroMedia = document.querySelector('.hero__media');
    const finaleMedia = document.querySelector('.finale__media');
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      if (heroMedia && y < window.innerHeight * 1.2) heroMedia.style.transform = `scale(${Math.max(1, 1.035 - y * .000018)}) translateY(${y * .025}px)`;
      if (finaleMedia) {
        const rect = finaleMedia.parentElement.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) finaleMedia.style.backgroundPositionY = `${52 + (window.innerHeight - rect.top) * .008}%`;
      }
    }, { passive: true });
  }
})();
