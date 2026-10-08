#!/usr/bin/env python3
"""Recette statique du site : règles d'or du contenu, typographie, parité FR/EN, liens internes.
Usage : python3 build/check.py   (code de sortie 1 en cas d'anomalie)
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = {"fr": ROOT / "index.html", "en": ROOT / "en" / "index.html"}
NB = " "


class Page(HTMLParser):
    """Texte visible par élément identifié, ids, liens, structure."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.ids, self.hrefs, self.tags, self.stack = [], set(), [], {}, []
        self.skip = 0
        self.scopes = {}  # id de section -> texte
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag in ("script", "style"):
            self.skip += 1
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href"):
            self.hrefs.append(a["href"])
        self.tags[tag] = self.tags.get(tag, 0) + 1
        if tag in ("void", "meta", "link", "br", "img", "input"):
            return
        self.stack.append(a.get("id"))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in ("meta", "link", "br", "img", "input"):
            return
        if self.stack:
            self.stack.pop()

    def handle_data(self, d):
        if self.skip or not d.strip():
            return
        self.text.append(d)
        for sid in self.stack:
            if sid:
                self.scopes[sid] = self.scopes.get(sid, "") + " " + d


errors = []


def fail(lang, msg):
    errors.append(f"[{lang}] {msg}")


parsed = {}
for lang, path in PAGES.items():
    raw = path.read_text(encoding="utf-8")
    pg = Page()
    pg.feed(raw)
    parsed[lang] = pg
    text = " ".join(pg.text)
    low = text.lower()

    # ---- Règles d'or ----
    if re.search(r"(\+33|0)\s?7[\s.]?69[\s.]?78", raw):
        fail(lang, "numéro de téléphone présent sur le site public")
    if "malt" in raw.lower():
        fail(lang, "lien ou mention Malt")
    for w in ("tjm", "day rate", "day-rate", "salaire", "salary", "témoignage", "testimonial"):
        if w in low:
            fail(lang, f"terme interdit : {w}")
    bred = pg.scopes.get("job-bred", "").lower()
    if not bred:
        fail(lang, "mission BRED introuvable")
    for w in ("oracle", "postgres", "écritures", "comité", "committee", "valide la comptabilité", "validates the accounting"):
        if w in bred:
            fail(lang, f"périmètre BRED dépassé : « {w} »")
    certs = pg.scopes.get("formation", "")
    if re.search(r"ISTQB[^.]*certifi(é|ed|cation)", text, re.I):
        fail(lang, "ISTQB présenté comme une certification")
    if "attestation" not in certs and "attendance" not in certs:
        fail(lang, "ISTQB : mention « attestation de formation » absente")
    if re.search(r"\b(C1|C2)\b", text):
        fail(lang, "niveau d'anglais gonflé (C1/C2)")
    if "B2" not in text:
        fail(lang, "niveau d'anglais B2 absent")

    # ---- Mots-clés ATS présents dans le HTML ----
    kw = ["Jira", "Xray", "Zephyr", "TestRail", "Agile", "ISTQB", "UAT", "Go/No", "Playwright", "SQL", "Confluence"]
    kw += ["recette fonctionnelle", "cahier de recette", "TNR"] if lang == "fr" else ["functional testing", "acceptance handbook", "regression"]
    for k in kw:
        if k.lower() not in low:
            fail(lang, f"mot-clé ATS manquant : {k}")

    # ---- Typographie française ----
    if lang == "fr":
        for m in re.finditer(r"\S( [:;?!»])", text):
            ctx = text[max(0, m.start() - 25): m.end() + 5]
            fail(lang, f"espace normale avant « {m.group(1).strip()} » : …{ctx}…")
        if "« " in text:
            fail(lang, "espace normale après « ")
        if re.search(r"\b(qq|svp|etc\.\.)", low):
            fail(lang, "abréviation familière")
    if "  " in text.replace(NB, " ").replace("\n", " ") and False:
        pass

    # ---- Accessibilité / SEO ----
    if pg.lang != lang:
        fail(lang, f"attribut lang incorrect : {pg.lang}")
    if pg.tags.get("h1") != 1:
        fail(lang, f"{pg.tags.get('h1')} titres h1 (attendu : 1)")
    for need in ('rel="canonical"', 'hreflang="fr"', 'hreflang="en"', 'og:image"', 'application/ld+json', 'name="description"'):
        if need not in raw:
            fail(lang, f"balise SEO manquante : {need}")
    for m in re.finditer(r"<img(?![^>]*\balt=)", raw):
        fail(lang, "image sans texte alternatif")

    # ---- Liens internes et fichiers ----
    base = path.parent
    for h in pg.hrefs:
        if h.startswith("#") and len(h) > 1 and h[1:] not in pg.ids:
            fail(lang, f"ancre cassée : {h}")
        elif not re.match(r"^(https?:|mailto:|#)", h):
            target = (base / h.split("#")[0].split("?")[0]).resolve()
            if h.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                fail(lang, f"fichier introuvable : {h}")

# ---- Parité FR / EN ----
fr, en = parsed["fr"], parsed["en"]
for tag in ("section", "details", "li", "h2", "h3", "a", "button", "td", "dt"):
    if fr.tags.get(tag) != en.tags.get(tag):
        errors.append(f"[parité] <{tag}> : FR {fr.tags.get(tag)} ≠ EN {en.tags.get(tag)}")
if fr.ids != en.ids:
    errors.append(f"[parité] ids différents : {sorted(fr.ids ^ en.ids)}")
nums = lambda p: sorted(re.findall(r"\b\d{2,4}\b", " ".join(p.text)))
if nums(fr) != nums(en):
    diff = set(nums(fr)) ^ set(nums(en))
    errors.append(f"[parité] chiffres différents entre FR et EN : {sorted(diff)}")

if errors:
    print(f"{len(errors)} anomalie(s) :")
    print("\n".join("  ✗ " + x for x in errors))
    sys.exit(1)
print("✓ Recette statique : aucune anomalie (règles d'or, typographie, ATS, SEO, liens, parité FR/EN).")
