(function () {
  'use strict';

  var root = document.documentElement;
  var me = document.currentScript;
  var sceneURL = me ? new URL(me.getAttribute('data-scene') || 'scene.js', me.src).href : null;
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

  /* ---------- Menu des sections (petit écran) ---------- */
  var menu = $('.menu');
  if (menu) {
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { menu.open = false; }); });
    document.addEventListener('click', function (ev) { if (menu.open && !menu.contains(ev.target)) menu.open = false; });
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && menu.open) { menu.open = false; $('summary', menu).focus(); } });
  }

  /* ---------- Chasse aux anomalies : 5 bugs cachés dans la page ---------- */
  var bugs = $$('[data-bug]'), hunt = $('.hunt'), huntN = $('[data-hunt]'), toast = $('[data-toast]');
  var nFound = 0, toastTimer = null;
  function showToast(msg, cta) {
    if (!toast) return;
    $('[data-toast-msg]', toast).textContent = msg;
    $('.toast-cta', toast).hidden = !cta;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove('show'); }, cta ? 9000 : 3800);
  }
  bugs.forEach(function (b) {
    b.addEventListener('click', function () {
      if (b.classList.contains('found')) return;
      b.classList.add('found');
      b.setAttribute('aria-disabled', 'true');
      nFound++;
      if (huntN) huntN.textContent = nFound;
      if (hunt) { hunt.classList.remove('bump'); void hunt.offsetWidth; hunt.classList.add('bump'); hunt.classList.toggle('done', nFound === bugs.length); }
      var left = bugs.length - nFound;
      if (!toast) return;
      if (!left) showToast(toast.getAttribute('data-t-done'), true);
      else if (left === 1) showToast(toast.getAttribute('data-t-found1'));
      else showToast(toast.getAttribute('data-t-found').replace('{n}', nFound).replace('{r}', left));
    });
  });

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
    var gcov = $('[data-gcov]', hero), gbar = $('[data-gbar]', hero), gfound = $('[data-gfound]', hero), gmsg = $('[data-gmsg]', hero);
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
      var pc = Math.min(100, Math.round(nCov / (cols * nrows) * 100));
      if (gcov) gcov.textContent = pc;
      if (gbar) gbar.style.transform = 'scaleX(' + pc / 100 + ')';
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
      if (hero.classList.contains('is-3d')) return;
      var p = local(ev); touch(p.x, p.y);
      if (reduce && !running) step(0);
      loopStart();
    });
    hero.addEventListener('click', function (ev) {
      if (defect < 0 || hero.classList.contains('is-3d')) return;
      var p = local(ev), cx = defect % cols, cy = Math.floor(defect / cols);
      if (Math.abs((cx + 0.5) * CS - p.x) < CS * 1.1 && Math.abs((cy + 0.5) * CS - p.y) < CS * 1.1) {
        activate(defect); cov[defect] = 1; nCov++; lit[defect] = 1; found++;
        setMsg(true); updateStats();
        if (found >= 3) { hero.classList.add('verdict-go'); if (gmsg) gmsg.textContent = hero.getAttribute('data-t-all'); }
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
        if ((reduce && !active.length) || !visible || hero.classList.contains('is-3d')) { running = false; return; }
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
    window.__heroDefect2d = function () {
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

  /* ---------- Scènes 3D (WebGL) : chargées après le contenu, jamais bloquantes ----------
     Pas de 3D si le rendu WebGL est logiciel (machine virtuelle, vieux pilote) ou en mode économie de données :
     le champ 2D et la liste des étapes restent alors affichés. La 3D démarre à la première interaction,
     ou peu après le chargement si le visiteur ne bouge pas. */
  var gpuOK = (function () {
    try {
      var c = document.createElement('canvas'), gl = c.getContext('webgl2') || c.getContext('webgl');
      if (!gl) return false;
      var ext = gl.getExtension('WEBGL_debug_renderer_info');
      var name = ext ? String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)) : '';
      var lose = gl.getExtension('WEBGL_lose_context'); if (lose) lose.loseContext();
      return window.__force3d === true || !/swiftshader|llvmpipe|software|basic render/i.test(name);
    } catch (e) { return false; }
  })();
  var saveData = navigator.connection && navigator.connection.saveData;
  if (gpuOK && !saveData && sceneURL) {
    var started3d = false;
    var load3d = function () {
      if (started3d) return;
      started3d = true;
      ['pointermove', 'pointerdown', 'scroll', 'keydown', 'touchstart'].forEach(function (t) { window.removeEventListener(t, load3d); });
      import(sceneURL).then(function (m) {
        var st = $('[data-pipe]');
        try { if (hero) m.hero(hero); } catch (e) { /* le champ 2D reste affiché */ }
        try { if (st) m.pipeline(st); } catch (e) { /* les étapes restent lisibles en liste */ }
      }).catch(function () { /* hors ligne ou bloqué : la page reste complète */ });
    };
    var arm = function () {
      ['pointermove', 'pointerdown', 'scroll', 'keydown', 'touchstart'].forEach(function (t) { window.addEventListener(t, load3d, { passive: true, once: true }); });
      setTimeout(load3d, window.__force3d ? 0 : 3500);
    };
    if (document.readyState === 'complete') arm(); else window.addEventListener('load', arm);
  }
})();
