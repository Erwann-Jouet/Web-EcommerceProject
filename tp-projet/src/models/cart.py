"""Modèle Cart pour la gestion du panier et des commandes."""

from datetime import datetime
from typing import TYPE_CHECKING, cast

from src.models.database import db

if TYPE_CHECKING:
    from src.models.cart_item import CartItem
    from src.models.product import Product



class Cart(db.Model):  # type: ignore
    """
    Représente un panier utilisateur.
    Le statut permet de gérer le cycle de vie : panier → commande → livraison.

    Contrainte métier : un utilisateur ne peut avoir qu'un seul panier actif
    (status='cart') à la fois. Cette contrainte est garantie par un index unique partiel.
    """


    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="cart")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ordered_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.Index(
            "ix_unique_active_cart_per_user",
            "user_id",
            unique=True,
            sqlite_where=db.text("status = 'cart'"),
            postgresql_where=db.text("status = 'cart'"),
        ),
    )

    user = db.relationship("User", backref="carts")
    items = db.relationship("CartItem", backref="cart", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Cart {self.id} (user={self.user_id}, status={self.status})>"

    @property
    def total(self) -> float:

        """Calcule le montant total du panier."""
        return cast(float, sum(item.subtotal for item in self.items.all()))

    @property
    def item_count(self) -> int:
        """Retourne le nombre total d'articles."""
        return sum(item.quantity for item in self.items.all())

    def get_items(self) -> list["CartItem"]:
        """Retourne la liste des articles du panier."""
        return list(self.items.all())

    def to_dict(self) -> dict:
        all_items = cast(list["CartItem"], self.items.all())
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "ordered_at": self.ordered_at.isoformat() if self.ordered_at else None,

            "items": [item.to_dict() for item in self.items.all()],
            "total": self.total,
        }

    def add_product(self, product: "Product", quantity: int = 1) -> "CartItem":

        """
        Ajoute un produit au panier.
        Si le produit est déjà présent, définit la quantité (ne l'incrémente pas).
        """
        from src.models.cart_item import CartItem  # noqa: PLC0415


        item = CartItem.query.filter_by(cart_id=self.id, product_id=product.id).first()

        if item:
            item.quantity = quantity
        else:
            item = CartItem(
                cart_id=self.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
            )
            db.session.add(item)

        db.session.commit()
        return cast("CartItem", item)

    def remove_product(self, product_id: int) -> bool:
        """Supprime un produit du panier. Retourne True si supprimé."""
        from src.models.cart_item import CartItem  # noqa: PLC0415


        item = CartItem.query.filter_by(cart_id=self.id, product_id=product_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False

    def update_quantity(self, product_id: int, quantity: int) -> bool:

        """Met à jour la quantité d'un produit. Retourne True si mis à jour."""
        from src.models.cart_item import CartItem  # noqa: PLC0415


        item = CartItem.query.filter_by(cart_id=self.id, product_id=product_id).first()
        if item:
            if quantity <= 0:
                db.session.delete(item)
            else:
                item.quantity = quantity
            db.session.commit()
            return True
        return False

    def clear(self) -> None:

        """Vide le panier de tous ses articles."""
        for item in self.items.all():
            db.session.delete(item)
            db.session.commit()

    def place_order(self) -> None:
        self.status = "ordered"
        self.ordered_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def find_by_id(cls, cart_id: int) -> "Cart | None":
        return cast("Cart | None", cls.query.get(cart_id))

    @classmethod
    def find_active_cart(cls, user_id: int) -> "Cart | None":
        return cast("Cart | None", cls.query.filter_by(user_id=user_id, status="cart").first())

    @classmethod
    def get_or_create_cart(cls, user_id: int) -> "Cart":
        cart = cls.find_active_cart(user_id)
        if cart is None:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
        return cart

    @classmethod
    def find_orders_by_user(cls, user_id: int) -> list["Cart"]:
        return cast(
            list["Cart"],
            cls.query.filter(cls.user_id == user_id, cls.status != "cart")
            .order_by(cls.ordered_at.desc())
            .all(),
        )

    @classmethod
    def find_all_orders(cls) -> list["Cart"]:
        return cast(
            list[Cart],
            cls.query.filter(cls.status != "cart").order_by(cls.ordered_at.desc()).all(),

        )
