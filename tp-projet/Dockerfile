# Dockerfile pour l'application e-commerce Flask
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY pyproject.toml ./

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Copier tout le projet
COPY . .

# Créer le fichier .env si nécessaire (sera surchargé par docker-compose)
RUN if [ ! -f .env ]; then \
    echo "FLASK_CONFIG=development" > .env && \
    echo "SECRET_KEY=dev-secret-key-change-in-production" >> .env && \
    echo "DATABASE_URL=sqlite:///app.db" >> .env; \
    fi

# Exposer le port Flask
EXPOSE 5000

# Variable d'environnement pour Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Script de démarrage
CMD ["python", "run.py", "development"]
