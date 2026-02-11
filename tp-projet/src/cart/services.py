from flask import session

from src.models.cart import Cart
from src.models.cart_item import CartItem
from src.models.database import db
from src.models.product import Product


def add_or_update_item(product_id: int, quantity: int = 1, user_id: int | None = None) -> None:
    cart = session.get("cart", {})
    product_id_str = str(product_id)

    current_qty = int(cart.get(product_id_str, 0))
    cart[product_id_str] = current_qty + quantity

    session["cart"] = cart
    session.modified = True


def update_item_quantity(product_id: int, quantity: int, user_id: int | None = None) -> None:
    """Met à jour la quantité d'un produit (ne cumule pas, remplace)."""
    cart = session.get("cart", {})
    product_id_str = str(product_id)

    if quantity > 0:
        cart[product_id_str] = quantity
    else:
        cart.pop(product_id_str, None)

    session["cart"] = cart
    session.modified = True


def get_items(user_id: int | None = None) -> list[dict]:
    """Récupère la liste complète des produits du panier avec leurs infos."""
    items = []
    cart = session.get("cart", {})

    if cart:

        product_ids = [int(k) for k in cart.keys()]
        products = Product.query.filter(Product.id.in_(product_ids)).all()

        for product in products:
            qty = int(cart.get(str(product.id), 0))
            items.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "product_image": product.image,
                    "quantity": qty,
                    "unit_price": product.price,
                    "subtotal": round(product.price * qty, 2),
                    "stock_quantity": product.stock_quantity,
                }
            )

    return items


def get_count(user_id: int | None = None) -> int:
    """Compte le nombre total d'articles."""
    cart = session.get("cart", {})
    if not cart:
        return 0
    return sum(int(qty) for qty in cart.values())


def get_total(user_id: int | None = None) -> float:
    """Calcule le prix total du panier."""
    items = get_items(user_id)
    return float(sum(item["subtotal"] for item in items))


def remove_item(product_id: int, user_id: int | None = None) -> None:
    """Supprime un article du panier."""
    product_id_str = str(product_id)
    cart = session.get("cart", {})

    if product_id_str in cart:
        del cart[product_id_str]
        session["cart"] = cart
        session.modified = True


def clear(user_id: int | None = None) -> None:
    """Vide le panier."""
    session.pop("cart", None)


def merge_session_to_db(user_id: int) -> None:
    """
    Migre le panier de la session vers la base de données.
    Appelée lors de la connexion d'un utilisateur.
    """
    try:
        # Récupérer le panier en session
        session_cart = session.get("cart", {})

        if not session_cart:
            return

        # Créer ou récupérer le panier de l'utilisateur
        user_cart = Cart.query.filter_by(user_id=user_id).first()
        if not user_cart:
            user_cart = Cart(user_id=user_id)
            db.session.add(user_cart)
            db.session.commit()

        # Ajouter les articles du panier en session à la base de données
        for product_id_str, quantity in session_cart.items():
            product_id = int(product_id_str)

            # Vérifier si l'article existe déjà dans le panier
            cart_item = CartItem.query.filter_by(cart_id=user_cart.id, product_id=product_id).first()

            if cart_item:
                # Mettre à jour la quantité
                cart_item.quantity = quantity
            else:
                # Créer un nouvel article
                cart_item = CartItem(cart_id=user_cart.id, product_id=product_id, quantity=quantity)
                db.session.add(cart_item)

        db.session.commit()

        # Vider la session du panier
        session.pop("cart", None)

    except Exception as e:
        print(f"Erreur lors de la migration du panier: {e}")
        db.session.rollback()
