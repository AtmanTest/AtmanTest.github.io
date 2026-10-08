#!/usr/bin/env python3
"""Génère index.html (FR) et en/index.html (EN) à partir de content.py.
Usage : python3 build/build.py
"""
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

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
        p = p.replace("« ", "«" + NB)
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
    mailto = f"mailto:{C.EMAIL}?subject={quote(L(C.CONTACT2['subject']))}"
    H = C.HERO2
    jobs_by_id = {j["id"]: j for j in C.JOBS}

    # ---------- hero ----------
    steps = C.CHAIN["steps"]
    run_items = "".join(
        f'<li class="{"found" if i == 5 else ""}"><span class="rn">{i + 1}</span><span class="rl">{e(L(s["name"]))}'
        + (f'<span class="rnote">{e(L(H["defect"]))}</span>' if i == 5 else "")
        + f'</span><span class="mark" aria-hidden="true"></span><span class="sr">{e(L(H["pass"]))}</span></li>'
        for i, s in enumerate(steps)
    )
    hero = f"""
<header class="hero" id="top" data-hero
  data-t-found="{e(L(H['fixed']))}">
  <canvas class="grid" aria-hidden="true"></canvas>
  <div class="wrap hero-in">
    <div class="hero-id">
      <p class="avail" data-solid><span class="dot" aria-hidden="true"></span><strong>{e(L(H['avail']))}</strong> — {e(L(H['avail2']))}</p>
      <h1 data-solid><span class="name">{e(C.HERO['name'])}</span><span class="role">{e(L(C.HERO['role']))}</span></h1>
      <p class="tagline" data-solid>{e(L(C.HERO['tagline']))}</p>
      <p class="sub" data-solid>{e(L(C.HERO['sub']))}</p>
      <p class="hero-cta" data-solid>
        <a class="btn primary" href="#contact">{e(L(H['cta1']))}</a>
        <a class="btn ghost" href="{cv_fr if lang == 'fr' else cv_en}" download>{e(L(H['cta2']))}</a>
      </p>
      <p class="where" data-solid>{e(L(C.HERO['where']))}</p>
    </div>
    <div class="runbox" data-solid>
      <p class="runlabel"><span>{e(L(H['sheet']))}</span><span class="rl2">{e(L(C.HERO['run_label']))}</span></p>
      <ol class="run" aria-label="{e(L(C.UI['steps_label']))}">{run_items}</ol>
      <p class="verdict" role="img" aria-label="{e(L(C.HERO['verdict_label']))} : {e(L(C.HERO['verdict']))}"><span class="vl" aria-hidden="true">{e(L(C.HERO['verdict_label']))}</span><span class="stamp" aria-hidden="true">{e(L(C.HERO['verdict']))}</span></p>
    </div>
    <div class="gamebar" aria-hidden="true" data-solid>
      <p class="hint">{e(L(H['hint']))}</p>
      <p class="g-stats"><span>{e(L(H['cov']))} <b data-gcov>0</b>&nbsp;%</span><span>{e(L(H['found']))} <b data-gfound>0</b></span></p>
    </div>
    <p class="g-msg" role="status" data-gmsg></p>
  </div>
</header>"""

    # ---------- preuves ----------
    stats = "".join(f'<div><dt data-count>{e(n)}</dt><dd>{e(L(t))}</dd></div>' for n, t in C.STATS)
    proof = f"""
<section class="proof" aria-label="{e(L(C.CLIENTS['label']))}"><div class="wrap">
  <dl class="stats">{stats}</dl>
  <div class="clients">
    <p class="cl-label">{e(L(C.CLIENTS['label']))}</p>
    <p class="cl-names">{e(C.CLIENTS['names'])}</p>
    <p class="cl-sectors">{e(L(C.CLIENTS['sectors']))}</p>
  </div>
</div></section>"""

    # ---------- profil + apports ----------
    p = C.PROFIL
    A = C.APPORTS
    apports_items = "".join(
        f'<li><h3>{e(L(it["t"]))}</h3><p>{e(L(it["d"]))}</p>'
        f'<p class="proof-l"><span>{e(L(A["proof"]))}</span><a href="{it["href"]}">{e(L(it["p"]))}</a></p></li>'
        for it in A["items"]
    )
    profil = f"""
<section class="sec" id="profil" aria-labelledby="h-profil"><div class="wrap">
  <h2 id="h-profil" class="h-big">{e(L(C.H2['profil']))}</h2>
  <div class="profil-grid">
    <div class="prose">
      <p class="lead">{e(L(p['lead']))}</p>
      {''.join(f'<p>{e(L(b))}</p>' for b in p['body'][:2])}
    </div>
    <div class="apports">
      <h3 class="h-mid">{e(L(A['title']))}</h3>
      <ul class="apports-list">{apports_items}</ul>
    </div>
  </div>
</div></section>"""

    # ---------- méthode ----------
    PR = C.PRINCIPLES
    principles = "".join(f'<li><h3>{e(L(t))}</h3><p>{e(L(d))}</p></li>' for t, d in PR["items"])
    ch = C.CHAIN
    nodes = "".join(
        f'<li role="presentation"><button type="button" class="step-btn" role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><span class="node"><b>{i + 1}</b></span><span class="nm">{e(L(s["name"]))}</span></button></li>'
        for i, s in enumerate(ch["steps"])
    )
    panels = "".join(
        f'<div class="step-panel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}" tabindex="0"{"" if i == 0 else " hidden"}>'
        f'<p class="step-n" aria-hidden="true">{i + 1}<span>/8</span></p>'
        f'<div class="step-txt"><h3>{e(L(s["name"]))}</h3>'
        f'<p class="lbl">{e(L(C.CHAIN_UI["does"]))}</p><p>{e(L(s["text"]))}</p>'
        f'<p class="lbl">{e(L(C.CHAIN_UI["delivers"]))}</p><p>{e(L(C.CHAIN_DELIVER[i]))}</p>'
        f'<p class="step-where"><span>{e(L(ch["where"]))}</span> {e(s["where"])}</p></div></div>'
        for i, s in enumerate(ch["steps"])
    )
    chaine = f"""
<section class="sec alt" id="chaine" aria-labelledby="h-chaine"><div class="wrap">
  <h2 id="h-chaine" class="h-big">{e(L(C.H2['chain']))}</h2>
  <p class="intro">{e(L(ch['intro']))}</p>
  <ul class="principles">{principles}</ul>
  <div class="chain" data-chain data-t-play="{e(L(C.CHAIN_UI['play']))}" data-t-pause="{e(L(C.CHAIN_UI['pause']))}">
    <div class="chain-bar">
      <button type="button" class="play" data-play aria-pressed="false">{e(L(C.CHAIN_UI['play']))}</button>
    </div>
    <ul class="stepper" role="tablist" aria-label="{e(L(C.UI['steps_label']))}">{nodes}</ul>
    <div class="step-panels">{panels}</div>
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
        f'<span class="bar" data-job="job-{j["id"]}" style="left:{pos(j["start"]):.2f}%;width:{max(pos(j["end"]) - pos(j["start"]), 0.9):.2f}%" '
        f'title="{e(j["client"])} · {e(L(j["dates"]).split(" · ")[0])}"><span>{e(j["short"])}</span></span>'
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
<section class="sec" id="parcours" aria-labelledby="h-parcours"><div class="wrap">
  <h2 id="h-parcours" class="h-big">{e(L(C.H2['parcours']))}</h2>
  <p class="intro">{e(L(P['intro']))}</p>
  <div class="timeline" aria-hidden="true">
    <div class="phases">{phases}</div>
    <div class="track">{bars}</div>
    <div class="ticks">{ticks}</div>
  </div>
  <div class="jobs">{jobs}
  </div>
  <p class="first">{e(L(P['first']))}</p>
</div></section>"""

    # ---------- matrice de compétences ----------
    M = C.MATRIX
    cols = [(cid, (lab if isinstance(lab, str) else L(lab))) for cid, lab in C.MATRIX_COLS]
    counts = {cid: sum(1 for _, tools in M["groups"] for _, used in tools if cid in used.split()) for cid, _ in cols}
    unit = ("outils", "tools")
    thead = "".join(
        f'<th scope="col"><button type="button" class="col-btn" data-col="{cid}" aria-pressed="false">{e(lab)}<small>{counts[cid]} {e(L(unit))}</small></button></th>' for cid, lab in cols
    )
    body = ""
    for gname, tools in M["groups"]:
        body += f'<tr class="grp"><th scope="rowgroup" colspan="{len(cols) + 1}">{e(L(gname))}</th></tr>'
        for tool, used in tools:
            ids = used.split()
            cells = "".join(
                f'<td class="{"on" if cid in ids else "off"}" data-col="{cid}">'
                + (f'<span class="sr">{e(L(M["used"]))} {e(lab)}</span>' if cid in ids else "") + "</td>"
                for cid, lab in cols
            )
            body += f'<tr data-tool="{e(tool)}" data-in="{used}"><th scope="row"><button type="button" class="row-btn" aria-pressed="false">{e(tool)}</button></th>{cells}</tr>'
    col_labels = json.dumps({cid: lab for cid, lab in cols}, ensure_ascii=False)
    col_stacks = {}
    for cid, _ in cols:
        col_stacks[cid] = [t for _, tools in M["groups"] for t, used in tools if cid in used.split()]
    full_groups = "".join(
        f'<div class="skill-group"><h3>{e(L(g["name"]))}</h3><ul class="tags">{"".join(f"<li>{e(x)}</li>" for x in (g["items"][0] if lang == "fr" else g["items"][1]))}</ul></div>'
        for g in C.SKILLS["groups"]
    )
    competences = f"""
<section class="sec alt" id="competences" aria-labelledby="h-competences"><div class="wrap">
  <h2 id="h-competences" class="h-big">{e(L(M['title']))}</h2>
  <p class="intro">{e(L(M['intro']))}</p>
  <div class="matrix" data-matrix data-labels='{e(col_labels)}' data-stacks='{e(json.dumps(col_stacks, ensure_ascii=False))}'
       data-t-used="{e(L(M['used']))}" data-t-stack="{e(L(M['stack']))}" data-t-none="{e(L(M['none']))}">
    <p class="m-status" role="status" data-mstatus>{e(L(M['none']))}</p>
    <div class="m-scroll"><table>
      <thead><tr><th scope="col"><button type="button" class="reset" data-reset>{e(L(M['reset']))}</button></th>{thead}</tr></thead>
      <tbody>{body}</tbody>
    </table></div>
  </div>
  <details class="all-skills"><summary>{e(L(M['all']))}</summary><div class="all-in">{full_groups}</div></details>
</div></section>"""

    # ---------- IA ----------
    AI = C.AI
    projs = ""
    for pr in AI["projects"]:
        name = pr["name"] if isinstance(pr["name"], str) else L(pr["name"])
        links = ""
        if pr["demo"]:
            links += f'<a href="{e(pr["demo"])}" target="_blank" rel="noopener">{e(L(AI["demo"]))}</a>'
        if pr["repo"]:
            links += f'<a href="{e(pr["repo"])}" target="_blank" rel="noopener">{e(L(AI["code"]))}</a>'
        projs += f"""
    <article class="proj"><h3>{e(name)}</h3><p>{e(L(pr['text']))}</p>
      <p class="stack"><b>{e(L(AI['stack']))}</b> {e(pr['stack'])}</p>{f'<p class="links">{links}</p>' if links else ''}</article>"""
    ia = f"""
<section class="sec" id="ia" aria-labelledby="h-ia"><div class="wrap">
  <h2 id="h-ia" class="h-big">{e(L(C.H2['ia']))}</h2>
  <p class="lead">{e(L(AI['lead']))}</p>
  <div class="projs">{projs}</div>
</div></section>"""

    # ---------- humain ----------
    S = C.SOFT
    work = "".join(f'<li><h4>{e(L(t))}</h4><p>{e(L(d))}</p></li>' for t, d in S["work"])
    life = "".join(
        f'<li><h4>{e(L(tr_))}</h4><p><strong>{e(L(t))}.</strong> {e(L(d))}</p></li>' for t, d, tr_ in C.INTERESTS["items"]
    )
    humain = f"""
<section class="sec alt" id="humain" aria-labelledby="h-humain"><div class="wrap">
  <h2 id="h-humain" class="h-big">{e(L(S['title']))}</h2>
  <p class="intro">{e(L(S['intro']))}</p>
  <div class="human-cols">
    <div><h3 class="h-mid">{e(L(S['work_title']))}</h3><ul class="traits">{work}</ul></div>
    <div><h3 class="h-mid">{e(L(S['life_title']))}</h3><ul class="traits life">{life}</ul></div>
  </div>
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
<section class="sec" id="formation" aria-labelledby="h-formation"><div class="wrap">
  <h2 id="h-formation" class="h-big">{e(L(C.H2['formation']))}</h2>
  <div class="edu-cols">
    <div><h3>{e(L(E['certs_title']))}</h3><ul class="plain">{certs}</ul></div>
    <div><h3>{e(L(E['edu_title']))}</h3><ul class="plain">{edu}</ul>
         <h3 class="h3-gap">{e(L(E['lang_title']))}</h3><ul class="plain">{langs}</ul></div>
  </div>
</div></section>"""

    # ---------- contact ----------
    K = C.CONTACT
    K2 = C.CONTACT2
    facts = "".join(f'<div><dt>{e(L(t))}</dt><dd>{e(L(d))}</dd></div>' for t, d in K2["facts"])
    contact = f"""
<section class="contact" id="contact" aria-labelledby="h-contact"><div class="wrap">
  <h2 id="h-contact" class="h-xl">{e(L(K2['headline']))}</h2>
  <p class="c-lead">{e(L(K['body']))}</p>
  <p class="cta"><a class="btn primary" href="{mailto}">{e(L(K['mail']))}</a>
    <button type="button" class="btn ghost" data-copy="{C.EMAIL}" data-t-ok="{e(L(K2['copied']))}">{e(L(K2['copy']))}</button>
    <a class="btn ghost" href="{cv_fr}" download>{e(L(K['cv_fr']))}</a>
    <a class="btn ghost" href="{cv_en}" download>{e(L(K['cv_en']))}</a></p>
  <p class="c-status" role="status" data-cstatus></p>
  <dl class="facts">{facts}</dl>
  <p class="elsewhere"><span>{e(L(K['other']))}</span>
    <a href="{C.LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
    <a href="{C.GITHUB}" target="_blank" rel="noopener">GitHub</a>
    <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
</div></section>"""

    nav_links = "".join(f'<a href="#{i}">{e(L(t))}</a>' for i, t in [
        ("profil", ("Apports", "Value")), ("chaine", ("Méthode", "Method")), ("parcours", ("Parcours", "Experience")),
        ("competences", ("Compétences", "Skills")), ("ia", ("IA", "AI")), ("humain", ("Profil humain", "Personal")), ("contact", ("Contact", "Contact"))])
    header = f"""
<nav class="nav" aria-label="Navigation">
  <div class="progress" aria-hidden="true"><i></i></div>
  <div class="wrap nav-in">
    <a class="brand" href="#top">Thasin Jahangir</a>
    <div class="nav-links">{nav_links}</div>
    <details class="menu"><summary>{e(L(H['menu']))}</summary><div class="menu-in">{nav_links}</div></details>
    <div class="nav-tools">
      <span class="cover" aria-hidden="true">{e(L(H['page_cov']))} <b data-pcov>0</b>&nbsp;%</span>
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
        "sameAs": [C.LINKEDIN, C.GITHUB],
        "knowsLanguage": ["fr", "en", "bn", "es"],
        "description": L(C.META["desc"]),
        "image": f"{C.SITE}/assets/{'og.png' if lang == 'fr' else 'og-en.png'}",
        "knowsAbout": [L(x) for x in (("Recette fonctionnelle", "Functional testing"), ("Recette utilisateur (UAT)", "User acceptance testing (UAT)"),
                       ("Tests de non-régression", "Regression testing"), ("Stratégie de test", "Test strategy"))]
                      + ["Jira", "Xray", "Zephyr", "TestRail", "SQL", "Playwright", "Appium", "Agile Scrum", "ISTQB"],
        "hasCredential": {"@type": "EducationalOccupationalCredential", "name": "PSPO I — Professional Scrum Product Owner",
                          "recognizedBy": {"@type": "Organization", "name": "Scrum.org"}},
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
<meta property="og:image" content="{C.SITE}/assets/{'og.png' if lang == 'fr' else 'og-en.png'}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(L(C.HERO['role']))} — Thasin Jahangir. {e(L(C.HERO['tagline']))}">
<meta property="og:site_name" content="Thasin Jahangir">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0c1722">
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
{proof}
{profil}
{chaine}
{parcours}
{competences}
{ia}
{humain}
{formation}
{contact}
</main>
<footer class="foot"><div class="wrap"><p>{e(L(K['legal']))}</p><p class="selftest"><span class="tick-s" aria-hidden="true"></span>{e(L(H['self_test']))} · <a href="https://github.com/AtmanTest/atmantest.github.io" target="_blank" rel="noopener">{e(L(H['self_link']))}</a></p><p>© 2026 Thasin Jahangir</p></div></footer>
<script src="{base}assets/site.js" defer></script>
</body>
</html>
"""
    return fr_typo(doc) if lang == "fr" else doc


if __name__ == "__main__":
    (ROOT / "index.html").write_text(render("fr"), encoding="utf-8")
    (ROOT / "en").mkdir(exist_ok=True)
    (ROOT / "en" / "index.html").write_text(render("en"), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {C.SITE}/sitemap.xml\n", encoding="utf-8")
    alt = (f'<xhtml:link rel="alternate" hreflang="fr" href="{C.SITE}/"/>'
           f'<xhtml:link rel="alternate" hreflang="en" href="{C.SITE}/en/"/>')
    urls = "".join(f"<url><loc>{u}</loc>{alt}</url>" for u in (C.SITE + "/", C.SITE + "/en/"))
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        + urls + "</urlset>\n", encoding="utf-8")
    print("ok")
