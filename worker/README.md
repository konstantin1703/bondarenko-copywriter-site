# Cloudflare Worker: /api/lead

Этот воркер принимает заявку с фронта (`POST /api/lead`) и отправляет её в Telegram **без секретов на клиенте**.

## Быстрый старт (Wrangler)

1) Установите Wrangler (если ещё не установлен):
- `npm i -g wrangler`

2) Перейдите в папку `worker/` и установите структуру:
- `cd worker`

3) Создайте KV namespace для rate limit (опционально, но рекомендуется):
- `wrangler kv:namespace create LEAD_RATELIMIT`
Скопируйте `id` и вставьте его в `wrangler.toml` вместо `REPLACE_WITH_KV_NAMESPACE_ID`.

4) Добавьте секреты Telegram:
- `wrangler secret put TELEGRAM_TOKEN`
- `wrangler secret put TELEGRAM_CHAT_ID`

5) (Опционально) Разрешённые Origin для CORS:
- откройте `wrangler.toml` и в `ALLOWED_ORIGINS` добавьте ваши домены через запятую.
  Пример: `https://konstantin1703.github.io,https://example.com`

6) Запуск локально:
- `wrangler dev`

7) Деплой:
- `wrangler deploy`

## Эндпоинт

- `POST /api/lead`
- JSON:
  ```json
  {
    "name": "Иван",
    "email": "mail@example.com",
    "message": "Хочу лендинг для услуги...",
    "page": "/index.html",
    "company": "",
    "client_ts": 1730000000000
  }
  ```

### Антиспам

- Honeypot `company`: если заполнено — запрос отклоняется.
- `client_ts`: если отправка < 2 секунд — 429.
- KV rate limit: 5 запросов/мин на IP (если подключён KV).

## Подключение на фронте

Во всех HTML в начале inline-скрипта есть одна строка:
```js
const LEAD_ENDPOINT = "/api/lead";
```

Если воркер развернут на отдельном домене — замените строку на:
```js
const LEAD_ENDPOINT = "https://YOUR_WORKER.workers.dev/api/lead";
```
