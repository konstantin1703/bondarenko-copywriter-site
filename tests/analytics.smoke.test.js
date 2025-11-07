import assert from "node:assert";
import { request } from "undici";

const MATOMO_URL = process.env.MATOMO_URL;
const TOKEN = process.env.MATOMO_TOKEN;
const SITE_ID = process.env.MATOMO_SITE_ID;

async function pingLive() {
  const url = new URL(MATOMO_URL);
  url.searchParams.set("module", "API");
  url.searchParams.set("method", "Live.getLastVisitsDetails");
  url.searchParams.set("idSite", SITE_ID);
  url.searchParams.set("period", "day");
  url.searchParams.set("date", "today");
  url.searchParams.set("format", "JSON");
  url.searchParams.set("token_auth", TOKEN);
  const res = await request(url.toString());
  assert.equal(res.statusCode, 200, "Matomo Live API should be reachable");
}

(async ()=>{
  if (MATOMO_URL && TOKEN && SITE_ID) {
    await pingLive();
    console.log("✓ Matomo Live reachable");
  } else {
    console.warn("Skipping live API test (missing env)");
  }
})();