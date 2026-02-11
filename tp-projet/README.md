# Projet MonShop - Flask & Jinja

**Projet pédagogique L2 Informatique - E-commerce**

---

## � Démarrage Rapide

### Avec Docker (Recommandé - 1 commande)

```bash
docker-compose up
```

Puis ouvrez <http://localhost:5000>

### Sans Docker

```bash
pip install -e .
python run.py development
```

**📘 Pour le déploiement en ligne ou plus de détails, consultez [DEPLOYMENT.md](DEPLOYMENT.md)**

---

## �📖 À propos

Ce projet est un support pédagogique pour apprendre Flask et Jinja à travers le développement progressif d'un site de e-commerce.
Vous allez construire le site en suivant les User Stories ci-dessous.

---

## 📁 Structure attendue du dépôt étudiant

```
tp-projet/
├── app.py                # Application Flask (point d'entrée)
├── run.py                # Script de lancement du serveur
├── README.md             # Ce fichier
├── requirements.txt      # Dépendances Python
├── pyproject.toml        
├── .vscode/
│   └── settings.json     # Configuration VS Code (doit être présent)
├── data/
│   └── json/
│       ├── categories.json
│       ├── products.json
│       └── users.json
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
│       └── products/
│       └── logo.svg
│       └── favicon.svg
├── templates/
│   ├── base.html
│   ├── index.html
│   └── catalog/
│       ├── products.html
│       └── product_detail.html
├── routes/
│   ├── __init__.py
│   └── catalog.py
```

---

## 📁 Modèles de données

Le projet utilise SQLAlchemy avec SQLite et fournit trois modèles de base :

### Category

Représente les catégories et sous-catégories de produits avec une relation parent-enfant.

- Champs : `id`, `name`, `slug`, `parent_id`
- Relations : `parent` (catégorie parente), `children` (sous-catégories)
- Méthodes : recherche par nom/slug/id, récupération des catégories principales et sous-catégories

### Product

Représente les produits du catalogue.

- Champs : `id`, `name`, `slug`, `brand`, `description`, `price`, `category_id`, `subcategory_id`, `image_url`, `stock_quantity`
- Relations : `category` (catégorie principale), `subcategory` (sous-catégorie optionnelle)
- Méthodes : recherche par nom/slug, filtrage par catégorie/marque, récupération des marques disponibles

### User

Représente les utilisateurs du site (admin, gérant, client).

- Champs : `id`, `username`, `password`, `email`, `role`, `adresse`, `code_postal`, `ville`, `pays`
- Méthodes : recherche par id/email/username, récupération de tous les utilisateurs

---

## 🚀 Installation et lancement

   Le projet se lance comme pour le cycle précédent (cf README du dossier parent avec installation des dépendances, lancement du projet web).

   La **différence** réside dans le fait que désormais nous utilisons une base de données. Il faut donc créer la structure et la peupler avant de lancer l'application web. Pour ce faire, il suffit d'exécuter ce qu'on appelle une **datafixtures** qui va créer la structure de la base de données à partir des modèles et dans un deuxième temps à partir de fichiers json va peupler la base de données avec des données initiales. Ces données seront ensuite modifiées en base de données via l'utilisation de l'application Web.

   **Initialiser la base de données** :

   ```bash
   python3 -m datafixtures.import_all
   ```

   Ce script va :

- Créer toutes les tables nécessaires (categories, users, products)
- Importer les catégories depuis `datafixtures/json/categories.json`
- Importer les utilisateurs depuis `datafixtures/json/users.json`
- Importer les produits depuis `datafixtures/json/products.json`

---

## 📖 Ressources et conseils

- [Liste des User stories à développer](https://foad.univ-rennes.fr/mod/page/view.php?id=1020062)
- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation Jinja](https://jinja.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Real Python - Flask](https://realpython.com/tutorials/flask/)

**Conseils :**

- Suivez la progression des User Stories dans l'ordre
- Testez régulièrement votre application
- Utilisez les outils de qualité de code (flake8, black, djlint...)
- Demandez de l'aide à l'enseignant en cas de blocage

---

## 📝 Licence

Projet pédagogique - Libre d'utilisation pour l'enseignement

---
