"""Empirical audit of firstblood / firstdragon / firstherald leakage.

The claim in docs/difficultes.md R3 is that `firstherald` is necessarily resolved
before minute 15 because the herald despawns at minute 14. That claim is only
true after patch 14.X (season 2024 onwards): in 2022 and 2023 the Rift Herald
spawned at 8:00 and stayed on the map until 19:45, so it could be taken well
after our prediction instant.

If that is right, we should see:
  - a per-season drift in corr(firstherald, result): higher in 2022-2023 (outcome
    bleeds into the flag), lower in 2024-2026.
  - a drift in the share of games where no herald was taken at all.
Possibly also for firstdragon and firstblood, though those are usually settled
earlier.

This script loads the raw team rows, applies the same inclusion rule as phase 3
without rebuilding the full dataset, and runs the audit on the TRAIN seasons
only. We never look at 2026 here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import config, extraction

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 40)


def apply_inclusion_rule(teams: pd.DataFrame) -> pd.DataFrame:
    """Drop invalid games and incomplete at15 pairs, same logic as phase 3."""
    winners = teams.groupby("gameid")["result"].sum()
    invalid = winners[winners != 1].index
    teams = teams[~teams["gameid"].isin(invalid)].copy()

    at15_ok = teams[config.REQUIRED_AT15].notna().all(axis=1)
    paired = teams.groupby("gameid")["gameid"].transform("count").eq(2)
    both_ok = teams.assign(_ok=at15_ok).groupby("gameid")["_ok"].transform("all")
    return teams[paired & both_ok].reset_index(drop=True)


def main() -> None:
    teams, _ = extraction.load_split_frames(verbose=False)
    teams["saison"] = teams["date"].dt.year
    teams = apply_inclusion_rule(teams)

    train = teams[teams["date"] < config.SPLIT_DATE].copy()
    print(f"Train rows (pre-2026): {len(train):,} across {train['saison'].nunique()} seasons")
    print()

    # ------------------------------------------------------------------
    # 1. Per-season correlation of each firstX with result, train only
    # ------------------------------------------------------------------
    print("=" * 70)
    print("1. Correlation with result, per season (TRAIN only, no 2026)")
    print("=" * 70)
    print()
    print("Reference ceiling: golddiffat15 is the strongest honest signal we have")
    print("at minute 15. Anything that scales with it or above suggests the flag")
    print("captures end-of-game information.")
    print()

    cols = ["firstblood", "firstdragon", "firstherald", "golddiffat15"]
    rows = []
    for season, block in train.groupby("saison"):
        row = {"saison": season, "n": len(block)}
        for col in cols:
            row[col] = block[[col, "result"]].dropna().corr().iloc[0, 1]
        rows.append(row)
    rows.append({"saison": "all", "n": len(train),
                 **{c: train[[c, "result"]].dropna().corr().iloc[0, 1] for c in cols}})
    corr_table = pd.DataFrame(rows).set_index("saison")
    print(corr_table.round(3).to_string())
    print()

    # ------------------------------------------------------------------
    # 2. NaN rate per season for each firstX
    # ------------------------------------------------------------------
    print("=" * 70)
    print("2. Share of rows where the flag is NaN, per season")
    print("=" * 70)
    print()
    print("A NaN here means Oracle's Elixir never attributed the objective. For")
    print("herald, if 2024+ shows a jump (either direction), the mechanic changed.")
    print()
    nan_rows = []
    for season, block in train.groupby("saison"):
        row = {"saison": season, "n": len(block)}
        for col in ["firstblood", "firstdragon", "firstherald"]:
            row[f"{col}_nan_%"] = block[col].isna().mean() * 100
        nan_rows.append(row)
    print(pd.DataFrame(nan_rows).set_index("saison").round(2).to_string())
    print()

    # ------------------------------------------------------------------
    # 3. Share where NEITHER team took the herald (both NaN or both 0)
    # ------------------------------------------------------------------
    print("=" * 70)
    print("3. Games where no team is credited with the first herald")
    print("=" * 70)
    print()
    print("Herald taken by at least one team each game vs skipped entirely.")
    print("A big jump at 2024 is the signature of the mechanic reshape.")
    print()
    neither_rows = []
    for season, block in train.groupby("saison"):
        games = block.groupby("gameid").agg(
            fh_sum=("firstherald", "sum"),
            fh_notna=("firstherald", lambda s: s.notna().sum()),
        )
        taken = (games["fh_sum"] >= 1).sum()
        skipped = ((games["fh_sum"] == 0) & (games["fh_notna"] == 2)).sum()
        unknown = (games["fh_notna"] < 2).sum()
        total = len(games)
        neither_rows.append({
            "saison": season,
            "games": total,
            "pct_taken": taken / total,
            "pct_skipped": skipped / total,
            "pct_unknown": unknown / total,
        })
    print(pd.DataFrame(neither_rows).set_index("saison").map(
        lambda x: f"{x:.1%}" if isinstance(x, float) else x).to_string())
    print()

    # ------------------------------------------------------------------
    # 4. Herald resolution timing proxy: when 'heralds' > 0, firstherald must
    #    be set. We can't see the clock, but we can look at the subset of games
    #    where EITHER side has heralds > 0: that proves the herald was taken.
    #    Compare the correlation of firstherald with result on that subset vs
    #    the full set. If firstherald is a clean min-15 signal, the correlation
    #    should be stable; if herald was taken after min 15 in some games, the
    #    unconditional corr pulls in outcome signal from those late games.
    # ------------------------------------------------------------------
    if "heralds" in train.columns:
        print("=" * 70)
        print("4. Subset check: games where the herald was taken (heralds>0)")
        print("=" * 70)
        print()
        print("heralds is a leaky end-of-game total, kept here for diagnostic only.")
        print("Null hypothesis: firstherald corr with result is identical whether")
        print("we restrict to games where the herald was actually taken.")
        print()
        gid_took = train.groupby("gameid")["heralds"].sum()
        taken_ids = gid_took[gid_took > 0].index
        rows_t = []
        for season, block in train.groupby("saison"):
            full = block[["firstherald", "result"]].dropna().corr().iloc[0, 1]
            sub = block[block["gameid"].isin(taken_ids)]
            sub_corr = sub[["firstherald", "result"]].dropna().corr().iloc[0, 1] if len(sub) else np.nan
            rows_t.append({"saison": season, "corr_all": full, "corr_taken": sub_corr,
                           "pct_taken": len(sub) / len(block)})
        print(pd.DataFrame(rows_t).set_index("saison").round(3).to_string())
        print()

    # ------------------------------------------------------------------
    # 5. objectifs_precoces components stacked. If dropping one component
    #    collapses the per-season correlation drift, that component is the
    #    culprit.
    # ------------------------------------------------------------------
    print("=" * 70)
    print("5. objectifs_precoces built with different subsets, train only")
    print("=" * 70)
    print()
    combos = {
        "all 3 (fb+fd+fh)": ["firstblood", "firstdragon", "firstherald"],
        "fb+fd": ["firstblood", "firstdragon"],
        "fb+fh": ["firstblood", "firstherald"],
        "fd+fh": ["firstdragon", "firstherald"],
    }
    rows = []
    for name, cols_c in combos.items():
        row = {"combo": name}
        for season, block in train.groupby("saison"):
            score = block[cols_c].sum(axis=1)
            row[season] = score.corr(block["result"])
        row["all"] = train[cols_c].sum(axis=1).corr(train["result"])
        rows.append(row)
    print(pd.DataFrame(rows).set_index("combo").round(3).to_string())
    print()

    # ------------------------------------------------------------------
    # 6. Model-level check: does removing a firstX hurt generalisation
    #    to 2026? Correlations are suggestive, the test score is decisive.
    #    If dropping firstherald leaves 2026 performance unchanged (or
    #    improves it), the flag is dispensable and we can let it go.
    # ------------------------------------------------------------------
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, roc_auc_score
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.impute import SimpleImputer

    print("=" * 70)
    print("6. Hold-one-out at the model level, logistic regression, 2026 as test")
    print("=" * 70)
    print()
    print("Minimal feature set: at-15 diffs, deaths at 15, and the three firstX.")
    print("Trained on seasons 2022-2025, scored on 2026.")
    print()

    teams_split = teams[teams[config.REQUIRED_AT15].notna().all(axis=1)].copy()
    teams_split["diff_kills_at15"] = (
        teams_split["killsat15"].astype(float) - teams_split["opp_killsat15"].astype(float)
    )

    base_num = ["golddiffat15", "xpdiffat15", "csdiffat15", "diff_kills_at15", "deathsat15"]
    first_cols = ["firstblood", "firstdragon", "firstherald"]
    for c in first_cols:
        teams_split[c] = teams_split[c].astype(float)

    tr = teams_split[teams_split["date"] < config.SPLIT_DATE].copy()
    te = teams_split[teams_split["date"] >= config.SPLIT_DATE].copy()

    def fit_eval(features: list[str], label: str):
        X_tr, y_tr = tr[features], tr["result"].astype(int)
        X_te, y_te = te[features], te["result"].astype(int)
        pipe = Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(C=0.05, max_iter=1000)),
        ])
        pipe.fit(X_tr, y_tr)
        p_tr = pipe.predict_proba(X_tr)[:, 1]
        p_te = pipe.predict_proba(X_te)[:, 1]
        print(f"  {label:<30} "
              f"train acc={accuracy_score(y_tr, p_tr>=0.5):.4f} "
              f"auc={roc_auc_score(y_tr, p_tr):.4f} | "
              f"test  acc={accuracy_score(y_te, p_te>=0.5):.4f} "
              f"auc={roc_auc_score(y_te, p_te):.4f}")

    fit_eval(base_num + first_cols, "all 3 firstX")
    fit_eval(base_num + ["firstdragon", "firstherald"], "without firstblood")
    fit_eval(base_num + ["firstblood", "firstherald"], "without firstdragon")
    fit_eval(base_num + ["firstblood", "firstdragon"], "without firstherald")
    fit_eval(base_num, "no firstX at all")
    print()
    print("Reading: if dropping firstherald closes the 2026 gap AND keeps 2022-2025")
    print("accuracy, the flag was adding leaked signal. If 2026 drops too, the flag")
    print("is a legitimate predictor we should keep.")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
