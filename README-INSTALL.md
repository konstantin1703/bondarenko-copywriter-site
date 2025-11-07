
# Готовая сборка сайта — Bondarenko Copywriter

Домен: https://konstantin1703.github.io/bondarenko-copywriter-site/

## Быстрый старт (локально)
1. Скопируйте `js/config.sample.js` → `js/config.js`.
2. Откройте `js/config.js` и вставьте:
   - `TELEGRAM_BOT_TOKEN`: ваш токен бота (**не коммитьте**)
   - `TELEGRAM_CHAT_ID`: 6135071547
   - `MATOMO_URL`: `https://YOUR_SUBDOMAIN.matomo.cloud/` (если нет — оставьте пустым)
   - `MATOMO_SITE_ID`: `1`
3. Запустите локальный сервер (например, VS Code Live Server).
4. Проверьте:
   - Форму на главной (сообщение придёт в Telegram).
   - Страницу `/testimonials.html` — демо-отзывы и отправка отзыва в Telegram.

## Продакшн (GitHub Pages)
- Убедитесь, что `js/config.js` **в .gitignore** и не попадает в репозиторий.
- Загрузите все файлы в репозиторий `bondarenko-copywriter-site` (ветка `main`).
- GitHub Pages обновит сайт по адресу https://konstantin1703.github.io/bondarenko-copywriter-site/

## SEO/Сервисные файлы
- `robots.txt`, `sitemap.xml`, `site.webmanifest`, `rss.xml` — уже настроены под ваш домен.
- `og-preview.png`, папка `favicons/` — готовы.

## Отзывы
- Исходная база: `data/reviews.json` (с демо-отзывами). Формат:
```json
[
  {"name":"Имя, роль","rating":5,"text":"Короткий отзыв","created_at":"2025-11-06T12:00:00Z"}
]
```
- Новые отзывы приходят в Telegram через форму на `/testimonials.html`.
- Для публикации добавляйте одобренные отзывы вручную в `data/reviews.json` и коммитьте изменения.
- Демо-отзывы скрываются автоматически, как только появятся реальные.

## Безопасность
- Никогда не публикуйте `js/config.js` с токенами.
- При утечке токена перевыпустите его (BotFather `/revoke` → `/token`).

Удачи!
