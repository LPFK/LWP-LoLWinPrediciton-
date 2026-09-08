# CLAUDE.md

Project brief for Claude Code. Read this before touching any file.

## Context

Graded academic ML project (Master 1, "Projet Final Machine Learning", Blocs 6 and 8).
Scored out of 100 points. The grading rubric drives every decision for us here.

**All user-facing content (notebooks markdown cells, reports in `docs/`, figure labels,
presentation) must be REVIEWED ONLY NEVER ANY CODE WRITTING.** that stends for Code, comments, variable names, commit
messages

## Goal

Binary classification: predict which professional League of Legends team wins a game,
using only information available **at the 15-minute mark**.

- Target: `result` (0/1), team-level rows from Oracle's Elixir
- Primary metric: ROC AUC. Secondary: accuracy (communication) and log loss (calibration)
- Split: chronological. Train on seasons 2022-2025, test on 2026. Also compute a random split, for comparison only.

## Three rules that cap the grade. Never violate them.

1. **Data leakage caps the modelling phase at 8/25.**
   - No preprocessing before the train/test split. Every imputer, scaler and encoder
     lives inside a `sklearn` `Pipeline` / `ColumnTransformer`.
   - No post-game columns as features. See the banned list in `src/config.py`.
   - Historical features (team form, champion winrate) must be computed with an
     expanding window over **past games only**, sorted by date. Never a global mean.
2. **A notebook that does not run end to end caps the final grade at 50/100.**
   - After any user edit, restart-and-run-all must succeed from a clean kernel.
   - No hidden state, no cell that depends on a previously user deleted variable.
3. **No baseline computed caps the modelling phase at 15/25.**
   - Three baselines are mandatory before any model: majority class, "blue side always
     wins", and "highest gold at 15 wins". They go in the notebook, not in a comment, always check these mistakes.

## Data sources

| Source | Format | Location | Notes |
|---|---|---|---|
| Oracle's Elixir 2022-2026 | CSV | `data/raw/*_LoL_esports_match_data_from_OraclesElixir.csv` | ~115k rows/season, ~165 cols, 12 rows per game |
| Riot Data Dragon champions | JSON | `data/raw/champions.json` | champion tags, no API key needed |
| League reference table | XLSX | `data/raw/referentiel_ligues.xlsx` | hand-built, league tier and region |

Oracle's Elixir structure: 12 rows per game. Rows 1-10 are players
(`position` in top/jng/mid/bot/sup), rows 11-12 are team aggregates (`position == "team"`).
**Work on team rows.** Player rows are used only to build aggregated features.

Attribution is required: data provided by Oracle's Elixir (Tim Sevenhuysen,
oracleselixir.com). Cite it in the notebook and the presentation.

## Repo layout

```
data/raw/         downloaded sources, never modified, never committed
data/interim/     after cleaning
data/processed/   final modelling dataset (parquet)
notebooks/        one notebook per project phase, all must run end to end
src/              importable helpers used by the notebooks
docs/             graded u-written deliverables
figures/          exported PNG, minimum 7
models/           joblib pipelines
reference/        the course material. Read-only, never edit.
```

## reference/ is the ground truth

`reference/` holds the course guide, phase by phase, plus `Grille_Evaluation.md`
(the marking scheme) and `Ressource_Workflow_ML_Complet.ipynb`.

Read the matching `reference/0X_*.md` before starting a review phase. If anything in this
file contradicts the guide, **the guide wins** and you flag the contradiction and report it.

`Ressource_Workflow_ML_Complet.ipynb` is the phase 7 skeleton supplied by the
trainer: split, `ColumnTransformer`, `Pipeline`, `GridSearchCV`, evaluation, joblib
export. Only three zones are meant to be adapted, marked `# <-- A ADAPTER`.
User builds `07_modelisation.ipynb` by adapting that skeleton, not by rewriting it from
scratch review and give needed changes. What is graded is the ability to adapt it and explain it.

Two deliberate departures from the skeleton, both decided in phase 0 and both to be
justified in a markdown cell:
- chronological split instead of `train_test_split`
- `TimeSeriesSplit` instead of the default `KFold` inside `GridSearchCV`

## Phase mapping

| Notebook | Phase | Deliverable |
|---|---|---|
| `01_extraction.ipynb` | 1 | 3 sources loaded, dtypes and encoding handled, source summary table |
| `02_eda_diagnostique.ipynb` | 2 | `docs/rapport_diagnostic.md`, 5 quality dimensions |
| `03_nettoyage.ipynb` | 3 | `data/interim/`, `docs/rapport_nettoyage.md`, JSON cleaning log |
| `04_transformation.ipynb` | 4 | `data/processed/`, `docs/data_dictionary.md`, 7+ engineered features |
| `05_eda_analytique.ipynb` | 5 | answers to the 5 business questions in `docs/00_cadrage.md` |
| `06_visualisation.ipynb` | 6 | 7+ figures in `figures/` |
| `07_modelisation.ipynb` | 7 | baselines, 3+ models, `models/pipeline_final.joblib` |

## Cleaning rules specific to this dataset

- **Inclusion rule.** A game is kept only if BOTH team rows have a complete
  15-minute snapshot (`config.REQUIRED_AT15` all non-null). If one row fails,
  drop both: dropping one side alone breaks the 50/50 target balance.
  Implemented in `src/quality.py::drop_incomplete_games`.
- **Do not hardcode a league exclusion.** `config.EXCLUDED_LEAGUES` stays empty
  unless the phase 2 audit proves a league is unusable for a reason other than
  missing at15 data. Run `quality.completeness_matrix` first and put the table
  in `docs/rapport_diagnostic.md`. Filtering on a measured criterion is
  defensible in the oral defence; filtering on a league name is not.
- **Five seasons means five schemas.** Columns appear over time (void grubs in
  2024, Atakhan in 2025). Run `quality.season_schema_diff` before concatenating
  and treat the resulting NaN blocks as structural, not accidental.
- Check for duplicated `gameid` + `teamid` pairs, and for games that do not have
  exactly 2 team rows.
- `patch` is a string like "14.19". Split into major/minor ints, do not treat as
  float (14.9 vs 14.19 sorts wrong). Then build `patch_seq`, the rank of the
  patch within its season, which is the only patch representation that
  generalises to the 2026 test set.
- Dates: parse with an explicit format, check consistency across five seasons.

## Engineered features to build (7+ required, i aim for 10)

1. `objectifs_precoces` = firstblood + firstdragon + firstherald + firsttower (0-4 score)
2. `diff_kills_at15` = killsat15 - opp_killsat15
3. `compo_nb_tank`, `compo_nb_mage`, `compo_nb_marksman`, `compo_nb_fighter` from
   Data Dragon tags over the team's 5 picks
4. `profil_degats` = ratio of AD-tagged to AP-tagged champions in the composition
5. `forme_equipe_10_derniers` = team winrate over its previous 10 games (expanding, past only)
6. `experience_roster` = number of games the current 5-player lineup has played together
7. `winrate_champion_patch` = each picked champion's winrate on prior games of the same patch
8. `tier_ligue`, `region` from the Excel reference table
9. `is_playoffs` boolean
10. `ecart_or_normalise` = golddiffat15 divided by the median gold at 15 for that patch
11. `patch_seq` = rank of the patch within its season

Every one of these must be traceable in `docs/data_dictionary.md`.

## Modelling

Compare at least three models including one simple and interpretable:

1. `LogisticRegression` — the simple baseline model, and the best calibrated
2. `RandomForestClassifier`
3. `HistGradientBoostingClassifier` (prefer it over XGBoost: it is in scikit-learn,
   handles NaN natively, no extra dependency)

Use `GridSearchCV` with `scoring="roc_auc"` and **`TimeSeriesSplit`** on the training set
sorted by date. A plain `KFold` shuffles the chronological order inside the training set,
which reproduces at small scale the exact problem the chronological split just fixed.
Look at the test set (2026) **once**, at the very end. Do not iterate against it.

Never feed a time-bound categorical to the model: `year`, `patch_major` and `league` take
values in 2026 that never appear in training. Use `region`, `tier_ligue` and `patch_seq`
instead. The allow-lists in `src/config.py` already enforce this.

Report per model: accuracy, ROC AUC, log loss, confusion matrix, and the gap between
train and test scores expressed **in number of rows**, not only in percentage points.

Expected ceiling: roughly 72 to 78 % accuracy. If a model reaches 90 %+, there is a leak.
Stop and find it.

Export the **full pipeline** (preprocessing + model) with joblib, never the bare estimator.


## Working agreement

- Explain each review. Any code that needs changes explain why and why it makes it better.
- Prefer short, readable cells over clever one-liners.
- When a choice is arbitrary, say so and offer the alternative rather than picking silently.
- now Log every prompt used into `docs/journal_ia.md`. It is worth 5 points. 
