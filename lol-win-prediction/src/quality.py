"""Phase 2 helpers: measure data completeness before deciding what to drop.

The point of this module is to replace "we exclude the LPL" with "we exclude
rows where the 15-minute snapshot was never recorded, and here is the table
that shows which leagues and seasons that hits".
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.config import REQUIRED_AT15, REQUIRED_COMPLETENESS  # noqa: E402


def team_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only the two aggregated team rows per game.

    Oracle's Elixir stores 12 rows per game: 10 players plus 2 team totals.
    Modelling happens at team level; player rows are used separately to build
    roster features.
    """
    return df[df["position"] == "team"].copy()


def completeness_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Share of team rows with a usable 15-minute snapshot, by league and year.

    This is the table that decides the inclusion rule. Read it before writing
    a single filter.
    """
    teams = team_rows(df)
    teams["at15_ok"] = teams[REQUIRED_AT15].notna().all(axis=1)

    pivot = (
        teams.pivot_table(
            index="league",
            columns="year",
            values="at15_ok",
            aggfunc="mean",
        )
        .mul(100)
        .round(1)
    )

    volumes = teams.pivot_table(
        index="league", columns="year", values="gameid", aggfunc="count"
    )

    print("Share of team rows with complete at15 data (%):")
    print(pivot.to_string())
    print()
    print("Row volume by league and year:")
    print(volumes.to_string())

    return pivot


def completeness_flag_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Cross the `datacompleteness` flag against actual at15 availability.

    The flag and the reality do not always agree. Trust the columns, use the
    flag as a secondary signal.
    """
    teams = team_rows(df)
    teams["at15_ok"] = teams[REQUIRED_AT15].notna().all(axis=1)
    table = pd.crosstab(teams["datacompleteness"], teams["at15_ok"])
    print(table.to_string())
    return table


def drop_incomplete_games(
    df: pd.DataFrame,
    excluded_leagues: list[str] | None = None,
    verbose: bool = True,
) -> tuple[pd.DataFrame, dict]:
    """Apply the inclusion rule and return the kept rows plus a cleaning log.

    A game is kept only if BOTH team rows pass. Dropping one side alone would
    break the 50/50 balance of the target, which is the one property that makes
    this dataset pleasant to model.

    Returns
    -------
    kept : DataFrame
    log : dict, ready to be dumped to docs/nettoyage_log.json
    """
    excluded_leagues = excluded_leagues or []
    teams = team_rows(df)
    before = len(teams)

    teams["at15_ok"] = teams[REQUIRED_AT15].notna().all(axis=1)

    # a game is valid only when both of its rows are usable
    valid_per_game = teams.groupby("gameid")["at15_ok"].transform("all")
    pair_complete = teams.groupby("gameid")["gameid"].transform("count").eq(2)

    keep = valid_per_game & pair_complete
    if excluded_leagues:
        keep &= ~teams["league"].isin(excluded_leagues)

    kept = teams[keep].drop(columns=["at15_ok"]).copy()

    dropped_by_league = (
        teams.loc[~keep, "league"].value_counts().head(15).to_dict()
    )

    log = {
        "regle": "conserver une partie si les deux lignes equipe ont un snapshot a 15 minutes complet",
        "colonnes_requises": REQUIRED_AT15,
        "flag_secondaire": REQUIRED_COMPLETENESS,
        "ligues_exclues_manuellement": excluded_leagues,
        "lignes_equipe_avant": int(before),
        "lignes_equipe_apres": int(len(kept)),
        "lignes_supprimees": int(before - len(kept)),
        "taux_suppression_pct": round(100 * (before - len(kept)) / before, 2),
        "principales_ligues_supprimees": dropped_by_league,
        "equilibre_cible_apres": kept["result"].value_counts(normalize=True).round(4).to_dict(),
    }

    if verbose:
        print(f"Team rows: {before:,} -> {len(kept):,} "
              f"({log['taux_suppression_pct']}% dropped)")
        print(f"Target balance after filtering: {log['equilibre_cible_apres']}")
        print("Top leagues affected:")
        for league, count in list(dropped_by_league.items())[:10]:
            print(f"  {league:<12} {count:>7,}")

    return kept, log


def season_schema_diff(frames: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Compare the column sets across seasons.

    Oracle's Elixir adds columns as the game evolves (void grubs in 2024,
    Atakhan in 2025). Concatenating five seasons produces NaN blocks that are
    structural, not accidental. Know about them before the imputer does.
    """
    all_cols: set[str] = set()
    for df in frames.values():
        all_cols |= set(df.columns)

    rows = []
    for col in sorted(all_cols):
        row = {"column": col}
        for year, df in sorted(frames.items()):
            row[year] = col in df.columns
        rows.append(row)

    table = pd.DataFrame(rows).set_index("column")
    inconsistent = table[~table.all(axis=1)]

    print(f"{len(inconsistent)} columns are not present in every season:")
    print(inconsistent.to_string())
    return inconsistent
