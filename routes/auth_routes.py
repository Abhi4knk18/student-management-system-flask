from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import user_model as users

auth_bp = Blueprint("auth", __name__)

# ---------- LOGIN ----------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        role = users.authenticate(username, password)
        if role:
            session["user"] = username
            session["role"] = role
            flash("Login successful", "success")
            return redirect(url_for("student.index"))

        flash("Invalid credentials", "error")

    return render_template("login.html")


# ---------- LOGOUT ----------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "success")
    return redirect(url_for("auth.login"))


# ---------- SIGNUP ----------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        from models.user_model import create_user
        create_user(username, password, "user")

        session["user"] = username
        session["role"] = "user"

        flash("Account created & logged in", "success")
        return redirect(url_for("student.index"))

    return render_template("signup.html")


# ---------- PROFILE ----------
@auth_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        old = request.form["old_password"]
        new = request.form["new_password"]

        if users.change_password(session["user"], old, new):
            flash("Password updated successfully", "success")
        else:
            flash("Old password incorrect", "error")

    return render_template("profile.html")


# ---------- FORGOT PASSWORD (SAFE PLACEHOLDER) ----------
@auth_bp.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")
