# 🔧 Troubleshooting Guide

Ce document recense tous les problèmes rencontrés à ce jour (april 02) lors du développement de ce projet et leurs solutions.

---

## 📋 Table des Matières

1. [isort échoue en CI mais passe en local](#1-isort-échoue-en-ci-mais-passe-en-local)
2. [trailing-whitespace modifie les fichiers](#2-trailing-whitespace-modifie-les-fichiers)
3. [imports src/train.py mal formatés](#3-imports-srctrainpy-mal-formatés)
4. [CRLF vs LF (line endings)](#4-crlf-vs-lf-line-endings)
5. [PowerShell affiche `>` rouge et bloque](#5-powershell-affiche--rouge-et-bloque)
6. [Warning Node.js 20 déprécié](#6-warning-nodejs-20-déprécié)

---

## 1. isort échoue en CI mais passe en local

### 🔍 Symptôme

```bash
isort (python)...........................................................Failed
- hook id: isort
- files were modified by this hook
Fixing /home/runner/work/Tabular-Benchmark-MLOps/Tabular-Benchmark-MLOps/src/train.py
Error: Process completed with exit code 1.
```

### ❓ Cause Racine

| Environnement | Configuration isort | Résultat |
| :--- | :--- | :--- |
| **Local** | Lit `pyproject.toml` → `profile = "black"` | ✅ Passed |
| **CI GitHub** | Ignore `pyproject.toml` → utilise config par défaut | ❌ Failed |

**Le problème :** `.pre-commit-config.yaml` ne spécifiait PAS `--profile black` pour isort.

### ✅ Solution

**Fichier à modifier :** `.pre-commit-config.yaml`

```yaml
# AVANT ❌
- repo: https://github.com/pycqa/isort
  rev: 5.12.0
  hooks:
    - id: isort
      name: isort (python)

# APRÈS ✅
- repo: https://github.com/pycqa/isort
  rev: 5.12.0
  hooks:
    - id: isort
      name: isort (python)
      args: ["--profile", "black"]  # ← ⭐ AJOUTER CETTE LIGNE
```

### 🧪 Vérification

```powershell
# Local
pre-commit run --all-files
# isort (python)...........................................................✅ Passed

# CI GitHub
# isort (python)...........................................................✅ Passed
```

---

## 2. trailing-whitespace modifie les fichiers

### 🔍 Symptôme

```bash
trim trailing whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook
Fixing .pre-commit-config.yaml
```

### ❓ Cause Racine

Après avoir édité `.pre-commit-config.yaml`, des **espaces en fin de ligne** ont été introduits :

```yaml
      args: ["--profile", "black"]␣␣␣␣␣␣␣␣  ← Espaces invisibles après
```

Le hook `trailing-whitespace` détecte ces espaces et **modifie le fichier**, ce qui fait échouer pre-commit.

### ✅ Solution

**Option A : Laisser pre-commit corriger automatiquement**

```powershell
# Exécuter pre-commit (va corriger automatiquement)
pre-commit run --all-files

# Exécuter une 2ème fois (tout devrait passer)
pre-commit run --all-files

# Commiter les changements
git add .
git commit -m "fix: apply pre-commit auto-fixes"
git push origin main
```

**Option B : Correction manuelle dans Notepad++**

```text
Menu → Édition → Traitement des espacements → Supprimer les espaces en fin de ligne
# OU raccourci : Ctrl+Alt+Maj+S (selon version)
```

### 🧪 Vérification

```powershell
pre-commit run --all-files
# trim trailing whitespace.................................................✅ Passed
```

---

## 3. imports src/train.py mal formatés

### 🔍 Symptôme

```bash
isort (python)...........................................................Failed
- hook id: isort
- files were modified by this hook
Fixing C:\Users\bbrod\Projets\tabular-benchmark-mlops\src\train.py
```

### ❓ Cause Racine

**Structure des imports AVANT :**

```python
"""Training pipeline with W&B logging."""
import wandb
from src.evaluate import evaluate_model  # ← Pas de ligne vide !
from src.models import ModelWrapper
from src.utils import get_logger
```

**isort attend (PEP 8 + Black) :**

```text
Groupe 1 : Standard Library
     ↓ (1 ligne vide)
Groupe 2 : Third-Party (wandb, torch, numpy...)
     ↓ (1 ligne vide) ← ⭐ MANQUANTE !
Groupe 3 : Local Application (from src.*)
```

### ✅ Solution

**isort avec `--profile black` ajoute automatiquement la ligne vide :**

```python
"""Training pipeline with W&B logging."""

import wandb
                           # ← ⭐ LIGNE VIDE AJOUTÉE
from src.evaluate import evaluate_model
from src.models import ModelWrapper
from src.utils import get_logger
```

### 🧪 Vérification

```powershell
# Vérifier que isort ne modifie plus le fichier
isort src/train.py --check-only --profile black
# SUCCESS: src/train.py Everything looks good!

# Ou via pre-commit
pre-commit run --all-files
# isort (python)...........................................................✅ Passed
```

---

## 4. CRLF vs LF (line endings)

### 🔍 Symptôme

```bash
trim trailing whitespace.................................................Failed
- hook id: trailing-whitespace
- files were modified by this hook
Fixing .pre-commit-config.yaml
```

**Dans Notepad++ :** L'indicateur en bas à droite montrait `CRLF` au lieu de `LF`.

### ❓ Cause Racine

| Système | Line Ending | Problème |
| :--- | :--- | :--- |
| **Windows** | `CRLF` (Carriage Return + Line Feed) | ❌ Détecté comme whitespace par pre-commit |
| **Linux/CI** | `LF` (Line Feed seul) | ✅ Standard attendu |

Le hook `trailing-whitespace` interprète le `CR` (Carriage Return) comme un **espace blanc en fin de ligne**.

### ✅ Solution

**Dans Notepad++ :**

```text
Menu → Édition → EOL Conversion → Unix (LF)
# OU
Clic-droit sur l'indicateur "CRLF" en bas à droite → Unix (LF)
```

**Puis enregistrer :** `Ctrl+S`

### 🧪 Vérification

```powershell
# Vérifier dans Notepad++ : doit afficher "Unix (LF)" en bas à droite

# Vérifier via pre-commit
pre-commit run --all-files
# trim trailing whitespace.................................................✅ Passed
```

---

## 5. PowerShell affiche `>` rouge et bloque

### 🔍 Symptôme

```powershell
(.venv) PS C:\...\tabular-benchmark-mlops> # Commande
>> ligne suivante
>> autre ligne
>  # ← Chevron rouge, PowerShell attend la suite
```

### ❓ Cause Racine

**Mauvaise utilisation des délimiteurs de chaîne multi-lignes :**

```powershell
# ❌ INCORRECT - PowerShell attend indéfiniment
$script = '@'      # ← Mauvais : quote + arobase + quote
ligne 1
ligne 2
'@
```

**Règles pour `@' ... '@` :**

| Élément | Correct ✅ | Incorrect ❌ |
| :--- | :--- | :--- |
| **Ouverture** | `@'` (seul sur ligne) | `'@'` (avec quote autour) |
| **Fermeture** | `'@` (seul sur ligne) | `'@'` (avec quote autour) |
| **Espaces avant** | Aucun | `  '@` |
| **Après fermeture** | Rien | `'@ quelque_chose` |

### ✅ Solution

```powershell
# ✅ CORRECT - Délimiteurs SEULS sur leur ligne
$script = @'
ligne 1
ligne 2
'@
```

**Sortie d'urgence :** Appuyer sur `Ctrl+C` jusqu'au retour de `PS >` normal.

### 🅿️ Analogie : Le "Frein de Parking" PowerShell

| Métaphore | Voiture 🚗 | PowerShell 💻 |
| :--- | :--- | :--- |
| **Frein de parking** | Empêche la voiture de rouler | `@'` non fermé empêche l'exécution |
| **Témoin d'alerte** | Voyant rouge au tableau de bord | Chevron `>` rouge dans le terminal |
| **Débloquer** | Relâcher le frein | Fermer avec `'@` seul sur ligne |
| **Démarrer** | Tourner la clé | Appuyer sur Entrée après fermeture |

**Leçon :** Cette "erreur" est une **protection** contre l'exécution accidentelle de scripts incomplets ou dangereux ! 🛡️

### 🧪 Vérification

```powershell
# Après correction, PowerShell doit afficher :
PS C:\Users\bbrod\Projets\tabular-benchmark-mlops>  # ← Normal, pas de >>

# Et la commande doit s'exécuter sans blocage
```

---

## 6. Warning Node.js 20 déprécié

### 🔍 Symptôme

```bash
Warning: Node.js 20 actions are deprecated. The following actions are running on Node.js 20
and may not work as expected: actions/checkout@v3, actions/setup-python@v3.
Actions will be forced to run with Node.js 24 by default starting June 2nd, 2026.
```

### ❓ Cause Racine

| Action | Version | Runtime Node.js | Statut |
| :--- | :--- | :--- | :--- |
| **actions/checkout** | v3 | Node.js 20 | ⚠️ Déprécié |
| **actions/setup-python** | v3 | Node.js 20 | ⚠️ Déprécié |

**Échéances GitHub :**
- 📅 **2 juin 2026** : Node.js 24 devient le défaut
- 📅 **16 septembre 2026** : Node.js 20 retiré des runners

### ✅ Solution

**Fichier à modifier :** `.github/workflows/ci.yml`

```yaml
# AVANT ❌
steps:
  - uses: actions/checkout@v3
  - name: Set up Python ${{ matrix.python-version }}
    uses: actions/setup-python@v3

# APRÈS ✅
steps:
  - uses: actions/checkout@v4      # ← Node.js 24 compatible
  - name: Set up Python ${{ matrix.python-version }}
    uses: actions/setup-python@v5  # ← Node.js 24 compatible
```

### 🧪 Vérification

```powershell
# Vérifier le fichier local
Get-Content ".github/workflows/ci.yml" | Select-String "actions/"
# DOIT AFFICHER :
# - uses: actions/checkout@v4
# - uses: actions/setup-python@v5

# Vérifier la CI GitHub
# ✅ build (3.11) - SUCCESS
# ⚠️ Avertissements : AUCUN !
```

---

## 📊 Résumé des Solutions

| # | Problème | Fichier | Solution | Statut |
| :--- | :--- | :--- | :--- | :--- |
| 1 | isort échouait en CI | `.pre-commit-config.yaml` | `args: ["--profile", "black"]` | ✅ Résolu |
| 2 | trailing-whitespace | `.pre-commit-config.yaml` | Unix LF + auto-fix | ✅ Résolu |
| 3 | imports src/train.py | `src/train.py` | isort ajoute ligne vide | ✅ Résolu |
| 4 | CRLF vs LF | `.pre-commit-config.yaml` | Notepad++ → Unix (LF) | ✅ Résolu |
| 5 | PowerShell `>` rouge | `CONTRIBUTING.md` (FAQ) | Délimiteurs `@' ... '@` corrects | ✅ Documenté |
| 6 | Node.js 20 warning | `.github/workflows/ci.yml` | actions v3 → v4/v5 | ✅ Résolu |

---

## 🎯 Leçons MLOps Clés

```text
┌─────────────────────────────────────────────────────────────┐
│  RÈGLES D'OR POUR ÉVITER CES PROBLÈMES                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. TOUJOURS spécifier les args dans .pre-commit-config.yaml│
│     → Ne pas compter sur pyproject.toml seul                │
│                                                             │
│  2. Tester pre-commit run --all-files LOCALEMENT avant push │
│     → Évite les échecs CI inattendus                        │
│                                                             │
│  3. Utiliser Unix (LF) line endings pour CI/CD              │
│     → Notepad++ : Édition → EOL Conversion → Unix (LF)      │
│                                                             │
│  4. Délimiteurs PowerShell : @' et '@ SEULS sur leur ligne  │
│     → Sortie d'urgence : Ctrl+C                             │
│                                                             │
│  5. Mettre à jour les GitHub Actions régulièrement          │
│     → actions/checkout@v4, setup-python@v5                  │
│                                                             │
│  6. Documenter les problèmes rencontrés                     │
│     → Aide les futurs contributeurs                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📞 Besoin d'Aide ?

- 📖 **[README.md](README.md)** - Documentation complète
- 🐛 **[Issues](https://github.com/valorisa/Tabular-Benchmark-MLOps/issues)** - Signaler un bug
- 💡 **[Feature Request](https://github.com/valorisa/Tabular-Benchmark-MLOps/pulls)** - Suggérer une idée

---

*Merci à tous les contributeurs qui ont aidé à résoudre ces problèmes !* 🎉

*Projet conçu par valorisa pour démonstration MLOps pédagogique.*

---
