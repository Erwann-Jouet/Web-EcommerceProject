from src.models.database import db
from src.models.category import Category
from src.models.product import Product
from datafixtures.import_users import load_users

print("🚀 Démarrage du chargement correct...")

# 1. Nettoyage
try:
    db.session.query(Product).delete()
    db.session.query(Category).delete()
    db.session.commit()
    print("🧹 Base de données nettoyée.")
except Exception:
    db.session.rollback()

# 2. Données Catégories
cats_structure = [
    {
        "name": "Vendée",
        "slug": "vendee",
        "subcategories": [
            {"name": "Douceurs Vendéennes", "slug": "douceurs-vendee"},
            {"name": "Apéro & Entrées", "slug": "apero-vendee"},
            {"name": "Terre & Mer", "slug": "terre-mer-vendee"},
            {"name": "Cave Vendéenne", "slug": "cave-vendee"},
        ],
    },
    {
        "name": "Bretagne",
        "slug": "bretagne",
        "subcategories": [
            {"name": "Douceurs Bretonnes", "slug": "douceurs-bretagne"},
            {"name": "Apéro & Terroir", "slug": "apero-bretagne"},
            {"name": "Gastronomie Bretonne", "slug": "gastronomie-bretagne"},
            {"name": "Cidrerie & Cave", "slug": "cidrerie-bretagne"},
        ],
    },
    {
        "name": "Idées Cadeaux",
        "slug": "idees-cadeaux",
        "subcategories": [
            {"name": "Coffrets Gourmands", "slug": "coffrets-gourmands"},
            {"name": "Accessoires", "slug": "accessoires"},
        ],
    },
]

# 3. Données Produits (AVEC NOMS DE FICHIERS LOCAUX)
products_list = [
    {
        "name": "Fion Vendéen",
        "slug": "fion-vendeen",
        "price": 14.50,
        "cat": "Vendée",
        "sub": "Douceurs Vendéennes",
        "img": "fion-vendeen.jpg",
    },
    {
        "name": "Brioche Vendéenne",
        "slug": "brioche-vendeenne",
        "price": 7.90,
        "cat": "Vendée",
        "sub": "Douceurs Vendéennes",
        "img": "brioche-vendeenne.jpg",
    },
    {
        "name": "Gâche Vendéenne",
        "slug": "gache-vendeenne",
        "price": 6.50,
        "cat": "Vendée",
        "sub": "Douceurs Vendéennes",
        "img": "gache-vendeenne.jpg",
    },
    {
        "name": "Foutimassons",
        "slug": "foutimassons",
        "price": 4.20,
        "cat": "Vendée",
        "sub": "Douceurs Vendéennes",
        "img": "foutimassons.jpg",
    },
    {
        "name": "Huîtres de Noirmoutier",
        "slug": "huitres-noirmoutier",
        "price": 19.90,
        "cat": "Vendée",
        "sub": "Apéro & Entrées",
        "img": "huitres-noirmoutier.jpg",
    },
    {
        "name": "Rillettes de Poissons",
        "slug": "rillettes-poissons",
        "price": 5.80,
        "cat": "Vendée",
        "sub": "Apéro & Entrées",
        "img": "rillettes-poissons.jpg",
    },
    {
        "name": "Préfou à l'Ail",
        "slug": "prefou-vendee",
        "price": 4.95,
        "cat": "Vendée",
        "sub": "Apéro & Entrées",
        "img": "prefou-vendee.jpg",
    },
    {
        "name": "Fleur de Sel",
        "slug": "fleur-de-sel",
        "price": 8.50,
        "cat": "Vendée",
        "sub": "Apéro & Entrées",
        "img": "fleur-de-sel.jpg",
    },
    {
        "name": "Mizotte",
        "slug": "mizotte",
        "price": 11.00,
        "cat": "Vendée",
        "sub": "Terre & Mer",
        "img": "mizotte.jpg",
    },
    {
        "name": "Mogettes de Vendée",
        "slug": "mogettes",
        "price": 3.90,
        "cat": "Vendée",
        "sub": "Terre & Mer",
        "img": "mogettes.jpg",
    },
    {
        "name": "Bonnotte de Noirmoutier",
        "slug": "pomme-de-terre-noirmoutier",
        "price": 7.50,
        "cat": "Vendée",
        "sub": "Terre & Mer",
        "img": "pomme-de-terre-noirmoutier.jpg",
    },
    {
        "name": "Soupe de Poissons",
        "slug": "soupe-poissons",
        "price": 9.20,
        "cat": "Vendée",
        "sub": "Terre & Mer",
        "img": "soupe-poissons.jpg",
    },
    {
        "name": "Bar de Ligne",
        "slug": "bar-de-ligne",
        "price": 28.00,
        "cat": "Vendée",
        "sub": "Terre & Mer",
        "img": "bar-de-ligne.jpg",
    },
    {
        "name": "Sole Sablaise",
        "slug": "sole-noirmoutier",
        "price": 32.00,
        "cat": "Vendée",
        "sub": "Terre & Mer",
        "img": "sole-noirmoutier.jpg",
    },
    {
        "name": "Poulet Noir de Challans",
        "slug": "poulet-challans",
        "price": 18.50,
        "cat": "Vendée",
        "sub": "Terre & Mer",
        "img": "poulet-challans.jpg",
    },
    {
        "name": "Troussepinette",
        "slug": "trouspinette",
        "price": 15.90,
        "cat": "Vendée",
        "sub": "Cave Vendéenne",
        "img": "trouspinette.jpg",
    },
    {
        "name": "Kiki Vendéen",
        "slug": "kiki-vendeen",
        "price": 13.50,
        "cat": "Vendée",
        "sub": "Cave Vendéenne",
        "img": "kiki-vendeen.jpg",
    },
    {
        "name": "Kamok",
        "slug": "kamok",
        "price": 24.00,
        "cat": "Vendée",
        "sub": "Cave Vendéenne",
        "img": "kamok.jpg",
    },
    {
        "name": "Cidre Fermier Breton",
        "slug": "cidre-breton",
        "price": 4.80,
        "cat": "Bretagne",
        "sub": "Cidrerie & Cave",
        "img": "cidre-breton.jpg",
    },
    {
        "name": "Chouchen Melmor",
        "slug": "chouchen",
        "price": 12.50,
        "cat": "Bretagne",
        "sub": "Cidrerie & Cave",
        "img": "chouchen.jpg",
    },
    {
        "name": "Kir Breton",
        "slug": "kir-breton",
        "price": 8.90,
        "cat": "Bretagne",
        "sub": "Cidrerie & Cave",
        "img": "kir-breton.jpg",
    },
    {
        "name": "Kouign-Amann",
        "slug": "kouign-amann",
        "price": 16.00,
        "cat": "Bretagne",
        "sub": "Douceurs Bretonnes",
        "img": "kouign-amann.jpg",
    },
    {
        "name": "Far Breton",
        "slug": "far-breton",
        "price": 9.50,
        "cat": "Bretagne",
        "sub": "Douceurs Bretonnes",
        "img": "far-breton.jpg",
    },
    {
        "name": "Caramel Beurre Salé",
        "slug": "caramel-beurre-sale",
        "price": 6.80,
        "cat": "Bretagne",
        "sub": "Douceurs Bretonnes",
        "img": "caramel-beurre-sale.jpg",
    },
    {
        "name": "Palets Bretons",
        "slug": "sable-breton",
        "price": 5.50,
        "cat": "Bretagne",
        "sub": "Douceurs Bretonnes",
        "img": "sable-breton.jpg",
    },
    {
        "name": "Galettes Sarrasin",
        "slug": "galette-ble-noir",
        "price": 3.80,
        "cat": "Bretagne",
        "sub": "Gastronomie Bretonne",
        "img": "galette-ble-noir.jpg",
    },
    {
        "name": "Cotriade",
        "slug": "cotriade",
        "price": 13.50,
        "cat": "Bretagne",
        "sub": "Gastronomie Bretonne",
        "img": "cotriade.jpg",
    },
    {
        "name": "Galette Saucisse",
        "slug": "galette-saucisse",
        "price": 4.50,
        "cat": "Bretagne",
        "sub": "Gastronomie Bretonne",
        "img": "galette-saucisse.jpg",
    },
    {
        "name": "Kig Ha Farz",
        "slug": "kig-ha-farz",
        "price": 15.00,
        "cat": "Bretagne",
        "sub": "Gastronomie Bretonne",
        "img": "kig-ha-farz.jpg",
    },
    {
        "name": "Ragoût Bigouden",
        "slug": "ragout-bigouden",
        "price": 12.00,
        "cat": "Bretagne",
        "sub": "Gastronomie Bretonne",
        "img": "ragout-bigouden.jpg",
    },
    {
        "name": "Poulet Janzé",
        "slug": "poulet-janze",
        "price": 14.50,
        "cat": "Bretagne",
        "sub": "Gastronomie Bretonne",
        "img": "poulet-janze.jpg",
    },
    {
        "name": "Andouille Guémené",
        "slug": "andouille-guemene",
        "price": 22.00,
        "cat": "Bretagne",
        "sub": "Gastronomie Bretonne",
        "img": "andouille-guemene.jpg",
    },
    {
        "name": "Beurre Demi-Sel",
        "slug": "beurre-sale",
        "price": 3.60,
        "cat": "Bretagne",
        "sub": "Apéro & Terroir",
        "img": "beurre-sale.jpg",
    },
    {
        "name": "Pâté Hénaff",
        "slug": "pate-henaff",
        "price": 2.80,
        "cat": "Bretagne",
        "sub": "Apéro & Terroir",
        "img": "pate-henaff.jpg",
    },
    {
        "name": "Coquilles St-Jacques",
        "slug": "coquille-st-jacques",
        "price": 35.00,
        "cat": "Bretagne",
        "sub": "Apéro & Terroir",
        "img": "coquille-st-jacques.jpg",
    },
    {
        "name": "Huîtres Cancale",
        "slug": "huitres-cancale",
        "price": 16.50,
        "cat": "Bretagne",
        "sub": "Apéro & Terroir",
        "img": "huitres-cancale.jpg",
    },
    {
        "name": "Coffret Vendée",
        "slug": "coffret-decouverte-vendeen",
        "price": 39.90,
        "cat": "Idées Cadeaux",
        "sub": "Coffrets Gourmands",
        "img": "coffret-decouverte-vendeen.jpg",
    },
    {
        "name": "Coffret Breton",
        "slug": "coffret-decouverte-breton",
        "price": 39.90,
        "cat": "Idées Cadeaux",
        "sub": "Coffrets Gourmands",
        "img": "coffret-decouverte-breton.jpg",
    },
    {
        "name": "Couteau Huîtres",
        "slug": "couteau-huitres",
        "price": 14.90,
        "cat": "Idées Cadeaux",
        "sub": "Accessoires",
        "img": "couteau-a-huitres.jpg",
    },
]

# 4. Exécution
cat_map = {}
print("📂 Création catégories...")
for main in cats_structure:
    parent = Category(name=main["name"], slug=main["slug"], parent_id=None)
    db.session.add(parent)
    db.session.commit()
    cat_map[main["name"]] = parent.id  # ID du parent

    for sub in main["subcategories"]:
        child = Category(name=sub["name"], slug=sub["slug"], parent_id=parent.id)
        db.session.add(child)
        db.session.commit()
        cat_map[(main["name"], sub["name"])] = child.id  # ID de l'enfant

print("📦 Création produits...")
for p in products_list:
    # On récupère les IDs
    parent_id = cat_map.get(p["cat"])
    child_id = cat_map.get((p["cat"], p["sub"]))

    prod = Product(
        name=p["name"],
        slug=p["slug"],
        brand="Artisanat",
        description="Produit authentique.",
        price=p["price"],
        stock_quantity=50,
        # Ici on lie le produit correctement :
        # category_id = Parent (Vendée), subcategory_id = Enfant (Douceurs)
        category_id=parent_id,
        subcategory_id=child_id,
        image=p["img"],  # Juste le nom du fichier !
    )
    db.session.add(prod)

db.session.commit()
print("✅ Base réparée : Images locales + Catégories correctes.")

# Charger les utilisateurs
print("👥 Chargement des utilisateurs...")
load_users()
print("✅ Utilisateurs chargés.")
