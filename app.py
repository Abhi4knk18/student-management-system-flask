from flask import Flask
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp

app = Flask(__name__)

# 🔐 REQUIRED FOR SESSION & FLASH
app.secret_key = "super-secret-key"   # you can change later

# ---------- REGISTER BLUEPRINTS ----------
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
