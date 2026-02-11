#!/bin/bash
# Script de setup automatique pour démarrer rapidement le projet

set -e  # Arrêter en cas d'erreur

echo "🚀 Setup automatique du projet E-commerce Flask"
echo "==============================================="
echo ""

# Vérifier si Docker est installé
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✅ Docker et Docker Compose détectés"
    echo ""
    read -p "Voulez-vous utiliser Docker ? (recommandé) [O/n] : " use_docker
    
    if [[ "$use_docker" != "n" && "$use_docker" != "N" ]]; then
        echo ""
        echo "🐳 Lancement avec Docker..."
        docker-compose up --build
        exit 0
    fi
fi

echo ""
echo "📦 Installation manuelle..."
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé !"
    echo "   Installez Python 3.8+ depuis https://python.org"
    exit 1
fi

echo "✅ Python 3 détecté : $(python3 --version)"

# Créer un environnement virtuel
if [ ! -d "venv" ]; then
    echo "📂 Création de l'environnement virtuel..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel existe déjà"
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install --upgrade pip > /dev/null
pip install -e . > /dev/null
echo "✅ Dépendances installées"

# Créer le fichier .env s'il n'existe pas
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📋 Copie de .env.example vers .env..."
        cp .env.example .env
        echo "✅ Fichier .env créé"
    else
        echo "📝 Création du fichier .env..."
        cat > .env << EOF
FLASK_CONFIG=development
SECRET_KEY=dev-secret-key-$(date +%s)
DATABASE_URL=sqlite:///app.db
FLASK_DEBUG=1
EOF
        echo "✅ Fichier .env créé"
    fi
else
    echo "✅ Fichier .env existe déjà"
fi

echo ""
echo "✨ Setup terminé avec succès !"
echo ""
echo "🚀 Pour lancer l'application :"
echo "   python run.py development"
echo ""
echo "📍 L'application sera accessible sur : http://localhost:5000"
echo ""

# Demander si on veut lancer maintenant
read -p "Voulez-vous lancer l'application maintenant ? [O/n] : " launch_now

if [[ "$launch_now" != "n" && "$launch_now" != "N" ]]; then
    echo ""
    echo "🚀 Lancement de l'application..."
    python run.py development
fi
