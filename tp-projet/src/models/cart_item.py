"""Modèle CartItem pour les lignes du panier."""

from typing import cast

from src.models.database import db


class CartItem(db.Model):  # type: ignore
    """
    Représente une ligne du panier (un produit avec sa quantité).
    Le prix unitaire est stocké pour conserver l'historique des prix au moment de l'achat.
    """

    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)

    # Relation vers Product
    product = db.relationship("Product")

    def __repr__(self) -> str:
        return f"<CartItem {self.product_id} x{self.quantity}>"

    @property
    def subtotal(self) -> float:
        """Calcule le sous-total de la ligne (prix x quantité)."""
        return cast(float, self.unit_price * self.quantity)

    def to_dict(self) -> dict:
        """Retourne une représentation dictionnaire de l'article."""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "product_slug": self.product.slug if self.product else None,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "subtotal": self.subtotal,
        }
