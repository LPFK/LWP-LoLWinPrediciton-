# Phase 1 : Extraction Multi-Sources

**Objectif** : Collecter vos données depuis différentes sources et formats, et les charger correctement dans votre environnement de travail.

---

## Pourquoi extraire depuis plusieurs sources ?

Dans le monde professionnel, les données sont rarement centralisées dans un seul fichier parfait. Vous devrez souvent :
- Combiner des exports CRM (CSV) avec des catalogues produits (Excel)
- Enrichir vos données avec des APIs externes
- Récupérer des historiques stockés dans le cloud

Maîtriser l'extraction multi-sources est une compétence essentielle du Data Analyst.

---

## 1. Les formats de données courants

### Vue d'ensemble des formats

| Format | Extension | Usage typique | Avantages | Inconvénients |
|--------|-----------|---------------|-----------|---------------|
| **CSV** | .csv | Exports, échanges | Simple, universel | Pas de typage, encoding |
| **Excel** | .xlsx | Rapports, catalogues | Multi-feuilles, formules | Lourd, formats mixtes |
| **JSON** | .json | APIs, web | Structuré, hiérarchique | Verbeux, imbrications |
| **Parquet** | .parquet | Big Data, cloud | Performant, typé | Moins lisible |
| **SQL** | .db, .sql | Bases de données | Relationnel, requêtes | Nécessite connexion |
| **API** | - | Données temps réel | Actualité, automatisation | Rate limits, auth |

---

## 2. Checklist par type de source

### Source CSV

- [ ] Identifier l'encodage du fichier (UTF-8, Latin-1, etc.)
- [ ] Repérer le séparateur utilisé (virgule, point-virgule, tabulation)
- [ ] Vérifier la présence d'un en-tête (header)
- [ ] Noter si des lignes sont à ignorer (skiprows)
- [ ] Identifier les valeurs représentant les données manquantes

**Questions à se poser** :
- Le fichier s'ouvre-t-il correctement dans un éditeur de texte ?
- Y a-t-il des caractères spéciaux ou accents mal affichés ?

---

### Source Excel

- [ ] Lister toutes les feuilles (sheets) du fichier
- [ ] Identifier quelle(s) feuille(s) contiennent les données utiles
- [ ] Vérifier si des lignes d'en-tête sont à ignorer
- [ ] Repérer les cellules fusionnées (source de problèmes)
- [ ] Noter les colonnes avec des formules (seront importées comme valeurs)

**Questions à se poser** :
- Y a-t-il plusieurs feuilles à charger ?
- Les données commencent-elles à la ligne 1 ou plus bas ?

---

### Source JSON

- [ ] Vérifier la structure du JSON (objet, liste, imbriqué)
- [ ] Identifier la clé contenant les données principales
- [ ] Repérer les niveaux d'imbrication
- [ ] Vérifier l'encodage des caractères spéciaux

**Questions à se poser** :
- Le JSON est-il une liste d'objets ou un objet avec des clés ?
- Faut-il "aplatir" des structures imbriquées ?

---

### Source API

- [ ] Lire la documentation de l'API
- [ ] Identifier le type d'authentification (clé API, OAuth, aucune)
- [ ] Noter les endpoints utiles pour votre projet
- [ ] Vérifier les limites de requêtes (rate limits)
- [ ] Tester l'API avec un outil (Postman, navigateur, curl)

**Questions à se poser** :
- Ai-je besoin d'une clé API ?
- Combien de requêtes puis-je faire par minute/jour ?
- Les données sont-elles paginées ?

---

### Source Parquet / Cloud

- [ ] Vérifier l'accès au fichier (chemin local ou S3/cloud)
- [ ] S'assurer d'avoir les bibliothèques nécessaires installées
- [ ] Vérifier les permissions d'accès (credentials AWS si S3)

**Questions à se poser** :
- Le fichier est-il accessible depuis mon environnement ?
- Ai-je configuré mes credentials cloud si nécessaire ?

---

### Source SQL / Base de données

- [ ] Obtenir les informations de connexion (host, port, user, password)
- [ ] Identifier les tables pertinentes pour le projet
- [ ] Comprendre le schéma relationnel (clés primaires, étrangères)
- [ ] Préparer les requêtes SQL nécessaires

**Questions à se poser** :
- Ai-je les droits d'accès à la base ?
- Quelles tables dois-je joindre ?

---

## 3. Tableau récapitulatif de vos données

Complétez ce tableau après l'extraction de chaque source :

| Source | Format | Nom du fichier/endpoint | Lignes | Colonnes | Observations |
|--------|--------|-------------------------|--------|----------|--------------|
| 1 | _____ | ________________________ | ______ | ________ | _____________ |
| 2 | _____ | ________________________ | ______ | ________ | _____________ |
| 3 | _____ | ________________________ | ______ | ________ | _____________ |
| 4 | _____ | ________________________ | ______ | ________ | _____________ |

### Informations à noter pour chaque source

- **Nombre de lignes** : Donne une idée du volume
- **Nombre de colonnes** : Indique la richesse des données
- **Observations** : Premiers problèmes repérés (encodage, valeurs manquantes...)

---

## 4. Pièges courants à éviter

### Problèmes d'encodage

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| Caractères bizarres (Ã©, â€™) | Mauvais encodage | Essayer UTF-8, Latin-1, cp1252 |
| Erreur "UnicodeDecodeError" | Encodage non supporté | Spécifier l'encodage correct |

### Problèmes de séparateur

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| Toutes les données dans 1 colonne | Mauvais séparateur | Vérifier ; ou \t au lieu de , |
| Colonnes décalées | Séparateur dans les données | Utiliser un autre séparateur ou des guillemets |

### Problèmes de types

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| Dates en texte | Pas de parsing automatique | Convertir explicitement les dates |
| Nombres en texte | Virgule décimale vs point | Spécifier le decimal separator |
| IDs en float | Valeurs manquantes dans colonne int | Gérer les NA avant conversion |

### Problèmes d'API

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| Erreur 401 | Authentification manquante | Vérifier la clé API |
| Erreur 429 | Trop de requêtes | Respecter les rate limits |
| Données incomplètes | Pagination | Boucler sur toutes les pages |

---

## 5. Utiliser l'IA pour vous aider

### Prompt 1 : Comprendre un format inconnu

```
Je dois charger un fichier au format [FORMAT] dans mon projet Python/Pandas.

Voici les premières lignes du fichier :
[COLLER LES PREMIÈRES LIGNES]

Peux-tu m'expliquer :
1. Comment charger ce fichier correctement ?
2. Quels paramètres dois-je spécifier ?
3. Quels problèmes potentiels dois-je anticiper ?
```

### Prompt 2 : Débugger un problème d'extraction

```
J'essaie de charger un fichier [FORMAT] mais j'obtiens cette erreur :
[COLLER L'ERREUR]

Voici ce que j'ai essayé :
[DÉCRIRE VOTRE TENTATIVE]

Peux-tu m'aider à comprendre l'erreur et me proposer une solution ?
```

### Prompt 3 : Appeler une API

```
Je souhaite récupérer des données depuis l'API [NOM DE L'API].

Voici la documentation : [LIEN OU EXTRAIT]

Peux-tu m'expliquer :
1. Comment m'authentifier ?
2. Quel endpoint utiliser pour [MON BESOIN] ?
3. Comment gérer la pagination si nécessaire ?
4. Comment transformer la réponse en DataFrame ?
```

### Prompt 4 : Comparer mes sources

```
J'ai extrait les données suivantes :

Source 1 : [NB LIGNES] lignes, [NB COLONNES] colonnes, format [FORMAT]
Colonnes : [LISTE DES COLONNES]

Source 2 : [NB LIGNES] lignes, [NB COLONNES] colonnes, format [FORMAT]
Colonnes : [LISTE DES COLONNES]

Peux-tu m'aider à :
1. Identifier les colonnes communes (clés de jointure potentielles)
2. Repérer d'éventuelles incohérences
3. Suggérer comment combiner ces sources
```

---

## 6. Premiers réflexes après chargement

Une fois vos données chargées, effectuez systématiquement ces vérifications :

### Checklist de validation post-extraction

Pour chaque DataFrame chargé :

- [ ] **Dimensions** : Nombre de lignes et colonnes cohérent ?
- [ ] **Types** : Les colonnes ont-elles les bons types (int, float, str, datetime) ?
- [ ] **Aperçu** : Les premières lignes semblent-elles correctes ?
- [ ] **Valeurs manquantes** : Y a-t-il des NaN/None ? Où ?
- [ ] **Valeurs uniques** : Les colonnes d'ID sont-elles uniques ?

### Questions à documenter

Pour chaque source, notez :

1. **Clé primaire** : Quelle colonne identifie de façon unique chaque ligne ?
2. **Clés de jointure** : Quelle(s) colonne(s) permettront de relier cette source aux autres ?
3. **Période couverte** : Quelle plage temporelle couvrent les données ?
4. **Problèmes détectés** : Quels soucis avez-vous repérés dès le chargement ?

---

## 7. Checklist de validation de la phase

Avant de passer à la phase suivante, vérifiez :

### Extraction complète
- [ ] Toutes mes sources identifiées dans le cadrage sont chargées
- [ ] J'ai au moins 2 formats différents
- [ ] Le tableau récapitulatif est complété

### Qualité du chargement
- [ ] Aucune erreur lors du chargement
- [ ] Les types de données semblent corrects
- [ ] L'encodage est correct (pas de caractères bizarres)

### Documentation
- [ ] J'ai noté les clés de jointure potentielles
- [ ] J'ai listé les premiers problèmes repérés
- [ ] J'ai documenté les paramètres utilisés pour chaque chargement

---

## 8. Questions de réflexion

1. **Qualité des sources** : Parmi vos sources, laquelle vous semble la plus fiable ? La moins fiable ? Pourquoi ?

2. **Jointures à venir** : Comment allez-vous relier vos différentes sources ? Quelles colonnes serviront de "pont" ?

3. **Données manquantes** : Y a-t-il des données que vous auriez aimé avoir mais qui ne sont pas disponibles ?

4. **Granularité** : Vos sources ont-elles la même granularité (par jour, par transaction, par client) ?

---

## 9. Critères d'évaluation de cette phase

| Critère | Insuffisant | Satisfaisant | Excellent |
|---------|-------------|--------------|-----------|
| **Diversité des sources** | 1 seule source/format | 2-3 sources, 2 formats | 3+ sources, 3+ formats différents |
| **Qualité du chargement** | Erreurs non résolues | Chargement fonctionnel | Chargement optimisé, types corrects |
| **Documentation** | Pas de documentation | Tableau récapitulatif | Récap + clés + problèmes identifiés |
| **Utilisation IA** | Non utilisée | Utilisée pour débugger | Utilisée proactivement |

---

## Prochaine étape

Vos données sont chargées ! Passez à la **Phase 2 : EDA Diagnostique** pour évaluer la qualité de vos données.

---

*Ce guide fait partie du workflow « Projet Final ML ». Consultez le fichier README pour la vue d'ensemble.*
