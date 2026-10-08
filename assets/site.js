(function () {
  'use strict';

  var root = document.documentElement;
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* ---------- Thème ---------- */
  var themeBtn = $('#theme');
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) { /* stockage indisponible */ }
    });
  }

  /* ---------- Chaîne QA : onglets accessibles (clic, flèches, Début / Fin) ---------- */
  var chain = $('[data-chain]');
  if (chain) {
    var tabs = $$('.tile', chain);
    var select = function (i, focus) {
      tabs.forEach(function (t, k) {
        var on = k === i;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i, false); });
      t.addEventListener('keydown', function (ev) {
        var n = tabs.length, k = -1;
        if (ev.key === 'ArrowRight' || ev.key === 'ArrowDown') k = (i + 1) % n;
        else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowUp') k = (i - 1 + n) % n;
        else if (ev.key === 'Home') k = 0;
        else if (ev.key === 'End') k = n - 1;
        if (k >= 0) { ev.preventDefault(); select(k, true); }
      });
    });
  }

  /* ---------- Missions : tout déplier / replier ---------- */
  var expand = $('[data-expand]'), jobs = $$('.job');
  if (expand) {
    var sync = function () {
      var all = jobs.every(function (j) { return j.open; });
      expand.textContent = expand.getAttribute(all ? 'data-t-close' : 'data-t-open');
      expand.setAttribute('aria-pressed', all ? 'true' : 'false');
    };
    expand.addEventListener('click', function () {
      var all = jobs.every(function (j) { return j.open; });
      jobs.forEach(function (j) { j.open = !all; });
      sync();
    });
    jobs.forEach(function (j) { j.addEventListener('toggle', sync); });
    sync();
  }

  /* ---------- Ouvrir la mission ciblée (frise, liens de preuve) ---------- */
  function openFromHash() {
    var id = location.hash.slice(1), el = id && document.getElementById(id);
    if (el && el.tagName === 'DETAILS') el.open = true;
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();

  /* ---------- Menu des sections (petit écran) ---------- */
  var menu = $('.menu');
  if (menu) {
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { menu.open = false; }); });
    document.addEventListener('click', function (ev) { if (menu.open && !menu.contains(ev.target)) menu.open = false; });
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && menu.open) { menu.open = false; $('summary', menu).focus(); } });
  }

  /* ---------- Copie de l'adresse e-mail ---------- */
  var copyBtn = $('[data-copy]'), cstatus = $('[data-cstatus]');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      var addr = copyBtn.getAttribute('data-copy'), ok = copyBtn.getAttribute('data-t-ok');
      var done = function () { if (cstatus) { cstatus.textContent = ok; setTimeout(function () { cstatus.textContent = ''; }, 2500); } };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(addr).then(done, function () { window.prompt('', addr); });
      } else { window.prompt('', addr); }
    });
  }
})();
