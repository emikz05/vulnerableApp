from flask import Blueprint, render_template, request, redirect, session
import sqlite3

admin_bp = Blueprint("admin", __name__)
DB = "database.db"
@admin_bp.route("/admin")
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