@echo off
REM WebTool wrapper pour Windows
REM Redirige vers le script Python principal

set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%.webTool\bin\webtool.py

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur : Python n'est pas installé sur votre ordinateur !
    echo ℹ️  Téléchargez Python sur : https://www.python.org/downloads/
    exit /b 1
)

REM Lancer le script Python
python "%PYTHON_SCRIPT%" %*
