# Phase 0 : Introduction et Cadrage du Projet

**Objectif** : Choisir un sujet pertinent et définir clairement le périmètre de votre projet data.

---

## Pourquoi cette étape est cruciale

Un projet data réussi commence toujours par un bon cadrage. Sans questions business claires, vous risquez de :
- Collecter des données inutiles
- Passer du temps sur des analyses sans impact
- Ne pas pouvoir conclure à la fin du projet

Prenez le temps de bien définir votre sujet — c'est un investissement qui vous fera gagner du temps par la suite.

---

## 1. Choisir un bon sujet

### Critères d'un bon sujet de projet data

| Critère | Description | Exemple |
|---------|-------------|---------|
| **Intérêt personnel** | Un sujet qui vous motive | Sport, musique, santé... |
| **Disponibilité des données** | Des données accessibles et exploitables | APIs publiques, Kaggle, Open Data |
| **Diversité des sources** | Au moins 2-3 sources différentes | CSV + API + Excel |
| **Questions business claires** | Des problématiques auxquelles répondre | "Quels facteurs influencent X ?" |
| **Faisabilité** | Réalisable dans le temps imparti | Éviter les sujets trop ambitieux |

### Questions à vous poser

- [ ] Ce sujet m'intéresse-t-il vraiment ?
- [ ] Ai-je identifié au moins 2 sources de données accessibles ?
- [ ] Puis-je formuler 3 à 5 questions auxquelles les données peuvent répondre ?
- [ ] Le périmètre est-il suffisamment délimité ?

---

## 2. Template de définition du contexte

Complétez ce template pour cadrer votre projet :

### Mon projet en quelques lignes

```
Domaine : _________________________________
(Ex : E-commerce, Santé, Sport, Finance, Culture...)

Sujet précis : _________________________________
(Ex : Analyse des performances des joueurs de Ligue 1)

Contexte / Problématique : _________________________________
_________________________________
(Ex : Un club de football souhaite optimiser son recrutement en identifiant
les caractéristiques des joueurs les plus performants)

Public cible : _________________________________
(Ex : Recruteurs sportifs, fans, analystes)

Période d'analyse : _________________________________
(Ex : Saison 2023-2024)
```

---

## 3. Formuler vos questions business

Une bonne question business est :
- **Spécifique** : Pas trop vague
- **Mesurable** : Les données peuvent y répondre
- **Actionnable** : La réponse permet de prendre une décision

### Template de questions business

Formulez 3 à 5 questions auxquelles votre projet doit répondre :

| # | Question business | Impact potentiel |
|---|-------------------|------------------|
| 1 | _________________________________ | _________________________________ |
| 2 | _________________________________ | _________________________________ |
| 3 | _________________________________ | _________________________________ |
| 4 | _________________________________ | _________________________________ |
| 5 | _________________________________ | _________________________________ |

### Exemples par domaine

**Sport** :
- Quels attributs distinguent les meilleurs buteurs ?
- Existe-t-il une corrélation entre l'âge et la performance ?

**E-commerce** :
- Quelles catégories de produits génèrent le plus de marge ?
- Quels sont les facteurs de fidélisation client ?

**Santé** :
- Quels facteurs sont corrélés à une pathologie donnée ?
- Comment évoluent les indicateurs au fil du temps ?

**Finance** :
- Quels secteurs ont les meilleures performances ?
- Existe-t-il des patterns saisonniers dans les cours ?

---

## 3 bis. Formuler votre question PRÉDICTIVE

Votre projet ne s'arrête pas à l'analyse : il doit aboutir à un **modèle de Machine Learning**. Il vous faut donc, en plus des questions business, **une question prédictive et une colonne cible**.

### Différence entre question business et question prédictive

| | Question business (Phase 5) | Question prédictive (Phase 7) |
|---|---|---|
| Nature | Décrit ce qui s'est passé | Anticipe ce qui va se passer |
| Exemple | « Quels clients ont résilié cette année ? » | « Peut-on prédire qui va résilier ? » |
| Livrable | Un insight chiffré | Un modèle entraîné et évalué |

### Template

```
Question prédictive : _________________________________
(Ex : « Peut-on prédire le prix de vente d'un logement à partir de ses caractéristiques ? »)

Colonne cible (y) : _________________________________
(Elle DOIT exister dans vos données, ou être calculable à partir d'elles)

Type de problème :  ☐ Classification binaire
                    ☐ Classification multi-classes
                    ☐ Régression

Répartition de la cible : _________________________________
(Classes équilibrées ? Distribution de la variable continue ?)

À qui servirait cette prédiction : _________________________________
```

> ⚠️ **Si vous n'arrivez pas à nommer une colonne cible, votre sujet n'est pas encore valide.** Changez de dataset ou reformulez avant d'aller plus loin.

---

## 3 ter. Validation obligatoire du dataset par le formateur

Avant de démarrer la Phase 1, votre sujet doit être **validé en séance**. Critères non négociables :

| Critère | Seuil |
|---|---|
| Volume | ≥ 10 000 lignes |
| Colonnes exploitables | ≥ 8 (dont au moins une catégorielle) |
| Colonne cible | Identifiée, présente dans les données |
| Type de problème | Classification ou régression, tranché |
| Accessibilité | Données **déjà téléchargées** sur votre machine |
| Répartition | Pas de classe ultra-minoritaire (< 5 %) sans stratégie prévue |

**Sujets refusés d'office** : données à scraper depuis zéro, données nécessitant une inscription payante, séries temporelles pures (hors programme), images ou texte brut (hors programme), dataset < 1 000 lignes.

---

## 4. Identifier vos sources de données

### Checklist des sources à rechercher

- [ ] **Source 1 - Principale** : _________________________________
  - Format : ☐ CSV ☐ Excel ☐ JSON ☐ API ☐ SQL ☐ Parquet ☐ Autre
  - Origine : _________________________________
  - Accès : ☐ Libre ☐ Inscription requise ☐ Payant

- [ ] **Source 2 - Complémentaire** : _________________________________
  - Format : ☐ CSV ☐ Excel ☐ JSON ☐ API ☐ SQL ☐ Parquet ☐ Autre
  - Origine : _________________________________
  - Accès : ☐ Libre ☐ Inscription requise ☐ Payant

- [ ] **Source 3 - Enrichissement** : _________________________________
  - Format : ☐ CSV ☐ Excel ☐ JSON ☐ API ☐ SQL ☐ Parquet ☐ Autre
  - Origine : _________________________________
  - Accès : ☐ Libre ☐ Inscription requise ☐ Payant

### Où trouver des données ?

| Plateforme | Type de données | Lien |
|------------|-----------------|------|
| Kaggle | Datasets variés, compétitions | kaggle.com/datasets |
| Data.gouv.fr | Open Data français | data.gouv.fr |
| UCI ML Repository | Datasets académiques | archive.ics.uci.edu |
| APIs publiques | Données en temps réel | Voir Annexe |
| Google Dataset Search | Moteur de recherche | datasetsearch.research.google.com |

---

## 5. Utiliser l'IA pour vous aider

### Prompt 1 : Brainstormer des questions business

```
Je travaille sur un projet data dans le domaine [VOTRE DOMAINE].

Mon sujet est : [VOTRE SUJET]

Contexte : [VOTRE CONTEXTE EN 2-3 PHRASES]

Peux-tu me suggérer 5 questions business pertinentes et actionnables
auxquelles je pourrais répondre avec des données ? Pour chaque question,
indique quel type de données serait nécessaire.
```

### Prompt 2 : Valider la faisabilité

```
Je souhaite réaliser un projet data sur [VOTRE SUJET].

Voici mes questions business :
1. [Question 1]
2. [Question 2]
3. [Question 3]

Voici les sources de données que j'ai identifiées :
- [Source 1]
- [Source 2]

Peux-tu évaluer la faisabilité de ce projet ? Quels risques ou difficultés
anticipes-tu ? Y a-t-il des sources de données complémentaires que tu
recommanderais ?
```

### Prompt 3 : Affiner le périmètre

```
Mon projet data porte sur [SUJET LARGE].

Je dispose de [X semaines/jours] pour le réaliser.

Peux-tu m'aider à délimiter un périmètre réaliste ? Quels aspects
devrais-je prioriser et lesquels pourrais-je exclure pour une première
version ?
```

---

## 6. Checklist de validation du cadrage

Avant de passer à la phase suivante, vérifiez que vous pouvez cocher toutes ces cases :

### Sujet et contexte
- [ ] J'ai choisi un domaine qui m'intéresse
- [ ] J'ai défini un sujet précis (pas trop large)
- [ ] J'ai rédigé le contexte/la problématique
- [ ] J'ai identifié mon public cible

### Questions business
- [ ] J'ai formulé au moins 3 questions business
- [ ] Mes questions sont spécifiques et mesurables
- [ ] Les réponses à ces questions ont un impact concret

### Question prédictive
- [ ] J'ai formulé une question prédictive claire
- [ ] J'ai identifié la colonne cible, elle existe bien dans mes données
- [ ] J'ai tranché : classification ou régression
- [ ] J'ai regardé la répartition de ma cible
- [ ] Mon dataset a été **validé par le formateur**

### Sources de données
- [ ] J'ai identifié au moins 2 sources de données
- [ ] J'ai vérifié que les données sont accessibles
- [ ] J'ai au moins 2 formats différents (CSV, JSON, Excel, API...)
- [ ] Les données couvrent la période souhaitée

### Faisabilité
- [ ] Le projet est réalisable dans le temps imparti
- [ ] J'ai utilisé l'IA pour valider/affiner mon cadrage

---

## 7. Questions de réflexion

Prenez quelques minutes pour réfléchir à ces questions :

1. **Pourquoi ce sujet ?** Qu'est-ce qui vous motive personnellement dans ce choix ?

2. **Qui bénéficierait de vos analyses ?** Imaginez une personne concrète qui utiliserait vos résultats.

3. **Quel serait l'insight le plus impactant ?** Si vous ne pouviez répondre qu'à une seule question, laquelle choisiriez-vous ?

4. **Quelles sont les limites prévisibles ?** Quels aspects de votre sujet ne pourrez-vous pas couvrir avec les données disponibles ?

---

## 8. Critères d'évaluation de cette phase

| Critère | Insuffisant | Satisfaisant | Excellent |
|---------|-------------|--------------|-----------|
| **Choix du sujet** | Sujet vague ou trop ambitieux | Sujet clair et réalisable | Sujet original, bien délimité, motivant |
| **Questions business** | < 3 questions ou questions floues | 3-4 questions claires | 5 questions SMART avec impact identifié |
| **Sources de données** | 1 seule source | 2-3 sources identifiées | 3+ sources variées, accessibilité vérifiée |
| **Utilisation IA** | Non utilisée | Utilisée pour 1 aspect | Utilisée stratégiquement pour cadrer |

---

## Prochaine étape

Une fois votre cadrage validé, passez à la **Phase 1 : Extraction Multi-Sources** pour collecter vos données.

---

*Ce guide fait partie du workflow « Projet Final ML ». Consultez le fichier README pour la vue d'ensemble.*
