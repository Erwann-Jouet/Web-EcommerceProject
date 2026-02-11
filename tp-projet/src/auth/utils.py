from functools import wraps
from typing import Any, Callable, cast

from flask import redirect, session, url_for

from src.models.user import User


def get_current_user() -> User | None:
    """Retourne l'utilisateur connecté ou None"""
    user_id = session.get("user_id")
    if user_id:
        return cast(User | None, User.query.get(user_id))
    return None


def login_required(f: Callable[..., Any]) -> Callable[..., Any]:
    """Décorateur pour protéger les routes - redirige vers home si non connecté"""

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if "user_id" not in session:
            session["login_error"] = "Veuillez vous connecter"
            return redirect(url_for("home"))
        return f(*args, **kwargs)

    return decorated_function
