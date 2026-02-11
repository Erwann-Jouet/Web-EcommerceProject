"""
Script pour importer les catégories et sous-catégories en base de données
à partir du fichier categories.json.
"""

import json

from src.models.category import Category
from src.models.database import db

CATEGORIES_JSON = "datafixtures/json/categories.json"


def import_categories() -> None:
    with open(CATEGORIES_JSON, encoding="utf-8") as f:
        data = json.load(f)

    for cat in data:
        # Crée la catégorie principale
        parent = Category.find_by_slug(cat["slug"])
        if not parent:
            parent = Category(name=cat["name"], slug=cat["slug"])
            db.session.add(parent)
            db.session.flush()  # Force l'attribution de l'ID
        # Crée les sous-catégories
        for sub in cat["subcategories"]:
            subcat = Category.find_by_slug(sub["slug"])
            if not subcat:
                subcat = Category(name=sub["name"], slug=sub["slug"], parent_id=parent.id)
                db.session.add(subcat)
    db.session.commit()
    print(f"{len(data)} catégories ajoutées.")
