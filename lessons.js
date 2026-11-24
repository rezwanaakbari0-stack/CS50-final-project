const grid = document.getElementById("lessons-grid");
const filters = document.getElementById("filters");

function card(l) {
  const div = document.createElement("div");
  div.className = "card";
  div.innerHTML = '<div class="ic"></div><h3></h3><p></p><span class="tag"></span>';
  div.querySelector(".ic").textContent = l.icon;
  div.querySelector("h3").textContent = l.title;
  div.querySelector("p").textContent = l.text;
  div.querySelector(".tag").textContent = l.category;
  return div;
}

async function load(category) {
  try {
    const res = await fetch("/api/lessons?category=" + encodeURIComponent(category));
    const items = await res.json();
    grid.replaceChildren(...items.map(card));
  } catch (err) {
    grid.textContent = "خطا در بارگذاری درس‌ها.";
  }
}

filters.addEventListener("click", (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;
  filters.querySelectorAll("button").forEach((b) => b.classList.remove("on"));
  btn.classList.add("on");
  load(btn.dataset.c);
});

load("all");
