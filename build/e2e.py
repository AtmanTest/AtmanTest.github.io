#!/usr/bin/env python3
"""Tests d'interaction (Playwright) : onglets, matrice, thème, langue, menu, copie d'e-mail,
lecture sans JavaScript, absence de défilement horizontal de 360 à 1920 px.
Usage : python3 build/e2e.py   (nécessite : pip install playwright && playwright install chromium)
"""
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

expect.set_options(timeout=6000)

ROOT = Path(__file__).resolve().parent.parent
results = []


def case(name):
    def deco(fn):
        def run(*a):
            try:
                fn(*a)
                results.append((True, name, ""))
            except Exception as ex:  # noqa: BLE001 — on consigne l'anomalie et on continue la campagne
                results.append((False, name, str(ex).splitlines()[0][:200]))
        run.__name__ = fn.__name__
        return run
    return deco


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@case("Recette 3D : le défilement pilote l'étape active")
def t_pipe_scroll(pg, url):
    pg.goto(url)
    pg.wait_for_function("document.querySelector('.pipe').classList.contains('is-3d')", timeout=15000)
    pg.evaluate("document.getElementById('etape-6').scrollIntoView({block:'center',behavior:'instant'})")
    expect(pg.locator("#etape-6")).to_have_class(re.compile(r"\bon\b"))
    expect(pg.locator('.pipe-nav a[data-pgo="5"]')).to_have_attribute("aria-current", "step")
    expect(pg.locator("[data-pstep]")).to_have_text("6")
    expect(pg.locator('.pipe-nav a.done')).to_have_count(5)


@case("Recette 3D : la navigation par étape mène au bon bloc")
def t_pipe_nav(pg, url):
    pg.goto(url)
    pg.wait_for_function("document.querySelector('.pipe').classList.contains('is-3d')", timeout=15000)
    pg.evaluate("document.getElementById('chaine').scrollIntoView({behavior:'instant'})")
    pg.locator('.pipe-nav a[data-pgo="2"]').click()
    expect(pg.locator("#etape-3")).to_be_in_viewport()


@case("Recette 3D : le GO apparaît en fin de parcours")
def t_pipe_go(pg, url):
    pg.goto(url)
    pg.wait_for_function("document.querySelector('.pipe').classList.contains('is-3d')", timeout=15000)
    pg.evaluate("window.scrollTo({top: document.querySelector('.pipe').offsetTop + document.querySelector('.pipe').offsetHeight - innerHeight, behavior:'instant'})")
    pg.wait_for_function("window.__pipeProgress().p > 7.6", timeout=5000)
    expect(pg.locator("[data-pstep]")).to_have_text("8")


@case("Chasse aux anomalies : 5 bugs, compteur et message final")
def t_hunt(pg, url):
    pg.goto(url)
    bugs = pg.locator("[data-bug]")
    expect(bugs).to_have_count(5)
    for i in range(5):
        bugs.nth(i).scroll_into_view_if_needed()
        bugs.nth(i).click()
    expect(pg.locator("[data-hunt]")).to_have_text("5")
    expect(pg.locator("[data-toast]")).to_have_class(re.compile(r"\bshow\b"))
    expect(pg.locator(".toast-cta")).to_be_visible()


@case("Thème : bascule et mémorisation")
def t_theme(pg, url):
    pg.goto(url)
    html = pg.locator("html")
    pg.locator("#theme").click()
    expect(html).to_have_attribute("data-theme", "dark")
    pg.reload()
    expect(html).to_have_attribute("data-theme", "dark")
    pg.locator("#theme").click()
    expect(html).to_have_attribute("data-theme", "light")


@case("Langue : FR ⇄ EN conserve la structure")
def t_lang(pg, url):
    pg.goto(url)
    pg.locator("a.lang").click()
    expect(pg.locator("html")).to_have_attribute("lang", "en")
    expect(pg.locator("h1 .role")).to_have_text("Senior QA Engineer")
    pg.locator("a.lang").click()
    expect(pg.locator("html")).to_have_attribute("lang", "fr")


@case("Copie de l'adresse e-mail")
def t_copy(pg, url):
    pg.context.grant_permissions(["clipboard-read", "clipboard-write"])
    pg.goto(url + "#contact")
    pg.locator("[data-copy]").click()
    expect(pg.locator("[data-cstatus]")).not_to_be_empty()
    assert pg.evaluate("navigator.clipboard.readText()") == "thasin@live.com"
    href = pg.locator('.contact a.btn.primary').get_attribute("href")
    assert href.startswith("mailto:thasin@live.com?subject="), href


@case("Frise : un clic ouvre la mission")
def t_timeline(pg, url):
    pg.goto(url)
    expect(pg.locator("#job-oodrive")).not_to_have_attribute("open", "")
    pg.locator('.bar[data-job="job-oodrive"]').click()
    expect(pg.locator("#job-oodrive")).to_have_attribute("open", "")


@case("Hero 3D : couvrir le champ, corriger 3 anomalies, obtenir le GO")
def t_hero(pg, url):
    pg.goto(url)
    pg.wait_for_function("document.querySelector('.hero').classList.contains('is-3d')", timeout=15000)
    for x in range(700, 1400, 20):
        pg.mouse.move(x, 600)
    assert int(pg.locator("[data-gcov]").inner_text()) > 0
    for n in range(1, 4):
        pos = pg.evaluate("window.__heroDefect()")
        assert pos, f"anomalie {n} introuvable"
        pg.mouse.click(pos["x"], pos["y"])
        expect(pg.locator("[data-gfound]")).to_have_text(str(n))
    expect(pg.locator(".hero")).to_have_class(re.compile(r"verdict-go"))
    expect(pg.locator(".hud .stamp")).to_be_visible()


@case("Menu des sections (mobile) : ouverture, lien, fermeture")
def t_menu(pg, url):
    pg.set_viewport_size({"width": 375, "height": 760})
    pg.goto(url)
    pg.locator(".menu summary").click()
    expect(pg.locator(".menu-in")).to_be_visible()
    pg.locator('.menu-in a[href="#parcours"]').click()
    expect(pg.locator(".menu")).not_to_have_attribute("open", "")


@case("Responsive : aucun défilement horizontal, 360 → 1920 px")
def t_widths(pg, url):
    bad = []
    for w in (360, 390, 768, 1024, 1280, 1920):
        for path in ("", "en/"):
            pg.set_viewport_size({"width": w, "height": 900})
            pg.goto(url + path)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            if sw > w:
                bad.append(f"{path or 'fr'}@{w}: {sw}")
    assert not bad, ", ".join(bad)


@case("Cibles tactiles ≥ 44 px (mobile)")
def t_targets(pg, url):
    pg.set_viewport_size({"width": 390, "height": 844})
    pg.goto(url)
    small = pg.evaluate("""() => [...document.querySelectorAll('.nav a.lang, #theme, .menu summary, .btn, .bug')]
        .filter(el => el.offsetParent).map(el => [el.className, el.getBoundingClientRect().height])
        .filter(([, h]) => h < 44)""")
    assert not small, small


@case("Sans JavaScript : tout le contenu reste lisible")
def t_nojs(browser, url):
    ctx = browser.new_context(java_script_enabled=False)
    pg = ctx.new_page()
    pg.goto(url)
    for i in range(1, 9):
        expect(pg.locator(f"#etape-{i}")).to_be_visible()
    expect(pg.locator("#job-bred .j-body")).to_be_visible()
    expect(pg.locator(".skills")).to_be_visible()
    expect(pg.locator(".bug").first).to_be_hidden()
    ctx.close()


@case("Mouvement réduit : scènes chargées, étape suivie au défilement")
def t_reduced(browser, url):
    ctx = browser.new_context(reduced_motion="reduce", viewport={"width": 1440, "height": 900})
    ctx.add_init_script("window.__force3d = true")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda ex: errs.append(str(ex)))
    pg.goto(url)
    pg.wait_for_function("document.querySelector('.hero').classList.contains('is-3d')", timeout=15000)
    pg.evaluate("document.getElementById('etape-6').scrollIntoView({block:'center',behavior:'instant'})")
    expect(pg.locator("[data-pstep]")).to_have_text("6")
    assert not errs, errs
    ctx.close()


if __name__ == "__main__":
    port = free_port()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "-d", str(ROOT)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)
    url = f"http://127.0.0.1:{port}/"
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
            for fn in (t_hero, t_pipe_scroll, t_pipe_nav, t_pipe_go, t_hunt, t_theme, t_lang, t_copy, t_timeline,
                       t_menu, t_widths, t_targets):
                ctx = browser.new_context(viewport={"width": 1440, "height": 900})
                ctx.add_init_script("window.__force3d = true")  # le navigateur de test rend WebGL en logiciel
                pg = ctx.new_page()
                pg.on("pageerror", lambda ex: errors.append(str(ex)))
                pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                fn(pg, url)
                ctx.close()
            t_nojs(browser, url)
            t_reduced(browser, url)
            browser.close()
    finally:
        srv.terminate()
    if errors:
        results.append((False, "Console sans erreur", "; ".join(sorted(set(errors)))[:300]))
    else:
        results.append((True, "Console sans erreur", ""))
    for ok, name, why in results:
        print(("  ✓ " if ok else "  ✗ ") + name + ("" if ok else f" — {why}"))
    ko = sum(1 for ok, *_ in results if not ok)
    print(f"{len(results) - ko}/{len(results)} cas passés")
    sys.exit(1 if ko else 0)
