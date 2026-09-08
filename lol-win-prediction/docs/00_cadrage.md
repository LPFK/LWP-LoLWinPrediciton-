# Phase 0 : Cadrage du projet

Projet final Machine Learning, Blocs 6 et 8.

---

## 1. Mon projet en quelques lignes

**Domaine** : Esport, League of Legends compétitif professionnel.

**Sujet précis** : Prédiction de l'issue d'une partie professionnelle de League of Legends à partir de l'état de jeu à la minute 15 et de la composition de draft.

**Contexte / problématique** : Dans une partie de League of Legends, les 15 premières minutes déterminent une grande partie de l'issue, mais pas la totalité. Les équipes professionnelles et les analystes veulent savoir quels avantages précoces se convertissent réellement en victoire, et lesquels sont surestimés. Un staff qui sait qu'un écart de 2000 or à la 15e minute vaut moins qu'un premier Baron sécurisé n'entraîne pas ses joueurs de la même manière. Une plateforme de statistiques ou un casteur veut, lui, afficher une probabilité de victoire en direct qui soit crédible.

**Public cible** : Analystes et coachs d'équipes professionnelles, plateformes de statistiques esport, casteurs et producteurs de contenu.

**Période d'analyse** : Saisons 2022 à 2026, ligues professionnelles mondiales (LCK, LPL, LEC, LTA, LCP, ligues régionales, tournois internationaux). Entraînement sur 2022 à 2025, test sur 2026.

---

## 2. Questions business

| # | Question business | Impact potentiel |
|---|-------------------|------------------|
| 1 | Parmi les avantages disponibles à la minute 15 (or, expérience, CS, objectifs neutres, tourelles), lesquels pèsent le plus sur la probabilité de victoire ? | Hiérarchiser les priorités d'early game à l'entraînement |
| 2 | L'avantage du blue side existe-t-il encore, et varie-t-il selon la ligue et le patch ? | Ajuster la stratégie de draft en fonction du side attribué |
| 3 | À avantage économique égal, la composition de draft (nombre de tanks, profil de dégâts AD/AP) change-t-elle la probabilité de victoire ? | Arbitrer entre une compo de tempo et une compo de scaling en phase de ban/pick |
| 4 | Une équipe en bonne forme récente convertit-elle mieux un avantage précoce qu'une équipe en difficulté ? | Identifier les équipes qui perdent des parties gagnées, et cibler le coaching mental ou macro |
| 5 | Les ligues majeures convertissent-elles leurs avantages précoces plus efficacement que les ligues mineures ? | Contextualiser les statistiques d'un joueur venant d'une ligue mineure lors d'un recrutement |

---

## 3. Question prédictive

**Question prédictive** : Peut-on prédire, à la minute 15 d'une partie professionnelle, quelle équipe va gagner, à partir du seul état de jeu observable à cet instant et du draft ?

**Colonne cible (y)** : `result` (0 = défaite, 1 = victoire), présente nativement dans le fichier Oracle's Elixir, au niveau des lignes équipe.

**Type de problème** : Classification binaire.

**Répartition de la cible** : strictement 50 / 50 par construction, puisque chaque partie produit exactement une ligne gagnante et une ligne perdante au niveau équipe. Aucun problème de classe minoritaire, aucune stratégie de rééquilibrage nécessaire. À vérifier tout de même après nettoyage : la suppression de lignes incomplètes peut casser des paires et déséquilibrer légèrement la cible. Si c'est le cas, supprimer les deux lignes de la partie concernée, jamais une seule.

**À qui servirait cette prédiction** : à un analyste d'équipe pour quantifier la valeur réelle de chaque avantage précoce, et à une plateforme de stats pour afficher une probabilité de victoire en direct.

---

## 4. Métrique d'évaluation et justification métier

| Métrique | Rôle | Justification |
|---|---|---|
| **ROC AUC** | Métrique principale de sélection | Classes parfaitement équilibrées, et on s'intéresse au classement des probabilités plutôt qu'à une décision binaire |
| **Accuracy** | Métrique de communication | Lisible par un public non technique, interprétable directement contre la baseline |
| **Log loss** | Métrique de calibration | Le livrable métier est une **probabilité** affichée à l'écran, pas un verdict. Un modèle qui annonce 95 % et se trompe une fois sur trois est inutilisable |

Le choix de la log loss comme métrique secondaire est le point à défendre en soutenance : dans un usage de type affichage temps réel, un modèle mal calibré détruit la confiance même avec une bonne accuracy.

---

## 5. Baselines obligatoires

À calculer **avant** tout modèle, sous peine de plafonnement de la Phase 7 à 15/25.

| Baseline | Règle | Score attendu |
|---|---|---|
| Baseline naïve | Prédire toujours la classe majoritaire | ~50 % accuracy, AUC 0.50 |
| Baseline métier 1 | L'équipe côté blue gagne toujours | ~52 à 54 % accuracy |
| Baseline métier 2 | L'équipe qui a le plus d'or à la minute 15 gagne | ~70 % accuracy |

La baseline 2 est la vraie référence. Un modèle qui ne bat pas nettement « le plus riche à 15 gagne » n'apporte rien. C'est cette comparaison qui doit apparaître en soutenance, pas la baseline naïve.

---

## 6. Sources de données

### Source 1 (principale) : Oracle's Elixir

- **Format** : CSV, un fichier par année
- **Origine** : oracleselixir.com/tools/downloads (distribution via Google Drive, mise à jour quotidienne)
- **Accès** : libre, gratuit, sans inscription
- **Licence** : usage libre avec attribution demandée à Tim Sevenhuysen. À citer explicitement dans le notebook et la présentation.
- **Volume** : environ 115 000 lignes par saison, environ 165 colonnes. Douze lignes par partie : cinq joueurs et une ligne agrégée par équipe.
- **Périmètre retenu** : lignes équipe uniquement (`position == "team"`), saisons 2022 à 2026, soit environ 90 000 à 110 000 lignes avant filtrage qualité.

### Source 2 (complémentaire) : Riot Data Dragon

- **Format** : JSON
- **Origine** : `https://ddragon.leagueoflegends.com/api/versions.json` pour la version courante, puis `https://ddragon.leagueoflegends.com/cdn/{version}/data/fr_FR/champion.json`
- **Accès** : libre, sans clé API, sans authentification
- **Contenu utilisé** : pour chaque champion, ses `tags` (Fighter, Mage, Marksman, Tank, Assassin, Support), son `partype` (mana, énergie, fureur) et ses statistiques de base
- **Rôle dans le projet** : traduire les cinq picks bruts d'une équipe en features de composition exploitables

### Source 3 (enrichissement) : référentiel des ligues

- **Format** : Excel (.xlsx), construit à la main
- **Origine** : construction manuelle à partir de la connaissance du circuit compétitif
- **Contenu** : pour chaque code ligue présent dans Oracle's Elixir, le tier (1 circuit qualifiant pour les Worlds et compétitions internationales, 2 ligue nationale ou régionale senior, 3 academy, challenger ou coupe secondaire), la région (Corée, Chine, Europe, Amériques, Asie-Pacifique, Turquie, Moyen-Orient, CEI, international) et le statut franchisé ou non
- **Couverture** : les 84 codes observés en 2022-2026, vérifiée à 100 % en phase 1. Une colonne `confiance` a été ajoutée aux quatre prévues : une trentaine de codes ont été identifiés en lisant les noms d'équipes présents dans la ligue plutôt que de mémoire, et représentent environ 16 % des lignes
- **Rôle dans le projet** : répondre à la question business 5, et fournir un troisième format de source comme demandé en Phase 1

### Tableau récapitulatif

| Source | Format | Lignes attendues | Colonnes retenues |
|---|---|---|---|
| Oracle's Elixir 2022-2026 | CSV | ~100 000 (lignes équipe) | ~40 sur 165 |
| Data Dragon champions | JSON | ~170 | 4 |
| Référentiel ligues | XLSX | 85 | 5 |

---

## 7. Risque majeur identifié : la fuite de données

C'est le point central du projet et la première règle éliminatoire du guide.

Oracle's Elixir est un fichier de **statistiques de fin de partie**. Une majorité de ses colonnes contiennent directement ou indirectement le résultat :

| Colonne | Pourquoi elle fuite |
|---|---|
| `kills`, `deaths`, `assists`, `teamkills` | Totaux de fin de partie |
| `towers`, `inhibitors`, `barons`, `dragons`, `elders` | Une équipe qui a détruit les inhibiteurs a gagné |
| `totalgold`, `earnedgold`, `gspd` | Totaux de fin de partie |
| `damagetochampions`, `dpm`, `visionscore` | Cumulés sur toute la durée |
| `gamelength` | Corrélé à l'issue, et inconnu à la minute 15 |
| `firstbaron` | Le Baron apparaît après la 20e minute, donc postérieur à l'instant de prédiction |

**Stratégie retenue** : définir explicitement un **instant de prédiction fixé à la minute 15**, et ne conserver que les colonnes dont la valeur est connue à cet instant. Toute colonne postérieure est supprimée en Phase 3, avec justification écrite dans le log de nettoyage.

Colonnes conservées côté état de jeu : `goldat15`, `xpat15`, `csat15`, `golddiffat15`, `xpdiffat15`, `csdiffat15`, `killsat15`, `assistsat15`, `deathsat15`, `opp_killsat15`, `firstblood`, `firstdragon`, `firstherald`, `firsttower`, `turretplates` (à vérifier : plates disparaissent à la 14e minute, donc valide).

Colonnes conservées côté contexte : `league`, `year`, `split`, `playoffs`, `patch`, `side`, `teamname`, `date`, `champion` des cinq joueurs, `ban1` à `ban5`.

**Second risque, plus subtil** : les features historiques (forme récente d'une équipe, winrate d'un champion) doivent être calculées uniquement sur les parties **antérieures** à la partie courante. Un winrate calculé sur l'ensemble du dataset injecte du futur dans le passé. Implémentation obligatoire en fenêtre glissante expansive, triée par date.

---

## 7 bis. Règle d'inclusion des parties

**Décision : filtrer sur la disponibilité mesurée du snapshot à 15 minutes, pas sur le nom de la ligue.**

Oracle's Elixir contient une colonne `datacompleteness` et, indépendamment, des colonnes `at15` parfois vides. Les deux ne coïncident pas toujours. La règle retenue :

Une partie entre dans le dataset si **ses deux lignes équipe** disposent d'un snapshot complet sur `goldat15`, `xpat15`, `csat15`, `golddiffat15` et `xpdiffat15`.

Si une ligne échoue, les deux lignes de la partie sont supprimées. Supprimer un seul côté casserait l'équilibre 50/50 de la cible, qui est la propriété la plus confortable de ce dataset.

Aucune ligue n'est exclue par son nom. La liste `EXCLUDED_LEAGUES` de `src/config.py` reste vide par défaut et ne sera remplie que si l'audit de Phase 2 met en évidence un problème d'une autre nature que la donnée manquante.

Justification : exclure sur un critère mesuré et documenté est défendable en soutenance, exclure une région sur réputation ne l'est pas. Et si la complétude de la LPL s'avère correcte sur certaines saisons, l'exclure par son nom reviendrait à jeter plusieurs milliers de parties propres de la région la plus dense du circuit.

Le tableau de complétude par ligue et par saison, produit par `src/quality.py::completeness_matrix`, est un livrable de la Phase 2 sur la dimension « complétude ».

---

## 8. Stratégie de split

**Décision : split chronologique.** Entraînement sur les saisons 2022, 2023, 2024 et 2025. Test sur la saison 2026. Le split aléatoire du notebook fourni est calculé en parallèle, uniquement à titre de comparaison.

Justification : le modèle est destiné à prédire des parties futures. Un split aléatoire mélange les patchs et les rosters de part et d'autre de la frontière, ce qui revient à entraîner le modèle sur des parties postérieures à celles qu'il évalue. L'écart entre les deux scores est en soi un résultat à présenter.

### Conséquence directe sur le choix des features

Un split chronologique disqualifie toute variable catégorielle dont les modalités ne survivent pas à la frontière 2025 / 2026.

| Variable | Problème | Décision |
|---|---|---|
| `year` | 2026 n'apparaît jamais à l'entraînement | Exclue des features, conservée pour l'analyse |
| `patch_major` | Les patchs 2026 sont inconnus du modèle | Exclue, remplacée par `patch_seq` |
| `league` | Le circuit a été réorganisé en 2025 : LCS devient LTA, PCS et LJL fusionnent en LCP | Exclue des features, conservée pour l'EDA de la question business 5 |
| `teamname` | Rosters et franchises changent chaque année, et l'encodage produirait des centaines de modalités bruitées | Jamais en feature, sert uniquement à construire les variables de forme |
| `region`, `tier_ligue` | Stables malgré la réorganisation | **Conservées**, elles remplacent `league` |
| `patch_seq` | Rang du patch dans sa saison, numérique | **Créée**, généralise d'une saison à l'autre |

Sans cette précaution, `OneHotEncoder(handle_unknown="ignore")` encoderait chaque ligne de 2026 en bloc de zéros sur ces colonnes. Le modèle ne planterait pas, il perdrait simplement l'information en silence, ce qui est pire.

### Validation croisée

`GridSearchCV` avec un `KFold` classique mélange l'ordre temporel à l'intérieur du jeu d'entraînement, ce qui reproduit à petite échelle le problème que le split chronologique vient de corriger. Utiliser `TimeSeriesSplit` sur le train trié par date.

À ne pas confondre avec l'interdiction des séries temporelles pures dans le guide : celle-ci porte sur le **sujet**, pas sur le **schéma de validation**. Le problème reste une classification tabulaire.

## 9. Checklist de validation Phase 0

- [x] Domaine choisi et motivant
- [x] Sujet précis et délimité
- [x] Contexte et problématique rédigés
- [x] Public cible identifié
- [x] 5 questions business formulées, spécifiques et actionnables
- [x] Question prédictive formulée
- [x] Colonne cible nommée et présente dans les données (`result`)
- [x] Classification tranchée
- [x] Répartition de la cible examinée (50/50)
- [x] Métrique justifiée par le métier (AUC + log loss)
- [x] 3 sources identifiées, 3 formats différents (CSV, JSON, XLSX)
- [x] Volume vérifié (bien au-dessus de 10 000 lignes)
- [x] Risque de fuite de données identifié et stratégie définie
