# Prédiction de victoire à la minute 15, League of Legends professionnel

Projet final du cours de Machine Learning, Blocs 6 et 8.

Classification binaire : prédire quelle équipe remporte une partie professionnelle de League of Legends, en n'utilisant que l'information disponible à la 15e minute.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Récupération des données

```bash
python src/extraction.py
```

Le script télécharge les trois sources dans `data/raw/` :

1. **Oracle's Elixir**, CSV, une saison par fichier. Redistribué via un dossier Google Drive mis à jour quotidiennement. Le script télécharge les saisons une par une, par identifiant de fichier (`OE_FILE_IDS`), et non le dossier entier qui contient aussi les saisons 2014 à 2021.

   Google Drive applique un quota journalier de téléchargement par fichier. Au-delà, il renvoie une page d'erreur au lieu du CSV, et aucun outil en ligne de commande ne passe outre. Dans ce cas, ouvrir oracleselixir.com/tools/downloads dans un navigateur connecté à un compte Google, télécharger les fichiers à la main et les déposer dans `data/raw/` sous leur nom d'origine. Si les identifiants changent, les récupérer depuis `OE_DRIVE_FOLDER` et mettre à jour `OE_FILE_IDS` dans `src/extraction.py`.
2. **Riot Data Dragon**, JSON, métadonnées des champions. Gratuit, sans clé API.
3. **Référentiel des ligues**, XLSX, construit à la main par le script. À compléter après avoir listé les valeurs réelles de la colonne `league` : le circuit a été réorganisé en 2025.

Attribution obligatoire : données fournies par Oracle's Elixir (Tim Sevenhuysen, oracleselixir.com). À citer dans le notebook et dans la présentation.

## Structure

```
data/raw/         sources téléchargées, jamais modifiées, jamais versionnées
data/interim/     après nettoyage
data/processed/   dataset final de modélisation (parquet)
notebooks/        un notebook par phase, tous exécutables de bout en bout
src/              fonctions réutilisables importées par les notebooks
docs/             livrables écrits notés
figures/          exports PNG, 7 minimum
models/           pipelines joblib
CLAUDE.md         brief projet pour Claude Code
```

## Avancement par phase

| Phase | Notebook | Livrable | Points | Statut |
|---|---|---|---|---|
| 0 Cadrage | — | `docs/00_cadrage.md` | 6 | FAIT |
| 1 Extraction | `01_extraction.ipynb` | 3 sources chargées | 4 | Fait, exécuté de bout en bout sur 104 544 lignes équipe |
| 2 Diagnostic | `02_eda_diagnostique.ipynb` | `docs/rapport_diagnostic.md` | 8 | Fait, 5 dimensions notées, score global 3,4 / 5 |
| 3 Nettoyage | `03_nettoyage.ipynb` | `docs/rapport_nettoyage.md` | 12 | Fait, 92 616 lignes et 66 colonnes en sortie |
| 4 Transformation | `04_transformation.ipynb` | `docs/data_dictionary.md` | 8 | Fait, 23 features construites, 49 colonnes |
| 5 EDA analytique | `05_eda_analytique.ipynb` | Réponses aux 5 questions business | 12 | Fait, 5 questions traitées sur 2022-2025 uniquement, `docs/rapport_analytique.md`, 5 figures |
| 6 Visualisation | `06_visualisation.ipynb` | 7+ figures | 8 | Fait, 9 figures et un tableau de bord, 15 dans `figures/`, `docs/visualisations.md` |
| 7 Modélisation | `07_modelisation.ipynb` | `models/pipeline_final.joblib` | 25 | À faire |
| 8 Documentation | — | Reproductibilité | 5 | Continu |
| 9 Soutenance | — | Support de présentation | 7 | À faire |
| IA | — | `docs/journal_ia.md` | 5 | Continu |

## Les trois règles éliminatoires

1. Fuite de données non détectée : Phase 7 plafonnée à 8/25
2. Notebook non exécutable de bout en bout : note finale plafonnée à 50/100
3. Aucune baseline calculée : Phase 7 plafonnée à 15/25

La politique anti-fuite est centralisée dans `src/config.py` (`LEAKY_COLUMNS`). Ne jamais réintroduire une de ces colonnes comme feature.
