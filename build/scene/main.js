// Scènes 3D du site (three.js, MIT). Source : build/scene/main.js → assets/scene.js (npm run build dans build/).
// Deux scènes, chargées après l'affichage du contenu, en pause hors écran :
//   hero(root)     — le champ de couverture : chaque cas de test est une case, trois anomalies s'y cachent.
//   pipeline(root) — la recette pilotée par le défilement : une release candidate traverse huit portes.
import {
  WebGLRenderer, Scene, PerspectiveCamera, BoxGeometry, PlaneGeometry, SphereGeometry, TubeGeometry,
  MeshStandardMaterial, MeshBasicMaterial, InstancedMesh, Mesh, Group, Object3D, Color, HemisphereLight,
  DirectionalLight, PointLight, Raycaster, Vector2, Vector3, Plane, Fog, CatmullRomCurve3, CanvasTexture,
  GridHelper, SRGBColorSpace, DynamicDrawUsage,
} from 'three';

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const NIGHT = 0x0c1722;
const css = (el, v, d) => getComputedStyle(el).getPropertyValue(v).trim() || d;
const damp = (a, b, k, dt) => a + (b - a) * (1 - Math.exp(-k * dt));
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const ease = (x) => 1 - Math.pow(1 - clamp(x, 0, 1), 3);
const DISPLAY = '"Bricolage", ui-sans-serif, system-ui, sans-serif';

function renderer(canvas) {
  const r = new WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'low-power' });
  r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  r.outputColorSpace = SRGBColorSpace;
  r.setClearColor(0x000000, 0);
  return r;
}

// Boucle de rendu active uniquement quand l'élément est visible et l'onglet affiché.
function runWhileVisible(el, frame) {
  let visible = false, raf = 0, last = 0;
  const tick = (t) => {
    raf = 0;
    if (!visible || document.hidden) return;
    const dt = last ? Math.min(0.05, (t - last) / 1000) : 0.016;
    last = t;
    frame(dt, t / 1000);
    raf = requestAnimationFrame(tick);
  };
  const start = () => { if (!raf && visible && !document.hidden) { last = 0; raf = requestAnimationFrame(tick); } };
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; start(); }, { rootMargin: '80px' }).observe(el);
  document.addEventListener('visibilitychange', start);
  return start;
}

function fit(r, cam, el) {
  const w = el.clientWidth, h = el.clientHeight;
  if (!w || !h) return;
  r.setSize(w, h, false);
  cam.aspect = w / h;
  cam.updateProjectionMatrix();
}

function textTexture(draw, w = 256, h = 256) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new CanvasTexture(c);
  t.colorSpace = SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

// Éclats de correction : petits cubes projetés puis retombés.
function sparks(scene, count = 90) {
  const m = new InstancedMesh(new BoxGeometry(0.16, 0.16, 0.16), new MeshBasicMaterial({ color: 0xffffff }), count);
  m.instanceMatrix.setUsage(DynamicDrawUsage);
  m.frustumCulled = false;
  const P = [], V = [], life = new Float32Array(count), d = new Object3D(), col = new Color();
  for (let i = 0; i < count; i++) { P.push(new Vector3()); V.push(new Vector3()); m.setColorAt(i, col.set(0xffffff)); }
  let next = 0;
  scene.add(m);
  return {
    burst(at, color, n = 18, power = 1) {
      for (let k = 0; k < n; k++) {
        const i = next++ % count;
        P[i].copy(at);
        const a = Math.random() * Math.PI * 2, up = 0.5 + Math.random();
        V[i].set(Math.cos(a) * (1 + Math.random() * 2), up * 4.5, Math.sin(a) * (1 + Math.random() * 2)).multiplyScalar(power);
        life[i] = 1;
        m.setColorAt(i, col.set(color));
      }
      m.instanceColor.needsUpdate = true;
    },
    update(dt) {
      for (let i = 0; i < count; i++) {
        if (life[i] > 0) {
          life[i] -= dt * 1.1;
          V[i].y -= 12 * dt;
          P[i].addScaledVector(V[i], dt);
          if (P[i].y < 0.05) { P[i].y = 0.05; V[i].y *= -0.35; V[i].x *= 0.7; V[i].z *= 0.7; }
        }
        const s = Math.max(0, life[i]);
        d.position.copy(P[i]);
        d.rotation.set(life[i] * 6, life[i] * 4, 0);
        d.scale.setScalar(s);
        d.updateMatrix();
        m.setMatrixAt(i, d.matrix);
      }
      m.instanceMatrix.needsUpdate = true;
    },
  };
}

/* =====================================================================
   1. Hero — le champ de couverture
   ===================================================================== */
export function hero(root) {
  const canvas = root.querySelector('canvas.field');
  if (!canvas) return;
  const R = renderer(canvas);
  const scene = new Scene();
  scene.fog = new Fog(NIGHT, 20, 46);
  const cam = new PerspectiveCamera(30, 1, 0.1, 120);
  scene.add(new HemisphereLight(0xd6ecff, 0x0c1722, 1.15));
  const sun = new DirectionalLight(0xffffff, 1.9);
  sun.position.set(-10, 20, 12);
  scene.add(sun);

  const PASS = new Color(css(root, '--pass', '#46d19a')), FAIL = new Color(css(root, '--fail', '#ff7a68'));
  const BASE = new Color('#142636'), LIFT = new Color('#2a4a63'), PASS_DIM = PASS.clone().lerp(BASE, 0.45);

  const NX = 46, NZ = 26, N = NX * NZ;
  const geo = new BoxGeometry(0.86, 1, 0.86);
  geo.translate(0, 0.5, 0);
  const mesh = new InstancedMesh(geo, new MeshStandardMaterial({ roughness: 0.5, metalness: 0.08 }), N);
  mesh.instanceMatrix.setUsage(DynamicDrawUsage);
  scene.add(mesh);
  const X = new Float32Array(N), Z = new Float32Array(N), Hh = new Float32Array(N).fill(0.2);
  const heat = new Float32Array(N), cover = new Uint8Array(N), isDef = new Uint8Array(N), onScreen = new Uint8Array(N);
  const d = new Object3D(), col = new Color();
  for (let iz = 0, i = 0; iz < NZ; iz++) for (let ix = 0; ix < NX; ix++, i++) {
    X[i] = ix - NX / 2 + 0.5; Z[i] = iz - NZ / 2 + 0.5;
    mesh.setColorAt(i, BASE);
  }
  const fx = sparks(scene);

  // Interface (HUD) : couverture, anomalies, verdict.
  const $ = (s) => root.querySelector(s);
  const gcov = $('[data-gcov]'), gbar = $('[data-gbar]'), gfound = $('[data-gfound]'), gmsg = $('[data-gmsg]');
  let defects = [], found = 0, nCover = 0, nScreen = 1, msgTimer = 0;
  const say = (txt) => {
    if (!gmsg) return;
    gmsg.textContent = txt;
    gmsg.classList.add('show');
    clearTimeout(msgTimer);
    msgTimer = setTimeout(() => gmsg.classList.remove('show'), 3600);
  };
  const hud = () => {
    const pc = Math.min(100, Math.round((nCover / nScreen) * 100));
    if (gcov) gcov.textContent = pc;
    if (gbar) gbar.style.transform = `scaleX(${pc / 100})`;
    if (gfound) gfound.textContent = found;
  };

  // Projection des cases à l'écran : on évite de cacher une anomalie sous le texte.
  const v = new Vector3();
  const screenOf = (i, y = 0.6) => {
    v.set(X[i], y, Z[i]).project(cam);
    const r = canvas.getBoundingClientRect();
    return { x: r.left + (v.x + 1) / 2 * r.width, y: r.top + (1 - v.y) / 2 * r.height, z: v.z };
  };
  const solids = () => [...root.querySelectorAll('.hero-id [data-solid], .hud')].map((el) => el.getBoundingClientRect());
  const placeDefects = () => {
    defects.forEach((i) => { isDef[i] = 0; });
    defects = [];
    const rects = solids(), r = canvas.getBoundingClientRect(), free = [];
    nScreen = 0;
    for (let i = 0; i < N; i++) {
      const p = screenOf(i, 0.2);
      const inView = p.z < 1 && p.x > r.left + 12 && p.x < r.right - 12 && p.y > r.top + 12 && p.y < r.bottom - 12;
      onScreen[i] = inView ? 1 : 0;
      if (!inView) continue;
      nScreen++;
      const under = rects.some((b) => p.x > b.left - 34 && p.x < b.right + 34 && p.y > b.top - 34 && p.y < b.bottom + 34);
      const edge = p.x < r.left + 70 || p.x > r.right - 70 || p.y < r.top + 70 || p.y > r.bottom - 60;
      if (!under && !edge && !cover[i]) free.push(i);
    }
    nScreen = Math.max(1, nScreen);
    nCover = 0;
    for (let i = 0; i < N; i++) if (cover[i] && onScreen[i]) nCover++;
    const left = 3 - found;
    for (let tries = 0; defects.length < left && tries < 400 && free.length; tries++) {
      const i = free[(Math.random() * free.length) | 0];
      if (defects.every((j) => Math.hypot(X[i] - X[j], Z[i] - Z[j]) > 5)) { defects.push(i); isDef[i] = 1; }
    }
    hud();
  };

  // Cadrage : le champ remplit le hero, incliné, avec une légère dérive au curseur.
  const look = new Vector3(), base = new Vector3();
  const frame = () => {
    fit(R, cam, canvas);
    const a = cam.aspect;
    base.set(a > 1.2 ? 2 : 0, a > 1.2 ? 15.5 : 27, a > 1.2 ? 15 : 17);
    look.set(a > 1.2 ? 3.5 : 0, 0, a > 1.2 ? 0.5 : 2);
    cam.position.copy(base);
    cam.lookAt(look);
    cam.updateMatrixWorld();
  };

  // Pointeur → case visée (intersection du rayon avec le plan du champ).
  const ray = new Raycaster(), ndc = new Vector2(), plane = new Plane(new Vector3(0, 1, 0), -0.4), hit = new Vector3();
  const drift = new Vector2();
  const cellAt = (ev) => {
    const r = canvas.getBoundingClientRect();
    ndc.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, cam);
    return ray.ray.intersectPlane(plane, hit) ? hit : null;
  };
  const brush = (p, radius = 2.3) => {
    for (let i = 0; i < N; i++) {
      const dd = Math.hypot(X[i] - p.x, Z[i] - p.z);
      if (dd < radius) {
        const k = 1 - dd / radius;
        if (k > heat[i]) heat[i] = k;
        if (k > 0.4 && !cover[i] && !isDef[i]) { cover[i] = 1; if (onScreen[i]) nCover++; }
      }
    }
    hud();
  };
  root.addEventListener('pointermove', (ev) => {
    const r = canvas.getBoundingClientRect();
    drift.set(((ev.clientX - r.left) / r.width) - 0.5, ((ev.clientY - r.top) / r.height) - 0.5);
    const p = cellAt(ev);
    if (p) brush(p);
    kick();
  }, { passive: true });
  root.addEventListener('pointerdown', (ev) => {
    if (ev.target.closest('a,button')) return;
    const p = cellAt(ev);
    if (!p) return;
    brush(p, 1.6);
    const k = defects.findIndex((i) => Math.abs(X[i] - p.x) < 1.25 && Math.abs(Z[i] - p.z) < 1.25);
    if (k < 0) return;
    const i = defects.splice(k, 1)[0];
    isDef[i] = 0; cover[i] = 1; heat[i] = 1; if (onScreen[i]) nCover++;
    found++;
    fx.burst(new Vector3(X[i], Hh[i] + 0.3, Z[i]), FAIL.getHex(), 10, 0.8);
    fx.burst(new Vector3(X[i], Hh[i] + 0.3, Z[i]), PASS.getHex(), 20, 1);
    hud();
    if (found >= 3) { root.classList.add('verdict-go'); say(root.getAttribute('data-t-all')); }
    else say(root.getAttribute('data-t-found'));
    kick();
  });

  // Point d'observation pour les tests automatisés (lecture seule).
  window.__heroDefect = () => (defects.length ? screenOf(defects[0], Hh[defects[0]]) : null);

  const kick = runWhileVisible(root, (dt, t) => {
    if (!reduce) {
      cam.position.x = damp(cam.position.x, base.x + drift.x * 2.2, 3, dt);
      cam.position.y = damp(cam.position.y, base.y - drift.y * 1.4, 3, dt);
      cam.lookAt(look);
    }
    const cool = Math.exp(-dt * 1.6);
    for (let i = 0; i < N; i++) {
      heat[i] *= reduce ? 0 : cool;
      const wave = reduce ? 0 : 0.07 * Math.sin(t * 0.9 + X[i] * 0.33 + Z[i] * 0.21);
      const pulse = isDef[i] ? 0.7 + (reduce ? 0 : 0.35 * Math.sin(t * 5 + i)) : 0;
      const target = 0.2 + wave + cover[i] * 0.32 + heat[i] * 1.35 + pulse;
      Hh[i] = reduce ? target : damp(Hh[i], target, 9, dt);
      d.position.set(X[i], 0, Z[i]);
      d.scale.set(1, Math.max(0.05, Hh[i]), 1);
      d.updateMatrix();
      mesh.setMatrixAt(i, d.matrix);
      if (isDef[i]) col.copy(FAIL);
      else if (cover[i]) col.lerpColors(PASS_DIM, PASS, Math.min(1, heat[i] * 1.4));
      else col.lerpColors(BASE, LIFT, heat[i]);
      mesh.setColorAt(i, col);
    }
    mesh.instanceMatrix.needsUpdate = true;
    mesh.instanceColor.needsUpdate = true;
    fx.update(dt);
    R.render(scene, cam);
  });

  let rt = 0;
  const relayout = () => { frame(); placeDefects(); kick(); };
  window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(relayout, 160); });
  relayout();
  root.classList.add('is-3d');
}

/* =====================================================================
   2. Méthode — la recette pilotée par le défilement
   ===================================================================== */
export function pipeline(stage) {
  const canvas = stage.querySelector('canvas');
  const section = stage.closest('.pipe');
  const blocks = [...section.querySelectorAll('.pstep')];
  if (!canvas || blocks.length !== 8) return;
  const labels = JSON.parse(stage.getAttribute('data-labels') || '[]');
  const R = renderer(canvas);
  const scene = new Scene();
  scene.fog = new Fog(NIGHT, 16, 44);
  const cam = new PerspectiveCamera(38, 1, 0.1, 150);
  scene.add(new HemisphereLight(0xd6ecff, 0x0c1722, 1.0));
  const sun = new DirectionalLight(0xffffff, 1.5);
  sun.position.set(-6, 14, 8);
  scene.add(sun);

  const PASS = new Color('#46d19a'), FAIL = new Color('#ff7a68'), IDLE = new Color('#2b4357'), INK = new Color('#eaf1ee');

  const grid = new GridHelper(140, 140, 0x25394a, 0x1a2c3b);
  grid.position.y = -0.01;
  scene.add(grid);

  // Le parcours : une courbe en S qui passe par les huit portes.
  const gatesAt = [[-5, 0, 2], [-1.5, 0, -4], [4, 0, -8], [5, 0, -15], [0, 0, -20], [-5.5, 0, -25], [-2.5, 0, -32], [3.5, 0, -37]];
  const pts = [[-8, 0, 7], ...gatesAt, [6, 0, -46], [7, 0, -52]].map((p) => new Vector3(...p));
  const curve = new CatmullRomCurve3(pts, false, 'catmullrom', 0.4);
  const SEG = 600;
  const track = new Mesh(new TubeGeometry(curve, SEG, 0.09, 6, false), new MeshBasicMaterial({ color: 0x2b4357 }));
  track.position.y = 0.06;
  scene.add(track);
  const trailGeo = new TubeGeometry(curve, SEG, 0.14, 6, false);
  const trail = new Mesh(trailGeo, new MeshBasicMaterial({ color: PASS }));
  trail.position.y = 0.07;
  scene.add(trail);
  const perSeg = trailGeo.index.count / SEG;

  // u (0..1) de chaque porte sur la courbe.
  const uOf = (p) => {
    let best = 0, bd = 1e9;
    for (let k = 0; k <= 400; k++) { const u = k / 400, dd = curve.getPointAt(u).distanceToSquared(p); if (dd < bd) { bd = dd; best = u; } }
    return best;
  };
  const gateU = gatesAt.map((g) => uOf(new Vector3(...g)));

  // Portes : deux montants, un linteau, une plaque numérotée.
  const gates = gatesAt.map((g, i) => {
    const grp = new Group();
    const u = gateU[i], tan = curve.getTangentAt(u);
    grp.position.copy(curve.getPointAt(u));
    grp.rotation.y = Math.atan2(tan.x, tan.z);
    const mat = new MeshStandardMaterial({ color: IDLE, roughness: 0.4, metalness: 0.2, emissive: new Color(0x000000) });
    const post = new BoxGeometry(0.28, 3.2, 0.28);
    const a = new Mesh(post, mat); a.position.set(-1.7, 1.6, 0);
    const b = new Mesh(post, mat); b.position.set(1.7, 1.6, 0);
    const top = new Mesh(new BoxGeometry(3.7, 0.3, 0.3), mat); top.position.set(0, 3.25, 0);
    const tex = textTexture((c, w, h) => {
      c.fillStyle = '#0c1722'; c.fillRect(0, 0, w, h);
      c.strokeStyle = '#eaf1ee'; c.lineWidth = 6; c.strokeRect(6, 6, w - 12, h - 12);
      c.fillStyle = '#eaf1ee'; c.textAlign = 'center'; c.textBaseline = 'middle';
      c.font = `800 92px ${DISPLAY}`; c.fillText(String(i + 1), w / 2, h * 0.4);
      c.font = `600 24px ${DISPLAY}`;
      const words = (labels[i] || '').split(' '); let line = '', y = h * 0.74; const lines = [];
      words.forEach((wd) => { const tt = line ? line + ' ' + wd : wd; if (c.measureText(tt).width > w - 30) { lines.push(line); line = wd; } else line = tt; });
      lines.push(line);
      lines.slice(0, 2).forEach((l, k) => c.fillText(l, w / 2, y + k * 28 - (lines.length > 1 ? 14 : 0)));
    });
    const plate = new Mesh(new PlaneGeometry(1.5, 1.5), new MeshBasicMaterial({ map: tex, transparent: true }));
    plate.position.set(0, 4.3, 0);
    const back = plate.clone(); back.rotation.y = Math.PI; back.position.z = -0.01;
    grp.add(a, b, top, plate, back);
    scene.add(grp);
    return { grp, mat };
  });

  // La release candidate, et l'anomalie qui s'y accroche à la porte 6.
  const rcMat = new MeshStandardMaterial({ color: INK, roughness: 0.3, metalness: 0.15, emissive: new Color(0x000000) });
  const rc = new Mesh(new BoxGeometry(1, 1, 1), rcMat);
  scene.add(rc);
  const halo = new PointLight(0x46d19a, 0, 8);
  scene.add(halo);
  const bug = new Mesh(new SphereGeometry(0.26, 16, 12), new MeshStandardMaterial({ color: FAIL, emissive: FAIL, emissiveIntensity: 0.6 }));
  scene.add(bug);
  const fx = sparks(scene, 60);

  // Le tampon GO, à la sortie de la dernière porte.
  const goTex = textTexture((c, w, h) => {
    c.clearRect(0, 0, w, h);
    c.strokeStyle = '#46d19a'; c.lineWidth = 22;
    c.beginPath(); c.roundRect(20, 40, w - 40, h - 80, 26); c.stroke();
    c.fillStyle = '#46d19a'; c.textAlign = 'center'; c.textBaseline = 'middle';
    c.font = `800 210px ${DISPLAY}`; c.fillText('GO', w / 2, h / 2 + 10);
  }, 512, 320);
  const go = new Mesh(new PlaneGeometry(4.2, 2.6), new MeshBasicMaterial({ map: goTex, transparent: true, depthWrite: false }));
  const goPos = new Vector3(7, 2.4, -55);
  go.position.copy(goPos);
  scene.add(go);

  // Défilement → progression continue p ∈ [0, 8] (chaque bloc d'étape compte pour 1).
  const pstep = stage.querySelector('[data-pstep]'), pname = stage.querySelector('[data-pname]');
  const dots = [...stage.querySelectorAll('[data-pgo]')];
  let p = 0, shown = 0, active = -1, zapped = false, fixedFx = false;
  const progress = () => {
    const anchor = window.innerHeight * 0.55;
    let q = 0;
    for (let i = 0; i < 8; i++) {
      const r = blocks[i].getBoundingClientRect();
      if (r.top <= anchor) q = i + clamp((anchor - r.top) / r.height, 0, 1);
    }
    return clamp(q, 0, 8);
  };
  const setActive = (i) => {
    if (i === active) return;
    active = i;
    blocks.forEach((b, k) => b.classList.toggle('on', k === i));
    dots.forEach((dd, k) => { dd.classList.toggle('on', k === i); dd.classList.toggle('done', k < i); if (k === i) dd.setAttribute('aria-current', 'step'); else dd.removeAttribute('aria-current'); });
    if (pstep) pstep.textContent = i + 1;
    if (pname) pname.textContent = labels[i] || '';
  };

  const camPos = new Vector3(), camLook = new Vector3(), tmp = new Vector3();
  const camOff = new Vector3(2.5, 11.5, 11);
  let first = true;
  const kick = runWhileVisible(section, (dt, t) => {
    p = progress();
    shown = reduce ? p : damp(shown, p, 6, dt);
    setActive(Math.min(7, Math.floor(p)));
    // p = k + 0.5 → la release candidate est sous la porte k.
    const gate = (q) => {
      const k = clamp(Math.floor(q - 0.5), -1, 7), f = q - 0.5 - k;
      const u0 = k < 0 ? 0.01 : gateU[k], u1 = k >= 7 ? 0.97 : gateU[k + 1];
      return u0 + (u1 - u0) * clamp(f, 0, 1);
    };
    const u = clamp(gate(shown), 0.005, 0.975);
    const pos = curve.getPointAt(u), tan = curve.getTangentAt(u);
    const inBug = shown > 4.95 && shown < 5.8;
    const shake = inBug && !reduce ? Math.sin(t * 38) * 0.08 : 0;
    rc.position.set(pos.x + shake, 0.62 + (reduce ? 0 : Math.sin(t * 2.4) * 0.06), pos.z);
    rc.rotation.y = Math.atan2(tan.x, tan.z) + (reduce ? 0 : t * 0.4);
    rcMat.color.copy(inBug ? FAIL : shown > 0.5 ? PASS : INK);
    rcMat.emissive.copy(rcMat.color).multiplyScalar(0.28);
    halo.position.set(pos.x, 1.6, pos.z);
    halo.color.copy(rcMat.color);
    halo.intensity = 6;
    // L'anomalie : apparaît à l'approche de la porte 6, tourne autour, puis est corrigée.
    if (shown > 4.8 && shown < 5.8) {
      zapped = false;
      bug.visible = true;
      const a = t * 4;
      bug.position.set(pos.x + Math.cos(a) * 0.95, 1.05 + Math.sin(t * 6) * 0.15, pos.z + Math.sin(a) * 0.95);
      bug.scale.setScalar(clamp((shown - 4.8) * 5, 0, 1));
    } else {
      if (shown >= 5.8 && !zapped && bug.visible) { fx.burst(bug.position.clone(), 0xff7a68, 12, 0.6); fx.burst(rc.position.clone(), 0x46d19a, 16, 0.8); }
      zapped = shown >= 5.8;
      bug.visible = false;
    }
    // Portes franchies : vertes ; porte courante : surlignée.
    gates.forEach((g, k) => {
      const passed = shown > k + 0.5, isBug = k === 5 && inBug;
      g.mat.color.copy(isBug ? FAIL : passed ? PASS : IDLE);
      g.mat.emissive.copy(g.mat.color).multiplyScalar(passed || isBug ? 0.35 : 0);
    });
    trailGeo.setDrawRange(0, Math.floor((u * SEG)) * perSeg);
    // GO : tombe et se pose quand la dernière porte est franchie.
    const g = ease((shown - 7.35) / 0.45);
    go.visible = g > 0;
    go.scale.setScalar(0.6 + 0.4 * g);
    go.position.set(goPos.x, goPos.y + (1 - g) * 4, goPos.z);
    go.rotation.z = (1 - g) * 0.5 - 0.1;
    if (g >= 1 && !fixedFx) { fixedFx = true; fx.burst(goPos.clone().setY(0.5), 0x46d19a, 30, 1.2); }
    if (g < 0.5) fixedFx = false;
    // Caméra : vue de trois quarts, surélevée, qui suit la release candidate puis recule pour le verdict.
    tmp.copy(pos).add(camOff);
    const end = ease((shown - 7.25) / 0.6);
    tmp.lerp(goPos.clone().add(new Vector3(-1, 4.5, 12.5)), end);
    const lookT = pos.clone().add(new Vector3(0, 0.3, -4.5)).lerp(goPos.clone().setY(1.4), end);
    if (first || reduce) { camPos.copy(tmp); camLook.copy(lookT); first = false; }
    camPos.x = damp(camPos.x, tmp.x, 3.2, dt); camPos.y = damp(camPos.y, tmp.y, 3.2, dt); camPos.z = damp(camPos.z, tmp.z, 3.2, dt);
    camLook.x = damp(camLook.x, lookT.x, 4, dt); camLook.y = damp(camLook.y, lookT.y, 4, dt); camLook.z = damp(camLook.z, lookT.z, 4, dt);
    cam.position.copy(camPos);
    cam.lookAt(camLook);
    fx.update(dt);
    rc.parent.updateMatrixWorld();
    R.render(scene, cam);
  });

  // L'étape active suit le défilement directement, indépendamment de la vitesse de rendu 3D.
  let sTick = 0;
  const onScroll = () => {
    kick();
    if (sTick) return;
    sTick = requestAnimationFrame(() => { sTick = 0; p = progress(); setActive(Math.min(7, Math.floor(p))); });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  const resize = () => { fit(R, cam, canvas); kick(); };
  window.addEventListener('resize', resize);
  new ResizeObserver(resize).observe(canvas);
  resize();
  section.classList.add('is-3d');
  window.__pipeProgress = () => ({ p, active });
}
