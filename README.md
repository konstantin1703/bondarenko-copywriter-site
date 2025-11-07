# Bondarenko — Final Ready Build

**Дата:** 2025-11-07T16:25:42.801942Z

## Быстрый старт
1) Скопируйте содержимое этого архива в корень репозитория `bondarenko-copywriter-site`.
2) В GitHub Desktop: Commit → Push.
3) Зайдите в GitHub → Actions: дождитесь зелёного деплоя.
4) Откройте сайт: https://konstantin1703.github.io/bondarenko-copywriter-site/

## Важно
- `vite.config.js` использует base: `/bondarenko-copywriter-site/` — это путь проекта на GitHub Pages.
- `404.html` делает редирект на главную — фикс для роутинга на Pages.

## Cloudflare Worker
```bash
cd cloudflare
wrangler kv:namespace create "REVIEWS"
wrangler kv:namespace create "REVIEWS" --preview
# Подставьте id/preview_id в wrangler.toml

wrangler secret put MATOMO_URL
wrangler secret put MATOMO_TOKEN
wrangler secret put MATOMO_SITE_ID

wrangler dev  # проверка /live, /widget, /reviews
```

## Превью
Замените файл `og-preview.png` в корне на вашу итоговую картинку.
