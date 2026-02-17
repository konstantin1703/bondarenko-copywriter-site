# Bondarenko Copywriter Portfolio Site

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![GitHub Pages](https://img.shields.io/badge/deployed-GitHub%20Pages-blue.svg)

Профессиональный сайт-портфолио копирайтера Константина Бондаренко.

## 🚀 Быстрый старт

### Предварительные требования

- Git установлен на вашем компьютере
- Современный веб-браузер
- (Опционально) Node.js 16+ для будущих инструментов разработки

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/konstantin1703/bondarenko-copywriter-site.git
cd bondarenko-copywriter-site
```

2. Откройте index.html в браузере или используйте локальный сервер:
```bash
# Используя Python 3
python -m http.server 8000

# Используя Node.js (если установлен http-server)
npx http-server -p 8000
```

3. Откройте браузер: http://localhost:8000

## 📁 Структура проекта

```
bondarenko-copywriter-site/
├── index.html           # Главная страница
├── robots.txt          # SEO: правила для поисковых роботов
├── sitemap.xml         # SEO: карта сайта
├── site.webmanifest    # PWA манифест
├── package.json        # Метаданные проекта
├── .gitignore         # Игнорируемые файлы Git
└── README.md          # Документация проекта
```

## 🛠️ Технологии

- **Frontend**: HTML5, CSS3, JavaScript
- **Хостинг**: GitHub Pages
- **Version Control**: Git

## 📝 Workflow разработки

### Ветки

- `main` - production-версия (деплоится на GitHub Pages)
- `dev-restructure` - разработка новых функций
- `jarvis/*` - экспериментальные ветки

### Процесс внесения изменений

1. Создайте новую ветку от `dev-restructure`:
```bash
git checkout dev-restructure
git pull origin dev-restructure
git checkout -b feature/your-feature-name
```

2. Внесите изменения и закоммитьте:
```bash
git add .
git commit -m "feat: описание изменений"
```

3. Запушьте изменения:
```bash
git push origin feature/your-feature-name
```

4. Создайте Pull Request в `dev-restructure`

### Соглашения о коммитах

Используем [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - новая функция
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование, отступы
- `refactor:` - рефакторинг кода
- `test:` - добавление тестов
- `chore:` - обновление зависимостей, конфигурация

## 🌐 Деплой

Сайт автоматически деплоится на GitHub Pages при пуше в ветку `main`:

**URL**: https://konstantin1703.github.io/bondarenko-copywriter-site/

## 📋 Roadmap

### Текущая версия (v1.0.0)
- ✅ Базовая структура сайта
- ✅ SEO-оптимизация (robots.txt, sitemap.xml)
- ✅ Документация проекта

### Планируется (v1.1.0)
- [ ] Разделение на модули (CSS, JS в отдельных файлах)
- [ ] Добавление favicon и Open Graph изображений
- [ ] Настройка системы сборки (Vite/Webpack)
- [ ] Оптимизация производительности
- [ ] Адаптивная верстка для мобильных устройств

### Будущие улучшения (v2.0.0)
- [ ] CI/CD через GitHub Actions
- [ ] Автоматические тесты
- [ ] PWA функциональность
- [ ] Многоязычность (RU/EN)
- [ ] Блог с системой управления контентом

## 🤝 Вклад в проект

Если у вас есть предложения по улучшению:

1. Форкните репозиторий
2. Создайте ветку для вашей функции
3. Закоммитьте изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License - см. файл LICENSE для деталей

## 📧 Контакты

- **GitHub**: [@konstantin1703](https://github.com/konstantin1703)
- **Email**: irisinsightai@gmail.com

---

*Последнее обновление: Февраль 2026*