import json
from src.models.category import Category
from src.models.database import db
from src.models.product import Product
from src.models.product_image import ProductImage

PRODUCTS_JSON = "datafixtures/json/products.json"


def load_products() -> None:
    """
    Charge les produits depuis un fichier JSON et les ajoute à la base de données SQLite.
    """
    with open(PRODUCTS_JSON, encoding="utf-8") as f:
        products = json.load(f)
    for data in products:
        if not Product.find_by_slug(slug=data["slug"]):
            # Chercher la catégorie principale
            cat = Category.find_by_name(data["category"])
            # Chercher la sous-catégorie avec le bon parent
            subcat = None
            if cat:
                subcat = Category.query.filter_by(name=data["subcategory"], parent_id=cat.id).first()
            # Créer le produit avec ID
            product = Product(
                name=data["name"],
                slug=data["slug"],
                brand=data["brand"],
                description=data["description"],
                price=data["price"],
                category_id=cat.id if cat else None,
                subcategory_id=subcat.id if subcat else None,
                stock_quantity=data["stock_quantity"],
            )
            db.session.add(product)
            db.session.flush()  # Force l'attribution de l'ID au produit

            # Ajouter les images du produit
            for index, image_url in enumerate(data.get("images", [])):
                product_image = ProductImage(
                    product_id=product.id,
                    url=image_url,
                    order=index,
                )
                db.session.add(product_image)
    db.session.commit()
    print(f"{len(products)} produits ajoutés.")
