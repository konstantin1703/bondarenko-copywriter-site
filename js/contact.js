
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const name = fd.get('name');
    const email = fd.get('email');
    const message = fd.get('message');
    const text = [
      '📩 <b>Новая заявка с сайта</b>',
      `👤 <b>Имя:</b> ${name}`,
      `✉️ <b>Email:</b> ${email}`,
      `💬 <b>Сообщение:</b> ${message}`
    ].join('\\n');
    const res = await sendTelegramMessage(text);
    const ok = res && (res.ok === true);
    const status = document.getElementById('contact-status');
    if (ok) { status.textContent = 'Спасибо! Сообщение отправлено.'; form.reset(); }
    else { status.textContent = 'Не удалось отправить. Попробуйте ещё раз.'; }
  });
});
