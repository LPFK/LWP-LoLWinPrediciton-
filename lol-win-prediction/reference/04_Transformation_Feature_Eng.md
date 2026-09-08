# Phase 4 : Transformation et Feature Engineering

**Objectif** : Combiner vos sources de données et créer des variables dérivées (features) qui enrichiront vos analyses.

---

## Pourquoi cette phase est importante

Les données brutes racontent rarement toute l'histoire. En créant de nouvelles variables, vous pouvez :
- Révéler des patterns cachés
- Préparer les données pour des analyses avancées
- Répondre plus directement à vos questions business

C'est souvent la phase qui fait la différence entre une analyse basique et une analyse percutante.

---

## 1. Jointures entre sources de données

### Types de jointures

| Type | Description | Quand l'utiliser | Résultat |
|------|-------------|------------------|----------|
| **Inner** | Garde seulement les correspondances | Besoin de données complètes | Moins de lignes |
| **Left** | Garde tout de la table gauche | Table principale + enrichissement | Même nb lignes (gauche) |
| **Right** | Garde tout de la table droite | Rarement utilisé | Même nb lignes (droite) |
| **Outer** | Garde tout des deux côtés | Vue exhaustive | Plus de lignes |

### Schéma visuel des jointures

```
Table A          Table B          Inner Join       Left Join        Outer Join
┌───┬───┐       ┌───┬───┐       ┌───┬───┬───┐   ┌───┬───┬───┐   ┌───┬───┬───┐
│ ID│ X │       │ ID│ Y │       │ ID│ X │ Y │   │ ID│ X │ Y │   │ ID│ X │ Y │
├───┼───┤       ├───┼───┤       ├───┼───┼───┤   ├───┼───┼───┤   ├───┼───┼───┤
│ 1 │ a │       │ 2 │ b │       │ 2 │ c │ b │   │ 1 │ a │NaN│   │ 1 │ a │NaN│
│ 2 │ c │       │ 3 │ d │       │ 3 │ e │ d │   │ 2 │ c │ b │   │ 2 │ c │ b │
│ 3 │ e │       └───┴───┘       └───┴───┴───┘   │ 3 │ e │ d │   │ 3 │ e │ d │
└───┴───┘                                       └───┴───┴───┘   │ 4 │NaN│ f │
                                                                └───┴───┴───┘
```

### Checklist avant jointure

- [ ] Identifier la clé de jointure dans chaque table
- [ ] Vérifier que les clés ont le même type de données
- [ ] Vérifier l'unicité des clés (1-1, 1-N, N-N)
- [ ] Choisir le type de jointure approprié
- [ ] Anticiper les valeurs manquantes après jointure

### Template de documentation des jointures

| Jointure | Table gauche | Table droite | Clé | Type | Lignes avant | Lignes après |
|----------|--------------|--------------|-----|------|--------------|--------------|
| 1 | ____________ | ____________ | ___ | ____ | ____________ | ____________ |
| 2 | ____________ | ____________ | ___ | ____ | ____________ | ____________ |
| 3 | ____________ | ____________ | ___ | ____ | ____________ | ____________ |

### Pièges à éviter

| Piège | Symptôme | Solution |
|-------|----------|----------|
| Clés de types différents | Jointure vide ou incomplète | Convertir les types avant |
| Doublons dans les clés | Multiplication des lignes | Dédupliquer ou agréger avant |
| Mauvais type de jointure | Perte de données inattendue | Vérifier le nombre de lignes après |

---

## 2. Catégories de features à créer

### Vue d'ensemble

| Catégorie | Description | Exemples |
|-----------|-------------|----------|
| **Temporelles** | Dérivées des dates | Mois, jour semaine, weekend |
| **Agrégées** | Calculs sur groupes | Moyenne par client, total par catégorie |
| **Calculées** | Opérations entre colonnes | Marge, ratio, pourcentage |
| **Catégorielles** | Regroupements en classes | Segments, tranches |
| **Textuelles** | Extraites du texte | Longueur, mots-clés |
| **Indicateurs** | Flags binaires | Est_nouveau, A_promotion |

---

### 2.1 Features temporelles

Si vous avez une colonne de date, vous pouvez extraire :

| Feature | Description | Usage |
|---------|-------------|-------|
| Année | 2024 | Comparaisons annuelles |
| Mois | 1-12 | Saisonnalité |
| Jour du mois | 1-31 | Patterns mensuels |
| Jour de la semaine | Lundi-Dimanche | Patterns hebdomadaires |
| Semaine de l'année | 1-52 | Analyses hebdomadaires |
| Trimestre | Q1-Q4 | Reporting trimestriel |
| Est weekend | Oui/Non | Comportement weekend |
| Est jour férié | Oui/Non | Impact des fériés |
| Heure | 0-23 | Patterns journaliers |

### Checklist features temporelles

- [ ] Identifier toutes les colonnes de type date/datetime
- [ ] Extraire les composantes pertinentes pour votre analyse
- [ ] Créer des indicateurs (weekend, férié, etc.)
- [ ] Calculer des durées si pertinent (ancienneté, délai, etc.)

---

### 2.2 Features agrégées

Les agrégations permettent de calculer des statistiques par groupe.

| Fonction | Description | Exemple |
|----------|-------------|---------|
| count | Nombre d'occurrences | Nb transactions par client |
| sum | Somme | CA total par produit |
| mean | Moyenne | Panier moyen par canal |
| median | Médiane | Prix médian par catégorie |
| min/max | Extremum | Première/dernière commande |
| std | Écart-type | Variabilité des achats |

### Stratégies d'agrégation

**Au niveau de la ligne (transform)** :
- La valeur agrégée est répétée pour chaque ligne du groupe
- Utile pour comparer une ligne à son groupe
- Exemple : "Cette transaction est-elle au-dessus de la moyenne du client ?"

**Au niveau du groupe (groupby + agg)** :
- Crée un nouveau DataFrame avec une ligne par groupe
- Utile pour l'analyse par segment
- Exemple : "Quel est le CA total par catégorie ?"

### Checklist features agrégées

- [ ] Identifier les dimensions d'agrégation pertinentes
- [ ] Choisir les métriques à calculer
- [ ] Décider : transform (au niveau ligne) ou agg (au niveau groupe)
- [ ] Nommer clairement les nouvelles colonnes

---

### 2.3 Features calculées

Opérations entre colonnes existantes.

| Type | Formule | Exemple |
|------|---------|---------|
| Différence | A - B | Marge = Prix vente - Coût |
| Ratio | A / B | Taux conversion = Achats / Visites |
| Pourcentage | (A / B) × 100 | Part de marché |
| Produit | A × B | Montant = Quantité × Prix |
| Combinaison | f(A, B, C) | Score pondéré |

### Checklist features calculées

- [ ] Identifier les calculs métier pertinents
- [ ] Vérifier les divisions par zéro
- [ ] Donner des noms explicites aux nouvelles colonnes
- [ ] Documenter les formules utilisées

---

### 2.4 Features catégorielles (binning/segmentation)

Transformer des valeurs continues en catégories.

| Méthode | Description | Quand l'utiliser |
|---------|-------------|------------------|
| **Cut** (intervalles fixes) | Bornes définies manuellement | Règles métier connues |
| **Qcut** (quantiles) | Même effectif par groupe | Distribution équilibrée |
| **Règles métier** | Logique conditionnelle | Critères complexes |

### Exemples de segmentations courantes

| Domaine | Variable | Segmentation |
|---------|----------|--------------|
| Client | Montant total | Petit / Moyen / Gros |
| Client | Récence | Actif / Dormant / Perdu |
| Produit | Prix | Low / Mid / Premium |
| Transaction | Montant | Petit panier / Panier moyen / Gros panier |

### Checklist features catégorielles

- [ ] Identifier les variables à segmenter
- [ ] Définir les bornes (métier ou statistiques)
- [ ] Nommer les catégories de façon explicite
- [ ] Vérifier la distribution des catégories

---

### 2.5 Features indicateurs (flags)

Variables binaires (Oui/Non, 0/1).

| Exemple | Condition |
|---------|-----------|
| est_nouveau_client | Première commande il y a < 30 jours |
| a_retour | Au moins un retour produit |
| est_premium | Montant total > seuil |
| est_complet | Aucune valeur manquante |
| est_weekend | Jour = Samedi ou Dimanche |

### Checklist features indicateurs

- [ ] Identifier les conditions métier importantes
- [ ] Créer des colonnes booléennes
- [ ] Vérifier la distribution (pas trop déséquilibrée)

---

## 3. Template de description du dataset final

### Informations générales

```
Nom du dataset : _________________________________
Date de création : _________________________________
Nombre de lignes : _________________________________
Nombre de colonnes : _________________________________
Période couverte : de __________ à __________
```

### Description des colonnes

| Colonne | Type | Description | Source | Transformation |
|---------|------|-------------|--------|----------------|
| _______ | ____ | ___________ | ______ | ______________ |
| _______ | ____ | ___________ | ______ | ______________ |
| _______ | ____ | ___________ | ______ | ______________ |

### Colonnes originales vs créées

| Catégorie | Nombre | Exemples |
|-----------|--------|----------|
| Originales (source 1) | _____ | _____________ |
| Originales (source 2) | _____ | _____________ |
| Features temporelles | _____ | _____________ |
| Features agrégées | _____ | _____________ |
| Features calculées | _____ | _____________ |
| Features catégorielles | _____ | _____________ |
| Flags | _____ | _____________ |

---

## 4. Comment choisir les colonnes à garder

### Critères de sélection

| Garder | Supprimer |
|--------|-----------|
| Nécessaire pour répondre aux questions business | Redondant avec une autre colonne |
| Clé de jointure ou identifiant | ID technique sans valeur analytique |
| Variable explicative potentielle | Colonne intermédiaire de calcul |
| Métadonnée utile (date, source) | Information sensible non nécessaire |

### Questions à se poser

Pour chaque colonne, demandez-vous :
1. Cette colonne aide-t-elle à répondre à mes questions business ?
2. Cette colonne sera-t-elle utilisée dans mes visualisations ?
3. Cette colonne est-elle redondante avec une autre ?
4. Cette colonne contient-elle des informations sensibles ?

### Checklist de sélection finale

- [ ] Lister toutes les colonnes du dataset
- [ ] Marquer celles qui répondent aux questions business
- [ ] Identifier et supprimer les redondances
- [ ] Retirer les colonnes intermédiaires de calcul
- [ ] Ordonner les colonnes de façon logique

---

## 5. Utiliser l'IA pour vous aider

### Prompt 1 : Suggérer des features pertinentes

```
Je travaille sur un projet data dans le domaine [DOMAINE].

Mon dataset contient les colonnes suivantes :
[LISTE DES COLONNES AVEC LEURS TYPES]

Mes questions business sont :
1. [Question 1]
2. [Question 2]
3. [Question 3]

Peux-tu me suggérer des features (variables dérivées) pertinentes à créer pour enrichir mon analyse ? Pour chaque feature, indique :
- Le nom proposé
- La formule ou logique de calcul
- Pourquoi elle serait utile
```

### Prompt 2 : Optimiser une jointure

```
Je dois joindre deux tables :

Table A : [DESCRIPTION, COLONNES, NB LIGNES]
Table B : [DESCRIPTION, COLONNES, NB LIGNES]

Clé de jointure envisagée : [CLÉ]
Objectif : [CE QUE JE VEUX OBTENIR]

Peux-tu me conseiller sur :
1. Le type de jointure à utiliser
2. Les vérifications à faire avant
3. Les problèmes potentiels à anticiper
```

### Prompt 3 : Définir une segmentation

```
Je souhaite segmenter mes [clients/produits/transactions] en fonction de [VARIABLE].

Voici les statistiques de cette variable :
- Min : [X]
- Max : [Y]
- Moyenne : [Z]
- Médiane : [W]
- Distribution : [DESCRIPTION]

Contexte métier : [DESCRIPTION]

Peux-tu me proposer :
1. Des bornes de segmentation pertinentes
2. Des noms de catégories explicites
3. La justification de ce découpage
```

### Prompt 4 : Documenter le dataset

```
J'ai créé un dataset final avec les colonnes suivantes :
[LISTE DES COLONNES]

Transformations appliquées :
1. [Transformation 1]
2. [Transformation 2]
...

Peux-tu m'aider à rédiger une documentation claire de ce dataset, incluant :
1. Une description de chaque colonne
2. Les unités et formats
3. Les valeurs possibles pour les catégorielles
```

---

## 6. Checklist de validation de la phase

Avant de passer à la phase suivante, vérifiez :

### Jointures
- [ ] Toutes les sources pertinentes sont combinées
- [ ] Les jointures sont documentées
- [ ] Pas de perte de données inattendue

### Feature Engineering
- [ ] Features temporelles créées (si dates disponibles)
- [ ] Features agrégées calculées
- [ ] Features métier pertinentes ajoutées
- [ ] Segmentations/catégorisations faites

### Dataset final
- [ ] Colonnes sélectionnées et ordonnées
- [ ] Documentation complète
- [ ] Noms de colonnes explicites

---

## 7. Questions de réflexion

1. **Feature la plus utile** : Parmi les features créées, laquelle vous semble la plus prometteuse pour vos analyses ?

2. **Jointures** : Avez-vous perdu des données lors des jointures ? Cela pose-t-il un problème ?

3. **Équilibre** : Votre dataset est-il équilibré ? (pas trop de colonnes, pas de redondance)

4. **Manques** : Y a-t-il des features que vous auriez aimé créer mais qui nécessiteraient des données supplémentaires ?

---

## 8. Critères d'évaluation de cette phase

| Critère | Insuffisant | Satisfaisant | Excellent |
|---------|-------------|--------------|-----------|
| **Jointures** | 1 source uniquement | 2-3 sources combinées | 3+ sources, jointures optimisées |
| **Feature Engineering** | 0-2 features créées | 5-10 features | 10+ features variées et pertinentes |
| **Pertinence** | Features non liées aux questions | Features utiles | Features directement actionnables |
| **Documentation** | Pas de documentation | Liste des colonnes | Description complète du dataset |
| **Utilisation IA** | Non utilisée | Pour 1-2 suggestions | Intégrée dans la conception |

---

## Prochaine étape

Votre dataset est enrichi et prêt ! Passez à la **Phase 5 : EDA Analytique** pour répondre à vos questions business.

---

*Ce guide fait partie du workflow « Projet Final ML ». Consultez le fichier README pour la vue d'ensemble.*
