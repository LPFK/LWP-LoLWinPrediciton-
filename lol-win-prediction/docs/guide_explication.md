# Guide d'explication : le code, l'architecture, la soutenance

Document de travail, écrit à la main. Il ne sert pas au jury, il sert à toi, pour répondre à la
seule question qui compte vraiment le jour de la soutenance : « expliquez-moi ce que fait cette
ligne ».

La grille est explicite là-dessus : *un code généré par IA que l'étudiant ne sait pas expliquer
en soutenance est pénalisé, pas valorisé*. Ce document existe pour renverser cette phrase.

---

## Comment utiliser ce document

Trois niveaux de lecture, selon le temps disponible.

| Si tu as | Lis |
|---|---|
| 10 minutes | La section 1, l'architecture en une page, et la section 9, l'antisèche |
| 1 heure | Ajoute les sections 4 et 5, les décisions et les six extraits de code |
| Une soirée | Tout, en ouvrant les fichiers en parallèle |

La règle de survie : **ne jamais dire « c'est ce que fait la fonction »**. Toujours dire pourquoi
elle le fait de cette façon plutôt qu'une autre. Un jury ne teste pas ta mémoire du code, il
teste si tu comprends le problème que le code résout.

---

## 1. L'architecture en une page

### Le flux de données

```
data/raw/                 3 sources brutes, jamais modifiées
   |                      Oracle's Elixir (CSV), Data Dragon (JSON), référentiel (XLSX)
   |  notebook 01         téléchargement, typage explicite, parsing des dates
   |  notebook 02         diagnostic qualité, aucune écriture
   v
data/interim/             lignes équipe et lignes joueur, nettoyées
   |                      equipes_interim.parquet, joueurs_interim.parquet
   |  notebook 03         retrait des colonnes de fuite, règle d'inclusion
   v
data/processed/           dataset final de modélisation
   |                      lol_at15.parquet, 94 840 lignes, 49 colonnes
   |  notebook 04         jointures, 11 variables construites
   |
   +--> notebooks 05, 06  analyse et figures, sur 2022-2025 uniquement
   +--> notebook 07       baselines, 3 modèles, verdict sur 2026
   +--> notebook 08       exports et documentation
   v
models/pipeline_final.joblib
```

### Le principe qui gouverne tout

**Chaque notebook produit un artefact, et un seul notebook peut écrire un artefact donné.**

C'est ce qui rend le projet rejouable. `docs/data_dictionary.md` est écrit par le notebook 04 et
par personne d'autre ; si le notebook 08 le réécrivait aussi, les deux finiraient par diverger et
plus personne ne saurait lequel dit vrai.

Corollaire à savoir défendre : **presque aucun document du projet n'est écrit à la main**. Trois
exceptions, `docs/00_cadrage.md` écrit avant le code, `docs/difficultes.md` et ce guide. Tous les
autres sont générés par le notebook qui produit les données qu'ils décrivent. C'est pour cela
qu'ils ne peuvent pas décrire un dataset qui n'existe plus.

### Pourquoi `src/` et pas tout dans les notebooks

Trois raisons, dans cet ordre d'importance.

**La politique anti-fuite doit vivre à un seul endroit.** `config.LEAKY_COLUMNS` est une liste de
colonnes interdites. Si elle était recopiée dans quatre notebooks, il suffirait d'en oublier un
pour réintroduire une fuite. Elle est dans `src/config.py`, importée partout, jamais dupliquée.

**Les fonctions à risque doivent être relisibles.** `forme_equipe` tient en cinq lignes dans
`src/features.py`. Noyée au milieu d'une cellule de notebook, personne ne verrait le `shift(1)`
qui est précisément l'endroit où tout se joue.

**Un notebook raconte, un module calcule.** Les cellules de notebook portent le raisonnement en
markdown, les modules portent la logique. Un lecteur qui veut comprendre la démarche lit les
notebooks, un lecteur qui veut auditer lit `src/`.

---

## 2. Les six modules, un par un

Pour chacun : ce qu'il fait, et **la phrase à savoir dire** si le jury l'ouvre.

### `src/config.py`, 230 lignes

Chemins, date du split, allow-lists de features, deny-list anti-fuite, palette de couleurs.
Aucune logique, uniquement des constantes.

**La phrase.** « C'est la source unique de vérité du projet. La liste des colonnes interdites y
est écrite une fois et importée partout, donc il est impossible qu'un notebook utilise une règle
différente d'un autre. »

Ce qu'il faut savoir montrer dedans :

- `LEAKY_COLUMNS`, la deny-list, avec les commentaires qui justifient chaque ajout tardif
- `NUMERIC_FEATURES`, `CATEGORICAL_FEATURES`, `BOOLEAN_FEATURES`, les 23 variables du modèle
- `SPLIT_DATE = "2026-01-01"`, et le commentaire qui explique pourquoi on coupe sur la date et
  non sur `year`
- `ANALYSIS_ONLY`, les colonnes gardées pour l'analyse et jamais données au modèle

### `src/extraction.py`, 512 lignes

Téléchargement des trois sources et lecture typée. Le plus long module, et le moins intéressant à
défendre sauf sur deux points.

**La phrase.** « Il fait l'entrée-sortie et le typage explicite. Deux pièges y sont traités, le
format des dates et la jointure des champions. »

- `parse_dates_explicit`, ligne 169. Les dates sont parsées avec un format explicite, jamais en
  laissant pandas deviner. Cinq saisons de fichiers peuvent avoir des conventions différentes, et
  une inférence silencieuse produirait des dates fausses sans lever d'erreur.
- `load_champions`, ligne 263. La jointure se fait sur le nom **anglais** du champion. Oracle's
  Elixir écrit les noms en anglais ; joindre sur `fr_FR` faisait disparaître cinq champions
  (K'Sante, Master Yi, Nunu & Willump, Seraphine, Zoe) en silence.

### `src/quality.py`, 158 lignes

Diagnostics de qualité et règle d'inclusion des parties.

**La phrase.** « Il contient la règle qui décide quelles parties entrent dans le dataset, et
cette règle porte sur une mesure, jamais sur un nom de ligue. »

La fonction à connaître : `drop_incomplete_games`, ligne 75. Une partie n'est gardée que si **ses
deux lignes équipe** ont un snapshot complet à 15 minutes. Si une seule ligne échoue, les deux
sont supprimées.

**Pourquoi supprimer les deux.** Garder une seule ligne casserait l'équilibre 50/50 de la cible.
Chaque partie produit une ligne gagnante et une perdante ; en supprimer une seule créerait un
déséquilibre artificiel qu'il faudrait ensuite corriger. C'est la réponse à donner si on te
demande pourquoi tu jettes de la donnée valide.

### `src/features.py`, 245 lignes

Construction des variables dérivées. **Le module le plus important à défendre**, parce qu'il
contient les quatre variables qui regardent le passé, donc les quatre endroits où une fuite
pouvait se produire.

**La phrase.** « Quatre variables regardent l'historique. Deux mécanismes seulement sont employés,
`shift(1)` après tri par date, et `cumcount` qui est passé seul par construction. Aucun
`groupby().mean()` global, qui serait la fuite classique. »

Détail en section 5.

### `src/analyse.py`, 231 lignes

Statistiques descriptives, avec l'incertitude attachée. Écrit en phase 5.

**La phrase.** « Chaque taux de victoire y revient avec son effectif et son intervalle de
confiance. Un pourcentage sans effectif ne veut rien dire, et quand l'intervalle contient 50 %,
la conclusion retenue est qu'il n'y a rien à conclure. »

Le point que le jury peut remarquer : `test_deux_proportions`, ligne 50, est **écrit à la main**
plutôt qu'importé de scipy. La raison est dans la docstring : scipy n'est pas dans les
dépendances, et trois lignes qu'on peut expliquer valent mieux qu'un appel de fonction dont on
n'a pas lu le contenu. C'est un argument qui joue en ta faveur, sache le sortir.

### `src/viz.py`, 104 lignes

Identité visuelle commune et formats numériques français. Écrit en phase 6.

**La phrase.** « Il évite que la légende de source soit recopiée à la main sur dix-neuf figures,
et il centralise le format numérique français, parce que les figures écrivaient 13.6 quand le
texte à côté écrivait 13,6. »

---

## 3. Les neuf notebooks, ce que chacun produit

| Notebook | Produit | La phrase à retenir |
|---|---|---|
| 01 Extraction | `data/raw/` | Trois sources, trois formats, typage explicite |
| 02 Diagnostic | `docs/rapport_diagnostic.md` | Le défaut le plus grave était dans une colonne parfaitement remplie |
| 03 Nettoyage | `data/interim/` | Cinq fuites rattrapées par un test empirique, pas par une liste de mémoire |
| 04 Transformation | `data/processed/`, dictionnaire | Onze variables construites, quatre regardent le passé |
| 05 EDA analytique | `docs/rapport_analytique.md` | Les cinq questions business, sur 2022-2025 uniquement |
| 06 Visualisation | 9 figures, `docs/visualisations.md` | Les titres énoncent la conclusion, pas le contenu |
| 07 Modélisation | `models/pipeline_final.joblib` | Trois baselines avant tout modèle, test ouvert une fois |
| 08 Documentation | Exports, reproductibilité | L'empreinte du dataset est publiée et vérifiable |
| 09 Soutenance | `docs/soutenance.md`, le deck | La checklist des livrables est vérifiée par le code |

---

## 4. Les six décisions structurantes

Celles sur lesquelles un jury va appuyer. Pour chacune : la décision, la raison, et **l'objection
à laquelle il faut être prêt**.

### Décision 1 : l'instant de prédiction est figé à 15:00

**Raison.** Oracle's Elixir est un export de fin de partie. Sans instant de prédiction fixé, il
est impossible de dire si une colonne est légitime. En fixant 15:00, la question devient
mécanique : cette information existait-elle à cet instant ?

**Objection probable.** « Pourquoi pas 10 ou 20 minutes ? »

**Réponse.** Les snapshots disponibles sont à 10, 15, 20 et 25 minutes. À 10 minutes le signal est
trop faible, à 20 la partie est souvent jouée. À 15 minutes, 29 % des parties ont moins de
1 000 or d'écart, donc il reste quelque chose à prédire, et le signal est déjà là. C'est le
dernier instant où les deux conditions sont réunies.

### Décision 2 : le split est chronologique, et coupe sur la date

**Raison.** Le modèle sert à prédire des parties futures. Un split aléatoire l'entraînerait sur
des parties postérieures à celles qu'il évalue, situation qu'il ne rencontrera jamais en usage.

**Le détail qui impressionne.** La coupure porte sur `date`, pas sur `year`. La phase 2 a montré
que `year` est une **étiquette de saison** et non une année civile : 2 712 lignes se jouent entre
septembre et décembre et portent l'étiquette de la saison suivante. Couper sur l'étiquette
enverrait des parties de décembre 2025 dans le test pendant que des parties postérieures
resteraient à l'entraînement, ce qui casserait l'ordre chronologique que le split existe pour
garantir.

**Objection probable.** « Le split aléatoire donne un meilleur score, pourquoi le garder ? »

**Réponse.** Effectivement, et de 0,85 point d'AUC. Mais les deux protocoles n'évaluent pas la
même population : le test chronologique ne contient que 2026, une saison homogène, alors que le
test aléatoire tire dans cinq saisons hétérogènes et donc plus difficiles. C'est un effet de
composition, pas un effet d'optimisme. Le choix se justifie par la condition d'usage, pas par le
score.

### Décision 3 : `TimeSeriesSplit` et non `KFold`

**Raison.** Un `KFold` remélange l'ordre chronologique **à l'intérieur** du jeu d'entraînement. Il
reproduit donc à petite échelle exactement le problème que le split chronologique vient de
corriger : le modèle validerait sur des parties antérieures à certaines de ses parties
d'entraînement.

**Le prix à payer, à annoncer soi-même.** Le premier pli n'entraîne que sur un sixième des
données, donc les scores de validation croisée sont légèrement pessimistes. C'est le bon sens de
l'erreur : mieux vaut sous-estimer que surestimer.

**La subtilité à sortir si on te pousse.** Une ligne est une équipe, donc une partie occupe deux
lignes consécutives après le tri. Une frontière de pli peut tomber entre les deux. Avec cinq
plis, cela concerne au plus quatre parties sur 38 035, donc c'est négligeable, mais il faut
savoir que le problème existe.

### Décision 4 : les variables historiques regardent le passé seul

**Raison.** C'est la fuite la plus difficile à voir, parce qu'elle ne passe par aucune colonne
suspecte. Elle passe par une statistique agrégée. Détail complet en section 5, c'est le cœur du
sujet.

### Décision 5 : la règle d'inclusion porte sur une mesure, pas sur un nom de ligue

**Raison.** Il aurait été plus simple d'exclure la LPL, réputée mal renseignée. Exclure sur un
critère mesuré et documenté est défendable ; exclure une région sur sa réputation ne l'est pas.

**Objection probable.** « Vous avez quand même perdu presque toute la LPL. »

**Réponse.** Oui, et c'est une limite du périmètre que je documente plutôt que de la cacher. La
différence est que le filtre porte sur la disponibilité du snapshot à 15 minutes, vérifiable ligne
par ligne. Si la LPL avait été correctement renseignée, elle serait dans le dataset. C'est
d'ailleurs le cas en 2026, où elle passe de 0,2 % à 6,4 % des lignes.

### Décision 6 : la log loss comme métrique secondaire

**Raison.** C'est le choix le plus défendable du cadrage et il faut savoir le raconter. Le
livrable métier annoncé est une **probabilité affichée à l'écran**, pas un verdict. L'AUC juge le
classement des probabilités, la log loss juge leur calibration. Un modèle qui annonce 95 % et se
trompe une fois sur trois est inutilisable pour une plateforme de statistiques, quelle que soit
son accuracy.

**C'est aussi la réponse au « votre gain est faible ».** La baseline « le plus riche à 15 gagne »
ne produit pas de probabilité. Le modèle apporte quelque chose qu'elle ne peut pas donner du tout.

---

## 5. Six extraits de code, expliqués ligne à ligne

Les six morceaux qu'un jury peut ouvrir. Si tu sais expliquer ceux-là, tu sais expliquer le
projet.

### Extrait 1 : la forme d'équipe, `src/features.py` ligne 107

```python
def forme_equipe(equipes, fenetre=10, cle="team_key"):
    ordonne = equipes.sort_values(["date", "gameid"])
    forme = ordonne.groupby(cle)["result"].transform(
        lambda s: s.shift(1).rolling(fenetre, min_periods=1).mean()
    )
    return forme.reindex(equipes.index)
```

**Lecture.** On trie par date. Pour chaque équipe, on décale ses résultats d'un cran avec
`shift(1)`, puis on prend la moyenne mobile sur dix parties.

**Le point à défendre : le `shift(1)`.** Sans lui, le résultat de la partie courante ferait partie
de sa propre variable explicative. Le modèle « saurait » qui a gagné. C'est une fuite, et elle est
invisible à l'inspection du dataset final, parce que la colonne obtenue ressemble à une colonne
parfaitement normale.

**La conséquence assumée.** La première partie d'une équipe donne `NaN`, parce qu'elle n'a pas de
passé. C'est la réponse honnête. On ne la remplace pas par 0,5, ce qui injecterait une hypothèse.

### Extrait 2 : le winrate de champion, `src/features.py` ligne 134

```python
groupe = ordonne.groupby(["champion", "patch"], observed=True)
victoires_avant = groupe["result"].cumsum() - ordonne["result"]
parties_avant = groupe.cumcount()
winrate = np.where(parties_avant > 0, victoires_avant / parties_avant, np.nan)
```

**Lecture.** Le numérateur est une somme cumulée **moins la ligne courante**. Le dénominateur est
`cumcount`, qui compte les lignes précédentes du groupe.

**Le point à défendre.** Les deux termes sont passés seuls, mais pour deux raisons différentes.
`cumcount` l'est par construction, il compte ce qui vient avant. `cumsum` ne l'est pas, il inclut
la ligne courante, d'où la soustraction explicite. Savoir dire pourquoi la soustraction est là est
exactement ce qu'un jury cherche.

### Extrait 3 : la fuite qu'on a failli commettre, `src/features.py` ligne 155

```python
def mediane_or_patch_expansive(equipes, min_parties=20):
    ordonne = equipes.sort_values(["date", "gameid"])
    mediane = ordonne.groupby("patch")["goldat15"].transform(
        lambda s: s.shift(1).expanding(min_periods=min_parties).median()
    )
    return mediane.reindex(equipes.index)
```

**Raconte l'erreur, elle joue en ta faveur.** L'écriture naturelle aurait été :

```python
equipes.groupby("patch")["goldat15"].transform("median")   # FUITE
```

Cette ligne donne à chaque partie la médiane de **tout son patch**, parties futures comprises.
Aucune liste de colonnes interdites ne l'aurait attrapée, puisque la fuite ne passe pas par une
colonne mais par une statistique agrégée. La version expansive ne voit que le passé.

**Pourquoi cette variable existe.** La phase 2 a mesuré 7 à 10 % de dérive économique entre les
saisons d'entraînement et de test. Un écart d'or brut ne veut pas dire la même chose en 2022 et en
2026 ; le normaliser par la médiane du patch porte la même information sous une forme qui traverse
la frontière du split.

### Extrait 4 : l'audit qui vérifie tout ça, `src/features.py` ligne 219

```python
premiere = ordonne.groupby(cle).cumcount() == 0
a_tort = int(ordonne.loc[premiere, col].notna().sum())
```

**Lecture.** On repère la première partie de chaque groupe, et on compte combien de variables
historiques y sont renseignées.

**Le point à défendre.** Une variable passée seule n'a rien à dire sur la première partie d'une
équipe, d'un roster ou d'un champion. Si elle dit quelque chose, c'est qu'elle a lu le présent.
C'est le test le moins cher qui existe pour cette classe de bug, et il tourne à chaque exécution
du notebook 04.

**La phrase.** « Je ne suppose pas que mes fenêtres sont correctes, je le vérifie. »

### Extrait 5 : la méthode qui donne le résultat principal, `src/analyse.py` ligne 192

```python
bande = donnees[donnees[colonne_or].abs() < bande_or]
avec = bande[bande[indicateur] == 1]
sans = bande[bande[indicateur] == 0]
```

**Lecture.** On se restreint aux parties où les deux équipes sont à moins de 250 or d'écart, puis
on compare celles qui ont pris l'objectif à celles qui ne l'ont pas pris.

**Le raisonnement à porter.** Dans cette bande, l'or n'explique plus rien. L'écart de taux de
victoire qui subsiste est donc ce que l'objectif apporte **en plus** de l'or qu'il a rapporté.

**Et la vérification que le contrôle fonctionne.** On mesure l'écart d'or moyen dans chaque groupe
comparé : il reste sous 15 or. Le contrôle est vérifié, pas supposé. C'est la différence entre une
méthode et une intuition.

**Pourquoi le résultat est crédible.** La mécanique du jeu le prédit. Le premier sang rapporte
400 or, donc son effet doit disparaître ; le dragon ne rapporte aucun or, donc son effet doit
survivre. C'est exactement ce qu'on observe. Une méthode qui retrouve une mécanique connue est une
méthode en laquelle on peut avoir confiance sur le reste.

### Extrait 6 : la pipeline, `notebooks/07_modelisation.ipynb`

```python
preprocesseur = ColumnTransformer([
    ("num",  Pipeline([("imputer", SimpleImputer(strategy="median")),
                       ("scaler",  StandardScaler())]), colonnes_num),
    ("bool", Pipeline([("imputer", SimpleImputer(strategy="most_frequent"))]), colonnes_bool),
    ("cat",  Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                       ("encoder", OneHotEncoder(handle_unknown="ignore"))]), colonnes_cat),
])
```

**Le point à défendre : pourquoi tout est dans la pipeline.** C'est structurel, pas cosmétique. Un
`SimpleImputer` ajusté à la main sur le dataset complet calculerait ses médianes en incluant 2026,
donc avant même le split. La pipeline garantit que chaque transformation est ajustée sur le seul
jeu d'entraînement, à chaque pli de validation croisée.

**Pourquoi trois branches et non deux.** Le squelette du formateur en prévoit deux. Les booléens
forment ici une troisième branche parce que ce sont des 0/1 qui n'ont pas besoin d'être
centrés-réduits, et que les standardiser rendrait les coefficients de la régression logistique
moins lisibles sans rien changer à la performance.

**Pourquoi `handle_unknown="ignore"`.** Si une modalité de région apparaissait en 2026 sans avoir
jamais été vue, l'encodeur produirait une ligne de zéros plutôt que de planter. C'est une perte
d'information silencieuse, ce qui est un défaut, mais c'est préférable à un plantage en
production. Savoir énoncer ce compromis vaut mieux que de faire semblant qu'il n'existe pas.

---

## 6. Les questions difficiles

Celles auxquelles il faut avoir réfléchi avant, parce qu'elles se répondent mal à froid.

### « Votre modèle ne bat la baseline que de 1,2 point. À quoi sert-il ? »

Ne pas se défendre sur l'accuracy, c'est le terrain perdant. Répondre en trois temps.

1. C'est vrai, et c'est pour cela que je l'annonce moi-même en synthèse.
2. La baseline ne produit pas de probabilité, seulement un verdict binaire. Elle est incapable de
   distinguer une partie serrée d'une partie pliée.
3. Le livrable métier défini au cadrage est une probabilité affichée. Le modèle atteint 0,486 de
   log loss avec une calibration proche de la diagonale. C'est ce que la baseline ne sait pas
   faire, et l'accuracy n'est pas la métrique qui le montre.

### « Le coefficient de `firstblood` est négatif. Le premier sang fait perdre ? »

Non, et c'est une question de lecture. Un coefficient de régression logistique est un effet
**marginal conditionnel** aux autres variables du modèle. Ce que dit le modèle : à écart d'or,
d'expérience et de kills donnés, avoir pris le premier sang est légèrement défavorable. Une équipe
qui a pris le premier sang et dont l'écart d'or est resté nul à la 15e minute a mal converti.

La nuance qui montre que tu maîtrises : sur un jeu où quatre variables économiques corrèlent entre
elles au-delà de 0,70, les coefficients se répartissent une information commune et leur signe
individuel peut surprendre. C'est aussi pour cela que la régularisation retenue est forte,
`C = 0,05`.

### « Comment savez-vous qu'il n'y a pas de fuite ? »

Trois garde-fous, à citer dans cet ordre.

1. Une deny-list centralisée, écrite à partir du cadrage.
2. Un test empirique : `golddiffat15` est le signal légitime le plus fort à la 15e minute et
   corrèle à 0,535 ; toute colonne qui corrèle davantage contient le résultat au lieu de le
   prédire. Ce test est appliqué au seul jeu d'entraînement et a rattrapé cinq oublis, dont `damagetotowers` à 0,829.
3. Un audit qui vérifie qu'aucune variable historique n'est renseignée sur la première partie d'un
   groupe.

Et le contrôle final : le résultat, 75,8 % d'accuracy, est dans le domaine de 72 à 78 % annoncé
**avant** la modélisation. Un score à 90 % aurait déclenché une recherche de fuite.

### « Pourquoi avoir écarté `firsttower` alors que votre cadrage le gardait ? »

Assumer le changement d'avis est un point fort. Deux mesures l'ont imposé : la colonne est
attribuée dans 100 % des parties, là où les trois autres objectifs laissent des parties sans
titulaire, et elle corrèle à 0,381 sur l'entraînement contre 0,17 à 0,23 pour les autres. En jeu professionnel la
première tourelle tombe souvent après la 15e minute.

Conséquence assumée : `objectifs_precoces` somme trois objectifs et non quatre comme annoncé au
départ.

### « Votre régression logistique gagne. N'est-ce pas décevant ? »

Non, c'est le meilleur résultat possible, et il faut le dire ainsi. Les trois familles tiennent en
0,003 d'AUC, ce qui signifie que le plafond vient de l'information disponible et non de
l'algorithme. Le modèle retenu est aussi le mieux calibré et le moins sujet au surapprentissage,
38 lignes d'écart contre 584 pour la forêt aléatoire. Et c'est celui dont on peut lire les
coefficients un par un, ce qui est exactement ce qu'on me demande de faire aujourd'hui.

### « Quelle est la principale faiblesse de votre travail ? »

Ne pas éluder. La bonne réponse est l'absence de contrôle sur le niveau des équipes. Le contrôle à
or égal neutralise l'économie, pas la force des équipes, et une équipe plus forte prend plus
souvent le dragon. Les 1 030 or sont donc un majorant. Lever cette limite demanderait un classement
de type Elo, qui n'existe dans aucune des trois sources.

---

## 7. Ce qu'il ne faut pas faire à l'oral

| À éviter | Pourquoi | À la place |
|---|---|---|
| Commencer par la méthodologie | C'est la partie la plus solide, elle répond mieux qu'elle n'introduit | Commencer par le renversement des objectifs |
| Dire « le modèle a trouvé que » | Un modèle ne trouve pas, il ajuste | « Le coefficient indique que, conditionnellement à » |
| Dire « corrélation » quand tu veux dire « effet » | Le jury attend cette confusion | « Associé à », et préciser le contrôle |
| Cacher le gain de 1,2 point | Il se verra, et le cacher décrédibilise le reste | L'annoncer en synthèse, comme troisième chiffre clé |
| Réciter le code | Personne ne teste ta mémoire | Expliquer le problème que la ligne résout |
| Dire « je ne sais pas » et s'arrêter | La question reste ouverte | « Je ne l'ai pas mesuré. Ce que je peux dire, c'est que » |

---

## 8. Si le jury demande une démonstration

Ouvrir `notebooks/07_modelisation.ipynb` et montrer trois cellules dans cet ordre.

1. **La section 2**, le contrôle anti-fuite. Six assertions qui échouent bruyamment. C'est ce qui
   ouvre le notebook, avant tout modèle, et cela pose le sérieux d'emblée.
2. **La section 4**, les trois baselines. Elles sont calculées avant la première pipeline, pas en
   commentaire.
3. **La section 9**, le verdict unique sur 2026, avec le garde-fou qui affiche une alerte de fuite
   si l'accuracy dépasse 90 %.

Si on demande à voir le modèle tourner : `notebooks/09_soutenance.ipynb` recharge la pipeline et la
fait prédire, en quelques secondes.

---

## 9. Antisèche, les chiffres à connaître par cœur

### Le dataset

| Chiffre | Valeur |
|---|---|
| Lignes équipe | 94 840 |
| Parties | 46 308 |
| Période | 2022 à 2026 |
| Ligues | 82 |
| Variables données au modèle | 23, dont 11 construites |
| Entraînement / test | 76 058 / 18 782 lignes |

### Les résultats d'analyse

| Chiffre | Valeur |
|---|---|
| 1 000 or d'avance | 13,6 points de taux de victoire |
| Premier dragon, à or égal | +14,1 points, soit 1 030 or |
| Premier sang, à or égal | +0,4 point, p = 0,77 |
| Premier héraut, brut puis à or égal | +22,9 puis +0,9 point |
| Côté bleu | 52,9 %, intervalle 52,4 à 53,4 |
| Composition, écart maximal | 2,8 points, tous intervalles contenant 50 % |
| Forme, partie serrée contre avance | 18,1 contre 12,4 points |
| Tier 1 contre tier 3 | 80,1 % contre 80,5 %, p = 0,56 |
| Régimes de partie | 29 % serrées, 43 % intermédiaires, 28 % larges |
| Conversion par régime | 57 %, 74 %, 92 % |

### Le modèle

| Chiffre | Valeur |
|---|---|
| Baselines sur 2026 | 50,0 % / 53,9 % / 74,6 % |
| Modèle retenu | Régression logistique, `C = 0,05` |
| Accuracy sur 2026 | 75,8 % |
| ROC AUC | 0,845 |
| Log loss | 0,486 |
| Gain sur la baseline économique | +1,2 point, 231 lignes sur 18 782 |
| Écart entre les trois familles | 0,003 d'AUC |
| Écart train/validation, logistique | 38 lignes |
| Écart train/validation, forêt | 584 lignes |
| Rang de `firstdragon` | 2 sur 34 |

### Les trois phrases à ne pas oublier

1. **Le message.** Le classement des avantages précoces auquel tout le monde se fie est presque
   exactement à l'envers, et il suffit de comparer à or égal pour le voir.
2. **La méthode.** Dans une bande où l'écart d'or est quasi nul, l'or n'explique plus rien, donc ce
   qui reste est un apport propre.
3. **L'honnêteté.** La baseline atteint déjà 74,6 %. Ce que le modèle apporte n'est pas l'accuracy,
   c'est une probabilité calibrée.
