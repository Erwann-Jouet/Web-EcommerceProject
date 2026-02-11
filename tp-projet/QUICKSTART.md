# 🚀 Démarrage Rapide - Pour les visiteurs GitHub

Ce projet est une application e-commerce Flask. Voici comment la visualiser sans installation complexe :

## ✨ Option 1 : Docker (Le plus simple - 2 commandes)

**Prérequis** : Avoir [Docker Desktop](https://www.docker.com/get-started) installé

```bash
# 1. Clonez le projet
git clone <votre-url-repo>
cd tp-projet

# 2. Lancez l'application
docker-compose up
```

**C'est tout !** 🎉 L'application est accessible sur <http://localhost:5000>

Pour arrêter : `Ctrl+C` puis `docker-compose down`

---

## 🌐 Option 2 : Voir une démo en ligne

**Versions déployées** (aucune installation nécessaire) :

- 🔗 **Demo Render** : [lien à venir après déploiement]
- 🔗 **Demo Railway** : [lien à venir après déploiement]

*Note : La première visite peut prendre 30-60 secondes (démarrage du serveur gratuit)*

---

## 💻 Option 3 : Installation traditionnelle

Si vous ne pouvez pas utiliser Docker :

```bash
# 1. Clonez et entrez dans le projet
git clone <votre-url-repo>
cd tp-projet

# 2. Créez un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 3. Installez les dépendances
pip install -e .

# 4. Lancez l'application
python run.py development
```

Ouvrez <http://localhost:5000>

---

## 📚 Documentation complète

- **Guide de déploiement complet** : [DEPLOYMENT.md](DEPLOYMENT.md)
- **README du projet** : [README.md](README.md)

---

## 🎯 Fonctionnalités

- 🛍️ Catalogue de produits avec recherche
- 🛒 Panier d'achat
- 👤 Authentification utilisateur
- 📱 Interface responsive
- 💾 Base de données SQLite (développement)

---

## 🐛 Problèmes courants

**Le port 5000 est déjà utilisé ?**

```bash
# Changez le port dans docker-compose.yml
ports:
  - "8080:5000"  # Utilisez 8080
```

**L'application ne démarre pas ?**

```bash
# Reconstruisez les images Docker
docker-compose build --no-cache
docker-compose up
```

---

## 📧 Contact

Pour toute question, ouvrez une issue sur GitHub.

**Bon test ! 🚀**
