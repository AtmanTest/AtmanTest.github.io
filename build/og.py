#!/usr/bin/env python3
"""Génère les images Open Graph (1200×630) FR et EN, dans le style de l'en-tête du CV.
Usage : python3 build/og.py   (nécessite : pip install playwright && playwright install chromium)
"""
from html import escape
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent.parent
A = (ROOT / "assets").as_uri()


def page(lang):
    L = lambda pair: pair[0] if lang == "fr" else pair[1]
    stats = "".join(f"<div><b>{escape(L(a))}</b><span>{escape(L(b))} {escape(L(c))}</span></div>" for a, b, c in C.STATS2)
    return f"""<!doctype html><html lang="{lang}"><meta charset="utf-8"><style>
@font-face{{font-family:I;src:url("{A}/fonts/inter.woff2");font-weight:100 900}}
@font-face{{font-family:I;src:url("{A}/fonts/inter-italic.woff2");font-weight:100 900;font-style:italic}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1200px;height:630px;font-family:I;background:#f5f8f8;padding:28px;display:grid;grid-template-rows:1fr auto;gap:16px}}
.c{{border-radius:22px;background:radial-gradient(120% 140% at 100% 0%,#103b49 0%,#0a2230 62%);color:#eef6f6;padding:44px 52px;display:grid;grid-template-columns:1fr 250px;gap:40px;align-items:center}}
h1{{font-size:76px;font-weight:800;letter-spacing:-3px;line-height:1;color:#fff}}
.t{{margin-top:14px;font-size:30px;font-style:italic;font-weight:650;color:#f2b544}}
.r{{margin-top:26px;font-size:38px;font-weight:700;color:#5fd8c3;letter-spacing:-.5px}}
.s{{margin-top:10px;font-size:22px;color:#cfe0e3}}
.a{{display:inline-flex;align-items:center;gap:10px;margin-top:22px;background:#13a38b;color:#fff;font-weight:700;font-size:20px;padding:10px 20px;border-radius:999px}}
.a i{{width:10px;height:10px;border-radius:50%;background:#fff}}
img{{width:250px;height:250px;border-radius:26px;border:5px solid #5fd8c3;object-fit:cover}}
.st{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.st div{{background:#fff;border:1px solid #d5e3e2;border-radius:16px;padding:14px 18px}}
.st b{{display:block;font-size:30px;font-weight:800;color:#0a7766;letter-spacing:-1px}}
.st span{{font-size:14px;font-weight:650;color:#5a6b77;text-transform:uppercase;letter-spacing:.5px}}
</style><body>
<div class="c"><div>
<h1>{escape(C.HERO['name'])}</h1>
<p class="t">{escape(L(C.HERO['tagline']))}</p>
<p class="r">{escape(L(C.HERO['role']))}</p>
<p class="s">{escape(L(C.TOP['chips'][2]))} · Freelance SASU</p>
<p class="a"><i></i>{escape(L(C.HERO2['avail']))}</p>
</div><img src="{A}/thasin.jpg" alt=""></div>
<div class="st">{stats}</div>
</body></html>"""


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    tmp = ROOT / "build" / "_og.html"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for lang, out in (("fr", "og.png"), ("en", "og-en.png")):
            tmp.write_text(page(lang), encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.wait_for_timeout(400)
            pg.screenshot(path=str(ROOT / "assets" / out))
        b.close()
    tmp.unlink()
    print("ok")
