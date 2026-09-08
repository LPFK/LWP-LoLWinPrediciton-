# Visualisations, phase 6

Document genere par `notebooks/06_visualisation.ipynb`, a ne pas editer a la main.

Donnees fournies par Oracle's Elixir (Tim Sevenhuysen, oracleselixir.com).
Toutes les figures portent sur les saisons 2022 a 2025, jeu d'entrainement uniquement.
La saison 2026 reste fermee jusqu'a la fin de la phase 7.

## Le fil rouge

Tous les avantages precoces ne se valent pas, et le classement auquel tout le monde se fie est
presque exactement a l'envers. Le premier heraut mene le classement brut avec
+22,9 points d'ecart de taux de victoire et ne vaut plus que
+0,9 point une fois l'or neutralise. Le premier dragon ferme ce meme
classement et vaut 1 030 or.

Le recit se deroule en quatre actes : ce que l'on sait a la 15e minute, le classement trompeur,
la mesure a avantage economique egal, puis les trois regimes de partie qui cadrent ce qu'un
modele peut esperer.

## Regles de design appliquees

| Regle | Application sur ce projet |
|---|---|
| Honnetete des axes | Toute barre part de zero. L'avantage du cote bleu, trop faible pour etre lisible ainsi, est represente comme un ecart au hasard centre sur zero plutot que par une barre tronquee |
| Focus | Ardoise pour le contexte, brique sourde pour l'element a regarder, une seule couleur d'accent par figure |
| Simplicite | Aucun effet de relief, aucun double axe, quatre couleurs au maximum |
| Coherence | Palette et styles centralises dans `src/config.py` et `src/viz.py` |
| Source et periode | Ajoutees automatiquement par `viz.signer` sur chaque figure |

## Fiches par figure

| Fichier | Question business | Type de graphique | Message transmis | Audience | Poids (ko) |
|---|---|---|---|---|---|
| 06_tableau_de_bord.png | Vue d'ensemble | Tableau de bord, tuiles plus courbe plus barres | Quatre chiffres a retenir et la relation qui structure le projet | Direction sportive, producteur | 190 |
| 06_hierarchie_avantages.png | Question 1 | Barres horizontales triees | Le classement brut place les objectifs precoces loin derriere l'or | Analyste, casteur | 101 |
| 06_illusion_des_objectifs.png | Question 1 | Barres groupees, contraste | A or egal le classement s'inverse : le dragon vaut 1 030 or, les autres zero | Coach, analyste | 81 |
| 06_avantage_cote_bleu.png | Question 2 | Ligne temporelle plus barres d'ecart au hasard | Un avantage de 2,9 points, faible mais stable sur quatre saisons | Coach, staff de draft | 113 |
| 06_composition_sans_effet.png | Question 3 | Petits multiples, points et intervalles | Aucune composition ne sort du hasard une fois l'or neutralise | Staff de draft | 83 |
| 06_forme_par_regime.png | Question 4 | Lignes multiples, trois series | La forme mesure le niveau de l'equipe, pas une capacite a conclure | Coach, preparateur mental | 111 |
| 06_ligues_conversion.png | Question 5 | Barres groupees depuis zero | Le niveau de ligue ne change pas la valeur d'une avance precoce | Recrutement, scouting | 83 |
| 06_trois_regimes_de_partie.png | Transversale | Histogramme avec zones | Un tiers des parties est deja pliee, un tiers est encore indecise | Analyste, jury technique | 87 |
| 06_redondance_features.png | Preparation phase 7 | Carte de chaleur divergente | Deux features portent la meme information a 1,00 de correlation | Technique | 278 |

## Chiffres cles portes par les figures

| Chiffre | Valeur | Figure |
|---|---|---|
| Pente de conversion de l'or | 13,6 points de taux de victoire pour 1 000 or | `06_tableau_de_bord.png` |
| Valeur reelle du premier dragon | 1 030 or, soit +14,1 points | `06_illusion_des_objectifs.png` |
| Valeur reelle du premier sang | +0,4 point, non significatif | `06_illusion_des_objectifs.png` |
| Avantage du cote bleu | 52,9 % [52,4 ; 53,4] | `06_avantage_cote_bleu.png` |
| Parties encore serrees a 15 minutes | 29 % des lignes, camp en avance a 57 % | `06_trois_regimes_de_partie.png` |
| Parties deja pliees | 28 % des lignes, camp en avance a 92 % | `06_trois_regimes_de_partie.png` |
| Ecart tier 1 contre tier 3 | -0,4 point, p = 0,56 | `06_ligues_conversion.png` |

## Inventaire du dossier figures/

15 fichiers, pour un minimum requis de 7.

- `02_completude_at15_ligue_saison.png`
- `05_avantage_cote_bleu.png`
- `05_conversion_ecart_or.png`
- `05_conversion_par_tier.png`
- `05_forme_et_conversion.png`
- `05_valeur_objectifs_precoces.png`
- `06_avantage_cote_bleu.png`
- `06_composition_sans_effet.png`
- `06_forme_par_regime.png`
- `06_hierarchie_avantages.png`
- `06_illusion_des_objectifs.png`
- `06_ligues_conversion.png`
- `06_redondance_features.png`
- `06_tableau_de_bord.png`
- `06_trois_regimes_de_partie.png`

## Ce que ces figures preparent pour la phase 7

1. L'attente de performance est cadree : 28 % des lignes se predisent presque seules
   et 29 % restent indecises, ce qui rend plausible une accuracy de 72 a 78 % et
   suspect tout score nettement superieur.
2. Une redondance forte est documentee entre `golddiffat15` et `ecart_or_normalise`. La
   regression logistique devra etre regularisee, ou l'une des deux variables retiree, decision a
   prendre sur la validation croisee du train.
3. Les variables de composition n'apportent rien en univarie ni a or egal. Elles restent au
   premier tour et sont les premieres candidates au retrait.
