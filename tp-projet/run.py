#!/usr/bin/env python3
"""
Script de lancement pour différents environnements.
Facilite le changement d'environnement pour les étudiants.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def copy_env_file(env_name: str) -> None:
    """Copie le fichier .env approprié."""
    env_file: str = f".env.{env_name}"
    example_file: str = f".env.{env_name}.example"

    # Vérifier si le fichier .env.{env_name} existe
    if not Path(env_file).exists():
        # Si il n'existe pas, vérifier si le fichier .example existe
        if Path(example_file).exists():
            print(f"📋 Fichier {env_file} introuvable, copie depuis {example_file}")
            shutil.copy(example_file, env_file)
            print(f"✅ Fichier {env_file} créé depuis le modèle")
        else:
            print(f"❌ Fichier {env_file} et {example_file} introuvables !")
            print(f"💡 Créez un fichier {example_file} ou {env_file} pour continuer")
            sys.exit(1)

    # Copier le fichier d'environnement vers .env
    shutil.copy(env_file, ".env")
    print(f"✅ Configuration {env_name.upper()} activée (.env mis à jour)")


def main() -> None:
    """Point d'entrée principal."""
    if len(sys.argv) != 2:
        print("Usage: python run.py [development|production]")
        print("\nExemples:")
        print("  python run.py development  # Lance en mode développement")
        print("  python run.py production   # Lance en mode production")
        sys.exit(1)

    env_name: str = sys.argv[1].lower()

    if env_name not in ["development", "production"]:
        print("❌ Environnement invalide. Utilisez 'development' ou 'production'")
        sys.exit(1)

    # Copier le bon fichier .env
    copy_env_file(env_name)

    # Lancer l'application
    print(f"🚀 Lancement en mode {env_name.upper()}...")

    # Déterminer le chemin vers l'environnement virtuel
    venv_path = os.path.join(os.getcwd(), "..", ".venv")
    flask_executable = os.path.join(venv_path, "bin", "flask")

    if env_name == "development":
        print("📍 URL: http://localhost:5000")
        if os.path.exists(flask_executable):
            os.system(f'"{flask_executable}" run --reload')
        else:
            print("⚠️ Environnement virtuel non trouvé, tentative avec flask global")
            os.system("flask run --reload")
    else:
        # Support du port variable pour les plateformes de déploiement (Render, Railway, Heroku, etc.)
        port: str = os.environ.get("PORT", "8000")
        print("📍 Mode production - Lancement avec Gunicorn")
        print(f"📍 URL: http://localhost:{port}")

        # Activer l'environnement virtuel et lancer gunicorn
        venv_activate: str = os.path.join(os.getcwd(), "..", ".venv", "bin", "activate")
        if os.path.exists(venv_activate):
            # Utiliser subprocess pour gérer correctement les espaces
            cmd: str = f'source "{venv_activate}" && gunicorn --bind 0.0.0.0:{port} --workers 4 app:app'
            subprocess.run(cmd, shell=True, executable="/bin/bash", check=False)
        else:
            print("⚠️ Environnement virtuel non trouvé, tentative avec gunicorn global")
            os.system(f"gunicorn --bind 0.0.0.0:{port} --workers 4 app:app")


if __name__ == "__main__":
    main()
