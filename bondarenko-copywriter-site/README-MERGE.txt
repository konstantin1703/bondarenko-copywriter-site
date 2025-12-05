Matomo Integration — Merge Notes
--------------------------------
1) Файлы пакета добавлены в проект. Конфликты оставлены как *.added — сравните и слейте вручную при необходимости.
2) В HTML файлы автоматически вставлен <script src="src/analytics/init-matomo.js"> перед </head>.
   Задайте переменные:
     window.MATOMO_BASE_URL = "https://analytics.example.com/"
     window.MATOMO_SITE_ID = "1"
3) Cloudflare Worker: см. /cloudflare/worker.js и wrangler.toml. Секреты задаются через:
     wrangler secret put MATOMO_URL
     wrangler secret put MATOMO_TOKEN
     wrangler secret put MATOMO_SITE_ID
4) GitHub Actions (.github/workflows/deploy.yml) — деплой в GitHub Pages при push в main.
5) Запуск целей: npm run matomo:auto-goals (предварительно MATOMO_* переменные окружения).
6) Дашборд: /dashboard/index.html использует /live и /widget (из Worker).
7) Смоук-тест: npm run test:analytics (при наличии MATOMO_*).