from flask import Flask, redirect

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.product import product_bp
from routes.profile import profile_bp

app = Flask(__name__)
app.secret_key = "secretkey"
app.secret_key = "super-secret-key-change-me"

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(product_bp)
app.register_blueprint(profile_bp)




@app.route("/")
def home():
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
