"""
Script principal pour importer catégories, utilisateurs et produits en une seule commande.
"""
from app import app
from datafixtures.import_categories import import_categories
from datafixtures.import_products import load_products
from datafixtures.import_users import load_users
from src.models.database import db

if __name__ == "__main__":
    with app.app_context():
        print("Suppression et création des tables...")
        db.drop_all()
        db.create_all()
        print("Import des catégories...")
        import_categories()
        print("Import des utilisateurs...")
        load_users()
        print("Import des produits...")
        load_products()
    print("Import global terminé.")
