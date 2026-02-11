# 🚀 Guide de Démarrage Rapide

Ce document explique comment lancer l'application e-commerce Flask.

## ⚡ Option 1 : Script automatique (Recommandé)

**La méthode la plus simple** - tout est automatisé !

```bash
# 1. Clonez le projet
git clone <votre-repo-url>
cd tp-projet

# 2. Lancez le script
./setup.sh
```

Le script va :

- ✅ Créer un environnement virtuel Python
- ✅ Installer toutes les dépendances
- ✅ Configurer le fichier .env
- ✅ Lancer l'application automatiquement

**⏱️ Temps** : 2-3 minutes  
**➜ Accès** : <http://localhost:5000>

---

## 💻 Option 2 : Installation manuelle

Si vous préférez contrôler chaque étape :

```bash
# 1. Cloner le projet
git clone <votre-repo-url>
cd tp-projet

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 3. Installer les dépendances
pip install -e .

# 4. Lancer l'application
python run.py development
```

**⏱️ Temps** : 5 minutes  
**➜ Accès** : <http://localhost:5000>

---

## 🎯 Fonctionnalités

- 🛍️ **Catalogue produits** - Navigation par catégories
- 🔍 **Recherche** - Trouvez rapidement vos produits
- 🛒 **Panier** - Ajout/suppression d'articles
- 👤 **Authentification** - Inscription et connexion
- 📱 **Responsive** - Fonctionne sur tous les écrans

---

## 🔧 Dépannage

### Le script setup.sh n'est pas exécutable

```bash
chmod +x setup.sh
./setup.sh
```

### Python introuvable

Installez Python 3.8+ depuis <https://python.org>

### Port 5000 déjà utilisé

Modifiez le port dans `run.py` ou arrêtez l'autre application.

### Erreur lors de l'installation des dépendances

```bash
pip install --upgrade pip
pip install -e .
```

---

## 📚 Documentation

- **README complet** : [README.md](README.md)
- **Configuration** : Voir `.env.example`
- **Dépendances** : Voir `pyproject.toml`

---

**Bon développement ! 🚀**
