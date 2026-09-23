(() => {
  const root = document.documentElement;

  // ---- theme ----
  const store = {
    get: () => { try { return localStorage.getItem("theme"); } catch { return null; } },
    set: (v) => { try { localStorage.setItem("theme", v); } catch { /* ignore */ } },
  };
  const saved = store.get();
  if (saved === "light" || saved === "dark") root.dataset.theme = saved;

  document.getElementById("theme-btn")?.addEventListener("click", () => {
    const current = root.dataset.theme
      || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const next = current === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    store.set(next);
  });

  // ---- footer year ----
  const year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  // ---- split-flap title ----
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  document.querySelectorAll(".flap").forEach((el) => {
    const word = el.dataset.flap || el.textContent.trim();
    el.setAttribute("aria-label", word);
    el.textContent = "";
    const cells = [...word].map((ch) => {
      const c = document.createElement("span");
      c.className = "cell";
      c.setAttribute("aria-hidden", "true");
      c.textContent = reduce ? ch : CHARS[Math.floor(Math.random() * CHARS.length)];
      el.appendChild(c);
      return { c, ch };
    });
    if (reduce) return;
    cells.forEach(({ c, ch }, i) => {
      let n = 0;
      const stop = 8 + i * 3;
      const t = setInterval(() => {
        n++;
        if (n >= stop) { c.textContent = ch; clearInterval(t); return; }
        c.textContent = CHARS[Math.floor(Math.random() * CHARS.length)];
      }, 55);
    });
  });

  // ---- reveal on scroll ----
  const targets = document.querySelectorAll(".section-title, .skill-card, .hobby, .work, .oss, .link-card, .board, .facts");
  if (!reduce && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach((t) => { t.classList.add("reveal"); io.observe(t); });
  }
})();
