from flask import Blueprint, render_template, session, redirect
import sqlite3

profile_bp = Blueprint("profile", __name__)
DB = "database.db"

@profile_bp.route("/profile")
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