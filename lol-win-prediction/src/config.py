"""Central configuration for the LoL win-prediction project.

Single source of truth for paths, column allow-lists and the leaky-column
deny-list. Importing this module instead of hardcoding column names in the
notebooks keeps the leakage policy auditable in one place.
"""

from pathlib import Path

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"
MODELS = ROOT / "models"
DOCS = ROOT / "docs"

# --------------------------------------------------------------------------
# Chronological split
# --------------------------------------------------------------------------
# Decided in phase 0: train on the past, test on the most recent season.
# Reproduces the real usage condition and exposes concept drift, unlike a
# random split which silently mixes patches and rosters across the boundary.

SEASONS = [2022, 2023, 2024, 2025, 2026]
TRAIN_SEASONS = [2022, 2023, 2024, 2025]
TEST_SEASONS = [2026]

# The split is cut on the DATE, never on `year`. Phase 2 established that `year`
# is a season label, not a calendar year: 2712 rows are played between September
# and December and carry the following season's label, and 10 rows are labelled
# 2027. Splitting on the label would send December 2025 games into the test set
# while later games stayed in training, breaking the very chronological ordering
# the split exists to guarantee.
SPLIT_DATE = "2026-01-01"

RANDOM_STATE = 42
TARGET = "result"

# --------------------------------------------------------------------------
# Prediction instant
# --------------------------------------------------------------------------
# Everything in this project assumes the model is called at minute 15.
# Any column whose value is unknown or not final at that instant is a leak.

PREDICTION_MINUTE = 15

# --------------------------------------------------------------------------
# Row-level inclusion rule (replaces a hardcoded league exclusion)
# --------------------------------------------------------------------------
# A game enters the dataset only if the 15-minute snapshot was actually
# recorded. Measurable criterion, not a judgement on a league name.
# Both rows of a game must pass, otherwise both are dropped, so the 50/50
# target balance survives. See src/quality.py::drop_incomplete_games.

REQUIRED_AT15 = ["goldat15", "xpat15", "csat15", "golddiffat15", "xpdiffat15"]
REQUIRED_COMPLETENESS = "complete"

# Fill this only if the phase 2 audit proves a league is unusable for a reason
# other than missing at15 data. Keep it empty by default.
EXCLUDED_LEAGUES: list[str] = []

# --------------------------------------------------------------------------
# Leaky columns: post-game or post-minute-15 information
# --------------------------------------------------------------------------

LEAKY_COLUMNS = [
    # end-of-game totals
    "kills", "deaths", "assists", "teamkills", "teamdeaths",
    "doublekills", "triplekills", "quadrakills", "pentakills",
    "totalgold", "earnedgold", "earned gpm", "earnedgoldshare", "goldspent",
    "gspd", "gpr",
    "total cs", "minionkills", "monsterkills", "monsterkillsownjungle",
    "monsterkillsenemyjungle", "cspm",
    "damagetochampions", "dpm", "damageshare", "damagetakenperminute",
    "damagemitigatedperminute",
    "wardsplaced", "wpm", "wardskilled", "wcpm", "controlwardsbought",
    "visionscore", "vspm",
    # objectives resolved after minute 15
    "firstbaron", "barons", "opp_barons",
    "elders", "opp_elders",
    "firstmidtower", "firsttothreetowers",
    "inhibitors", "opp_inhibitors",
    "towers", "opp_towers",
    "dragons", "opp_dragons", "dragons (type unknown)",
    "infernals", "mountains", "clouds", "oceans", "chemtechs", "hextechs",
    "heralds", "opp_heralds", "void_grubs", "opp_void_grubs",
    "atakhans", "opp_atakhans",
    # Found in phase 3: these survived the original deny-list and are end-of-game
    # aggregates. Their absolute correlation with `result` is higher than that of
    # golddiffat15 (0.535), which is the strongest legitimate signal available at
    # minute 15. Anything above that line is answering the question, not
    # predicting it.
    "damagetotowers",        # 0.760
    "team kpm",              # 0.679
    "elementaldrakes",       # 0.586
    "opp_elementaldrakes",   # 0.586
    "ckpm",                  # 0.000, symmetric between both rows, but still a
                             # whole-game rate: unknown at minute 15
    # `firsttower` is a whole-game flag, not a minute-15 state. It is attributed
    # in 100 % of games, while firstblood, firstdragon and firstherald leave a
    # few hundred games unattributed. A first tower routinely falls after minute
    # 15 in professional play, so the flag imports future information, which its
    # correlation confirms: 0.391 against 0.18 to 0.25 for the other three.
    "firsttower",
    # duration is unknown at minute 15 and strongly correlated with the outcome
    "gamelength",
    # snapshots taken after the prediction instant
    "goldat20", "xpat20", "csat20", "opp_goldat20", "opp_xpat20", "opp_csat20",
    "golddiffat20", "xpdiffat20", "csdiffat20",
    "killsat20", "assistsat20", "deathsat20",
    "opp_killsat20", "opp_assistsat20", "opp_deathsat20",
    "goldat25", "xpat25", "csat25", "opp_goldat25", "opp_xpat25", "opp_csat25",
    "golddiffat25", "xpdiffat25", "csdiffat25",
    "killsat25", "assistsat25", "deathsat25",
    "opp_killsat25", "opp_assistsat25", "opp_deathsat25",
]

# Columns that only exist in recent seasons (void grubs from 2024, Atakhan
# from 2025). Already banned above as leaks, but the note matters when
# concatenating five seasons: pd.concat fills the gap with NaN, and an unaware
# imputer would invent values for 2022.
SEASON_DEPENDENT_COLUMNS = ["void_grubs", "opp_void_grubs", "atakhans", "opp_atakhans"]

# --------------------------------------------------------------------------
# Columns kept as raw features (known at minute 15)
# --------------------------------------------------------------------------

GAMESTATE_AT_15 = [
    "goldat15", "xpat15", "csat15",
    "opp_goldat15", "opp_xpat15", "opp_csat15",
    "golddiffat15", "xpdiffat15", "csdiffat15",
    "killsat15", "assistsat15", "deathsat15",
    "opp_killsat15", "opp_assistsat15", "opp_deathsat15",
    # `firsttower` deliberately absent: see the leak note above.
    "firstblood", "firstdragon", "firstherald",
    # Known at minute 15, but the scale changes in 2026 (max 15 up to 2025, 45
    # afterwards). Kept in the dataset for analysis, excluded from the features.
    "turretplates", "opp_turretplates",
    # Snapshot taken before the prediction instant, so legitimate.
    "goldat10", "xpat10", "csat10",
    "opp_goldat10", "opp_xpat10", "opp_csat10",
    "golddiffat10", "xpdiffat10", "csdiffat10",
    "killsat10", "assistsat10", "deathsat10",
    "opp_killsat10", "opp_assistsat10", "opp_deathsat10",
]

CONTEXT_COLUMNS = [
    "gameid", "datacompleteness", "league", "year", "split", "playoffs",
    "date", "game", "patch", "side", "teamname", "teamid", "position",
    "ban1", "ban2", "ban3", "ban4", "ban5",
]

PICK_COLUMNS = ["pick_top", "pick_jng", "pick_mid", "pick_bot", "pick_sup"]

# --------------------------------------------------------------------------
# Feature groups for the ColumnTransformer
# --------------------------------------------------------------------------
# Time-bound categoricals are deliberately excluded. With a chronological
# split, `year` and `patch_major` take values in the test set that never
# appear in training: OneHotEncoder(handle_unknown="ignore") encodes every
# 2026 row as an all-zero block, which is dead weight at best.
# `league` is excluded for the same reason: the circuit was reorganised in
# 2025 (LCS became LTA, PCS and LJL merged into LCP), so the codes do not
# survive the train/test boundary. Region and tier, read from the reference
# table, do survive it.
#
# `league` stays in the dataframe for phase 5 analysis. It is simply not fed
# to the model. See ANALYSIS_ONLY below.

CATEGORICAL_FEATURES = [
    "side",
    "region",
    "tier_ligue",
    # `split` removed in phase 3. It fails the same test as `league`: 32 values,
    # 19.8 % missing, and 3 values appear only in 2026. OneHotEncoder with
    # handle_unknown="ignore" would encode those rows as an all-zero block, so
    # the information would be lost silently. `playoffs` carries the useful part
    # of the signal as a stable boolean.
]

NUMERIC_FEATURES = [
    "golddiffat15", "xpdiffat15", "csdiffat15",
    "diff_kills_at15", "deathsat15",
    # `turretplates` removed in phase 3: its scale changes exactly on the
    # train/test boundary (max 15 up to 2025, 45 in 2026, above 15 on 61 % of
    # rows). A scaler fitted on 2022-2025 would map 2026 far outside the learned
    # range and degrade the test season without raising anything.
    "objectifs_precoces",
    "compo_nb_tank", "compo_nb_mage", "compo_nb_marksman", "compo_nb_fighter",
    "profil_degats",
    "forme_equipe_10_derniers", "experience_roster", "winrate_champion_patch",
    "ecart_or_normalise",
    "patch_seq",
]

# `firsttower` removed in phase 3, see the leak note in LEAKY_COLUMNS. The
# engineered feature `objectifs_precoces` is therefore built on three components
# instead of the four announced in CLAUDE.md, and scores 0 to 3.
BOOLEAN_FEATURES = ["playoffs", "firstblood", "firstdragon", "firstherald"]

# Objectives resolved before minute 15, used to build `objectifs_precoces`.
EARLY_OBJECTIVES = ["firstblood", "firstdragon", "firstherald"]

# Kept for analysis and traceability, never passed to the model.
ANALYSIS_ONLY = ["gameid", "date", "year", "league", "teamname", "teamid", "patch"]

# --------------------------------------------------------------------------
# Plot palette (charcoal / slate)
# --------------------------------------------------------------------------

PALETTE = {
    "primary": "#2F3640",     # charcoal
    "secondary": "#5A6572",   # slate
    "accent": "#8D99AE",      # light slate
    "highlight": "#B54B3A",   # muted brick, sparingly
    "grid": "#D8DCE1",
    "background": "#FFFFFF",
}

PALETTE_SEQUENCE = [
    PALETTE["primary"],
    PALETTE["secondary"],
    PALETTE["accent"],
    PALETTE["highlight"],
]
