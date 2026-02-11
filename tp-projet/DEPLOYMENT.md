# 🚀 Guide de Déploiement

Ce document explique comment déployer facilement cette application e-commerce Flask.

## 📦 Option 1 : Lancement avec Docker (Recommandé)

### Prérequis

- Docker installé ([Télécharger Docker](https://www.docker.com/get-started))
- Docker Compose installé (inclus avec Docker Desktop)

### Lancement rapide

1. **Clonez le dépôt :**

   ```bash
   git clone <votre-repo-url>
   cd tp-projet
   ```

2. **Lancez l'application avec Docker Compose :**

   ```bash
   docker-compose up
   ```

3. **Accédez à l'application :**
   Ouvrez votre navigateur à l'adresse : <http://localhost:5000>

4. **Pour arrêter l'application :**

   ```bash
   docker-compose down
   ```

### Initialiser la base de données

Si vous devez initialiser la base de données avec des données de test :

```bash
# Entrez dans le conteneur
docker-compose exec web bash

# Lancez les fixtures
python datafixtures/import_all.py

# Sortez du conteneur
exit
```

---

## 🌐 Option 2 : Déploiement en ligne GRATUIT

### A) Déploiement sur Render (Gratuit)

1. Créez un compte sur [Render.com](https://render.com)

2. Créez un fichier `render.yaml` à la racine du projet :

   ```yaml
   services:
     - type: web
       name: ecommerce-flask
       env: python
       buildCommand: "pip install -e ."
       startCommand: "gunicorn app:app --bind 0.0.0.0:$PORT"
       envVars:
         - key: FLASK_CONFIG
           value: production
         - key: SECRET_KEY
           generateValue: true
         - key: DATABASE_URL
           fromDatabase:
             name: ecommerce-db
             property: connectionString
   
   databases:
     - name: ecommerce-db
       databaseName: ecommerce
       user: ecommerce_user
   ```

3. Sur Render, cliquez sur "New +" → "Blueprint" et connectez votre dépôt Git

4. Render détectera automatiquement le fichier `render.yaml` et déploiera votre application

### B) Déploiement sur Railway (Gratuit)

1. Créez un compte sur [Railway.app](https://railway.app)

2. Cliquez sur "New Project" → "Deploy from GitHub repo"

3. Sélectionnez votre dépôt

4. Railway détectera automatiquement qu'il s'agit d'une application Python

5. Ajoutez les variables d'environnement :
   - `FLASK_CONFIG` = production
   - `SECRET_KEY` = (générez une clé aléatoire)

6. Ajoutez une base de données PostgreSQL depuis l'onglet "Add Plugin"

### C) Déploiement sur Fly.io (Gratuit)

1. Installez Fly.io CLI :

   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Connectez-vous :

   ```bash
   fly auth login
   ```

3. Lancez le déploiement :

   ```bash
   fly launch
   ```

4. Suivez les instructions pour configurer votre application

---

## 🛠️ Option 3 : Installation manuelle (sans Docker)

### Prérequis

- Python 3.8 ou supérieur
- pip

### Étapes

1. **Clonez le dépôt :**

   ```bash
   git clone <votre-repo-url>
   cd tp-projet
   ```

2. **Créez un environnement virtuel :**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installez les dépendances :**

   ```bash
   pip install -e .
   ```

4. **Configurez l'environnement :**

   ```bash
   cp .env.example .env
   # Éditez .env avec vos valeurs
   ```

5. **Lancez l'application :**

   ```bash
   python run.py development
   ```

6. **Accédez à l'application :**
   <http://localhost:5000>

---

## 📝 Notes importantes

- **En production**, changez toujours `SECRET_KEY` par une valeur sécurisée
- **La base de données SQLite** n'est pas recommandée en production, utilisez PostgreSQL
- **Pour les déploiements gratuits**, il peut y avoir des limitations (temps d'inactivité, ressources)

---

## 🐛 Dépannage

### L'application ne démarre pas avec Docker

```bash
# Reconstruisez les images
docker-compose build --no-cache
docker-compose up
```

### Erreur de base de données

```bash
# Supprimez la base de données existante et recréez-la
rm -rf data/app.db
docker-compose restart
```

### Port 5000 déjà utilisé

Modifiez le port dans `docker-compose.yml` :

```yaml
ports:
  - "8080:5000"  # Utilisez le port 8080 au lieu du 5000
```

---

## 📧 Support

Pour toute question, ouvrez une issue sur le dépôt GitHub.
