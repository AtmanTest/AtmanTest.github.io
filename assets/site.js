(function () {
  'use strict';

  // Thème : clair / sombre, mémorisé si possible.
  var root = document.documentElement;
  var btn = document.getElementById('theme');
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  if (btn) {
    btn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) { /* stockage indisponible */ }
    });
  }

  // Chaîne QA : onglets accessibles (flèches, Début, Fin).
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.step-btn'));
  function select(i, focus) {
    tabs.forEach(function (t, k) {
      var on = k === i;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      var p = document.getElementById(t.getAttribute('aria-controls'));
      if (p) p.hidden = !on;
    });
    if (focus) tabs[i].focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(i, false); });
    t.addEventListener('keydown', function (ev) {
      var n = tabs.length, k = -1;
      if (ev.key === 'ArrowDown' || ev.key === 'ArrowRight') k = (i + 1) % n;
      else if (ev.key === 'ArrowUp' || ev.key === 'ArrowLeft') k = (i - 1 + n) % n;
      else if (ev.key === 'Home') k = 0;
      else if (ev.key === 'End') k = n - 1;
      if (k >= 0) { ev.preventDefault(); select(k, true); }
    });
  });

  // Frise : ouvrir la mission ciblée.
  function openFromHash() {
    var id = location.hash.slice(1);
    var el = id && document.getElementById(id);
    if (el && el.tagName === 'DETAILS') el.open = true;
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();
})();
