from flask import Blueprint, render_template, session, redirect
import sqlite3

dashboard_bp = Blueprint("dashboard", __name__)
DB = "database.db"


@dashboard_bp.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, short_description, price, image
        FROM products
    """)
    products = cur.fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        title="Shop",
        products=[
            {
                "id": p[0],
                "name": p[1],
                "short": p[2],
                "price": p[3],
                "image": p[4]
            }
            for p in products
        ]
    )
