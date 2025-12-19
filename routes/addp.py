from flask import Blueprint, render_template, request, redirect, session
import sqlite3, os

addp_bp = Blueprint("addp", __name__)
DB = "database.db"
UPLOAD_FOLDER = 'static/images'

@addp_bp.route("/admin/add", methods=["GET", "POST"])
def admin_add_product():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        short = request.form["short"]
        full = request.form["full"]
        price = request.form["price"]

        file = request.files["image"]
        filename = file.filename
        filepath= os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        owner_id = session.get("user_id")

        cur.execute("""
            INSERT INTO products 
            (name, short_description, full_description, price, image, owner_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (name, short, full, price, filename, owner_id))

        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("admin_add.html")