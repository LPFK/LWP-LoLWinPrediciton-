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
# We settled this in phase 0: train on the past, test on the latest season. That's how
# the model would really be used, and it shows concept drift. A random split would
# quietly mix patches and rosters on both sides.

SEASONS = [2022, 2023, 2024, 2025, 2026]
TRAIN_SEASONS = [2022, 2023, 2024, 2025]
TEST_SEASONS = [2026]

# Careful: we split on the DATE, not on `year`. Phase 2 showed `year` is a season label,
# not a calendar year. 2712 rows are played between September and December but carry
# next season's label, and 10 rows are even labelled 2027. Splitting on the label would
# push December 2025 games into test while later games stayed in train, which defeats
# the whole point of a chronological split.
SPLIT_DATE = "2026-01-01"

RANDOM_STATE = 42
TARGET = "result"

# --------------------------------------------------------------------------
# Prediction instant
# --------------------------------------------------------------------------
# The whole project assumes we call the model at minute 15. If a column isn't known (or
# isn't final yet) at that point, it's a leak.

PREDICTION_MINUTE = 15

# --------------------------------------------------------------------------
# Row-level inclusion rule (replaces a hardcoded league exclusion)
# --------------------------------------------------------------------------
# A game only gets in if its 15-minute snapshot was actually recorded. That's something
# we can measure, not a judgement call on a league's name. Both rows of a game have to
# pass or we drop both, so the target stays 50/50. See
# src/quality.py::drop_incomplete_games.

REQUIRED_AT15 = ["goldat15", "xpat15", "csat15", "golddiffat15", "xpdiffat15"]
REQUIRED_COMPLETENESS = "complete"

# Only fill this in if the phase 2 audit shows a league is unusable for some reason
# other than missing at15 data. Empty by default.
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
    # Caught these in phase 3: they slipped past the original deny-list, but they're
    # end-of-game aggregates. They correlate with `result` more strongly than
    # golddiffat15 (0.535), which is the best honest signal we have at minute 15.
    # Anything above that line is basically reading the answer, not predicting it.
    "damagetotowers",        # 0.760
    "team kpm",              # 0.679
    "elementaldrakes",       # 0.586
    "opp_elementaldrakes",   # 0.586
    "ckpm",                  # 0.000, symmetric between both rows, but still a
                             # whole-game rate: unknown at minute 15
    # `firsttower` is a whole-game flag, not a minute-15 state. It's set in 100 % of
    # games, whereas firstblood, firstdragon and firstherald leave a few hundred games
    # unattributed. In pro play the first tower often falls after minute 15, so the flag
    # leaks future info, and the correlation backs that up: 0.391 vs 0.18 to 0.25 for
    # the other three.
    "firsttower",
    # we don't know the duration at minute 15, and it's strongly tied to the outcome
    "gamelength",
    # snapshots taken after minute 15
    "goldat20", "xpat20", "csat20", "opp_goldat20", "opp_xpat20", "opp_csat20",
    "golddiffat20", "xpdiffat20", "csdiffat20",
    "killsat20", "assistsat20", "deathsat20",
    "opp_killsat20", "opp_assistsat20", "opp_deathsat20",
    "goldat25", "xpat25", "csat25", "opp_goldat25", "opp_xpat25", "opp_csat25",
    "golddiffat25", "xpdiffat25", "csdiffat25",
    "killsat25", "assistsat25", "deathsat25",
    "opp_killsat25", "opp_assistsat25", "opp_deathsat25",
]

# Columns that only exist in recent seasons (void grubs since 2024, Atakhan since 2025).
# They're already banned above as leaks, but it's worth flagging when we stack five
# seasons: pd.concat fills the gap with NaN, and a careless imputer would happily make
# up values for 2022.
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
    # `firsttower` left out on purpose, see the leak note above.
    "firstblood", "firstdragon", "firstherald",
    # Known at minute 15, but the scale changes in 2026 (capped at 15 up to 2025, 45
    # after). We keep it around for analysis but don't use it as a feature.
    "turretplates", "opp_turretplates",
    # Snapshot taken before minute 15, so this one is fine.
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
# Time-bound categoricals are left out on purpose. With a chronological split, `year`
# and `patch_major` take values in test that never show up in train, so
# OneHotEncoder(handle_unknown="ignore") turns every 2026 row into an all-zero block.
# Dead weight at best. `league` is out for the same reason: the circuit got reshuffled
# in 2025 (LCS became LTA, PCS and LJL merged into LCP), so the codes don't survive the
# train/test boundary. Region and tier, read from the reference table, do.
#
# `league` is still in the dataframe for the phase 5 analysis, we just don't feed it to
# the model. See ANALYSIS_ONLY below.

CATEGORICAL_FEATURES = [
    "side",
    "region",
    "tier_ligue",
    # Dropped `split` in phase 3. Same problem as `league`: 32 values, 19.8 % missing,
    # and 3 values that only show up in 2026. OneHotEncoder with handle_unknown="ignore"
    # would turn those rows into zeros and we'd lose the info without noticing.
    # `playoffs` keeps the useful part as a stable boolean.
]

NUMERIC_FEATURES = [
    "golddiffat15", "xpdiffat15", "csdiffat15",
    "diff_kills_at15", "deathsat15",
    # Dropped `turretplates` in phase 3: its scale changes right on the train/test
    # boundary (max 15 up to 2025, 45 in 2026, above 15 on 61 % of rows). A scaler
    # fitted on 2022-2025 would throw 2026 way outside the learned range and quietly
    # hurt the test season.
    "objectifs_precoces",
    "compo_nb_tank", "compo_nb_mage", "compo_nb_marksman", "compo_nb_fighter",
    "profil_degats",
    "forme_equipe_10_derniers", "experience_roster", "winrate_champion_patch",
    "ecart_or_normalise",
    "patch_seq",
]

# `firsttower` was dropped in phase 3 (see the leak note in LEAKY_COLUMNS). So
# `objectifs_precoces` is built from three components instead of the four CLAUDE.md
# mentions, and goes from 0 to 3.
BOOLEAN_FEATURES = ["playoffs", "firstblood", "firstdragon", "firstherald"]

# Objectives settled before minute 15, used to build `objectifs_precoces`.
EARLY_OBJECTIVES = ["firstblood", "firstdragon", "firstherald"]

# Kept for analysis and traceability, but never fed to the model.
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
