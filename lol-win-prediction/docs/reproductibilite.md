# Reproduire ce projet

Document genere par `notebooks/08_export_documentation.ipynb`, a ne pas editer a la main.

Donnees fournies par Oracle's Elixir (Tim Sevenhuysen, oracleselixir.com).

## En cinq commandes

```
git clone <url-du-depot>
cd lol-win-prediction
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-lock.txt
```

Puis ouvrir les notebooks et les executer **dans l'ordre 01 a 08**, chacun avec un noyau
redemarre.

## Environnement de reference

| Element | Valeur |
|---|---|
| Python | 3.13.7 |
| Systeme | Windows 11 |
| Graine aleatoire | 42, fixee dans `src/config.py` et propagee partout |
| Versions exactes | `requirements-lock.txt` |
| Contraintes minimales | `requirements.txt` |

`requirements.txt` dit ce qui est necessaire, `requirements-lock.txt` dit ce qui a reellement
tourne. Pour rejouer les resultats a l'identique, installer le second.

## Ordre d'execution

| Notebook | Role | Produit | Duree indicative |
|---|---|---|---|
| 01_extraction.ipynb | Telecharge et charge les 3 sources | data/raw/ | 5 a 20 min selon le reseau |
| 02_eda_diagnostique.ipynb | Audit qualite sur 5 dimensions | docs/rapport_diagnostic.md, 1 figure | 2 min |
| 03_nettoyage.ipynb | Retrait des fuites, regle d'inclusion | data/interim/, docs/rapport_nettoyage.md | 3 min |
| 04_transformation.ipynb | Jointures et variables derivees | data/processed/, docs/data_dictionary.md | 2 min |
| 05_eda_analytique.ipynb | Reponses aux 5 questions business | docs/rapport_analytique.md, 5 figures | 1 min |
| 06_visualisation.ipynb | Figures de communication | docs/visualisations.md, 9 figures | 1 min |
| 07_modelisation.ipynb | Baselines, 3 modeles, verdict | models/pipeline_final.joblib, 4 figures | 10 a 15 min |
| 08_export_documentation.ipynb | Exports et documentation | data/exports/, requirements-lock.txt | 2 min |

Les notebooks 05 a 08 dependent de `data/processed/lol_at15.parquet`, produit par le 04. Les
notebooks 01 a 04 doivent donc etre executes au moins une fois avant les suivants.

## Controle d'integrite

Le dataset final doit avoir cette empreinte. Elle est calculee sur les valeurs et non sur le
fichier, car deux ecritures Parquet du meme contenu ne donnent pas des octets identiques.

```
e2e286e55ddf9cda302b2f174749c0a62d8b68d53709dafa4337698b28cc70df
```

| Propriete | Valeur attendue |
|---|---|
| Lignes | 94 840 |
| Colonnes | 49 |
| Parties | 47 420 |
| Periode | 2022-01-10 au 2026-10-07 |
| Taux de victoire | 50.00 % |

Pour la verifier :

```python
import hashlib, pandas as pd
d = pd.read_parquet("data/processed/lol_at15.parquet")
v = pd.util.hash_pandas_object(d.sort_index(axis=1), index=False)
print(hashlib.sha256(v.values.tobytes()).hexdigest())
```

Une empreinte differente signifie que les sources ou le code ont change. Oracle's Elixir est mis
a jour quotidiennement : un retelechargement posterieur ajoutera des parties recentes et
modifiera legitimement l'empreinte. Dans ce cas, comparer les dimensions plutot que le hachage.

## Ce qui n'est pas versionne

| Chemin | Raison | Comment le reconstituer |
|---|---|---|
| `data/raw/` | 750 Mo de CSV publics | `src/extraction.py`, fonction `download_oracles_elixir` |
| `data/interim/` | Intermediaire | Notebook 03 |
| `data/processed/` | Derive | Notebook 04 |
| `data/exports/` | Derive | Notebook 08 |
| `models/*.joblib` | Derive | Notebook 07 |

## Points d'attention pour qui reprend le projet

1. **Le jeu de test ne s'ouvre qu'une fois.** La saison 2026 est reservee a la section 9 du
   notebook 07. Les notebooks 05 et 06 travaillent sur 2022-2025 uniquement, et c'est
   intentionnel : choisir des hypotheses en regardant le test invaliderait la mesure finale.
2. **La politique anti-fuite est centralisee** dans `src/config.py`, liste `LEAKY_COLUMNS`. Ne
   jamais reintroduire une de ces colonnes comme feature.
3. **Les variables historiques regardent le passe seul.** Toute modification de
   `src/features.py` doit conserver le `shift(1)` ou le `cumcount`, et l'audit de fuite
   temporelle du notebook 04 doit rester au vert.
4. **Le split se fait sur la date, pas sur `year`.** L'etiquette de saison d'Oracle's Elixir
   avance sur l'annee civile pour les parties de septembre a decembre.

## Formats d'export disponibles

| Fichier | Format | Usage |
|---|---|---|
| `data/exports/lolwin_at15_20261008.parquet` | Parquet | Reference, typage preserve |
| `data/exports/lolwin_at15_20261008.csv` | CSV UTF-8 | Echange, compatibilite |
| `data/exports/lolwin_at15_20261008.xlsx` | Excel, 3 feuilles | Partage avec un public non technique |
