# atmantest.github.io

CV en ligne bilingue de Thasin Jahangir (FR par défaut, EN dans `/en/`). Site statique, sans dépendance externe ni cookie ; polices hébergées dans `assets/fonts/`.

## Modifier le contenu

Tout le texte est dans `build/content.py` (un tuple `(FR, EN)` par texte), seule source des deux pages. La règle : chaque phrase doit se retrouver dans les CV PDF de `cv/`.

```sh
python3 build/build.py   # régénère index.html, en/index.html, robots.txt, sitemap.xml
python3 build/check.py   # recette statique : règles d'or, typographie FR, mots-clés ATS, SEO, liens, parité FR/EN
python3 build/e2e.py     # tests d'interaction Playwright (onglets, matrice, thème, langue, copie, responsive, sans JS)
python3 build/og.py      # régénère les images Open Graph (assets/og.png, assets/og-en.png)
```

`build/e2e.py` et `build/og.py` demandent `pip install playwright && python3 -m playwright install chromium`.

## Scènes 3D

`assets/scene.js` est construit à partir de `build/scene/main.js` (three.js, MIT, seuls les modules utilisés sont embarqués) :

```sh
cd build && npm ci && npm run build
```

- **Hero** : le champ de couverture. Le survol couvre les cas de test ; trois anomalies s'y cachent, les corriger donne le GO.
- **Méthode** : la recette pilotée par le défilement. Une release candidate traverse les huit portes, prend une anomalie à la porte 6, puis reçoit le GO.
- La 3D se charge après le contenu (première interaction ou 3,5 s) et seulement si le rendu WebGL est matériel. Sinon, ou sans JavaScript, la page reste complète : champ 2D et liste des étapes.
- Cinq anomalies sont aussi cachées dans la page (compteur dans la barre de navigation).

La recette complète tourne sur GitHub Actions à chaque push (`.github/workflows/recette.yml`).
