# Tabular Benchmark MLOps

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI](https://github.com/valorisa/Tabular-Benchmark-MLOps/actions/workflows/ci.yml/badge.svg)](https://github.com/valorisa/Tabular-Benchmark-MLOps/actions/workflows/ci.yml)

## 🎯 Objectif du Projet

Ce dépôt est une référence pédagogique et technique pour le benchmarking de modèles sur des données tabulaires. Il compare trois approches majeures :

1.  **Scikit-Learn** (Random Forest)
2.  **XGBoost** (Gradient Boosting)
3.  **PyTorch** (Multi-Layer Perceptron)

Le projet est conçu pour être **exécutable immédiatement** (données synthétiques), **structuré comme un projet production** (MLOps), et **compatible Windows/PowerShell**.

## 🚀 Démarrage Rapide (Windows 11 / PowerShell)

### 1. Prérequis

Assurez-vous d'avoir les outils suivants installés :

-   **Python 3.11+** : [Télécharger](https://www.python.org/downloads/)
-   **Git** : [Télécharger](https://git-scm.com/download/win)
-   **Compte Weights & Biases** : [Inscription gratuite](https://wandb.ai/)

### 2. Installation

Ouvrez **PowerShell 7** et naviguez vers le projet :

```powershell
cd C:\Users\bbrod\Projets\tabular-benchmark-mlops
```

Créez un environnement virtuel et activez-le :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installez les dépendances :

```powershell
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 3. Configuration Weights & Biases

Connectez-vous à W&B :

```powershell
wandb login
```

*Pour tester sans compte, ajoutez le flag `--offline`.*

### 4. Lancement du Benchmark

#### Classification (XGBoost)

```powershell
python src/main.py --task classification --model xgboost --epochs 100
```

#### Régression (PyTorch)

```powershell
python src/main.py --task regression --model pytorch --epochs 50
```

#### Benchmark Complet

```powershell
python src/main.py --task classification --model all --epochs 100
```

## 📂 Structure du Projet

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── ci.yml
├── .venv/                    # Environnement virtuel (ignoré par git)
├── backup-*/                 # Sauvegardes pre-commit (ignoré par git)
├── configs/
│   ├── default.yaml
│   └── experiment.yaml
├── docs/
│   └── ADR.md
├── logs/                     # Logs d'exécution (ignoré par git)
├── models/                   # Modèles sauvegardés (ignoré par git)
├── scripts/
│   └── fix-ci-issues.ps1
├── src/
│   ├── __init__.py
│   ├── data.py
│   ├── evaluate.py
│   ├── main.py
│   ├── models.py
│   ├── train.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_data.py
│   └── test_train.py
├── wandb/                    # W&B runs (ignoré par git)
├── .gitignore
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
└── requirements.txt
```

## 🛠 Commandes Utiles (PowerShell)

| Action | Commande PowerShell |
| :--- | :--- |
| **Installer** | `pip install -e .` |
| **Tester** | `pytest tests/ -v` |
| **Linter** | `pre-commit run --all-files` |
| **Entraîner** | `python src/main.py --task classification --model all` |
| **Nettoyer** | `Remove-Item -Recurse -Force __pycache__, .venv` |

## 📊 Métriques Suivi

-   **Classification** : Accuracy, F1-Score, Loss
-   **Régression** : RMSE, R², Loss
-   **Système** : Temps d'entraînement (via W&B)


## 🚀 Guide Complet des Commandes (PowerShell)

### 📦 Installation et Configuration

```powershell
# Naviguer vers le projet
cd C:\Users\bbrod\Projets\tabular-benchmark-mlops

# Créer et activer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Mettre à jour pip et installer les dépendances
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# Installer les outils de développement (optionnel)
pip install -e .[dev]

# Configurer pre-commit (pour les commits locaux)
pre-commit install
```

### 🧪 Lancement du Benchmark

```powershell
# Benchmark complet - Classification (100 epochs)
python src/main.py --task classification --model all --epochs 100 --offline

# Benchmark complet - Régression (50 epochs)
python src/main.py --task regression --model all --epochs 50 --offline

# Modèle individuel - Scikit-Learn
python src/main.py --task classification --model sklearn --epochs 100 --offline

# Modèle individuel - XGBoost (meilleur performeur)
python src/main.py --task classification --model xgboost --epochs 100 --offline

# Modèle individuel - PyTorch MLP
python src/main.py --task classification --model pytorch --epochs 100 --offline

# Avec configuration personnalisée
python src/main.py --task classification --model all --config configs/experiment.yaml --offline

# En mode online (sync vers W&B cloud)
python src/main.py --task classification --model all --epochs 100
```

### ✅ Tests et Validation

```powershell
# Lancer tous les tests unitaires
pytest tests/ -v

# Lancer les tests avec couverture de code (optionnel)
pytest tests/ -v --cov=src --cov-report=html

# Vérifier le linting (pre-commit hooks)
pre-commit run --all-files

# Vérifier uniquement avec flake8
flake8 src/ tests/ --max-line-length=88 --ignore=E501,E402,E203,W503

# Vérifier le formatage Black
black src/ tests/ --check

# Vérifier l'ordre des imports isort
isort src/ tests/ --check-only
```

### 📊 Weights & Biases (W&B)

```powershell
# Se connecter à W&B (première fois uniquement)
wandb login

# Vérifier le statut de connexion
wandb online

# Travailler en offline (par défaut)
python src/main.py --task classification --model all --epochs 100 --offline

# Travailler en online (sync vers le cloud)
wandb online
python src/main.py --task classification --model all --epochs 100

# Sync les runs offline vers le cloud
wandb sync wandb/offline-run-*

# Sync un run spécifique
wandb sync wandb/offline-run-20260401_185248-m5qu6w33

# Voir tous les runs offline
Get-ChildItem wandb\offline-run-* | Select-Object Name

# Ouvrir le dashboard W&B dans le navigateur
Start-Process "https://wandb.ai/bbrodeau/tabular-benchmark-mlops"
```

### 🔧 Git et GitHub

```powershell
# Vérifier l'état du repository
git status

# Voir les changements
git diff

# Ajouter tous les fichiers modifiés
git add .

# Ajouter un fichier spécifique
git add src/models.py

# Commiter avec un message
git commit -m "fix: description du changement"

# Commiter en sautant l'étape d'add (fichiers déjà tracked)
git commit -am "feat: nouvelle fonctionnalité"

# Pousser vers GitHub
git push origin main

# Tirer les changements depuis GitHub
git pull origin main

# Créer une nouvelle branche
git checkout -b feature/nouvelle-fonctionnalite

# Changer de branche
git checkout main

# Voir l'historique des commits
git log --oneline -10

# Annuler les changements non commités
git checkout -- .
```

### 🧹 Nettoyage et Maintenance

```powershell
# Supprimer les fichiers __pycache__
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force

# Supprimer l'environnement virtuel
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# Supprimer les logs d'exécution
Remove-Item -Recurse -Force logs\* -ErrorAction SilentlyContinue

# Supprimer les modèles sauvegardés
Remove-Item -Recurse -Force models\* -ErrorAction SilentlyContinue

# Supprimer les builds
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# Nettoyer les runs W&B offline (après sync)
Remove-Item -Recurse -Force wandb\offline-run-* -ErrorAction SilentlyContinue

# Script de nettoyage complet
Remove-Item -Recurse -Force __pycache__, .venv, logs, models, build, dist -ErrorAction SilentlyContinue
```

### 📈 Commandes Rapides (Récapitulatif)

| Action | Commande |
| :--- | :--- |
| **Activer venv** | `.\.venv\Scripts\Activate.ps1` |
| **Benchmark classification** | `python src/main.py --task classification --model all --epochs 100 --offline` |
| **Benchmark régression** | `python src/main.py --task regression --model all --epochs 50 --offline` |
| **Tests unitaires** | `pytest tests/ -v` |
| **Linting** | `pre-commit run --all-files` |
| **W&B login** | `wandb login` |
| **W&B sync** | `wandb sync wandb/offline-run-*` |
| **Git push** | `git push origin main` |
| **Nettoyage** | `Remove-Item -Recurse -Force __pycache__, .venv` |

---


1.  Forker le projet
2.  Créer une branche (`git checkout -b feature/nom`)
3.  Committer (`git commit -m 'Add feature'`)
4.  Pusher (`git push origin feature/nom`)
5.  Ouvrir une Pull Request

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les détails.

## 📄 Licence

Distribué sous la licence MIT. Voir [LICENSE](LICENSE).


## 📚 Qu'est-ce que le MLOps ?

### Définition

**MLOps** (Machine Learning Operations) désigne l'ensemble des pratiques et outils qui visent à **automatiser et industrialiser** le cycle de vie des projets de Machine Learning, du développement au déploiement et à la surveillance.

C'est l'équivalent du **DevOps** appliqué au Machine Learning.

---

### 🎯 Pourquoi le MLOps ?

| Problème Sans MLOps | Solution Avec MLOps |
| :--- | :--- |
| ❌ Modèles développés localement, impossibles à reproduire | ✅ Environnements reproductibles et versionnés |
| ❌ Tests manuels et erreurs humaines | ✅ Tests automatisés et CI/CD |
| ❌ Pas de suivi des expériences | ✅ Tracking centralisé (W&B, MLflow) |
| ❌ Déploiements longs et risqués | ✅ Déploiements automatisés et rollback facile |
| ❌ Pas de surveillance en production | ✅ Monitoring des performances et alertes |

---

### 🔄 Cycle de Vie MLOps

```text
┌─────────────────────────────────────────────────────────────┐
│  CYCLE DE VIE MLOPS                                         │
├─────────────────────────────────────────────────────────────┤
│  1. 📊 COLLECTE DE DONNÉES                                  │
│  2. 🧪 DÉVELOPPEMENT DE MODÈLES                             │
│  3. ✅ VALIDATION ET TESTS                                  │
│  4. 🚀 DÉPLOIEMENT                                          │
│  5. 📈 SURVEILLANCE                                         │
│  6. 🔄 ITÉRATION                                            │
└─────────────────────────────────────────────────────────────┘
```

---

### 🛠 Composants Clés du MLOps

| Composant | Outil(s) | Rôle |
| :--- | :--- | :--- |
| **Gestion de Code** | Git, GitHub | Versionning du code source |
| **CI/CD** | GitHub Actions | Tests et déploiements automatisés |
| **Tracking d'Expériences** | W&B, MLflow | Suivi des runs et métriques |
| **Gestion de Données** | DVC, Pandas | Versionning des datasets |
| **Packaging** | pip, Docker | Reproductibilité des environnements |
| **Testing** | pytest | Validation automatique du code |
| **Code Quality** | Black, isort, flake8 | Standards de code cohérents |
| **Monitoring** | W&B, Prometheus | Surveillance des modèles en prod |

---

### 📋 Tâches Typiques en MLOps

Le MLOps implique des tâches telles que :

-   ✅ **Suivi des tests et des résultats** pour identifier les meilleurs modèles
-   ✅ **Versionning du code** et des données pour la reproductibilité
-   ✅ **Automatisation des pipelines** d'entraînement et d'évaluation
-   ✅ **Validation de la qualité** des données et des modèles
-   ✅ **Déploiement continu** des nouveaux modèles
-   ✅ **Surveillance des performances** en production
-   ✅ **Gestion des dépendances** et des environnements
-   ✅ **Documentation** des décisions et des expériences

---

### 🎓 Comment Ce Projet Démontre le MLOps ?

| Pratique MLOps | Implémentation dans Ce Projet |
| :--- | :--- |
| **CI/CD** | GitHub Actions avec pre-commit + pytest |
| **Tracking** | Weights & Biases pour les métriques |
| **Testing** | Tests unitaires avec pytest |
| **Code Quality** | Black, isort, flake8 via pre-commit |
| **Packaging** | `pip install -e .` avec pyproject.toml |
| **Configuration** | Fichiers YAML dans `configs/` |
| **Documentation** | README, CONTRIBUTING, TROUBLESHOOTING |
| **Reproductibilité** | Seeds fixes, environnements virtuels |

---

### 🚀 Avantages du MLOps

| Pour Qui ? | Bénéfices |
| :--- | :--- |
| **Data Scientists** | Plus de temps sur les modèles, moins sur le déploiement |
| **Ingénieurs ML** | Déploiements fiables et reproductibles |
| **Entreprises** | Réduction des risques, time-to-market accéléré |
| **Équipes** | Collaboration facilitée, knowledge sharing |

---
## 🙏 Remerciements

-   **Scikit-Learn** : Datasets synthétiques
-   **Weights & Biases** : Tracking d'expériences
-   **PyTorch & XGBoost** : Moteurs d'entraînement

---
*Projet conçu par valorisa pour démonstration MLOps pédagogique.*
