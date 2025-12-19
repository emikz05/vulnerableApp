from flask import Blueprint, render_template, request, redirect, session
import sqlite3

edit_bp = Blueprint("edit", __name__)
DB = "database.db"
@edit_bp.route("/admin/edit/<product_id>", methods=["GET", "POST"])
def admin_edit_product(product_id):
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

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

