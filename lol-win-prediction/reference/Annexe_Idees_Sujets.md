# Annexe : Idées de Sujets de Projet

Cette annexe propose des idées de sujets organisées par domaine pour vous inspirer. Chaque suggestion inclut des sources de données et des questions business potentielles.

---

## Comment utiliser cette annexe

1. **Parcourez les domaines** qui vous intéressent
2. **Choisissez un sujet** qui vous motive
3. **Vérifiez la disponibilité** des données suggérées
4. **Adaptez les questions business** à votre contexte
5. **Identifiez la colonne cible** : sans elle, pas de modèle — donc pas de projet valide

**Conseil** : Choisissez un sujet qui vous passionne — vous passerez beaucoup de temps dessus !

---

## ⚠️ Avant de valider votre sujet

Ces suggestions sont écrites du point de vue de l'**analyse**. Votre projet doit aller plus loin : il doit aboutir à une **prédiction**. Pour chaque sujet qui vous tente, posez-vous les trois questions suivantes.

| Question | Si la réponse est non |
|---|---|
| Quelle **colonne** vais-je prédire ? | Changez de sujet ou de dataset |
| Est-ce une **classification** ou une **régression** ? | Reformulez jusqu'à pouvoir trancher |
| Cette information serait-elle **inconnue** au moment de prédire ? | Attention : vous préparez une fuite de données |

**Exemples de transformation d'un sujet d'analyse en sujet de ML :**

| Sujet d'analyse | Question prédictive | Cible | Type |
|---|---|---|---|
| Performances des joueurs de Ligue 1 | Peut-on prédire la valeur marchande d'un joueur ? | `valeur_marchande` | Régression |
| Comportement d'achat e-commerce | Peut-on prédire si un client va repasser commande ? | `réachat_90j` | Classification |
| Qualité de l'air en ville | Peut-on prédire le niveau de pollution de demain ? | `indice_qualité_air` | Régression |
| Films et box-office | Peut-on prédire si un film sera rentable ? | `est_rentable` | Classification |

**Rappel des seuils obligatoires** : ≥ 1 000 lignes, ≥ 8 colonnes exploitables dont une catégorielle, données déjà téléchargées. Pas de scraping à construire, pas de série temporelle pure, pas d'images ni de texte brut.

---

## 1. Sport

### Sujet 1.1 : Analyse des performances en Ligue 1

**Description** : Analyser les statistiques des joueurs et équipes pour identifier les facteurs de succès.

**Sources de données** :

- FBref.com (stats gratuites)
- Kaggle : "Football Data from Transfermarkt"
- API-Football (freemium)

**Questions business** :

1. Quels attributs caractérisent les meilleurs buteurs ?
2. Y a-t-il une corrélation entre possession et victoire ?
3. Comment l'avantage à domicile a-t-il évolué post-COVID ?

---

### Sujet 1.2 : Analyse des performances NBA

**Description** : Étudier les statistiques des joueurs NBA pour identifier les profils de performance.

**Sources de données** :

- Basketball-Reference.com
- Kaggle : "NBA Players Stats"
- API NBA (nba_api)

**Questions business** :

1. Quels sont les différents profils de joueurs (scoreurs, défenseurs, etc.) ?
2. Comment la performance évolue-t-elle avec l'âge ?
3. Quels indicateurs prédisent le succès d'un rookie ?

---

### Sujet 1.3 : Analyse du cyclisme professionnel

**Description** : Analyser les données de courses cyclistes (Tour de France, etc.).

**Sources de données** :

- ProCyclingStats
- Kaggle : "Tour de France"
- Strava Metro (données agrégées)

**Questions business** :

1. Quelles caractéristiques distinguent les grimpeurs des sprinteurs ?
2. Comment la nationalité influence-t-elle les performances par type d'étape ?
3. L'altitude d'entraînement impacte-t-elle les résultats ?

---

## 2. E-commerce / Retail

### Sujet 2.1 : Analyse du comportement client e-commerce

**Description** : Étudier les parcours d'achat et le comportement des clients en ligne.

**Sources de données** :

- Kaggle : "E-Commerce Data" (UK Retail)
- Kaggle : "Brazilian E-Commerce (Olist)"
- Google Merchandise Store (BigQuery public)

**Questions business** :

1. Quels sont les segments de clients (RFM) ?
2. Quels produits sont souvent achetés ensemble ?
3. Quels facteurs influencent le taux de conversion ?

---

### Sujet 2.2 : Analyse des ventes retail

**Description** : Analyser les tendances de ventes d'un retailer.

**Sources de données** :

- Kaggle : "Superstore Sales"
- Kaggle : "Walmart Sales"
- Kaggle : "Retail Sales Forecasting"

**Questions business** :

1. Quelles catégories sont les plus rentables ?
2. Y a-t-il des patterns saisonniers ?
3. Quelles régions/magasins sous-performent ?

---

### Sujet 2.3 : Analyse des avis produits

**Description** : Analyser les avis clients pour comprendre la satisfaction.

**Sources de données** :

- Kaggle : "Amazon Product Reviews"
- Kaggle : "Yelp Dataset"
- Web scraping (avec précaution)

**Questions business** :

1. Quels facteurs corrèlent avec les bonnes notes ?
2. Comment évoluent les avis dans le temps ?
3. Peut-on identifier les produits problématiques ?

---

## 3. Santé

### Sujet 3.1 : Analyse des données COVID-19

**Description** : Étudier l'évolution de la pandémie et les facteurs associés.

**Sources de données** :

- Johns Hopkins COVID-19 Data
- Our World in Data
- Santé Publique France (data.gouv.fr)

**Questions business** :

1. Quels facteurs (densité, PIB, politique) corrèlent avec le taux de mortalité ?
2. Comment les vagues se comparent-elles entre pays ?
3. Quel a été l'impact de la vaccination ?

---

### Sujet 3.2 : Analyse des données de fitness

**Description** : Analyser des données d'activité physique et de santé.

**Sources de données** :

- Kaggle : "Fitbit Fitness Tracker Data"
- Kaggle : "Apple Watch Health Data"
- MyFitnessPal exports

**Questions business** :

1. Quels patterns d'activité corrèlent avec une meilleure santé ?
2. Comment le sommeil impacte-t-il l'activité ?
3. Quels profils d'utilisateurs peut-on identifier ?

---

### Sujet 3.3 : Analyse épidémiologique

**Description** : Étudier les facteurs de risque de maladies.

**Sources de données** :

- Kaggle : "Heart Disease Dataset"
- Kaggle : "Diabetes Dataset"
- UCI ML Repository (health datasets)

**Questions business** :

1. Quels facteurs sont les plus prédictifs de la maladie ?
2. Peut-on identifier des profils à risque ?
3. Comment les facteurs interagissent-ils ?

---

## 4. Finance

### Sujet 4.1 : Analyse boursière

**Description** : Étudier l'évolution des cours et identifier des patterns.

**Sources de données** :

- Yahoo Finance (yfinance API)
- Kaggle : "S&P 500 Stock Data"
- Alpha Vantage API

**Questions business** :

1. Quels secteurs ont les meilleures performances ?
2. Y a-t-il des patterns saisonniers ?
3. Comment les actions corrèlent-elles entre elles ?

---

### Sujet 4.2 : Analyse des cryptomonnaies

**Description** : Étudier l'évolution du marché crypto.

**Sources de données** :

- CoinGecko API
- Kaggle : "Cryptocurrency Historical Prices"
- Binance API

**Questions business** :

1. Comment Bitcoin et altcoins corrèlent-ils ?
2. Quels indicateurs précèdent les hausses/baisses ?
3. Comment la volatilité a-t-elle évolué ?

---

### Sujet 4.3 : Analyse des prêts bancaires

**Description** : Étudier les facteurs de risque de défaut de paiement.

**Sources de données** :

- Kaggle : "Lending Club Loan Data"
- Kaggle : "Home Credit Default Risk"
- Kaggle : "Credit Card Fraud Detection"

**Questions business** :

1. Quels profils présentent le plus de risque ?
2. Quels facteurs prédisent le défaut ?
3. Comment optimiser la politique de crédit ?

---

## 5. Environnement

### Sujet 5.1 : Analyse de la qualité de l'air

**Description** : Étudier la pollution atmosphérique et ses facteurs.

**Sources de données** :

- OpenAQ (API mondiale)
- data.gouv.fr (France)
- Kaggle : "Air Quality Data"

**Questions business** :

1. Quelles villes sont les plus polluées ?
2. Comment la pollution évolue-t-elle dans la journée/semaine ?
3. Quel impact ont eu les confinements ?

---

### Sujet 5.2 : Analyse météorologique

**Description** : Étudier les tendances climatiques.

**Sources de données** :

- Open-Meteo API
- NOAA Climate Data
- Kaggle : "Historical Weather Data"

**Questions business** :

1. Comment les températures évoluent-elles sur 50 ans ?
2. Y a-t-il plus d'événements extrêmes ?
3. Quels patterns saisonniers observe-t-on ?

---

### Sujet 5.3 : Analyse de la consommation énergétique

**Description** : Étudier les patterns de consommation d'énergie.

**Sources de données** :

- RTE (éco2mix) - France
- Kaggle : "Household Electric Power Consumption"
- Our World in Data (Energy)

**Questions business** :

1. Quels facteurs influencent la consommation ?
2. Comment la production renouvelable évolue-t-elle ?
3. Peut-on identifier des patterns de consommation ?

---

## 6. Culture et Divertissement

### Sujet 6.1 : Analyse de films (IMDB/TMDB)

**Description** : Étudier ce qui fait le succès d'un film.

**Sources de données** :

- Kaggle : "IMDB Movies Dataset"
- TMDB API
- Kaggle : "The Movies Dataset"

**Questions business** :

1. Quels facteurs corrèlent avec le succès (box-office, notes) ?
2. Comment les genres ont-ils évolué dans le temps ?
3. Quel est l'impact du budget sur les recettes ?

---

### Sujet 6.2 : Analyse musicale (Spotify)

**Description** : Étudier les caractéristiques des chansons populaires.

**Sources de données** :

- Spotify API
- Kaggle : "Spotify Dataset"
- Kaggle : "Top Spotify Songs"

**Questions business** :

1. Quelles caractéristiques audio font un hit ?
2. Comment les préférences musicales évoluent-elles ?
3. Quels artistes dominent quelles régions ?

---

### Sujet 6.3 : Analyse des jeux vidéo

**Description** : Étudier le marché du jeu vidéo.

**Sources de données** :

- Kaggle : "Video Game Sales"
- RAWG API
- Steam API

**Questions business** :

1. Quels genres dominent quelles plateformes ?
2. Comment le marché a-t-il évolué ?
3. Quels facteurs corrèlent avec les bonnes ventes ?

---

## 7. Transport et Mobilité

### Sujet 7.1 : Analyse des vélos en libre-service

**Description** : Étudier l'utilisation des vélos partagés.

**Sources de données** :

- Vélib' Open Data (Paris)
- Kaggle : "Bike Sharing Dataset"
- data.gouv.fr (autres villes)

**Questions business** :

1. Quels patterns d'utilisation observe-t-on ?
2. Comment la météo impacte-t-elle l'usage ?
3. Quelles stations sont sous/sur-utilisées ?

---

### Sujet 7.2 : Analyse des retards de trains

**Description** : Étudier la ponctualité ferroviaire.

**Sources de données** :

- SNCF Open Data
- data.gouv.fr
- Kaggle : "Train Delay"

**Questions business** :

1. Quelles lignes sont les plus problématiques ?
2. Quels facteurs causent les retards ?
3. Comment la ponctualité évolue-t-elle ?

---

### Sujet 7.3 : Analyse du trafic urbain

**Description** : Étudier la congestion et les flux de trafic.

**Sources de données** :

- Google Maps API (Traffic)
- TomTom Traffic Index
- Kaggle : "Traffic Volume"

**Questions business** :

1. Quels sont les points noirs de circulation ?
2. Comment le télétravail a-t-il impacté le trafic ?
3. Quels patterns quotidiens/hebdomadaires observe-t-on ?

---

## 8. Éducation

### Sujet 8.1 : Analyse des résultats scolaires

**Description** : Étudier les facteurs de réussite scolaire.

**Sources de données** :

- Kaggle : "Student Performance"
- PISA (OECD)
- data.gouv.fr (résultats bac, etc.)

**Questions business** :

1. Quels facteurs corrèlent avec la réussite ?
2. Y a-t-il des disparités géographiques/sociales ?
3. Comment les résultats évoluent-ils ?

---

### Sujet 8.2 : Analyse des MOOCs

**Description** : Étudier l'engagement et la réussite dans les cours en ligne.

**Sources de données** :

- Kaggle : "MOOC Dataset"
- edX Research Data
- Kaggle : "Online Learning"

**Questions business** :

1. Quels facteurs prédisent l'achèvement d'un cours ?
2. Comment l'engagement évolue-t-il ?
3. Quels types de cours ont le plus de succès ?

---

## 9. Ressources de données générales

### Plateformes de datasets

| Plateforme | URL | Spécialité |
|------------|-----|------------|
| Kaggle | kaggle.com/datasets | Varié, compétitions |
| data.gouv.fr | data.gouv.fr | Open Data France |
| UCI ML Repository | archive.ics.uci.edu | Académique |
| Google Dataset Search | datasetsearch.research.google.com | Moteur de recherche |
| AWS Open Data | registry.opendata.aws | Big Data, cloud |
| Hugging Face | huggingface.co/datasets | NLP, ML |

### APIs gratuites utiles

| API | Usage | Limite |
|-----|-------|--------|
| OpenWeatherMap | Météo | 1000 appels/jour |
| News API | Actualités | 100 appels/jour |
| Spotify | Musique | Auth requise |
| TMDB | Films | 40 appels/10s |
| Alpha Vantage | Finance | 5 appels/min |

---

## 10. Conseils pour choisir

### Questions à vous poser

1. **Motivation** : Ce sujet me passionne-t-il vraiment ?
2. **Données** : Les données sont-elles accessibles et suffisantes ?
3. **Questions** : Puis-je formuler 3-5 questions business claires ?
4. **Faisabilité** : Le scope est-il réaliste pour le temps disponible ?
5. **Originalité** : Mon angle est-il intéressant ?

### Red flags (éviter si...)

- ❌ Données introuvables ou payantes
- ❌ Sujet trop vaste (ex: "analyser internet")
- ❌ Pas de questions business claires
- ❌ Données trop petites (< 1000 lignes)
- ❌ Données trop complexes pour votre niveau

---

*Cette annexe fait partie du workflow « Projet Final ML ». Bonne exploration !*
