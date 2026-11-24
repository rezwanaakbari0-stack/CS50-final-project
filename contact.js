const form = document.getElementById("contact-form");
const statusBox = document.getElementById("status");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = Object.fromEntries(new FormData(form));
  statusBox.textContent = "در حال ارسال...";
  statusBox.className = "";
  try {
    const res = await fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (data.ok) {
      form.reset();
      statusBox.textContent = "✅ پیام شما ثبت شد. ممنون!";
      statusBox.className = "ok";
    } else {
      statusBox.textContent = data.error || "خطایی رخ داد.";
      statusBox.className = "err";
    }
  } catch (err) {
    statusBox.textContent = "ارتباط با سرور برقرار نشد.";
    statusBox.className = "err";
  }
});
