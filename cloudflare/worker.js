export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const cors = {"access-control-allow-origin":"*","access-control-allow-methods":"GET,POST,OPTIONS","access-control-allow-headers":"content-type"};
    if (req.method === "OPTIONS") return new Response("", { headers: cors });

    if (url.pathname === "/live") {
      const limit = url.searchParams.get("limit") || "10";
      const liveUrl = `${env.MATOMO_URL}index.php?module=API&method=Live.getLastVisitsDetails&idSite=${env.MATOMO_SITE_ID}&period=day&date=today&format=JSON&token_auth=${env.MATOMO_TOKEN}&filter_limit=${limit}`;
      const r = await fetch(liveUrl, { headers: { "accept":"application/json" } });
      const j = await r.json();
      return new Response(JSON.stringify(j), { headers: { "content-type":"application/json; charset=UTF-8", ...cors } });
    }

    if (url.pathname === "/widget") {
      const html = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Live</title>
      <style>body{background:#0b0d0f;color:#eaeaea;font:14px/1.4 system-ui;margin:0;padding:16px}.c{max-width:820px;margin:0 auto}.item{border:1px solid #222;border-radius:12;padding:12px;margin:8px 0}</style>
      </head><body><div class="c"><h3>Matomo Live</h3><div id="root"></div><script>
      async function load(){const r=await fetch('/live');const j=await r.json();const root=document.getElementById('root');root.innerHTML=j.map(v=>'<div class=item><b>'+ (v.country||'—') +'</b> • '+(v.referrerTypeName||'Direct')+'<div style=opacity:.8;font-size:12px>'+(v.actionDetails?.[0]?.pageTitle||'')+'</div></div>').join('')}
      load();setInterval(load,8000);
      </script></div></body></html>`;
      return new Response(html, { headers: { "content-type":"text/html; charset=UTF-8", ...cors } });
    }

    if (url.pathname === "/reviews") {
      if (req.method === "GET") {
        const raw = await env.REVIEWS.get("items");
        const items = raw ? JSON.parse(raw) : [];
        const avg = items.length ? items.reduce((a,c)=>a+(Number(c.rating)||5),0)/items.length : 5;
        return new Response(JSON.stringify({ avg: Math.round(avg*10)/10, count: items.length, items: items.slice(-20).reverse() }), { headers: { "content-type":"application/json; charset=UTF-8", ...cors } });
      }
      if (req.method === "POST") {
        const body = await req.json();
        const item = { name: (body.name||"Гость").slice(0,48), text: (body.text||"").slice(0,1000), rating: Number(body.rating)||5, at: new Date().toISOString() };
        const raw = await env.REVIEWS.get("items");
        const items = raw ? JSON.parse(raw) : [];
        items.push(item);
        await env.REVIEWS.put("items", JSON.stringify(items));
        return new Response(JSON.stringify({ ok:true }), { headers: { "content-type":"application/json; charset=UTF-8", ...cors } });
      }
      return new Response(JSON.stringify({error:"method_not_allowed"}), { status:405, headers: { "content-type":"application/json; charset=UTF-8", ...cors } });
    }

    return new Response("OK", { status: 200, headers: cors });
  }
}
