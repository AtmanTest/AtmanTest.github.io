#!/usr/bin/env python3
"""Génère index.html (FR) et en/index.html (EN) à partir de content.py.
Usage : python3 build/build.py
"""
import json
import re
from html import escape
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent.parent
NB = " "


def tr(pair, lang):
    return pair[0] if lang == "fr" else pair[1]


def e(s):
    return escape(s, quote=True)


def fr_typo(html):
    """Espaces insécables françaises, hors <style>/<script>."""
    parts = re.split(r"(<style.*?</style>|<script.*?</script>)", html, flags=re.S)
    out = []
    for p in parts:
        if p.startswith("<style") or p.startswith("<script"):
            out.append(p)
            continue
        p = re.sub(r" ([:;?!»])", NB + r"\1", p)
        p = p.replace("« ", "«" + NB).replace("“ ", "“")
        out.append(p)
    return "".join(out)


def icon_theme():
    return ('<svg class="i-sun" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/>'
            '<path d="M12 2.5v2.6M12 18.9v2.6M2.5 12h2.6M18.9 12h2.6M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
            '<svg class="i-moon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>')


def render(lang):
    L = lambda pair: tr(pair, lang)
    base = "" if lang == "fr" else "../"
    url_self = C.SITE + ("/" if lang == "fr" else "/en/")
    url_fr, url_en = C.SITE + "/", C.SITE + "/en/"
    other_href = "en/" if lang == "fr" else "../"
    cv_fr, cv_en = base + "cv/CV_Thasin_Jahangir_QA_2026_FR.pdf", base + "cv/CV_Thasin_Jahangir_QA_2026_EN.pdf"

    # ---------- hero run ----------
    steps = C.CHAIN["steps"]
    run_items = "".join(
        f'<li class="{"found" if i == 5 else ""}"><span class="mark" aria-hidden="true"></span><span class="rl"><b>{i + 1}</b> {e(L(s["name"]))}</span></li>'
        for i, s in enumerate(steps)
    )
    hero = f"""
<header class="hero" id="top">
  <div class="wrap">
    <h1><span class="name">{e(C.HERO['name'])}</span><span class="role">{e(L(C.HERO['role']))}</span></h1>
    <p class="tagline">{e(L(C.HERO['tagline']))}</p>
    <p class="sub">{e(L(C.HERO['sub']))}</p>
    <p class="status"><span class="dot" aria-hidden="true"></span><strong>{e(L(C.HERO['status']))}</strong> — {e(L(C.HERO['status2']))}<br><span class="where">{e(L(C.HERO['where']))}</span></p>

    <div class="runbox">
      <p class="runlabel">{e(L(C.HERO['run_label']))}</p>
      <ol class="run" aria-label="{e(L(C.UI['steps_label']))}">{run_items}</ol>
      <p class="verdict" role="img" aria-label="{e(L(C.HERO['verdict_label']))} : {e(L(C.HERO['verdict']))}"><span class="vl">{e(L(C.HERO['verdict_label']))}</span><span class="stamp" aria-hidden="true">{e(L(C.HERO['verdict']))}</span></p>
    </div>

    <dl class="stats">
      {''.join(f'<div><dt>{e(n)}</dt><dd>{e(L(t))}</dd></div>' for n, t in C.STATS)}
    </dl>
    <div class="clients">
      <p class="cl-label">{e(L(C.CLIENTS['label']))}</p>
      <p class="cl-names">{e(C.CLIENTS['names'])}</p>
      <p class="cl-sectors">{e(L(C.CLIENTS['sectors']))}</p>
    </div>
  </div>
</header>"""

    # ---------- profil ----------
    p = C.PROFIL
    profil = f"""
<section class="sec" id="profil" aria-labelledby="h-profil"><div class="wrap sec-grid">
  <h2 id="h-profil">{e(L(p['title']))}</h2>
  <div class="sec-body prose">
    <p class="lead">{e(L(p['lead']))}</p>
    {''.join(f'<p>{e(L(b))}</p>' for b in p['body'])}
  </div>
</div></section>"""

    # ---------- chaîne ----------
    ch = C.CHAIN
    btns = "".join(
        f'<li><button type="button" class="step-btn" role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><b>{i + 1}</b><span>{e(L(s["name"]))}</span></button></li>'
        for i, s in enumerate(ch["steps"])
    )
    panels = "".join(
        f'<div class="step-panel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}" tabindex="0"{"" if i == 0 else " hidden"}>'
        f'<p class="step-n" aria-hidden="true">{i + 1}<span>/8</span></p><h3>{e(L(s["name"]))}</h3><p>{e(L(s["text"]))}</p>'
        f'<p class="step-where"><span>{e(L(ch["where"]))}</span> {e(s["where"])}</p></div>'
        for i, s in enumerate(ch["steps"])
    )
    chaine = f"""
<section class="sec" id="chaine" aria-labelledby="h-chaine"><div class="wrap sec-grid">
  <h2 id="h-chaine">{e(L(ch['title']))}</h2>
  <div class="sec-body">
    <p class="intro">{e(L(ch['intro']))}</p>
    <div class="chain">
      <ul class="step-list" role="tablist" aria-label="{e(L(C.UI['steps_label']))}" aria-orientation="vertical">{btns}</ul>
      <div class="step-panels">{panels}</div>
    </div>
  </div>
</div></section>"""

    # ---------- parcours ----------
    P = C.PARCOURS
    t0, t1 = 2006.0, 2026.5
    pos = lambda y: (y - t0) / (t1 - t0) * 100
    phases = "".join(
        f'<span class="phase" style="left:{pos(a):.2f}%;width:{pos(b) - pos(a):.2f}%"><span>{e(L(n))}</span></span>' for a, b, n in P["phases"]
    )
    bars = "".join(
        f'<a class="bar" href="#job-{j["id"]}" style="left:{pos(j["start"]):.2f}%;width:{max(pos(j["end"]) - pos(j["start"]), 0.9):.2f}%" '
        f'aria-label="{e(j["client"])}, {e(L(j["dates"]))}" title="{e(j["client"])} · {e(L(j["dates"]).split(" · ")[0])}"><span>{e(j["short"])}</span></a>'
        for j in sorted(C.JOBS, key=lambda j: j["start"])
    )
    ticks = "".join(f'<span class="tick" style="left:{pos(y):.2f}%">{y}</span>' for y in (2006, 2011, 2016, 2021, 2026))
    jobs = ""
    for n, j in enumerate(C.JOBS):
        intro = f'<p class="job-intro">{e(L(j["intro"]))}</p>' if j["intro"] else ""
        lis = "".join(f"<li>{e(L(b))}</li>" for b in j["bullets"])
        ul = f"<ul>{lis}</ul>" if lis else ""
        jobs += f"""
  <details class="job" id="job-{j['id']}"{" open" if n == 0 else ""}>
    <summary>
      <span class="j-head"><span class="j-client">{e(j['client'])}</span><span class="j-dates">{e(L(j['dates']))} · {e(L(j['dur']))}</span></span>
      <span class="j-role">{e(L(j['role']))}</span>
      <span class="j-title">{e(L(j['title']))}</span>
    </summary>
    <div class="j-body">{intro}{ul}<p class="env"><b>{e(L(P['env']))}</b> {e(j['env'])}</p></div>
  </details>"""
    parcours = f"""
<section class="sec" id="parcours" aria-labelledby="h-parcours"><div class="wrap sec-grid">
  <h2 id="h-parcours">{e(L(P['title']))}</h2>
  <div class="sec-body">
    <p class="intro">{e(L(P['intro']))}</p>
    <div class="timeline" role="group" aria-label="{e(L(P['timeline_label']))}">
      <div class="phases">{phases}</div>
      <div class="track">{bars}</div>
      <div class="ticks">{ticks}</div>
    </div>
    <div class="jobs">{jobs}
    </div>
    <p class="first">{e(L(P['first']))}</p>
  </div>
</div></section>"""

    # ---------- compétences ----------
    S = C.SKILLS
    groups = "".join(
        f'<div class="skill-group"><h3>{e(L(g["name"]))}</h3><ul class="tags">{"".join(f"<li>{e(x)}</li>" for x in (g["items"][0] if lang == "fr" else g["items"][1]))}</ul></div>'
        for g in S["groups"]
    )
    competences = f"""
<section class="sec" id="competences" aria-labelledby="h-competences"><div class="wrap sec-grid">
  <h2 id="h-competences">{e(L(S['title']))}</h2>
  <div class="sec-body">{groups}</div>
</div></section>"""

    # ---------- IA ----------
    A = C.AI
    projs = ""
    for pr in A["projects"]:
        name = pr["name"] if isinstance(pr["name"], str) else L(pr["name"])
        links = ""
        if pr["demo"]:
            links += f'<a href="{e(pr["demo"])}" target="_blank" rel="noopener">{e(L(A["demo"]))}</a>'
        if pr["repo"]:
            links += f'<a href="{e(pr["repo"])}" target="_blank" rel="noopener">{e(L(A["code"]))}</a>'
        projs += f"""
    <article class="proj"><h3>{e(name)}</h3><p>{e(L(pr['text']))}</p>
      <p class="stack"><b>{e(L(A['stack']))}</b> {e(pr['stack'])}</p>{f'<p class="links">{links}</p>' if links else ''}</article>"""
    ia = f"""
<section class="sec" id="ia" aria-labelledby="h-ia"><div class="wrap sec-grid">
  <h2 id="h-ia">{e(L(A['title']))}</h2>
  <div class="sec-body"><p class="lead">{e(L(A['lead']))}</p><div class="projs">{projs}</div></div>
</div></section>"""

    # ---------- formation ----------
    E = C.EDU
    certs = "".join(
        f'<li><span class="c-name">{e(L(n))}</span> <span class="c-meta">{e(m)}</span>'
        + (f' <a href="{e(u)}" target="_blank" rel="noopener" aria-label="{e(L(E["cert_link"]))} : {e(L(n))}">{e(L(E["cert_link"]))}</a>' if u else "")
        + "</li>"
        for n, m, u in E["certs"]
    )
    edu = "".join(f'<li><span class="c-name">{e(L(n))}</span> <span class="c-meta">{e(L(m))}</span></li>' for n, m in E["edu"])
    langs = "".join(f'<li><span class="c-name">{e(L(n))}</span> <span class="c-meta">{e(L(m))}</span></li>' for n, m in E["langs"])
    formation = f"""
<section class="sec" id="formation" aria-labelledby="h-formation"><div class="wrap sec-grid">
  <h2 id="h-formation">{e(L(E['title']))}</h2>
  <div class="sec-body edu-cols">
    <div><h3>{e(L(E['certs_title']))}</h3><ul class="plain">{certs}</ul></div>
    <div><h3>{e(L(E['edu_title']))}</h3><ul class="plain">{edu}</ul>
         <h3 class="h3-gap">{e(L(E['lang_title']))}</h3><ul class="plain">{langs}</ul></div>
  </div>
</div></section>"""

    # ---------- intérêts ----------
    I = C.INTERESTS
    items = "".join(f'<li><h3>{e(L(t))}</h3><p>{e(L(d))}</p><p class="trait">{e(L(tr_))}</p></li>' for t, d, tr_ in I["items"])
    interets = f"""
<section class="sec" id="interets" aria-labelledby="h-interets"><div class="wrap sec-grid">
  <h2 id="h-interets">{e(L(I['title']))}</h2>
  <div class="sec-body"><p class="intro">{e(L(I['intro']))}</p><ul class="interests">{items}</ul></div>
</div></section>"""

    # ---------- contact ----------
    K = C.CONTACT
    contact = f"""
<section class="sec contact" id="contact" aria-labelledby="h-contact"><div class="wrap sec-grid">
  <h2 id="h-contact">{e(L(K['title']))}</h2>
  <div class="sec-body">
    <p class="big">{e(L(K['lead']))}</p>
    <p>{e(L(K['body']))}</p>
    <p class="cta"><a class="btn primary" href="mailto:{C.EMAIL}">{e(L(K['mail']))}</a>
      <a class="btn" href="{cv_fr}" download>{e(L(K['cv_fr']))}</a>
      <a class="btn" href="{cv_en}" download>{e(L(K['cv_en']))}</a></p>
    <p class="elsewhere"><span>{e(L(K['other']))}</span>
      <a href="{C.LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      <a href="{C.MALT}" target="_blank" rel="noopener">Malt</a>
      <a href="{C.GITHUB}" target="_blank" rel="noopener">GitHub</a>
      <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
  </div>
</div></section>"""

    nav_links = "".join(f'<a href="#{i}">{e(L(t))}</a>' for i, t in C.NAV)
    header = f"""
<nav class="nav" aria-label="Navigation">
  <div class="wrap nav-in">
    <a class="brand" href="#top">Thasin Jahangir</a>
    <div class="nav-links">{nav_links}</div>
    <div class="nav-tools">
      <a class="lang" href="{other_href}" hreflang="{'en' if lang == 'fr' else 'fr'}" lang="{'en' if lang == 'fr' else 'fr'}" title="{e(L(C.UI['lang_switch']))}">{e(L(C.UI['lang_switch_short']))}</a>
      <button type="button" class="theme" id="theme" aria-label="{e(L(C.UI['theme']))}">{icon_theme()}</button>
    </div>
  </div>
</nav>"""

    ld = {
        "@context": "https://schema.org", "@type": "Person", "name": "Thasin Jahangir",
        "jobTitle": L(C.HERO["role"]), "url": url_self, "email": C.EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Paris", "addressCountry": "FR"},
        "worksFor": {"@type": "Organization", "name": "SASU ATMAN"},
        "sameAs": [C.LINKEDIN, C.MALT, C.GITHUB],
        "knowsLanguage": ["fr", "en", "bn", "es"],
    }

    doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(L(C.META['title']))}</title>
<meta name="description" content="{e(L(C.META['desc']))}">
<meta name="author" content="Thasin Jahangir">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{url_self}">
<link rel="alternate" hreflang="fr" href="{url_fr}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="x-default" href="{url_fr}">
<meta property="og:type" content="profile">
<meta property="og:title" content="{e(L(C.META['title']))}">
<meta property="og:description" content="{e(L(C.META['desc']))}">
<meta property="og:url" content="{url_self}">
<meta property="og:locale" content="{'fr_FR' if lang == 'fr' else 'en_GB'}">
<meta property="og:image" content="{C.SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{base}assets/fonts/display.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fonts/text.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/site.css">
<script>
(function(){{try{{var t=localStorage.getItem('theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}document.documentElement.classList.add('js');}})();
</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#profil">{e(L(C.UI['skip']))}</a>
{header}
<main>
{hero}
{profil}
{chaine}
{parcours}
{competences}
{ia}
{formation}
{interets}
{contact}
</main>
<footer class="foot"><div class="wrap"><p>{e(L(K['legal']))}</p><p>© 2026 Thasin Jahangir</p></div></footer>
<script src="{base}assets/site.js" defer></script>
</body>
</html>
"""
    return fr_typo(doc) if lang == "fr" else doc


if __name__ == "__main__":
    (ROOT / "index.html").write_text(render("fr"), encoding="utf-8")
    (ROOT / "en").mkdir(exist_ok=True)
    (ROOT / "en" / "index.html").write_text(render("en"), encoding="utf-8")
    print("ok")
