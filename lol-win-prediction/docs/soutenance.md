# Dossier de soutenance

Document genere par `notebooks/09_soutenance.ipynb`, a ne pas editer a la main.

Projet : prediction de l'issue d'une partie professionnelle de League of Legends a la 15e minute.
Donnees fournies par Oracle's Elixir (Tim Sevenhuysen, oracleselixir.com).

---

## Executive summary

**Contexte.** Dans une partie professionnelle de League of Legends, les quinze premieres minutes
pesent lourd sans tout decider. Les staffs et les plateformes de statistiques veulent savoir
quels avantages precoces se convertissent reellement en victoire, et lesquels sont surestimes.

**Objectif.** Determiner ce que vaut chaque avantage disponible a la 15e minute, et construire un
modele qui affiche une probabilite de victoire credible a cet instant.

**Methodologie.** 94 840 lignes equipe, 47 420 parties professionnelles de
2022 a 2026, 84 ligues, croisees avec les tags de champions de Riot Data Dragon et
un referentiel de ligues construit a la main. 23 variables retenues, toutes connues
a la 15e minute. Entrainement sur 2022-2025, test sur 2026 ouvert une seule fois.

**Principaux resultats.**

1. **Le premier dragon vaut environ 1 030 or.** A ecart d'or nul, l'equipe qui
   l'obtient gagne 14,1 points de plus. Il ne rapporte pourtant aucun or.
2. **Le premier sang ne vaut rien au-dela de l'or qu'il rapporte** : 0,4 point
   a avantage egal, p = 0,77. Le premier heraut non plus, alors qu'il mene le
   classement brut avec 22,9 points d'ecart.
3. **Le modele atteint 75,8 % d'accuracy et 0,845 d'AUC**
   contre 74,6 % pour la regle « le plus riche a 15 gagne », soit
   1,2 point de gain. Son apport reel est la probabilite calibree, que la
   baseline ne sait pas produire.

**Recommandations.** Prioriser la contestation du premier dragon sur la recherche du premier
sang. Afficher le dragon plutot que le premier sang sur un habillage de diffusion. Concentrer le
travail de macro sur les parties serrees, qui representent 29 % des situations et
ou l'ecart de niveau pese le plus.

**Limites.** Association n'est pas causalite : le controle porte sur l'or, pas sur le niveau des
equipes. Le perimetre exclut une grande partie de la LPL sur la periode d'entrainement.

---

## Structure de la presentation

### Diapositive 1, titre

Predire l'issue d'une partie professionnelle de League of Legends a la 15e minute.
Projet final Machine Learning, blocs 6 et 8.

### Diapositive 2, contexte et objectif

- Les quinze premieres minutes pesent lourd, sans tout decider
- Question : quels avantages precoces se convertissent vraiment en victoire ?
- Public vise : analystes et coachs, plateformes de statistiques, casteurs
- Enjeu : un staff qui sait ce que vaut un dragon n'entraine pas comme un staff qui l'ignore

### Diapositive 3, les donnees

- Trois sources, trois formats : Oracle's Elixir (CSV), Riot Data Dragon (JSON), referentiel de
  ligues (XLSX)
- 94 840 lignes equipe, 47 420 parties, 2022 a 2026, 84 ligues
- Defi qualite principal : un export de fin de partie, ou la majorite des colonnes contiennent le
  resultat. Instant de prediction fige a la 15e minute, tout le reste supprime
- Regle d'inclusion fondee sur la completude mesuree, jamais sur un nom de ligue

### Diapositive 4, insight 1, la hierarchie des avantages

- Question : quels avantages pesent le plus a la 15e minute ?
- Figure : `06_hierarchie_avantages.png`
- Chiffre : l'ecart d'or atteint 0,82 d'AUC a lui seul, les objectifs neutres entre 0,58 et 0,61
- Implication : le classement brut semble clair, et il est trompeur

### Diapositive 5, insight 2, le renversement

- Question : que reste-t-il de chaque objectif, a avantage economique egal ?
- Figure : `06_illusion_des_objectifs.png`, la diapositive centrale de la soutenance
- Chiffres : premier heraut 22,9 points en brut, 0,9 a or
  egal. Premier dragon 14,1 points a or egal, soit 1 030 or
- Implication : le classement est presque exactement inverse. Mecanique : le sang et le heraut
  rapportent de l'or, deja compte ; le dragon n'en rapporte aucun

### Diapositive 6, insight 3, ce qui ne compte pas

- Questions : la composition de draft, le niveau de ligue
- Figures : `06_composition_sans_effet.png`, `06_ligues_conversion.png`
- Chiffres : ecart maximal de 2,8 points pour la composition, tous les
  intervalles contiennent 50 %. Tier 1 80,1 % contre tier 3
  80,5 %, p = 0,56
- Implication : deux idees recues desamorcees. Ne pas arbitrer un pick sur un comptage de tags,
  ne pas decoter un joueur de ligue mineure sur sa conversion

### Diapositive 7, insight 4, ou se joue la partie

- Question : la forme recente aide-t-elle a convertir une avance ?
- Figures : `06_trois_regimes_de_partie.png`, `06_forme_par_regime.png`
- Chiffres : 29 % des parties encore serrees a 15 minutes, le camp en avance n'y
  gagne que 57 %. L'amplitude de la forme vaut 18,1 points en
  partie serree contre 12,4 points quand l'equipe mene
- Implication : la forme mesure le niveau, pas une capacite a conclure. L'ecart de niveau se joue
  dans les parties serrees

### Diapositive 8, insight 5, le cote bleu

- Question : l'avantage du cote bleu existe-t-il encore ?
- Figure : `06_avantage_cote_bleu.png`
- Chiffre : 52,9 % de victoires, soit environ 215 or offerts avant
  le premier pick, stable sur quatre saisons
- Implication : parametre fixe a integrer a la strategie de draft, pas a reviser chaque patch

### Diapositive 9, le modele predictif

- Cible : `result`, classification binaire, classes equilibrees a 50 %
- Metrique principale : ROC AUC. Secondaires : accuracy pour la communication, log loss pour la
  calibration, car le livrable est une probabilite affichee et non un verdict
- Trois baselines calculees avant tout modele, la plus forte a 74,6 % sur 2026
- Trois familles comparees par `GridSearchCV` avec `TimeSeriesSplit` : regression logistique,
  foret aleatoire, gradient boosting. Elles tiennent en 0,003 d'AUC
- **La regression logistique gagne** : la mieux calibree, et 38 lignes d'ecart
  entrainement/validation contre 584 pour la foret
- Verdict sur 2026, ouvert une seule fois : 75,8 % d'accuracy,
  0,845 d'AUC, 0,486 de log loss
- Figures : `07_courbe_roc.png`, `07_calibration.png`, `07_coefficients_logistique.png`
- Interpretation : `firstdragon` ressort au rang 2 sur 34, confirmant la mesure
  de la phase 5 par une methode independante
- Limites : le modele est le moins performant sur le tier 1, la ou les remontees sont les plus
  frequentes

### Diapositive 10, synthese

| Chiffre | Message |
|---|---|
| **1 030 or** | Ce que vaut le premier dragon a avantage economique egal |
| **0** | Ce que vaut le premier sang dans les memes conditions |
| **1,2 point** | Ce que le modele ajoute a une regle d'une ligne |

Message principal : tous les avantages precoces ne se valent pas, et le classement auquel tout le
monde se fie est presque exactement a l'envers.

### Diapositive 11, recommandations

Voir la section dediee ci-dessous.

### Diapositive 12, annexes

Methodologie detaillee, limites, `docs/reproductibilite.md`, inventaire des figures.

---

## Recommandations priorisees

### Recommandation 1, priorite haute

**Insight source.** A ecart d'or nul, le premier dragon apporte 14,1 points de
taux de victoire, soit 1 030 or, avec une p-valeur de l'ordre de 10 puissance
moins 26. Le premier sang en apporte 0,4, non significatif.

**Action.** Reecrire la priorite d'early game : contester systematiquement le premier dragon,
cesser de rechercher le premier sang lorsqu'il coute une position sur la carte.

**Resultat attendu.** Un premier dragon supplementaire vaut l'equivalent de 1 030
or d'avance, soit environ 14,1 points de taux de victoire sur les parties
concernees.

**Prerequis.** Aucun. La consigne est immediatement applicable en scrim.

### Recommandation 2, priorite haute

**Insight source.** Le premier sang et le premier heraut dominent le classement brut et ne valent
rien une fois l'or neutralise.

**Action.** Pour une plateforme de statistiques ou un habillage de diffusion, remplacer
l'indicateur « premier sang » par « premier dragon » dans les elements affiches en direct.

**Resultat attendu.** Un indicateur affiche qui porte reellement de l'information, au lieu d'un
indicateur qui duplique l'ecart d'or deja affiche a cote.

**Prerequis.** Modification de l'habillage graphique.

### Recommandation 3, priorite moyenne

**Insight source.** 29 % des parties restent indecises a la 15e minute, et
l'amplitude de la forme y vaut 18,1 points contre 12,4
points dans les parties deja engagees.

**Action.** Concentrer le travail de macro et de prise de decision sur les situations serrees
plutot que sur la conversion des avances.

**Resultat attendu.** Gain sur le segment ou l'ecart de niveau se joue reellement.

**Prerequis.** Selection de scrims et de revues video ciblees sur ce regime.

### Recommandation 4, priorite basse

**Insight source.** Tier 1 et tier 3 convertissent une avance de plus de 1 000 or de facon
statistiquement indiscernable, p = 0,56.

**Action.** En recrutement, ne pas decoter les statistiques de conversion d'un joueur venant
d'une ligue mineure.

**Resultat attendu.** Elargissement du vivier sans perte de qualite sur ce critere.

**Prerequis.** Aucun.

---

## Limites, avec mitigation

### Limite 1, association et non causalite

**Description.** Le controle a or egal neutralise l'avantage economique, pas le niveau des
equipes. Une equipe plus forte prend plus souvent le dragon.

**Impact potentiel.** La valeur de 1 030 or attribuee au dragon est un majorant :
elle melange la valeur de l'objectif et la force de qui l'obtient.

**Mitigation appliquee.** La comparaison est faite dans une bande ou l'ecart d'or moyen entre
groupes reste sous 15 or, verifie et non suppose. La formulation retenue est « associe a » et non
« cause ».

**Pour lever la limite.** Un indicateur de niveau independant, type classement Elo, absent des
sources du projet.

### Limite 2, perimetre incomplet

**Description.** La regle d'inclusion exige un snapshot complet a 15 minutes sur les deux lignes
d'une partie. Elle a ecarte une grande partie de la LPL sur 2022-2025.

**Impact potentiel.** La Chine passe de 0,2 % du jeu d'entrainement a 6,4 % du jeu de test, et le
modele y obtient sa plus mauvaise AUC regionale. Aucune conclusion regionale sur la LPL n'est
possible.

**Mitigation appliquee.** Le filtrage porte sur un critere mesure et documente, jamais sur un nom
de ligue. La derive est mesuree et publiee dans le rapport de modelisation.

**Pour lever la limite.** Reentrainer des que la LPL est disponible en volume sur plusieurs
saisons.

### Limite 3, representation grossiere de la draft

**Description.** La composition est reduite a un comptage de tags Data Dragon. La synergie entre
champions et l'ordre des picks sont absents d'Oracle's Elixir.

**Impact potentiel.** Le resultat negatif de la question 3 porte sur cette representation, pas
sur la draft en general.

**Mitigation appliquee.** La conclusion est formulee comme telle dans le rapport d'analyse.

**Pour lever la limite.** Une source contenant l'ordre de draft.

### Limite 4, un modele qui ignore la structure des parties

**Description.** Chaque ligne equipe est predite independamment. Les deux probabilites d'une meme
partie ne somment donc a 1 qu'approximativement, avec 220 parties ou les deux equipes sont
donnees gagnantes.

**Impact potentiel.** Visible sur un affichage en direct.

**Mitigation appliquee.** L'incoherence est mesuree et publiee plutot que passee sous silence.

**Pour lever la limite.** Normaliser les deux probabilites, ou reformuler le probleme au niveau
de la partie avec des variables en difference.

### Limite 5, derive du meta

**Description.** Quatre saisons de meta sont agregees a l'entrainement, dont deux changements de
regles majeurs.

**Impact potentiel.** Un modele unique est moins juste sur une periode heterogene.

**Mitigation appliquee.** `patch_seq` remplace le numero de patch, `ecart_or_normalise` corrige la
derive economique, et les categorielles instables sont exclues.

**Pour lever la limite.** Reentrainement periodique, a chaque debut de saison.

---

## Auto-evaluation

| Critere | Note sur 5 | Commentaire |
|---|---|---|
| Cadrage | 5 | Question predictive, cible, metrique et risque de fuite definis avant toute ligne de code |
| Extraction | 4 | Trois sources, trois formats. Le referentiel de ligues repose a 16 % sur une identification de confiance moyenne, tracee par une colonne dediee |
| Diagnostic qualite | 5 | Cinq dimensions, et le defaut le plus grave trouve dans une colonne parfaitement remplie, `turretplates` |
| Nettoyage | 5 | Cinq fuites rattrapees par un controle empirique de correlation, `firsttower` ecartee contre le cadrage initial |
| Transformation | 5 | Onze variables construites, fuite evitee sur la mediane de patch par fenetre expansive |
| Analyse | 4 | Cinq questions traitees avec intervalles de confiance. Le controle porte sur l'or seul, pas sur le niveau |
| Visualisation | 5 | Dix-neuf figures, un tableau de bord, titres formules comme des messages |
| Modelisation | 5 | Trois baselines avant tout modele, trois familles, test ouvert une fois, modele simple retenu |
| Documentation | 5 | Documents generes par le code, empreinte publiee, audit des dependances |
| Utilisation de l'IA | 4 | Prompts et corrections journalises, y compris les affirmations reecrites apres mesure |

### Reflexion metacognitive

**Ce que j'ai appris.** Qu'une correlation ne repond presque jamais a la question posee. Le
premier sang correle a 0,199 avec la victoire et ne vaut rien : il a fallu comparer a or egal
pour le voir. C'est la lecon la plus transferable du projet.

**L'etape la plus difficile.** La phase 3. Une liste de colonnes interdites ecrite de memoire est
insuffisante sur un export de fin de partie ; c'est un test empirique, comparer la correlation de
chaque colonne a celle de `golddiffat15`, qui a rattrape cinq oublis.

**Ce dont je suis le plus fier.** Que la regression logistique gagne. Le modele le plus simple est
aussi le mieux calibre et le moins sujet au surapprentissage, et c'est celui dont on peut lire les
coefficients un par un devant un jury.

**Ce que je ferais differemment.** L'audit des dependances en phase 1 et non en phase 8. Il a
revele que `requirements.txt` decrivait un environnement qui n'etait pas celui de l'execution,
incoherence qui a vecu tout le projet sans consequence visible.

**Transfert professionnel.** La discipline du jeu de test ouvert une seule fois, et l'habitude de
verifier une affirmation plutot que de la supposer, valent bien au-dela de ce sujet.

---

## Preparation aux questions du jury

| Question probable | Reponse |
|---|---|
| Pourquoi la 15e minute et pas la 10e ou la 20e ? | Oracle's Elixir fournit des snapshots a 10, 15, 20 et 25 minutes. La 15e est le dernier instant ou une majorite de parties reste indecise, 29 % sous 1 000 or d'ecart, tout en portant deja du signal |
| Pourquoi avoir ecarte `firsttower` alors que le cadrage la gardait ? | Deux mesures. Elle est attribuee dans 100 % des parties, la ou les trois autres objectifs laissent des parties sans titulaire, et elle correle a 0,381 sur l'entrainement contre 0,17 a 0,23 pour les autres. En jeu professionnel la premiere tourelle tombe souvent apres la 15e minute. Les trois drapeaux conserves ont ete reaudites empiriquement en phase 3 section 3.3 et passent |
| Pourquoi `TimeSeriesSplit` plutot qu'un `KFold` ? | Un `KFold` remelange l'ordre chronologique a l'interieur du train et reproduit a petite echelle le probleme que le split chronologique corrige : le modele validerait sur des parties anterieures a certaines de ses parties d'entrainement |
| Le gain de 1,2 point justifie-t-il un modele ? | En accuracy, difficilement. Mais la baseline ne produit pas de probabilite, seulement un verdict binaire. Le livrable metier est une probabilite affichee, et le modele atteint 0,486 de log loss avec une calibration proche de la diagonale |
| Pourquoi le coefficient de `firstblood` est-il negatif ? | Il se lit conditionnellement, pas causalement. A ecart d'or, d'experience et de kills donnes, le residu du premier sang n'a plus de valeur. C'est coherent avec la phase 5, qui mesurait 0,4 point non significatif a or egal |
| Le split aleatoire donne un meilleur score, pourquoi garder le chronologique ? | Parce que les deux protocoles n'evaluent pas la meme population : le test chronologique ne contient que 2026, homogene, le test aleatoire tire dans cinq saisons heterogenes. Le choix se justifie par la condition d'usage, predire des parties futures, pas par le score |
| Comment savez-vous qu'il n'y a pas de fuite ? | Trois garde-fous. Une deny-list centralisee dans `src/config.py`, un test empirique de correlation qui a rattrape cinq oublis, et un audit verifiant qu'aucune variable historique n'est renseignee sur la premiere partie d'un groupe. Le resultat, 75,8 % d'accuracy, est dans le domaine annonce avant modelisation |
| Que feriez-vous avec plus de temps ? | L'ordre de la draft et un classement Elo par equipe. Trois familles de modeles se tiennent en 0,003 d'AUC : le plafond vient de l'information disponible, pas de l'algorithme |

---

## Inventaire des figures

- `figures/02_completude_at15_ligue_saison.png`
- `figures/05_avantage_cote_bleu.png`
- `figures/05_conversion_ecart_or.png`
- `figures/05_conversion_par_tier.png`
- `figures/05_forme_et_conversion.png`
- `figures/05_valeur_objectifs_precoces.png`
- `figures/06_avantage_cote_bleu.png`
- `figures/06_composition_sans_effet.png`
- `figures/06_forme_par_regime.png`
- `figures/06_hierarchie_avantages.png`
- `figures/06_illusion_des_objectifs.png`
- `figures/06_ligues_conversion.png`
- `figures/06_redondance_features.png`
- `figures/06_tableau_de_bord.png`
- `figures/06_trois_regimes_de_partie.png`
- `figures/07_calibration.png`
- `figures/07_coefficients_logistique.png`
- `figures/07_courbe_roc.png`
- `figures/07_matrice_confusion.png`
