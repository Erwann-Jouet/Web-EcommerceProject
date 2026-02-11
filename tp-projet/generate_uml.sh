#!/bin/bash
# Script pour générer le diagramme de classes UML des modèles

echo "📊 Génération du diagramme de classes UML..."

# Vérifier si graphviz est installé
if ! command -v dot &> /dev/null; then
    echo "⚠️  Graphviz n'est pas installé. Installation requise:"
    echo "   sudo apt install graphviz  # Sur Ubuntu/Debian"
    echo "   brew install graphviz      # Sur macOS"
    exit 1
fi

# Vérifier si le fichier DOT existe
if [ ! -f "classes_models.dot" ]; then
    echo "❌ Fichier classes_models.dot introuvable"
    exit 1
fi

# Générer le diagramme PNG à partir du fichier DOT
dot -Tpng classes_models.dot -o classes_models.png

if [ $? -eq 0 ]; then
    echo "✅ Diagramme généré avec succès!"
    echo "   📄 classes_models.png  - Diagramme de classes"
    echo ""
    echo "💡 Pour modifier le diagramme, éditez le fichier classes_models.dot"
    echo "   puis relancez ce script pour regénérer l'image."
else
    echo "❌ Erreur lors de la génération du diagramme"
    exit 1
fi
