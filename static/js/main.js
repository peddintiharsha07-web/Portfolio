document.addEventListener("DOMContentLoaded", function () {
  /* ---------- Page loader ---------- */
  const loader = document.getElementById("pageLoader");
  window.addEventListener("load", () => {
    setTimeout(() => loader && loader.classList.add("loaded"), 250);
  });

  /* ---------- Mobile nav toggle ---------- */
  const navToggle = document.getElementById("navToggle");
  const navMenu = document.getElementById("navMenu");
  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      const isOpen = navMenu.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
    navMenu.querySelectorAll(".nav-link-item").forEach((link) => {
      link.addEventListener("click", () => navMenu.classList.remove("open"));
    });
  }

  /* ---------- Sticky header shadow ---------- */
  const header = document.getElementById("siteHeader");
  window.addEventListener("scroll", () => {
    if (header) header.style.boxShadow = window.scrollY > 20 ? "0 6px 24px rgba(20,20,31,0.08)" : "none";
  });

  /* ---------- Scroll reveal ---------- */
  const revealEls = document.querySelectorAll("[data-reveal]");
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  revealEls.forEach((el) => revealObserver.observe(el));

  /* ---------- Animated stat counters ---------- */
  const counters = document.querySelectorAll(".stat-num[data-count]");
  const counterObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = parseInt(el.getAttribute("data-count"), 10) || 0;
        const duration = 1200;
        const start = performance.now();
        function tick(now) {
          const progress = Math.min((now - start) / duration, 1);
          el.textContent = Math.floor(progress * target);
          if (progress < 1) requestAnimationFrame(tick);
          else el.textContent = target;
        }
        requestAnimationFrame(tick);
        counterObserver.unobserve(el);
      });
    },
    { threshold: 0.4 }
  );
  counters.forEach((el) => counterObserver.observe(el));

  /* ---------- Skill circular progress rings ---------- */
  const RADIUS = 52;
  const CIRCUMFERENCE = 2 * Math.PI * RADIUS;
  document.querySelectorAll(".ring-fg").forEach((circle) => {
    circle.style.strokeDasharray = `${CIRCUMFERENCE}`;
    circle.style.strokeDashoffset = `${CIRCUMFERENCE}`;
  });

  const skillObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const wrap = entry.target;
        const pct = parseFloat(wrap.getAttribute("data-percentage")) || 0;
        const circle = wrap.querySelector(".ring-fg");
        const percentLabel = wrap.querySelector(".ring-percent");
        if (circle) {
          const offset = CIRCUMFERENCE - (pct / 100) * CIRCUMFERENCE;
          requestAnimationFrame(() => (circle.style.strokeDashoffset = `${offset}`));
        }
        if (percentLabel) {
          const target = parseInt(percentLabel.getAttribute("data-target"), 10) || 0;
          const duration = 1200;
          const start = performance.now();
          function tick(now) {
            const progress = Math.min((now - start) / duration, 1);
            percentLabel.textContent = `${Math.floor(progress * target)}%`;
            if (progress < 1) requestAnimationFrame(tick);
            else percentLabel.textContent = `${target}%`;
          }
          requestAnimationFrame(tick);
        }
        skillObserver.unobserve(wrap);
      });
    },
    { threshold: 0.4 }
  );
  document.querySelectorAll(".skill-ring").forEach((el) => skillObserver.observe(el));

  /* ---------- Auto-dismiss Django messages, if present ---------- */
  document.querySelectorAll(".alert").forEach((alertEl) => {
    setTimeout(() => alertEl.classList.add("fade-out"), 4000);
  });
});
