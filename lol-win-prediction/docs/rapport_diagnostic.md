# Rapport de diagnostic qualité

Phase 2 du projet final Machine Learning. Document généré par
`notebooks/02_eda_diagnostique.ipynb`, à ne pas éditer à la main.

Périmètre : lignes équipe d'Oracle's Elixir, saisons 2022 à 2026.
Volume analysé : 104,544 lignes équipe, 52,272 parties, 165 colonnes.

## Score de qualité global

**3.4 / 5**

| Dimension | Note sur 5 | Principaux problèmes | Priorité |
|---|---|---|---|
| Complétude | 3 | 11.4 % des lignes équipe sans snapshot à 15 min, 17 colonnes au-dessus de 30 % de manquants | haute |
| Unicité | 5 | Aucun doublon, structure parfaite. Seule réserve : 1,800 lignes sans teamid | basse |
| Cohérence | 3 | split ingérable (32 modalités, 3 absentes du train). year est une étiquette de saison, pas une année civile. Arithmétique interne parfaite | haute |
| Exactitude | 2 | turretplates change d'échelle en 2026 (max 15 vers 45) sur la frontière du split, 3 parties sans vainqueur | haute |
| Fraîcheur | 4 | Source à jour et sans trou mensuel, mais 2026 est tronquée au 6 septembre, sans Worlds | moyenne |

## 1. Complétude

88.6 % des lignes équipe disposent d'un snapshot complet à la minute 15,
sur les colonnes `goldat15`, `xpat15`, `csat15`, `golddiffat15`, `xpdiffat15`.

La règle d'inclusion retenue en phase 0 impose que **les deux** lignes d'une partie soient
complètes, faute de quoi la partie entière est écartée. Supprimer une ligne isolée
déséquilibrerait la cible, dont le 50/50 est la propriété la plus utile de ce jeu de données.

| Mesure | Valeur |
|---|---|
| Lignes équipe complètes | 92,616 |
| Lignes équipe incomplètes | 11,928 |
| Parties entièrement exploitables | 46,308 sur 52,272 |
| Lignes réellement perdues, par paires | 11,928 |
| Surcoût de la règle des deux lignes | 0 lignes |

17 colonnes dépassent 30 % de valeurs manquantes,
dont 9 sont vides à 100 %. Ces dernières ne sont pas un défaut : ce sont des champs de
ligne joueur, structurellement absents des lignes équipe.

L'incomplétude n'est pas aléatoire, elle se concentre par ligue et par saison. Voir
`figures/02_completude_at15_ligue_saison.png`.

| Ligue | Lignes | Complétude at15 (%) | Lignes perdues |
|---|---|---|---|
| LPL | 7432 | 14.2 | 6377 |
| LDL | 4704 | 0.0 | 4704 |
| ASCI | 300 | 0.0 | 300 |
| DCup | 424 | 35.4 | 274 |
| MSI | 770 | 79.7 | 156 |
| WLDs | 1040 | 90.0 | 104 |
| LEC | 2988 | 99.9 | 3 |
| ESLOL | 1666 | 99.9 | 2 |

Cela confirme la décision de phase 0 : filtrer sur la disponibilité **mesurée** du snapshot,
jamais sur le nom d'une ligue.

Aucune imputation n'est réalisée à ce stade, conformément au guide. Elle interviendra en
phase 7, dans un `Pipeline` ajusté sur le seul jeu d'entraînement.

## 2. Unicité

| Contrôle | Résultat |
|---|---|
| Lignes dupliquées à l'identique | 0 |
| Doublons sur gameid + teamid, clé renseignée | 0 |
| Parties n'ayant pas exactement 2 lignes équipe | 0 |
| Parties n'ayant pas exactement 10 lignes joueur | 0 |
| Lignes sans teamid | 1,800 |

Dimension la plus saine du jeu de données. Piège méthodologique à signaler : `duplicated`
traite deux `NaN` comme égaux, si bien qu'un test naïf sur `gameid` + `teamid` remonte
325 faux doublons, qui sont en réalité des parties valides opposant deux équipes
distinctes dépourvues d'identifiant.

## 3. Cohérence

L'arithmétique interne est exacte : `golddiffat15`, `xpdiffat15` et `csdiffat15` valent toujours
la différence entre les deux camps, et les deux lignes d'une partie sont bien le miroir l'une de
l'autre. La source est fiable sur ce plan, et `golddiffat15` est donc redondant avec le couple
`goldat15` et `opp_goldat15`.

Deux problèmes réels.

**La colonne `split` ne survit pas au split chronologique.** 32 modalités,
19.8 % de valeurs manquantes, et 3 modalités
présentes en 2026 mais absentes de l'entraînement (Lock-In, Rounds 3-4, Versus).
`OneHotEncoder(handle_unknown="ignore")` les encoderait en bloc de zéros, donc perdrait
l'information sans lever d'erreur. Action : retirer `split` de `CATEGORICAL_FEATURES` et
conserver `playoffs`.

**`year` est une étiquette de saison, pas une année civile.** 2,712 lignes
(2.6 %) portent un `year` différent de l'année de leur
date. Ce ne sont pas des erreurs : ces parties se jouent entre septembre et décembre et portent
l'étiquette de la saison suivante, parce que les circuits ouvrent leur saison à l'automne
précédent. À cela s'ajoutent 10 lignes étiquetées 2027.

Le défaut n'est donc pas dans la colonne mais dans l'usage qu'on voudrait en faire. Découper sur
`year` reviendrait à découper sur une étiquette de compétition alors que l'objectif est un
découpage chronologique : des parties de décembre 2025 basculeraient dans le test tandis que des
parties postérieures resteraient dans l'entraînement, rompant l'ordre temporel là même où on
cherche à le garantir. Action : **découper sur la date**, frontière au 1er janvier 2026.

## 4. Exactitude

Dimension la plus faible, et porteuse du risque principal du projet.

**`turretplates` change d'échelle exactement sur la frontière du split.** Le maximum théorique
est de 15, soit trois tourelles extérieures à cinq plaques. De 2022 à 2025 la colonne le
respecte. En 2026 elle atteint 45 et dépasse 15 sur 61 %
des lignes.

Cette colonne figurait dans `config.NUMERIC_FEATURES` au moment du diagnostic, et la phase 3
l'en a retirée sur la base de ce constat. Un modèle entraîné sur 2022-2025 n'a jamais
vu de telles valeurs, et un `StandardScaler` ajusté sur ces saisons projetterait 2026 hors de la
plage apprise. Le modèle ne planterait pas, il se tromperait en silence sur toute la saison de
test. Action : retirer la colonne des features.

**Dérive de méta.** L'or, l'expérience et les sbires à 15 minutes progressent de 7 à 10 % entre
l'entraînement et le test. Ce n'est pas une erreur mais une évolution réelle du jeu. Elle
justifie le split chronologique, qu'un split aléatoire aurait masqué, et motive la feature
`ecart_or_normalise` prévue en phase 4.

**Outliers.** Les valeurs extrêmes d'écart d'or sont de vraies parties déséquilibrées. Décision
assumée : aucun retrait, sous peine de supprimer les parties les plus faciles à prédire et de
dégrader artificiellement la performance mesurée.

**3 parties n'ont aucun vainqueur**, leurs deux lignes portant `result` à 0. Six
lignes à supprimer par paires.

Contrôle rassurant : aucune des 10 parties de moins de quinze minutes ne porte de
snapshot à quinze minutes. La source n'invente pas de données.

## 5. Fraîcheur

| Mesure | Valeur |
|---|---|
| Première partie | 2022-01-10 |
| Dernière partie | 2026-09-06 |
| Retard de la source | 0 jour(s) |
| Mois sans aucune partie | 0 |

La source est à jour et sans trou mensuel. En revanche **la saison de test est tronquée** : 2026
s'arrête au 6 septembre, alors que les saisons d'entraînement vont jusqu'en novembre ou
décembre. Il manque la fin de saison et les Worlds.

Deux conséquences à annoncer en soutenance. Le jeu de test est plus petit qu'une saison
complète, ce qui élargit l'intervalle de confiance des scores. Et il penche vers la saison
régulière, alors que les saisons d'entraînement contiennent leurs phases finales.

## 6. Priorisation des corrections

| Problème | Impact | Difficulté | Priorité | Action retenue | Phase |
|---|---|---|---|---|---|
| 3 parties sans vainqueur | eleve | facile | 1 | Supprimer les 6 lignes par paires | 3 |
| Colonnes post-partie omniprésentes | eleve | facile | 1 | Supprimer config.LEAKY_COLUMNS | 3 |
| Snapshot at15 absent sur 11 % des lignes | eleve | facile | 1 | Supprimer les parties par paires (quality.drop_incomplete_games) | 3 |
| split ne survit pas à la frontière | eleve | facile | 1 | Retirer split de CATEGORICAL_FEATURES, garder playoffs | 3 |
| turretplates change d'échelle en 2026 | eleve | facile | 1 | Retirer la colonne de NUMERIC_FEATURES | 3 |
| year est une étiquette de saison, pas une année civile | eleve | facile | 1 | Découper sur la date au 1er janvier 2026, jamais sur year | 3 |
| 2026 tronquée, sans Worlds | eleve | difficile | 2 | Non corrigeable, à énoncer comme limite d'évaluation | 9 |
| Dérive de méta sur l'or et l'expérience | eleve | difficile | 2 | Construire ecart_or_normalise, rapporté à la médiane du patch | 4 |
| Région CEI réduite à 32 lignes | faible | facile | 3 | Regrouper les régions rares | 4 |
| teamid manquant sur 1,800 lignes | faible | facile | 3 | Se rabattre sur teamname pour les variables de forme | 4 |
| Outliers d'écart d'or | faible | difficile | 4 | Ne rien faire, ce sont de vraies parties déséquilibrées | 3 |

Les chantiers de priorité 1 sont tous à fort impact et faciles à corriger. Ils tiennent en
quelques filtres de phase 3 et lèvent l'essentiel du risque.

## 7. Réponses aux questions de réflexion

**Le problème le plus surprenant.** Le changement d'échelle de `turretplates` en 2026. Une
colonne d'apparence anodine, dont la définition change précisément à la frontière entre
l'entraînement et le test, et qui aurait dégradé le modèle sans provoquer la moindre erreur.
C'est le type de défaut qu'un contrôle de valeurs manquantes ne voit pas et qu'un contrôle de
bornes métier attrape immédiatement.

**Le problème à corriger en priorité.** Les colonnes post-partie. Elles sont majoritaires parmi
les 165 colonnes et contiennent le résultat, directement ou non. Les laisser passer produirait
un modèle à plus de 95 % d'exactitude, sans aucune valeur, et plafonnerait la phase de
modélisation à 8 sur 25.

**L'origine des problèmes.** Presque tous viennent de la collecte et de l'évolution du jeu, pas
d'erreurs de saisie. Le snapshot manquant reflète l'absence d'instrumentation sur certaines
ligues mineures. Le changement de `turretplates` suit une modification des règles du jeu. Les
modalités de `split` reflètent l'organisation propre à chaque circuit. La seule erreur
véritable est celle des trois parties sans vainqueur.

**Ce qui ne sera pas corrigé.** Les outliers d'écart d'or, parce que ce sont de vraies parties.
Les noms d'équipe multiples pour un même identifiant, parce que `teamname` n'est jamais une
feature. Et la troncature de 2026, parce qu'elle n'est pas corrigeable : elle sera énoncée
comme une limite de l'évaluation.
