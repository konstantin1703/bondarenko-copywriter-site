/**
 * Include this early in your app (e.g., in <head> for static sites).
 * It injects Matomo tracker and adds simple click & form listeners.
 */
(function(){
  var _paq = window._paq = window._paq || [];
  // Optional: enable link tracking & heatmap if plugin exists
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  // Respect DNT (optional)
  _paq.push(['setDoNotTrack', true]);

  // Replace with your Matomo settings
  var u = window.MATOMO_BASE_URL || "{{MATOMO_URL}}/";
  var idSite = window.MATOMO_SITE_ID || "{{MATOMO_SITE_ID}}";
  _paq.push(['setTrackerUrl', u+'matomo.php']);
  _paq.push(['setSiteId', idSite]);

  var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
  g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);

  // Lightweight event hooks
  function closestSelector(el){
    if (!el) return '';
    if (el.id) return '#'+el.id;
    if (el.className && typeof el.className === 'string'){
      const cls = el.className.split(' ').filter(Boolean).slice(0,3).join('.');
      if (cls) return el.tagName.toLowerCase()+'.'+cls;
    }
    return el.tagName ? el.tagName.toLowerCase() : '';
  }

  document.addEventListener('click', function(ev){
    try {
      var t = ev.target;
      var sel = closestSelector(t);
      _paq.push(['trackEvent', 'cta', 'click', sel]);
    } catch (e){}
  }, { capture: true });

  document.addEventListener('submit', function(ev){
    try {
      var f = ev.target;
      var name = f.getAttribute('name') || f.getAttribute('id') || 'form';
      _paq.push(['trackEvent', 'form', 'submit', name]);
    } catch (e){}
  }, { capture: true });
})();