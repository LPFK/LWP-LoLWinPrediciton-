# Rapport d'analyse, phase 5

Document genere par `notebooks/05_eda_analytique.ipynb`, a ne pas editer a la main.

Donnees fournies par Oracle's Elixir (Tim Sevenhuysen, oracleselixir.com).

## Perimetre

| Propriete | Valeur |
|---|---|
| Lignes analysees | 76,070 |
| Parties | 38,035 |
| Periode | 2022-01-10 au 2025-12-29 |
| Saisons | 2022 a 2025 |
| Cible | equilibree a 50.00 % |
| Saison 2026 | 16,546 lignes reservees au test, non ouvertes |

Toutes les analyses sont calculees sur le seul jeu d'entrainement. La saison 2026 est ouverte
une fois, a la fin de la phase 7. La regarder ici reviendrait a choisir des hypotheses en
fonction du jeu de test, et le score final ne mesurerait plus rien.

Chaque taux de victoire est accompagne de son effectif et d'un intervalle de confiance a 95 %
calcule par la methode de Wilson. Quand l'intervalle contient 50 %, la conclusion retenue est
qu'il n'y a rien a conclure.

## Synthese des cinq questions business

| # | Question business | Insight principal | Chiffre cle | Confiance | Action proposee |
|---|---|---|---|---|---|
| 1 | Quels avantages pesent le plus a 15 minutes ? | L'or domine, mais seul le premier dragon apporte quelque chose au-dela | 1 000 or = 13.6 pts ; premier dragon = 1031 or | elevee | Prioriser le dragon sur le premier sang a l'entrainement |
| 2 | L'avantage du cote bleu existe-t-il encore ? | Oui, faible mais reel et stable sur quatre saisons | 52.9 % [52.4 ; 53.4] | elevee | Preparer une strategie de draft distincte par cote |
| 3 | La composition compte-t-elle a or egal ? | Aucun effet mesurable avec les tags de Data Dragon | ecart maximal a 50 % : 2.8 pt, tous les IC contiennent 50 % | moyenne | Ne pas arbitrer un pick sur un comptage de tags |
| 4 | La forme aide-t-elle a convertir une avance ? | Non, elle pese davantage dans les parties serrees | 18.1 pts en partie serree contre 12.4 pts en avance | moyenne | Cibler le coaching sur les parties serrees |
| 5 | Les ligues majeures convertissent-elles mieux ? | Non, les courbes de conversion se superposent | tier 1 80.1 % contre tier 3 80.5 %, p = 0.56 | moyenne a elevee | Ne pas decoter un joueur de ligue mineure sur ce critere |

## Methode commune aux analyses de contribution

L'ecart d'or a la 15e minute est de tres loin le premier signal disponible. La question posee
pour la plupart des variables n'est donc pas de savoir si elle est associee a la victoire, mais
si elle apporte quelque chose au-dela de l'or.

La methode employee est la meme partout : restreindre l'analyse aux parties ou les deux equipes
sont au coude a coude a la 15e minute. Dans cette bande, l'or n'explique plus rien, et l'ecart
de taux de victoire qui subsiste est un apport propre. La pente locale de la courbe de
conversion, 13.64 points de taux de victoire pour 1 000 or, permet ensuite de
traduire cet apport en or.

Le controle a ete verifie et non suppose : dans la bande a 500 or, l'ecart d'or moyen de chaque
groupe de composition suffisamment peuple reste a moins de 14 or de zero.

## Question 1 : hierarchie des avantages a la 15e minute

Classement univarie, AUC sur le jeu d'entrainement :

| feature | auc_univarie | correlation | sens | manquant_pct |
|---|---|---|---|---|
| ecart_or_normalise | 0.82 | 0.534 | positif | 2.36 |
| golddiffat15 | 0.82 | 0.533 | positif | 0.0 |
| xpdiffat15 | 0.792 | 0.494 | positif | 0.0 |
| diff_kills_at15 | 0.763 | 0.449 | positif | 0.0 |
| csdiffat15 | 0.748 | 0.43 | positif | 0.0 |
| objectifs_precoces | 0.679 | 0.327 | positif | 0.0 |

Valeur propre des objectifs, mesuree a ecart d'or inferieur a 250 :

| indicateur | taux_avec | taux_sans | n_avec | ecart_points | p_valeur | or_equivalent |
|---|---|---|---|---|---|---|
| firstblood | 50.19 | 49.81 | 2843 | 0.39 | 7.7e-01 | 28.0 |
| firstdragon | 57.03 | 42.97 | 2844 | 14.06 | 2.8e-26 | 1031.0 |
| firstherald | 50.44 | 49.56 | 2837 | 0.88 | 5.1e-01 | 64.0 |

Le premier dragon vaut environ 1031 or. Le premier sang et le
premier heraut ne valent rien de plus que l'or qu'ils rapportent deja, ce qui est coherent avec
la mecanique du jeu : les deux rapportent de l'or, le dragon n'en rapporte aucun.

Figures : `figures/05_conversion_ecart_or.png` et `figures/05_valeur_objectifs_precoces.png`.

## Question 2 : avantage du cote bleu

Taux de victoire du cote bleu sur 38,035 parties : 52.93 %,
intervalle de confiance [52.43 % ; 53.43 %]. L'intervalle ne contient
pas 50 %, l'avantage est reel. Il equivaut a environ
215 or offerts avant le debut de la partie.

Par saison :

| saison | effectif | taux | ic_bas | ic_haut | fiable |
|---|---|---|---|---|---|
| 2022 | 10641 | 0.523 | 0.5135 | 0.5325 | True |
| 2023 | 9371 | 0.5335 | 0.5233 | 0.5435 | True |
| 2024 | 8802 | 0.5287 | 0.5183 | 0.5392 | True |
| 2025 | 9221 | 0.5329 | 0.5227 | 0.5431 | True |

L'avantage est stable, sans tendance, et les intervalles des quatre saisons se recoupent.

Figure : `figures/05_avantage_cote_bleu.png`.

## Question 3 : composition de draft a avantage economique egal

Aucun effet mesurable. Sur les groupes de composition suffisamment peuples, l'ecart maximal au
hasard est de 2.83 points et 100 % des intervalles de
confiance contiennent 50 %. Le controle economique tient : l'ecart d'or moyen de ces groupes
reste a moins de 14 or de zero.

Ce resultat porte sur cette representation de la composition, un comptage de tags Data Dragon,
et non sur la composition en general. La synergie entre champions et l'ordre de la draft, absent
d'Oracle's Elixir, ne sont pas captures.

## Question 4 : forme recente et conversion d'une avance

Amplitude du taux de victoire entre une equipe a moins de 30 % de forme et une equipe a plus de
70 %, selon le regime de partie :

| Regime | Amplitude |
|---|---|
| Partie equilibree, ecart d'or inferieur a 500 | 18.1 points |
| Avance de plus de 1 000 or | 12.4 points |
| Retard de plus de 1 000 or | 15.0 points |

L'effet de la forme est le plus fort dans les parties serrees, pas dans celles ou une avance est
deja prise. La forme mesure donc surtout le niveau de l'equipe, pas une capacite a conclure.

Figure : `figures/05_forme_et_conversion.png`.

## Question 5 : niveau de ligue et conversion

Conversion d'une avance de plus de 1 000 or :

| tier_ligue | effectif | taux | ic_bas | ic_haut | fiable |
|---|---|---|---|---|---|
| 1 | 3602 | 0.8009 | 0.7876 | 0.8137 | True |
| 2 | 12530 | 0.815 | 0.8081 | 0.8217 | True |
| 3 | 10777 | 0.8054 | 0.7978 | 0.8128 | True |

Comparaison tier 1 contre tier 3 : ecart de -0.45 point, p-valeur
0.558. Aucune difference significative.

Pentes de conversion, en points de taux de victoire pour 1 000 or : tier 1 12.83,
tier 2 13.65, tier 3 13.95. La tendance va a l'inverse de l'idee recue, le
tier 1 etant marginalement le moins deterministe.

Figure : `figures/05_conversion_par_tier.png`.

## Decouvertes inattendues

| Decouverte | Chiffre | Implication |
|---|---|---|
| Le premier sang est entierement mediatise par l'or | correlation brute 0.20, apport a or egal 0.4 pt | Un indicateur tres commente qui n'ajoute rien au modele |
| La forme pese plus dans une partie serree que dans une partie engagee | 18.1 pts contre 12.4 pts | La forme mesure le niveau, pas une capacite a conclure |
| Une minorite de parties est deja jouee a la 15e minute | 28.2 % des lignes ont plus de 3 000 or d'ecart, converties a 91.8 % | Le plafond de performance attendu vient des parties serrees |

## Limites

- Le perimetre exclut une grande partie de la LPL, consequence de la regle de completude de la
  phase 3. Aucune conclusion regionale sur la Chine n'est possible.
- Association n'est pas causalite. Le controle par la bande d'or porte sur une seule dimension.
- Quatre saisons de meta sont agregees, dont deux changements de regles majeurs.
- La saison 2026 n'a pas ete regardee, limite volontaire.

## Implications pour la phase 7

1. Le plafond attendu de 72 a 78 % d'accuracy est coherent avec la structure des donnees :
   28.2 % des lignes seulement presentent plus de 3 000 or d'ecart a la 15e minute.
2. Les cinq variables de composition sont les premieres candidates au retrait.
3. `firstblood` et `firstherald` n'apportent rien en univarie a or egal, leur coefficient dans
   la regression logistique sera a examiner.
4. Les relations observees sont presque toutes monotones, ce qui conforte la regression
   logistique comme modele de reference interpretable.
