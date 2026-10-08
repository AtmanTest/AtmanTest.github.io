# Versions du site

Chaque version est un tag git. Voir toutes les versions : `git tag -n`.

| Tag | Contenu |
|---|---|
| `v5.5` | Version courante. Liens Coursera corrigés (Postman, SQL, Python, SAP, Intro IA) d'après le CV. Liens attestation ISTQB / certificat IMESG retirés : les images du CV (`jobhunt/.../cv_octs_page1.jpg`, `page2.jpg`) renvoient 404. |
| `v5.4` | Liens rétablis dans « Formation » : « attestation de formation » (ISTQB) et « certificat » (IMESG), comme sur le CV. |
| `v5.3` | Retour à la section « Ce que vous obtenez » de la v5 (6 cartes avec liens de preuve), avec **toutes** les entreprises citées. « Où je l'ai pratiqué » restauré dans la chaîne QA, avec les six entreprises. Carte « Une culture cybersécurité » supprimée. Cybersécurité (Bitdefender 2007-2011, Witigo 2011-2016) uniquement dans la mission Profil Technology. |
| `v5.2-a-eviter` | Ajout non demandé de la carte cybersécurité, liens de preuve retirés. |
| `v5.0` | Le site comme version web du CV (version validée). |

## Revenir à une version

Aperçu local : `git checkout v5.0` (puis `git checkout main` pour revenir).

Rétablir en ligne, sans perdre l'historique :

    git revert --no-edit v5.3..main     # annule les commits postérieurs à v5.3
    # ou, pour restaurer l'état exact d'un tag :
    git checkout v5.0 -- . && git commit -m "Retour à v5.0" && git push
