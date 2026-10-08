# Prédiction de victoire à la minute 15, League of Legends professionnel

Projet final du cours de Machine Learning, Blocs 6 et 8.

Classification binaire : prédire quelle équipe remporte une partie professionnelle de League of Legends, en n'utilisant que l'information disponible à la 15e minute.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements-lock.txt
```

`requirements.txt` donne les contraintes minimales, `requirements-lock.txt` les versions exactes
de l'environnement qui a produit les résultats. Pour rejouer le projet à l'identique, installer
le second. Le détail est dans `docs/reproductibilite.md`.

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
data/exports/     exports de partage, parquet + csv + xlsx
notebooks/        un notebook par phase, tous exécutables de bout en bout
src/              fonctions réutilisables importées par les notebooks
docs/             livrables écrits notés
figures/          exports PNG, 7 minimum
models/           pipelines joblib
CLAUDE.md         brief projet pour Claude Code
```

Les six modules de `src/` :

| Module | Rôle |
|---|---|
| `config.py` | Chemins, allow-lists de features, deny-list anti-fuite, palette. Source unique de vérité |
| `extraction.py` | Téléchargement et lecture des trois sources, typage explicite |
| `quality.py` | Diagnostics de qualité, règle d'inclusion des parties |
| `features.py` | Construction des variables dérivées, dont les fenêtres passées seules |
| `analyse.py` | Statistiques descriptives avec intervalles de confiance |
| `viz.py` | Identité visuelle commune, formats numériques français |

## Avancement par phase

| Phase | Notebook | Livrable | Points | Statut |
|---|---|---|---|---|
| 0 Cadrage | — | `docs/00_cadrage.md` | 6 | FAIT |
| 1 Extraction | `01_extraction.ipynb` | 3 sources chargées | 4 | Fait, exécuté de bout en bout sur 106 796 lignes équipe |
| 2 Diagnostic | `02_eda_diagnostique.ipynb` | `docs/rapport_diagnostic.md` | 8 | Fait, 5 dimensions notées, score global 3,4 / 5 |
| 3 Nettoyage | `03_nettoyage.ipynb` | `docs/rapport_nettoyage.md` | 12 | Fait, 94 840 lignes et 66 colonnes en sortie |
| 4 Transformation | `04_transformation.ipynb` | `docs/data_dictionary.md` | 8 | Fait, 23 features construites, 49 colonnes |
| 5 EDA analytique | `05_eda_analytique.ipynb` | Réponses aux 5 questions business | 12 | Fait, 5 questions traitées sur 2022-2025 uniquement, `docs/rapport_analytique.md`, 5 figures |
| 6 Visualisation | `06_visualisation.ipynb` | 7+ figures | 8 | Fait, 9 figures et un tableau de bord, 19 dans `figures/`, `docs/visualisations.md` |
| 7 Modélisation | `07_modelisation.ipynb` | `models/pipeline_final.joblib` | 25 | Fait, 3 baselines et 3 familles comparées, régression logistique retenue, 75,8 % d'accuracy et 0,845 d'AUC sur 2026 |
| 8 Documentation | `08_export_documentation.ipynb` | Reproductibilité | 5 | Fait, exports en 3 formats, `docs/reproductibilite.md`, `CHANGELOG.md`, `requirements-lock.txt` |
| 9 Soutenance | `09_soutenance.ipynb` | Support de présentation | 7 | Fait, `docs/soutenance.md` et `docs/soutenance_deck.html`, checklist des 14 livrables vérifiée par le code |
| IA | — | `docs/journal_ia.md` | 5 | Continu |

## Résultats

| Indicateur | Valeur |
|---|---|
| Modèle retenu | Régression logistique, `C = 0,05` |
| Accuracy sur 2026 | 75,8 % |
| ROC AUC | 0,845 |
| Log loss | 0,486 |
| Meilleure baseline | 74,6 %, « le plus riche à 15 gagne » |
| Gain sur la baseline | +1,2 point, soit 231 lignes sur 18 782 |

Le résultat d'analyse principal : à avantage économique égal, le **premier dragon** vaut environ
**1 030 or**, alors que le **premier sang** et le **premier héraut** ne valent rien de plus que
l'or qu'ils rapportent déjà. Le classement brut des objectifs précoces est donc presque
exactement inversé.

## Documentation

| Document | Contenu |
|---|---|
| `docs/00_cadrage.md` | Cadrage initial, écrit avant tout code |
| `docs/data_dictionary.md` | Les 49 colonnes, unités, valeurs possibles, transformations, limitations |
| `docs/rapport_diagnostic.md` | Audit qualité sur 5 dimensions |
| `docs/rapport_nettoyage.md` | Fuites retirées, règle d'inclusion |
| `docs/rapport_analytique.md` | Réponses aux 5 questions business |
| `docs/visualisations.md` | Fiche par figure, règles de design appliquées |
| `docs/rapport_modelisation.md` | Baselines, comparaison, verdict, biais |
| `docs/reproductibilite.md` | Comment tout rejouer, empreinte de contrôle |
| `docs/soutenance.md` | Executive summary, 12 diapositives, recommandations, limites, questions du jury |
| `docs/soutenance_deck.html` | Le support de présentation. Imprimer pour obtenir un PDF |
| `docs/guide_explication.md` | Comment expliquer le code et l'architecture à l'oral |
| `docs/journal_ia.md` | Journal d'utilisation de l'IA |
| `docs/difficultes.md` | Journal des difficultés rencontrées |

## Les trois règles éliminatoires

1. Fuite de données non détectée : Phase 7 plafonnée à 8/25
2. Notebook non exécutable de bout en bout : note finale plafonnée à 50/100
3. Aucune baseline calculée : Phase 7 plafonnée à 15/25

La politique anti-fuite est centralisée dans `src/config.py` (`LEAKY_COLUMNS`). Ne jamais réintroduire une de ces colonnes comme feature.
