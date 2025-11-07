
async function sendTelegramMessage(text) {
  try {
    const res = await fetch("https://bondarenko-proxy.irisinsightai.workers.dev/telegram", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    if (data.ok) {
      console.log("✅ Сообщение успешно отправлено через Worker!");
    } else {
      console.error("⚠️ Ошибка при отправке:", data);
    }
  } catch (e) {
    console.error("❌ Ошибка подключения к Worker:", e);
  }
}
