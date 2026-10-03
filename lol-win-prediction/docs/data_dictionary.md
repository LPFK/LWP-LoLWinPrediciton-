# Data dictionary

Dataset final : `data/processed/lol_at15.parquet`

Document genere par `notebooks/04_transformation.ipynb`, a ne pas editer a la main.

Une ligne est une equipe dans une partie. Deux lignes par partie, identifiees par `gameid`
plus `side`.

## Informations generales

| Attribut | Valeur |
|---|---|
| Nom du fichier | `lol_at15.parquet` |
| Format | Parquet, compression par defaut de pyarrow |
| Encodage | UTF-8 |
| Lignes | 92 616 |
| Colonnes | 49 |
| Parties | 46 308 |
| Date de generation | 2026-09-08 |
| Periode couverte | 2022-01-10 au 2026-09-06 |
| Auteur | Projet final Machine Learning, Master 1, blocs 6 et 8 |
| Cible | `result`, equilibree a 50.0 % |
| Entrainement | 76 070 lignes, avant le 2026-01-01 |
| Test | 16 546 lignes |

## Sources de donnees

| Source | Format original | Description |
|---|---|---|
| Oracle's Elixir 2022-2026 | CSV, un fichier par saison | Statistiques du circuit professionnel, 12 lignes par partie dont 2 lignes equipe. Attribution demandee a Tim Sevenhuysen, oracleselixir.com |
| Riot Data Dragon | JSON | Tags de chaque champion, utilises pour construire les variables de composition |
| Referentiel des ligues | XLSX construit a la main | Tier et region de chacun des 84 codes ligue observes, avec une colonne de confiance |

## Instant de prediction

Toutes les colonnes de ce dataset sont connues a la **minute 15**. Les colonnes posterieures
ont ete supprimees en phase 3, liste `config.LEAKY_COLUMNS`, et le rapport de nettoyage detaille
les cinq oublis rattrapes par un controle de correlation.

## Features historiques et fuite temporelle

Cinq colonnes regardent le passe : `forme_equipe_10_derniers`, `experience_roster`,
`winrate_champion_patch`, `mediane_or_patch` et `ecart_or_normalise` qui en derive.

Toutes sont calculees en fenetre expansive sur les parties **anterieures** uniquement, triees
par date, au moyen d'un `shift(1)` ou d'un `cumcount`. Le code est dans `src/features.py`, et
l'audit de la section 5.5 du notebook verifie qu'aucune n'est renseignee sur la premiere partie
d'un groupe.

Leurs valeurs manquantes sont des amorcages et ne sont **pas** imputees ici. L'imputation a lieu
dans le `Pipeline` de la phase 7, ajuste sur le seul jeu d'entrainement.

## Colonnes

| Colonne | Type | Unite | Description | Valeurs possibles | Source | Transformation | Feature modele | Manquant (%) |
|---|---|---|---|---|---|---|---|---|
| `gameid` | string | sans unite | Identifiant de la partie | 46 308 modalites | Oracle's Elixir | brute | non | 0.0 |
| `teamid` | object | sans unite | Identifiant de l'équipe, Inconnu si absent | 1 140 modalites | Oracle's Elixir | nettoyée | non | 0.0 |
| `team_key` | object | sans unite | Clé d'équipe, teamid ou teamname en repli | 1 386 modalites | Dérivée | construite | non | 0.0 |
| `teamname` | object | sans unite | Nom de l'équipe | 1 366 modalites | Oracle's Elixir | nettoyée | non | 0.0 |
| `date` | datetime64[ns] | horodatage | Date et heure de la partie | 2022-01-10 a 2026-09-06 | Oracle's Elixir | parsée format explicite | non | 0.0 |
| `saison` | int32 | annee | Année civile de la date, porte le split | 2022, 2023, 2024, 2025, 2026 | Dérivée | construite | non | 0.0 |
| `league` | object | sans unite | Code de la ligue, analyse seulement | 82 modalites | Oracle's Elixir | brute | non | 0.0 |
| `patch` | string | sans unite | Version du jeu, texte | 107 modalites | Oracle's Elixir | brute | non | 0.0 |
| `result` | int8 | booleen, 1 si victoire | Cible, 1 si l'équipe gagne | 0 ou 1 | Oracle's Elixir | brute | non | 0.0 |
| `golddiffat15` | float64 | or | Écart d'or à 15 minutes | -1.706e+04 a 1.706e+04 | Oracle's Elixir | brute | oui | 0.0 |
| `xpdiffat15` | float64 | points d'experience | Écart d'expérience à 15 minutes | -1.156e+04 a 1.156e+04 | Oracle's Elixir | brute | oui | 0.0 |
| `csdiffat15` | float64 | sbires | Écart de sbires à 15 minutes | -233 a 233 | Oracle's Elixir | brute | oui | 0.0 |
| `diff_kills_at15` | float64 | eliminations | killsat15 moins opp_killsat15 | -24 a 24 | Dérivée | calculée | oui | 0.0 |
| `deathsat15` | float64 | morts | Morts de l'équipe à 15 minutes | 0 a 29 | Oracle's Elixir | brute | oui | 0.0 |
| `objectifs_precoces` | Int64 | nombre d'objectifs, 0 a 3 | firstblood plus firstdragon plus firstherald, 0 à 3 | 0, 1, 2, 3 | Dérivée | calculée | oui | 0.0 |
| `compo_nb_tank` | int32 | champions | Champions taggés Tank parmi les 5 | 0, 1, 2, 3, 4 | Data Dragon | construite | oui | 0.0 |
| `compo_nb_mage` | int32 | champions | Champions taggés Mage parmi les 5 | 0, 1, 2, 3, 4, 5 | Data Dragon | construite | oui | 0.0 |
| `compo_nb_marksman` | int32 | champions | Champions taggés Marksman parmi les 5 | 0, 1, 2, 3, 4 | Data Dragon | construite | oui | 0.0 |
| `compo_nb_fighter` | int32 | champions | Champions taggés Fighter parmi les 5 | 0, 1, 2, 3, 4, 5 | Data Dragon | construite | oui | 0.0 |
| `profil_degats` | float64 | part, 0 a 1 | Part de champions AD parmi AD plus AP, 0 à 1 | 0 a 1 | Data Dragon | construite | oui | 0.0 |
| `forme_equipe_10_derniers` | float64 | taux de victoire, 0 a 1 | Taux de victoire sur les 10 parties précédentes | 0 a 1 | Dérivée | fenêtre expansive, passé seul | oui | 1.5 |
| `experience_roster` | int64 | parties | Parties déjà jouées par ce cinq | 0 a 425 | Dérivée | cumcount, passé seul | oui | 0.0 |
| `winrate_champion_patch` | float64 | taux de victoire, 0 a 1 | Taux de victoire moyen des 5 champions sur le patch, parties antérieures | 0 a 1 | Dérivée | fenêtre expansive, passé seul | oui | 0.46 |
| `ecart_or_normalise` | float64 | sans unite, ratio | golddiffat15 divisé par la médiane d'or du patch | -0.6697 a 0.6703 | Dérivée | fenêtre expansive, passé seul | oui | 2.3 |
| `patch_seq` | int64 | rang dans la saison | Rang du patch dans sa saison | 1 a 24 | Dérivée | construite | oui | 0.0 |
| `side` | string | sans unite | Côté de la carte, Blue ou Red | Blue, Red | Oracle's Elixir | brute | oui | 0.0 |
| `region` | object | sans unite | Région du circuit | 9 modalites | Référentiel XLSX | jointure | oui | 0.0 |
| `tier_ligue` | int64 | niveau, 1 a 3 | Niveau de ligue, 1 à 3 | 1, 2, 3 | Référentiel XLSX | jointure | oui | 0.0 |
| `playoffs` | Int64 | sans unite | Phase finale ou saison régulière | 0 ou 1 | Oracle's Elixir | brute | oui | 0.0 |
| `firstblood` | Int64 | sans unite | Premier sang obtenu | 0 ou 1 | Oracle's Elixir | brute | oui | 0.0 |
| `firstdragon` | Int64 | sans unite | Premier dragon obtenu | 0 ou 1 | Oracle's Elixir | brute | oui | 0.0 |
| `firstherald` | Int64 | sans unite | Premier héraut obtenu | 0 ou 1 | Oracle's Elixir | brute | oui | 0.0 |
| `is_playoffs` | int32 | sans unite | Copie entière de playoffs | 0 ou 1 | Dérivée | calculée | non | 0.0 |
| `mois` | int32 | mois civil | Mois de la partie, analyse seulement | 1 a 12 | Dérivée | construite | non | 0.0 |
| `year` | int64 | etiquette de saison | Étiquette de saison d'Oracle's Elixir, analyse seulement | 2022, 2023, 2024, 2025, 2026, 2027 | Oracle's Elixir | brute | non | 0.0 |
| `patch_major` | Int64 | version majeure | Partie majeure du patch, analyse seulement | 12, 13, 14, 15, 16 | Dérivée | construite | non | 0.0 |
| `patch_minor` | Int64 | version mineure | Partie mineure du patch, analyse seulement | 1 a 24 | Dérivée | construite | non | 0.0 |
| `compo_nb_assassin` | int32 | champions | Champions taggés Assassin parmi les 5 | 0, 1, 2, 3, 4, 5 | Data Dragon | construite | non | 0.0 |
| `compo_nb_support` | int32 | champions | Champions taggés Support parmi les 5 | 0, 1, 2, 3, 4 | Data Dragon | construite | non | 0.0 |
| `turretplates` | float64 | plaques | Plaques prises, hors features car l'échelle change en 2026 | 0 a 45 | Oracle's Elixir | brute | non | 0.1 |
| `flag_ecart_or_extreme` | bool | sans unite | Écart d'or hors bornes IQR | 0 ou 1 | Dérivée | drapeau | non | 0.0 |
| `confiance` | object | sans unite | Fiabilité du classement de la ligue | haute, moyenne | Référentiel XLSX | jointure | non | 0.0 |
| `franchisee` | bool | sans unite | Ligue franchisée | 0 ou 1 | Référentiel XLSX | jointure | non | 0.0 |
| `mediane_or_patch` | float64 | or | Médiane d'or à 15 sur les parties antérieures du patch | 2.313e+04 a 2.703e+04 | Dérivée | fenêtre expansive, passé seul | non | 2.3 |
| `roster_key` | object | sans unite | Identifiant du cinq de départ | 7 375 modalites | Dérivée | construite | non | 0.0 |
| `goldat15` | float64 | or | Or de l'équipe à 15 minutes | 1.88e+04 a 3.739e+04 | Oracle's Elixir | brute | non | 0.0 |
| `opp_goldat15` | float64 | or | Or adverse à 15 minutes | 1.88e+04 a 3.739e+04 | Oracle's Elixir | brute | non | 0.0 |
| `xpat15` | float64 | points d'experience | Expérience de l'équipe à 15 minutes | 2.036e+04 a 3.861e+04 | Oracle's Elixir | brute | non | 0.0 |
| `csat15` | float64 | sbires | Sbires de l'équipe à 15 minutes | 289 a 665 | Oracle's Elixir | brute | non | 0.0 |

## Transformations appliquees

Chaque transformation est tracee dans le notebook qui la produit.

1. **Phase 1, extraction.** Lecture des cinq CSV saisonniers avec un encodage explicite,
   typage de `patch` en texte, parsing des dates au format explicite. Jointure des champions sur
   le nom anglais et non le nom francais, qui aurait fait disparaitre cinq champions en silence.
2. **Phase 3, nettoyage.** Suppression des colonnes posterieures a la 15e minute, liste
   `config.LEAKY_COLUMNS`, dont cinq rattrapees par un controle de correlation. Application de
   la regle d'inclusion : une partie n'entre que si ses deux lignes equipe ont un snapshot
   complet a 15 minutes, sinon les deux lignes sont supprimees pour preserver l'equilibre 50/50.
3. **Phase 4, jointures.** Composition et roster rattaches sur `gameid` plus `side`, jamais sur
   `gameid` plus `teamid` qui est manquant sur 1 800 lignes. Referentiel des ligues joint en
   `many_to_one` avec `validate`.
4. **Phase 4, variables derivees.** Ecarts calcules, score d'objectifs precoces, comptages de
   tags de composition, decoupage du patch en majeur et mineur puis rang dans la saison.
5. **Phase 4, variables historiques.** Fenetres expansives sur le passe seul, verifiees par un
   audit de fuite temporelle.

## Notes et limitations

- **Le perimetre n'est pas le circuit complet.** La regle de completude a ecarte une grande
  partie de la LPL sur 2022-2025, alors qu'Oracle's Elixir renseigne ces colonnes en 2026. La
  Chine passe ainsi de 0,2 % du jeu d'entrainement a 6,4 % du jeu de test, ce qui est mesure
  dans le rapport de modelisation.
- **Cinq saisons, cinq schemas.** Des colonnes apparaissent en cours de periode, larves du Neant
  en 2024 et Atakhan en 2025. Elles sont ecartees comme fuites, mais les blocs de NaN qu'elles
  produisent sont structurels et non accidentels.
- **`turretplates` change d'echelle en 2026**, maximum de 15 jusqu'en 2025 puis 45. La colonne
  est conservee pour l'analyse et exclue des features.
- **Les tags de Data Dragon decrivent le patch courant**, pas celui de la partie. Un champion
  joue en support en 2022 mais classe Marksman aujourd'hui est mal decrit retrospectivement.
- **L'ordre de la draft est absent** d'Oracle's Elixir. Les variables de composition ne sont donc
  qu'un comptage de tags, sans synergie ni contexte de pick.

## Colonnes volontairement absentes des features

| Colonne | Raison |
|---|---|
| `league`, `year`, `patch_major` | Modalites qui ne survivent pas a la frontiere 2025/2026 |
| `split` | 32 modalites, 19,8 % de manquants, 3 absentes du train |
| `turretplates` | Echelle qui change en 2026, maximum de 15 a 45 |
| `firsttower` | Drapeau de fin de partie, ecarte pour fuite en phase 3 |
| `teamname`, `teamid`, `roster_key` | Identifiants, servent aux variables de forme uniquement |
| `mois` | Aucun sens predictif, conservee pour l'analyse de phase 5 |
