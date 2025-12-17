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

            # Redirect to DASHBOARD (not home)
            return redirect(url_for("student.index"))

        flash("Invalid credentials", "error")

    return render_template("login.html")


# ---------- LOGOUT ----------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "success")

    # After logout, go to LOGIN (not dashboard)
    return redirect(url_for("auth.login"))


# ---------- SIGNUP ----------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        from models.user_model import create_user
        create_user(username, password, "user")

        # AUTO LOGIN AFTER SIGNUP
        session["user"] = username
        session["role"] = "user"

        flash("Account created & logged in", "success")

        # Redirect to DASHBOARD
        return redirect(url_for("student.index"))

    return render_template("signup.html")



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
