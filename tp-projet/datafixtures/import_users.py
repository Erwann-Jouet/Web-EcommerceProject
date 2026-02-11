"""
Script pour charger les utilisateurs depuis un fichier JSON dans la base SQLite.
"""

import json

from werkzeug.security import generate_password_hash

from src.models import User
from src.models.database import db

USERS_FILE = "datafixtures/json/users.json"


def load_users() -> None:
    """
    Charge les utilisateurs depuis un fichier JSON et les ajoute à la base de données SQLite.
    Si un utilisateur existe déjà (même username), il n'est pas ajouté à nouveau.
    """
    with open(USERS_FILE, encoding="utf-8") as f:
        users = json.load(f)
    for user in users:
        # Vérifier si l'utilisateur existe déjà
        if not User.find_by_username(username=user["username"]):
            # Hasher le mot de passe avant insertion
            user["password"] = generate_password_hash(user["password"])
            user = User(**user)
            db.session.add(user)
    db.session.commit()
    print(f"{len(users)} utilisateurs chargés.")
