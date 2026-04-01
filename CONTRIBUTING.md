# Contributing to tabular-benchmark-mlops

Merci de l'intérêt porté à ce projet !

## Code of Conduct

Soyez respectueux et constructifs.

## Comment contribuer

1.  **Issues** : Vérifiez les issues existantes.
2.  **Branches** : eature/nom-fonctionnalité depuis main.
3.  **Commits** : Messages clairs (Conventional Commits).
4.  **Tests** : pytest doit passer.
5.  **Linting** : pre-commit avant push.

## Setup de développement

`powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
pre-commit install
`

## Pull Requests

Les PR doivent :
-   Passer la CI
-   Inclure des tests si nouvelle fonctionnalité
-   Mettre à jour le README si besoin
