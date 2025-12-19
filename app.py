from flask import Flask, redirect

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.product import product_bp
from routes.profile import profile_bp
from routes.edit import edit_bp
from routes.addp import addp_bp
from routes.delete import delete_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.secret_key = "secretkey"

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(product_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(edit_bp)
app.register_blueprint(addp_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def home():
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
