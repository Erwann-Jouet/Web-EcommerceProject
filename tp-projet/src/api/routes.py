from typing import Any

from flask import jsonify, request, session

from src.api import api_bp
from src.cart import services as cart_services
from src.models.product import Product
from src.models.user import User


@api_bp.route("/user/check", methods=["GET"])
def check_user() -> Any:
    try:
        username = request.args.get("username", "").strip()
        email = request.args.get("email", "").strip()

        if not username and not email:
            return jsonify({"error": "Veuillez fournir un username ou un email"}), 400

        if username:
            user = User.find_by_username(username)
            return jsonify({"field": "username", "exists": user is not None, "value": username})

        if email:
            user = User.find_by_email(email)
            return jsonify({"field": "email", "exists": user is not None, "value": email})

        return jsonify({"error": "Paramètre invalide"}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@api_bp.route("/cart/add/<int:product_id>", methods=["POST", "GET"])
def add_to_cart(product_id: int) -> Any:
    try:
        user_id = session.get("user_id")

        if request.is_json and request.json:
            quantity_str = request.json.get("quantity", "1")
        else:
            quantity_str = request.form.get("quantity") or request.args.get("quantity", "1")

        try:
            quantity = int(quantity_str)
        except (TypeError, ValueError):
            return (
                jsonify(
                    {
                        "error": "La quantité doit être un nombre entier",
                        "message": "Quantité invalide",
                    }
                ),
                400,
            )

        if quantity <= 0:
            return (
                jsonify(
                    {
                        "error": "La quantité doit être au moins 1",
                        "message": "Quantité invalide",
                    }
                ),
                400,
            )

        product = Product.query.get(product_id)
        if product is None:
            return (
                jsonify(
                    {
                        "error": "Produit non trouvé",
                        "message": "Ce produit n'existe pas",
                    }
                ),
                404,
            )

        cart = session.get("cart", {})
        current_qty = int(cart.get(str(product_id), 0))

        if current_qty + quantity > product.stock_quantity:
            return (
                jsonify(
                    {
                        "error": "Stock insuffisant",
                        "message": (f"Stock insuffisant. Disponible: " f"{product.stock_quantity}"),
                        "available": product.stock_quantity,
                    }
                ),
                400,
            )

        cart_services.add_or_update_item(product_id, quantity, user_id)

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Produit ajouté au panier",
                    "cart_count": cart_services.get_count(user_id),
                    "cart_total": round(cart_services.get_total(user_id), 2),
                }
            ),
            200,
        )
    except Exception as exc:
        return jsonify({"error": str(exc), "message": "Erreur serveur"}), 500


@api_bp.route("/cart/remove/<int:product_id>", methods=["POST", "DELETE"])
def remove_from_cart(product_id: int) -> Any:
    try:
        user_id = session.get("user_id")
        cart = session.get("cart", {})

        if str(product_id) not in cart:
            return (
                jsonify(
                    {
                        "error": "Produit non trouvé dans le panier",
                        "message": "Ce produit n'est pas dans votre panier",
                    }
                ),
                404,
            )

        cart_services.remove_item(product_id, user_id)

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Produit supprimé du panier",
                    "cart_count": cart_services.get_count(user_id),
                    "cart_total": round(cart_services.get_total(user_id), 2),
                }
            ),
            200,
        )
    except Exception as exc:
        return jsonify({"error": str(exc), "message": "Erreur serveur"}), 500


@api_bp.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart_quantity(product_id: int) -> Any:
    try:
        user_id = session.get("user_id")

        if request.is_json and request.json:
            quantity_str = request.json.get("quantity", "1")
        else:
            quantity_str = request.form.get("quantity") or request.args.get("quantity", "1")

        try:
            quantity = int(quantity_str)
        except (TypeError, ValueError):
            return (
                jsonify(
                    {
                        "error": "La quantité doit être un nombre entier",
                        "message": "Quantité invalide",
                    }
                ),
                400,
            )

        if quantity <= 0:
            return (
                jsonify(
                    {
                        "error": "La quantité doit être au moins 1",
                        "message": "Quantité invalide",
                    }
                ),
                400,
            )

        product = Product.query.get(product_id)
        if product is None:
            return (
                jsonify(
                    {
                        "error": "Produit non trouvé",
                        "message": "Ce produit n'existe pas",
                    }
                ),
                404,
            )

        if quantity > product.stock_quantity:
            return (
                jsonify(
                    {
                        "error": "Stock insuffisant",
                        "message": (f"Stock insuffisant. Disponible: " f"{product.stock_quantity}"),
                    }
                ),
                400,
            )

        cart_services.update_item_quantity(product_id, quantity, user_id)

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Quantité mise à jour",
                    "cart_count": cart_services.get_count(user_id),
                    "cart_total": round(cart_services.get_total(user_id), 2),
                }
            ),
            200,
        )
    except Exception as exc:
        return jsonify({"error": str(exc), "message": "Erreur serveur"}), 500


@api_bp.route("/cart/summary", methods=["GET"])
def cart_summary() -> Any:
    try:
        user_id = session.get("user_id")

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Résumé du panier",
                    "cart_count": cart_services.get_count(user_id),
                    "cart_total": round(cart_services.get_total(user_id), 2),
                    "items": cart_services.get_items(user_id),
                }
            ),
            200,
        )
    except Exception as exc:
        return jsonify({"error": str(exc), "message": "Erreur serveur"}), 500
