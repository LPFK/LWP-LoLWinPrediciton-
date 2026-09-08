"""Phase 6 helpers: one visual identity for every figure of the project.

Introduced in phase 6. Notebooks 02 and 05 keep their own inline rcParams block,
identical in content, rather than being edited after they were validated and
re-executed. Everything still reads the same palette from ``src/config.py``, so
the figures match whichever path produced them.

Three things are enforced here rather than left to each cell.

- The charcoal and slate palette, so no figure ever falls back to the default
  matplotlib blue and orange.
- The source and period caption. The phase 6 checklist asks for it on every
  figure, and a caption written by hand nine times is a caption that will be
  wrong once.
- ``axes.axisbelow``, so the grid is drawn behind the marks instead of striping
  them.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from . import config

PALETTE = config.PALETTE

# Diverging ramp, brick to charcoal through a warm neutral. Used for the
# correlation heatmap, where the sign matters as much as the magnitude.
CMAP_ARDOISE = LinearSegmentedColormap.from_list(
    "ardoise", [PALETTE["highlight"], "#E8D5C4", PALETTE["accent"], PALETTE["primary"]]
)

SOURCE = "Source : Oracle's Elixir (Tim Sevenhuysen, oracleselixir.com)"
PERIODE = "Saisons 2022 à 2025, jeu d'entraînement uniquement"


def appliquer_style() -> None:
    """Apply the project palette to every subsequent figure."""
    plt.rcParams.update({
        "figure.facecolor": PALETTE["background"],
        "axes.facecolor": PALETTE["background"],
        "axes.edgecolor": PALETTE["secondary"],
        "axes.labelcolor": PALETTE["primary"],
        "text.color": PALETTE["primary"],
        "xtick.color": PALETTE["secondary"],
        "ytick.color": PALETTE["secondary"],
        "grid.color": PALETTE["grid"],
        "font.size": 10,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    config.FIGURES.mkdir(parents=True, exist_ok=True)


def nombre_fr(valeur: float, decimales: int = 1, signe: bool = False) -> str:
    """French decimal notation: comma, not point.

    Every figure of this project is read in French, where 13,6 is a number and
    13.6 is a typo. The notebook prose already writes it that way; without this
    helper the figures would say something else than the paragraph next to them.
    """
    gabarit = f"{{:{'+' if signe else ''}.{decimales}f}}"
    return gabarit.format(valeur).replace(".", ",")


def entier_fr(valeur: float) -> str:
    """French thousands notation: space, not comma."""
    return f"{int(round(valeur)):,}".replace(",", " ")


def signer(fig, periode: str = PERIODE, source: str = SOURCE, y: float = -0.01) -> None:
    """Add the source and period caption at the bottom left of a figure.

    Required by the phase 6 checklist: a reader who meets the figure outside the
    notebook, in the slide deck for instance, must still know where the numbers
    come from and which seasons they cover.
    """
    fig.text(0.01, y, f"{source}  |  {periode}", ha="left", va="top",
             fontsize=7.5, color=PALETTE["secondary"])


def enregistrer(fig, nom: str, dpi: int = 150):
    """Save a figure into ``figures/`` and return its path."""
    chemin = config.FIGURES / nom
    fig.savefig(chemin, dpi=dpi, facecolor=PALETTE["background"], bbox_inches="tight")
    return chemin


def tuile_kpi(ax, valeur: str, libelle: str, accent: bool = False) -> None:
    """Draw one KPI tile: a large number over a small caption, no axes.

    Used only by the dashboard. The tiles carry the four figures a reader should
    remember even if they read nothing else.
    """
    ax.axis("off")
    couleur = PALETTE["highlight"] if accent else PALETTE["primary"]
    ax.text(0.5, 0.62, valeur, ha="center", va="center", fontsize=21,
            fontweight="bold", color=couleur)
    ax.text(0.5, 0.20, libelle, ha="center", va="center", fontsize=8,
            color=PALETTE["secondary"])
    ax.add_patch(plt.Rectangle((0.02, 0.05), 0.96, 0.9, transform=ax.transAxes,
                               fill=False, edgecolor=PALETTE["grid"], linewidth=1))
