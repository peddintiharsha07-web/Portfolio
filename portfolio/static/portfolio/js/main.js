(function () {
  var root = document.documentElement;
  var $ = function (s) { return document.querySelector(s); };
  var save = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* light / dark (visitors) */
  var modeBtn = $("#modeToggle");
  if (modeBtn) {
    var paintMode = function () { modeBtn.innerHTML = '<i class="bi bi-' + (root.dataset.mode === "dark" ? "sun-fill" : "moon-stars-fill") + '"></i>'; };
    modeBtn.addEventListener("click", function () {
      root.dataset.mode = root.dataset.mode === "dark" ? "light" : "dark";
      save("mode", root.dataset.mode); paintMode();
    });
    paintMode();
  }

  /* site colour palette (rendered for admins only; saved on the server for everyone) */
  var palette = $("#palette"), pbtn = $("#paletteBtn");
  if (palette && pbtn) {
    var swatches = document.querySelectorAll(".swatch");
    var paintSwatch = function () { swatches.forEach(function (s) { s.classList.toggle("on", s.dataset.color === root.dataset.color); }); };
    pbtn.addEventListener("click", function (e) { e.stopPropagation(); palette.classList.toggle("open"); });
    document.addEventListener("click", function (e) { if (!palette.contains(e.target)) palette.classList.remove("open"); });
    swatches.forEach(function (s) {
      s.addEventListener("click", function () {
        root.dataset.color = s.dataset.color; paintSwatch();
        var body = new URLSearchParams({ color: s.dataset.color });
        fetch($("meta[name=color-url]").content, {
          method: "POST", body: body,
          headers: { "X-CSRFToken": $("meta[name=csrf-token]").content }
        });
      });
    });
    paintSwatch();
  }

  /* mobile menu */
  var menu = $("#menu");
  var burger = $("#burger");
  if (menu && burger) {
    var closeMenu = function () {
      menu.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
      burger.setAttribute("aria-label", "Open navigation menu");
      var icon = burger.querySelector("i");
      if (icon) icon.className = "bi bi-list";
    };
    burger.addEventListener("click", function () {
      var isOpen = menu.classList.toggle("open");
      burger.setAttribute("aria-expanded", String(isOpen));
      burger.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
      var icon = burger.querySelector("i");
      if (icon) icon.className = isOpen ? "bi bi-x-lg" : "bi bi-list";
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
    document.addEventListener("click", function (e) {
      if (menu.classList.contains("open") && !menu.contains(e.target) && !burger.contains(e.target)) closeMenu();
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 960) closeMenu();
    });
  }

  /* typing animation: types each word, pauses, deletes, moves on */
  var typed = $("#typed");
  if (typed && !reduce) {
    var words = typed.dataset.words.split("|").filter(Boolean);
    if (words.length) {
      var wi = 0, ci = 0, del = false;
      typed.textContent = "";
      (function tick() {
        var w = words[wi], delay = del ? 45 : 90;
        ci += del ? -1 : 1;
        typed.textContent = w.slice(0, ci);
        if (!del && ci === w.length) { if (words.length === 1) return; del = true; delay = 1500; }
        else if (del && ci === 0) { del = false; wi = (wi + 1) % words.length; delay = 350; }
        setTimeout(tick, delay);
      })();
    }
  }

  /* carousels (projects + certificates) with arrows and dots */
  function carousel(sel, prev, next, dotsSel) {
    var el = $(sel); if (!el || !el.firstElementChild) return;
    var dots = dotsSel && $(dotsSel);
    var step = function () { return el.firstElementChild.offsetWidth + (parseFloat(getComputedStyle(el).columnGap) || 16); };
    var pages = function () { return Math.max(1, Math.round((el.scrollWidth - el.clientWidth) / step()) + 1); };
    var draw = function () {
      if (!dots) return;
      var n = pages(), cur = Math.round(el.scrollLeft / step());
      dots.innerHTML = ""; 
      for (var k = 0; k < n; k++) { var d = document.createElement("i"); if (k === cur) d.className = "on"; dots.appendChild(d); }
    };
    $(next).addEventListener("click", function () { el.scrollBy({ left: step(), behavior: "smooth" }); });
    $(prev).addEventListener("click", function () { el.scrollBy({ left: -step(), behavior: "smooth" }); });
    el.addEventListener("scroll", draw, { passive: true }); window.addEventListener("resize", draw); draw();
  }
  carousel("#slider", "#prev", "#next");
  carousel("#certSlider", "#cPrev", "#cNext", "#certDots");

  /* reveal on scroll + active nav link */
  var links = document.querySelectorAll(".menu a[href*='#']:not(.btn)");
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        links.forEach(function (a) { a.classList.toggle("active", a.getAttribute("href").split("#")[1] === en.target.id); });
      });
    }, { threshold: 0.25 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else { revealEls.forEach(function (el) { el.classList.add("in"); }); }
})();
