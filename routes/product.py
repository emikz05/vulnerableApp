from flask import Blueprint, render_template, request, redirect, session
import sqlite3

product_bp = Blueprint("product", __name__)
DB = "database.db"


@product_bp.route("/product/<int:product_id>", methods=["GET", "POST"])
def product(product_id):
    
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Получаем товар
    cur.execute("""
        SELECT id, name, full_description, price, image
        FROM products
        WHERE id = ?
    """, (product_id,))
    product = cur.fetchone()

    # Добавление review
    if request.method == "POST":
        content = request.form.get("content")
        user_id = session.get("user_id", 1)

        cur.execute(
            "INSERT INTO comments (product_id, user_id, content) VALUES (?, ?, ?)",
            (product_id, user_id, content)
        )
        conn.commit()
        return redirect(f"/product/{product_id}")

    # Получаем reviews
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
        title=product[1],
        product={
            "id": product[0],
            "name": product[1],
            "desc": product[2],
            "price": product[3],
            "image": product[4]
        },
        comments=[{"user": c[0], "text": c[1]} for c in comments]
    )
