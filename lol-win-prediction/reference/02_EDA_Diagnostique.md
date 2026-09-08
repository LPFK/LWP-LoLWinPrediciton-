# Phase 2 : EDA Diagnostique

**Objectif** : Évaluer la qualité de vos données avant de les analyser. Identifier et documenter tous les problèmes à corriger.

---

## Pourquoi un diagnostic qualité ?

"Garbage in, garbage out" — si vos données sont de mauvaise qualité, vos analyses seront fausses, même avec les meilleures méthodes.

Cette phase est **critique** : elle vous permet de :
- Identifier les problèmes avant qu'ils ne faussent vos résultats
- Planifier les actions de nettoyage nécessaires
- Documenter l'état initial de vos données (traçabilité)

---

## 1. Les 5 dimensions de la qualité des données

### Vue d'ensemble

| Dimension | Question clé | Exemple de problème |
|-----------|--------------|---------------------|
| **Complétude** | Des données manquent-elles ? | 15% des emails sont vides |
| **Unicité** | Y a-t-il des doublons ? | 200 transactions en double |
| **Cohérence** | Les données sont-elles uniformes ? | "Paris" vs "PARIS" vs "paris" |
| **Exactitude** | Les valeurs sont-elles correctes ? | Âge = 250 ans |
| **Fraîcheur** | Les données sont-elles à jour ? | Dernière mise à jour il y a 2 ans |

---

## 2. Diagnostic de la Complétude

### Qu'est-ce que la complétude ?
La complétude mesure la présence des données. Une colonne est complète si toutes les valeurs attendues sont présentes.

### Checklist complétude

Pour chaque DataFrame :

- [ ] Calculer le nombre de valeurs manquantes par colonne
- [ ] Calculer le pourcentage de valeurs manquantes
- [ ] Identifier les colonnes avec > 5% de manquants
- [ ] Identifier les colonnes avec > 30% de manquants (critiques)
- [ ] Vérifier si les manquants sont aléatoires ou systématiques

### Template de rapport - Complétude

| Colonne | Valeurs manquantes | % manquant | Criticité | Action envisagée |
|---------|-------------------|------------|-----------|------------------|
| _______ | _______ | _______ % | ☐ Faible ☐ Moyenne ☐ Haute | _____________ |
| _______ | _______ | _______ % | ☐ Faible ☐ Moyenne ☐ Haute | _____________ |
| _______ | _______ | _______ % | ☐ Faible ☐ Moyenne ☐ Haute | _____________ |

### Seuils recommandés

| % manquant | Criticité | Recommandation (préparation) |
|------------|-----------|---------------------------|
| 0-5% | Faible | Suppression de lignes OU flag + conservation |
| 5-30% | Moyenne | Flag + conservation (imputation ❌ à ce stade) |
| > 30% | Haute | Suppression de colonne OU flag si info importante |

> ⚠️ **Attention** : L'imputation (moyenne, médiane, mode) est **INTERDITE** à ce stade (préparation des données) car elle cause du **data leakage**. Elle sera enseignée dans le **le pipeline ML** avec les bonnes pratiques (fit sur train uniquement).

---

## 3. Diagnostic de l'Unicité

### Qu'est-ce que l'unicité ?
L'unicité garantit qu'il n'y a pas de doublons indésirables dans vos données.

### Checklist unicité

Pour chaque DataFrame :

- [ ] Compter les lignes en double exactes (toutes colonnes identiques)
- [ ] Identifier les doublons sur la clé primaire (ID)
- [ ] Vérifier les quasi-doublons (même transaction, timestamps différents)
- [ ] Calculer le pourcentage de doublons

### Template de rapport - Unicité

| DataFrame | Lignes totales | Doublons exacts | Doublons ID | % doublons |
|-----------|----------------|-----------------|-------------|------------|
| _________ | _______ | _______ | _______ | _______ % |
| _________ | _______ | _______ | _______ | _______ % |

### Questions à se poser

- Les doublons sont-ils des erreurs d'export ou des vraies occurrences ?
- Y a-t-il une raison métier pour avoir des lignes similaires ?
- Quelle est la "vraie" clé primaire de mes données ?

---

## 4. Diagnostic de la Cohérence

### Qu'est-ce que la cohérence ?
La cohérence vérifie que les données suivent des formats et conventions uniformes.

### Checklist cohérence

Pour les colonnes catégorielles :
- [ ] Lister les valeurs uniques de chaque colonne
- [ ] Repérer les variations de casse (majuscules/minuscules)
- [ ] Repérer les variations orthographiques
- [ ] Repérer les valeurs qui représentent la même chose

Pour les colonnes numériques :
- [ ] Vérifier les unités (euros vs centimes, kg vs g)
- [ ] Vérifier les décimales (virgule vs point)

Pour les dates :
- [ ] Vérifier le format (YYYY-MM-DD, DD/MM/YYYY, etc.)
- [ ] Vérifier les fuseaux horaires

### Template de rapport - Cohérence

| Colonne | Valeurs distinctes | Problèmes détectés | Mapping proposé |
|---------|-------------------|-------------------|-----------------|
| _______ | _______ | Ex: "Paris", "PARIS", "paris" | Tout en minuscules |
| _______ | _______ | _________________________ | _________________ |
| _______ | _______ | _________________________ | _________________ |

### Exemples courants de problèmes de cohérence

| Type | Exemple problématique | Version standardisée |
|------|----------------------|---------------------|
| Casse | "Web", "WEB", "web" | "web" |
| Accents | "Région", "Region" | "region" |
| Espaces | " Paris ", "Paris" | "Paris" |
| Abréviations | "IDF", "Ile-de-France" | Choisir une convention |

---

## 5. Diagnostic de l'Exactitude

### Qu'est-ce que l'exactitude ?
L'exactitude vérifie que les valeurs sont correctes et plausibles.

### Checklist exactitude

Pour les colonnes numériques :
- [ ] Calculer min, max, moyenne, médiane
- [ ] Identifier les valeurs négatives (si inappropriées)
- [ ] Identifier les outliers (valeurs extrêmes)
- [ ] Vérifier les ordres de grandeur

Pour les colonnes catégorielles :
- [ ] Vérifier que les valeurs sont dans la liste attendue
- [ ] Identifier les valeurs inattendues

Pour les dates :
- [ ] Vérifier que les dates sont dans la plage attendue
- [ ] Identifier les dates futures (si inappropriées)
- [ ] Identifier les dates très anciennes

### Template de rapport - Exactitude

| Colonne | Min | Max | Outliers détectés | Plausibilité |
|---------|-----|-----|-------------------|--------------|
| _______ | ___ | ___ | _______ valeurs | ☐ OK ☐ Suspect |
| _______ | ___ | ___ | _______ valeurs | ☐ OK ☐ Suspect |

### Méthodes de détection des outliers

| Méthode | Description | Quand l'utiliser |
|---------|-------------|------------------|
| **IQR** | Valeurs hors [Q1-1.5×IQR, Q3+1.5×IQR] | Distribution quelconque |
| **Z-score** | Valeurs à plus de 3 écarts-types | Distribution normale |
| **Seuils métier** | Valeurs hors bornes connues | Règles métier claires |

---

## 6. Diagnostic de la Fraîcheur

### Qu'est-ce que la fraîcheur ?
La fraîcheur vérifie que les données sont suffisamment récentes pour votre analyse.

### Checklist fraîcheur

- [ ] Identifier la date la plus ancienne des données
- [ ] Identifier la date la plus récente
- [ ] Vérifier si la période couvre vos besoins
- [ ] Vérifier s'il y a des "trous" dans les données temporelles

### Template de rapport - Fraîcheur

| Source | Date min | Date max | Période attendue | Conforme ? |
|--------|----------|----------|------------------|------------|
| ______ | ________ | ________ | ________________ | ☐ Oui ☐ Non |
| ______ | ________ | ________ | ________________ | ☐ Oui ☐ Non |

---

## 7. Rapport de diagnostic global

### Synthèse de la qualité

Complétez ce tableau récapitulatif :

| Dimension | Score (1-5) | Principaux problèmes | Priorité |
|-----------|-------------|---------------------|----------|
| Complétude | ⭐⭐⭐⭐⭐ | ______________________ | ☐ Haute ☐ Moyenne ☐ Basse |
| Unicité | ⭐⭐⭐⭐⭐ | ______________________ | ☐ Haute ☐ Moyenne ☐ Basse |
| Cohérence | ⭐⭐⭐⭐⭐ | ______________________ | ☐ Haute ☐ Moyenne ☐ Basse |
| Exactitude | ⭐⭐⭐⭐⭐ | ______________________ | ☐ Haute ☐ Moyenne ☐ Basse |
| Fraîcheur | ⭐⭐⭐⭐⭐ | ______________________ | ☐ Haute ☐ Moyenne ☐ Basse |

### Score de qualité global

```
Score global = (Complétude + Unicité + Cohérence + Exactitude + Fraîcheur) / 5

Mon score : _____ / 5
```

---

## 8. Comment prioriser les problèmes

### Matrice de priorisation

| | Impact faible | Impact élevé |
|---|---------------|--------------|
| **Facile à corriger** | Priorité 3 | Priorité 1 |
| **Difficile à corriger** | Priorité 4 | Priorité 2 |

### Ordre de traitement recommandé

1. **Doublons** → Supprimer d'abord pour ne pas fausser les stats
2. **Erreurs évidentes** → Prix négatifs, dates impossibles
3. **Cohérence** → Standardiser les formats
4. **Valeurs manquantes** → Décider imputation ou suppression
5. **Outliers** → Analyser au cas par cas

---

## 9. Utiliser l'IA pour vous aider

### Prompt 1 : Interpréter les statistiques descriptives

```
Voici les statistiques descriptives de ma colonne [NOM_COLONNE] :
- Count : [X]
- Mean : [X]
- Std : [X]
- Min : [X]
- 25% : [X]
- 50% : [X]
- 75% : [X]
- Max : [X]

Le contexte est [DÉCRIRE LE CONTEXTE - ex: prix de vente de produits électroniques].

Peux-tu m'aider à :
1. Interpréter ces statistiques
2. Identifier d'éventuelles anomalies
3. Suggérer des visualisations pertinentes
```

### Prompt 2 : Analyser les valeurs manquantes

```
Dans mon dataset sur [SUJET], j'ai les colonnes suivantes avec des valeurs manquantes :
- [Colonne 1] : [X]% manquant
- [Colonne 2] : [X]% manquant
- [Colonne 3] : [X]% manquant

Contexte : [DÉCRIRE L'USAGE PRÉVU]

Peux-tu me conseiller sur :
1. La stratégie à adopter pour chaque colonne (suppression, imputation, autre)
2. Les risques de chaque approche
3. Comment vérifier si les données manquent de façon aléatoire ou non
```

### Prompt 3 : Comprendre les outliers

```
J'ai détecté des outliers dans ma colonne [NOM_COLONNE] :
- Valeurs normales : entre [X] et [Y]
- Outliers détectés : [LISTE DES VALEURS]

Contexte : [DÉCRIRE LE DOMAINE]

Peux-tu m'aider à :
1. Comprendre si ces valeurs sont des erreurs ou des cas légitimes
2. Proposer des stratégies de traitement
3. Identifier les questions à poser au métier si nécessaire
```

---

## 10. Checklist de validation de la phase

Avant de passer à la phase suivante, vérifiez :

### Diagnostic effectué
- [ ] J'ai analysé la complétude de chaque DataFrame
- [ ] J'ai vérifié les doublons
- [ ] J'ai listé les problèmes de cohérence
- [ ] J'ai identifié les outliers et valeurs suspectes
- [ ] J'ai vérifié la fraîcheur des données

### Documentation
- [ ] J'ai complété le rapport de diagnostic global
- [ ] J'ai attribué un score de qualité
- [ ] J'ai priorisé les problèmes à traiter

### Préparation du nettoyage
- [ ] J'ai une liste claire des actions à mener
- [ ] J'ai identifié les questions à poser (si données ambiguës)

---

## 11. Questions de réflexion

1. **Surprise** : Quel problème de qualité vous a le plus surpris ? Pourquoi ?

2. **Impact** : Si vous ne corrigiez qu'un seul problème, lequel choisiriez-vous ? Quel serait son impact sur vos analyses ?

3. **Source** : D'où viennent selon vous les problèmes de qualité identifiés ? (erreur humaine, système, processus...)

4. **Compromis** : Y a-t-il des problèmes que vous allez choisir de ne pas corriger ? Pourquoi ?

---

## 12. Critères d'évaluation de cette phase

| Critère | Insuffisant | Satisfaisant | Excellent |
|---------|-------------|--------------|-----------|
| **Exhaustivité** | 1-2 dimensions analysées | 4-5 dimensions couvertes | Toutes dimensions + détails |
| **Documentation** | Pas de rapport | Rapport partiel | Rapport complet + scores |
| **Priorisation** | Pas de priorisation | Liste des problèmes | Matrice priorisée + justifications |
| **Utilisation IA** | Non utilisée | Pour 1-2 analyses | Intégrée dans le diagnostic |

---

## Prochaine étape

Vous connaissez maintenant l'état de vos données. Passez à la **Phase 3 : Nettoyage des Données** pour corriger les problèmes identifiés.

---

*Ce guide fait partie du workflow « Projet Final ML ». Consultez le fichier README pour la vue d'ensemble.*
