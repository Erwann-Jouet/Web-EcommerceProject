from flask import Blueprint, render_template, session

from src.cart import services as cart_services

cart_bp = Blueprint("cart", __name__, template_folder="templates")


@cart_bp.route("/")
def view_cart() -> str:
    user_id = session.get("user_id")
    cart_items = cart_services.get_items(user_id)
    cart_count = cart_services.get_count(user_id)
    total_global = cart_services.get_total(user_id)

    return render_template(
        "cart/index.html", cart_items=cart_items, cart_count=cart_count, total_global=round(total_global, 2)
    )
