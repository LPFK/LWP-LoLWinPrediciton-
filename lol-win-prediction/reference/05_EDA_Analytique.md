# Phase 5 : EDA Analytique

**Objectif** : Analyser vos données pour répondre aux questions business définies lors du cadrage, et formuler des insights actionnables.

---

## La différence avec l'EDA Diagnostique

| EDA Diagnostique (Phase 2) | EDA Analytique (Phase 5) |
|---------------------------|--------------------------|
| Trouver les **problèmes** | Trouver les **réponses** |
| "Mes données sont-elles propres ?" | "Que disent mes données ?" |
| Focus : qualité | Focus : business |
| Avant nettoyage | Après enrichissement |

---

## 1. Méthodologie : Question → Analyse → Insight → Action

### Le framework d'analyse

Pour chaque question business, suivez ce processus :

```
┌─────────────────┐
│   QUESTION      │  Quelle est la question business ?
│   BUSINESS      │
└────────┬────────┘
         ▼
┌─────────────────┐
│    ANALYSE      │  Quelle analyse permet d'y répondre ?
│    TECHNIQUE    │  (agrégation, corrélation, segmentation...)
└────────┬────────┘
         ▼
┌─────────────────┐
│    RÉSULTAT     │  Que montrent les données ?
│    BRUT         │  (chiffres, tableaux, graphiques)
└────────┬────────┘
         ▼
┌─────────────────┐
│    INSIGHT      │  Qu'est-ce que cela signifie ?
│    FORMULÉ      │  (interprétation, implications)
└────────┬────────┘
         ▼
┌─────────────────┐
│    ACTION       │
│    PROPOSÉE     │
└─────────────────┘
```

### Template d'analyse par question

```
## Question Business #X : [Votre question]

### Reformulation
- Question précise : _________________________________
- Métriques nécessaires : _________________________________
- Granularité : _________________________________

### Analyse effectuée
- Type d'analyse : _________________________________
- Variables utilisées : _________________________________
- Méthode : _________________________________

### Résultats bruts
[Tableau ou description des chiffres clés]

### Insight
[Ce que cela signifie en langage business]

### Recommandation
[Action concrète à entreprendre]

### Confiance
- Niveau de confiance : ☐ Faible ☐ Moyen ☐ Élevé
- Limites : _________________________________
```

---

## 2. Types d'analyses courantes

### 2.1 Analyse de distribution

**Question type** : "Comment se répartit X ?"

| Quoi analyser | Méthode | Ce que ça révèle |
|---------------|---------|------------------|
| Variable numérique | Histogramme, boxplot | Forme, tendance centrale, outliers |
| Variable catégorielle | Barres, camembert | Répartition entre catégories |
| Deux variables | Scatter plot | Relation entre variables |

**Checklist analyse de distribution**
- [ ] Calculer les statistiques descriptives (moyenne, médiane, écart-type)
- [ ] Visualiser la distribution
- [ ] Identifier la forme (normale, asymétrique, bimodale)
- [ ] Repérer les outliers
- [ ] Interpréter en termes business

---

### 2.2 Analyse de tendance temporelle

**Question type** : "Comment X évolue-t-il dans le temps ?"

| Granularité | Ce qu'on cherche | Exemple |
|-------------|------------------|---------|
| Quotidien | Patterns journaliers | Pics de trafic |
| Hebdomadaire | Effet jour de semaine | Weekend vs semaine |
| Mensuel | Saisonnalité | Fêtes, vacances |
| Annuel | Tendance long terme | Croissance |

**Checklist analyse temporelle**
- [ ] Agréger les données à la bonne granularité
- [ ] Visualiser l'évolution (ligne, aire)
- [ ] Identifier les tendances (hausse, baisse, stable)
- [ ] Repérer les saisonnalités
- [ ] Identifier les événements exceptionnels (pics, creux)

---

### 2.3 Analyse de corrélation

**Question type** : "Y a-t-il un lien entre X et Y ?"

| Type de variables | Méthode | Interprétation |
|-------------------|---------|----------------|
| Num. vs Num. | Corrélation Pearson | -1 à +1 |
| Cat. vs Num. | ANOVA, boxplots | Différence de moyennes |
| Cat. vs Cat. | Chi-2, heatmap | Association |

**Interprétation du coefficient de corrélation**

| Valeur | Interprétation |
|--------|----------------|
| 0.9 - 1.0 | Très forte corrélation positive |
| 0.7 - 0.9 | Forte corrélation positive |
| 0.4 - 0.7 | Corrélation modérée positive |
| 0.2 - 0.4 | Faible corrélation positive |
| -0.2 - 0.2 | Pas de corrélation |

**Attention** : Corrélation ≠ Causalité !

**Checklist analyse de corrélation**
- [ ] Calculer les coefficients de corrélation
- [ ] Visualiser les relations (scatter, heatmap)
- [ ] Identifier les corrélations significatives
- [ ] Vérifier la causalité potentielle
- [ ] Formuler avec prudence ("associé à" plutôt que "cause")

---

### 2.4 Analyse de segmentation

**Question type** : "Quels sont les différents profils de X ?"

| Approche | Description | Quand l'utiliser |
|----------|-------------|------------------|
| Règles métier | Critères prédéfinis | Segmentation connue |
| Quantiles | Découpage statistique | Pas de règle métier |
| Clustering | Algorithme | Découverte de profils |

**Segmentation RFM classique (clients)**
- **R**écence : Quand a-t-il acheté pour la dernière fois ?
- **F**réquence : Combien de fois a-t-il acheté ?
- **M**ontant : Combien a-t-il dépensé au total ?

**Checklist analyse de segmentation**
- [ ] Choisir les critères de segmentation
- [ ] Définir les seuils ou la méthode
- [ ] Créer les segments
- [ ] Profiler chaque segment (caractéristiques moyennes)
- [ ] Nommer les segments de façon explicite
- [ ] Visualiser la répartition

---

### 2.5 Analyse comparative

**Question type** : "X est-il différent de Y ?"

| Comparaison | Méthode | Exemple |
|-------------|---------|---------|
| Deux groupes | Test t, Mann-Whitney | Clients web vs mobile |
| Plusieurs groupes | ANOVA, Kruskal-Wallis | Performance par région |
| Avant/après | Test apparié | Impact d'une campagne |

**Checklist analyse comparative**
- [ ] Définir les groupes à comparer
- [ ] Calculer les métriques par groupe
- [ ] Visualiser les différences (boxplot, barres)
- [ ] Évaluer si la différence est significative
- [ ] Interpréter l'écart en termes business

---

### 2.6 Analyse de composition

**Question type** : "Quelle est la part de X dans Y ?"

| Ce qu'on mesure | Visualisation | Exemple |
|-----------------|---------------|---------|
| Parts de marché | Camembert, donut | CA par catégorie |
| Décomposition | Barres empilées | Coût vs Marge |
| Évolution des parts | Aires empilées | Mix produit sur l'année |

**Checklist analyse de composition**
- [ ] Calculer les parts (pourcentages)
- [ ] Vérifier que le total = 100%
- [ ] Visualiser les proportions
- [ ] Identifier les composantes dominantes
- [ ] Comparer l'évolution si pertinent

---

## 3. Comment quantifier un insight

### Les chiffres qui marquent

Un insight sans chiffre n'est qu'une opinion. Quantifiez systématiquement :

| Type de chiffre | Exemple | Impact |
|-----------------|---------|--------|
| **Valeur absolue** | "12M€ de CA" | Donne l'échelle |
| **Pourcentage** | "35% du total" | Met en perspective |
| **Variation** | "+15% vs N-1" | Montre l'évolution |
| **Ratio** | "3x plus que" | Compare |
| **Classement** | "1er sur 5" | Positionne |

### Template de quantification

```
L'insight : [Votre insight]

Les chiffres clés :
- Valeur principale : _____________
- En pourcentage : _______________
- Évolution : ___________________
- Comparaison : _________________
```

### Exemples d'insights bien quantifiés

❌ **Mauvais** : "Les smartphones sont notre meilleure catégorie"

✅ **Bon** : "Les smartphones représentent 45% de notre CA (5,4M€), soit 2,5x plus que la deuxième catégorie (Laptops). Cette part a augmenté de 8 points vs N-1."

---

## 4. Template de documentation des findings

### Synthèse des analyses

| # | Question Business | Insight Principal | Chiffre Clé | Confiance | Action |
|---|-------------------|-------------------|-------------|-----------|--------|
| 1 | _________________ | _________________ | ___________ | ☐☐☐ | ______ |
| 2 | _________________ | _________________ | ___________ | ☐☐☐ | ______ |
| 3 | _________________ | _________________ | ___________ | ☐☐☐ | ______ |
| 4 | _________________ | _________________ | ___________ | ☐☐☐ | ______ |
| 5 | _________________ | _________________ | ___________ | ☐☐☐ | ______ |

### Findings inattendus

Au-delà des questions initiales, avez-vous découvert quelque chose de surprenant ?

| Finding | Données source | Implication potentielle |
|---------|----------------|------------------------|
| _______ | ______________ | _______________________ |
| _______ | ______________ | _______________________ |

---

## 5. Utiliser l'IA pour vous aider

### Prompt 1 : Interpréter des résultats

```
J'ai analysé mes données et obtenu les résultats suivants :

Question business : [VOTRE QUESTION]

Résultats :
[COLLER VOS RÉSULTATS - TABLEAUX, STATISTIQUES]

Contexte : [DOMAINE, PÉRIODE, ENJEUX]

Peux-tu m'aider à :
1. Interpréter ces résultats
2. Formuler un insight clair et actionnable
3. Identifier les limites de cette analyse
4. Suggérer des analyses complémentaires
```

### Prompt 2 : Formuler un insight percutant

```
J'ai découvert que [RÉSULTAT BRUT].

Contexte : [DOMAINE, PUBLIC CIBLE]

Peux-tu m'aider à :
1. Reformuler cet insight de façon percutante
2. Proposer une façon de le quantifier
3. Suggérer une recommandation associée
4. Anticiper les questions qu'il pourrait susciter
```

### Prompt 3 : Choisir la bonne analyse

```
Je cherche à répondre à cette question business :
[VOTRE QUESTION]

Mes données disponibles :
- Variables : [LISTE DES COLONNES PERTINENTES]
- Période : [PÉRIODE]
- Volume : [NB LIGNES]

Peux-tu me recommander :
1. Le type d'analyse le plus adapté
2. Les étapes à suivre
3. Les pièges à éviter
4. Comment interpréter les résultats
```

### Prompt 4 : Valider une conclusion

```
Suite à mon analyse, je souhaite conclure que :
[VOTRE CONCLUSION]

Cette conclusion est basée sur :
[RÉSUMÉ DE L'ANALYSE]

Peux-tu :
1. Évaluer la solidité de cette conclusion
2. Identifier les hypothèses implicites
3. Suggérer des vérifications supplémentaires
4. Proposer une formulation plus prudente si nécessaire
```

---

## 6. Checklist de validation des conclusions

### Avant de valider un insight

- [ ] L'analyse répond-elle vraiment à la question posée ?
- [ ] Les données utilisées sont-elles fiables ?
- [ ] L'échantillon est-il représentatif ?
- [ ] Ai-je considéré des explications alternatives ?
- [ ] La conclusion est-elle cohérente avec le contexte métier ?

### Red flags (signaux d'alerte)

| Signal | Risque | Action |
|--------|--------|--------|
| Résultat trop beau | Erreur de calcul possible | Vérifier les formules |
| Résultat contre-intuitif | Peut être vrai ou erreur | Investiguer davantage |
| Corrélation parfaite | Probablement un artefact | Vérifier les données |
| Échantillon très petit | Pas représentatif | Nuancer la conclusion |

### Questions de validation

1. Si quelqu'un contestait cette conclusion, que répondriez-vous ?
2. Quelles données supplémentaires renforceraient cette conclusion ?
3. Dans quelles conditions cette conclusion ne serait-elle plus vraie ?

---

## 7. Checklist de validation de la phase

Avant de passer à la phase suivante, vérifiez :

### Analyses effectuées
- [ ] Chaque question business a été analysée
- [ ] Les insights sont quantifiés
- [ ] Les limites sont identifiées

### Documentation
- [ ] Template de findings complété
- [ ] Synthèse des insights disponible
- [ ] Découvertes inattendues notées

### Qualité
- [ ] Conclusions validées (checklist red flags)
- [ ] Recommandations formulées
- [ ] Prêt pour la visualisation

---

## 8. Questions de réflexion

1. **Surprise** : Quel résultat vous a le plus surpris ? Correspond-il à vos intuitions initiales ?

2. **Impact** : Quel insight aura le plus d'impact pour votre public cible ?

3. **Limites** : Quelles sont les principales limites de vos analyses ? Qu'est-ce qui vous empêche d'être plus affirmatif ?

4. **Suite** : Quelles analyses complémentaires auraient enrichi vos conclusions ?

---

## 9. Critères d'évaluation de cette phase

| Critère | Insuffisant | Satisfaisant | Excellent |
|---------|-------------|--------------|-----------|
| **Couverture** | < 3 questions traitées | Toutes questions traitées | + findings inattendus |
| **Quantification** | Insights sans chiffres | Chiffres présents | Chiffres percutants et contextualisés |
| **Rigueur** | Conclusions hâtives | Conclusions justifiées | Limites explicitement mentionnées |
| **Actionnabilité** | Insights descriptifs | Recommandations présentes | Recommandations priorisées |
| **Utilisation IA** | Non utilisée | Pour interpréter | Intégrée dans tout le processus |

---

## Prochaine étape

Vos insights sont prêts ! Passez à la **Phase 6 : Visualisation et Storytelling** pour les présenter de façon impactante.

---

*Ce guide fait partie du workflow « Projet Final ML ». Consultez le fichier README pour la vue d'ensemble.*
