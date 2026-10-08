// Scènes 3D du site (three.js, MIT). Source : build/scene/main.js → assets/scene.js (npm run build dans build/).
// Deux scènes, chargées après l'affichage du contenu, en pause hors écran :
//   hero(root)     — le champ de couverture : chaque cas de test est une case, trois anomalies s'y cachent.
//   pipeline(root) — la recette pilotée par le défilement : une release candidate traverse huit portes.
import {
  WebGLRenderer, Scene, PerspectiveCamera, BoxGeometry, PlaneGeometry, SphereGeometry, TubeGeometry,
  MeshStandardMaterial, MeshBasicMaterial, InstancedMesh, Mesh, Group, Object3D, Color, HemisphereLight,
  DirectionalLight, PointLight, Raycaster, Vector2, Vector3, Plane, Fog, CatmullRomCurve3, CanvasTexture,
  GridHelper, SRGBColorSpace, DynamicDrawUsage, TorusGeometry, MeshPhysicalMaterial, ShadowMaterial,
  PCFSoftShadowMap, ACESFilmicToneMapping, PMREMGenerator, AmbientLight,
} from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';

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
    const dt = last ? Math.min(0.2, (t - last) / 1000) : 0.016;
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
   Registre « maison » : sol ivoire, lumière de studio, huit anneaux de métal brossé,
   une sphère de porcelaine qui glisse le long d'un fil d'or. Aucun effet appuyé.
   ===================================================================== */
export function pipeline(stage) {
  const canvas = stage.querySelector('canvas');
  const section = stage.closest('.pipe');
  const blocks = [...section.querySelectorAll('.pstep')];
  if (!canvas || blocks.length !== 8) return;
  const labels = JSON.parse(stage.getAttribute('data-labels') || '[]');

  const IVORY = new Color(css(section, '--pipe-bg', '#f3efe7'));
  const R = renderer(canvas);
  R.shadowMap.enabled = true;
  R.shadowMap.type = PCFSoftShadowMap;
  R.toneMapping = ACESFilmicToneMapping;
  R.toneMappingExposure = 1.05;
  const scene = new Scene();
  scene.fog = new Fog(IVORY, 15, 34);
  const pmrem = new PMREMGenerator(R);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.03).texture;
  const cam = new PerspectiveCamera(30, 1, 0.1, 120);

  scene.add(new AmbientLight(0xfff6ea, 0.35));
  const key = new DirectionalLight(0xfff3e2, 2.1);
  key.position.set(-6, 14, 8);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.radius = 9;
  key.shadow.bias = -0.0004;
  Object.assign(key.shadow.camera, { left: -16, right: 16, top: 16, bottom: -16, near: 1, far: 50 });
  scene.add(key, key.target);

  // Sol : n'affiche que les ombres, il se fond dans l'ivoire de la page.
  const floor = new Mesh(new PlaneGeometry(200, 200), new ShadowMaterial({ opacity: 0.13 }));
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  scene.add(floor);

  // Huit anneaux, alignés sur une courbe douce.
  const H = 1.75, RAD = 1.45;
  const at = (i) => new Vector3(i * 3.4, H, Math.sin(i * 0.55) * 1.1);
  const ringPos = Array.from({ length: 8 }, (_, i) => at(i));
  const curve = new CatmullRomCurve3([at(-1.6), ...ringPos, at(8.6)], false, 'centripetal');
  const PLATINUM = new Color('#cfc8bb'), GOLD = new Color('#b8925a'), TERRA = new Color('#a5543b');
  const ringGeo = new TorusGeometry(RAD, 0.03, 24, 220);
  const rings = ringPos.map((pos, i) => {
    const mat = new MeshStandardMaterial({ color: PLATINUM.clone(), metalness: 1, roughness: 0.32, envMapIntensity: 1.1 });
    const m = new Mesh(ringGeo, mat);
    const u = i / 8;
    m.position.copy(pos);
    const t = curve.getTangentAt(clamp((i + 1.6) / 10.2, 0, 1));
    m.lookAt(pos.clone().add(t));
    m.castShadow = true;
    scene.add(m);
    return { m, mat, u };
  });
  // u de chaque anneau sur la courbe (recherche du point le plus proche).
  const uOf = (p) => {
    let best = 0, bd = 1e9;
    for (let k = 0; k <= 600; k++) { const u = k / 600, dd = curve.getPointAt(u).distanceToSquared(p); if (dd < bd) { bd = dd; best = u; } }
    return best;
  };
  const ringU = ringPos.map(uOf);

  // Le fil d'or : se déroule derrière la sphère.
  const SEG = 700;
  const threadGeo = new TubeGeometry(curve, SEG, 0.007, 6, false);
  const thread = new Mesh(threadGeo, new MeshStandardMaterial({ color: GOLD, metalness: 1, roughness: 0.25 }));
  scene.add(thread);
  const perSeg = threadGeo.index.count / SEG;

  // La sphère : porcelaine laquée.
  const pearl = new Mesh(new SphereGeometry(0.42, 64, 48), new MeshPhysicalMaterial({
    color: 0xf7f3ec, roughness: 0.18, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.08, sheen: 0.4, sheenColor: new Color(0xffe9cc),
  }));
  pearl.castShadow = true;
  scene.add(pearl);
  // Un liseré terre cuite, discret, autour de la sphère pendant l'anomalie (étape 6).
  const flawMat = new MeshStandardMaterial({ color: TERRA, metalness: 0.6, roughness: 0.35, transparent: true, opacity: 0 });
  const flaw = new Mesh(new TorusGeometry(0.62, 0.012, 12, 120), flawMat);
  scene.add(flaw);

  // Défilement → progression continue p ∈ [0, 8].
  const pstep = stage.querySelector('[data-pstep]'), pname = stage.querySelector('[data-pname]');
  const dots = [...stage.querySelectorAll('[data-pgo]')];
  let p = 0, shown = 0, active = -1;
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
    if (pstep) pstep.textContent = String(i + 1).padStart(2, '0');
    if (pname) pname.textContent = labels[i] || '';
  };

  // q = k + 0.5 → la sphère est au cœur de l'anneau k.
  const uAt = (q) => {
    const k = clamp(Math.floor(q - 0.5), -1, 7), f = clamp(q - 0.5 - k, 0, 1);
    const u0 = k < 0 ? 0.02 : ringU[k], u1 = k >= 7 ? 0.97 : ringU[k + 1];
    // Ralenti au passage de chaque anneau : la sphère s'y attarde, comme une pièce qu'on présente.
    const e = f < 0.5 ? 4 * f * f * f : 1 - Math.pow(-2 * f + 2, 3) / 2;
    return u0 + (u1 - u0) * e;
  };

  const camPos = new Vector3(), camLook = new Vector3(), want = new Vector3(), look = new Vector3();
  const center = ringPos[0].clone().add(ringPos[7]).multiplyScalar(0.5);
  // Plan final : les huit anneaux alignés en perspective, comme une vitrine.
  const finalCam = ringPos[0].clone().add(new Vector3(-7.5, 1.6, 7.5)), finalLook = center.clone().setY(H - 0.1);
  let first = true;
  const kick = runWhileVisible(section, (dt, t) => {
    p = progress();
    shown = reduce ? p : damp(shown, p, 2.4, dt);
    setActive(Math.min(7, Math.floor(p)));
    const u = clamp(uAt(shown), 0.01, 0.975);
    const pos = curve.getPointAt(u), tan = curve.getTangentAt(u);
    const float = reduce ? 0 : Math.sin(t * 0.9) * 0.025;
    pearl.position.set(pos.x, pos.y + float, pos.z);
    pearl.rotation.y += reduce ? 0 : dt * 0.25;

    // Anneaux : platine avant le passage, or après ; l'anneau 6 vire à la terre cuite pendant l'anomalie.
    const flawK = clamp((shown - 4.9) / 0.35, 0, 1) * (1 - clamp((shown - 5.75) / 0.35, 0, 1));
    rings.forEach((r, k) => {
      const passed = clamp((shown - (k + 0.35)) / 0.3, 0, 1);
      r.mat.color.lerpColors(PLATINUM, GOLD, passed);
      if (k === 5) r.mat.color.lerp(TERRA, flawK);
      r.mat.roughness = 0.32 - passed * 0.1;
    });
    flaw.position.copy(pearl.position);
    flaw.lookAt(pearl.position.clone().add(tan));
    flaw.scale.setScalar(1 + (1 - flawK) * 0.4);
    flawMat.opacity = flawK;
    flaw.visible = flawK > 0.01;

    threadGeo.setDrawRange(0, Math.floor(u * SEG) * perSeg);

    // Caméra : plan de trois quarts à hauteur d'objet ; à la fin, recul lent qui révèle les huit anneaux.
    const end = clamp((shown - 6.95) / 0.75, 0, 1), e = end * end * (3 - 2 * end);
    want.set(pos.x - 2.2, pos.y + 1.4, pos.z + 10.5).lerp(finalCam, e);
    look.copy(pos).addScaledVector(tan, 0.9).setY(H - 0.15).lerp(finalLook, e);
    scene.fog.near = 15 + e * 10; scene.fog.far = 34 + e * 22;
    if (!reduce) want.y += Math.sin(t * 0.35) * 0.08;
    if (first || reduce) { camPos.copy(want); camLook.copy(look); first = false; }
    camPos.x = damp(camPos.x, want.x, 2, dt); camPos.y = damp(camPos.y, want.y, 2, dt); camPos.z = damp(camPos.z, want.z, 2, dt);
    camLook.x = damp(camLook.x, look.x, 2.4, dt); camLook.y = damp(camLook.y, look.y, 2.4, dt); camLook.z = damp(camLook.z, look.z, 2.4, dt);
    cam.position.copy(camPos);
    cam.lookAt(camLook);
    key.position.set(pos.x - 6, 14, pos.z + 8);
    key.target.position.copy(pos).setY(0);
    stage.classList.toggle('done', shown > 7.55);
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
