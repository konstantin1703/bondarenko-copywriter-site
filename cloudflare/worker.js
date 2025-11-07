/**
 * Cloudflare Worker that proxies Matomo Live API and serves a tiny widget UI.
 * Secrets: MATOMO_URL, MATOMO_TOKEN, MATOMO_SITE_ID
 */
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === "/live") {
      const qs = new URLSearchParams({
        module: "API",
        method: "Live.getLastVisitsDetails",
        idSite: env.MATOMO_SITE_ID,
        period: url.searchParams.get("period") || "day",
        date: url.searchParams.get("date") || "today",
        format: "JSON",
        token_auth: env.MATOMO_TOKEN,
        countVisitorsToFetch: url.searchParams.get("limit") || "20",
      });
      const target = `${env.MATOMO_URL}?${qs.toString()}`;
      const r = await fetch(target, { headers: { "Accept": "application/json" } });
      const data = await r.text();
      return new Response(data, {
        headers: {
          "content-type": "application/json; charset=UTF-8",
          "access-control-allow-origin": "*",
        }
      });
    }
    if (url.pathname === "/widget") {
      const html = `<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Live</title>
<style>
*{box-sizing:border-box} body{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;margin:0;padding:12px;background:#0b0b0b;color:#e6e6e6}
.card{background:#161616;border:1px solid #222;border-radius:14px;padding:12px;margin:8px 0}
.h{display:flex;gap:8px;align-items:center;justify-content:space-between}
.badge{font-size:12px;padding:2px 8px;border:1px solid #333;border-radius:999px}
.small{opacity:.8;font-size:12px}
</style></head>
<body>
<div class="h">
  <div><strong>Live Visitors</strong></div>
  <div class="badge" id="count">–</div>
</div>
<div id="list"></div>
<script type="module">
async function load(){
  const res = await fetch('/live?limit=25');
  const data = await res.json();
  document.getElementById('count').textContent = data.length;
  const list = document.getElementById('list'); list.innerHTML='';
  for (const v of data){
    const el = document.createElement('div'); el.className='card';
    const ref = v.referrerTypeName || 'Direct';
    const ua = (v.deviceType || '') + ' ' + (v.operatingSystem || '');
    el.innerHTML = '<div><strong>'+(v.country || '—')+'</strong> • '+ref+'</div>' +
                   '<div class="small">'+ua+' • '+(v.actionDetails?.[0]?.pageTitle||v.lastActionDateTime||'')+'</div>';
    list.appendChild(el);
  }
}
load(); setInterval(load, 8000);
</script>
</body></html>`;
      return new Response(html, { headers: { "content-type": "text/html; charset=UTF-8" } });
    }
    return new Response("OK", { status: 200 });
  }
}