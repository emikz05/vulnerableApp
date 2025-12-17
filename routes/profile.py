from flask import Blueprint, render_template, session, redirect
import sqlite3

profile_bp = Blueprint("profile", __name__)
DB = "database.db"


@profile_bp.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT username FROM users WHERE id = ?",
        (session["user_id"],)
    )
    user = cur.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        title="My Profile",
        user={"username": user[0]}
    )
