from flask import Blueprint, abort, render_template

from src.models.category import Category
from src.models.product import Product

catalog_bp = Blueprint('catalog', __name__, template_folder='templates')


@catalog_bp.route('/')
def products() -> str:
    products_data = Product.find_all()
    categories = Category.find_main_categories()
    return render_template('products.html', products=products_data, categories=categories)


@catalog_bp.route('/<int:product_id>')
def product_detail(product_id: int) -> str:
    product = Product.find_by_id(product_id)
    if not product:
        abort(404)
    return render_template('product_detail.html', product=product)


@catalog_bp.route('/category/<slug>')
def category_products(slug: str) -> str:
    current = Category.query.filter_by(slug=slug).first()
    if not current:
        abort(404)
    products_data = Product.find_by_any_category_id(current.id)

    categories = Category.find_main_categories()

    return render_template(
        'products.html',
        products=products_data,
        categories=categories,
        current_category=current
    )
