#!/usr/bin/env python3
"""Génère index.html (FR) et en/index.html (EN) à partir de content.py.
Le site reprend la structure et le langage visuel du CV : en-tête nuit avec photo, chiffres en cartes,
bandeau clients, profil aux mots-clés en gras, chaîne QA, frise et missions, compétences, formation, intérêts.
Usage : python3 build/build.py
"""
import hashlib
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


def rich(s):
    """Texte échappé, **gras** → <strong>."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e(s))


def lead_bold(s):
    """Puce de mission : le segment avant les deux-points est mis en gras, comme sur le CV."""
    m = re.match(r"^(.{3,90}?)( ?: )(.*)$", s)
    if not m:
        return e(s)
    return f"<strong>{e(m.group(1))}</strong>{e(m.group(2))}{e(m.group(3))}"


def ver(path):
    """Empreinte courte : l'URL change à chaque modification, le cache ne sert jamais une version périmée."""
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:10]


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


ICONS = {
    "sun": '<svg class="i-sun" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2.5v2.6M12 18.9v2.6M2.5 12h2.6M18.9 12h2.6M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "moon": '<svg class="i-moon" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
    "dl": '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 20h16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "copy": '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
    "in": '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.1c0-1.22-.02-2.79-1.7-2.79-1.7 0-1.96 1.33-1.96 2.7V21h-4z"/></svg>',
    "gh": '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.11-1.47-1.11-1.47-.9-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.89 1.53 2.34 1.09 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85v2.74c0 .27.18.58.69.48A10 10 0 0 0 12 2Z"/></svg>',
    "chip": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><rect x="7" y="7" width="10" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
    "watch": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><rect x="6.5" y="6.5" width="11" height="11" rx="3" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M9 6.5 9.5 3h5l.5 3.5M9 17.5l.5 3.5h5l.5-3.5M12 10v2.2l1.4 1" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
    "code": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "camera": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M4 8h3l1.5-2h7L17 8h3v11H4z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="12" cy="13" r="3.3" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>',
    "palette": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18c1.2 0 1.8-.8 1.8-1.7 0-1.1-.9-1.5-.9-2.5 0-.9.7-1.6 1.7-1.6H17a4 4 0 0 0 4-4C21 6.6 17 3 12 3Z" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="7.5" cy="11.5" r="1.2" fill="currentColor"/><circle cx="10" cy="7.5" r="1.2" fill="currentColor"/><circle cx="14.5" cy="7.5" r="1.2" fill="currentColor"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M3 12h18M12 3c2.5 2.6 3.7 5.6 3.7 9S14.5 18.4 12 21c-2.5-2.6-3.7-5.6-3.7-9S9.5 5.6 12 3Z" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>',
    "yin": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 3a4.5 4.5 0 0 1 0 9 4.5 4.5 0 0 0 0 9" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="7.5" r="1.1" fill="currentColor"/><circle cx="12" cy="16.5" r="1.1" fill="currentColor"/></svg>',
}
INTEREST_ICONS = ["chip", "watch", "code", "camera", "palette", "globe", "yin"]


def sec_head(sid, label):
    return f'<h2 class="sh" id="h-{sid}"><span class="dia" aria-hidden="true"></span>{e(label)}</h2>'


def render(lang):
    L = lambda pair: tr(pair, lang)
    base = "" if lang == "fr" else "../"
    url_self = C.SITE + ("/" if lang == "fr" else "/en/")
    url_fr, url_en = C.SITE + "/", C.SITE + "/en/"
    other_href = "en/" if lang == "fr" else "../"
    cv_fr, cv_en = base + "cv/CV_Thasin_Jahangir_QA_2026_FR.pdf", base + "cv/CV_Thasin_Jahangir_QA_2026_EN.pdf"
    cv_mine = cv_fr if lang == "fr" else cv_en
    mailto = f"mailto:{C.EMAIL}?subject={quote(L(C.CONTACT2['subject']))}"
    T = C.TOP
    colon = " :" if lang == "fr" else ":"

    # ---------- en-tête (carte nuit, comme le CV) ----------
    chips = "".join(f'<li class="chip">{e(L(c))}</li>' for c in T["chips"])
    top = f"""
<header class="top" id="top"><div class="wrap">
  <div class="card-night">
    <div class="id">
      <h1 class="name">{e(C.HERO['name'])}</h1>
      <p class="tagline">{e(L(C.HERO['tagline']))}</p>
      <p class="ids">{e(L(T['ids']))}</p>
      <p class="role">{e(L(C.HERO['role']))}</p>
      <p class="sub">{e(L(C.HERO['sub']))}</p>
      <p class="reach">Paris / Île-de-France &amp; Remote <span aria-hidden="true">·</span> <a href="{mailto}">{C.EMAIL}</a> <span aria-hidden="true">·</span> <a href="{C.LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></p>
      <ul class="chips"><li class="chip on"><span class="dot" aria-hidden="true"></span>{e(L(T['badge']))}</li>{chips}</ul>
      <p class="cta">
        <a class="btn primary" href="{mailto}">{ICONS['mail']}{e(L(T['cta_mail']))}</a>
        <a class="btn ghost" href="{cv_mine}" download>{ICONS['dl']}{e(L(T['cta_cv']))}</a>
      </p>
    </div>
    <picture class="photo">
      <source srcset="{base}assets/thasin.webp" type="image/webp">
      <img src="{base}assets/thasin.jpg" width="300" height="300" alt="{e(L(T['photo_alt']))}" fetchpriority="high">
    </picture>
  </div>
  <dl class="stats">{"".join(f'<div class="stat"><dt>{e(L(a))}</dt><dd><b>{e(L(b))}</b> {e(L(c))}</dd></div>' for a, b, c in C.STATS2)}</dl>
  <div class="clients">
    <p class="cl-label">{e(L(C.CLIENTS['label']))}</p>
    <p class="cl-names">{e(C.CLIENTS['names'])}</p>
    <p class="cl-sectors">{e(L(C.CLIENTS['sectors']))}</p>
  </div>
</div></header>"""

    # ---------- profil + ce que vous obtenez ----------
    A = C.APPORTS
    gains = "".join(
        f'<li><h3>{e(L(it["t"]))}</h3><p>{e(L(it["d"]))}</p><p class="proof"><a href="{it["href"]}">{e(L(it["p"]))}</a></p></li>'
        for it in A["items"]
    )
    profil = f"""
<section class="sec" id="profil" aria-labelledby="h-profil">
  {sec_head('profil', L(C.SEC['profil']))}
  <p class="lead">{e(L(C.PROFILE_LEAD))}</p>
  <p class="body">{rich(L(C.PROFILE_BODY))}</p>
  <h3 class="mini">{e(L(C.SEC['gain']))}</h3>
  <ul class="gains">{gains}</ul>
</section>"""

    # ---------- chaîne QA ----------
    ch = C.CHAIN
    tiles = "".join(
        f'<li role="presentation"><button type="button" class="tile" role="tab" id="tab-{i}" aria-controls="panel-{i}" '
        f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><b>{i + 1}</b><span>{e(L(s["name"]))}</span></button></li>'
        for i, s in enumerate(ch["steps"])
    )
    panels = "".join(
        f'<div class="panel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}" tabindex="0"{"" if i == 0 else " hidden"}>'
        f'<h3><b>{i + 1}</b> {e(L(s["name"]))}</h3>'
        f'<dl><div><dt>{e(L(C.CHAIN_UI["does"]))}</dt><dd>{e(L(s["text"]))}</dd></div>'
        f'<div><dt>{e(L(C.CHAIN_UI["delivers"]))}</dt><dd>{e(L(C.CHAIN_DELIVER[i]))}</dd></div>'
        f'<div><dt>{e(L(ch["where"]))}</dt><dd>{e(s["where"])}</dd></div></dl></div>'
        for i, s in enumerate(ch["steps"])
    )
    chaine = f"""
<section class="sec" id="chaine" aria-labelledby="h-chaine">
  {sec_head('chaine', L(C.SEC['chaine']))}
  <p class="hint">{e(L(C.CHAIN_HINT))}</p>
  <div class="chain" data-chain>
    <ul class="tiles" role="tablist" aria-label="{e(L(C.UI['steps_label']))}">{tiles}</ul>
    <div class="panels">{panels}</div>
  </div>
</section>"""

    # ---------- expérience ----------
    P = C.PARCOURS
    t0, t1 = 2006.0, 2026.5
    pos = lambda y: (y - t0) / (t1 - t0) * 100
    phases = "".join(
        f'<span class="ph ph{k}" style="left:{pos(a):.2f}%;width:{pos(b) - pos(a):.2f}%">{e(L(n))}</span>' for k, (a, b, n) in enumerate(P["phases"])
    )
    bars = '<span class="bar first" style="left:0;width:{:.2f}%"></span>'.format(pos(2007.0) - 0.4)
    bars += "".join(
        f'<a class="bar" href="#job-{j["id"]}" tabindex="-1" style="left:{pos(j["start"]):.2f}%;width:{max(pos(j["end"]) - pos(j["start"]), 0.9):.2f}%" '
        f'title="{e(j["client"])} · {e(L(j["dates"]).split(" · ")[0])}"><span>{e("Profil Technology · Bitdefender · Witigo" if j["id"] == "profil" else j["short"])}</span></a>'
        for j in sorted(C.JOBS, key=lambda j: j["start"])
    )
    ticks = "".join(f'<span class="tick" style="left:{pos(y):.2f}%">{y}</span>' for y in (2006, 2011, 2016, 2021, 2026))
    jobs = ""
    for n, j in enumerate(C.JOBS):
        intro = f'<p class="j-intro">{e(L(j["intro"]))}</p>' if j["intro"] else ""
        lis = "".join(f"<li>{lead_bold(L(b))}</li>" for b in j["bullets"])
        ul = f"<ul>{lis}</ul>" if lis else ""
        dur = f'<span class="dur">{e(L(j["dur"]))}</span>'
        jobs += f"""
  <details class="job" id="job-{j['id']}"{" open" if n < 2 else ""}>
    <summary>
      <span class="j-top"><span class="j-client">{e(j['client'])}</span> <span class="j-title">— {e(L(j['title']))}</span></span>
      <span class="j-meta">{e(L(j['dates']))}{dur}</span>
      <span class="j-role">{e(L(j['role']))}</span>
    </summary>
    <div class="j-body">{intro}{ul}<p class="env"><b>{e(L(P['env']))}</b> {e(j['env'])}</p></div>
  </details>"""
    first_head, first_rest = L(P["first"]).split(colon + " ", 1) if lang == "fr" else L(P["first"]).split(": ", 1)
    parcours = f"""
<section class="sec" id="parcours" aria-labelledby="h-parcours">
  {sec_head('parcours', L(C.SEC['parcours']))}
  <div class="timeline" aria-hidden="true">
    <div class="phases">{phases}</div>
    <div class="track">{bars}</div>
    <div class="ticks">{ticks}</div>
  </div>
  <p class="jobs-tools"><button type="button" class="link-btn" data-expand data-t-open="{e(L(C.EXPAND[0]))}" data-t-close="{e(L(C.EXPAND[1]))}" aria-pressed="false">{e(L(C.EXPAND[0]))}</button></p>
  <div class="jobs">{jobs}
  </div>
  <p class="first"><strong>{e(first_head)}{colon}</strong> {e(first_rest)}</p>
</section>"""

    # ---------- compétences ----------
    def skill_items(items):
        return ' <span class="sep" aria-hidden="true">·</span> '.join(
            f"<strong>{e(x)}</strong>" if x in C.SKILL_STRONG else e(x) for x in items)
    groups = "".join(
        f'<div class="sk"><h3 class="mini">{e(L(g["name"]))}</h3><p>{skill_items(g["items"][0] if lang == "fr" else g["items"][1])}</p></div>'
        for g in C.SKILLS["groups"]
    )
    competences = f"""
<section class="sec" id="competences" aria-labelledby="h-competences">
  {sec_head('competences', L(C.SEC['competences']))}
  <div class="skills">{groups}</div>
</section>"""

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
        links_html = f'<p class="links">{links}</p>' if links else ""
        projs += (f'<article class="proj"><h3>{e(name)}</h3><p>{e(L(pr["text"]))}</p>'
                  f'<p class="stack">{e(pr["stack"])}</p>{links_html}</article>')
    ia = f"""
<section class="sec" id="ia" aria-labelledby="h-ia">
  {sec_head('ia', L(C.SEC['ia']))}
  <p class="body">{e(L(AI['lead']))}</p>
  <div class="projs">{projs}</div>
</section>"""

    # ---------- formation ----------
    E = C.EDU
    certs = "".join(
        f'<li><strong>{e(L(n))}</strong> <span class="m">· {e(m)}</span>'
        + (f' · <a href="{e(u)}" target="_blank" rel="noopener" aria-label="{e(L(E["cert_link"]))} : {e(L(n))}">{e(L(E["cert_link"]))}</a>' if u else "")
        + "</li>"
        for n, m, u in E["certs"]
    )
    edu = "".join(f'<li><strong>{e(L(n))}</strong> <span class="m">· {e(L(m))}</span></li>' for n, m in E["edu"])
    langs = "".join(
        f'<li><span class="ln">{e(L(n))}</span><span class="lv">{e(L(m))}</span><span class="lb" aria-hidden="true"><i style="width:{lvl}%"></i></span></li>'
        for (n, m), lvl in zip(E["langs"], C.LANG_LEVEL)
    )
    formation = f"""
<section class="sec" id="formation" aria-labelledby="h-formation">
  {sec_head('formation', L(C.SEC['formation']))}
  <div class="edu">
    <div><h3 class="mini">{e(L(E['certs_title']))}</h3><ul class="plain">{certs}</ul></div>
    <div><h3 class="mini">{e(L(E['edu_title']))}</h3><ul class="plain">{edu}</ul>
      <h3 class="mini gap">{e(L(E['lang_title']))}</h3><ul class="langs">{langs}</ul></div>
  </div>
</section>"""

    # ---------- centres d'intérêt ----------
    cards = "".join(
        f'<li class="int"><span class="ic">{ICONS[INTEREST_ICONS[k]]}</span><h3>{e(L(t))}</h3><p>{e(L(d))}</p><p class="trait">→ {e(L(tr_))}</p></li>'
        for k, (t, d, tr_) in enumerate(C.INTERESTS["items"])
    )
    interets = f"""
<section class="sec" id="interets" aria-labelledby="h-interets">
  {sec_head('interets', L(C.SEC['interets']))}
  <ul class="ints">{cards}</ul>
</section>"""

    # ---------- colonne contact (collante) ----------
    S = C.SIDE
    facts = "".join(f'<div><dt>{e(L(a))}</dt><dd>{e(L(b))}</dd></div>' for a, b in S["facts"])
    aside = f"""
<aside class="side" id="contact" aria-labelledby="h-contact">
  <div class="side-card">
    <p class="avail"><span class="dot" aria-hidden="true"></span>{e(L(C.HERO2['avail']))}</p>
    <h2 id="h-contact">{e(L(S['title']))}</h2>
    <dl class="facts">{facts}</dl>
    <a class="btn primary wide" href="{mailto}">{ICONS['mail']}{e(L(C.CONTACT['mail']))}</a>
    <p class="mailrow"><a href="{mailto}">{C.EMAIL}</a><button type="button" class="icon-btn" data-copy="{C.EMAIL}" data-t-ok="{e(L(S['copied']))}" aria-label="{e(L(S['copy']))}">{ICONS['copy']}</button></p>
    <p class="c-status" role="status" data-cstatus></p>
    <p class="cvs"><a class="btn ghost" href="{cv_fr}" download>{ICONS['dl']}CV FR</a><a class="btn ghost" href="{cv_en}" download>{ICONS['dl']}CV EN</a></p>
    <p class="social"><a href="{C.LINKEDIN}" target="_blank" rel="noopener">{ICONS['in']}LinkedIn</a><a href="{C.GITHUB}" target="_blank" rel="noopener">{ICONS['gh']}GitHub</a></p>
  </div>
</aside>"""

    closing = f"""
<section class="closing" aria-label="{e(L(C.CONTACT2['facts'][0][0]))}"><div class="wrap"><div>
  <p>{rich(L(C.CLOSING))}</p>
  <p class="cta"><a class="btn primary" href="{mailto}">{ICONS['mail']}{e(L(T['cta_mail']))}</a><a class="btn ghost" href="{cv_mine}" download>{ICONS['dl']}{e(L(T['cta_cv']))}</a></p>
</div></div></section>"""

    nav_items = [("profil", ("Profil", "Profile")), ("chaine", ("Méthode", "Method")), ("parcours", ("Expérience", "Experience")),
                 ("competences", ("Compétences", "Skills")), ("formation", ("Formation", "Education")), ("contact", ("Contact", "Contact"))]
    nav_links = "".join(f'<a href="#{i}">{e(L(t))}</a>' for i, t in nav_items)
    nav = f"""
<nav class="nav" aria-label="Navigation">
  <div class="wrap nav-in">
    <a class="brand" href="#top"><img src="{base}assets/thasin.webp" width="28" height="28" alt=""><span class="bn">Thasin Jahangir</span><span class="br">{e(L(C.HERO['role']))}</span></a>
    <div class="nav-links">{nav_links}</div>
    <details class="menu"><summary><span class="ms">{e(L(C.HERO2['menu']))}</span></summary><div class="menu-in">{nav_links}</div></details>
    <div class="nav-tools">
      <a class="lang" href="{other_href}" hreflang="{'en' if lang == 'fr' else 'fr'}" lang="{'en' if lang == 'fr' else 'fr'}" title="{e(L(C.UI['lang_switch']))}">{e(L(C.UI['lang_switch_short']))}</a>
      <button type="button" class="theme" id="theme" aria-label="{e(L(C.UI['theme']))}">{ICONS['sun']}{ICONS['moon']}</button>
      <a class="btn primary sm" href="{mailto}">{e(L(T['cta_mail']))}</a>
    </div>
  </div>
</nav>"""

    mbar = (f'<div class="mbar"><a class="btn primary" href="{mailto}">{ICONS["mail"]}{e(L(T["cta_mail"]))}</a>'
            f'<a class="btn ghost" href="{cv_mine}" download>{ICONS["dl"]}{e(L(T["cta_cv"]))}</a></div>')

    ld = {
        "@context": "https://schema.org", "@type": "Person", "name": "Thasin Jahangir",
        "jobTitle": L(C.HERO["role"]), "url": url_self, "email": C.EMAIL,
        "image": f"{C.SITE}/assets/thasin.jpg",
        "address": {"@type": "PostalAddress", "addressLocality": "Paris", "addressCountry": "FR"},
        "worksFor": {"@type": "Organization", "name": "SASU ATMAN"},
        "sameAs": [C.LINKEDIN, C.GITHUB],
        "knowsLanguage": ["fr", "en", "bn", "es"],
        "description": L(C.META["desc"]),
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
<meta name="theme-color" content="#0d2633">
<link rel="canonical" href="{url_self}">
<link rel="alternate" hreflang="fr" href="{url_fr}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="x-default" href="{url_fr}">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Thasin Jahangir">
<meta property="og:title" content="{e(L(C.META['title']))}">
<meta property="og:description" content="{e(L(C.META['desc']))}">
<meta property="og:url" content="{url_self}">
<meta property="og:locale" content="{'fr_FR' if lang == 'fr' else 'en_GB'}">
<meta property="og:image" content="{C.SITE}/assets/{'og.png' if lang == 'fr' else 'og-en.png'}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(L(C.HERO['role']))} — Thasin Jahangir. {e(L(C.HERO['tagline']))}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{base}assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/site.css?v={ver('assets/site.css')}">
<script>
(function(){{try{{var t=localStorage.getItem('theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}document.documentElement.classList.add('js');}})();
</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#profil">{e(L(C.UI['skip']))}</a>
{nav}
<main>
{top}
<div class="wrap layout">
  <div class="main">
{profil}
{chaine}
{parcours}
{competences}
{ia}
{formation}
{interets}
  </div>
{aside}
</div>
{closing}
</main>
<footer class="foot"><div class="wrap"><p><strong>Thasin Jahangir</strong> · {e(L(C.HERO['role']))} · {e(L(C.CONTACT['legal']))}</p><p><a href="{mailto}">{C.EMAIL}</a> · © 2026</p></div></footer>
{mbar}
<script src="{base}assets/site.js?v={ver('assets/site.js')}" defer></script>
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
