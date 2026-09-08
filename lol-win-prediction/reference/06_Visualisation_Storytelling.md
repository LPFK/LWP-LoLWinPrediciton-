# Phase 6 : Visualisation et Storytelling

**Objectif** : Créer des visualisations claires et impactantes qui racontent une histoire avec vos données.

---

## Pourquoi la visualisation est cruciale

"Une image vaut mille mots" — mais une mauvaise visualisation peut induire en erreur.

Vos visualisations doivent :

- **Clarifier** : Rendre compréhensible en un coup d'œil
- **Convaincre** : Appuyer vos insights avec évidence
- **Mémoriser** : Laisser une impression durable

---

## 1. Guide de choix du type de graphique

### Matrice de décision

| Je veux montrer... | Type de graphique | Exemple |
|--------------------|-------------------|---------|
| Une **distribution** | Histogramme, Boxplot | Répartition des âges |
| Une **composition** | Camembert, Barres empilées | Parts de marché |
| Une **comparaison** | Barres (horizontales/verticales) | CA par catégorie |
| Une **évolution** | Ligne, Aire | Ventes mensuelles |
| Une **relation** | Scatter plot, Heatmap | Corrélation prix/ventes |
| Une **répartition géographique** | Carte | Ventes par région |
| Un **classement** | Barres horizontales triées | Top 10 produits |

### Aide au choix détaillé

#### Pour les données catégorielles

| Nombre de catégories | Recommandation |
|---------------------|----------------|
| 2-5 | Camembert ou Donut |
| 5-10 | Barres horizontales |
| > 10 | Top N + "Autres" ou treemap |

#### Pour les séries temporelles

| Type de pattern | Recommandation |
|-----------------|----------------|
| Tendance simple | Ligne |
| Plusieurs séries | Lignes multiples (max 4-5) |
| Composition qui évolue | Aires empilées |
| Saisonnalité | Heatmap calendrier |

#### Pour les comparaisons

| Ce qu'on compare | Recommandation |
|------------------|----------------|
| Valeurs absolues | Barres |
| Parts/pourcentages | Barres empilées 100% |
| Avant/après | Barres groupées |
| Plusieurs dimensions | Radar (avec parcimonie) |

---

## 2. Principes de design

### Les 5 règles d'or

| Règle | Description | Exemple |
|-------|-------------|---------|
| **Simplicité** | Éliminer le superflu | Pas de 3D, pas de décoration inutile |
| **Lisibilité** | Textes lisibles, échelles claires | Police ≥ 10pt, axes labellisés |
| **Honnêteté** | Ne pas déformer les données | Axes commençant à 0 pour les barres |
| **Focus** | Guider l'œil vers l'essentiel | Mise en évidence des insights clés |
| **Cohérence** | Style uniforme | Mêmes couleurs, mêmes polices |

### Ce qu'il faut éviter

| Mauvaise pratique | Problème | Alternative |
|-------------------|----------|-------------|
| Effets 3D | Déforme les proportions | Rester en 2D |
| Trop de couleurs | Confusion | Max 5-6 couleurs |
| Axes tronqués (barres) | Exagère les différences | Commencer à 0 |
| Légendes loin du graphique | Difficile à lire | Légende intégrée ou labels directs |
| Double axe Y | Peut induire en erreur | Deux graphiques séparés |
| Camembert > 5 parts | Illisible | Barres horizontales |

### Palette de couleurs recommandée

| Usage | Couleurs |
|-------|----------|
| **Catégories distinctes** | Palette qualitative (bleu, orange, vert, rouge, violet) |
| **Valeurs ordonnées** | Dégradé (du clair au foncé) |
| **Divergent** (positif/négatif) | Rouge-Blanc-Bleu ou similaire |
| **Mise en évidence** | Gris pour le contexte, couleur vive pour le focus |

---

## 3. Checklist d'une bonne visualisation

### Avant de créer

- [ ] Quel message précis doit transmettre ce graphique ?
- [ ] Quel type de graphique est le plus adapté ?
- [ ] Qui est l'audience ? (technique vs business)

### Éléments obligatoires

- [ ] **Titre** : Clair, informatif, exprime le message clé
- [ ] **Axes labellisés** : Avec unités (€, %, nombre)
- [ ] **Source** : D'où viennent les données
- [ ] **Période** : Quand (si temporel)
- [ ] **Légende** : Si plusieurs séries/catégories

### Vérifications finales

- [ ] Le message est-il compréhensible en 5 secondes ?
- [ ] Les proportions sont-elles respectées ?
- [ ] Les couleurs sont-elles distinguables (même en noir et blanc) ?
- [ ] La police est-elle lisible ?
- [ ] Y a-t-il des éléments superflus à retirer ?

---

## 4. Anatomie d'une bonne visualisation

### Structure type

```
┌─────────────────────────────────────────────────────┐
│  TITRE : Message principal du graphique             │
│  Sous-titre : Contexte ou précision                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Axe Y    ┌─────────────────────────────┐           │
│  (unité)  │                             │          │
│           │      [GRAPHIQUE]            │ Légende  │
│           │                             │          │
│           └─────────────────────────────┘           │
│                    Axe X (unité)                    │
│                                                     │
├─────────────────────────────────────────────────────┤
│  Annotation : Insight clé mis en évidence           │
│  Source : Origine des données | Période             │
└─────────────────────────────────────────────────────┘
```

### Exemples de bons titres

| Type | Mauvais titre | Bon titre |
|------|---------------|-----------|
| Descriptif | "Ventes" | "Ventes mensuelles 2024 (en M€)" |
| Insight | "CA par catégorie" | "Les smartphones génèrent 45% du CA" |
| Question | "Répartition clients" | "Qui sont nos clients VIP ?" |

---

## 5. Storytelling avec les données

### Structure narrative

Un bon récit data suit cette structure :

```
1. CONTEXTE     → Planter le décor
   "TechShop souhaite optimiser sa stratégie produit..."

2. TENSION      → Poser le problème/la question
   "Mais quelles catégories génèrent vraiment de la valeur ?"

3. DONNÉES      → Présenter les preuves
   [Visualisations avec insights]

4. RÉSOLUTION   → Répondre avec des insights
   "Les smartphones représentent 45% du CA mais..."

5. ACTION       → Recommander
   "Nous recommandons de..."
```

### Les 3 types de récits data

| Type | Objectif | Structure |
|------|----------|-----------|
| **Exploratoire** | Découvrir | "Voici ce que les données montrent..." |
| **Explicatif** | Convaincre | "Voici pourquoi nous recommandons..." |
| **Prescriptif** | Décider | "Voici les options et notre recommandation..." |

### Techniques de storytelling

| Technique | Description | Exemple |
|-----------|-------------|---------|
| **Contraste** | Montrer avant/après ou différences | "Web: 60% vs Mobile: 40%" |
| **Progression** | Raconter une évolution | "De janvier à décembre, le CA a augmenté de..." |
| **Zoom** | Du général au particulier | "Global → Catégorie → Produit" |
| **Comparaison** | Mettre en perspective | "3x plus que la moyenne du marché" |
| **Personnification** | Donner vie aux données | "Le client type achète..." |

---

## 6. Template de visualisation

### Pour chaque visualisation, documentez

```
## Visualisation #X : [Titre]

### Objectif
- Message à transmettre : _________________________________
- Audience cible : _________________________________

### Spécifications
- Type de graphique : _________________________________
- Variables : _________________________________
- Période : _________________________________

### Design
- Couleurs utilisées : _________________________________
- Annotations : _________________________________

### Insight mis en évidence
[L'insight principal que le lecteur doit retenir]

### Fichier
- Nom : _________________________________
- Format : _________________________________
```

---

## 7. Dashboard : assembler vos visualisations

### Principes d'un bon dashboard

| Principe | Description |
|----------|-------------|
| **Hiérarchie** | Les infos importantes en haut/gauche |
| **Flow** | Lecture naturelle (Z ou F pattern) |
| **Espacement** | Aérer, ne pas surcharger |
| **Cohérence** | Style uniforme |
| **Interactivité** | Filtres si pertinent |

### Structure type d'un dashboard

```
┌─────────────────────────────────────────────────────────┐
│  TITRE DU DASHBOARD                       Filtres ▼     │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │   KPI   │  │   KPI   │  │   KPI   │  │   KPI   │    │
│  │  12.5M€ │  │   +15%  │  │  4,500  │  │   85%   │    │
│  │   CA    │  │  vs N-1 │  │ Clients │  │  Satisf │    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │
├───────────────────────────────┬─────────────────────────┤
│                               │                         │
│   GRAPHIQUE PRINCIPAL         │   GRAPHIQUE SECONDAIRE  │
│   (tendance, évolution)       │   (répartition)         │
│                               │                         │
├───────────────────────────────┴─────────────────────────┤
│                                                         │
│   GRAPHIQUE DÉTAILLÉ (comparaisons, détails)           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Checklist dashboard

- [ ] KPIs clés visibles immédiatement
- [ ] Graphique principal met en avant l'insight majeur
- [ ] Navigation logique du général au détail
- [ ] Pas de surcharge (max 6-8 éléments visuels)
- [ ] Cohérence visuelle (couleurs, polices)

---

## 8. Utiliser l'IA pour vous aider

### Prompt 1 : Choisir le bon graphique

```
Je souhaite visualiser les données suivantes :
- Variable(s) : [DESCRIPTION]
- Type de données : [Catégoriel/Numérique/Temporel]
- Message à transmettre : [CE QUE JE VEUX MONTRER]
- Audience : [Technique/Business/Grand public]

Peux-tu me recommander :
1. Le type de graphique le plus adapté
2. Les alternatives possibles
3. Les erreurs à éviter pour ce type de visualisation
```

### Prompt 2 : Critiquer une visualisation

```
J'ai créé une visualisation avec les caractéristiques suivantes :
- Type : [TYPE DE GRAPHIQUE]
- Données : [DESCRIPTION]
- Titre : [VOTRE TITRE]
- Éléments inclus : [AXES, LÉGENDE, COULEURS...]

[SI POSSIBLE, DÉCRIRE OU JOINDRE L'IMAGE]

Peux-tu :
1. Identifier les points forts
2. Suggérer des améliorations
3. Vérifier si le message est clair
4. Proposer un meilleur titre si nécessaire
```

### Prompt 3 : Construire un récit data

```
J'ai les insights suivants à présenter :
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

Contexte : [DOMAINE, AUDIENCE, OBJECTIF]

Peux-tu m'aider à :
1. Structurer ces insights en un récit cohérent
2. Proposer un ordre de présentation
3. Suggérer des transitions entre les points
4. Identifier le "hook" (accroche) le plus impactant
```

### Prompt 4 : Rédiger des annotations

```
Mon graphique montre [DESCRIPTION DU GRAPHIQUE].

L'insight principal est : [VOTRE INSIGHT]

Peux-tu me proposer :
1. Un titre percutant (max 10 mots)
2. Une annotation explicative (1-2 phrases)
3. Une légende claire
4. Un call-to-action si pertinent
```

---

## 9. Checklist de validation de la phase

Avant de passer à la phase suivante, vérifiez :

### Visualisations créées

- [ ] Au moins 5-7 visualisations produites
- [ ] Chaque question business a une visualisation associée
- [ ] Un dashboard ou une vue d'ensemble existe

### Qualité

- [ ] Chaque visualisation a un titre clair
- [ ] Les axes sont labellisés avec unités
- [ ] Les sources et périodes sont indiquées
- [ ] Pas de mauvaises pratiques (3D, axes tronqués...)

### Storytelling

- [ ] Un fil narratif relie les visualisations
- [ ] Les insights clés sont mis en évidence
- [ ] L'audience peut comprendre sans explication orale

---

## 10. Questions de réflexion

1. **Impact** : Quelle visualisation est la plus impactante ? Pourquoi ?

2. **Clarté** : Quelqu'un qui ne connaît pas votre projet pourrait-il comprendre vos graphiques ?

3. **Choix** : Y a-t-il une visualisation que vous auriez faite différemment avec plus de temps ?

4. **Récit** : Quel est le "fil rouge" de votre histoire data ?

---

## 11. Critères d'évaluation de cette phase

| Critère | Insuffisant | Satisfaisant | Excellent |
|---------|-------------|--------------|-----------|
| **Quantité** | < 3 visualisations | 5-7 visualisations | 7+ visualisations variées |
| **Choix des graphiques** | Types inadaptés | Types appropriés | Types optimaux + justifiés |
| **Design** | Mauvaises pratiques | Propre et lisible | Professionnel et impactant |
| **Storytelling** | Pas de fil conducteur | Récit présent | Récit captivant et structuré |
| **Utilisation IA** | Non utilisée | Pour améliorer | Intégrée dans la conception |

---

## Prochaine étape

Vos visualisations sont prêtes et vos données sont comprises. Passez à la **Phase 7 : Modélisation Machine Learning** pour construire votre modèle prédictif.

---

*Ce guide fait partie du workflow « Projet Final ML ». Consultez le fichier README pour la vue d'ensemble.*
