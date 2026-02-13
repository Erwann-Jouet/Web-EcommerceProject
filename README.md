# 🛍️ MonShop - E-commerce Flask

> Modern e-commerce application built with Flask and SQLAlchemy

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.25-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Detailed Installation](#-detailed-installation)
- [Project Structure](#-project-structure)
- [Data Models](#-data-models)
- [Documentation](#-documentation)

---

## 📖 About

**MonShop** is a complete e-commerce application with:

- 🛍️ Product catalog management with categories and subcategories
- 🛒 Dynamic shopping cart system
- 👤 Multi-role authentication (admin, manager, customer)
- 💾 Relational database with SQLAlchemy ORM
- 📱 Responsive interface
- 🔍 Advanced search and filters

**Tech Stack:** Flask, SQLAlchemy, Jinja2, SQLite

---

## ✨ Features

### 🛍️ Catalog

- Navigation by categories and subcategories
- Product search
- Filtering by brand and price
- Detailed product pages

### 🛒 Cart

- Add/remove items
- Modify quantities
- Session-based cart persistence

### 👤 Authentication

- Registration and login
- User profile management
- User roles (admin, manager, customer)

### 💾 Database

- SQLite (development)
- Models with SQLAlchemy ORM
- Data fixtures for testing

---

## 🚀 Quick Start

### ⚡ Option 1: Automated Script (Recommended)

```bash
# Clone the project
git clone https://github.com/your-username/your-repo.git
cd tp-projet

# Install and launch
./setup.sh
```

**➜** The application will be accessible at <http://localhost:5000>

---

## 📁 Project Structure

```
tp-projet/
├── 📄 app.py                   # Main Flask application
├── 📄 run.py                   # Launch script
├── 📄 config.py                # Application configuration
├── 📄 setup.sh                 # Automated installation script
├── 📄 pyproject.toml           # Dependencies and configuration
│
├── 📂 src/                     # Source code
│   ├── 📂 models/              # Data models (SQLAlchemy)
│   │   ├── category.py
│   │   ├���─ product.py
│   │   ├── user.py
│   │   ├── cart.py
│   │   └── cart_item.py
│   │
│   ├── 📂 auth/                # Authentication
│   │   ├── routes.py
│   │   └── utils.py
│   │
│   ├── 📂 catalog/             # Product catalog
│   │   └── routes.py
│   │
│   ├── 📂 cart/                # Shopping cart
│   │   ├── routes.py
│   │   └── services.py
│   │
│   ├── 📂 api/                 # REST API
│   │   └── routes.py
│   │
│   └── 📂 templates/           # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       └── cart/
│
├── 📂 static/                  # Static files
│   ├── css/
│   ├── js/
│   └── img/
│
└── 📂 datafixtures/            # Test data
    ├── import_all.py
    └── json/
        ├── categories.json
        ├── products.json
        └── users.json
```

---

## 💾 Data Models

The project uses **SQLAlchemy** with **SQLite** and provides five main models:

### 📦 Category

Represents product categories and subcategories with a parent-child relationship.

**Fields:**

- `id`: Unique identifier
- `name`: Category name
- `slug`: URL-friendly identifier
- `parent_id`: Reference to parent category

**Relationships:**

- `parent`: Parent category
- `children`: Subcategories

### 🏷️ Product

Represents catalog products.

**Fields:**

- `id`, `name`, `slug`, `brand`
- `description`, `price`
- `category_id`, `subcategory_id`
- `image_url`, `stock_quantity`

**Relationships:**

- `category`: Main category
- `subcategory`: Subcategory (optional)

### 👤 User

Represents site users.

**Fields:**

- `id`, `username`, `password`, `email`
- `role`: admin, manager, customer
- `adresse`, `code_postal`, `ville`, `pays`

### 🛒 Cart & CartItem

Shopping cart management.

**Cart:**

- `id`, `user_id`, `created_at`, `updated_at`

**CartItem:**

- `id`, `cart_id`, `product_id`, `quantity`

---

## 🛠️ Technologies Used

| Technology | Version | Usage |
|-------------|---------|-------|
| **Python** | 3.8+ | Main language |
| **Flask** | 3.0.0 | Web framework |
| **SQLAlchemy** | 2.0.25 | Database ORM |
| **Flask-SQLAlchemy** | 3.1.1 | SQLAlchemy integration |
| **Jinja2** | - | Template engine |
| **SQLite** | - | Database |

---

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - 5-minute installation
- **[Project Information](PROJET_INFO.md)** - Complete overview
- **[Configuration](config.py)** - Application settings

### External Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

---

## 👨‍💻 Author

**Erwann Jouet**

- GitHub: [@Erwann-Jouet](https://github.com/Erwann-Jouet)

---

**⭐ Feel free to star this project if you like it!**

**Happy coding! 🚀**