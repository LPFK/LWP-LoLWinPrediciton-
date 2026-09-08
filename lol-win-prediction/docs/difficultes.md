# Journal des difficultés

Suivi transversal du projet, tenu au fil des phases. Deux parties : ce qui a été rencontré et
résolu, et ce qui reste ouvert et doit être surveillé jusqu'à la soutenance.

Ce document sert deux usages. Il évite de reperdre du temps sur un problème déjà tranché, et il
fournit les réponses aux questions de type « pourquoi avoir fait ce choix » que la soutenance
posera.

---

## Partie 1 : difficultés rencontrées et résolues

### D1. Téléchargement d'Oracle's Elixir bloqué par un quota

**Phase 1.** `gdown` et une requête directe échouent tous les deux sur « Google Drive, quota
exceeded ». Le fichier est plafonné côté serveur, pas côté code.

**Résolution.** Téléchargement manuel depuis un navigateur connecté à un compte Google. Le
script a été modifié pour télécharger saison par saison par identifiant de fichier, au lieu du
dossier entier qui contient aussi 2014 à 2021, et il affiche la marche à suivre manuelle en cas
d'échec.

**Ce qu'il faut retenir.** Le quota se réinitialise sous 24 heures. C'est un point de
reproductibilité à mentionner : un tiers qui relance le projet peut se heurter au même mur.

### D2. Les noms de champions ne correspondaient pas entre les deux sources

**Phase 1.** `src/extraction.py` téléchargeait Data Dragon en `fr_FR` et joignait sur le nom
d'affichage. Or Oracle's Elixir écrit les noms en anglais.

Cinq champions diffèrent : K'Sante, Master Yi, Nunu & Willump, Seraphine et Zoe. La jointure
n'aurait levé aucune erreur, elle aurait produit des `NaN`, et les compositions concernées
auraient été comptées avec un champion de moins.

**Résolution.** Téléchargement des deux locales. `champion` porte le nom anglais et sert de clé,
`nom_fr` est conservé pour les figures et les rapports, qui doivent être en français.

**Vérifié en phase 4.** Les 5 champions sont reconnus sur les 92 616 équipes-parties.

### D3. `csv.Sniffer` n'arrivait pas à détecter le séparateur

**Phase 1.** Le sniffer recevait une tranche de 5 000 caractères. Avec 165 colonnes, une seule
ligne dépasse 2 000 caractères, donc la tranche se terminait au milieu d'une ligne et il ne
disposait d'aucune ligne complète à comparer.

**Résolution.** Lui passer 20 lignes entières. La détection fonctionne.

**Ce qu'il faut retenir.** Un échantillon pour un sniffer se compte en lignes, jamais en
caractères.

### D4. La comparaison des schémas de saison ne détectait rien

**Phase 2.** Le cadrage annonçait que les colonnes apparaissent au fil des saisons, larves du
Néant en 2024, Atakhan en 2025. La comparaison des en-têtes renvoie zéro différence : les cinq
fichiers ont exactement les mêmes 165 colonnes.

**Cause.** Oracle's Elixir republie chaque saison avec le schéma courant et laisse vides les
colonnes sans objet à l'époque. La dérive existe, mais dans le **taux de remplissage**.

**Résolution.** Mesure du remplissage par saison. `void_grubs` passe de 6 % à 94 % en 2024,
`atakhans` de 0 % à 92 % en 2025.

**Ce qu'il faut retenir.** Un contrôle de schéma qui renvoie « rien à signaler » peut mesurer la
mauvaise chose. Sur cette source, le contrôle utile porte sur le remplissage.

### D5. 325 faux doublons sur la clé primaire

**Phase 2.** Le test `duplicated(subset=["gameid", "teamid"])` remontait 325 doublons.

**Cause.** `duplicated` traite deux `NaN` comme égaux, et 650 lignes n'ont pas de `teamid`. Deux
équipes distinctes d'une même partie, toutes deux sans identifiant, passaient pour un doublon.
Vérification faite : noms différents, un gagnant et un perdant, ce sont de vraies parties.

**Résolution.** Le test porte sur les seules lignes à clé renseignée, et les `teamid` manquants
sont comptés à part. Il y en a 1 800 au total, dont 650 formant ces faux doublons.

### D6. `turretplates` change d'échelle à la frontière du split

**Phase 2.** Maximum théorique de 15, soit trois tourelles extérieures à cinq plaques. Respecté
de 2022 à 2025. En 2026 la colonne atteint 45 et dépasse 15 sur 61 % des lignes.

**Pourquoi c'était grave.** La colonne était dans `NUMERIC_FEATURES`. Un `StandardScaler` ajusté
sur 2022-2025 aurait projeté 2026 hors de la plage apprise, sans lever la moindre erreur.

**Résolution.** Retirée des features en phase 3. La colonne reste dans le dataset pour l'analyse.

**Ce qu'il faut retenir.** C'est un contrôle de **bornes métier** qui l'a attrapé, pas un
contrôle statistique. La colonne était parfaitement remplie et sans valeur aberrante au sens de
l'IQR.

### D7. `year` n'est pas une année civile

**Phase 2.** 2 712 lignes ont un `year` différent de l'année de leur date.

**Ma première lecture était fausse.** J'ai d'abord écrit qu'elles étaient toutes étiquetées 2027.
Le croisement montre autre chose : ces parties se jouent entre septembre et décembre et portent
l'étiquette de la saison **suivante**, parce que les circuits ouvrent leur saison à l'automne
précédent. Seules 10 lignes sont réellement étiquetées 2027.

**Résolution.** `SPLIT_DATE = "2026-01-01"` et une colonne `saison` construite sur la date. Le
découpage est strictement temporel et n'abandonne aucune ligne.

**Ce qu'il faut retenir.** La recommandation n'a pas changé, mais sa justification si. Découper
sur la date ne sert pas à rattraper des erreurs, il sert à préserver l'ordre chronologique.

### D8. La liste des colonnes de fuite était incomplète

**Phase 3.** `config.LEAKY_COLUMNS`, écrite de mémoire au cadrage, laissait passer cinq colonnes
de fin de partie.

**Comment elles ont été trouvées.** Un test empirique : corrélation absolue de chaque colonne
survivante avec la cible. `golddiffat15` est le meilleur signal légitime à la minute 15 et
corrèle à 0,535. Toute colonne au-dessus contient le résultat au lieu de le prédire.

| Colonne | Corrélation |
|---|---|
| `damagetotowers` | 0,760 |
| `team kpm` | 0,679 |
| `elementaldrakes` et `opp_elementaldrakes` | 0,586 |
| `ckpm` | 0,000 |

**Le cas `ckpm` est instructif.** Sa corrélation est nulle parce qu'elle vaut la même chose pour
les deux équipes. Elle ne trahit pas le gagnant, mais reste inconnue à la minute 15. La
corrélation détecte, elle ne suffit pas à décider.

**Ce qu'il faut retenir.** Sur un export de fin de partie, ce test devrait précéder toute liste
rédigée à la main, et pas la compléter après coup.

### D9. `firsttower` est un drapeau de fin de partie

**Phase 3.** Le cadrage le classait connu à la minute 15 et en faisait le quatrième terme de
`objectifs_precoces`.

**Deux mesures le contredisent.** Il est attribué dans 100 % des parties, alors que
`firstblood`, `firstdragon` et `firstherald` laissent des parties sans titulaire : un drapeau qui
trouve toujours un titulaire décrit la partie entière, pas un instant. Et il corrèle à 0,391,
contre 0,18 à 0,25 pour les trois autres. En jeu professionnel la première tourelle tombe
couramment après la quinzième minute, les plaques ne disparaissant qu'à la quatorzième.

**Résolution.** Ajouté aux colonnes de fuite. `objectifs_precoces` somme trois objectifs et vaut
0 à 3. Divergence assumée avec CLAUDE.md, motivée par une mesure.

### D10. La clé de jointure évidente était la mauvaise

**Phase 4.** `gameid` + `teamid` semble être la clé naturelle pour rattacher la composition à
l'équipe. Elle est fausse ici : `teamid` manque sur 1 800 lignes, remplies par la constante
`Inconnu` en phase 3. Regrouper là-dessus fusionne les deux équipes d'une même partie.

**Symptôme observé.** Une première tentative ne récupérait que 7 992 des 8 314 compositions
attendues, sans erreur ni avertissement.

**Résolution.** Joindre sur `gameid` + `side`. `side` vaut toujours `Blue` ou `Red`, sans
exception, et distingue donc toujours les deux camps. Couverture obtenue : 100 %.

### D11. Les colonnes de picks sont incomplètes

**Phase 4.** `pick1` à `pick5` manquent sur 9 % des lignes équipe, soit 8 314 lignes.

**Résolution.** Reconstruire la composition depuis les **lignes joueur**, où `champion` ne manque
sur aucune ligne, et qui sont en plus la seule source associant un champion à un poste. Les
colonnes `pick*` ne sont pas utilisées du tout.

### D12. La normalisation par patch était une fuite déguisée

**Phase 4.** `ecart_or_normalise` divise l'écart d'or par la médiane d'or du patch.
L'implémentation naturelle, `groupby("patch")["goldat15"].transform("median")`, donne à chaque
partie la médiane de tout son patch, parties postérieures comprises.

**Pourquoi c'est le piège le plus discret du projet.** La fuite ne passe pas par une colonne
suspecte mais par une statistique agrégée. Aucune liste de colonnes interdites ne l'aurait
attrapée.

**Résolution.** Médiane en fenêtre expansive sur les parties antérieures du même patch, avec un
amorçage de 20 parties.

### D13. Les amorçages produisent des valeurs manquantes, et c'est normal

**Phase 4.** Les features historiques laissent des `NaN` : 1,5 % pour la forme d'équipe,
0,46 % pour le winrate champion, 2,3 % pour l'écart d'or normalisé.

**Décision.** Ne pas les imputer. Une équipe qui joue sa première partie n'a pas de forme, et
remplir par 0,5 injecterait une hypothèse. Le guide interdit de toute façon l'imputation avant
le split. Elle aura lieu dans le `Pipeline` de la phase 7, ajusté sur le seul jeu
d'entraînement, et `HistGradientBoostingClassifier` sait les traiter nativement.

---

## Partie 2 : difficultés à suivre

Points non résolus, ou résolus sous conditions. À relire avant la phase 7 et avant la soutenance.

### R1. La saison de test est tronquée

Les données s'arrêtent au 6 septembre 2026, alors que les saisons d'entraînement vont jusqu'en
novembre ou décembre. Il manque la fin de saison 2026 et surtout les Worlds, qui se jouent en
octobre.

**Conséquences.** Le jeu de test est plus petit qu'une saison complète, donc l'intervalle de
confiance des scores est plus large. Et sa composition penche vers la saison régulière, alors
que les saisons d'entraînement contiennent leurs phases finales.

**À faire.** L'énoncer soi-même en soutenance plutôt que de se le faire opposer. Ne pas comparer
directement un score 2026 à un score 2025 sans rappeler cette asymétrie.

### R2. 16 % des lignes reposent sur une classification de ligue incertaine

Le référentiel couvre les 84 codes observés, mais une trentaine d'entre eux ont été identifiés
en lisant les noms d'équipes plutôt que de mémoire. La colonne `confiance` les marque `moyenne`.

Pour ces lignes, la **région** est solide, c'est le **tier** qui est le plus incertain.

**À faire.** Si la question business 5, sur les ligues majeures contre les mineures, donne un
résultat serré, ce chiffre est la première objection à anticiper. Un contrôle de robustesse
consisterait à refaire l'analyse sur les seules lignes en confiance haute.

### R3. Les trois objectifs conservés restent des drapeaux de partie entière

`firsttower` a été écarté, mais `firstblood`, `firstdragon` et `firstherald` sont construits de
la même façon : ils décrivent toute la partie, pas l'état à la minute 15.

Le risque est faible et documenté. Le héraut disparaît de la carte à la quatorzième minute, donc
`firstherald` est nécessairement résolu avant l'instant de prédiction. Le premier dragon apparaît
à la cinquième minute et le premier sang tombe presque toujours tôt.

**À faire.** Si un modèle dépasse nettement les 78 % d'exactitude attendus, tester en retirant
`objectifs_precoces` pour mesurer sa contribution réelle.

### R4. `ecart_or_normalise` dépasse légèrement le plafond de corrélation

Le contrôle anti-fuite retenu est : aucune colonne ne doit corréler avec la cible plus fort que
`golddiffat15`, à 0,535. Or `ecart_or_normalise` corrèle à 0,536.

**Ce n'est pas une fuite.** La feature dérive de `golddiffat15` divisé par une médiane calculée
sur le passé seul, et l'audit temporel confirme qu'elle n'est pas renseignée avant l'heure. Le
gain de 0,001 vient du retrait du bruit de méta, ce qui est précisément son but.

**À faire.** Savoir l'expliquer si la question tombe. Le plafond est une heuristique pour les
colonnes brutes, pas une règle absolue pour les variables dérivées.

### R5. Les tags de champions décrivent le patch courant, pas l'historique

Data Dragon donne les tags de la version 16.17.1. Un champion joué en support en 2022 mais
classé Marksman aujourd'hui sera mal décrit rétrospectivement, et cela affecte les six colonnes
`compo_nb_*` ainsi que `profil_degats`.

Data Dragon expose les anciennes versions, mais les aligner patch par patch sur cinq saisons
dépasse le périmètre du projet.

**À faire.** Limite assumée, à rappeler en soutenance. Si les features de composition ressortent
importantes dans le modèle, la nuance devient un vrai sujet.

### R6. Redondance entre l'écart d'or brut et sa version normalisée

`golddiffat15` vaut exactement `goldat15` moins `opp_goldat15`, et `ecart_or_normalise` en
dérive. Les trois portent largement la même information.

**À faire.** La phase 7 tranchera avec les coefficients de la régression logistique. Si la
colinéarité déstabilise les coefficients, ne garder que la version normalisée.

### R7. Biais de sélection sur les parties écartées

11,4 % des lignes ont été supprimées faute de snapshot à 15 minutes, et elles ne sont pas
réparties au hasard : les ligues mineures y sont surreprésentées. Le jeu final penche donc vers
les circuits les mieux instrumentés.

**À faire.** L'annoncer, et ne pas présenter le modèle comme valable sur n'importe quelle ligue
mineure.

### R8. La région `CEI` ne compte que 32 lignes

Toutes en 2022, la ligue ayant disparu. C'est une modalité trop rare pour être encodée telle
quelle.

**À faire.** Regrouper les régions rares avant l'encodage, ou vérifier que
`OneHotEncoder(handle_unknown="ignore")` ne crée pas une colonne quasi vide qui déstabilise la
régression.

### R9. Reproductibilité du téléchargement

Le quota Google Drive peut bloquer un tiers qui relance le projet. Les fichiers ne sont pas
versionnés, `.gitignore` excluant `data/raw/`.

**À faire.** Mentionner la marche à suivre manuelle dans le README, ce qui est déjà le cas, et
prévoir la question en soutenance.

### R10. Le seuil d'alerte de la phase 7

L'attendu est de 72 à 78 % d'exactitude. Si un modèle atteint 90 %, il y a une fuite.

**À faire.** Ne pas se réjouir d'un bon score. Rejouer le contrôle de corrélation de la phase 3
et l'audit temporel de la phase 4 avant toute autre chose.
