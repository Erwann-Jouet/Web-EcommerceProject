import re
from typing import Any

from flask import flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.wrappers import Response

from src.auth import auth_bp
from src.auth.utils import get_current_user, login_required
from src.cart import services as cart_services
from src.models.database import db
from src.models.user import User


def validate_required_fields(form: dict[str, str]) -> str | None:
    required_fields = [
        form.get("username"),
        form.get("email"),
        form.get("password"),
        form.get("password_confirm"),
        form.get("firstname"),
        form.get("lastname"),
    ]

    if not all(required_fields):
        return "Tous les champs sont obligatoires"

    return None


def validate_username(username: str) -> str | None:
    if not 3 <= len(username) <= 64:
        return "Le nom utilisateur doit contenir entre 3 et 64 caractères"

    if not re.fullmatch(r"[a-z0-9]+", username):
        return "Le nom utilisateur doit contenir uniquement des lettres " "minuscules et des chiffres"

    if User.find_by_username(username):
        return "Ce nom utilisateur existe déjà"

    return None


def validate_name(firstname: str, lastname: str) -> str | None:
    if not 2 <= len(firstname) <= 64:
        return "Le prénom doit contenir entre 2 et 64 caractères"

    if not 2 <= len(lastname) <= 64:
        return "Le nom doit contenir entre 2 et 64 caractères"

    return None


def validate_email(email: str) -> str | None:
    if len(email) > 120:
        return "L'email doit contenir moins de 120 caractères"

    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        return "L'email n'est pas valide"

    if User.find_by_email(email):
        return "Cet email existe déjà"

    return None


def validate_address(
    adresse: str,
    code_postal: str,
    ville: str,
    pays: str,
) -> str | None:
    if not adresse and not code_postal and not ville and not pays:
        return None

    if not 5 <= len(adresse) <= 128:
        return "L'adresse doit contenir entre 5 et 128 caractères"

    if not re.fullmatch(r"\d{5}", code_postal):
        return "Le code postal doit contenir exactement 5 chiffres"

    if not 2 <= len(ville) <= 64:
        return "La ville doit contenir entre 2 et 64 caractères"

    if not 2 <= len(pays) <= 64:
        return "Le pays doit contenir entre 2 et 64 caractères"

    return None


def validate_password(password: str, password_confirm: str) -> str | None:
    if len(password) < 6:
        return "Le mot de passe doit contenir au moins 6 caractères"

    if not re.fullmatch(
        r"(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}",
        password,
    ):
        return "Le mot de passe doit contenir au moins une majuscule, " "un chiffre et un caractère spécial"

    if password != password_confirm:
        return "Les mots de passe ne correspondent pas"

    return None


def validate_registration(form: dict[str, str]) -> str | None:
    validators = [
        lambda f: validate_required_fields(f),
        lambda f: validate_username(f.get("username", "")),
        lambda f: validate_name(f.get("firstname", ""), f.get("lastname", "")),
        lambda f: validate_email(f.get("email", "")),
        lambda f: validate_address(
            f.get("adresse", ""),
            f.get("code_postal", ""),
            f.get("ville", ""),
            f.get("pays", ""),
        ),
        lambda f: validate_password(
            f.get("password", ""),
            f.get("password_confirm", ""),
        ),
    ]

    for validator in validators:
        error = validator(form)
        if error:
            return error

    return None


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if request.method == "POST":
        username_input = request.form.get("login")
        password_input = request.form.get("password")

        if not username_input or not password_input:
            flash("Veuillez remplir tous les champs", "error")
            return render_template("auth/login.html")

        user = User.find_by_username(username_input)

        if user and check_password_hash(user.password, password_input):
            session["user_id"] = user.id
            session["username"] = user.username
            session["firstname"] = user.firstname

            cart_services.merge_session_to_db(user.id)

            flash("Connexion réussie", "success")
            return redirect(url_for("home"))

        flash("Identifiants invalides", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout() -> Response:
    session.clear()
    flash("Déconnexion réussie", "success")
    return redirect(url_for("home"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    if request.method == "POST":
        form = {key: request.form.get(key, "").strip() for key in request.form}
        error = validate_registration(form)

        if error:
            session["register_error"] = error
            return render_template("register.html")

        session.pop("register_error", None)

        new_user = User(
            username=form["username"],
            email=form["email"],
            firstname=form["firstname"],
            lastname=form["lastname"],
            password=generate_password_hash(form["password"]),
            adresse=form.get("adresse", ""),
            code_postal=form.get("code_postal", ""),
            ville=form.get("ville", ""),
            pays=form.get("pays", ""),
            phone=form.get("phone", ""),
            role="client",
        )

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["username"] = new_user.username
        session["firstname"] = new_user.firstname

        flash("Inscription réussie!", "success")
        return redirect(url_for("home"))

    return render_template("register.html")


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile() -> Any:
    user = get_current_user()
    if not user:
        return redirect(url_for("home"))

    if request.method == "POST":
        firstname = request.form.get("firstname", "").strip()
        lastname = request.form.get("lastname", "").strip()
        email = request.form.get("email", "").strip()
        adresse = request.form.get("adresse", "").strip()
        code_postal = request.form.get("code_postal", "").strip()
        ville = request.form.get("ville", "").strip()
        pays = request.form.get("pays", "").strip()

        error = validate_name(firstname, lastname)
        if not error:
            error = validate_email(email)
        if not error:
            error = validate_address(adresse, code_postal, ville, pays)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            if error:
                return jsonify({"success": False, "error": error})

            user.firstname = firstname
            user.lastname = lastname
            user.email = email
            user.adresse = adresse
            user.code_postal = code_postal
            user.ville = ville
            user.pays = pays
            db.session.commit()

            return jsonify({"success": True})

        if error:
            session["profile_error"] = error
            return render_template("profile.html", user=user)

        user.firstname = firstname
        user.lastname = lastname
        user.email = email
        user.adresse = adresse
        user.code_postal = code_postal
        user.ville = ville
        user.pays = pays
        db.session.commit()

        return redirect(url_for("auth.profile"))

    return render_template("profile.html", user=user)
