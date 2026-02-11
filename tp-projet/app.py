import os
from flask import Flask, render_template, session
from config import config
from src.auth import auth_bp
from src.cart.routes import cart_bp
from src.catalog.routes import catalog_bp
from src.models.database import db
from src.api import api_bp
from src.cart import services as cart_services

def create_app() -> Flask:
    config_name: str = os.environ.get("FLASK_CONFIG", "development")
    app: Flask = Flask(__name__, template_folder="src/templates")

    app.config.from_object(config[config_name])
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    db.init_app(app)

    app.register_blueprint(catalog_bp, url_prefix="/products")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.context_processor
    def inject_cart_count():
        user_id = session.get('user_id')
        count = cart_services.get_count(user_id)
        return dict(cart_count=count)

    @app.route("/")
    def home() -> str:
        user_id = session.get('user_id')
        count = cart_services.get_count(user_id)
        return render_template("index.html", cart_count=count)

    return app

app = create_app()

with app.app_context():
    db.create_all()
    from src.models.product import Product
    if not Product.query.first():
        try:
            chargeur_path = os.path.join(os.path.dirname(__file__), "chargeur.py")
            if os.path.exists(chargeur_path):
                with open(chargeur_path, encoding="utf-8") as f:
                    exec(f.read())
        except Exception:
            pass
