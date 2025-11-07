Интеграционный оверлей — Vite + React Widgets + Cloudflare Worker (KV)

1) Скопируйте содержимое этого архива в КОРЕНЬ вашего репозитория,
   согласившись на замену package.json, добавление vite.config.js, /src, /.github/workflows,
   /cloudflare/worker.patched.js, /cloudflare/wrangler.toml и og-preview.png.

2) Вставьте в index.html (в <head>) OG-теги, если их нет:
   (см. OG-HEAD.txt в архиве)

3) Перед </body> добавьте:
   <script type="module" src="/src/main.js"></script>
   И блок виджета:
   <div data-widget="reviews"></div>
   (для Live-виджета: <div data-widget="live"></div>)

4) Cloudflare:
   wrangler kv:namespace create "REVIEWS"
   Подставьте id/preview_id в cloudflare/wrangler.toml
   wrangler secret put MATOMO_URL
   wrangler secret put MATOMO_TOKEN
   wrangler secret put MATOMO_SITE_ID
   wrangler dev  # проверить /live, /reviews, /widget

5) GitHub:
   Коммитните изменения — Pages сам соберёт Vite и задеплоит из dist/.