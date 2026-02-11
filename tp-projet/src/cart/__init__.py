# src/cart/__init__.py

from flask import Blueprint

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


from . import routes  # noqa: E402
