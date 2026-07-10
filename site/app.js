(function () {
  "use strict";

  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var THEME_KEY = "rr-theme";

  var toggle = document.getElementById("themeToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var current =
        root.getAttribute("data-theme") ||
        (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      var next = current === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {
        localStorage.setItem(THEME_KEY, next);
      } catch (e) {}
    });
  }

  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  var reveals = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) {
      el.classList.add("is-visible");
    });
  } else {
    var revealIO = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealIO.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach(function (el) {
      revealIO.observe(el);
    });
  }

  function countUp(el) {
    var to = parseFloat(el.getAttribute("data-to")) || 0;
    var pre = el.getAttribute("data-prefix") || "";
    var suf = el.getAttribute("data-suffix") || "";
    if (reduce) {
      el.textContent = pre + to + suf;
      return;
    }
    var duration = 1100;
    var startTime = null;
    function step(now) {
      if (startTime === null) startTime = now;
      var t = Math.min(1, (now - startTime) / duration);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = pre + Math.round(to * eased) + suf;
      if (t < 1) requestAnimationFrame(step);
      else el.textContent = pre + to + suf;
    }
    requestAnimationFrame(step);
  }

  var metrics = document.querySelectorAll(".metric__val");
  var counted = false;
  function runCounters() {
    if (counted) return;
    counted = true;
    metrics.forEach(countUp);
  }
  var panel = document.querySelector(".panel");
  if (panel && "IntersectionObserver" in window && !reduce) {
    var panelIO = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            runCounters();
            panelIO.disconnect();
          }
        });
      },
      { threshold: 0.4 }
    );
    panelIO.observe(panel);
  } else {
    runCounters();
  }

  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".nav__links a"));
  var sections = navLinks
    .map(function (link) {
      return document.querySelector(link.getAttribute("href"));
    })
    .filter(Boolean);

  if (sections.length && "IntersectionObserver" in window) {
    var navIO = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var id = entry.target.getAttribute("id");
            navLinks.forEach(function (link) {
              link.classList.toggle(
                "is-active",
                link.getAttribute("href") === "#" + id
              );
            });
          }
        });
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    sections.forEach(function (section) {
      navIO.observe(section);
    });
  }
})();
