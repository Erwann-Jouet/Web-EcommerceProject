"""Modèle ProductImage pour les images des produits."""

from src.models.database import db


class ProductImage(db.Model):  # type: ignore
    """
    Représente une image d'un produit.
    Chaque produit peut avoir plusieurs images.
    """

    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    url = db.Column(db.String(256), nullable=False)
    order = db.Column(db.Integer, default=0)  # Pour l'ordre d'affichage

    def __repr__(self) -> str:
        return f"<ProductImage {self.url} (product_id={self.product_id})>"

    def to_dict(self) -> dict:
        """Retourne une représentation dictionnaire de l'image."""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "url": self.url,
            "order": self.order,
        }
