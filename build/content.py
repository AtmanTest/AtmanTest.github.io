# Contenu bilingue du site. Chaque texte est un tuple (FR, EN).
# Source : CV_Thasin_Jahangir_QA_2026_FR/EN.pdf — modifier ici, puis `python3 build/build.py`.

SITE = "https://atmantest.github.io"
EMAIL = "thasin@live.com"
LINKEDIN = "https://www.linkedin.com/in/thasin-j-47582635/"
MALT = "https://www.malt.fr/profile/thasinjahangir"
GITHUB = "https://github.com/AtmanTest"

META = {
    "title": ("Thasin Jahangir — Ingénieur QA Senior, freelance à Paris",
              "Thasin Jahangir — Senior QA Engineer, freelance in Paris"),
    "desc": ("Ingénieur QA Senior freelance à Paris : 15 ans de recette fonctionnelle, stratégie de test, "
             "non-régression et UAT pour la banque, l'hôtellerie, le cloud souverain et la santé. Disponible pour missions longues.",
             "Freelance Senior QA Engineer in Paris: 15 years of functional testing, test strategy, regression and UAT "
             "for banking, hospitality, sovereign cloud and healthcare. Available for long-term assignments."),
}

NAV = [
    ("profil", ("Profil", "Profile")),
    ("chaine", ("Méthode", "Method")),
    ("parcours", ("Parcours", "Experience")),
    ("competences", ("Compétences", "Skills")),
    ("ia", ("IA & projets", "AI & projects")),
    ("formation", ("Formation", "Education")),
    ("contact", ("Contact", "Contact")),
]

HERO = {
    "name": "Thasin Jahangir",
    "role": ("Ingénieur QA Senior", "Senior QA Engineer"),
    "tagline": ("« Je trouve ce qui casse avant vos utilisateurs. »", "“I find what breaks before your users do.”"),
    "sub": ("20 ans en IT dont 15 en tests & recette. Recette fonctionnelle, stratégie de test, tests de non-régression (TNR) et recette utilisateur (UAT).",
            "20 years in IT, 15 of them in testing & acceptance. Functional testing, test strategy, regression testing and user acceptance testing (UAT)."),
    "status": ("Prochaine mission : sélection en cours", "Next assignment: selection in progress"),
    "status2": ("Missions longues privilégiées", "Long-term assignments preferred"),
    "where": ("Paris / Île-de-France & remote · Freelance SASU, facturation directe",
              "Paris / Île-de-France & remote · Freelance SASU, direct invoicing"),
    "verdict": ("GO", "GO"),
    "verdict_label": ("Verdict de recette", "Acceptance verdict"),
    "run_label": ("Une recette, de bout en bout", "One test run, end to end"),
}

STATS = [
    ("15", ("ans de tests logiciels, 2011 → 2026", "years of software testing, 2011 → 2026")),
    ("4", ("missions longues, de 2 à 6 ans chez le même client", "long assignments, 2 to 6 years with the same client")),
    ("100+", ("pays pour les applications Accor, iOS & Android", "countries served by the Accor apps, iOS & Android")),
    ("6", ("grands comptes : banque, santé, cloud", "major accounts: banking, healthcare, cloud")),
]

CLIENTS = {
    "label": ("Ils m'ont confié leur recette fonctionnelle", "They trusted me with their functional testing"),
    "names": "BRED Banque Populaire · Accor · Oodrive · Vinci Construction · Visiodent · Profil Technology",
    "sectors": ("Banque · Hôtellerie internationale · Cloud souverain · Santé · ERP & consolidation financière · Cybersécurité",
                "Banking · International hospitality · Sovereign cloud · Healthcare · ERP & financial consolidation · Cybersecurity"),
}

PROFIL = {
    "title": ("Profil", "Profile"),
    "lead": ("Ingénieur QA Senior avec 15 ans d'expérience en recette fonctionnelle : je transforme les besoins métier en plans de test, "
             "je détecte les anomalies qui comptent et je donne aux équipes projet un Go/NoGo clair, fondé sur des preuves.",
             "Senior QA Engineer with 15 years of hands-on functional testing: I turn business requirements into test plans, "
             "find the defects that matter and give project teams a clear, evidence-based Go/No-Go."),
    "body": [
        ("Autonome et vrai esprit d'équipe, à l'aise avec les responsables métier, les Business Analysts et les développeurs. "
         "Je couvre toute la chaîne de la qualité logicielle, de l'analyse des besoins au Go/NoGo.",
         "Autonomous and a true team player, at ease with business owners, Business Analysts and developers alike. "
         "I cover the whole software-quality chain, from requirements analysis to Go/No-Go."),
        ("Chez BRED Banque Populaire, j'ai conçu les cas de test et les cahiers de recette sous Xray / Jira pour la recette IT d'un nouvel outil P2P "
         "de facturation électronique, et contrôlé par SQL la reprise des données de l'ancienne base vers la nouvelle. "
         "Chez Accor (applications iOS / Android déployées dans plus de 100 pays), Oodrive, Visiodent et Vinci Construction, "
         "j'ai mené cette chaîne de bout en bout, avec les techniques ISTQB et des campagnes multi-équipes dans Jira / Xray.",
         "At BRED Banque Populaire, I designed the test cases and acceptance handbooks in Xray / Jira for the IT acceptance testing of a new P2P "
         "e-invoicing tool, and checked with SQL the migration of data from the legacy database to the new one. "
         "At Accor (iOS / Android apps deployed in 100+ countries), Oodrive, Visiodent and Vinci Construction, "
         "I ran this chain end to end, using ISTQB techniques and multi-team campaigns in Jira / Xray."),
        ("Rigoureux et proche du métier : je sais quoi tester, où sont les risques et comment les remonter clairement.",
         "Rigorous and close to the business: I know what to test, where the risks are and how to report them clearly."),
    ],
}

# Les 8 étapes sont une vraie séquence : numérotation justifiée.
CHAIN = {
    "title": ("La chaîne QA, de bout en bout", "The full QA chain, end to end"),
    "intro": ("Huit étapes, de la première user story au rapport final. Choisissez-en une pour voir ce que je fais concrètement, et où je l'ai fait.",
              "Eight steps, from the first user story to the final report. Pick one to see what I actually do, and where I did it."),
    "where": ("Où je l'ai pratiqué", "Where I practised it"),
    "steps": [
        {"name": ("Analyse des besoins", "Requirements analysis"),
         "text": ("Lecture des user stories et des spécifications avec le PO, critères d'acceptation, testabilité dès la conception. Je pose les questions qui évitent un défaut avant qu'il ne soit codé.",
                  "Reading user stories and specifications with the PO, acceptance criteria, testability from design. I ask the questions that prevent a defect before it is coded."),
         "where": "Accor · BRED · Visiodent"},
        {"name": ("Stratégie & plan de test", "Test strategy & plan"),
         "text": ("Plans de test, périmètre et priorisation par les risques, critères d'entrée / sortie. Chez Oodrive, j'ai structuré la pratique QA de l'éditeur : modèles de plans de test et workflow d'anomalies.",
                  "Test plans, scope and risk-based prioritisation, entry / exit criteria. At Oodrive, I structured the publisher's QA practice: test plan templates and defect workflow."),
         "where": "Oodrive · Visiodent"},
        {"name": ("Conception des cas de test", "Test case design"),
         "text": ("Cas de test et matrices de couverture avec les techniques ISTQB (partitions d'équivalence, valeurs limites, tables de décision, transitions d'état). Scénarios formalisés en Gherkin, cahiers de recette sous Xray / Jira.",
                  "Test cases and coverage matrices using ISTQB techniques (equivalence partitioning, boundary values, decision tables, state transitions). Scenarios formalised in Gherkin, acceptance handbooks in Xray / Jira."),
         "where": "BRED · Accor · Vinci Construction"},
        {"name": ("Environnements & données", "Environments & test data"),
         "text": ("Appareils réels et BrowserStack pour le mobile, ferme de VM Nutanix pour le multi-OS, plateformes de test Windows / macOS / Linux / Android / iOS, jeux de données de test.",
                  "Real devices and BrowserStack for mobile, a Nutanix VM farm for multi-OS, Windows / macOS / Linux / Android / iOS test platforms, test data preparation."),
         "where": "Accor · Oodrive · Profil Technology"},
        {"name": ("Exécution des tests", "Test execution"),
         "text": ("Campagnes fonctionnelles, de non-régression et de compatibilité (mobile, cross-browser, multi-OS), tests exploratoires. Notifications push, installation / mise à jour, reprise après arrêt forcé, multilingue, multi-devises.",
                  "Functional, regression and compatibility campaigns (mobile, cross-browser, multi-OS), exploratory testing. Push notifications, install / upgrade, recovery after forced kill, multi-language, multi-currency."),
         "where": "Accor · Oodrive · BRED"},
        {"name": ("Gestion des anomalies", "Defect management"),
         "text": ("Analyse des échanges réseau et API (Charles Proxy), qualification avec analyse d'impact dans Jira / Xray, suivi jusqu'au re-test. Contrôles SQL de la reprise de données chez BRED. Support niveau 3 des comptes clés chez Oodrive.",
                  "Analysis of network and API exchanges (Charles Proxy), qualification with impact analysis in Jira / Xray, follow-up through re-test. SQL checks on the data migration at BRED. Level-3 support for key accounts at Oodrive."),
         "where": "Accor · BRED · Oodrive"},
        {"name": ("Recette & Go/NoGo", "Acceptance & Go/No-Go"),
         "text": ("Recette utilisateur (UAT, FAT / SAT) et mise en production (MEP). Chez Accor, un Go/NoGo clair, fondé sur des preuves, remis au product management.",
                  "User acceptance testing (UAT, FAT / SAT) and production release. At Accor, a clear, evidence-based Go/No-Go delivered to product management."),
         "where": "Accor"},
        {"name": ("Reporting & rétrospective", "Reporting & retrospective"),
         "text": ("Reporting de l'avancement au daily, bilans de recette et indicateurs qualité (KPI), retours d'expérience pour la campagne suivante.",
                  "Progress reporting at the daily stand-up, test reports and quality KPIs, lessons learned for the next campaign."),
         "where": "BRED · Accor · Oodrive"},
    ],
}

# start / end en années décimales pour la frise
JOBS = [
    {"id": "bred", "client": "BRED Banque Populaire", "start": 2023.25, "end": 2026.42, "short": "BRED",
     "title": ("Facturation électronique & conformité réglementaire", "Electronic invoicing & regulatory compliance"),
     "role": ("Consultant QA Senior — Freelance SASU", "Senior QA Consultant — Freelance SASU"),
     "dates": ("Avr. 2023 — Mai 2026 · Paris", "Apr. 2023 — May 2026 · Paris"),
     "dur": ("3 ans", "3 yrs"),
     "intro": ("Programme de mise en conformité de la réforme de la facturation électronique, périmètre P2P / O2C, SI bancaire (Mainframe, SQL), avec la comptabilité et les équipes DSI.",
               "Compliance programme for the electronic invoicing reform, P2P / O2C scope, banking IS (Mainframe, SQL), with the accounting department and the IT (DSI) teams."),
     "bullets": [
         ("Recette IT du nouvel outil P2P : conception des cas de test et des cahiers de recette sous Xray / Jira, à partir des user stories.",
          "IT acceptance testing of the new P2P tool: design of the test cases and acceptance handbooks in Xray / Jira, based on the user stories."),
         ("Contrôles SQL de la reprise de données : vérification que les données de l'ancienne base (base COM) sont correctement reprises dans la nouvelle base, sur la bonne source.",
          "SQL checks on the data migration: verifying that data from the legacy database (COM database) is correctly migrated into the new database, from the right source."),
         ("Exécution des campagnes de test, suivi des anomalies et reporting de l'avancement au daily.",
          "Execution of the test campaigns, defect follow-up and progress reporting at the daily stand-up."),
         ("Collaboration avec la comptabilité, la DSI (propriétaire des données), les Business Analysts et les développeurs, en Agile / Scrum.",
          "Collaboration with accounting, IT (DSI, the data owner), Business Analysts and developers, in Agile / Scrum."),
     ],
     "env": "Jira, Xray, SQL, Mainframe, Corcentric, ServiceNow, Confluence — Agile / Scrum"},
    {"id": "accor", "client": "Accor", "start": 2019.67, "end": 2022.99, "short": "Accor",
     "title": ("Applications mobiles iOS & Android, 100+ pays", "Mobile apps iOS & Android, 100+ countries"),
     "role": ("Responsable QA Mobile — Consultant", "Mobile QA Lead — Consultant"),
     "dates": ("Sept. 2019 — Déc. 2022 · Paris", "Sep. 2019 — Dec. 2022 · Paris"),
     "dur": ("3 ans 4 mois", "3 yrs 4 mo"),
     "intro": ("Lead QA de l'équipe « parcours de réservation » du premier groupe hôtelier européen, sur des applications déployées dans plus de 100 pays. Toute la chaîne QA :",
               "QA lead for the “booking journey” feature team of Europe's #1 hotel group, on apps deployed in more than 100 countries. The full QA chain:"),
     "bullets": [
         ("Analyse des besoins : étude des user stories avec le PO, critères d'acceptation, testabilité dès la conception.",
          "Requirements analysis: study of user stories with the PO, acceptance criteria, testability from design."),
         ("Conception des cas de test du parcours E2E critique (connexion → recherche d'hôtel → disponibilités → chambre / tarif / options → devises → paiement → confirmation) ; formalisation Gherkin des scénarios.",
          "Test case design for the critical E2E journey (login → hotel search → availability → room / rate / options → currencies → payment → confirmation); Gherkin formalisation of the scenarios."),
         ("Exécution des campagnes fonctionnelles, de non-régression et de compatibilité (Android / iOS, appareils réels, BrowserStack) : notifications push, installation / mise à jour, reprise après arrêt forcé, multilingue, multi-devises.",
          "Execution of functional, regression and compatibility campaigns (Android / iOS, real devices, BrowserStack): push notifications, install / upgrade, recovery after forced kill, multi-language, multi-currency."),
         ("Gestion des anomalies : analyse des échanges réseau et API (Charles Proxy), qualification avec analyse d'impact dans Jira / Xray, suivi jusqu'au re-test.",
          "Defect management: analysis of network and API exchanges (Charles Proxy), qualification with impact analysis in Jira / Xray, follow-up through re-test."),
         ("Reporting Go/NoGo auprès du product management ; cas de test automatisés (Appium) en appui des ingénieurs d'automatisation.",
          "Go/No-Go reporting to product management; automated test cases (Appium) supporting the automation engineers."),
     ],
     "env": "Jira, Xray, BrowserStack, TestFlight, Charles Proxy, Crashlytics, Gherkin, Appium, Android, iOS, Confluence"},
    {"id": "visiodent", "client": "Visiodent", "start": 2019.42, "end": 2019.67, "short": "Visiodent",
     "title": ("Éditeur de logiciels de santé (Veasy)", "Healthcare software publisher (Veasy)"),
     "role": ("Responsable Qualité Logiciel", "Software Quality Manager"),
     "dates": ("Juin — Août 2019 · Paris", "Jun — Aug 2019 · Paris"),
     "dur": ("3 mois", "3 mo"),
     "intro": None,
     "bullets": [
         ("Analyse des parcours métier et des exigences réglementaires ; intégration de la lecture de la Carte Vitale dans les scénarios de test.",
          "Analysis of business journeys and regulatory requirements; integration of French health insurance card (Carte Vitale) reading into test scenarios."),
         ("Plans de test, matrices de couverture et cas de test sur les parcours métier et réglementaires.",
          "Test plans, coverage matrices and test cases on business and regulatory journeys."),
         ("Exécution des campagnes fonctionnelles, de non-régression et de compatibilité cross-browser ; gestion des anomalies et reporting qualité.",
          "Execution of functional, regression and cross-browser compatibility campaigns; defect management and quality reporting."),
         ("Management d'une équipe de testeurs et supervision d'un prestataire d'automatisation externe sur le logiciel métier de santé Veasy.",
          "Lead of a team of testers and supervision of an external automation vendor on the Veasy healthcare business software."),
     ],
     "env": "Jira, Xray, Dynatrace, CloudNetCare"},
    {"id": "oodrive", "client": "Oodrive", "start": 2017.04, "end": 2019.33, "short": "Oodrive",
     "title": ("Cloud souverain B2B/B2C (BoardNox, WebSynchro, PostFiles)", "Sovereign cloud B2B/B2C (BoardNox, WebSynchro, PostFiles)"),
     "role": ("Ingénieur Qualité Logiciel / Responsable QA", "Software Quality Engineer / QA Manager"),
     "dates": ("Janv. 2017 — Avr. 2019 · Paris", "Jan. 2017 — Apr. 2019 · Paris"),
     "dur": ("2 ans 4 mois", "2 yrs 4 mo"),
     "intro": ("Responsable qualité de 3 produits critiques du cloud souverain français : gouvernance des conseils d'administration, synchronisation chiffrée, transfert sécurisé de gros fichiers.",
               "Quality lead on 3 critical products of the French sovereign cloud: board meeting governance, encrypted synchronisation, secure transfer of large files."),
     "bullets": [
         ("Structuration de la pratique QA de l'éditeur : modèles de plans de test, critères d'entrée / sortie, workflow de gestion des anomalies dans Jira / Zephyr.",
          "Structuring the publisher's QA practice: test plan templates, entry / exit criteria, defect workflow in Jira / Zephyr."),
         ("Analyse des besoins, conception et exécution des cas de test sur les 3 produits : campagnes fonctionnelles et de non-régression des versions majeures.",
          "Requirements analysis, test case design and execution across the 3 products: functional and regression campaigns for major releases."),
         ("Validation de la compatibilité multi-OS (Windows / macOS) sur ferme de VM Nutanix, cross-browser (Chrome, Firefox, Edge, Safari) et multi-versions d'Outlook.",
          "Validation of multi-OS compatibility (Windows / macOS) on a Nutanix VM farm, cross-browser (Chrome, Firefox, Edge, Safari) and multi-version Outlook."),
         ("Gestion des anomalies et reporting qualité ; support niveau 3 des comptes clés (diagnostic, reproductibilité, escalade ciblée).",
          "Defect management and quality reporting; level-3 support for key accounts (diagnosis, reproducibility, targeted escalation)."),
         ("Mise en place de l'automatisation des tests de non-régression (Ranorex) pour accélérer les cycles de validation.",
          "Introduction of regression test automation (Ranorex) to speed up validation cycles."),
     ],
     "env": "Jira, Zephyr, Ranorex, Nutanix, VMware, Confluence, Windows / macOS / Linux, Outlook"},
    {"id": "vinci", "client": "Vinci Construction", "start": 2016.75, "end": 2017.04, "short": "Vinci",
     "title": ("Applications SAP BPC (consolidation financière)", "SAP BPC applications (financial consolidation)"),
     "role": ("Consultant QA / Ingénieur Qualité", "QA Consultant / Quality Engineer"),
     "dates": ("Oct. 2016 — Janv. 2017 · Paris", "Oct. 2016 — Jan. 2017 · Paris"),
     "dur": ("4 mois", "4 mo"),
     "intro": ("Recette fonctionnelle d'applications SAP BPC : conformité, intégrité et cohérence des données des états financiers consolidés. "
               "Analyse des exigences métier, conception des cas de test, exécution des campagnes de validation, suivi des anomalies et reporting.",
               "Functional testing of SAP BPC applications: compliance, data integrity and consistency of consolidated financial statements. "
               "Analysis of business requirements, test case design, execution of validation campaigns, defect tracking and reporting."),
     "bullets": [],
     "env": "Redmine, TestRail, SAP BPC, SAP HANA"},
    {"id": "profil", "client": "Profil Technology", "start": 2007.0, "end": 2016.8, "short": "Profil Technology",
     "title": ("R&D Witigo, contrôle parental multi-plateforme", "Witigo R&D, multi-platform parental control"),
     "role": ("Ingénieur Tests & Support N3 · auparavant Support N3 – Malware Analyst – Testeur",
              "Test Engineer & Level-3 Support · previously Level-3 Support – Malware Analyst – Tester"),
     "dates": ("Janv. 2007 — Oct. 2016 · Paris", "Jan. 2007 — Oct. 2016 · Paris"),
     "dur": ("9 ans 10 mois", "9 yrs 10 mo"),
     "intro": ("Division R&D de Profil Technology, éditeur de Witigo, gamme grand public de protection des enfants sur internet (filtrage de contenus numériques), "
               "développée from scratch sur Windows, macOS et Android, avec une brique de détection d'images reposant sur des approches d'IA précoces (2011 – 2016).",
               "R&D division of Profil Technology, publisher of Witigo, a consumer range protecting children online (digital content filtering), "
               "built from scratch across Windows, macOS and Android, with an image-detection component based on early AI approaches (2011 – 2016)."),
     "bullets": [
         ("Recette fonctionnelle de Witigo sur Windows, macOS et Android : filtrage des sites par catégories et par langue, listes blanche / noire, plages horaires, filtrage par mots-clés, contrôle des applications.",
          "Functional testing of Witigo on Windows, macOS and Android: website filtering by category and language, allow / block lists, time schedules, keyword filtering, application control."),
         ("Recette de la brique de détection d'images (approche IA précoce) et des composants multi-environnements du produit.",
          "Testing of the image-detection component (early AI approach) and of the product's multi-environment components."),
         ("Analyse des spécifications et des évolutions produit, conception des plans de test et campagnes de tests fonctionnels, de non-régression et d'acceptation multi-plateformes ; cas de test (TestLink, Excel) ; gestion des anomalies de la rédaction du bug à la clôture (Flyspray, BugProfiler).",
          "Specification analysis of product changes, test plan design and functional, regression and acceptance test campaigns across platforms; test cases (TestLink, Excel); defect management from bug report to closure (Flyspray, BugProfiler)."),
         ("Mise en place des plateformes de test (Windows, macOS, Linux, tablettes Android, iOS, VMware / VirtualBox, images système) ; automatisation de tâches répétitives (AutoIT) ; reporting et levée d'alertes.",
          "Set up test platforms (Windows, macOS, Linux, Android tablets, iOS, VMware / VirtualBox, system images); automation of repetitive tasks (AutoIT); reporting and raising alerts."),
         ("Propositions d'amélioration du produit (ergonomie, options) ; support N1 à N3 en français, anglais et espagnol, rédaction de FAQ, support avant-vente d'un client important.",
          "Product improvement proposals (ergonomics, options); level 1 to 3 support in French, English and Spanish, FAQ writing, pre-sales support for a key customer."),
         ("2007 – 2011, les débuts : support N3 Bitdefender (Retail et Corporate), analyse de malwares, laboratoire de tests sur DMZ, premiers tests des produits Bitdefender et du proxy WebFilter.",
          "2007 – 2011, the early years: Bitdefender level-3 support (Retail and Corporate), malware analysis, DMZ test lab, first tests of Bitdefender products and the WebFilter proxy."),
     ],
     "env": "TestLink, Flyspray, BugProfiler, AutoIT, VMware, VirtualBox, Windows / macOS / Linux, Android, iOS"},
]

PARCOURS = {
    "title": ("Parcours", "Experience"),
    "intro": ("Vingt ans, du support technique à la direction de la recette. Cliquez sur une mission pour lire le détail.",
              "Twenty years, from technical support to leading acceptance testing. Open an assignment to read the detail."),
    "phases": [
        (2006.0, 2011.0, ("Support technique", "Technical support")),
        (2011.0, 2016.0, ("QA & support N3", "QA & L3 support")),
        (2016.0, 2026.5, ("QA Lead Engineer", "QA Lead Engineer")),
    ],
    "env": ("Environnement", "Environment"),
    "first": ("Premiers pas (2006 – 2007), support technique : Conforama — Ingénieur support micro-informatique · Samsung — Ingénieur support",
              "First steps (2006 – 2007), technical support: Conforama — IT Support Engineer · Samsung — Support Engineer"),
    "timeline_label": ("Frise des missions de 2006 à 2026", "Assignments timeline, 2006 to 2026"),
}

SKILLS = {
    "title": ("Compétences", "Skills"),
    "groups": [
        {"name": ("Recette fonctionnelle & stratégie de test", "Functional testing & test strategy"),
         "items": (
             ["Recette fonctionnelle", "Recette utilisateur (UAT)", "FAT / SAT", "Analyse des user stories et des spécifications", "Stratégie de test", "Plan de test",
              "Cahier de recette", "Conception de cas de test", "Matrice de couverture", "Tests de non-régression (TNR)", "Tests exploratoires", "Tests E2E",
              "Tests de compatibilité (mobile iOS / Android, cross-browser, multi-OS)", "Jeux de données de test", "Gestion des anomalies",
              "Cadrage et pilotage de la recette", "Bilans de recette et reporting (KPI)", "Go/NoGo", "Mise en production (MEP)", "Priorisation par les risques",
              "Techniques ISTQB (partitions d'équivalence, valeurs limites, tables de décision, transitions d'état)", "Support niveau 3"],
             ["Functional testing", "User acceptance testing (UAT)", "FAT / SAT", "User story and specification analysis", "Test strategy", "Test plan",
              "Acceptance handbook", "Test case design", "Coverage matrix", "Regression testing", "Exploratory testing", "E2E testing",
              "Compatibility testing (mobile iOS / Android, cross-browser, multi-OS)", "Test data preparation", "Defect management",
              "Test scoping and coordination", "Test reports and reporting (KPIs)", "Go/No-Go", "Production release", "Risk-based prioritisation",
              "ISTQB techniques (equivalence partitioning, boundary value analysis, decision table testing, state transition testing)", "Level-3 support"])},
        {"name": ("Outils de test & anomalies", "Test & defect-tracking tools"),
         "items": (["Jira", "Xray", "Zephyr", "TestRail", "TestLink", "Flyspray", "BugProfiler", "Confluence", "ServiceNow", "Redmine",
                    "Postman (API REST, JSON, HTTP, SOAP)", "SQL Oracle", "Mainframe", "SAP BPC / HANA"],
                   ["Jira", "Xray", "Zephyr", "TestRail", "TestLink", "Flyspray", "BugProfiler", "Confluence", "ServiceNow", "Redmine",
                    "Postman (REST API, JSON, HTTP, SOAP)", "SQL Oracle", "Mainframe", "SAP BPC / HANA"])},
        {"name": ("Méthodes & posture", "Methods & soft skills"),
         "items": (["Agile Scrum", "Cycle en V", "3 Amigos", "Shift-left", "BDD / Gherkin", "Coordination multi-équipes", "Interface MOA / métiers",
                    "Encadrement de testeurs", "Supervision de prestataires", "Autonomie", "Esprit d'équipe", "Rigueur", "Créativité", "Sens du détail", "Communication"],
                   ["Agile Scrum", "V-model", "3 Amigos", "Shift-left", "BDD / Gherkin", "Multi-team coordination", "Business-owner liaison",
                    "Tester team lead", "Vendor supervision", "Autonomy", "Team spirit", "Rigour", "Creativity", "Attention to detail", "Communication"])},
        {"name": ("Environnements & mobile", "Environments & mobile"),
         "items": (["BrowserStack", "TestFlight", "Charles Proxy", "Crashlytics", "Dynatrace", "Android / iOS", "Windows / macOS / Linux", "VMware", "VirtualBox", "Nutanix", "Corcentric"],
                   ["BrowserStack", "TestFlight", "Charles Proxy", "Crashlytics", "Dynatrace", "Android / iOS", "Windows / macOS / Linux", "VMware", "VirtualBox", "Nutanix", "Corcentric"])},
        {"name": ("Automatisation & IA appliquée au test", "Automation & AI applied to testing"),
         "items": (["Playwright (E2E, TypeScript)", "Vitest", "Appium", "Ranorex", "AutoIT", "GitHub Actions (CI/CD)", "Git", "Docker", "Python",
                    "Génération de cas de test assistée par IA", "Prompt engineering", "LLM (Claude, GPT, DeepSeek, Ollama, LM Studio)"],
                   ["Playwright (E2E, TypeScript)", "Vitest", "Appium", "Ranorex", "AutoIT", "GitHub Actions (CI/CD)", "Git", "Docker", "Python",
                    "AI-assisted test case generation", "Prompt engineering", "LLMs (Claude, GPT, DeepSeek, Ollama, LM Studio)"])},
    ],
}

AI = {
    "title": ("IA & projets", "AI & projects"),
    "lead": ("Je teste aussi avec des agents. J'orchestre des LLM cloud et locaux pour générer et maintenir des suites Playwright et Vitest, que je spécifie et relis moi-même.",
             "I test with agents too. I orchestrate cloud and local LLMs to generate and maintain Playwright and Vitest suites, which I specify and review myself."),
    "projects": [
        {"name": "Nous AI News",
         "text": ("Agrégation d'actualités IA en temps réel : ingestion de 86 flux RSS, extraction d'entités, catégorisation par LLM, boucle d'auto-amélioration continue. 263 tests et CI/CD GitHub Actions.",
                  "Real-time AI news aggregation: ingestion of 86 RSS feeds, entity extraction, LLM categorisation, continuous self-improvement loop. 263 tests and GitHub Actions CI/CD."),
         "stack": "TypeScript, Next.js 14, Supabase, OpenAI, Tailwind",
         "demo": "https://nous-daily.vercel.app/", "repo": "https://github.com/AtmanTest/nous-ai-news"},
        {"name": "JobHunt",
         "text": ("Tableau de bord de recherche de missions : scraping planifié multi-sources, scoring CV / offres sur 100, détection des doublons, analyse du TJM marché, alertes en temps réel. "
                  "83 tests unitaires et d'intégration, 19 scénarios BDD Gherkin, Playwright E2E.",
                  "Assignment-search dashboard: scheduled multi-source scraping, CV / offer scoring out of 100, duplicate detection, market day-rate analysis, real-time alerts. "
                  "83 unit and integration tests, 19 BDD Gherkin scenarios, Playwright E2E."),
         "stack": "Python, Flask, DeepSeek, Render, GitHub Actions, Playwright, Gherkin",
         "demo": "https://jobhunt-1-ar3w.onrender.com/", "repo": "https://github.com/AtmanTest/jobhunt"},
        {"name": ("Pipelines QA agentiques", "Agentic QA pipelines"),
         "text": ("Orchestration multi-agents pour la QA : délégation des tâches, génération de tests par IA, analyse de régression assistée, mémoire persistante.",
                  "Multi-agent orchestration for QA: task delegation, AI test generation, assisted regression analysis, persistent memory."),
         "stack": "MCP, Claude Code, Codex CLI, DeepSeek, Gemma", "demo": None, "repo": None},
    ],
    "demo": ("Démo", "Demo"),
    "code": ("Code source", "Source code"),
    "stack": ("Stack", "Stack"),
}

EDU = {
    "title": ("Formation", "Education"),
    "certs_title": ("Certifications", "Certifications"),
    "certs": [
        (("PSPO I — Professional Scrum Product Owner", "PSPO I — Professional Scrum Product Owner"), "Scrum.org, 2020", "https://www.scrum.org/user/678954"),
        (("IA générative & Prompt Engineering", "Generative AI & Prompt Engineering"), "Google / Coursera, 2025", "https://www.coursera.org/account/accomplishments/verify/9XZNI1D7BS99"),
        (("Tests d'API avec Postman", "API Testing with Postman"), "Coursera, 2025", "https://www.coursera.org/account/accomplishments/verify/4OEVH2E3WN6Z"),
        (("Gestion de produit numérique", "Digital Product Management"), "Coursera, 2025", "https://www.coursera.org/account/accomplishments/verify/WDJ5GP56DKQ3"),
        (("Syntaxe SQL de base", "Basic SQL Syntax"), "Coursera, 2025", "https://www.coursera.org/account/accomplishments/verify/KWH6Q433FXWY"),
        (("Introduction à Python", "Introduction to Python"), "Coursera, 2025", "https://www.coursera.org/account/accomplishments/verify/JNR9XMHGX03P"),
        (("SAP Professional", "SAP Professional"), "Coursera, 2025", "https://www.coursera.org/account/accomplishments/verify/2CKOHAZJQF8U"),
        (("Introduction à l'IA", "Introduction to AI"), "Coursera, 2025", None),
    ],
    "cert_link": ("Vérifier", "Verify"),
    "edu_title": ("Formation", "Training"),
    "edu": [
        (("ISTQB Foundation Level — formation aux tests logiciels", "ISTQB Foundation Level — software testing training"),
         ("Learning Tree, 2015 · attestation de formation", "Learning Tree, 2015 · certificate of attendance")),
        (("Administrateur sécurité informatique", "IT Security Administrator"), ("IMESG, 2005 · certificat", "IMESG, 2005 · certificate")),
        (("Génie électronique", "Electronic Engineering"), ("Lycée Dorian, Paris, 2005", "Lycée Dorian, Paris, 2005")),
    ],
    "lang_title": ("Langues", "Languages"),
    "langs": [
        (("Français", "French"), ("langue maternelle", "native")),
        (("Anglais", "English"), ("B2 · formation TOEIC 4 skills en cours", "B2 · TOEIC 4 skills training in progress")),
        (("Bengali", "Bengali"), ("courant", "fluent")),
        (("Espagnol", "Spanish"), ("professionnel", "professional")),
    ],
}

INTERESTS = {
    "title": ("Centres d'intérêt", "Interests"),
    "intro": ("Ce que je fais hors mission compte aussi : c'est là que se forment le regard d'utilisateur et la curiosité.",
              "What I do outside assignments counts too: that is where the user's eye and the curiosity come from."),
    "items": [
        (("LLM en local, hardware & multi-OS", "Local LLMs, hardware & multi-OS"),
         ("Je fais tourner des LLM en local sur Apple Silicon (M5 Max, 128 Go), AMD (Vulkan) et NVIDIA sous Ubuntu, et j'aime tester de nouvelles distributions Linux.",
          "I run local LLMs on Apple Silicon (M5 Max, 128 GB), AMD (Vulkan) and NVIDIA on Ubuntu, and I enjoy trying out new Linux distributions."),
         ("Curiosité technique : hardware, software, multi-OS", "Technical curiosity: hardware, software, multi-OS")),
        (("Objets connectés", "Connected devices"),
         ("Smartwatch, Plaud Pro, smartphones, produits de santé connectés.", "Smartwatches, Plaud Pro, smartphones, connected health products."),
         ("Œil d'utilisateur", "A user's eye")),
        (("Vibe coding & agents IA", "Vibe coding & AI agents"),
         ("Claude Code, Hermes Agent, Perplexity, DeepSeek, Harness.", "Claude Code, Hermes Agent, Perplexity, DeepSeek, Harness."),
         ("De l'idée à l'outil qui tourne", "From idea to working tool")),
        (("Street photography", "Street photography"),
         ("Fujifilm série X, dans l'esprit d'Henri Cartier-Bresson : le « moment décisif ».", "Fujifilm X-Series, in the spirit of Henri Cartier-Bresson: the “decisive moment”."),
         ("Sens de l'observation", "Sharp observation")),
        (("Peinture acrylique", "Acrylic painting"),
         ("Abstrait et portrait.", "Abstract and portrait."),
         ("Créativité : utile aussi pour imaginer les cas de test imprévus", "Creativity: also useful to imagine the test cases nobody expected")),
        (("Voyages", "Travel"),
         ("41 pays visités en solo, anglais au quotidien.", "41 countries visited solo, daily English practice."),
         ("Adaptabilité", "Adaptability")),
        (("Kung-fu Wing Chun & méditation", "Kung-fu Wing Chun & meditation"),
         ("Pratique du Wing Chun et de la méditation.", "Wing Chun practice and meditation."),
         ("Discipline, maîtrise de soi", "Discipline, self-control")),
    ],
}

CONTACT = {
    "title": ("Contact", "Contact"),
    "lead": ("Disponible immédiatement, pour des missions longues.", "Available immediately, for long-term assignments."),
    "body": ("Freelance SASU, en facturation directe ou en sous-traitance via ESN. Paris / Île-de-France, remote, hybride ou sur site, et mobile en France et en Europe. Intervention : recette fonctionnelle & pilotage QA.",
             "Freelance SASU, with direct invoicing or subcontracting through consulting firms. Paris / Île-de-France, remote, hybrid or on-site, and mobile across France and Europe. Scope: functional testing & QA leadership."),
    "mail": ("Écrire à Thasin", "Email Thasin"),
    "cv_fr": ("Télécharger le CV (PDF, français)", "Download the CV (PDF, French)"),
    "cv_en": ("Télécharger le CV (PDF, anglais)", "Download the CV (PDF, English)"),
    "other": ("Ailleurs", "Elsewhere"),
    "legal": ("SASU ATMAN · SIREN 921 464 210 · Nationalité française, autorisé à travailler dans l'UE",
              "SASU ATMAN · SIREN 921 464 210 · French national, EU work authorised"),
}

UI = {
    "skip": ("Aller au contenu", "Skip to content"),
    "lang_switch": ("Read in English", "Lire en français"),
    "lang_switch_short": ("EN", "FR"),
    "theme": ("Changer de thème", "Toggle theme"),
    "steps_label": ("Étapes de la chaîne QA", "Steps of the QA chain"),
}
