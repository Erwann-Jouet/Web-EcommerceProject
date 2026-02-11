"""Modèle User pour les utilisateurs du site (admin, gérant, client)."""

from typing import Any, cast

from src.models.database import db


class User(db.Model):  # type: ignore
    """
    Modèle représentant un utilisateur du site (admin, gérant, client).
    Inclut les informations de connexion et l'adresse postale.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default="client")  # admin, gerant, client
    adresse = db.Column(db.String(128))
    code_postal = db.Column(db.String(10))
    ville = db.Column(db.String(64))
    pays = db.Column(db.String(64))

    def __repr__(self) -> str:
        return f"<User {self.username} ({self.role})>"

    def to_dict(self) -> dict:
        """Retourne une représentation dictionnaire de l'utilisateur (sans le mot de passe)."""
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "adresse": self.adresse,
            "code_postal": self.code_postal,
            "ville": self.ville,
            "pays": self.pays,
        }

    @classmethod
    def find_by_id(cls, user_id: int) -> "User | None":
        """Retourne un utilisateur par son id ou None s'il n'existe pas."""
        return cast("User | None", cls.query.get(user_id))

    @classmethod
    def find_by_email(cls, email: str) -> "User | None":
        """Retourne un utilisateur par son email ou None s'il n'existe pas."""
        return cast("User | None", cls.query.filter_by(email=email).first())

    @classmethod
    def find_by_username(cls, username: str) -> "User | None":
        """Retourne un utilisateur par son username ou None s'il n'existe pas."""
        return cast("User | None", cls.query.filter_by(username=username).first())

    @classmethod
    def find_all(cls) -> list["User"]:
        """Retourne la liste de tous les utilisateurs."""
        return cast(list[User], cls.query.all())

    @classmethod
    def create(cls, username: str, firstname: str, lastname: str,
               password: str, email: str, phone: str | None = None,
               role: str = "client", adresse: str | None = None,
               code_postal: str | None = None, ville: str | None = None,
               pays: str | None = None) -> "User":
        """Crée un nouvel utilisateur et l'ajoute à la base de données."""
        user = cls(
            username=username,
            firstname=firstname,
            lastname=lastname,
            password=password,
            email=email,
            phone=phone,
            role=role,
            adresse=adresse,
            code_postal=code_postal,
            ville=ville,
            pays=pays
        )
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, **kwargs: Any) -> None:
        """Met à jour les champs de l'utilisateur avec les valeurs fournies."""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)
        db.session.commit()
