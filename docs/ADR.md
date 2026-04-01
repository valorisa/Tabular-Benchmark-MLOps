# Architecture Decision Record : Benchmark Tabulaire

## Contexte
Comparer des modèles de ML sur données tabulaires dans un cadre pédagogique.

## Décision
Architecture modulaire avec :
-   Données synthétiques (exécution immédiate)
-   CLI unique pour orchestrer les runs
-   W&B pour le tracking
-   PyTorch, XGBoost, Sklearn comme backends

## Conséquences
-   (+) Exécution immédiate sans download
-   (+) Comparaison équitable des modèles
-   (-) Données non représentatives de cas réels complexes
