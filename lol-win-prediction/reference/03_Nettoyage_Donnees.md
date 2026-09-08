# Phase 3 : Nettoyage des Données

**Objectif** : Appliquer les stratégies de nettoyage appropriées pour corriger les problèmes identifiés lors du diagnostic, tout en documentant chaque transformation.

---

> ⚠️ **AVERTISSEMENT IMPORTANT — Data Leakage**
>
> Dans ce module (Pipeline Data pour l'analytique), **certaines techniques de nettoyage sont INTERDITES** car elles provoquent un **data leakage** si les données sont ensuite utilisées pour le Machine Learning :
>
> | ❌ INTERDIT à ce stade | ✅ AUTORISÉ à ce stade |
> |------------------------|------------------------|
> | Imputation par moyenne/médiane | Suppression de lignes |
> | Imputation par mode | Suppression de colonnes |
> | Winsorization des outliers | Flag + conservation |
> | Transformation des outliers | Correction si valeur vraie connue |
> | Interpolation | Valeur constante explicite ("Inconnu") |
>
> **Pourquoi ?** L'imputation utilise des statistiques calculées sur **tout le dataset**. Si vous divisez ensuite vos données en train/test pour le ML (le pipeline ML), les statistiques du test "fuient" dans le train → résultats faussement optimistes.
>
> **Règle d'or** : À ce stade (préparation des données), on **diagnostique** et on **documente** les problèmes. L'imputation statistique sera faite **dans le pipeline ML**, après le split train/test, en utilisant `fit()` uniquement sur les données d'entraînement.

---

## Principe fondamental

**Ne jamais modifier les données originales.** Travaillez toujours sur une copie et documentez chaque transformation. Vous devez pouvoir expliquer et justifier chaque décision de nettoyage.

---

## 1. Stratégies de nettoyage par type de problème

### Tableau décisionnel

| Problème | Stratégie | Quand l'utiliser | Risques | Préparation |
|----------|-----------|------------------|---------|----------|
| **Doublons exacts** | Suppression | Toujours | Aucun si vraiment identiques | ✅ |
| **Doublons partiels** | Analyse + décision | Cas par cas | Perte d'info si mal géré | ✅ |
| **Valeurs manquantes** | Suppression de lignes | < 5% et aléatoire | Biais si non aléatoire | ✅ |
| **Valeurs manquantes** | ~~Imputation (moyenne/médiane)~~ | ~~Numérique~~ | ⚠️ **DATA LEAKAGE** | ❌ |
| **Valeurs manquantes** | ~~Imputation (mode)~~ | ~~Catégoriel~~ | ⚠️ **DATA LEAKAGE** | ❌ |
| **Valeurs manquantes** | Valeur spéciale ("Inconnu") | Catégoriel, info à conserver | Crée une nouvelle catégorie | ✅ |
| **Valeurs manquantes** | Suppression de colonne | > 50% manquant | Perte d'information | ✅ |
| **Incohérence de casse** | Standardisation (lower/upper) | Colonnes texte | Aucun | ✅ |
| **Variations orthographiques** | Mapping/dictionnaire | Valeurs connues | Manuel, peut être incomplet | ✅ |
| **Outliers (erreurs)** | Suppression | Erreur évidente | Perte de données | ✅ |
| **Outliers (erreurs)** | Correction | Valeur correcte connue | Nécessite source fiable | ✅ |
| **Outliers (extrêmes)** | ~~Winsorization~~ | ~~Valeurs extrêmes~~ | ⚠️ **DATA LEAKAGE** | ❌ |
| **Outliers (extrêmes)** | Flag + conservation | Analyse séparée souhaitée | Complexifie l'analyse | ✅ |
| **Formats de date** | Conversion standardisée | Formats mixtes | Dates invalides possibles | ✅ |
| **Types incorrects** | Conversion de type | Type mal inféré | Erreurs de conversion | ✅ |

> 💡 **Note** : Les stratégies marquées ❌ seront enseignées dans le **le pipeline ML** où elles seront appliquées correctement avec `fit()` sur le train set uniquement.

---

## 2. Ordre de nettoyage recommandé

Suivez cet ordre pour éviter les problèmes en cascade :

```
1. Doublons          → Éliminer les lignes en double
       ↓
2. Erreurs évidentes → Supprimer/corriger les valeurs impossibles
       ↓
3. Types de données  → Convertir les colonnes aux bons types
       ↓
4. Standardisation   → Uniformiser les formats et conventions
       ↓
5. Valeurs manquantes → Traiter selon la stratégie choisie
       ↓
6. Outliers          → Décider du traitement
       ↓
7. Validation        → Vérifier que tout est correct
```

---

## 3. Checklist de nettoyage

### Étape 1 : Préparation

- [ ] Créer une copie du DataFrame original
- [ ] Noter le nombre de lignes avant nettoyage
- [ ] Préparer un log des transformations

### Étape 2 : Doublons

- [ ] Identifier et supprimer les doublons exacts
- [ ] Documenter le nombre de doublons supprimés
- [ ] Vérifier l'impact sur les statistiques

### Étape 3 : Erreurs évidentes

- [ ] Supprimer les lignes avec des erreurs irréparables
- [ ] Corriger les valeurs corrigeables
- [ ] Documenter chaque correction

### Étape 4 : Types de données

- [ ] Convertir les dates en datetime
- [ ] Convertir les numériques en int/float
- [ ] Vérifier les conversions (pas d'erreurs)

### Étape 5 : Standardisation

- [ ] Standardiser la casse des colonnes texte
- [ ] Appliquer les mappings de valeurs
- [ ] Supprimer les espaces superflus
- [ ] Uniformiser les formats

### Étape 6 : Valeurs manquantes

- [ ] Appliquer la stratégie choisie par colonne
- [ ] Créer des flags si nécessaire (ex: "client_inconnu")
- [ ] Documenter le traitement appliqué

### Étape 7 : Outliers

- [ ] Appliquer le traitement décidé
- [ ] Justifier chaque décision

### Étape 8 : Validation

- [ ] Comparer avant/après
- [ ] Vérifier qu'aucun nouveau problème n'est apparu
- [ ] Valider avec des statistiques descriptives

---

## 4. Documentation des transformations

### Template de log de nettoyage

Pour chaque transformation, documentez :

| # | Colonne | Problème | Action | Lignes affectées | Justification |
|---|---------|----------|--------|------------------|---------------|
| 1 | _______ | ________ | ______ | _______ | _____________ |
| 2 | _______ | ________ | ______ | _______ | _____________ |
| 3 | _______ | ________ | ______ | _______ | _____________ |

### Exemple de documentation

| # | Colonne | Problème | Action | Lignes affectées | Justification |
|---|---------|----------|--------|------------------|---------------|
| 1 | - | Doublons exacts | Suppression | 150 | Erreur d'export CRM |
| 2 | prix | Valeurs négatives | Suppression | 3 | Erreur de saisie |
| 3 | canal | Casse mixte | Standardisation lower | 5150 | Harmonisation |
| 4 | region | Variations | Mapping vers standard | 5150 | Cohérence |
| 5 | client_id | 5% manquant | Flag + conservation | 257 | Transactions valides |

---

## 5. Stratégies détaillées

### Traitement des doublons

**Doublons exacts** (toutes colonnes identiques)
- Action : Supprimer les occurrences supplémentaires
- Conserver : La première occurrence (ou selon règle métier)

**Doublons partiels** (même ID, valeurs différentes)
- Investiguer : Pourquoi les valeurs diffèrent ?
- Options : Garder le plus récent, fusionner, demander au métier

### Traitement des valeurs manquantes

> ⚠️ **Rappel (préparation des données)** : Seules les stratégies sans calcul statistique sont autorisées ici.

| Stratégie | Quand l'appliquer | Avantages | Inconvénients | Préparation |
|-----------|-------------------|-----------|---------------|----------|
| **Suppression de lignes** | < 5% manquant, aléatoire | Simple | Perte de données | ✅ |
| **Suppression de colonne** | > 50% manquant | Simplifie le dataset | Perte d'information | ✅ |
| ~~**Imputation par moyenne**~~ | ~~Numérique, symétrique~~ | ~~Préserve la moyenne~~ | ⚠️ DATA LEAKAGE | ❌ |
| ~~**Imputation par médiane**~~ | ~~Numérique, avec outliers~~ | ~~Robuste~~ | ⚠️ DATA LEAKAGE | ❌ |
| ~~**Imputation par mode**~~ | ~~Catégoriel~~ | ~~Simple~~ | ⚠️ DATA LEAKAGE | ❌ |
| **Valeur constante** | Signification métier | Explicite | Crée une catégorie | ✅ |
| **Flag "is_missing"** | Conserver l'info du manquant | Traçabilité | Colonne supplémentaire | ✅ |

> 📌 **Pour le ML (le pipeline ML)** : L'imputation statistique sera faite après le split train/test, en utilisant `SimpleImputer` avec `fit()` sur le train uniquement.

### Traitement des outliers

> ⚠️ **Rappel (préparation des données)** : Les transformations statistiques des outliers causent du data leakage.

| Stratégie | Description | Quand l'utiliser | Préparation |
|-----------|-------------|------------------|----------|
| **Suppression** | Retirer les lignes | Erreur certaine | ✅ |
| **Correction** | Remplacer par valeur correcte | Vraie valeur connue | ✅ |
| ~~**Winsorization**~~ | ~~Ramener aux percentiles~~ | ~~Valeurs extrêmes légitimes~~ | ❌ DATA LEAKAGE |
| **Flag** | Marquer mais conserver | Analyse séparée | ✅ |
| ~~**Transformation**~~ | ~~Log, sqrt~~ | ~~Réduire l'impact~~ | ❌ DATA LEAKAGE |

> 📌 **Pour le ML (le pipeline ML)** : Winsorization et transformations seront appliquées dans un Pipeline sklearn, après le split train/test.

---

## 6. Validation post-nettoyage

### Tableau comparatif avant/après

| Métrique | Avant | Après | Variation |
|----------|-------|-------|-----------|
| Nombre de lignes | _______ | _______ | _______ |
| Nombre de colonnes | _______ | _______ | _______ |
| Doublons | _______ | _______ | _______ |
| Valeurs manquantes (total) | _______ | _______ | _______ |
| Valeurs aberrantes | _______ | _______ | _______ |

### Checklist de validation

- [ ] Plus de doublons exacts
- [ ] Valeurs manquantes traitées (selon stratégie)
- [ ] Formats standardisés (vérifier avec .unique())
- [ ] Types de données corrects (.dtypes)
- [ ] Pas de nouvelles anomalies introduites
- [ ] Statistiques descriptives cohérentes

### Questions de validation

1. Le nombre de lignes supprimées est-il justifiable ?
2. Les statistiques (moyenne, médiane) sont-elles cohérentes après nettoyage ?
3. Les valeurs uniques des colonnes catégorielles sont-elles standardisées ?
4. Les conversions de types ont-elles réussi sans erreur ?

---

## 7. Bonnes pratiques

### À faire

- ✅ Toujours travailler sur une copie des données
- ✅ Documenter chaque transformation avec sa justification
- ✅ Valider après chaque étape majeure
- ✅ Conserver les données originales
- ✅ Utiliser des noms de variables explicites (df_raw, df_clean)
- ✅ Créer des flags plutôt que perdre de l'information

### À éviter

- ❌ Modifier les données originales
- ❌ Supprimer des données sans justification
- ❌ Appliquer des transformations sans vérifier le résultat
- ❌ Ignorer les warnings lors des conversions
- ❌ Imputer sans comprendre pourquoi les données manquent

---

## 8. Utiliser l'IA pour vous aider

### Prompt 1 : Choisir une stratégie de nettoyage

```
J'ai un problème de qualité de données :

Colonne : [NOM_COLONNE]
Type de données : [TYPE]
Problème : [DESCRIPTION DU PROBLÈME]
Contexte : [DOMAINE / USAGE PRÉVU]
% affecté : [POURCENTAGE]

Peux-tu me recommander :
1. La meilleure stratégie de nettoyage
2. Les risques de cette approche
3. Comment valider que le nettoyage est correct
```

### Prompt 2 : Créer un mapping de valeurs

```
J'ai une colonne [NOM_COLONNE] avec les valeurs suivantes :
[LISTE DES VALEURS UNIQUES]

Ces valeurs devraient être standardisées. Par exemple :
- "Paris", "PARIS", "paris" → "Paris"

Peux-tu me créer un dictionnaire de mapping complet pour standardiser toutes ces valeurs ?
```

### Prompt 3 : Valider le nettoyage

```
J'ai nettoyé mon dataset. Voici les changements :

Avant :
- [X] lignes, [Y] colonnes
- [Z]% de valeurs manquantes
- [W] doublons

Après :
- [X'] lignes, [Y'] colonnes
- [Z']% de valeurs manquantes
- [W'] doublons

Transformations appliquées :
1. [Transformation 1]
2. [Transformation 2]
...

Peux-tu m'aider à valider que ces transformations sont cohérentes et identifier d'éventuels problèmes ?
```

### Prompt 4 : Gérer un cas complexe

```
J'ai un cas de nettoyage complexe :

Situation : [DÉCRIRE LA SITUATION]
Contraintes : [DÉCRIRE LES CONTRAINTES]
Options envisagées :
1. [Option 1]
2. [Option 2]

Peux-tu m'aider à choisir la meilleure approche et m'expliquer les implications de chaque option ?
```

---

## 9. Checklist de validation de la phase

Avant de passer à la phase suivante, vérifiez :

### Nettoyage effectué
- [ ] Tous les problèmes identifiés au diagnostic sont traités
- [ ] Chaque transformation est documentée et justifiée
- [ ] Le log de nettoyage est complet

### Validation
- [ ] Tableau comparatif avant/après complété
- [ ] Pas de nouveaux problèmes introduits
- [ ] Statistiques descriptives vérifiées

### Qualité
- [ ] Le dataset est prêt pour l'analyse
- [ ] Les données originales sont préservées
- [ ] La traçabilité est assurée

---

## 10. Questions de réflexion

1. **Décision difficile** : Quelle décision de nettoyage a été la plus difficile à prendre ? Pourquoi ?

2. **Perte d'information** : Avez-vous dû supprimer des données ? Comment cela pourrait-il affecter vos analyses ?

3. **Reproductibilité** : Si quelqu'un d'autre devait refaire votre nettoyage, pourrait-il obtenir exactement le même résultat ?

4. **Amélioration** : Avec du recul, auriez-vous fait quelque chose différemment ?

---

## 11. Critères d'évaluation de cette phase

| Critère | Insuffisant | Satisfaisant | Excellent |
|---------|-------------|--------------|-----------|
| **Complétude** | Problèmes non traités | Principaux problèmes traités | Tous problèmes traités |
| **Documentation** | Pas de log | Log partiel | Log complet + justifications |
| **Validation** | Pas de vérification | Vérification basique | Comparatif détaillé |
| **Bonnes pratiques** | Données originales modifiées | Copie utilisée | Copie + traçabilité complète |
| **Utilisation IA** | Non utilisée | Pour 1-2 décisions | Intégrée dans le processus |

---

## Prochaine étape

Vos données sont propres ! Passez à la **Phase 4 : Transformation et Feature Engineering** pour enrichir votre dataset.

---

*Ce guide fait partie du workflow « Projet Final ML ». Consultez le fichier README pour la vue d'ensemble.*
