/**
 * Cloudflare Worker: /api/lead
 *
 * Принимает заявки с фронта и отправляет их в Telegram.
 *
 * Secrets (wrangler secret put):
 * - TELEGRAM_TOKEN
 * - TELEGRAM_CHAT_ID
 *
 * Optional env:
 * - ALLOWED_ORIGINS (comma-separated, e.g. "https://konstantin1703.github.io,https://example.com")
 *
 * KV binding (optional but recommended):
 * - LEAD_RATELIMIT (for simple rate limiting)
 */
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_RE = /^(\+7|8|7)\d{10}$/;

function jsonResponse(body, { status = 200, corsOrigin = null } = {}) {
  const headers = new Headers({
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  });

  if (corsOrigin) {
    headers.set('Access-Control-Allow-Origin', corsOrigin);
    headers.set('Vary', 'Origin');
    headers.set('Access-Control-Allow-Credentials', 'true');
  }

  return new Response(JSON.stringify(body), { status, headers });
}

function optionsResponse({ corsOrigin = null } = {}) {
  const headers = new Headers({
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400'
  });

  if (corsOrigin) {
    headers.set('Access-Control-Allow-Origin', corsOrigin);
    headers.set('Vary', 'Origin');
    headers.set('Access-Control-Allow-Credentials', 'true');
  }

  return new Response(null, { status: 204, headers });
}

function getAllowedOrigins(env) {
  const fallback = ['https://konstantin1703.github.io'];
  const raw = (env.ALLOWED_ORIGINS || '').trim();
  if (!raw) return fallback;

  return raw
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
}

function getCorsOrigin(request, env) {
  const origin = request.headers.get('Origin');
  if (!origin) return null;

  const requestOrigin = new URL(request.url).origin;
  if (origin === requestOrigin) return origin;

  const allowed = getAllowedOrigins(env);
  return allowed.includes(origin) ? origin : null;
}

function getClientIp(request) {
  return (
    request.headers.get('CF-Connecting-IP') ||
    (request.headers.get('X-Forwarded-For') || '').split(',')[0].trim() ||
    'unknown'
  );
}

async function enforceRateLimit(env, ip) {
  if (!env.LEAD_RATELIMIT) return { ok: true };

  const key = `rl:${ip}`;
  const raw = await env.LEAD_RATELIMIT.get(key);
  const count = raw ? Number(raw) : 0;

  if (!Number.isFinite(count)) {
    await env.LEAD_RATELIMIT.put(key, '1', { expirationTtl: 60 });
    return { ok: true };
  }

  if (count >= 5) {
    return { ok: false };
  }

  await env.LEAD_RATELIMIT.put(key, String(count + 1), { expirationTtl: 60 });
  return { ok: true };
}

function normalizeString(value) {
  return typeof value === 'string' ? value.trim() : '';
}

function normalizePhone(value) {
  return normalizeString(value).replace(/[\s\-\(\)]/g, '');
}

function isValidLead({ name, email, phone, message }) {
  if (name.length < 2) return { ok: false, error: 'Имя должно быть не короче 2 символов.' };
  if (!EMAIL_RE.test(email)) return { ok: false, error: 'Некорректный email.' };
  if (!phone || !PHONE_RE.test(phone)) return { ok: false, error: 'Некорректный номер телефона.' };
  if (message.length < 10) return { ok: false, error: 'Сообщение должно быть не короче 10 символов.' };
  return { ok: true };
}

async function sendToTelegram(env, text) {
  if (!env.TELEGRAM_TOKEN || !env.TELEGRAM_CHAT_ID) {
    throw new Error('Missing TELEGRAM_TOKEN / TELEGRAM_CHAT_ID');
  }

  const baseUrl = 'https://api.telegram.org';
  const url = baseUrl + '/bot' + env.TELEGRAM_TOKEN + '/sendMessage';

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: env.TELEGRAM_CHAT_ID,
      text
    })
  });

  const data = await res.json().catch(() => null);

  if (!res.ok || !data || !data.ok) {
    const status = res.status;
    const desc = data && data.description ? data.description : 'Telegram API error';
    const err = new Error(`${status}: ${desc}`);
    err.status = 502;
    throw err;
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const corsOrigin = getCorsOrigin(request, env);

    const hasOrigin = Boolean(request.headers.get('Origin'));
    if (hasOrigin && !corsOrigin) {
      return jsonResponse(
        { ok: false, error: 'CORS: origin not allowed' },
        { status: 403, corsOrigin: null }
      );
    }

    if (request.method === 'OPTIONS') {
      return optionsResponse({ corsOrigin });
    }

    if (request.method !== 'POST') {
      return jsonResponse({ ok: false, error: 'Method not allowed' }, { status: 405, corsOrigin });
    }

    if (url.pathname !== '/api/lead') {
      return jsonResponse({ ok: false, error: 'Not found' }, { status: 404, corsOrigin });
    }

    const contentType = request.headers.get('Content-Type') || '';
    if (!contentType.includes('application/json')) {
      return jsonResponse({ ok: false, error: 'Expected application/json' }, { status: 415, corsOrigin });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return jsonResponse({ ok: false, error: 'Invalid JSON' }, { status: 400, corsOrigin });
    }

    const name = normalizeString(body.name);
    const email = normalizeString(body.email);
    const phone = normalizePhone(body.phone);
    const message = normalizeString(body.message);
    const page = normalizeString(body.page) || '(unknown)';

    // Honeypot: must be empty
    const company = normalizeString(body.company);
    if (company) {
      return jsonResponse({ ok: false, error: 'Spam detected' }, { status: 400, corsOrigin });
    }

    // Time-based quick-submit protection
    const clientTs = Number(body.client_ts);
    if (Number.isFinite(clientTs)) {
      const delta = Date.now() - clientTs;
      if (delta >= 0 && delta < 2000) {
        return jsonResponse({ ok: false, error: 'Слишком быстро. Попробуйте ещё раз.' }, { status: 429, corsOrigin });
      }
    }

    const valid = isValidLead({ name, email, phone, message });
    if (!valid.ok) {
      return jsonResponse({ ok: false, error: valid.error }, { status: 400, corsOrigin });
    }

    const ip = getClientIp(request);
    const rl = await enforceRateLimit(env, ip);
    if (!rl.ok) {
      return jsonResponse({ ok: false, error: 'Слишком много запросов. Попробуйте позже.' }, { status: 429, corsOrigin });
    }

    const ua = request.headers.get('User-Agent') || '';
    const text =
      `📬 Новая заявка\n` +
      `👤 Имя: ${name}\n` +
      `📧 Email: ${email}\n` +
      `📱 Телефон: ${phone}\n` +
      `💬 Сообщение: ${message}\n` +
      `📄 Страница: ${page}\n` +
      `🌐 IP: ${ip}\n` +
      (ua ? `🧭 UA: ${ua}` : '');

    try {
      await sendToTelegram(env, text);
      return jsonResponse({ ok: true }, { status: 200, corsOrigin });
    } catch (err) {
      const status = (err && err.status) ? err.status : 500;
      return jsonResponse(
        { ok: false, error: 'Ошибка сервера. Попробуйте позже.' },
        { status, corsOrigin }
      );
    }
  }
};
