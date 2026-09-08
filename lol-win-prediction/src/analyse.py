"""Phase 5 helpers: descriptive analysis with the uncertainty attached.

Two conventions are enforced here rather than left to the notebook.

First, every win rate comes back with the size of the group that produced it and
a confidence interval. A win rate of 56 % on 80 rows and a win rate of 56 % on
8 000 rows are not the same finding, and a table that shows only the percentage
makes them look identical.

Second, nothing in this module knows about the test season. The notebook slices
the training period once and passes it in. The 2026 rows are opened once, in
phase 7, and reading them here to "just have a look" would spend that single
look on an exploratory question.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

Z_95 = 1.959963985


# --------------------------------------------------------------------------
# Proportions and their uncertainty
# --------------------------------------------------------------------------

def intervalle_wilson(succes: int, effectif: int, z: float = Z_95) -> tuple[float, float]:
    """95 % confidence interval of a proportion, Wilson score method.

    Wilson rather than the textbook normal approximation because several groups
    here are small or land near 0 and 1 (a comeback rate below a 3 000 gold
    deficit, for instance), where the normal interval leaves the [0, 1] range and
    stops meaning anything.
    """
    if effectif == 0:
        return (np.nan, np.nan)
    p = succes / effectif
    denominateur = 1 + z**2 / effectif
    centre = (p + z**2 / (2 * effectif)) / denominateur
    demi_largeur = (
        z * math.sqrt(p * (1 - p) / effectif + z**2 / (4 * effectif**2)) / denominateur
    )
    return (centre - demi_largeur, centre + demi_largeur)


def test_deux_proportions(succes_a: int, n_a: int, succes_b: int, n_b: int) -> dict:
    """Two-sided z test comparing two independent proportions.

    Hand-written rather than imported: scipy is not in requirements.txt, and the
    three lines below are easier to defend orally than a function call whose
    internals the student has not read. ``erfc`` gives the two-sided p-value of a
    standard normal directly.
    """
    if n_a == 0 or n_b == 0:
        return {"ecart": np.nan, "z": np.nan, "p_valeur": np.nan}
    p_a, p_b = succes_a / n_a, succes_b / n_b
    p_commun = (succes_a + succes_b) / (n_a + n_b)
    erreur = math.sqrt(p_commun * (1 - p_commun) * (1 / n_a + 1 / n_b))
    if erreur == 0:
        return {"ecart": p_a - p_b, "z": np.nan, "p_valeur": np.nan}
    z = (p_a - p_b) / erreur
    return {
        "ecart": p_a - p_b,
        "z": z,
        "p_valeur": math.erfc(abs(z) / math.sqrt(2)),
    }


# --------------------------------------------------------------------------
# Win rate by group
# --------------------------------------------------------------------------

def taux_victoire(
    donnees: pd.DataFrame,
    par: str | list[str],
    cible: str = "result",
    effectif_minimum: int = 100,
) -> pd.DataFrame:
    """Win rate per group, with sample size and 95 % interval.

    Groups below `effectif_minimum` are kept but flagged, never silently dropped:
    a league with 75 rows is a real finding about the coverage of the dataset,
    and hiding it would make the table look more solid than it is.
    """
    groupes = donnees.groupby(par, observed=True)[cible].agg(
        victoires="sum", effectif="size"
    )
    groupes["taux"] = groupes["victoires"] / groupes["effectif"]

    bornes = [
        intervalle_wilson(int(v), int(n))
        for v, n in zip(groupes["victoires"], groupes["effectif"])
    ]
    groupes["ic_bas"] = [b[0] for b in bornes]
    groupes["ic_haut"] = [b[1] for b in bornes]
    groupes["fiable"] = groupes["effectif"] >= effectif_minimum
    return groupes.drop(columns="victoires")


def taux_victoire_par_tranche(
    donnees: pd.DataFrame,
    colonne: str,
    bornes: np.ndarray,
    cible: str = "result",
) -> pd.DataFrame:
    """Win rate along the bins of a continuous variable, with bin midpoints.

    The midpoint column is what makes the result plottable and lets a slope be
    fitted on it, which is how the gold value of an objective is derived.
    """
    decoupe = pd.cut(donnees[colonne], bornes)
    table = taux_victoire(
        donnees.assign(_tranche=decoupe), "_tranche", cible=cible, effectif_minimum=50
    )
    table["milieu"] = [intervalle.mid for intervalle in table.index]
    return table


# --------------------------------------------------------------------------
# Discriminant power
# --------------------------------------------------------------------------

def pouvoir_discriminant(
    donnees: pd.DataFrame, colonnes: list[str], cible: str = "result"
) -> pd.DataFrame:
    """Univariate ROC AUC and point-biserial correlation of each column.

    The AUC is folded above 0.5: a variable that separates the classes perfectly
    in the wrong direction is just as informative as one that does it in the
    right direction, and `deathsat15` is exactly that case. The `sens` column
    keeps the direction, which is what the interpretation needs.

    This is a descriptive measure, not a model. It ignores every correlation
    between features, which is precisely why phase 5 also looks at objectives at
    equal gold: a variable can score well here and add nothing once the gold lead
    is known.
    """
    lignes = []
    for colonne in colonnes:
        valeurs = pd.to_numeric(donnees[colonne], errors="coerce")
        renseigne = valeurs.notna()
        if renseigne.sum() == 0 or valeurs[renseigne].nunique() < 2:
            continue
        auc_brut = roc_auc_score(donnees.loc[renseigne, cible], valeurs[renseigne])
        lignes.append(
            {
                "feature": colonne,
                "auc_univarie": max(auc_brut, 1 - auc_brut),
                "correlation": valeurs.corr(donnees[cible].astype(float)),
                "sens": "positif" if auc_brut >= 0.5 else "negatif",
                "manquant_pct": 100 * (~renseigne).mean(),
            }
        )
    return (
        pd.DataFrame(lignes)
        .sort_values("auc_univarie", ascending=False)
        .reset_index(drop=True)
    )


# --------------------------------------------------------------------------
# Gold equivalence
# --------------------------------------------------------------------------

def pente_or(
    donnees: pd.DataFrame,
    colonne_or: str = "golddiffat15",
    amplitude: int = 1500,
    pas: int = 250,
) -> tuple[float, pd.DataFrame]:
    """Local slope of the win rate against the gold lead, in win rate per gold.

    Fitted on the central band only, where the empirical curve is close to
    linear. Extending it to the tails would flatten the slope through the
    saturation near 0 and 1 and undervalue every objective priced with it.

    Returns the slope and the curve it was fitted on, so the notebook can show
    the fit rather than assert it.
    """
    bande = donnees[donnees[colonne_or].abs() <= amplitude]
    courbe = taux_victoire_par_tranche(
        bande, colonne_or, np.arange(-amplitude, amplitude + 1, pas)
    )
    pente = np.polyfit(courbe["milieu"], courbe["taux"], 1)[0]
    return float(pente), courbe


def valeur_en_or(
    donnees: pd.DataFrame,
    indicateur: str,
    pente: float,
    bande_or: int = 250,
    colonne_or: str = "golddiffat15",
    cible: str = "result",
) -> dict:
    """Price a binary early objective in gold, at equal gold lead.

    The comparison is restricted to the games where both teams are within
    `bande_or` gold of each other at minute 15. Inside that band the gold lead no
    longer explains anything, so the win rate gap between the team that took the
    objective and the team that did not is what the objective carries *on top of*
    the gold it already granted.

    A first blood hands 400 gold to the killer, so its value is already inside
    `golddiffat15` and it should price near zero here. A dragon grants no gold at
    all, only a stacking buff, so whatever it is worth has to show up in this
    residual. That contrast is the point of the measure.
    """
    bande = donnees[donnees[colonne_or].abs() < bande_or]
    avec = bande[bande[indicateur] == 1]
    sans = bande[bande[indicateur] == 0]

    test = test_deux_proportions(
        int(avec[cible].sum()), len(avec), int(sans[cible].sum()), len(sans)
    )
    return {
        "indicateur": indicateur,
        "taux_avec": avec[cible].mean(),
        "taux_sans": sans[cible].mean(),
        "n_avec": len(avec),
        "n_sans": len(sans),
        "ecart_points": 100 * test["ecart"],
        "p_valeur": test["p_valeur"],
        "or_equivalent": test["ecart"] / pente if pente else np.nan,
    }
