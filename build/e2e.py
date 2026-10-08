#!/usr/bin/env python3
"""Tests d'interaction (Playwright) : onglets, matrice, thème, langue, menu, copie d'e-mail,
lecture sans JavaScript, absence de défilement horizontal de 360 à 1920 px.
Usage : python3 build/e2e.py   (nécessite : pip install playwright && playwright install chromium)
"""
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

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


@case("Chaîne QA : clic, flèches, Début/Fin")
def t_tabs(pg, url):
    pg.goto(url + "#chaine")
    tabs = pg.locator(".step-btn")
    expect(tabs).to_have_count(8)
    tabs.nth(2).click()
    expect(tabs.nth(2)).to_have_attribute("aria-selected", "true")
    expect(pg.locator("#panel-2")).to_be_visible()
    expect(pg.locator("#panel-0")).to_be_hidden()
    pg.keyboard.press("ArrowRight")
    expect(tabs.nth(3)).to_be_focused()
    expect(pg.locator("#panel-3")).to_be_visible()
    pg.keyboard.press("End")
    expect(tabs.nth(7)).to_have_attribute("aria-selected", "true")
    pg.keyboard.press("ArrowRight")
    expect(tabs.nth(0)).to_have_attribute("aria-selected", "true")
    expect(pg.locator(".stepper li.done")).to_have_count(0)


@case("Chaîne QA : lecture automatique puis pause")
def t_play(pg, url):
    pg.goto(url + "#chaine")
    btn = pg.locator("[data-play]")
    btn.click()
    expect(btn).to_have_attribute("aria-pressed", "true")
    expect(pg.locator(".step-btn").nth(1)).to_have_attribute("aria-selected", "true", timeout=5000)
    btn.click()
    expect(btn).to_have_attribute("aria-pressed", "false")


@case("Matrice : un outil montre ses missions")
def t_matrix_row(pg, url):
    pg.goto(url + "#competences")
    pg.locator('tr[data-tool="Xray"] .row-btn').click()
    st = pg.locator("[data-mstatus]")
    for name in ("BRED", "Accor", "Visiodent"):
        expect(st).to_contain_text(name)
    expect(st).not_to_contain_text("Oodrive")
    pg.locator('tr[data-tool="Xray"] .row-btn').click()
    expect(pg.locator(".matrix.has-sel")).to_have_count(0)


@case("Matrice : une mission montre sa pile")
def t_matrix_col(pg, url):
    pg.goto(url + "#competences")
    pg.locator('.col-btn[data-col="vinci"]').click()
    st = pg.locator("[data-mstatus]")
    for name in ("TestRail", "Redmine", "SAP BPC / HANA"):
        expect(st).to_contain_text(name)
    pg.locator("[data-reset]").click()
    expect(pg.locator('.col-btn[aria-pressed="true"]')).to_have_count(0)


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


@case("Hero : un défaut se cache dans la grille et se corrige")
def t_hero(pg, url):
    pg.goto(url)
    pg.wait_for_timeout(400)
    for x in range(40, 1400, 40):
        pg.mouse.move(x, 820)
    assert int(pg.locator("[data-gcov]").inner_text()) > 0
    pos = pg.evaluate("window.__heroDefect && window.__heroDefect()")
    assert pos, "défaut introuvable"
    pg.mouse.click(pos["x"], pos["y"])
    expect(pg.locator("[data-gfound]")).to_have_text("1")


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
    small = pg.evaluate("""() => [...document.querySelectorAll('.nav a.lang, #theme, .menu summary, .btn, .step-btn, .play')]
        .filter(el => el.offsetParent).map(el => [el.className, el.getBoundingClientRect().height])
        .filter(([, h]) => h < 44)""")
    assert not small, small


@case("Sans JavaScript : tout le contenu reste lisible")
def t_nojs(browser, url):
    ctx = browser.new_context(java_script_enabled=False)
    pg = ctx.new_page()
    pg.goto(url)
    for i in range(8):
        expect(pg.locator(f"#panel-{i}")).to_be_visible()
    expect(pg.locator("#job-bred .j-body")).to_be_visible()
    expect(pg.locator(".stamp")).to_be_visible()
    ctx.close()


@case("Mouvement réduit : verdict et coches affichés d'emblée")
def t_reduced(browser, url):
    ctx = browser.new_context(reduced_motion="reduce")
    pg = ctx.new_page()
    pg.goto(url)
    op = pg.evaluate("getComputedStyle(document.querySelector('.stamp')).opacity")
    assert op == "1", op
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
            browser = p.chromium.launch()
            for fn in (t_tabs, t_play, t_matrix_row, t_matrix_col, t_theme, t_lang, t_copy, t_timeline,
                       t_hero, t_menu, t_widths, t_targets):
                ctx = browser.new_context(viewport={"width": 1440, "height": 900})
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
