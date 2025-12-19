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

        query = f""" SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}' """
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
            f"""
            INSERT INTO users (username, password, role)
            VALUES ('{username}', '{password}', 'user')
            """
        )


        conn.commit()
        conn.close()

        return redirect("/login?success=1")

    return render_template("register.html", title="Sign up")



@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

