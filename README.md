# atmantest.github.io

CV en ligne bilingue de Thasin Jahangir (FR par défaut, EN dans `/en/`), même structure et même langage visuel que le CV PDF. Site statique, sans dépendance externe ni cookie ; police Inter (OFL) hébergée dans `assets/fonts/`.

## Modifier le contenu

Tout le texte est dans `build/content.py` (un tuple `(FR, EN)` par texte), seule source des deux pages. La règle : chaque phrase doit se retrouver dans les CV PDF de `cv/`.

```sh
python3 build/build.py   # régénère index.html, en/index.html, robots.txt, sitemap.xml
python3 build/check.py   # recette statique : règles d'or, typographie FR, mots-clés ATS, SEO, liens, parité FR/EN
python3 build/e2e.py     # tests d'interaction Playwright (chaîne QA, missions, thème, langue, copie, responsive, sans JS)
python3 build/og.py      # régénère les images Open Graph (assets/og.png, assets/og-en.png)
```

`build/e2e.py` et `build/og.py` demandent `pip install playwright && python3 -m playwright install chromium`.
