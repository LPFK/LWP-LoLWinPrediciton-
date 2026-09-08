# Phase 7 : Modélisation Machine Learning

**Objectif** : Passer de l'analyse descriptive (« ce que disent les données ») à la prédiction (« ce que le modèle peut anticiper »), en construisant un modèle honnêtement évalué.

> **Ressource centrale de cette phase** : le notebook [`Ressource_Workflow_ML_Complet.ipynb`](Ressource_Workflow_ML_Complet.ipynb).
> Il contient le squelette de code complet (split → `ColumnTransformer` → `Pipeline` → `GridSearchCV` → évaluation → sauvegarde). **Vous n'avez pas à réinventer ce code** : vous l'adaptez à votre dataset. Trois zones seulement sont à modifier, elles sont marquées `# <-- A ADAPTER`.

---

## Pourquoi cette étape est cruciale

Les phases 0 à 6 ont produit un dataset propre, enrichi et compris. C'est exactement ce dont un modèle a besoin — et c'est pour ça que la modélisation arrive maintenant et pas avant.

Cette phase est aussi celle où l'on peut se mentir le plus facilement. Un score de 99 % obtenu avec une fuite de données ne vaut rien. **Ce qui est évalué ici, ce n'est pas la performance de votre modèle, c'est la rigueur de votre démarche.** Un modèle honnête à 0.72 vaut mieux qu'un modèle truqué à 0.99.

---

## 1. Formuler le problème de ML

Avant toute ligne de code, répondez à ces questions. Elles déterminent tout le reste.

### Template de cadrage ML

```
Question prédictive : _________________________________
(Ex : « Peut-on prédire si un client va résilier son abonnement ? »)

Colonne cible (y) : _________________________________

Type de problème :  ☐ Classification binaire
                    ☐ Classification multi-classes
                    ☐ Régression

Features (X) : _________________________________
(Quelles colonnes servent à prédire ? Lesquelles doivent être EXCLUES ?)

Métrique principale : _________________________________
(Celle qui décidera du "meilleur" modèle)

Pourquoi cette métrique : _________________________________

Baseline à battre : _________________________________
(Le score du modèle bête — voir section 3)
```

### Choisir sa métrique

La métrique dépend du **problème**, jamais du modèle. Tous les modèles candidats sont comparés avec la même.

| Situation | Métrique | Pourquoi |
|---|---|---|
| Classification, classes équilibrées | `accuracy` | Simple et lisible |
| Classification, classes déséquilibrées | `f1`, `roc_auc` | L'accuracy est trompeuse si 95 % des lignes sont d'une classe |
| Classification, les faux négatifs coûtent cher | `recall` | Mieux vaut une fausse alerte qu'un cas manqué (fraude, maladie) |
| Classification, les fausses alertes coûtent cher | `precision` | Ne déranger que quand on est sûr |
| Régression | `neg_mean_absolute_error` | Erreur moyenne, dans l'unité de la cible : interprétable |
| Régression, les grosses erreurs sont graves | `neg_root_mean_squared_error` | Pénalise davantage les gros écarts |

> ⚠️ **Le piège n° 1 du projet** : choisir `accuracy` sur un dataset déséquilibré. Regardez `y.value_counts()` **avant** de choisir.

---

## 2. Le piège absolu : la fuite de données (data leakage)

Une fuite, c'est quand le modèle a accès, à l'entraînement, à une information qu'il n'aurait pas au moment de prédire pour de vrai. Le score explose, et le modèle est inutilisable.

### Les trois fuites classiques dans un projet étudiant

| Fuite | Exemple | Comment l'éviter |
|---|---|---|
| **Une feature qui contient la réponse** | Prédire `a_resilié` en gardant la colonne `date_de_résiliation` | Se demander pour CHAQUE colonne : « cette info existe-t-elle vraiment *avant* l'événement à prédire ? » |
| **Preprocessing avant le split** | Faire un `StandardScaler().fit()` sur tout le dataset, puis découper | Découper **d'abord**, puis mettre le preprocessing dans une `Pipeline` |
| **Regarder le test pour décider** | Tester plusieurs modèles sur le test et garder le meilleur | Le test s'ouvre **une seule fois**, à la toute fin |

### Checklist anti-fuite

- [ ] J'ai passé en revue **chaque colonne** de `X` et vérifié qu'elle serait disponible au moment de la prédiction réelle
- [ ] J'ai supprimé les identifiants (`id`, `nom`, `numéro de dossier`) : ils ne portent aucune information généralisable
- [ ] Le `train_test_split` est fait **avant** tout imputer / scaler / encoder
- [ ] Tout mon preprocessing est **dans** la `Pipeline`, pas exécuté à la main sur le DataFrame complet
- [ ] Je n'ai touché au jeu de test qu'une seule fois

---

## 3. Toujours commencer par une baseline

Un score ne veut rien dire tout seul. Il faut savoir ce que fait un modèle **stupide** sur vos données, sinon vous ne saurez pas si votre RandomForest est bon ou juste chanceux.

```python
from sklearn.dummy import DummyClassifier   # ou DummyRegressor

baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)
print("Baseline :", baseline.score(X_val, y_val))
```

- **Classification** : `strategy="most_frequent"` prédit toujours la classe majoritaire.
- **Régression** : `DummyRegressor(strategy="mean")` prédit toujours la moyenne.

> Si votre modèle ne bat pas nettement la baseline, le problème n'est pas le choix du modèle : c'est que vos features ne portent pas l'information. Retournez à la Phase 4.

**À noter dans votre rapport** : `Baseline = _______ | Modèle final = _______ | Gain = _______`

---

## 4. Construire, entraîner, comparer

Suivez le notebook `Ressource_Workflow_ML_Complet.ipynb`, étapes 3 à 7. La démarche attendue :

### Checklist de modélisation

- [ ] **Split** train / validation / test réalisé en premier (`stratify=y` en classification)
- [ ] **Preprocessing** dans un `ColumnTransformer` : numérique (imputer + scaler) et catégoriel (imputer + `OneHotEncoder(handle_unknown="ignore")`)
- [ ] **Pipeline** assemblant preprocessing + modèle en un seul objet
- [ ] **Baseline** calculée et notée
- [ ] **Au moins 3 modèles** comparés via une `param_grid` en liste de dictionnaires
- [ ] **`GridSearchCV`** avec `cv=5` et le `scoring` choisi en section 1
- [ ] **Tableau de comparaison** des scénarios exporté (`cv_results_`) — c'est lui qui *justifie* votre choix

### Quels modèles proposer selon le problème

| Problème | Trois candidats raisonnables |
|---|---|
| Classification | `LogisticRegression(max_iter=1000)`, `RandomForestClassifier()`, `SVC()` ou `DecisionTreeClassifier()` |
| Régression | `LinearRegression()` ou `Ridge()`, `RandomForestRegressor()`, `DecisionTreeRegressor()` |

Incluez **toujours un modèle simple** (régression linéaire ou logistique) dans la comparaison. S'il fait aussi bien qu'un RandomForest, c'est lui qu'il faut garder — et c'est un excellent résultat à commenter.

---

## 5. Évaluer honnêtement

L'ordre n'est pas négociable (notebook, étape 8) :

| Étape | Sur quoi | Combien de fois | Peut encore changer le modèle ? |
|---|---|---|---|
| Confirmer le choix | validation | autant qu'on veut | oui |
| Diagnostiquer le surapprentissage | train vs validation croisée | autant qu'on veut | oui |
| **Verdict final** | **test** | **une seule fois** | **non** |

### Diagnostiquer le surapprentissage

Comparez le score sur le train (déjà vu) et sur la validation (jamais vu), puis **traduisez l'écart en nombre de lignes** :

```
écart × nombre de lignes de validation = nombre de lignes concernées
```

Sur 100 lignes de validation, un écart de 0.02 = **2 lignes**. Ce n'est pas du surapprentissage, c'est du hasard de découpage. Ne surinterprétez pas.

### Métriques à reporter obligatoirement

**Classification** :
- [ ] `classification_report` (precision / recall / f1 par classe)
- [ ] `confusion_matrix` — et son interprétation en une phrase : *où* le modèle se trompe-t-il ?
- [ ] Courbe ROC / AUC si binaire

**Régression** :
- [ ] MAE et RMSE, **exprimées dans l'unité de la cible** (« on se trompe en moyenne de 18 500 € »)
- [ ] R²
- [ ] Graphique des résidus (prédictions vs valeurs réelles)

---

## 6. Interpréter le modèle

Un modèle qu'on ne sait pas expliquer n'est pas défendable en soutenance. **Reliez ce que le modèle a appris à ce que votre EDA (Phase 5) avait montré.**

```python
# Modèles à base d'arbres
importances = pd.Series(
    modele_final.named_steps["modele"].feature_importances_,
    index=modele_final.named_steps["preprocessing"].get_feature_names_out()
).sort_values(ascending=False)
print(importances.head(10))

# Modèles linéaires : .coef_ au lieu de .feature_importances_
```

### Questions à traiter dans votre rapport

1. Quelles sont les **5 features les plus importantes** ?
2. Ces features **correspondent-elles** aux corrélations vues en Phase 5 ? Si non, pourquoi ?
3. Y a-t-il une feature importante qui vous **surprend** ? Est-ce un vrai signal, ou une fuite que vous auriez ratée ?
4. Quelles sont les **limites** du modèle : sur quels cas se trompe-t-il, et pour qui est-ce grave ?
5. Le modèle présente-t-il un **risque de biais** (Bloc 7) selon un attribut sensible ?

---

## 7. Livrer le modèle

- [ ] Pipeline complète sauvegardée avec `joblib.dump(modele_final, "modele_final.joblib")`
- [ ] Une cellule de démonstration : prédiction sur 2-3 lignes de nouvelles données **brutes**
- [ ] Le `random_state` est fixé partout : le notebook redonne les mêmes résultats à chaque exécution

> Sauvegardez toujours la **pipeline entière**, jamais le modèle seul : sinon le preprocessing doit être rejoué à la main, et la moindre différence fausse les résultats en silence.

---

## 8. Utiliser l'IA pour vous aider

### Prompt 1 : Cadrer le problème de ML

```
Voici les colonnes de mon dataset nettoyé, avec leur type et un exemple de valeur :
[COLLER LE RÉSULTAT DE df.info() ET df.head()]

Je veux prédire : [VOTRE CIBLE]

Peux-tu m'aider à :
1. Confirmer s'il s'agit d'une classification ou d'une régression
2. Identifier les colonnes qui provoqueraient une FUITE DE DONNÉES et qu'il faut exclure
3. Recommander la métrique d'évaluation la plus adaptée, en justifiant
```

### Prompt 2 : Traquer la fuite de données

```
Je veux prédire [CIBLE] à partir de ces colonnes :
[LISTE DES COLONNES AVEC UNE DESCRIPTION D'UNE LIGNE CHACUNE]

Le contexte métier est : [CONTEXTE]

Pour chaque colonne, cette information serait-elle réellement disponible AU MOMENT
où l'on doit faire la prédiction ? Signale-moi toute colonne suspecte de fuite.
```

### Prompt 3 : Interpréter les résultats

```
Voici les résultats de mon GridSearchCV :
[COLLER LE TABLEAU cv_results_]

Score train : [X] | Score validation : [Y] | Score test : [Z]
Baseline : [B]
Taille du jeu de validation : [N] lignes

Peux-tu m'aider à interpréter : le modèle sur-apprend-il ? L'écart est-il significatif
ou dans le bruit ? Le gain sur la baseline est-il convaincant ?
```

### Prompt 4 : Préparer la défense du modèle

```
Mon modèle final est [MODÈLE] avec les hyperparamètres [PARAMS].
Il obtient [SCORE] sur le test, contre [BASELINE] pour la baseline.
Les features les plus importantes sont : [TOP 5].

Quelles questions critiques un évaluateur pourrait-il me poser ?
Quels sont les points faibles de ma démarche ?
```

---

## 9. Questions de réflexion

1. **Le gain est-il réel ?** De combien votre modèle bat-il la baseline ? Ce gain justifie-t-il sa complexité ?
2. **Simplicité** : le modèle simple faisait-il presque aussi bien ? Qu'auriez-vous perdu à le garder ?
3. **Confiance** : accepteriez-vous que ce modèle décide à votre place dans la vraie vie ? Pourquoi ?
4. **Fuite** : rétrospectivement, quelle colonne aurait pu vous faire tomber dans le piège ?
5. **Données vs modèle** : pour améliorer les performances, valait-il mieux changer de modèle ou collecter d'autres données ?

---

## 10. Critères d'évaluation de cette phase

| Critère | Insuffisant | Satisfaisant | Excellent |
|---------|-------------|--------------|-----------|
| **Cadrage du problème** | Type de problème ou cible flous | Problème et cible clairs | + métrique justifiée par le métier |
| **Baseline** | Absente | Calculée | Calculée et comparée explicitement au modèle final |
| **Rigueur méthodologique** | Fuite de données présente | Pipeline + split corrects | + test ouvert une seule fois, `random_state` fixé partout |
| **Comparaison de modèles** | 1 seul modèle | 2-3 modèles comparés | 3+ modèles via GridSearchCV, tableau de résultats à l'appui |
| **Évaluation** | Un seul chiffre d'accuracy | Métriques adaptées reportées | + diagnostic de surapprentissage argumenté |
| **Interprétation** | Absente | Features importantes listées | + reliées à l'EDA, limites et biais discutés |

---

## Prochaine étape

Votre modèle est entraîné, évalué et interprété. Passez à la **Phase 8 : Chargement et Documentation** pour exporter le dataset final, le modèle et documenter votre travail.

---

*Ce guide fait partie du workflow « Projet Final ML ». Consultez le fichier README pour la vue d'ensemble.*
