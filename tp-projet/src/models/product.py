"""Modèle Product pour les produits du site LeVélo."""

from typing import Any, cast

from sqlalchemy import or_

from src.models.database import db


class Product(db.Model):  # type: ignore
    """
    Modèle SQLAlchemy représentant un produit du site LeVélo.
    """

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(64), nullable=False, unique=True)
    brand = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(255))
    # Relations avec les catégories
    # category_id stocke l'ID de la catégorie principale (obligatoire)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    # subcategory_id stocke l'ID de la sous-catégorie (optionnel)
    subcategory_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)

    # category permet d'accéder directement à l'objet Category via product.category
    # foreign_keys indique quelle colonne utiliser (car on a 2 relations vers Category)
    # backref='products' permet d'accéder aux produits depuis une catégorie via category.products
    category = db.relationship("Category", foreign_keys=[category_id], backref="products")
    # subcategory permet d'accéder à l'objet sous-catégorie via product.subcategory
    # backref='sub_products' permet d'accéder aux produits depuis une sous-catégorie via category.sub_products
    subcategory = db.relationship("Category", foreign_keys=[subcategory_id], backref="sub_products")

    # Relation avec les images du produit
    # images permet d'accéder à la liste des images via product.images
    # cascade='all, delete-orphan' supprime les images si le produit est supprimé
    # order_by trie les images par ordre croissant
    images = db.relationship(
        "ProductImage",
        backref="product",
        lazy="dynamic",
        cascade="all, delete-orphan",
        order_by="ProductImage.order",
    )

    def get_images_url(self) -> list[str]:
        """Retourne la liste des URLs des images du produit."""
        return [img.url for img in self.images.all()]

    def get_first_image_url(self) -> str | None:
        """Retourne l'URL de la première image ou None si aucune image."""
        first = self.images.first()
        return first.url if first else None

    # Ajoute une propriété dynamiques pour accéder à l'URL de la première image
    @property
    def image_url(self) -> str | None:
        """Retourne l'image, qu'elle vienne de la nouvelle colonne ou de l'ancienne table."""
        if self.image:                                    
            return str(self.image)
        return self.get_first_image_url()

    # Ajoute une propriété dynamiques pour accéder à la liste des URLs des images
    @property
    def images_url(self) -> list[str]:
        """Propriété qui retourne la liste des URLs des images (pour compatibilité)."""
        return self.get_images_url()

    def __repr__(self) -> str:
        """
        Retourne une représentation lisible de l'objet Product pour le debug.
        """
        cat = self.category.name if self.category else None
        subcat = self.subcategory.name if self.subcategory else None
        return f"<Product {self.name} ({cat}/{subcat})>"

    def to_dict(self) -> dict:
        """
        Retourne un dictionnaire représentant le produit, utile pour la sérialisation JSON.
        """
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "brand": self.brand,
            "description": self.description,
            "price": self.price,
            "category": self.category.name if self.category else None,
            "subcategory": self.subcategory.name if self.subcategory else None,
            "images": self.get_images_url(),
            "stock_quantity": self.stock_quantity,
        }

    @classmethod
    def find_by_id(cls, product_id: int) -> "Product | None":
        """Retourne un produit par son ID ou None s'il n'existe pas."""
        return cast("Product | None", cls.query.get(product_id))

    @classmethod
    def find_by_name(cls, name: str) -> "Product | None":
        """Retourne un produit par son nom ou None s'il n'existe pas."""
        return cast("Product | None", cls.query.filter_by(name=name).first())

    @classmethod
    def find_by_slug(cls, slug: str) -> "Product | None":
        """Retourne un produit par son slug ou None s'il n'existe pas."""
        return cast("Product | None", cls.query.filter_by(slug=slug).first())

    @classmethod
    def find_by_any_category_id(cls, category_id: int) -> list["Product"]:
        """Retourne les produits appartenant à cette catégorie (principale ou sous-catégorie)."""
        return cast(list[Product], cls.query.filter(
            or_(
                cls.category_id == category_id,
                cls.subcategory_id == category_id
            )
        ).all())
    
    @classmethod
    def find_all(cls) -> list["Product"]:
        """Retourne la liste de tous les produits."""
        return cast(list[Product], cls.query.all())

    @classmethod
    def find_by_category_id(cls, category_id: int) -> list["Product"]:
        """Retourne la liste des produits d'une catégorie donnée."""
        return cast(list[Product], cls.query.filter_by(category_id=category_id).all())

    @classmethod
    def find_by_filters(
        cls,
        category_id: int | None = None,
        subcategory_id: int | None = None,
        brand: str | None = None,
    ) -> list["Product"]:
        """
        Retourne la liste des produits filtrés par catégorie, sous-catégorie et marque.
        Tous les paramètres sont optionnels. Si aucun filtre n'est fourni, retourne tous les produits.
        """
        query = cls.query
        if category_id is not None:
            query = query.filter_by(category_id=category_id)
        if subcategory_id is not None:
            query = query.filter_by(subcategory_id=subcategory_id)
        if brand is not None:
            query = query.filter_by(brand=brand)
        return cast(list[Product], query.all())

    @classmethod
    def find_brands_by_category(cls, category_id: int) -> list[str]:
        """
        Retourne la liste des marques pour une catégorie donnée.
        """
        return [
            row[0]
            for row in (
                cls.query.with_entities(cls.brand).filter_by(category_id=category_id).distinct().all()
            )
        ]

    @classmethod
    def find_brands_by_subcategory(cls, subcategory_id: int) -> list[str]:
        """
        Retourne la liste des marques pour une sous-catégorie donnée.
        """
        return [
            row[0]
            for row in (
                cls.query.with_entities(cls.brand).filter_by(subcategory_id=subcategory_id).distinct().all()
            )
        ]

    def update(self, **kwargs: Any) -> None:
        """
        Met à jour les attributs du produit et sauvegarde en base de données.

        Args:
            **kwargs: Les attributs à mettre à jour (name, price, stock_quantity, etc.)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()