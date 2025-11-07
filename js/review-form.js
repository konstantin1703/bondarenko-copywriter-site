
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('review-form');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const name = fd.get('name');
    const email = fd.get('email');
    const rating = fd.get('rating');
    const message = fd.get('message');
    const text = [
      '📝 <b>Новый отзыв с сайта</b>',
      `👤 <b>Имя:</b> ${name}`,
      `✉️ <b>Email:</b> ${email}`,
      `⭐ <b>Оценка:</b> ${rating}`,
      `💬 <b>Отзыв:</b> ${message}`
    ].join('\\n');
    const res = await sendTelegramMessage(text);
    const ok = res && (res.ok === true);
    const status = document.getElementById('review-status');
    if (ok) { status.textContent = 'Спасибо! Отзыв отправлен на модерацию.'; form.reset(); }
    else { status.textContent = 'Не удалось отправить. Попробуйте ещё раз.'; }
  });
});
