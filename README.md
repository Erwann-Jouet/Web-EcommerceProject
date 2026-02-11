# WebTool - Projet Flask MonShop

**Environnement de développement pédagogique pour projets Flask**

---

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.10+** ([Télécharger Python](https://www.python.org/downloads/))
- **pip** (inclus avec Python)
- **Git** ⚠️ **OBLIGATOIRE** ([Télécharger Git](https://git-scm.com/downloads))
- **VS Code** (recommandé)

### Vérifier les installations

```bash
# Vérifier Python sur Linux/Mac
python3 --version
# ou sur Windows
python --version

# Vérifier ou sur Linux/Mac
pip3 --version
# ou pip sur Windows
pip --version

# Vérifier Git (OBLIGATOIRE)
git --version
```

---

## 🚀 Installation et configuration

### 1️⃣ Ouvrir dans VS Code

```bash
# Ouvrir le dossier dans VS Code
code .
```

Ou via le menu : `Fichier > Ouvrir le dossier...`

**⚠️ Important** : Ouvrez bien le dossier racine (celui qui contient `webTool` et `webTool.bat`)

### 2️⃣ Créer l'environnement virtuel

```bash
# Linux/Mac
python3 -m venv .venv --copies

# Windows
python -m venv .venv --copies
```

### 3️⃣ Activer l'environnement virtuel

```bash
# Linux/Mac
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat
```

Une fois activé, vous devriez voir `(.venv)` au début de votre ligne de commande.

### 4️⃣ Recharger la fenêtre VS Code

**Très important** : Après la création de l'environnement virtuel, rechargez VS Code pour qu'il détecte automatiquement le `.venv`

1. Ouvrir la palette de commandes : `Ctrl+Shift+P` (ou `Cmd+Shift+P` sur Mac)
2. Taper : `Developer: Reload Window` ou `Développeur: Recharger la fenêtre`
3. Appuyer sur `Entrée`

VS Code va redémarrer et détecter automatiquement l'environnement virtuel.

### 5️⃣ Vérifier l'interpréteur Python

A la racine du projet :

```bash
# Linux/Mac
which python3

# Windows
which python
```

Vous devriez avoir comme chemin, le chemin absolu qui pointe vers l'interpréteur de votre dossier `.venv/bin/python3` ou `.venv/bin/python`

### Si .venv pas activé -> 6️⃣ Activer manuellement l'environnement virtuel

Voir étape 3️⃣

---

## 🛠️ Utilisation de webTool

`webTool` est un **gestionnaire de projet simplifié** qui encapsule les commandes Git (outil que vous allez étudier dans le module GEN au Semestre 4).  
Il permet de sauvegarder et gérer votre travail **sans avoir besoin de connaître Git**.

### 📚 Commandes disponibles

#### Linux/Mac

```bash
./webTool help           # Afficher l'aide complète
./webTool init           # Initialiser le projet (clone votre dépôt)
./webTool status         # Voir la branche actuelle et l'état du projet
./webTool go <branche>   # Changer de branche (tp ou projet)
./webTool submit [titre] # Sauvegarder et envoyer vos modifications
./webTool sync           # Synchronise votre projet avec le dépôt distant. Attention, cette commande réinitialise votre branche locale pour qu'elle soit identique à celle du dépôt. Toutes les modifications locales non "commit" seront perdues.
./webTool history        # Afficher l'historique des sauvegardes
./webTool update         # Récupérer les mises à jour de l'enseignant
```

#### Windows

```cmd
webTool.bat help           # Afficher l'aide complète
webTool.bat init           # Initialiser le projet (clone votre dépôt)
webTool.bat status         # Voir la branche actuelle et l'état du projet
webTool.bat go <branche>   # Changer de branche (tp ou projet)
webTool.bat submit [titre] # Sauvegarder et envoyer vos modifications
webTool.bat sync           # Synchroniser le projet avec le dépôt distant
webTool.bat history        # Afficher l'historique des sauvegardes
webTool.bat update         # Récupérer les mises à jour de l'enseignant
```

### 📝 Détail des commandes

| Commande         | Description                                                                                                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `help`           | Affiche l'aide complète avec tous les détails                                                                                                                             |
| `init`           | **À lancer une fois** : Clone le dépôt de votre projet hébergé sur le gitlab de l'ISTIC                                                                                   |
| `status`         | Affiche la branche actuelle et l'état des modifications. Vous n'utiliserez que deux branches (tp ou projet). Une branche correspond à un état spécifique de votre projet. |
| `go <branche>`   | Change de branche (`tp` ou `projet`), sauvegarde automatiquement au préalable les modifications faites sur la branche initiale (avant l'exécution de la commande).        |
| `submit [titre]` | Sauvegarde et envoie vos modifications avec un titre                                                                                                                      |
| `sync`           | Synchroniser votre code avec le dépôt. Attention, supprime les modifications locales non soumises. A n'utiliser que si votre projet a été mis à jour entre temps.         |
| `history`        | Affiche la liste des sauvegardes (titre, date, heure)                                                                                                                     |
| `update`         | Récupère les mises à jour (uniquement si demandé par l'enseignant)                                                                                                        |

---

## 🎯 Initialiser et démarrer le projet

### Première utilisation - Étape par étape

Une fois l'environnement virtuel créé et activé (voir section précédente), suivez ces étapes :

#### 1. Initialiser le projet avec webTool

**⚠️ IMPORTANT** : Cette commande va créer le dossier `tp-projet` en clonant le dépôt du projet

```bash
# Linux/Mac
./webTool init

# Windows
webTool.bat init
```

Pour réaliser l'initialisation de votre projet, un **PASSPHRASE** est nécessaire. Ce PASSPHRASE est disponible dans votre Home de la [plateforme PWA-DASHBOARD](https://pwa-dashboard.istic.univ-rennes1.fr/). Ce PASSPHRASE est personnel, **il ne faut pas le communiquer**.

Cette commande va :

- Cloner le dépôt du projet dans le dossier `tp-projet`
- Configurer l'environnement de travail
- Vous placer sur la branche `tp` pour commencer

#### 2. Installer les dépendances Flask

```bash
# Se placer dans le dossier tp-projet
cd tp-projet

# Installer Flask et les dépendances sur Linux/Mac
pip3 install -e ".[dev]"  # Pour les outils de développement
# ou sur Windows
pip install -e ".[dev]"  # Pour les outils de développement
```

#### 3. Lancer le serveur Flask en mode développement

```bash
# Depuis le dossier tp-projet
python run.py development
# ou sur Linux/Mac
python3 run.py development
```

#### 4. Accéder au site en mode développement

- Ouvrir votre navigateur
- Aller sur : **http://localhost:5000**

Pour arrêter le serveur : **`Ctrl+C`**

### Utilisation quotidienne

Une fois l'environnement configuré et le projet initialisé :

```bash
# 1. Activer l'environnement virtuel (si pas déjà fait)
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate       # Windows

# 2. Vérifier le chemin de l'interpréteur Python
which python3 # Linux/Mac
which python # Windows
# Vous devriez avoir comme chemin, le chemin absolu qui pointe vers
# l'interpréteur de votre dossier `.venv/bin/python3` ou `.venv/bin/python`

# 3. Vérifier l'état du projet
./webTool status             # Linux/Mac
webTool.bat status           # Windows

# 4. Aller sur la branche de travail tp
./webTool go tp              # Linux/Mac
webTool.bat go tp            # Windows

# 5. Lancer le serveur Flask en mode développement (depuis tp-projet/)
cd tp-projet
python3 run.py development               # Linux/Mac
python run.py development                # Windows
```

---

## 💾 Sauvegarder votre travail avec webTool

### Commande submit

La commande `submit` sauvegarde vos modifications et les envoie.

```bash
# Avec un titre directement
./webTool submit "TP.US1 : Page d'accueil créée"

# Sans titre (il vous le sera demandé en ligne de commande)
./webTool submit
```

### 📝 Recommandations pour les titres de sauvegarde

- **Commencez par le code de la user story** : `TP.US1`, `TP.US2`, `PRJ.US1`, etc.
- **Titre court et explicite** : décrivez ce qui a été fait
- Si vous n'avez pas fini d'implémenter une User Story, vous pouvez sauvegarder votre travail avec cette commande, il faut juste commencer le titre de sauvegarde par **WIP** (comme pour Work In Progress)
- **Exemples** :
  - ✅ `PRJ.US1 : Correction bug login`
  - ✅ `TP.US2 : Ajout page profil`
  - ✅ `WIP TP.US3 : User story en cours`
  - ❌ `sauvegarde` (trop générique)
  - ❌ `modif` (pas assez précis)

### Exemple de workflow

```bash
# 1. Travailler sur une user story
cd tp-projet
# ... vous codez ...

# 2. Sauvegarder quand c'est terminé
cd ..
./webTool submit "TP.US2 : Affichage liste des produits du catalogue"

# 3. Vérifier l'historique
./webTool history
```

### Affichage de l'historique

```bash
./webTool history
```

Exemple de sortie :

```
>  1:  Initial commit 07-11-2025 05:03:08
>  2:  TP.US1 : Développement page accueil 11-11-2025 06:02:28
>  3:  TP.US2 : Développement de la page produits 11-11-2025 08:38:57
>  4:  TP.TS3 : Implémentation du refactoring 11-11-2025 09:48:08
>  5:  TP.US3 : Développement page Fiche produit 11-11-2025 22:34:06
```

---

## 📁 Structure du projet

**Avant `./webTool init`** :

```
web-tp-projet-xx-yy/
├── .vscode/                  # Configuration VS Code
├── .webTool/                 # Configuration webTool
├── webTool                   # Script utilitaire Linux/Mac
├── webTool.bat               # Script utilitaire Windows
└── README.md                 # Ce fichier
```

**Après `./webTool init` et `initialisation du venv`** :

```
web-tp-projet-xx-yy/
├── .venv/                    # Environnement virtuel Python
├── .vscode/                  # Configuration VS Code
├── .webTool/                 # Configuration webTool
├── tp-projet/
│   ├── app.py                # Application Flask (point d'entrée de l'application)
│   ├── run.py                # Script de lancement du serveur (développement ou production)
│   ├── README.md             # Fichier README de tp-projet
│   ├── ...
├── webTool                   # Script utilitaire Linux/Mac
├── webTool.bat               # Script utilitaire Windows
└── README.md                 # Ce fichier
```

---

## 🔧 Configuration de l'environnement virtuel

### Pourquoi un environnement virtuel ?

Un environnement virtuel Python permet de :

- **Isoler les dépendances** du projet
- **Éviter les conflits** entre différents projets
- **Faciliter le déploiement** en reproduisant l'environnement exact
- **Gérer les versions** de paquets spécifiques au projet

### Vérifier que l'environnement est activé

Lorsque l'environnement est activé, vous devriez voir :

- `(.venv)` au début de votre invite de commande
- Dans VS Code, en bas à gauche : indication de l'environnement Python

### Désactiver l'environnement virtuel

```bash
deactivate
```

### Recréer l'environnement (si nécessaire)

```bash
# Supprimer l'ancien
rm -rf .venv                  # Linux/Mac
rmdir /s .venv                # Windows

# Recréer avec --copies pour éviter les problèmes de symlinks
python3 -m venv .venv --copies    # Linux/Mac
python -m venv .venv --copies     # Windows

# Réinstaller les dépendances Python
cd tp-projet
pip3 install -r requirements.txt     # Linux/Mac
pip install -r requirements.txt      # Windows
```

---

## 🌿 Branches de travail

Le projet utilise deux branches principales :

- **`tp`** : Pour les deux séances de travaux pratiques
- **`projet`** : Pour les huit séances de TP-projet

### Changer de branche

```bash
# Passer sur la branche TP
./webTool go tp

# Passer sur la branche projet
./webTool go projet
```

**Note** : webTool sauvegarde automatiquement vos modifications avant de changer de branche.

---

## ⚠️ Points importants

### 1. Lancer webTool depuis la racine

**Toujours** lancer les commandes webTool depuis le dossier racine (celui qui contient `webTool`)

```bash
# ✅ Correct
./webTool status

# ❌ Incorrect (depuis tp-projet/)
cd tp-projet
./webTool status  # Ne fonctionnera pas
```

### 2. Sauvegarder régulièrement

N'oubliez pas de faire `./webTool submit` :

- Dès que vous avez terminé une user story
- À la fin de chaque séance de TP
- Avant de changer de branche

### 3. Git est encapsulé par webTool

Vous **n'avez pas besoin** de connaître ou d'utiliser Git directement.  
webTool gère tout pour vous :

- Sauvegarde des modifications
- Changement de branche
- Historique des versions

---

## 🐛 Dépannage

### Le serveur Flask ne démarre pas

**Problème** : `ModuleNotFoundError: No module named 'flask'`

**Solution** :

```bash
# 1. Vérifier que l'environnement virtuel est activé
# Vous devez voir (.venv) dans votre terminal

# 2. Si pas activé, l'activer
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate       # Windows

# 3. Installer Flask
cd tp-projet
pip3 install -r requirements.txt # Linux/Mac
pip install -r requirements.txt  # Windows
```

### Git n'est pas installé

**Problème** : `git: command not found` ou `git n'est pas reconnu`

**Solution** :

- Git est **OBLIGATOIRE** pour ce projet
- Télécharger et installer Git : https://git-scm.com/downloads
- Redémarrer le terminal après installation
- Vérifier : `git --version`

### Python non trouvé sur Linux/Mac

**Problème** : `python: command not found`

**Solution** : Utilisez `python3` au lieu de `python`

```bash
python3 -m venv .venv
python3 run.py production
```

### Permission refusée pour webTool (Linux/Mac)

**Problème** : `Permission denied: ./webTool`

**Solution** : Rendre le script exécutable

```bash
chmod +x webTool
./webTool help
```

### VS Code n'utilise pas le bon Python

**Problème** : VS Code utilise le Python système au lieu de `.venv`

**Solution** :

1. `Ctrl+Shift+P` → `Python: Select Interpreter` ou `Python: Sélectionner un interpréteur`
2. Choisir l'interpréteur dans `.venv`
3. Recharger la fenêtre : `Developer: Reload Window` ou `Développeur: Recharger la fenêtre`

### Le dossier tp-projet n'existe pas

**Problème** : Le dossier `tp-projet` n'est pas présent

**Solution** :

```bash
# Vous devez d'abord initialiser le projet
./webTool init
```

Cette commande va cloner le dépôt et créer le dossier `tp-projet`.

### Erreur de port déjà utilisé

**Problème** : `Address already in use - Port 5000`

**Solution** :

```bash
# Trouver et arrêter le processus utilisant le port 5000
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Le venv ne s'active pas correctement (Linux/Mac)

**Problème** : Après activation du venv, `which python3` pointe toujours vers `/usr/bin/python3` au lieu du `.venv`

**Explication** : Le venv a été créé avec des liens symboliques au lieu de copies des binaires Python.

**Solution** : Recréer le venv avec l'option `--copies`

```bash
# 1. Désactiver et supprimer l'ancien venv
deactivate
rm -rf .venv

# 2. Recréer avec --copies
python3 -m venv .venv --copies

# 3. Activer le nouveau venv
source .venv/bin/activate

# 4. Vérifier que ça fonctionne
which python3
# Devrait afficher : .../web-tp-projet-xx-yy/.venv/bin/python3

# 5. Réinstaller les dépendances
cd tp-projet
pip3 install -r requirements.txt
```

---

## 📚 Documentation du projet

Pour plus d'informations sur le projet Flask MonShop :

- Consultez le fichier [tp-projet/README.md](./tp-projet/README.md) (après `./webTool init`)
- Ce fichier contient la documentation complète du projet
- User Stories, progression pédagogique, concepts Flask/Jinja, etc.

---

## 💡 Exemple de workflow complet

```bash
# === PREMIÈRE SÉANCE ===

# 1. Créer et activer l'environnement virtuel
python3 -m venv .venv --copies
source .venv/bin/activate

# 2. Ouvrir dans VS Code et recharger
code .
# Ctrl+Shift+P → Developer: Reload Window

# 3. Initialiser le projet
./webTool init

# 4. Installer les dépendances
cd tp-projet
pip3 install -r requirements.txt

# 5. Lancer le serveur
python3 run.py development
# Navigateur : http://localhost:5000

# 6. Travailler sur le code
cd tp-projet
# ... coder ...
python3 run.py

# 7. Sauvegarder à la fin
cd ..
./webTool submit "TP.US1 : Page d'accueil terminée"

# 8. Vérifier l'historique
./webTool history

# === SÉANCES SUIVANTES ===

# 1. Activer l'environnement ou juste ouvrir le projet avec VS Code
source .venv/bin/activate

# 2. Vérifier l'état
./webTool status

# 3. Aller sur la bonne branche
./webTool go tp

# 4. Travailler sur le code
cd tp-projet
# ... coder ...
python3 run.py

# 5. Sauvegarder à la fin
cd ..
./webTool submit "TP.US1 : Page d'accueil terminée"

# 6. Vérifier l'historique
./webTool history
```

---

## 🆘 Besoin d'aide ?

1. **Afficher l'aide webTool** :

   ```bash
   ./webTool help
   ```

2. **Documentation officielle** :

   - [Flask](https://flask.palletsprojects.com/)
   - [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

3. **Problèmes courants** : Consultez la section Dépannage ci-dessus

4. **Enseignant** : Contactez votre enseignant pour toute question

---

## 📝 Notes importantes

- ⚠️ **Git est OBLIGATOIRE** pour utiliser webTool
- ⚠️ **Lancez toujours webTool depuis la racine** du projet
- ⚠️ **Toujours activer l'environnement virtuel** avant de travailler
- ⚠️ **Recharger VS Code** après création du `.venv`
- ✅ **Faire `./webTool init`** avant de commencer (une seule fois)
- ✅ **Utiliser `./webTool submit`** dès qu'une user story est terminée
- ✅ **Sauvegardes fréquentes** pour ne pas perdre votre travail
- ✅ **Titres de sauvegarde explicites** pour un historique clair

---

**Bon développement ! 🚀**
