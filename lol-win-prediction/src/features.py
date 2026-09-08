"""Phase 4 helpers: build the engineered features, leak-free by construction.

Every historical feature in this module answers the same question: "what was
known BEFORE this game started?" The answer is never allowed to include the
current row, nor any later row.

Two mechanisms enforce that, and they are the only two used here:

- ``shift(1)`` after sorting by date, so a rolling window ends on the previous
  game.
- ``cumcount()`` and a shifted ``cumsum()``, which are past-only by definition.

A global ``groupby().mean()`` would be the classic mistake: it would hand a team
its own future results, and the model would look excellent right up to the day
it is used for real.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Composition, rebuilt from the player rows
# --------------------------------------------------------------------------
# The team rows carry pick1..pick5, but they are missing on 9 % of rows. The
# player rows carry `champion` with no gaps at all, and they are the only place
# where a champion is tied to a role. They are therefore the source of truth.
#
# The join key is gameid + side, never gameid + teamid: `teamid` is missing on
# 1 800 team rows, and a NaN key silently drops those groups.

DAMAGE_PHYSIQUE = {"Marksman", "Fighter", "Assassin"}
DAMAGE_MAGIQUE = {"Mage"}

TAGS_CONNUS = ["Tank", "Mage", "Marksman", "Fighter", "Assassin", "Support"]


def composition_par_equipe(joueurs: pd.DataFrame, champions: pd.DataFrame) -> pd.DataFrame:
    """One row per team-game, with the tag counts of its five champions.

    Parameters
    ----------
    joueurs : player rows, needs gameid, side, champion
    champions : Data Dragon table, needs champion (English name), tag_principal,
        tag_secondaire

    Returns
    -------
    DataFrame keyed by gameid + side, with the compo_nb_* counts, profil_degats
    and the number of champions actually matched.
    """
    tags = champions.set_index("champion")[["tag_principal", "tag_secondaire"]]
    j = joueurs.merge(tags, left_on="champion", right_index=True, how="left")

    # A champion counts for a tag whether it is its primary or secondary one:
    # Nunu & Willump is Tank/Mage, and ignoring the second tag would lose that.
    for tag in TAGS_CONNUS:
        j[f"est_{tag}"] = (
            (j["tag_principal"] == tag) | (j["tag_secondaire"] == tag)
        ).astype(int)

    j["est_ad"] = j["tag_principal"].isin(DAMAGE_PHYSIQUE).astype(int)
    j["est_ap"] = j["tag_principal"].isin(DAMAGE_MAGIQUE).astype(int)
    j["champion_reconnu"] = j["tag_principal"].notna().astype(int)

    compo = j.groupby(["gameid", "side"]).agg(
        compo_nb_tank=("est_Tank", "sum"),
        compo_nb_mage=("est_Mage", "sum"),
        compo_nb_marksman=("est_Marksman", "sum"),
        compo_nb_fighter=("est_Fighter", "sum"),
        compo_nb_assassin=("est_Assassin", "sum"),
        compo_nb_support=("est_Support", "sum"),
        _n_ad=("est_ad", "sum"),
        _n_ap=("est_ap", "sum"),
        champions_reconnus=("champion_reconnu", "sum"),
    )

    # Share of physical damage among the champions whose damage profile is
    # identifiable. Expressed as a share rather than an AD/AP ratio, which would
    # divide by zero on a composition without a single mage.
    total = compo["_n_ad"] + compo["_n_ap"]
    compo["profil_degats"] = np.where(total > 0, compo["_n_ad"] / total, np.nan)

    return compo.drop(columns=["_n_ad", "_n_ap"]).reset_index()


def roster_par_equipe(joueurs: pd.DataFrame) -> pd.DataFrame:
    """One row per team-game, with a stable identifier of its five-player lineup.

    The names are sorted before being joined, so the same five people always
    produce the same key whatever the row order.
    """
    return (
        joueurs.dropna(subset=["playername"])
        .groupby(["gameid", "side"])["playername"]
        .apply(lambda s: "|".join(sorted(s)))
        .rename("roster_key")
        .reset_index()
    )


# --------------------------------------------------------------------------
# Historical features: expanding windows over past games only
# --------------------------------------------------------------------------

def forme_equipe(
    equipes: pd.DataFrame, fenetre: int = 10, cle: str = "team_key"
) -> pd.Series:
    """Win rate of a team over its `fenetre` previous games.

    ``shift(1)`` is the whole point: without it the current result would be part
    of its own predictor, which is a textbook leak.

    The first game of a team is NaN by construction, since it has no past.
    """
    ordonne = equipes.sort_values(["date", "gameid"])
    forme = ordonne.groupby(cle)["result"].transform(
        lambda s: s.shift(1).rolling(fenetre, min_periods=1).mean()
    )
    return forme.reindex(equipes.index)


def experience_roster(equipes: pd.DataFrame, cle: str = "roster_key") -> pd.Series:
    """Number of games the current five-player lineup has already played together.

    ``cumcount`` counts the rows that came before within the group, so it is
    past-only by definition and needs no shift.
    """
    ordonne = equipes.sort_values(["date", "gameid"])
    return ordonne.groupby(cle).cumcount().reindex(equipes.index)


def winrate_champion_patch(joueurs_avec_resultat: pd.DataFrame) -> pd.Series:
    """Win rate of each champion on the PRIOR games of the same patch.

    Computed on player rows, where one row is one champion in one game.

    Both terms are past-only: the numerator is a cumulative sum from which the
    current row is subtracted, the denominator is ``cumcount``. The first
    appearance of a champion on a patch has no history and yields NaN, which is
    the honest answer. Filling it with 0.5 would inject an assumption; the phase
    7 imputer will deal with it on the training set alone.
    """
    ordonne = joueurs_avec_resultat.sort_values(["date", "gameid"])
    groupe = ordonne.groupby(["champion", "patch"], observed=True)

    victoires_avant = groupe["result"].cumsum() - ordonne["result"]
    parties_avant = groupe.cumcount()

    winrate = np.where(parties_avant > 0, victoires_avant / parties_avant, np.nan)
    return pd.Series(winrate, index=ordonne.index).reindex(joueurs_avec_resultat.index)


def mediane_or_patch_expansive(equipes: pd.DataFrame, min_parties: int = 20) -> pd.Series:
    """Median team gold at 15 over the PRIOR games of the same patch.

    Used to normalise the gold lead. Phase 2 measured a 7 to 10 % meta drift on
    gold between the training and test seasons, so a raw gold lead does not carry
    the same meaning in 2022 and in 2026.

    The obvious implementation, ``groupby('patch')['goldat15'].transform('median')``,
    is a leak: it hands every game the median of its whole patch, including games
    played after it. The expanding median below only ever sees the past.
    """
    ordonne = equipes.sort_values(["date", "gameid"])
    mediane = ordonne.groupby("patch")["goldat15"].transform(
        lambda s: s.shift(1).expanding(min_periods=min_parties).median()
    )
    return mediane.reindex(equipes.index)


# --------------------------------------------------------------------------
# Patch handling
# --------------------------------------------------------------------------

def decouper_patch(patch: pd.Series) -> pd.DataFrame:
    """Split "12.01" into integer major and minor parts.

    Read as a float, "12.01" and "12.10" would become 12.01 and 12.1, and the
    sort would invert them. Oracle's Elixir zero-pads the minor part, so a text
    sort happens to work, but the explicit split does not depend on that.
    """
    morceaux = patch.str.split(".", n=1, expand=True)
    return pd.DataFrame(
        {
            "patch_major": pd.to_numeric(morceaux[0], errors="coerce").astype("Int64"),
            "patch_minor": pd.to_numeric(morceaux[1], errors="coerce").astype("Int64"),
        },
        index=patch.index,
    )


def rang_patch_dans_saison(equipes: pd.DataFrame) -> np.ndarray:
    """Rank of the patch within its season, starting at 1.

    `patch_major` cannot be a feature: its 2026 values never appear in training.
    The rank does generalise, because every season has a first patch, a second
    one, and so on.
    """
    couples = (
        equipes[["saison", "patch_major", "patch_minor"]]
        .drop_duplicates()
        .dropna()
        .sort_values(["saison", "patch_major", "patch_minor"])
    )
    couples["patch_seq"] = couples.groupby("saison").cumcount() + 1

    fusion = equipes[["saison", "patch_major", "patch_minor"]].merge(
        couples, on=["saison", "patch_major", "patch_minor"], how="left"
    )
    return fusion["patch_seq"].to_numpy()


# --------------------------------------------------------------------------
# Leak audit
# --------------------------------------------------------------------------

def auditer_fuite_temporelle(
    donnees: pd.DataFrame, colonnes: list[str], cle: str
) -> pd.DataFrame:
    """Check that each historical feature is undefined on the first game of a group.

    A past-only feature has nothing to say about the first game of a team, a
    roster or a champion. If it does say something there, it read the present.
    This is the cheapest available test for that class of bug.
    """
    ordonne = donnees.sort_values(["date", "gameid"])
    premiere = ordonne.groupby(cle).cumcount() == 0

    lignes = []
    for col in colonnes:
        if col not in ordonne.columns:
            continue
        a_tort = int(ordonne.loc[premiere, col].notna().sum())
        lignes.append(
            {
                "feature": col,
                "cle_de_groupe": cle,
                "premieres_parties": int(premiere.sum()),
                "renseignees_a_tort": a_tort,
                "verdict": "ok" if a_tort == 0 else "fuite probable",
            }
        )
    return pd.DataFrame(lignes)
