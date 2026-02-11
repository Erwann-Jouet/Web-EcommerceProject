# 🛍️ MonShop - E-commerce Flask

> Application e-commerce moderne développée avec Flask et SQLAlchemy

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.25-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Démarrage rapide](#-démarrage-rapide)
- [Installation détaillée](#-installation-détaillée)
- [Structure du projet](#-structure-du-projet)
- [Modèles de données](#-modèles-de-données)
- [Documentation](#-documentation)

---

## 📖 À propos

**MonShop** est une application e-commerce complète avec :

- 🛍️ Gestion de catalogue produits avec catégories et sous-catégories
- 🛒 Système de panier d'achat dynamique
- 👤 Authentification multi-rôles (admin, gérant, client)
- 💾 Base de données relationnelle avec SQLAlchemy ORM
- 📱 Interface responsive
- 🔍 Recherche et filtres avancés

**Stack technique :** Flask, SQLAlchemy, Jinja2, SQLite

---

## ✨ Fonctionnalités

### 🛍️ Catalogue

- Navigation par catégories et sous-catégories
- Recherche de produits
- Filtrage par marque et prix
- Fiches produits détaillées

### 🛒 Panier

- Ajout/suppression d'articles
- Modification des quantités
- Persistance du panier en session

### 👤 Authentification

- Inscription et connexion
- Gestion de profil utilisateur
- Rôles utilisateurs (admin, gérant, client)

### 💾 Base de données

- SQLite (développement)
- Modèles avec SQLAlchemy ORM
- Fixtures de données pour tests

---

## 🚀 Démarrage rapide

### ⚡ Option 1 : Script automatique (Recommandé)

```bash
# Cloner le projet
git clone https://github.com/votre-username/votre-repo.git
cd tp-projet

# Installer et lancer
./setup.sh
```

**➜** L'application sera accessible sur <http://localhost:5000>

---

## 📁 Structure du projet

```
tp-projet/
├── 📄 app.py                   # Application Flask principale
├── 📄 run.py                   # Script de lancement
├── 📄 config.py                # Configuration de l'application
├── 📄 setup.sh                 # Script d'installation automatique
├── 📄 pyproject.toml           # Dépendances et configuration
│
├── 📂 src/                     # Code source
│   ├── 📂 models/              # Modèles de données (SQLAlchemy)
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── user.py
│   │   ├── cart.py
│   │   └── cart_item.py
│   │
│   ├── 📂 auth/                # Authentification
│   │   ├── routes.py
│   │   └── utils.py
│   │
│   ├── 📂 catalog/             # Catalogue produits
│   │   └── routes.py
│   │
│   ├── 📂 cart/                # Panier d'achat
│   │   ├── routes.py
│   │   └── services.py
│   │
│   ├── 📂 api/                 # API REST
│   │   └── routes.py
│   │
│   └── 📂 templates/           # Templates Jinja2
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       └── cart/
│
├── 📂 static/                  # Fichiers statiques
│   ├── css/
│   ├── js/
│   └── img/
│
└── 📂 datafixtures/            # Données de test
    ├── import_all.py
    └── json/
        ├── categories.json
        ├── products.json
        └── users.json
```

---

## 💾 Modèles de données

Le projet utilise **SQLAlchemy** avec **SQLite** et fournit cinq modèles principaux :

### 📦 Category

Représente les catégories et sous-catégories de produits avec une relation parent-enfant.

**Champs :**

- `id` : Identifiant unique
- `name` : Nom de la catégorie
- `slug` : URL-friendly identifier
- `parent_id` : Référence à la catégorie parente

**Relations :**

- `parent` : Catégorie parente
- `children` : Sous-catégories

### 🏷️ Product

Représente les produits du catalogue.

**Champs :**

- `id`, `name`, `slug`, `brand`
- `description`, `price`
- `category_id`, `subcategory_id`
- `image_url`, `stock_quantity`

**Relations :**

- `category` : Catégorie principale
- `subcategory` : Sous-catégorie (optionnelle)

### 👤 User

Représente les utilisateurs du site.

**Champs :**

- `id`, `username`, `password`, `email`
- `role` : admin, gérant, client
- `adresse`, `code_postal`, `ville`, `pays`

### 🛒 Cart & CartItem

Gestion du panier d'achat.

**Cart :**

- `id`, `user_id`, `created_at`, `updated_at`

**CartItem :**

- `id`, `cart_id`, `product_id`, `quantity`

---

## 🛠️ Technologies utilisées

| Technologie | Version | Usage |
|-------------|---------|-------|
| **Python** | 3.8+ | Langage principal |
| **Flask** | 3.0.0 | Framework web |
| **SQLAlchemy** | 2.0.25 | ORM base de données |
| **Flask-SQLAlchemy** | 3.1.1 | Intégration SQLAlchemy |
| **Jinja2** | - | Moteur de templates |
| **SQLite** | - | Base de données |

---

## 📚 Documentation

- **[Guide de démarrage rapide](QUICKSTART.md)** - Installation en 5 minutes
- **[Informations projet](PROJET_INFO.md)** - Vue d'ensemble complète
- **[Configuration](config.py)** - Paramètres de l'application

### Ressources externes

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentation Jinja2](https://jinja.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

---

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 Auteur

**Erwann Jouet**

- GitHub: [@Erwann-Jouet](https://github.com/Erwann-Jouet)

---

## 🙏 Remerciements

- Flask et SQLAlchemy pour leurs excellents frameworks
- La communauté Python pour les ressources et documentation

---

**⭐ N'hésitez pas à mettre une étoile si ce projet vous a plus !

**Bon développement ! 🚀**
