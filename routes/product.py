from flask import Blueprint, render_template, request, redirect, session
import sqlite3

product_bp = Blueprint("product", __name__)
DB = "database.db"


@product_bp.route("/product/<product_id>", methods=["GET", "POST"])
def product(product_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    if request.method == "POST":
        content = request.form.get("content")
        user_id = session.get("user_id")

        if content and user_id:
            cur.execute(
                "INSERT INTO comments (product_id, user_id, content) VALUES (?, ?, ?)",
                (product_id, user_id, content)
            )
            conn.commit()

        return redirect(f"/product/{product_id}")

    cur.execute("""
        SELECT id, name, full_description, price, image
        FROM products
        WHERE id = ?
    """, (product_id,))
    product = cur.fetchone()

    if not product:
        conn.close()
        return "Product not found", 404

    cur.execute("""
        SELECT users.username, comments.content
        FROM comments
        JOIN users ON users.id = comments.user_id
        WHERE comments.product_id = ?
    """, (product_id,))
    comments = cur.fetchall()

    conn.close()

    return render_template(
        "product.html",
        product={
            "id": product[0],
            "name": product[1],
            "desc": product[2],
            "price": product[3],
            "image": product[4]
        },
        comments=[{"user": c[0], "text": c[1]} for c in comments]
    )
