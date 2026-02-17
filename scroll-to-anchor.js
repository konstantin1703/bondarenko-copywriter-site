/**
 * Scroll to anchor helper
 * When navigating from subpages (blog/portfolio) back to main page with hash
 * e.g. ../index.html#portfolio
 */
(function() {
  'use strict';

  function scrollToHash() {
    const hash = window.location.hash;
    if (!hash) return;

    // Small delay to let page render
    setTimeout(function() {
      const target = document.querySelector(hash);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  }

  // On page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scrollToHash);
  } else {
    scrollToHash();
  }

  // On hash change (for SPA-like navigation)
  window.addEventListener('hashchange', scrollToHash);
})();
