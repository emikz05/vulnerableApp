from flask import Blueprint, render_template, request, redirect, session
import sqlite3

auth_bp = Blueprint("auth", __name__)
DB = "database.db"


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template(
                "login.html",
                title="Login",
                error="Username and password are required"
            )

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        query = f"""
        SELECT id, username, role FROM users
        WHERE username = '{username}'
        AND password = '{password}'
        """
        cur.execute(query)
        user = cur.fetchone()

        conn.close()

        if not user:
            return render_template(
                "login.html",
                title="Login",
                error="Invalid username or password"
            )

        session["user_id"] = user[0]
        session["username"] = user[1]
        session["role"] = user[2] 
        return redirect("/dashboard")

    return render_template("login.html", title="Login")



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not password or not confirm_password:
            return render_template(
                "register.html",
                title="Sign up",
                error="All fields are required"
            )

        if password != confirm_password:
            return render_template(
                "register.html",
                title="Sign up",
                error="Passwords do not match"
            )

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute(
            f"SELECT id FROM users WHERE username = '{username}'"
        )
        existing_user = cur.fetchone()

        if existing_user:
            conn.close()
            return render_template(
                "register.html",
                title="Sign up",
                error="Username already exists"
            )

        cur.execute(
            f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        )

        conn.commit()
        conn.close()

        return redirect("/login?success=1")

    return render_template("register.html", title="Sign up")



@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@auth_bp.route("/admin")
def admin():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT id, name, price FROM products")
    products = [
        {"id": p[0], "name": p[1], "price": p[2]}
        for p in cur.fetchall()
    ]

    conn.close()

    return render_template(
        "admin.html",
        products=products
    )


@auth_bp.route("/admin")
def admin_panel():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, price
        FROM products
    """)
    products = cur.fetchall()
    conn.close()

    return render_template(
        "admin.html",
        products=products
    )


@auth_bp.route("/admin/delete/<int:product_id>")
def delete_product(product_id):
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )
    conn.commit()
    conn.close()

    return redirect("/admin")

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/images"

@auth_bp.route("/admin/add", methods=["GET", "POST"])
def admin_add_product():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        short = request.form["short"]
        full = request.form["full"]
        price = request.form["price"]

        image_file = request.files["image"]
        filename = secure_filename(image_file.filename)

        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(image_path)

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO products (name, short_description, full_description, price, image)
            VALUES (?, ?, ?, ?, ?)
        """, (name, short, full, price, filename))

        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("admin_add.html")

@auth_bp.route("/admin/edit/<int:product_id>", methods=["GET", "POST"])
def admin_edit_product(product_id):
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # SAVE CHANGES
    if request.method == "POST":
        name = request.form["name"]
        short = request.form["short"]
        full = request.form["full"]
        price = request.form["price"]

        image_file = request.files.get("image")
        image_name = request.form.get("current_image")

        if image_file and image_file.filename:
            from werkzeug.utils import secure_filename
            import os

            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join("static/images", filename))
            image_name = filename

        cur.execute("""
            UPDATE products
            SET name = ?, short_description = ?, full_description = ?, price = ?, image = ?
            WHERE id = ?
        """, (name, short, full, price, image_name, product_id))

        conn.commit()
        conn.close()

        return redirect("/admin")

    # LOAD PRODUCT
    cur.execute("""
        SELECT name, short_description, full_description, price, image
        FROM products
        WHERE id = ?
    """, (product_id,))
    product = cur.fetchone()
    conn.close()

    return render_template(
        "admin_edit.html",
        product={
            "id": product_id,
            "name": product[0],
            "short": product[1],
            "full": product[2],
            "price": product[3],
            "image": product[4]
        }
    )

@auth_bp.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect("/login")

    user = {
        "username": session.get("username"),
        "role": session.get("role")
    }

    admin_stats = None

    if session.get("role") == "admin":
        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM products")
        products_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM users")
        users_count = cur.fetchone()[0]

        conn.close()

        admin_stats = {
            "products": products_count,
            "users": users_count
        }

    return render_template(
        "profile.html",
        user=user,
        admin_stats=admin_stats
    )
