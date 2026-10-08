#!/usr/bin/env python3
"""Génère les images Open Graph (1200×630) FR et EN à partir de content.py.
Usage : python3 build/og.py   (nécessite : pip install playwright && playwright install chromium)
"""
from html import escape
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent.parent
FONTS = (ROOT / "assets" / "fonts").as_uri()


def page(lang):
    L = lambda pair: pair[0] if lang == "fr" else pair[1]
    steps = "".join(
        f'<li class="{"f" if i == 5 else ""}"><b>{i + 1}</b><span>{escape(L(s["name"]))}</span><i></i></li>'
        for i, s in enumerate(C.CHAIN["steps"])
    )
    stats = "".join(f"<div><strong>{n}</strong><span>{escape(L(t))}</span></div>" for n, t in C.STATS[:3])
    return f"""<!doctype html><html lang="{lang}"><meta charset="utf-8"><style>
@font-face{{font-family:D;src:url("{FONTS}/display.woff2");font-weight:200 800}}
@font-face{{font-family:T;src:url("{FONTS}/text-italic.woff2");font-style:italic;font-weight:200 900}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1200px;height:630px;background:#0c1722;color:#eaf1ee;font-family:D;overflow:hidden;position:relative;
  background-image:linear-gradient(#25394a 1px,transparent 1px),linear-gradient(90deg,#25394a 1px,transparent 1px);background-size:30px 30px}}
.v{{position:absolute;inset:0;background:radial-gradient(ellipse at 30% 45%,rgba(12,23,34,.92) 30%,rgba(12,23,34,.55) 75%)}}
.in{{position:absolute;inset:0;padding:64px 64px 56px;display:grid;grid-template-columns:1fr 360px;gap:48px}}
.av{{font-size:22px;display:flex;align-items:center;gap:12px}}.av i{{width:13px;height:13px;border-radius:50%;background:#46d19a}}
.nm{{margin-top:34px;font-size:30px;color:#9fb2ba;font-weight:500}}
h1{{font-size:96px;line-height:.92;letter-spacing:-3px;font-weight:750;margin-top:10px}}
.tg{{font-family:T;font-style:italic;font-size:33px;margin-top:28px;line-height:1.2;max-width:15em}}
.st{{display:flex;gap:34px;margin-top:34px}}.st div{{display:grid;gap:4px;max-width:190px}}
.st strong{{font-size:40px;line-height:1}}.st span{{font-size:16px;color:#9fb2ba;line-height:1.3}}
.sh{{align-self:start;background:#122231;border:1px solid #25394a;border-top:4px solid #eaf1ee;border-radius:4px;padding:20px 22px 22px}}
.sh p{{font-weight:700;font-size:20px;padding-bottom:10px;border-bottom:1px solid #25394a}}
.sh li{{list-style:none;display:grid;grid-template-columns:24px 1fr 22px;gap:10px;align-items:center;padding:7px 0;border-bottom:1px dashed #25394a;font-size:17px}}
.sh b{{color:#9fb2ba}}.sh i{{width:22px;height:22px;border-radius:4px;background:#46d19a;position:relative}}
.sh i::after{{content:"";position:absolute;left:6px;top:6px;width:9px;height:5px;border-left:3px solid #0c1722;border-bottom:3px solid #0c1722;transform:rotate(-45deg)}}
.sh li.f{{background:linear-gradient(90deg,rgba(255,122,104,.25),transparent);margin:0 -8px;padding-left:8px;padding-right:8px}}
.sh li.f i{{background:#ff7a68}}
.go{{display:flex;justify-content:flex-end;margin-top:18px}}
.go span{{font-weight:800;font-size:46px;letter-spacing:3px;color:#46d19a;border:5px solid #46d19a;border-radius:7px;padding:0 18px;transform:rotate(-6deg)}}
</style><body><div class="v"></div><div class="in"><div>
<p class="av"><i></i>{escape(L(C.HERO2['avail']))} · Paris</p>
<p class="nm">{escape(C.HERO['name'])}</p>
<h1>{escape(L(C.HERO['role']))}</h1>
<p class="tg">{escape(L(C.HERO['tagline']))}</p>
<div class="st">{stats}</div></div>
<div class="sh"><p>{escape(L(C.HERO2['sheet']))}</p><ol>{steps}</ol><div class="go"><span>GO</span></div></div>
</div></body></html>"""


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    tmp = ROOT / "build" / "_og.html"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for lang, out in (("fr", "og.png"), ("en", "og-en.png")):
            tmp.write_text(page(lang), encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(ROOT / "assets" / out))
        b.close()
    tmp.unlink()
    print("ok")
