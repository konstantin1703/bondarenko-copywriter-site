(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const sections = [...document.querySelectorAll('#r1, #performance, #design, #material, #system, #finale')];
  const navLinks = [...document.querySelectorAll('.desktop-nav a[href^="#"]')];

  const setActiveNav = (id) => {
    navLinks.forEach((link) => {
      const active = link.getAttribute('href') === `#${id}`;
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  };

  if ('IntersectionObserver' in window && sections.length) {
    const navObserver = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (visible?.target?.id) setActiveNav(visible.target.id);
    }, {
      rootMargin: '-28% 0px -56% 0px',
      threshold: [0, .12, .3, .5]
    });
    sections.forEach((section) => navObserver.observe(section));
  }

  const inviewTargets = document.querySelectorAll('.cinema, .detail, .system, .finale');
  if ('IntersectionObserver' in window) {
    const visualObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-inview');
        observer.unobserve(entry.target);
      });
    }, { threshold: .14, rootMargin: '0px 0px -8% 0px' });
    inviewTargets.forEach((el) => visualObserver.observe(el));
  } else {
    inviewTargets.forEach((el) => el.classList.add('is-inview'));
  }

  /* Desktop-only image drift: enough depth to feel cinematic, never enough to fight the copy. */
  if (!reduceMotion && window.matchMedia('(min-width: 981px) and (pointer: fine)').matches) {
    const cinema = document.querySelector('.cinema');
    const cinemaImage = document.querySelector('.cinema__image');
    let ticking = false;

    const render = () => {
      ticking = false;
      if (!cinema || !cinemaImage) return;
      const rect = cinema.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;
      const progress = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
      const y = Math.max(-18, Math.min(18, (progress - .5) * 28));
      cinemaImage.style.backgroundPositionY = `calc(54% + ${y}px)`;
    };

    window.addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(render);
    }, { passive: true });
    render();
  }
})();
