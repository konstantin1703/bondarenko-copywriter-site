
async function fetchReviews() {
  try {
    const res = await fetch('/bondarenko-copywriter-site/data/reviews.json', { cache: 'no-store' });
    if (!res.ok) throw new Error('Fetch failed');
    const json = await res.json();
    const real = json.filter(x => !x.demo);
    if (real.length) return real;
    return json;
  } catch (e) {
    console.warn('reviews.json не найден, используем демо-набор', e);
    return [
      { name: "Анна, заказчик", rating: 5, text: "Работа выполнена быстро и качественно. Текст полностью соответствует задаче, спасибо!", demo: true, created_at: new Date().toISOString() },
      { name: "Иван, владелец сайта", rating: 5, text: "Отличный копирайтер. Грамотный, пунктуальный, всегда на связи.", demo: true, created_at: new Date().toISOString() },
      { name: "Мария, маркетолог", rating: 5, text: "Тексты повышают конверсию — протестировали на лендингах.", demo: true, created_at: new Date().toISOString() }
    ];
  }
}
function renderStars(rating) {
  const full = '★'.repeat(Math.round(rating));
  const empty = '☆'.repeat(5 - Math.round(rating));
  return `<span aria-label="Рейтинг ${rating} из 5" class="text-amber-400 text-xl">${full}${empty}</span>`;
}
function calcAverage(reviews) {
  if (!reviews.length) return 0;
  return (reviews.reduce((s, r) => s + (r.rating || 0), 0) / reviews.length).toFixed(1);
}
async function mountReviews() {
  const reviews = await fetchReviews();
  const avg = calcAverage(reviews);
  const wrap = document.getElementById('reviews-list');
  const header = document.getElementById('reviews-summary');
  if (header) header.innerHTML = `⭐ ${avg} из 5 на основе ${reviews.length} отзывов`;
  if (!wrap) return;
  wrap.innerHTML = reviews.map(r => `
    <article class="p-5 rounded-2xl bg-slate-800/60 border border-slate-700">
      <div class="flex items-center justify-between mb-2">
        <h4 class="font-semibold">${r.name || "Клиент"}</h4>
        ${renderStars(r.rating || 5)}
      </div>
      <p class="text-slate-300">${r.text}</p>
      ${r.demo ? '<span class="text-xs text-slate-500">демо-отзыв</span>' : ''}
    </article>
  `).join('');
}
document.addEventListener('DOMContentLoaded', mountReviews);
