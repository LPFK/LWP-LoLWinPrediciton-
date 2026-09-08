"""Phase 1: download and load the three data sources.

Run once from the repo root:

    python src/extraction.py

The Oracle's Elixir download link is redistributed through a Google Drive folder
that the maintainer refreshes daily. If the folder id below stops working, get the
current one from https://oracleselixir.com/tools/downloads and update OE_DRIVE_FOLDER.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.config import DATA_RAW, SEASONS  # noqa: E402

OE_DRIVE_FOLDER = "https://drive.google.com/drive/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH"
DDRAGON_VERSIONS = "https://ddragon.leagueoflegends.com/api/versions.json"
DDRAGON_CHAMPIONS = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/champion.json"

# Per-season Drive file ids, read from the public folder listing. Downloading by
# id fetches only the five seasons we model instead of the whole 2014-2026
# folder. Refresh them from OE_DRIVE_FOLDER if the maintainer re-uploads.
OE_FILE_IDS = {
    2022: "1EHmptHyzY8owv0BAcNKtkQpMwfkURwRy",
    2023: "1XXk2LO0CsNADBB1LRGOV5rUpyZdEZ8s2",
    2024: "1IjIEhLc9n8eLKeY-yh_YigKVWbhgGBsN",
    2025: "1v6LRphp2kYciU4SXp0PCjEMuev1bDejc",
    2026: "1hnpbrUpBMS1TZI7IovfpKeZfWJH1Aptm",
}

OE_FILENAME = "{season}_LoL_esports_match_data_from_OraclesElixir.csv"

MANUAL_DOWNLOAD_HINT = (
    "Google Drive refuses anonymous downloads once a file reaches its daily quota.\n"
    "Workaround: open https://oracleselixir.com/tools/downloads in a browser while\n"
    "signed in to a Google account, download the season CSV files by hand and drop\n"
    "them into data/raw/ under their original names, for example\n"
    "  2025_LoL_esports_match_data_from_OraclesElixir.csv"
)


# --------------------------------------------------------------------------
# Source 1: Oracle's Elixir (CSV)
# --------------------------------------------------------------------------

def missing_seasons(seasons: list[int] | None = None) -> list[int]:
    """Return the seasons whose CSV is absent from data/raw.

    Used by the notebooks to decide whether a download is needed, without
    triggering one as a side effect of importing anything.
    """
    seasons = seasons or SEASONS
    return [s for s in seasons if not (DATA_RAW / OE_FILENAME.format(season=s)).exists()]


def download_oracles_elixir(seasons: list[int] | None = None) -> list[int]:
    """Download the season CSV files by file id, one per season.

    Only the seasons in `seasons` are fetched, unlike a full folder download
    which also pulls 2014-2021. Returns the seasons that could not be
    downloaded, so the caller can fall back to a manual download instead of
    dying on the first quota error.
    """
    try:
        import gdown
    except ImportError:
        raise SystemExit("gdown is required: pip install gdown")

    seasons = seasons or SEASONS
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    failed = []

    for season in seasons:
        out = DATA_RAW / OE_FILENAME.format(season=season)
        if out.exists():
            print(f"  season {season}: already in data/raw, skipped")
            continue

        file_id = OE_FILE_IDS.get(season)
        if file_id is None:
            print(f"  season {season}: no file id known, skipped")
            failed.append(season)
            continue

        print(f"  season {season}: downloading ...")
        try:
            gdown.download(id=file_id, output=str(out), quiet=True)
        except Exception as exc:  # quota, network, revoked share
            print(f"  season {season}: FAILED ({type(exc).__name__})")
            out.unlink(missing_ok=True)
            failed.append(season)
            continue
        print(f"  season {season}: {out.stat().st_size / 1e6:.1f} MB")

    if failed:
        print()
        print(f"Could not download seasons {failed}.")
        print(MANUAL_DOWNLOAD_HINT)

    return failed


def load_oracles_elixir(seasons: list[int] | None = None) -> pd.DataFrame:
    """Load and concatenate the season CSV files found in data/raw.

    low_memory=False avoids the mixed-dtype warning: several columns are sparse
    and pandas otherwise infers a different type per chunk.
    """
    seasons = seasons or SEASONS
    frames = []

    for season in seasons:
        matches = list(DATA_RAW.glob(f"{season}_LoL_esports_match_data*.csv"))
        if not matches:
            print(f"  season {season}: no file found, skipped")
            continue
        path = matches[0]
        df = pd.read_csv(path, low_memory=False)
        print(f"  season {season}: {len(df):,} rows, {df.shape[1]} columns  ({path.name})")
        frames.append(df)

    if not frames:
        raise FileNotFoundError(f"No Oracle's Elixir CSV found in {DATA_RAW}")

    full = pd.concat(frames, ignore_index=True)
    print(f"Total: {len(full):,} rows, {full.shape[1]} columns")
    return full


# --------------------------------------------------------------------------
# Typed loading, shared by every notebook after phase 1
# --------------------------------------------------------------------------
# `patch` must stay text: read as a float, "12.01" and "12.10" become 12.01 and
# 12.1, and the sort inverts them. Ids must stay text too, otherwise a missing
# value turns the column into floats and "12345.0" no longer joins to "12345".

OE_DTYPES = {
    "gameid": "string",
    "teamid": "string",
    "playerid": "string",
    "patch": "string",
    "league": "string",
    "split": "string",
    "position": "string",
    "teamname": "string",
    "playername": "string",
    "champion": "string",
    "side": "string",
    "datacompleteness": "string",
}

# The only player-row columns later phases need: they alone tie a champion to a
# role. Everything else on a player row is an end-of-game aggregate.
PLAYER_PROJECTION = [
    "gameid", "teamid", "side", "position", "playername", "champion", "year", "patch",
]

DATE_FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]


def parse_dates_explicit(series: pd.Series, formats: list[str] | None = None):
    """Parse a date column with an explicit format, never by inference.

    Inference can silently switch interpretation between blocks and confuse day
    and month. Tries each known format and keeps the first that fails on nothing.

    Returns (parsed, format_used, n_failures).
    """
    formats = formats or DATE_FORMATS
    best = (None, None, len(series) + 1)
    for fmt in formats:
        parsed = pd.to_datetime(series, format=fmt, errors="coerce")
        failures = int((parsed.isna() & series.notna()).sum())
        if failures == 0:
            return parsed, fmt, 0
        if failures < best[2]:
            best = (parsed, fmt, failures)
    return best


def load_split_frames(seasons: list[int] | None = None, verbose: bool = True):
    """Load the seasons once and return (team_rows, player_rows).

    Phase 1 spells this loading out cell by cell because that is what it is
    graded on. Every later notebook calls this helper instead of repeating it,
    so the dtype and date policy lives in exactly one place.

    One season is held in memory at a time: the five raw seasons together do not
    fit comfortably.
    """
    seasons = seasons or SEASONS
    team_blocks, player_blocks = [], []

    for season in seasons:
        path = DATA_RAW / OE_FILENAME.format(season=season)
        if not path.exists():
            raise FileNotFoundError(f"{path} missing.\n{MANUAL_DOWNLOAD_HINT}")

        header = pd.read_csv(path, nrows=0)
        dtypes = {c: t for c, t in OE_DTYPES.items() if c in header.columns}
        df = pd.read_csv(path, dtype=dtypes, low_memory=False)

        team_blocks.append(df[df["position"] == "team"])
        player_blocks.append(df[df["position"] != "team"][PLAYER_PROJECTION])

        if verbose:
            print(f"  saison {season} : {len(df):>7,} lignes, {df.shape[1]} colonnes")
        del df

    teams = pd.concat(team_blocks, ignore_index=True)
    players = pd.concat(player_blocks, ignore_index=True)

    teams["date"], fmt, failures = parse_dates_explicit(teams["date"])
    if failures:
        raise ValueError(f"{failures} dates unparsed with {fmt!r}")

    if verbose:
        print(f"Lignes équipe : {len(teams):>8,} | lignes joueur : {len(players):>8,}")

    return teams, players


# --------------------------------------------------------------------------
# Source 2: Riot Data Dragon (JSON)
# --------------------------------------------------------------------------

def download_champions() -> Path:
    """Fetch the current champion metadata as JSON, in two locales.

    Data Dragon is versioned. versions.json returns the list newest-first, so
    element 0 is the live patch. No API key and no authentication.

    Two locales are fetched on purpose. Oracle's Elixir writes champion names in
    English, so en_US supplies the join key. fr_FR supplies the display name used
    in the French figures and reports. Five champions differ between the two
    (K'Sante, Master Yi, Nunu & Willump, Seraphine, Zoe); joining on the French
    name would drop them silently.
    """
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    versions = requests.get(DDRAGON_VERSIONS, timeout=30).json()
    version = versions[0]
    print(f"Data Dragon current version: {version}")

    for locale, filename in (("fr_FR", "champions.json"), ("en_US", "champions_en.json")):
        url = DDRAGON_CHAMPIONS.format(version=version, locale=locale)
        payload = requests.get(url, timeout=30).json()
        out = DATA_RAW / filename
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved {len(payload['data'])} champions ({locale}) to {out}")

    return DATA_RAW / "champions.json"


def load_champions() -> pd.DataFrame:
    """Flatten the champion JSON into one row per champion.

    Data Dragon keys champions by an internal id (Wukong is MonkeyKing, Nunu &
    Willump is Nunu) and exposes a localised display name. Oracle's Elixir writes
    the English display name, so `champion` holds the English name and is the
    join key; `nom_fr` is kept for French labels. Tags are English in every
    locale, so they are read from the French payload without conversion.

    Always check for unmatched names before trusting the merge downstream.
    """
    path_fr = DATA_RAW / "champions.json"
    path_en = DATA_RAW / "champions_en.json"

    if not path_fr.exists():
        raise FileNotFoundError(f"{path_fr} missing, run download_champions() first")
    if not path_en.exists():
        raise FileNotFoundError(
            f"{path_en} missing, re-run download_champions() to fetch the en_US locale "
            "(it supplies the join key to Oracle's Elixir)"
        )

    data_fr = json.loads(path_fr.read_text(encoding="utf-8"))["data"]
    data_en = json.loads(path_en.read_text(encoding="utf-8"))["data"]

    rows = []
    for key, champ in data_fr.items():
        tags = champ.get("tags") or []
        rows.append(
            {
                "champion_key": key,
                "champion": data_en[key]["name"],   # English, joins to Oracle's Elixir
                "nom_fr": champ["name"],            # French, for figures and reports
                "tag_principal": tags[0] if tags else None,
                "tag_secondaire": tags[1] if len(tags) > 1 else None,
                "partype": champ.get("partype"),
                "attack": champ["info"]["attack"],
                "defense": champ["info"]["defense"],
                "magic": champ["info"]["magic"],
                "difficulty": champ["info"]["difficulty"],
            }
        )

    df = pd.DataFrame(rows).sort_values("champion").reset_index(drop=True)
    n_diff = int((df["champion"] != df["nom_fr"]).sum())
    print(f"Loaded {len(df)} champions, tags: {sorted(df['tag_principal'].dropna().unique())}")
    print(f"{n_diff} champions have a French name different from the English join key")
    return df


# --------------------------------------------------------------------------
# Source 3: league reference table (XLSX)
# --------------------------------------------------------------------------

# Covers every `league` code observed in the 2022-2026 team rows, 84 in total,
# plus "LCK CL" kept as a spelling variant of "LCKC".
#
# Tier is a competitive level, not a judgement on play quality:
#   1  circuit qualifying directly to Worlds, plus the international events
#   2  senior national or regional league
#   3  academy, challenger, development, collegiate, or secondary cup
#
# `confiance` records how each row was established, so the uncertainty stays
# visible instead of being laundered into a clean-looking table:
#   haute    competition identified with certainty
#   moyenne  region established from the rosters, exact competition inferred
#
# Codes whose meaning was not obvious were resolved by reading the team names
# actually present in that league. LAS, for instance, is not a Latin American
# league despite the initials: its rosters are T1 Esports Academy Rookies and
# DRX Academy, so it is the Korean academy series.
LEAGUE_REFERENCE = [
    # league, tier, region, franchisee, confiance

    # Tier 1: circuits qualifying to Worlds, and international events
    ("LCK", 1, "Coree", True, "haute"),
    ("LPL", 1, "Chine", True, "haute"),
    ("LEC", 1, "Europe", True, "haute"),
    ("LCS", 1, "Ameriques", True, "haute"),
    ("LTA", 1, "Ameriques", True, "haute"),
    ("LTA N", 1, "Ameriques", True, "haute"),
    ("LTA S", 1, "Ameriques", True, "haute"),
    ("LCP", 1, "Asie-Pacifique", True, "haute"),
    ("WLDs", 1, "International", False, "haute"),
    ("MSI", 1, "International", False, "haute"),
    ("EWC", 1, "International", False, "haute"),
    ("FST", 1, "International", False, "haute"),
    ("ASI", 1, "International", False, "moyenne"),

    # Tier 2: senior national and regional leagues
    ("CBLOL", 2, "Ameriques", True, "haute"),
    ("LLA", 2, "Ameriques", False, "haute"),
    ("CD", 2, "Ameriques", False, "haute"),
    ("LJL", 2, "Asie-Pacifique", True, "haute"),
    ("PCS", 2, "Asie-Pacifique", False, "haute"),
    ("VCS", 2, "Asie-Pacifique", False, "haute"),
    ("LCO", 2, "Asie-Pacifique", False, "haute"),
    ("KeSPA", 2, "Coree", False, "haute"),
    ("KeSPA Cup", 2, "Coree", False, "haute"),
    ("EM", 2, "Europe", False, "haute"),
    ("EUM", 2, "Europe", False, "haute"),
    ("LFL", 2, "Europe", False, "haute"),
    ("PRM", 2, "Europe", False, "haute"),
    ("NLC", 2, "Europe", False, "haute"),
    ("LVP SL", 2, "Europe", False, "haute"),
    ("UL", 2, "Europe", False, "haute"),
    ("RL", 2, "Europe", False, "moyenne"),
    ("EBL", 2, "Europe", False, "haute"),
    ("LPLOL", 2, "Europe", False, "haute"),
    ("GLL", 2, "Europe", False, "haute"),
    ("HLL", 2, "Europe", False, "moyenne"),
    ("PGN", 2, "Europe", False, "haute"),
    ("LIT", 2, "Europe", False, "moyenne"),
    ("HM", 2, "Europe", False, "haute"),
    ("ESLOL", 2, "Europe", False, "moyenne"),
    ("ROL", 2, "Europe", False, "moyenne"),
    ("LCL", 2, "CEI", False, "haute"),
    ("TCL", 2, "Turquie", False, "haute"),
    ("TSC", 2, "Turquie", False, "moyenne"),
    ("AL", 2, "Moyen-Orient", False, "haute"),

    # Tier 3: academy, challenger, development, collegiate, secondary cups
    ("LCKC", 3, "Coree", False, "haute"),
    ("LCK CL", 3, "Coree", False, "haute"),
    ("LAS", 3, "Coree", False, "haute"),
    ("LDL", 3, "Chine", False, "haute"),
    ("DCup", 3, "Chine", False, "moyenne"),
    ("NACL", 3, "Ameriques", False, "haute"),
    ("LCSA", 3, "Ameriques", False, "haute"),
    ("CBLOLA", 3, "Ameriques", False, "haute"),
    ("AC", 3, "Ameriques", False, "moyenne"),
    ("IGNIS", 3, "Ameriques", False, "moyenne"),
    ("LRN", 3, "Ameriques", False, "haute"),
    ("LRS", 3, "Ameriques", False, "haute"),
    ("LMF", 3, "Ameriques", False, "haute"),
    ("SL (LATAM)", 3, "Ameriques", False, "haute"),
    ("DDH", 3, "Ameriques", False, "moyenne"),
    ("GL", 3, "Ameriques", False, "moyenne"),
    ("VL", 3, "Ameriques", False, "moyenne"),
    ("LHE", 3, "Ameriques", False, "moyenne"),
    ("EL", 3, "Ameriques", False, "moyenne"),
    ("PGC", 3, "Ameriques", False, "moyenne"),
    ("UPL", 3, "Ameriques", False, "moyenne"),
    ("LJLA", 3, "Asie-Pacifique", False, "haute"),
    ("PCL", 3, "Asie-Pacifique", False, "haute"),
    ("ASCI", 3, "Asie-Pacifique", False, "moyenne"),
    ("Asia Master", 3, "Asie-Pacifique", False, "moyenne"),
    ("LFL2", 3, "Europe", False, "haute"),
    ("CDF", 3, "Europe", False, "haute"),
    ("NL", 3, "Europe", False, "moyenne"),
    ("PRMP", 3, "Europe", False, "haute"),
    ("NLC Aurora Open", 3, "Europe", False, "haute"),
    ("GLLPA", 3, "Europe", False, "haute"),
    ("EBLPA", 3, "Europe", False, "haute"),
    ("HC", 3, "Europe", False, "moyenne"),
    ("HW", 3, "Europe", False, "moyenne"),
    ("EPL", 3, "Europe", False, "moyenne"),
    ("NEXO", 3, "Europe", False, "moyenne"),
    ("CT", 3, "Europe", False, "moyenne"),
    ("IC", 3, "Europe", False, "moyenne"),
    ("LES", 3, "Europe", False, "moyenne"),
    ("USP", 3, "Europe", False, "moyenne"),
    ("CCWS", 3, "Europe", False, "moyenne"),
    ("TAL", 3, "Turquie", False, "haute"),
]


def build_league_reference() -> Path:
    """Write the hand-built league reference table as an Excel file.

    This is the third source and the third format required by phase 1. Keep it
    as a real .xlsx: the point of the exercise is loading a second file format.
    """
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(
        LEAGUE_REFERENCE,
        columns=["league", "tier_ligue", "region", "franchisee", "confiance"],
    )
    duplicates = df.loc[df["league"].duplicated(), "league"].tolist()
    if duplicates:
        raise ValueError(f"Duplicated league codes in LEAGUE_REFERENCE: {duplicates}")
    out = DATA_RAW / "referentiel_ligues.xlsx"
    df.to_excel(out, index=False, sheet_name="ligues")
    print(f"Saved {len(df)} leagues to {out}")
    return out


def load_league_reference() -> pd.DataFrame:
    path = DATA_RAW / "referentiel_ligues.xlsx"
    if not path.exists():
        build_league_reference()
    return pd.read_excel(path, sheet_name="ligues")


def audit_league_coverage(oe: pd.DataFrame, ref: pd.DataFrame) -> pd.DataFrame:
    """List league codes present in the match data but absent from the reference.

    Run this before merging. An unmatched league silently becomes NaN and drags
    the whole row into the missing-value bucket.
    """
    missing = set(oe["league"].dropna().unique()) - set(ref["league"])
    counts = oe[oe["league"].isin(missing)]["league"].value_counts()
    if len(missing):
        print(f"{len(missing)} league codes missing from the reference table:")
        print(counts.to_string())
    else:
        print("Every league code is covered by the reference table.")
    return counts.rename_axis("league").reset_index(name="rows")


# --------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("Source 1: Oracle's Elixir")
    print("=" * 70)
    if missing_seasons():
        download_oracles_elixir()
    oe = load_oracles_elixir()

    print()
    print("=" * 70)
    print("Source 2: Riot Data Dragon")
    print("=" * 70)
    if not (DATA_RAW / "champions_en.json").exists():
        download_champions()
    champs = load_champions()

    print()
    print("=" * 70)
    print("Source 3: league reference table")
    print("=" * 70)
    ref = load_league_reference()
    print(f"Loaded {len(ref)} leagues")

    print()
    print("=" * 70)
    print("Coverage audit")
    print("=" * 70)
    audit_league_coverage(oe, ref)

    print()
    print("Source summary")
    print(f"  Oracle's Elixir : {len(oe):>8,} rows x {oe.shape[1]:>3} cols  (CSV)")
    print(f"  Data Dragon     : {len(champs):>8,} rows x {champs.shape[1]:>3} cols  (JSON)")
    print(f"  Ligues          : {len(ref):>8,} rows x {ref.shape[1]:>3} cols  (XLSX)")


if __name__ == "__main__":
    main()
