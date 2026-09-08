# Data dictionary

Dataset final : `data/processed/lol_at15.parquet`

Document généré par `notebooks/04_transformation.ipynb`, à ne pas éditer à la main.

Une ligne est une équipe dans une partie. Deux lignes par partie, identifiées par `gameid`
plus `side`.

| Propriété | Valeur |
|---|---|
| Lignes | 92,616 |
| Colonnes | 49 |
| Parties | 46,308 |
| Période | 2022-01-10 au 2026-09-06 |
| Cible | `result`, équilibrée à 50.0 % |
| Entraînement | 76,070 lignes, avant le 2026-01-01 |
| Test | 16,546 lignes |

## Instant de prédiction

Toutes les colonnes de ce dataset sont connues à la **minute 15**. Les colonnes postérieures
ont été supprimées en phase 3, liste `config.LEAKY_COLUMNS`, et le rapport de nettoyage détaille
les cinq oublis rattrapés par un contrôle de corrélation.

## Features historiques et fuite temporelle

Cinq colonnes regardent le passé : `forme_equipe_10_derniers`, `experience_roster`,
`winrate_champion_patch`, `mediane_or_patch` et `ecart_or_normalise` qui en dérive.

Toutes sont calculées en fenêtre expansive sur les parties **antérieures** uniquement, triées
par date, au moyen d'un `shift(1)` ou d'un `cumcount`. Le code est dans `src/features.py`, et
l'audit de la section 5.5 du notebook vérifie qu'aucune n'est renseignée sur la première partie
d'un groupe.

Leurs valeurs manquantes sont des amorçages et ne sont **pas** imputées ici. L'imputation aura
lieu dans le `Pipeline` de la phase 7, ajusté sur le seul jeu d'entraînement.

## Colonnes

| Colonne | Type | Description | Source | Transformation | Feature modèle | Manquant (%) |
|---|---|---|---|---|---|---|
| `gameid` | string | Identifiant de la partie | Oracle's Elixir | brute | non | 0.0 |
| `teamid` | object | Identifiant de l'équipe, Inconnu si absent | Oracle's Elixir | nettoyée | non | 0.0 |
| `team_key` | object | Clé d'équipe, teamid ou teamname en repli | Dérivée | construite | non | 0.0 |
| `teamname` | object | Nom de l'équipe | Oracle's Elixir | nettoyée | non | 0.0 |
| `date` | datetime64[ns] | Date et heure de la partie | Oracle's Elixir | parsée format explicite | non | 0.0 |
| `saison` | int32 | Année civile de la date, porte le split | Dérivée | construite | non | 0.0 |
| `league` | object | Code de la ligue, analyse seulement | Oracle's Elixir | brute | non | 0.0 |
| `patch` | string | Version du jeu, texte | Oracle's Elixir | brute | non | 0.0 |
| `result` | int8 | Cible, 1 si l'équipe gagne | Oracle's Elixir | brute | non | 0.0 |
| `golddiffat15` | float64 | Écart d'or à 15 minutes | Oracle's Elixir | brute | oui | 0.0 |
| `xpdiffat15` | float64 | Écart d'expérience à 15 minutes | Oracle's Elixir | brute | oui | 0.0 |
| `csdiffat15` | float64 | Écart de sbires à 15 minutes | Oracle's Elixir | brute | oui | 0.0 |
| `diff_kills_at15` | float64 | killsat15 moins opp_killsat15 | Dérivée | calculée | oui | 0.0 |
| `deathsat15` | float64 | Morts de l'équipe à 15 minutes | Oracle's Elixir | brute | oui | 0.0 |
| `objectifs_precoces` | Int64 | firstblood plus firstdragon plus firstherald, 0 à 3 | Dérivée | calculée | oui | 0.0 |
| `compo_nb_tank` | int32 | Champions taggés Tank parmi les 5 | Data Dragon | construite | oui | 0.0 |
| `compo_nb_mage` | int32 | Champions taggés Mage parmi les 5 | Data Dragon | construite | oui | 0.0 |
| `compo_nb_marksman` | int32 | Champions taggés Marksman parmi les 5 | Data Dragon | construite | oui | 0.0 |
| `compo_nb_fighter` | int32 | Champions taggés Fighter parmi les 5 | Data Dragon | construite | oui | 0.0 |
| `profil_degats` | float64 | Part de champions AD parmi AD plus AP, 0 à 1 | Data Dragon | construite | oui | 0.0 |
| `forme_equipe_10_derniers` | float64 | Taux de victoire sur les 10 parties précédentes | Dérivée | fenêtre expansive, passé seul | oui | 1.5 |
| `experience_roster` | int64 | Parties déjà jouées par ce cinq | Dérivée | cumcount, passé seul | oui | 0.0 |
| `winrate_champion_patch` | float64 | Taux de victoire moyen des 5 champions sur le patch, parties antérieures | Dérivée | fenêtre expansive, passé seul | oui | 0.46 |
| `ecart_or_normalise` | float64 | golddiffat15 divisé par la médiane d'or du patch | Dérivée | fenêtre expansive, passé seul | oui | 2.3 |
| `patch_seq` | int64 | Rang du patch dans sa saison | Dérivée | construite | oui | 0.0 |
| `side` | string | Côté de la carte, Blue ou Red | Oracle's Elixir | brute | oui | 0.0 |
| `region` | object | Région du circuit | Référentiel XLSX | jointure | oui | 0.0 |
| `tier_ligue` | int64 | Niveau de ligue, 1 à 3 | Référentiel XLSX | jointure | oui | 0.0 |
| `playoffs` | Int64 | Phase finale ou saison régulière | Oracle's Elixir | brute | oui | 0.0 |
| `firstblood` | Int64 | Premier sang obtenu | Oracle's Elixir | brute | oui | 0.0 |
| `firstdragon` | Int64 | Premier dragon obtenu | Oracle's Elixir | brute | oui | 0.0 |
| `firstherald` | Int64 | Premier héraut obtenu | Oracle's Elixir | brute | oui | 0.0 |
| `is_playoffs` | int32 | Copie entière de playoffs | Dérivée | calculée | non | 0.0 |
| `mois` | int32 | Mois de la partie, analyse seulement | Dérivée | construite | non | 0.0 |
| `year` | int64 | Étiquette de saison d'Oracle's Elixir, analyse seulement | Oracle's Elixir | brute | non | 0.0 |
| `patch_major` | Int64 | Partie majeure du patch, analyse seulement | Dérivée | construite | non | 0.0 |
| `patch_minor` | Int64 | Partie mineure du patch, analyse seulement | Dérivée | construite | non | 0.0 |
| `compo_nb_assassin` | int32 | Champions taggés Assassin parmi les 5 | Data Dragon | construite | non | 0.0 |
| `compo_nb_support` | int32 | Champions taggés Support parmi les 5 | Data Dragon | construite | non | 0.0 |
| `turretplates` | float64 | Plaques prises, hors features car l'échelle change en 2026 | Oracle's Elixir | brute | non | 0.1 |
| `flag_ecart_or_extreme` | bool | Écart d'or hors bornes IQR | Dérivée | drapeau | non | 0.0 |
| `confiance` | object | Fiabilité du classement de la ligue | Référentiel XLSX | jointure | non | 0.0 |
| `franchisee` | bool | Ligue franchisée | Référentiel XLSX | jointure | non | 0.0 |
| `mediane_or_patch` | float64 | Médiane d'or à 15 sur les parties antérieures du patch | Dérivée | fenêtre expansive, passé seul | non | 2.3 |
| `roster_key` | object | Identifiant du cinq de départ | Dérivée | construite | non | 0.0 |
| `goldat15` | float64 | Or de l'équipe à 15 minutes | Oracle's Elixir | brute | non | 0.0 |
| `opp_goldat15` | float64 | Or adverse à 15 minutes | Oracle's Elixir | brute | non | 0.0 |
| `xpat15` | float64 | Expérience de l'équipe à 15 minutes | Oracle's Elixir | brute | non | 0.0 |
| `csat15` | float64 | Sbires de l'équipe à 15 minutes | Oracle's Elixir | brute | non | 0.0 |

## Colonnes volontairement absentes des features

| Colonne | Raison |
|---|---|
| `league`, `year`, `patch_major` | Modalités qui ne survivent pas à la frontière 2025/2026 |
| `split` | 32 modalités, 19,8 % de manquants, 3 absentes du train |
| `turretplates` | Échelle qui change en 2026, maximum de 15 à 45 |
| `firsttower` | Drapeau de fin de partie, écarté pour fuite en phase 3 |
| `teamname`, `teamid`, `roster_key` | Identifiants, servent aux features de forme uniquement |
| `mois` | Aucun sens prédictif, conservée pour l'analyse de phase 5 |
