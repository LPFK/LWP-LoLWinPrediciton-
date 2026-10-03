# Rapport de modelisation, phase 7

Document genere par `notebooks/07_modelisation.ipynb`, a ne pas editer a la main.

Donnees fournies par Oracle's Elixir (Tim Sevenhuysen, oracleselixir.com).

## Cadrage

| Element | Valeur |
|---|---|
| Question predictive | Quelle equipe gagne, sachant l'etat de jeu a la 15e minute |
| Cible | `result`, classification binaire, 50.0 % de positifs |
| Features | 23 colonnes, toutes connues a la 15e minute |
| Metrique principale | ROC AUC |
| Metriques secondaires | accuracy pour la communication, log loss pour la calibration |
| Entrainement | 76 070 lignes, 2022 a 2025 |
| Test | 16 546 lignes, saison 2026, ouvert une seule fois |
| Graine aleatoire | 42, fixee partout |

## Ecarts assumes au squelette du formateur

| Squelette | Ce projet | Justification |
|---|---|---|
| `train_test_split` aleatoire | Split chronologique sur la date | Le modele sert a predire des parties futures, un split aleatoire entrainerait sur des parties posterieures a celles qu'il evalue |
| `cv=5`, donc `KFold` | `TimeSeriesSplit(n_splits=5)` | Un `KFold` remelange l'ordre temporel dans le train et reproduit a petite echelle le probleme que le split chronologique corrige |
| Jeu de validation separe | Les cinq plis de `TimeSeriesSplit` | Chaque pli valide sur des parties posterieures a son entrainement, cinq fois au lieu d'une |

## Baselines, mesurees avant tout modele

| modele | accuracy | roc_auc | log_loss |
|---|---|---|---|
| Naive, classe majoritaire | 0.5 | 0.5 | 0.6931 |
| Metier 1, le cote bleu gagne | 0.5293 | nan | nan |
| Metier 2, le plus riche a 15 gagne | 0.7387 | nan | nan |

La baseline economique atteint 73.87 % sur l'entrainement. C'est la
reference qui compte : une regle d'une ligne capture deja l'essentiel du signal, ce que la
phase 6 avait annonce en montrant que 28 % des lignes presentent plus de 3 000 or d'ecart.

## Comparaison des modeles, validation croisee temporelle

| famille | hyperparametres | mean_test_roc_auc | mean_test_accuracy | log_loss |
|---|---|---|---|---|
| LogisticRegression | {'C': 0.05} | 0.8362 | 0.7525 | 0.4959 |
| RandomForestClassifier | {'max_depth': 10, 'min_samples_leaf': 5} | 0.8337 | 0.7496 | 0.5007 |
| HistGradientBoostingClassifier | {'learning_rate': 0.05} | 0.8332 | 0.75 | 0.5002 |

Modele retenu : **LogisticRegression**, AUC de 0.8362 en validation croisee.
Ecart d'AUC entre la meilleure et la moins bonne famille : 0.0030.

## Diagnostic de surapprentissage

Taille d'un pli de validation : 12 678 lignes.

| famille | mean_train_roc_auc | mean_test_roc_auc | ecart_auc | lignes_concernees |
|---|---|---|---|---|
| LogisticRegression | 0.8391 | 0.8362 | 0.003 | 38.0 |
| RandomForestClassifier | 0.8797 | 0.8337 | 0.046 | 584.0 |
| HistGradientBoostingClassifier | 0.8632 | 0.8332 | 0.03 | 381.0 |

## Verdict final, saison 2026

| modele | accuracy | roc_auc | log_loss |
|---|---|---|---|
| Baseline naive | 0.5 | 0.5 | 0.6931 |
| Baseline cote bleu | 0.5392 | nan | nan |
| Baseline plus riche a 15 | 0.7448 | nan | nan |
| Modele final, LogisticRegression | 0.7587 | 0.8438 | 0.4874 |

Gain du modele sur la baseline economique : +1.38 points d'accuracy, soit
229 lignes mieux classees sur 16 546.

Ecart entrainement / test : -0.0072 d'AUC et
-0.0055 d'accuracy, soit
91 lignes du jeu de test.

## Comparaison des protocoles de split

| protocole | accuracy | roc_auc |
|---|---|---|
| Chronologique, test 2026 | 0.7587 | 0.8438 |
| Aleatoire, meme taille | 0.7511 | 0.8353 |

Le split aleatoire affiche -0.85 points d'AUC par rapport au split
chronologique, soit l'inverse de ce que la phase 0 anticipait.

L'explication n'est pas que le split aleatoire serait vertueux, mais que les deux protocoles
n'evaluent pas sur la meme population. Le test chronologique ne contient que 2026, une saison
homogene ; le test aleatoire tire ses lignes des cinq saisons, y compris les plus anciennes et
les plus heterogenes, et il est donc mecaniquement plus difficile. L'effet de composition
l'emporte ici sur l'effet d'optimisme.

Le choix du split chronologique ne se justifie donc pas par le score, il se justifie par la
condition d'usage : le modele servira a predire des parties futures, et c'est cela qu'il faut
simuler, que le score y gagne ou y perde.

## Interpretation

Coefficients de la regression logistique, variables standardisees, dix premiers en valeur
absolue :

| feature | coefficient |
|---|---|
| num__golddiffat15 | 0.6937 |
| bool__firstdragon | 0.3667 |
| num__xpdiffat15 | 0.3138 |
| num__ecart_or_normalise | 0.2875 |
| num__csdiffat15 | 0.2686 |
| num__forme_equipe_10_derniers | 0.2436 |
| bool__firstblood | -0.2139 |
| num__diff_kills_at15 | 0.2135 |
| num__objectifs_precoces | 0.2096 |
| cat__region_International | -0.1618 |

Prediction laissee par la phase 6, `firstdragon` devant `firstblood` : **confirmee**.
`firstdragon` au rang 2, `firstblood` au rang 7.

## Biais, lien avec le bloc 7

Performance par region, groupes de plus de 300 lignes :

| region | lignes | accuracy | roc_auc | log_loss |
|---|---|---|---|---|
| Asie-Pacifique | 1816 | 0.7819 | 0.8771 | 0.4351 |
| Turquie | 408 | 0.7843 | 0.8757 | 0.4406 |
| Europe | 6728 | 0.7626 | 0.8479 | 0.4826 |
| Coree | 2486 | 0.7574 | 0.8377 | 0.4981 |
| Moyen-Orient | 660 | 0.7212 | 0.8338 | 0.4922 |
| Ameriques | 2700 | 0.753 | 0.8336 | 0.5024 |
| Chine | 1052 | 0.7367 | 0.8139 | 0.5335 |
| International | 696 | 0.7399 | 0.8116 | 0.5276 |

Ecart d'AUC entre la meilleure et la moins bonne region :
0.0655.

Performance par niveau de ligue :

| tier_ligue | lignes | accuracy | roc_auc | log_loss |
|---|---|---|---|---|
| 2 | 8134 | 0.7729 | 0.8621 | 0.4598 |
| 3 | 3944 | 0.7632 | 0.8432 | 0.4915 |
| 1 | 4468 | 0.7287 | 0.8079 | 0.5341 |

Deux constats a signaler.

Le modele est le **moins performant sur le tier 1**, ce qui est coherent avec la phase 5 : elle
avait mesure que le tier 1 est marginalement le moins deterministe, avec un taux de remontee de
19,9 % contre 18,5 % en tier 2. Les meilleures equipes renversent un peu plus souvent une partie
mal engagee, donc l'etat de jeu a la 15e minute y predit un peu moins bien. Le modele retrouve
sans qu'on le lui demande un resultat etabli deux phases plus tot par une methode differente.

La **Chine** obtient la plus mauvaise AUC regionale. La regle de completude de la phase 3 avait
ecarte presque toute la LPL des saisons 2022 a 2025, alors qu'Oracle's Elixir renseigne les
colonnes a 15 minutes en 2026 : le modele predit une region qu'il n'a pratiquement jamais vue a
l'entrainement. C'est une limite du perimetre et non un defaut du modele, et un deploiement reel
exigerait de reentrainer des que la LPL est disponible en volume.

## Limite structurelle du cadrage

Le modele predit une ligne equipe a la fois et ignore que deux lignes forment une partie. Les
deux probabilites d'une meme partie ne somment donc a 1 qu'approximativement, ce qui se verrait
sur un affichage temps reel. Une mise en production normaliserait les deux probabilites, ou
reformulerait le probleme au niveau de la partie avec des features en difference.

## Livrables

- `models/pipeline_final.joblib`, pipeline complete, preprocessing inclus
- `figures/07_courbe_roc.png`
- `figures/07_calibration.png`
- `figures/07_matrice_confusion.png`
- `figures/07_coefficients_logistique.png`
