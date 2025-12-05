
// Analytics helper for Matomo
(function(){
  const DEBUG_MODE = true;
  const MATOMO_URL = "https://bondarenko.matomo.cloud/";
  const SITE_ID = "1";

  function ensureInit(){
    if (window._paq && window._paq.__inited) return;
    window._paq = window._paq || [];
    window._paq.push(["trackPageView"]);
    window._paq.push(["enableLinkTracking"]);
    (function() {
      var u = MATOMO_URL;
      window._paq.push(["setTrackerUrl", u + "matomo.php"]);
      window._paq.push(["setSiteId", SITE_ID]);
      var d=document,g=d.createElement("script"),s=d.getElementsByTagName("script")[0];
      g.async=true; g.src="https://cdn.matomo.cloud/bondarenko.matomo.cloud/matomo.js"; s.parentNode.insertBefore(g,s);
    })();
    window._paq.__inited = true;
    if (DEBUG_MODE) console.log("[Matomo] inited");
  }

  function trackEvent(category, action, name){
    try{
      ensureInit();
      window._paq.push(["trackEvent", category, action, name || ""]);
      if (DEBUG_MODE) console.debug("[Matomo event]", {category, action, name});
    }catch(e){
      if (DEBUG_MODE) console.warn("[Matomo] track error", e);
    }
  }

  // Expose
  window.analyticsTrack = trackEvent;

  // Bind clicks for email / telegram
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[href]");
    if (!a) return;
    const href = a.getAttribute("href") || "";
    if (href.startsWith("mailto:")) trackEvent("Contact","Click","Email");
    if (href.includes("t.me") || href.includes("telegram.me") || href.includes("telegram.org")) trackEvent("Contact","Click","Telegram");
  }, true);

  // Bind impressions for sections
  const observed = new Set();
  function ioTrack(id, label){
    const el = document.getElementById(id);
    if (!el) return;
    const io = new IntersectionObserver((entries)=>{
      entries.forEach(en=>{
        if (en.isIntersecting && !observed.has(id)){
          observed.add(id);
          trackEvent("Scroll","View Section", label);
          io.disconnect();
        }
      });
    }, {threshold: 0.3});
    io.observe(el);
  }
  document.addEventListener("DOMContentLoaded", ()=>{
    ioTrack("reviews-list","Reviews");
    ioTrack("portfolio","Portfolio");
  });
})(); 
