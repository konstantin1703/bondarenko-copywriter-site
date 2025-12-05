/**
 * Auto-create/update common Matomo Goals via HTTP API.
 * Usage: MATOMO_URL=... MATOMO_TOKEN=... MATOMO_SITE_ID=... node scripts/matomo_auto_goals.js
 */
import { request } from "undici";

const MATOMO_URL = process.env.MATOMO_URL;
const TOKEN = process.env.MATOMO_TOKEN;
const SITE_ID = process.env.MATOMO_SITE_ID;

if (!MATOMO_URL || !TOKEN || !SITE_ID) {
  console.error("Missing MATOMO_URL / MATOMO_TOKEN / MATOMO_SITE_ID");
  process.exit(1);
}

const goals = [
  // Destination URL goals
  { name: "View Pricing", matchAttribute: "url", patternType: "contains", pattern: "/pricing" },
  { name: "Start Checkout", matchAttribute: "url", patternType: "contains", pattern: "/checkout" },
  { name: "Thank You", matchAttribute: "url", patternType: "contains", pattern: "/thank-you" },
  // Event goals (tracked via _paq.push(['trackEvent', ...]))
  { name: "Form Submit (Contact)", eventCategory: "form", eventAction: "submit", eventName: "contact" },
  { name: "Download", eventCategory: "download", eventAction: "click" },
  { name: "CTA Click", eventCategory: "cta", eventAction: "click" },
];

async function call(method, params) {
  const url = new URL(MATOMO_URL);
  url.searchParams.set("module", "API");
  url.searchParams.set("format", "JSON");
  url.searchParams.set("method", method);
  url.searchParams.set("token_auth", TOKEN);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, String(v));
  const res = await request(url.toString(), { method: "GET" });
  const body = await res.body.json();
  return body;
}

async function getExistingGoals() {
  const res = await call("Goals.getGoals", { idSite: SITE_ID });
  const index = new Map();
  (res || []).forEach(g => index.set(g.name, g));
  return index;
}

async function ensureGoal(goal) {
  const existing = await getExistingGoals();
  if (existing.has(goal.name)) {
    console.log(`✓ Goal exists: ${goal.name}`);
    return existing.get(goal.name);
  }
  // Create
  let params = { idSite: SITE_ID, name: goal.name };
  if (goal.pattern) {
    params.matchAttribute = goal.matchAttribute || "url";
    params.pattern = goal.pattern;
    params.patternType = goal.patternType || "contains";
    params.caseSensitive = 0;
  } else if (goal.eventCategory) {
    params.matchAttribute = "event";
    params.pattern = JSON.stringify({
      category: goal.eventCategory,
      action: goal.eventAction || "*",
      name: goal.eventName || "*",
    });
    params.patternType = "exact";
  } else {
    throw new Error("Unsupported goal definition: " + goal.name);
  }
  const created = await call("Goals.addGoal", params);
  console.log(`+ Created goal: ${goal.name}`, created);
  return created;
}

(async () => {
  console.log("Creating/updating Matomo Goals...");
  for (const g of goals) {
    try {
      await ensureGoal(g);
    } catch (e) {
      console.error("Failed for goal:", g.name, e?.stack || e);
    }
  }
  console.log("Done.");
})();