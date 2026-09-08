# Phase 9 : Présentation et Soutenance

**Objectif** : Préparer vos livrables finaux et présenter vos résultats de façon professionnelle et impactante.

---

## Les livrables attendus

À la fin de votre projet, vous devez produire :

| Livrable | Format | Description |
|----------|--------|-------------|
| **Dataset final** | .parquet ou .csv | Données nettoyées et enrichies |
| **Data Dictionary** | .md ou .pdf | Documentation du dataset |
| **Notebook** | .ipynb | Code reproductible commenté |
| **Visualisations** | .png ou .pdf | Dashboard ou graphiques clés |
| **Modèle entraîné** | .joblib | Pipeline complète (preprocessing + modèle) |
| **Présentation** | .pptx ou .pdf | Synthèse pour le public cible |

---

## 1. Structure de la présentation

### Template de présentation

```
SLIDE 1 : Titre
─────────────────
[Titre du projet]
[Votre nom]
[Date]

SLIDE 2 : Contexte et objectifs
─────────────────
- Le problème/la question
- Pourquoi c'est important
- Ce que vous avez cherché à faire

SLIDE 3 : Les données
─────────────────
- Sources utilisées
- Volume (lignes, colonnes, période)
- Principaux défis qualité

SLIDE 4-8 : Insights clés (1 slide par insight)
─────────────────
Pour chaque insight :
- La question business
- La visualisation clé
- Le chiffre qui marque
- L'implication

SLIDE 9 : Le modèle prédictif
─────────────────
- La question prédictive et la cible
- Les modèles comparés + la métrique choisie (et pourquoi)
- Baseline vs modèle retenu : le gain
- Le score de test, une seule fois, honnêtement
- Les features les plus importantes
- Les limites : où le modèle se trompe, et pour qui c'est grave

SLIDE 10 : Synthèse
─────────────────
- Les 3 chiffres à retenir
- Le message principal

SLIDE 11 : Recommandations
─────────────────
- Actions concrètes proposées
- Prochaines étapes

SLIDE 12 : Annexes (optionnel)
─────────────────
- Méthodologie détaillée
- Limites de l'analyse
- Sources complémentaires
```

---

## 2. L'art de l'Executive Summary

### Qu'est-ce qu'un Executive Summary ?

Un résumé concis (1 page max) qui permet à un décideur de comprendre l'essentiel sans lire tout le rapport.

### Structure de l'Executive Summary

```markdown
# Executive Summary : [Titre du projet]

## Contexte
[2-3 phrases sur le problème/l'opportunité]

## Objectif
[1 phrase sur ce que l'analyse cherchait à déterminer]

## Méthodologie
[2-3 phrases sur les données et l'approche]

## Principaux résultats
1. [Insight 1 + chiffre clé]
2. [Insight 2 + chiffre clé]
3. [Insight 3 + chiffre clé]

## Recommandations
1. [Action 1]
2. [Action 2]
3. [Action 3]

## Prochaines étapes
[Ce qui reste à faire ou à approfondir]
```

### Template à compléter

```
En analysant [QUOI] sur la période [PÉRIODE], nous avons cherché à
répondre à [QUESTIONS PRINCIPALES].

Les données proviennent de [SOURCES] et représentent [VOLUME].

Les principaux enseignements sont :
• [INSIGHT 1] : [CHIFFRE]
• [INSIGHT 2] : [CHIFFRE]
• [INSIGHT 3] : [CHIFFRE]

Nous recommandons de [ACTIONS].

Les limites de cette analyse incluent [LIMITES], ce qui suggère
d'approfondir [PROCHAINES ÉTAPES].
```

---

## 3. Les 3 chiffres qui marquent

### Comment choisir vos chiffres clés

Un bon chiffre clé est :

- **Surprenant** : Différent des attentes
- **Significatif** : Impact business réel
- **Simple** : Compréhensible immédiatement
- **Mémorable** : Facile à retenir

### Types de chiffres impactants

| Type | Exemple | Effet |
|------|---------|-------|
| **Absolu impressionnant** | "12 millions d'euros" | Donne l'échelle |
| **Pourcentage frappant** | "45% du CA" | Met en perspective |
| **Multiplicateur** | "3x plus que" | Crée le contraste |
| **Évolution** | "+25% vs N-1" | Montre le changement |
| **Ratio simple** | "1 client sur 4" | Facile à visualiser |

### Template des 3 chiffres

```
## Mes 3 chiffres clés

1. Chiffre : _______________
   Message : _______________
   Impact : _______________

2. Chiffre : _______________
   Message : _______________
   Impact : _______________

3. Chiffre : _______________
   Message : _______________
   Impact : _______________
```

---

## 4. Formuler des recommandations actionnables

### Caractéristiques d'une bonne recommandation

| Critère | Mauvais exemple | Bon exemple |
|---------|-----------------|-------------|
| **Spécifique** | "Améliorer les ventes" | "Augmenter le budget marketing mobile de 20%" |
| **Mesurable** | "Fidéliser les clients" | "Réduire le churn de 15% en ciblant les clients à risque" |
| **Basée sur les données** | "Il faudrait..." | "Les données montrent que... donc nous recommandons..." |
| **Priorisée** | Liste sans ordre | "En priorité : 1. ... 2. ... 3. ..." |

### Template de recommandation

```
RECOMMANDATION #X

Insight source : [L'analyse qui justifie cette recommandation]

Action proposée : [Ce qu'il faut faire concrètement]

Résultat attendu : [L'impact espéré, quantifié si possible]

Priorité : ☐ Haute  ☐ Moyenne  ☐ Basse

Prérequis : [Ce qui est nécessaire pour mettre en œuvre]
```

---

## 5. Mentionner les limites

### Pourquoi mentionner les limites ?

- Montre votre rigueur intellectuelle
- Prévient les mauvaises interprétations
- Identifie les axes d'amélioration
- Renforce la crédibilité de vos conclusions solides

### Types de limites à mentionner

| Type | Exemple |
|------|---------|
| **Données** | "Données manquantes sur certaines périodes" |
| **Périmètre** | "Analyse limitée aux clients français" |
| **Méthodologie** | "Corrélation observée, causalité non démontrée" |
| **Temporalité** | "Période atypique (COVID, etc.)" |
| **Biais potentiel** | "Surreprésentation de certains segments" |

### Comment formuler une limite

```
Limite : [Description de la limite]

Impact potentiel : [Comment cela pourrait affecter les conclusions]

Mitigation : [Ce qui a été fait pour limiter l'impact]

Recommandation : [Ce qu'il faudrait faire pour lever cette limite]
```

---

## 6. Grille d'auto-évaluation

### Évaluez votre projet

| Critère | Note (1-5) | Commentaire |
|---------|------------|-------------|
| **Cadrage** | ⭐⭐⭐⭐⭐ | _______________ |
| **Extraction** | ⭐⭐⭐⭐⭐ | _______________ |
| **Diagnostic qualité** | ⭐⭐⭐⭐⭐ | _______________ |
| **Nettoyage** | ⭐⭐⭐⭐⭐ | _______________ |
| **Transformation** | ⭐⭐⭐⭐⭐ | _______________ |
| **Analyse** | ⭐⭐⭐⭐⭐ | _______________ |
| **Visualisation** | ⭐⭐⭐⭐⭐ | _______________ |
| **Modélisation ML** | ⭐⭐⭐⭐⭐ | _______________ |
| **Documentation** | ⭐⭐⭐⭐⭐ | _______________ |
| **Utilisation IA** | ⭐⭐⭐⭐⭐ | _______________ |

### Questions de réflexion métacognitive

1. **Apprentissage** : Qu'avez-vous appris de nouveau pendant ce projet ?

2. **Difficultés** : Quelle étape a été la plus difficile ? Pourquoi ?

3. **Fierté** : De quoi êtes-vous le plus fier dans ce projet ?

4. **Amélioration** : Si vous deviez refaire ce projet, que feriez-vous différemment ?

5. **Transfert** : Comment allez-vous utiliser ces compétences dans votre futur professionnel ?

---

## 7. Checklist finale des livrables

### Dataset final

- [ ] Format approprié (parquet/csv)
- [ ] Nommé selon la convention
- [ ] Vérifié (lisible, complet)

### Data Dictionary

- [ ] Toutes colonnes documentées
- [ ] Sources identifiées
- [ ] Transformations tracées

### Notebook

- [ ] Code exécutable de bout en bout
- [ ] Commentaires et markdown explicatifs
- [ ] Structuré logiquement

### Visualisations

- [ ] 5-7 visualisations minimum
- [ ] Titres et légendes présents
- [ ] Insights mis en évidence

### Modèle

- [ ] Pipeline complète sauvegardée en .joblib
- [ ] Baseline calculée et comparée
- [ ] Au moins 3 modèles comparés, tableau de résultats à l'appui
- [ ] Score de test reporté une seule fois
- [ ] Features importantes interprétées

### Présentation

- [ ] Structure claire (intro → insights → recommandations)
- [ ] 3 chiffres clés identifiés
- [ ] Limites mentionnées
- [ ] Recommandations actionnables

---

## 8. Utiliser l'IA pour vous aider

### Prompt 1 : Rédiger l'Executive Summary

```
Voici les principaux résultats de mon analyse :

Contexte : [DOMAINE, PROBLÉMATIQUE]

Données : [SOURCES, VOLUME, PÉRIODE]

Insights :
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

Peux-tu m'aider à rédiger un Executive Summary professionnel d'une page maximum, incluant contexte, méthodologie, résultats clés et recommandations ?
```

### Prompt 2 : Améliorer une recommandation

```
J'ai formulé la recommandation suivante :
[VOTRE RECOMMANDATION]

Basée sur cet insight :
[L'INSIGHT SOURCE]

Peux-tu m'aider à :
1. Rendre cette recommandation plus spécifique et actionnable
2. Quantifier l'impact attendu si possible
3. Identifier les prérequis de mise en œuvre
4. Proposer une formulation plus impactante
```

### Prompt 3 : Préparer les questions/objections

```
Je vais présenter mon analyse avec les conclusions suivantes :
1. [Conclusion 1]
2. [Conclusion 2]
3. [Conclusion 3]

Audience : [DESCRIPTION DE L'AUDIENCE]

Peux-tu :
1. Anticiper les questions qu'on pourrait me poser
2. Identifier les objections possibles
3. Me suggérer des réponses ou clarifications
4. Identifier les points faibles de mon argumentation
```

### Prompt 4 : Synthétiser pour différentes audiences

```
Voici le résumé de mon analyse :
[VOTRE RÉSUMÉ]

Peux-tu m'aider à adapter ce message pour :
1. Un comité de direction (2 minutes max)
2. Une équipe technique (focus méthodologie)
3. Une équipe métier (focus impact opérationnel)
```

---

## 9. Conseils pour la présentation orale

### Structure du pitch (7 minutes)

| Temps | Contenu |
|-------|---------|
| 0:00-0:30 | Accroche + contexte |
| 0:30-1:00 | Problématique et objectifs |
| 1:00-3:00 | 3 insights clés (30-40s chacun) |
| 3:00-5:00 | Le modèle : démarche, comparaison, score, limites |
| 5:00-6:00 | Recommandations |
| 6:00-7:00 | Conclusion + questions du jury |

### Do's and Don'ts

| ✅ À faire | ❌ À éviter |
|-----------|-------------|
| Commencer par l'insight principal | Commencer par la méthodologie |
| Utiliser des chiffres mémorables | Noyer dans les détails |
| Raconter une histoire | Lire les slides |
| Anticiper les questions | Être sur la défensive |
| Mentionner les limites proactivement | Cacher les faiblesses |

---

## 10. Questions de réflexion finale

1. **Message principal** : Si votre audience ne devait retenir qu'une seule chose, ce serait quoi ?

2. **Impact** : En quoi votre analyse peut-elle changer les décisions de votre audience ?

3. **Crédibilité** : Qu'est-ce qui rend vos conclusions fiables ?

4. **Suite** : Quelle serait la prochaine analyse logique à mener ?

5. **Apprentissage** : Qu'avez-vous appris sur vous-même en réalisant ce projet ?

---

## 11. Critères d'évaluation de cette phase

| Critère | Insuffisant | Satisfaisant | Excellent |
|---------|-------------|--------------|-----------|
| **Livrables** | Incomplets | Tous présents | Complets + soignés |
| **Executive Summary** | Absent ou confus | Clair | Impactant et professionnel |
| **Chiffres clés** | Mal choisis | Pertinents | Mémorables et bien contextualisés |
| **Recommandations** | Vagues | Spécifiques | Actionnables et priorisées |
| **Limites** | Non mentionnées | Listées | Analysées avec mitigation |
| **Auto-évaluation** | Non faite | Superficielle | Réflexive et constructive |

---

## Félicitations

Vous avez terminé votre projet data pipeline de bout en bout.

Vous avez démontré votre capacité à :

- ✅ Extraire des données de sources multiples
- ✅ Diagnostiquer et nettoyer des données
- ✅ Transformer et enrichir un dataset
- ✅ Analyser pour répondre à des questions business
- ✅ Visualiser et communiquer vos résultats
- ✅ Construire, comparer et évaluer honnêtement un modèle de Machine Learning
- ✅ Interpréter un modèle et en reconnaître les limites
- ✅ Documenter votre travail
- ✅ Utiliser l'IA comme assistant

**Ce sont les compétences fondamentales d'un Data Scientist.**

---

*Ce guide fait partie du workflow « Projet Final ML ». Consultez le fichier README pour la vue d'ensemble.*
