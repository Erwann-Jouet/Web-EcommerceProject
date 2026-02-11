#!/bin/bash

# Script de correction des permissions des clés SSH
# Ce script vérifie et corrige automatiquement les permissions des clés SSH

# Couleurs pour l'affichage
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🔧 Vérification des permissions des clés SSH..."
echo ""

# Récupérer le dossier du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SSH_DIR="$SCRIPT_DIR/.webTool/.ssh"

# Vérifier que le dossier .ssh existe
if [ ! -d "$SSH_DIR" ]; then
    echo -e "${RED}❌ Erreur: Le dossier .webTool/.ssh n'existe pas${NC}"
    exit 1
fi

# Variables pour compter les corrections
corrections=0
errors=0

# Parcourir tous les fichiers dans .ssh
for file in "$SSH_DIR"/*; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        
        # Clé privée (sans extension .pub)
        if [[ ! "$filename" =~ \.pub$ ]]; then
            current_perms=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%A" "$file" 2>/dev/null)
            
            if [ "$current_perms" != "600" ]; then
                echo -e "${YELLOW}⚠️  Clé privée $filename a les permissions $current_perms${NC}"
                chmod 600 "$file"
                if [ $? -eq 0 ]; then
                    echo -e "${GREEN}✅ Permissions corrigées en 600 pour $filename${NC}"
                    ((corrections++))
                else
                    echo -e "${RED}❌ Impossible de modifier les permissions de $filename${NC}"
                    ((errors++))
                fi
            else
                echo -e "${GREEN}✓${NC} Clé privée $filename : permissions OK (600)"
            fi
        
        # Clé publique (avec extension .pub)
        else
            current_perms=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%A" "$file" 2>/dev/null)
            
            if [ "$current_perms" != "644" ]; then
                echo -e "${YELLOW}⚠️  Clé publique $filename a les permissions $current_perms${NC}"
                chmod 644 "$file"
                if [ $? -eq 0 ]; then
                    echo -e "${GREEN}✅ Permissions corrigées en 644 pour $filename${NC}"
                    ((corrections++))
                else
                    echo -e "${RED}❌ Impossible de modifier les permissions de $filename${NC}"
                    ((errors++))
                fi
            else
                echo -e "${GREEN}✓${NC} Clé publique $filename : permissions OK (644)"
            fi
        fi
    fi
done

# Vérifier aussi les permissions du dossier .ssh lui-même
ssh_dir_perms=$(stat -c "%a" "$SSH_DIR" 2>/dev/null || stat -f "%A" "$SSH_DIR" 2>/dev/null)
if [ "$ssh_dir_perms" != "700" ]; then
    echo -e "${YELLOW}⚠️  Dossier .ssh a les permissions $ssh_dir_perms${NC}"
    chmod 700 "$SSH_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Permissions du dossier .ssh corrigées en 700${NC}"
        ((corrections++))
    else
        echo -e "${RED}❌ Impossible de modifier les permissions du dossier .ssh${NC}"
        ((errors++))
    fi
else
    echo -e "${GREEN}✓${NC} Dossier .ssh : permissions OK (700)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $corrections -eq 0 ] && [ $errors -eq 0 ]; then
    echo -e "${GREEN}✅ Toutes les permissions sont correctes !${NC}"
elif [ $errors -eq 0 ]; then
    echo -e "${GREEN}✅ $corrections correction(s) effectuée(s) avec succès${NC}"
else
    echo -e "${RED}❌ $errors erreur(s) lors de la correction${NC}"
    exit 1
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
