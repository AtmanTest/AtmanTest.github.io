#!/usr/bin/env python3
"""Tests d'interaction (Playwright) : appels à l'action, chaîne QA (onglets clavier), missions, thème, langue,
menu mobile, copie d'e-mail, lecture sans JavaScript, absence de défilement horizontal de 360 à 1920 px.
Usage : python3 build/e2e.py   (nécessite : pip install playwright && playwright install chromium)
"""
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

expect.set_options(timeout=8000)
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


@case("Premier écran : nom, poste, photo, disponibilité, deux appels à l'action")
def t_fold(pg, url):
    pg.goto(url)
    expect(pg.locator("h1")).to_have_text("Thasin Jahangir")
    expect(pg.locator(".card-night .role")).to_have_text("Ingénieur QA Senior")
    expect(pg.locator(".photo img")).to_be_in_viewport()
    assert pg.evaluate("document.querySelector('.photo img').naturalWidth") > 0, "photo non chargée"
    expect(pg.locator(".chip.on")).to_contain_text("disponible")
    expect(pg.locator(".card-night .btn.primary")).to_be_in_viewport()
    href = pg.locator(".card-night .btn.ghost").get_attribute("href")
    assert href.endswith("_FR.pdf"), href
    r = pg.request.get(url + href)
    assert r.ok and r.headers["content-type"].startswith("application/pdf"), r.status


@case("Colonne contact : toujours visible en défilant (bureau)")
def t_sticky(pg, url):
    pg.goto(url)
    pg.evaluate("document.getElementById('competences').scrollIntoView({behavior:'instant'})")
    expect(pg.locator(".side-card .btn.primary")).to_be_in_viewport()


@case("Chaîne QA : clic, flèches, Début / Fin")
def t_tabs(pg, url):
    pg.goto(url + "#chaine")
    tabs = pg.locator(".tile")
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


@case("Missions : tout déplier puis tout replier")
def t_expand(pg, url):
    pg.goto(url + "#parcours")
    btn = pg.locator("[data-expand]")
    btn.click()
    assert pg.evaluate("[...document.querySelectorAll('.job')].every(j => j.open)")
    expect(btn).to_have_attribute("aria-pressed", "true")
    btn.click()
    assert pg.evaluate("[...document.querySelectorAll('.job')].every(j => !j.open)")


@case("Lien de preuve : ouvre la mission ciblée")
def t_proof(pg, url):
    pg.goto(url)
    pg.evaluate("document.getElementById('job-profil').open = false")
    pg.locator('.gains a[href="#job-profil"]').click()
    expect(pg.locator("#job-profil")).to_have_attribute("open", "")


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
    expect(pg.locator(".card-night .role")).to_have_text("Senior QA Engineer")
    pg.locator("a.lang").click()
    expect(pg.locator("html")).to_have_attribute("lang", "fr")


@case("Copie de l'adresse e-mail")
def t_copy(pg, url):
    pg.context.grant_permissions(["clipboard-read", "clipboard-write"])
    pg.goto(url + "#contact")
    pg.locator("[data-copy]").click()
    expect(pg.locator("[data-cstatus]")).not_to_be_empty()
    assert pg.evaluate("navigator.clipboard.readText()") == "thasin@live.com"
    href = pg.locator(".side-card .btn.primary").get_attribute("href")
    assert href.startswith("mailto:thasin@live.com?subject="), href


@case("Mobile : menu des sections et barre d'action fixe")
def t_mobile(pg, url):
    pg.set_viewport_size({"width": 375, "height": 760})
    pg.goto(url)
    expect(pg.locator(".mbar .btn.primary")).to_be_in_viewport()
    pg.locator(".menu summary").click()
    expect(pg.locator(".menu-in")).to_be_visible()
    pg.locator('.menu-in a[href="#parcours"]').click()
    expect(pg.locator(".menu")).not_to_have_attribute("open", "")
    box = pg.evaluate("(() => { const b = document.querySelector('.brand').getBoundingClientRect(), m = document.querySelector('.menu').getBoundingClientRect(); return [b.right, m.left]; })()")
    assert box[0] <= box[1] + 0.5, f"le nom chevauche le menu : {box}"


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
    small = pg.evaluate("""() => [...document.querySelectorAll('.nav a.lang, #theme, .menu summary, .btn, .icon-btn, .link-btn')]
        .filter(el => el.offsetParent).map(el => [el.className, Math.round(el.getBoundingClientRect().height)])
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
    expect(pg.locator(".skills")).to_be_visible()
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
            for fn in (t_fold, t_sticky, t_tabs, t_expand, t_proof, t_theme, t_lang, t_copy, t_mobile, t_widths, t_targets):
                ctx = browser.new_context(viewport={"width": 1440, "height": 900})
                pg = ctx.new_page()
                pg.on("pageerror", lambda ex: errors.append(str(ex)))
                pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                fn(pg, url)
                ctx.close()
            t_nojs(browser, url)
            browser.close()
    finally:
        srv.terminate()
    results.append((not errors, "Console sans erreur", "; ".join(sorted(set(errors)))[:300]))
    for ok, name, why in results:
        print(("  ✓ " if ok else "  ✗ ") + name + ("" if ok else f" — {why}"))
    ko = sum(1 for ok, *_ in results if not ok)
    print(f"{len(results) - ko}/{len(results)} cas passés")
    sys.exit(1 if ko else 0)
