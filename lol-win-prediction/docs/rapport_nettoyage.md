# Rapport de nettoyage

Phase 3 du projet final Machine Learning. Document généré par
`notebooks/03_nettoyage.ipynb`, à ne pas éditer à la main.

Source : `data/raw/`, jamais modifiée.
Sortie : `data/interim/equipes_interim.parquet` et `data/interim/joueurs_interim.parquet`.

## Règle qui encadre tout le nettoyage

Aucune imputation statistique n'est réalisée ici. Le guide l'interdit et la grille en fait une
règle éliminatoire : remplacer une valeur manquante par une moyenne calculée sur l'ensemble des
données ferait fuiter le jeu de test dans le jeu d'entraînement.

Les seules stratégies employées sont la suppression de lignes, la suppression de colonnes, le
drapeau avec conservation, la valeur constante explicite et la conversion de type. L'imputation
aura lieu en phase 7, dans un `Pipeline` ajusté sur le seul jeu d'entraînement.

## Comparatif avant et après

| Métrique | Avant | Après | Variation | Variation (%) |
|---|---|---|---|---|
| lignes | 104544 | 92616 | -11928 | -11.4 |
| colonnes | 165 | 66 | -99 | -60.0 |
| parties | 52272 | 46308 | -5964 | -11.4 |
| valeurs_manquantes | 2782881 | 52703 | -2730178 | -98.1 |
| doublons_exacts | 0 | 0 | 0 | nan |

88.6 % des lignes équipe et
88.6 % des parties sont
conservées.

## Journal des transformations

| # | Colonne | Problème | Action | Lignes affectées | Justification |
|---|---|---|---|---|---|
| 1 | toutes | Doublons exacts | Aucune suppression nécessaire | 0 | Aucun doublon exact ni doublon de clé sur les lignes à clé renseignée, vérifié plutôt que supposé |
| 2 | result | Partie sans vainqueur, result à 0 des deux côtés | Suppression des parties entières, par paires | 6 | Cible inexistante, lignes inutilisables en apprentissage supervisé. Suppression par paires pour préserver l'équilibre 50/50 |
| 3 | 105 colonnes | Information postérieure à l'instant de prédiction | Suppression de colonnes | 0 | Colonnes de fin de partie contenant le résultat, colonnes de ligne joueur vides sur les lignes équipe, et métadonnées sans valeur prédictive |
| 4 | playoffs, firstblood, firstdragon, firstherald, result | Booléens stockés en flottant | Conversion en entier nullable Int64, et result en int8 | 0 | Int64 accepte les valeurs manquantes sans les remplacer, contrairement à int. Aucune imputation n'est donc introduite par la conversion |
| 5 | teamname | Espaces superflus en bordure | Suppression des espaces de bordure, casse laissée intacte | 0 | Abaisser la casse fusionnerait des organisations distinctes. teamname ne sera de toute façon jamais une feature, il sert aux variables de forme |
| 6 | saison | year est une étiquette de saison, pas une année civile | Création de saison à partir de l'année de la date | 0 | Garantit un découpage strictement chronologique et n'abandonne aucune ligne hors du train comme du test. year est conservée pour l'analyse |
| 7 | region, tier_ligue, franchisee, confiance | league ne survit pas à la réorganisation du circuit en 2025 | Jointure du référentiel des ligues, validate=many_to_one | 0 | region et tier_ligue sont stables dans le temps et remplacent league comme features. La validation empêche toute duplication silencieuse |
| 8 | goldat15, xpat15, csat15, golddiffat15, xpdiffat15 | Snapshot à 15 minutes absent | Suppression des parties entières dont une des deux lignes est incomplète | 11922 | Critère mesuré, et non un nom de ligue. Suppression par paires pour préserver l'équilibre 50/50 de la cible. Aucune imputation |
| 9 | split, teamname, teamid | Catégories manquantes | Valeur constante explicite 'Inconnu' | 0 | Le guide interdit l'imputation par le mode. 'Inconnu' conserve l'information de l'absence au lieu d'inventer une modalité plausible |
| 10 | golddiffat15 | Valeurs extrêmes détectées par l'IQR | Drapeau flag_ecart_or_extreme, aucune ligne supprimée ni modifiée | 0 | Vraies parties déséquilibrées, pas des erreurs. Les supprimer retirerait les parties les plus prévisibles. La winsorization est interdite à ce stade |

## La fuite de données, chantier principal de cette phase

Oracle's Elixir est un export de fin de partie : 97 de ses colonnes sont
postérieures à la minute 15, auxquelles s'ajoutent 9 colonnes de ligne
joueur vides sur les lignes équipe et 2 métadonnées sans valeur
prédictive.

### Cinq colonnes découvertes en phase 3

La liste héritée du cadrage était incomplète. Un contrôle empirique, la corrélation absolue de
chaque colonne survivante avec la cible, a révélé cinq oublis. Le seuil de jugement :
`golddiffat15` est le signal légitime le plus fort disponible à la minute 15 et corrèle à
0,535. Toute colonne qui corrèle davantage contient le résultat au lieu de le prédire.

| Colonne | Corrélation | Nature |
|---|---|---|
| `damagetotowers` | 0,760 | Dégâts aux tourelles sur toute la partie |
| `team kpm` | 0,679 | Éliminations par minute, calculé en fin de partie |
| `elementaldrakes` | 0,586 | Dragons élémentaires pris sur toute la partie |
| `opp_elementaldrakes` | 0,586 | Idem, côté adverse |
| `ckpm` | 0,000 | Symétrique donc non corrélée, mais taux de fin de partie |

`ckpm` illustre la limite du détecteur : sa corrélation est nulle parce qu'elle vaut la même
chose pour les deux équipes. Elle ne trahit pas le gagnant, mais reste inconnue à la minute 15.
La corrélation est un outil utile, pas un critère suffisant.

### `firsttower` écarté, contre le cadrage

Le cadrage classait `firsttower` parmi les colonnes connues à la minute 15, et la feature
`objectifs_precoces` devait sommer quatre objectifs. Deux mesures contredisent ce classement.

`firsttower` est attribué dans 100 % des parties, alors que `firstblood`, `firstdragon` et
`firstherald` laissent des parties sans attribution. Un drapeau qui trouve toujours un titulaire
décrit la partie entière, pas un état à un instant donné. Et en jeu professionnel la première
tourelle tombe couramment après la quinzième minute, puisque les plaques ne disparaissent qu'à
la quatorzième.

Sa corrélation le confirme : 0,391 contre 0,18 à 0,25 pour les trois autres objectifs.

**Décision : `firsttower` rejoint les colonnes de fuite.** `objectifs_precoces` sommera trois
objectifs et vaudra 0 à 3. Divergence assumée avec le cadrage, motivée par une mesure.

Les trois objectifs conservés sont aussi des drapeaux de partie entière, mais le risque est
faible : le héraut disparaît de la carte à la quatorzième minute, donc `firstherald` est
nécessairement résolu avant l'instant de prédiction.

### Contrôle final

Après nettoyage, la corrélation la plus forte avec la cible est celle de `golddiffat15`
(0.535), et 0 colonne la dépasse. Ce contrôle sera rejoué en phase 7 :
si un modèle atteint 90 % d'exactitude, c'est ici qu'il faudra revenir.

## Deux autres décisions issues du diagnostic

**`turretplates` retirée des features.** Son échelle change exactement sur la frontière du
split : maximum de 15 jusqu'en 2025, 45 en 2026, au-dessus de 15 sur 61 % des lignes. Un scaler
ajusté sur l'entraînement projetterait 2026 hors de la plage apprise. La colonne reste dans le
jeu de données pour l'analyse de phase 5, mais sort de `NUMERIC_FEATURES`.

**`split` retirée des features.** 32 modalités, 19,8 % de valeurs manquantes et 3 modalités
présentes uniquement en 2026. `playoffs` porte la même opposition sous une forme binaire stable.

## Outliers, décision de ne pas agir

Les écarts d'or extrêmes sont de vraies parties déséquilibrées, pas des erreurs. Les supprimer
retirerait du jeu les parties les plus faciles à prédire et ferait chuter artificiellement la
performance mesurée. La winsorization est de toute façon interdite à ce stade.

Stratégie retenue : drapeau `flag_ecart_or_extreme` et conservation, pour permettre une analyse
séparée en phase 5.

## Contrôles de validation

| Contrôle | Statut |
|---|---|
| Aucun doublon exact | ok |
| Deux lignes équipe par partie, sans exception | ok |
| Un vainqueur unique par partie | ok |
| Cible parfaitement équilibrée | ok |
| Aucune valeur manquante sur les colonnes requises à 15 minutes | ok |
| Aucune colonne de fuite résiduelle | ok |
| Aucune corrélation au-dessus du plafond golddiffat15 | ok |
| region et tier_ligue entièrement renseignées | ok |
| Dates toujours au bon type | ok |
| patch toujours en texte | ok |
| Données originales intactes | ok |
| Aucune imputation statistique réalisée | ok |

## Réponses aux questions de réflexion

**La décision la plus difficile.** Écarter `firsttower`. Elle contredit le cadrage, elle ampute
une feature prévue, et la colonne semble légitime au premier regard. C'est le taux
d'attribution de 100 % qui a tranché : un objectif qui trouve toujours un titulaire ne décrit
pas un instant, il décrit une partie.

**La perte d'information.** 11,928 lignes équipe supprimées, soit
11.4 %. La quasi-totalité vient de l'absence de
snapshot à 15 minutes, qui rend la ligne inutilisable par construction. Le biais introduit est
réel et documenté : les ligues mineures sont surreprésentées parmi les parties écartées, donc le
jeu final penche vers les circuits les mieux instrumentés. C'est à énoncer en soutenance.

**La reproductibilité.** Le notebook s'exécute de bout en bout depuis un noyau neuf, ne modifie
jamais `data/raw/`, et écrit son journal en JSON. Un tiers qui le relance obtient le même
résultat, aux mises à jour quotidiennes de la source près.

**Ce que je referais autrement.** Le contrôle de corrélation avec la cible aurait dû être fait
dès la phase 2. Il a détecté cinq colonnes de fuite que la liste écrite à la main avait
manquées, pour un coût d'une ligne de code. Sur ce type de source, un export de fin de partie,
il devrait être systématique et précéder toute liste rédigée de mémoire.
