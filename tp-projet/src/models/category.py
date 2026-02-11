
"""Modèle Category pour les catégories et sous-catégories du site LeVélo."""

from typing import cast

from src.models.database import db


class Category(db.Model):  # type: ignore
    """
    Modèle SQLAlchemy représentant une catégorie (ou sous-catégorie) de produit.
    """
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    slug = db.Column(db.String(64), nullable=False, unique=True)

    # Relation parent-enfant : une catégorie peut avoir une catégorie parente
    # parent_id stocke l'ID de la catégorie parente (None si c'est une catégorie principale)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    # parent permet d'accéder directement à l'objet Category parent via category.parent
    # children (via backref) permet d'accéder aux sous-catégories via category.children
    # remote_side=[id] indique que le côté "distant" de la relation est l'id
    parent = db.relationship('Category', remote_side=[id], backref='children')

    def __repr__(self) -> str:
        return (
            f"<Category {self.name}"
            f"{' (sous-catégorie de ' + self.parent.name + ')' if self.parent else ''}>"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "parent_id": self.parent_id,
            "parent_name": self.parent.name if self.parent else None,
        }

    @classmethod
    def find_by_name(cls, name: str) -> "Category | None":
        """
        Retourne une catégorie par son nom.
        """
        return cast("Category | None", cls.query.filter_by(name=name).first())

    @classmethod
    def find_by_slug(cls, slug: str) -> "Category | None":
        """
        Retourne une catégorie par son slug.
        """
        return cast("Category | None", cls.query.filter_by(slug=slug).first())

    @classmethod
    def find_by_id(cls, id: int) -> "Category | None":
        """
        Retourne une catégorie par son ID.
        """
        return cast("Category | None", cls.query.get(id))

    @classmethod
    def find_all_parents(cls) -> list["Category"]:
        """
        Retourne toutes les catégories mères (parent_id=None).
        """
        return cast(list[Category], cls.query.filter_by(parent_id=None).all())

    @classmethod
    def find_subcategories_by_parent_id(cls, parent_id: int) -> list["Category"]:
        """
        Retourne toutes les sous-catégories d'une catégorie par son id.
        """
        return cast(list[Category], cls.query.filter_by(parent_id=parent_id).all())
    
    @classmethod
    def find_main_categories(cls) -> list["Category"]:
        """Retourne uniquement les catégories principales (sans parent)."""
        return cast(list[Category], cls.query.filter_by(parent_id=None).all())
    
    @classmethod
    def find_subcategories_by_parent_slug(cls, parent_slug: str) -> list["Category"]:
        """
        Retourne toutes les sous-catégories d'une catégorie par son slug.
        Si le parent n'existe pas, retourne une liste vide.
        """
        parent = cls.find_by_slug(parent_slug)
        if parent is None:
            return []
        return cls.find_subcategories_by_parent_id(parent.id)
