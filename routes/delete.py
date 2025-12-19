from flask import Blueprint, render_template, request, redirect, session
import sqlite3

delete_bp = Blueprint("delete", __name__)
DB = "database.db"

@delete_bp.route("/admin/delete/<product_id>")
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
