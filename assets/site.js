(function () {
  'use strict';

  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
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

  /* ---------- Couverture de la page (défilement) ---------- */
  var nav = $('.nav'), pcov = $('[data-pcov]'), ticking = false;
  function onScroll() {
    ticking = false;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    if (nav) nav.style.setProperty('--p', p.toFixed(4));
    if (pcov) pcov.textContent = Math.round(p * 100);
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- Chiffres animés ---------- */
  var counters = $$('[data-count]');
  function runCount(el) {
    var txt = el.textContent, m = txt.match(/^(\d+)(.*)$/);
    if (!m || reduce) return;
    var target = parseInt(m[1], 10), suffix = m[2], t0 = null, dur = 1000;
    function step(t) {
      if (t0 === null) t0 = t;
      var k = Math.min(1, (t - t0) / dur), eased = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (k < 1) requestAnimationFrame(step); else el.textContent = txt;
    }
    el.textContent = '0' + suffix;
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window && counters.length) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { runCount(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ---------- Chaîne QA : onglets, flèches, lecture automatique ---------- */
  var chain = $('[data-chain]');
  if (chain) {
    var tabs = $$('.step-btn', chain), items = $$('.stepper li', chain);
    var playBtn = $('[data-play]', chain), timer = null, cur = 0;
    var tPlay = chain.getAttribute('data-t-play'), tPause = chain.getAttribute('data-t-pause');
    var select = function (i, focus) {
      cur = i;
      tabs.forEach(function (t, k) {
        var on = k === i;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
        items[k].classList.toggle('done', k < i);
      });
      if (focus) tabs[i].focus();
    };
    var stop = function () {
      if (timer) { clearInterval(timer); timer = null; }
      if (playBtn) { playBtn.setAttribute('aria-pressed', 'false'); playBtn.textContent = tPlay; }
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { stop(); select(i, false); });
      t.addEventListener('keydown', function (ev) {
        var n = tabs.length, k = -1;
        if (ev.key === 'ArrowRight' || ev.key === 'ArrowDown') k = (i + 1) % n;
        else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowUp') k = (i - 1 + n) % n;
        else if (ev.key === 'Home') k = 0;
        else if (ev.key === 'End') k = n - 1;
        if (k >= 0) { ev.preventDefault(); stop(); select(k, true); }
      });
    });
    if (playBtn) {
      playBtn.addEventListener('click', function () {
        if (timer) { stop(); return; }
        playBtn.setAttribute('aria-pressed', 'true');
        playBtn.textContent = tPause;
        if (cur >= tabs.length - 1) select(0, false);
        timer = setInterval(function () {
          if (cur >= tabs.length - 1) { stop(); return; }
          select(cur + 1, false);
        }, 3200);
      });
    }
    select(0, false);
  }

  /* ---------- Matrice outils × missions ---------- */
  var matrix = $('[data-matrix]');
  if (matrix) {
    var labels = JSON.parse(matrix.getAttribute('data-labels'));
    var stacks = JSON.parse(matrix.getAttribute('data-stacks'));
    var tUsed = matrix.getAttribute('data-t-used'), tStack = matrix.getAttribute('data-t-stack'), tNone = matrix.getAttribute('data-t-none');
    var status = $('[data-mstatus]', matrix), rows = $$('tbody tr[data-tool]', matrix);
    var rowBtns = $$('.row-btn', matrix), colBtns = $$('.col-btn', matrix), cells = $$('tbody td', matrix);
    var clear = function () {
      matrix.classList.remove('has-sel', 'sel-col-on');
      rows.forEach(function (r) { r.classList.remove('sel-row', 'dim-row'); });
      cells.forEach(function (c) { c.classList.remove('sel-c'); });
      rowBtns.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      colBtns.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); b.classList.remove('sel-col-h'); });
      status.textContent = tNone;
    };
    var selRow = function (tr, btn) {
      var was = btn.getAttribute('aria-pressed') === 'true';
      clear();
      if (was) return;
      matrix.classList.add('has-sel');
      tr.classList.add('sel-row');
      btn.setAttribute('aria-pressed', 'true');
      var names = tr.getAttribute('data-in').split(' ').map(function (id) { return labels[id]; });
      status.textContent = tr.getAttribute('data-tool') + ' — ' + tUsed + ' ' + names.join(', ') + '.';
    };
    var selCol = function (id, btn) {
      var was = btn.getAttribute('aria-pressed') === 'true';
      clear();
      if (was) return;
      matrix.classList.add('sel-col-on');
      btn.setAttribute('aria-pressed', 'true');
      btn.classList.add('sel-col-h');
      cells.forEach(function (c) { c.classList.toggle('sel-c', c.getAttribute('data-col') === id); });
      rows.forEach(function (r) { r.classList.toggle('dim-row', r.getAttribute('data-in').split(' ').indexOf(id) < 0); });
      status.textContent = labels[id] + ' — ' + stacks[id].join(', ') + '.';
    };
    rows.forEach(function (tr) {
      var b = $('.row-btn', tr);
      b.addEventListener('click', function () { selRow(tr, b); });
    });
    colBtns.forEach(function (b) {
      b.addEventListener('click', function () { selCol(b.getAttribute('data-col'), b); });
    });
    var reset = $('[data-reset]', matrix);
    if (reset) reset.addEventListener('click', clear);
  }

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

  /* ---------- Frise : ouvrir la mission ciblée ---------- */
  function openFromHash() {
    var id = location.hash.slice(1), el = id && document.getElementById(id);
    if (el && el.tagName === 'DETAILS') el.open = true;
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();
  /* Les barres de la frise sont un raccourci visuel (pointeur) ; la liste des missions reste l'accès accessible. */
  $$('.bar[data-job]').forEach(function (b) {
    b.addEventListener('click', function () {
      var d = document.getElementById(b.getAttribute('data-job'));
      if (!d) return;
      d.open = true;
      d.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      var sm = d.querySelector('summary'); if (sm) sm.focus({ preventScroll: true });
    });
  });

  /* ---------- Hero : grille de couverture (canvas) ---------- */
  var hero = $('[data-hero]'), cv = hero && $('canvas.grid', hero);
  if (hero && cv && cv.getContext) {
    var ctx = cv.getContext('2d');
    var CS = 30, W = 0, H = 0, cols = 0, nrows = 0, lit, cov, blocked, defect = -1, found = 0, nCov = 0;
    var running = false, visible = true;
    var gcov = $('[data-gcov]', hero), gfound = $('[data-gfound]', hero), gmsg = $('[data-gmsg]', hero);
    var msgTxt = hero.getAttribute('data-t-found'), msgTimer = null;
    var cs = getComputedStyle(hero);
    var C = {};
    var readColors = function () {
      cs = getComputedStyle(hero);
      C.pass = cs.getPropertyValue('--pass').trim() || '#46d19a';
      C.fail = cs.getPropertyValue('--fail').trim() || '#ff7a68';
      C.rule = cs.getPropertyValue('--rule').trim() || '#25394a';
    };
    var computeBlocked = function () {
      var hr = hero.getBoundingClientRect();
      blocked = new Uint8Array(cols * nrows);
      $$('[data-solid]', hero).forEach(function (el) {
        var r = el.getBoundingClientRect();
        var w = r.width;
        var x0 = Math.floor((r.left - hr.left - 8) / CS), x1 = Math.floor((r.left - hr.left + w + 8) / CS);
        var y0 = Math.floor((r.top - hr.top - 8) / CS), y1 = Math.floor((r.bottom - hr.top + 8) / CS);
        for (var y = Math.max(0, y0); y <= Math.min(nrows - 1, y1); y++)
          for (var x = Math.max(0, x0); x <= Math.min(cols - 1, x1); x++) blocked[y * cols + x] = 1;
      });
    };
    var placeDefect = function () {
      var free = [];
      for (var i = 0; i < cols * nrows; i++) if (!blocked[i]) free.push(i);
      defect = free.length ? free[Math.floor(Math.random() * free.length)] : -1;
    };
    var setMsg = function (show) {
      if (!gmsg) return;
      gmsg.textContent = show ? msgTxt : '';
      gmsg.classList.toggle('show', !!show);
      if (msgTimer) clearTimeout(msgTimer);
      if (show) msgTimer = setTimeout(function () { gmsg.classList.remove('show'); }, 3200);
    };
    var updateStats = function () {
      if (gcov) gcov.textContent = Math.min(100, Math.round(nCov / (cols * nrows) * 100));
      if (gfound) gfound.textContent = found;
    };
    var resize = function () {
      var r = hero.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = r.width; H = r.height;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cols = Math.ceil(W / CS); nrows = Math.ceil(H / CS);
      lit = new Float32Array(cols * nrows); cov = new Uint8Array(cols * nrows); nCov = 0; active = [];
      readColors(); computeBlocked(); placeDefect(); updateStats(); draw(0);
    };
    var hexAlpha = function (col, a) {
      var m = col.match(/^#([0-9a-f]{6})$/i);
      if (!m) return col;
      var n = parseInt(m[1], 16);
      return 'rgba(' + (n >> 16) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')';
    };
    /* Rendu incrémental : seules les cellules qui changent sont redessinées. */
    var active = [], pulseAt = 0;
    var drawCell = function (i, pulse) {
      var x = i % cols, y = (i - x) / cols, px = x * CS, py = y * CS, l = lit[i];
      ctx.clearRect(px, py, CS, CS);
      if (cov[i]) { ctx.fillStyle = hexAlpha(C.pass, 0.09 + l * 0.5); ctx.fillRect(px + 1, py + 1, CS - 2, CS - 2); }
      else if (l > 0.02) { ctx.fillStyle = hexAlpha(C.pass, l * 0.5); ctx.fillRect(px + 1, py + 1, CS - 2, CS - 2); }
      ctx.strokeStyle = hexAlpha(C.rule, blocked[i] ? 0.35 : 0.8);
      ctx.lineWidth = 1;
      ctx.strokeRect(px + 0.5, py + 0.5, CS - 1, CS - 1);
      if (i === defect) { ctx.fillStyle = hexAlpha(C.fail, pulse); ctx.fillRect(px + 3, py + 3, CS - 6, CS - 6); }
    };
    var pulseOf = function (t) { return reduce ? 0.7 : 0.55 + 0.35 * Math.sin(t / 380); };
    var draw = function (t) {
      ctx.clearRect(0, 0, W, H);
      for (var i = 0, n = cols * nrows; i < n; i++) drawCell(i, pulseOf(t));
    };
    var step = function (t) {
      var next = [];
      for (var k = 0; k < active.length; k++) {
        var i = active[k], l = lit[i] * (reduce ? 0 : 0.93);
        lit[i] = l < 0.02 ? 0 : l;
        drawCell(i, pulseOf(t));
        if (lit[i] > 0) next.push(i);
      }
      active = next;
      if (defect >= 0 && t - pulseAt > 90) { pulseAt = t; drawCell(defect, pulseOf(t)); }
    };
    var activate = function (i) { if (lit[i] === 0) active.push(i); };
    var touch = function (x, y) {
      var R = 2.4, cx = x / CS, cy = y / CS;
      for (var yy = Math.max(0, Math.floor(cy - R)); yy <= Math.min(nrows - 1, Math.ceil(cy + R)); yy++) {
        for (var xx = Math.max(0, Math.floor(cx - R)); xx <= Math.min(cols - 1, Math.ceil(cx + R)); xx++) {
          var d = Math.sqrt(Math.pow(xx + 0.5 - cx, 2) + Math.pow(yy + 0.5 - cy, 2));
          if (d < R) {
            var i = yy * cols + xx, v = 1 - d / R;
            if (v > lit[i]) { activate(i); lit[i] = v; }
            if (v > 0.45 && !cov[i] && i !== defect) { cov[i] = 1; nCov++; }
          }
        }
      }
      updateStats();
    };
    var local = function (ev) { var r = hero.getBoundingClientRect(); return { x: ev.clientX - r.left, y: ev.clientY - r.top }; };
    hero.addEventListener('pointermove', function (ev) {
      var p = local(ev); touch(p.x, p.y);
      if (reduce && !running) step(0);
      loopStart();
    });
    hero.addEventListener('click', function (ev) {
      if (defect < 0) return;
      var p = local(ev), cx = defect % cols, cy = Math.floor(defect / cols);
      if (Math.abs((cx + 0.5) * CS - p.x) < CS * 1.1 && Math.abs((cy + 0.5) * CS - p.y) < CS * 1.1) {
        activate(defect); cov[defect] = 1; nCov++; lit[defect] = 1; found++;
        setMsg(true); updateStats();
        var old = defect; defect = -1;
        setTimeout(function () { placeDefect(); if (defect === old) placeDefect(); drawCell(defect, 0.7); loopStart(); }, 900);
      }
    });
    var loopStart = function () {
      if (running || !visible) return;
      running = true;
      var tick = function (t) {
        step(t);
        /* En mouvement réduit, pas de pulsation : la boucle s'arrête dès que la grille est stable. */
        if ((reduce && !active.length) || !visible) { running = false; return; }
        requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting;
        if (visible) loopStart();
      }, { threshold: 0 }).observe(hero);
    }
    /* Point d'observation pour les tests automatisés : position du défaut dans la page (lecture seule). */
    window.__heroDefect = function () {
      if (defect < 0) return null;
      var r = hero.getBoundingClientRect();
      return { x: r.left + (defect % cols + 0.5) * CS, y: r.top + (Math.floor(defect / cols) + 0.5) * CS };
    };
    var rt = null;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(resize, 150); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(resize);
    resize();
    /* La pulsation du défaut démarre une fois la page chargée, pour ne pas concurrencer le premier rendu. */
    var started = function () { setTimeout(loopStart, 800); };
    if (document.readyState === 'complete') started(); else window.addEventListener('load', started);
  }
})();
