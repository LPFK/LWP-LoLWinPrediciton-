# Changelog

Journal des versions du projet. Genere par `notebooks/08_export_documentation.ipynb`.

## v1.0 - 2026-09-08

Premiere version complete, phases 0 a 8.

### Donnees
- Chargement des 3 sources : Oracle's Elixir 2022-2026, Riot Data Dragon, referentiel des ligues
- Regle d'inclusion fondee sur la completude mesuree du snapshot a 15 minutes, jamais sur un nom
  de ligue : 92 616 lignes equipe retenues
- 5 colonnes de fuite rattrapees par un controle de correlation, dont `damagetotowers` a 0,760
- `firsttower` ecartee contre le cadrage initial, apres mesure

### Variables
- 23 variables retenues pour le modele, dont 11 construites
- 5 variables historiques en fenetre expansive sur le passe seul, verifiees par un audit
- Exclusion des categorielles qui ne survivent pas a la frontiere 2025/2026

### Analyse
- 5 questions business traitees sur le seul jeu d'entrainement
- Resultat principal : le premier dragon vaut environ 1 030 or a avantage economique egal, le
  premier sang et le premier heraut ne valent rien de plus que l'or qu'ils rapportent
- 15 figures produites, dont un tableau de bord

### Modelisation
- 3 baselines calculees avant tout modele, la plus forte a 73,87 % d'accuracy
- 3 familles comparees par `GridSearchCV` avec `TimeSeriesSplit`
- Regression logistique retenue : 75,87 % d'accuracy et 0,8438 d'AUC sur 2026
- Pipeline complete exportee, preprocessing inclus

### Documentation
- Dictionnaire de donnees enrichi : unites, valeurs possibles, transformations, limitations
- Exports en 3 formats, `requirements-lock.txt`, guide de reproductibilite
- Audit des dependances : contrainte `numpy` corrigee, `seaborn` retire car jamais importe
